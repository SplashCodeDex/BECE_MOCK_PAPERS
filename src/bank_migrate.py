"""Phase 1 migration: legacy extracted_questions -> canonical bank tables.

- Seeds the `sources` registry from harvested_files domains (Q6).
- Deduplicates questions by normalized text (+ options for MCQs).
- Preserves every raw appearance in `question_occurrences` with full provenance
  (harvested file id, original URL, source registry entry).
- Routes answer conflicts to `tag_review_queue` for human review (Q3).
"""

import hashlib
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.bank_schema import init_bank_schema
from src.config import DATABASE_PATH

# Source classification by domain: official bodies first, then known teacher hubs.
OFFICIAL_DOMAINS = {"waecgh.org", "ghana.waecdirect.org"}
CURRICULUM_DOMAINS = {"ges.gov.gh", "nacca.gov.gh", "curriculumforum.gov.gh"}
LEGACY_SOURCE_NAME = "Legacy crawl (pre-curation harvest)"


def _classify_domain(domain: str) -> str:
    d = domain.lower().removeprefix("www.")
    if d in OFFICIAL_DOMAINS:
        return "waec_official"
    if d in CURRICULUM_DOMAINS:
        return "ges_curriculum"
    return "mock_compilation"


def normalize_for_dedup(row: sqlite3.Row) -> str:
    """Canonical form of a question for duplicate detection.

    Lowercased, whitespace/punctuation-collapsed text; for MCQs the options
    are included so identical stems with different options stay distinct.
    """
    parts = [row["question_text"] or ""]
    if row["paper_type"] and "objective" in row["paper_type"].lower():
        parts += [row[f"option_{c}"] or "" for c in "abcd"]
    joined = " ".join(parts).lower()
    joined = re.sub(r"[^a-z0-9]+", " ", joined)
    return re.sub(r"\s+", " ", joined).strip()


def dedup_hash(row: sqlite3.Row) -> str:
    subject = (row["subject"] or "").lower().strip()
    payload = f"{subject}|{normalize_for_dedup(row)}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _pick_best(current: Optional[Dict[str, Any]], candidate: Dict[str, Any]) -> Dict[str, Any]:
    """Merge duplicate rows: prefer the one with an answer, then a year."""
    if current is None:
        return dict(candidate)
    merged = dict(current)
    for key in ("correct_answer", "year", "diagram_path"):
        if not merged.get(key) and candidate.get(key):
            merged[key] = candidate[key]
    return merged


def migrate(db_path: Path = DATABASE_PATH, dry_run: bool = False) -> Dict[str, int]:
    init_bank_schema(db_path)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON;")
    stats = {
        "legacy_rows": 0,
        "canonical_questions": 0,
        "duplicates_merged": 0,
        "occurrences": 0,
        "sources_seeded": 0,
        "answer_conflicts": 0,
    }

    # 1. Seed sources registry from harvested_files domains.
    domains = conn.execute(
        "SELECT DISTINCT source_domain FROM harvested_files ORDER BY source_domain;"
    ).fetchall()
    domain_to_source_id: Dict[str, int] = {}
    for d in domains:
        domain = d["source_domain"]
        cur = conn.execute(
            "INSERT OR IGNORE INTO sources (name, domain, source_type, acquisition, tos_notes) "
            "VALUES (?, ?, ?, 'legacy_crawl', ?);",
            (
                LEGACY_SOURCE_NAME if _classify_domain(domain) != "waec_official" else "WAEC Ghana official",
                domain,
                _classify_domain(domain),
                "Harvested pre-curation; private study use only, not redistributed.",
            ),
        )
        if cur.rowcount:
            stats["sources_seeded"] += 1
        row = conn.execute("SELECT id FROM sources WHERE domain = ?;", (domain,)).fetchone()
        domain_to_source_id[domain] = row["id"]

    file_provenance = {
        r["file_name"]: r
        for r in conn.execute(
            "SELECT id, file_name, original_url, source_domain FROM harvested_files;"
        )
    }

    # 2. Dedup pass over legacy extracted_questions.
    legacy = conn.execute("SELECT * FROM extracted_questions ORDER BY id;").fetchall()
    stats["legacy_rows"] = len(legacy)
    canonical: Dict[str, Dict[str, Any]] = {}
    occurrence_plan: List[Tuple[str, sqlite3.Row, Optional[Dict[str, Any]]]] = []
    for row in legacy:
        h = dedup_hash(row)
        occurrence_plan.append((h, row, file_provenance.get(row["source_file"])))
        canonical[h] = _pick_best(canonical.get(h), dict(row))

    # 3. Answer-conflict detection per dedup group.
    groups: Dict[str, List[sqlite3.Row]] = {}
    for row in legacy:
        groups.setdefault(dedup_hash(row), []).append(row)

    now = datetime.now(timezone.utc).isoformat()
    try:
        with conn:
            for h, best in canonical.items():
                qid = f"Q_{h[:12]}"
                conn.execute(
                    """
                    INSERT OR IGNORE INTO questions (
                        id, subject, question_text, option_a, option_b, option_c, option_d,
                        correct_answer, has_diagram, diagram_path, year, paper_type,
                        dedup_hash, migrated_from, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        qid, best["subject"], best["question_text"],
                        best["option_a"], best["option_b"], best["option_c"], best["option_d"],
                        best["correct_answer"], best["has_diagram"], best["diagram_path"],
                        best["year"], best["paper_type"], h, best["id"], now,
                    ),
                )

            for h, row, prov in occurrence_plan:
                qid = f"Q_{h[:12]}"
                stats["occurrences"] += 1
                source_id = None
                harvested_id = None
                url = None
                if prov:
                    harvested_id = prov["id"]
                    url = prov["original_url"]
                    source_id = domain_to_source_id.get(prov["source_domain"])
                conn.execute(
                    """
                    INSERT OR IGNORE INTO question_occurrences (
                        question_id, original_id, source_file, harvested_file_id,
                        source_id, original_url, year, paper_type, question_number, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        qid, row["id"], row["source_file"], harvested_id,
                        source_id, url, row["year"], row["paper_type"],
                        row["question_number"], now,
                    ),
                )

            for h, rows in groups.items():
                answers = {
                    (r["correct_answer"] or "").strip().upper()
                    for r in rows
                    if (r["correct_answer"] or "").strip()
                }
                if len(answers) > 1:
                    stats["answer_conflicts"] += 1
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO tag_review_queue (question_id, reason, details, created_at)
                        VALUES (?, 'answer_conflict', ?, ?);
                        """,
                        (f"Q_{h[:12]}", f"Dedup group disagrees on answer: {sorted(answers)}", now),
                    )

            stats["canonical_questions"] = conn.execute(
                "SELECT COUNT(*) FROM questions;"
            ).fetchone()[0]
            stats["duplicates_merged"] = stats["legacy_rows"] - stats["canonical_questions"]

            if dry_run:
                conn.rollback()
            else:
                # 4. Build the FTS index after bulk insert.
                conn.execute("INSERT INTO questions_fts (questions_fts) VALUES ('rebuild');")
    finally:
        conn.close()

    return stats
