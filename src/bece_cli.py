"""Cross-Repo BECE Question Bank CLI (`src/bece_cli.py`).

Designed to be invoked by AI tutor agents in `Grade9-Maths` and `Grade9-Computing`
(or directly from any terminal) with zero background daemon overhead.

Examples:
    python w:/StaralexSchoolStudies/BECE_MOCK_PAPERS/src/bece_cli.py query --indicator B9.1.1.2.2 --subject Mathematics
    python w:/StaralexSchoolStudies/BECE_MOCK_PAPERS/src/bece_cli.py search "rationalise surd denominator" --subject Mathematics
    python w:/StaralexSchoolStudies/BECE_MOCK_PAPERS/src/bece_cli.py save-solution --id Q_123456789abc --lesson "Lesson-04-Surds" --answer "(sqrt(3)+1)/2" --sympy-lhs "1/(sqrt(3)-1)" --sympy-rhs "(sqrt(3)+1)/2" --steps "Step 1: Multiply numerator and denominator by conjugate..."
    python w:/StaralexSchoolStudies/BECE_MOCK_PAPERS/src/bece_cli.py stats
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
import sqlite3
import sys
from typing import Any, Dict, List, Optional

# Ensure repo root is on sys.path when invoked from sibling learning repos
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.bank_schema import init_bank_schema
from src.config import DATABASE_PATH
from src.verifier import verify_solution


def _get_conn(db_path: Path = DATABASE_PATH) -> sqlite3.Connection:
    init_bank_schema(db_path)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def _enrich_questions(conn: sqlite3.Connection, rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
    """Attach provenance occurrences and cached worked solutions to question rows."""
    results: List[Dict[str, Any]] = []
    for r in rows:
        d = dict(r)
        d.pop("embedding", None)
        qid = d["id"]

        occs = conn.execute(
            """
            SELECT original_id, source_file, original_url, year, paper_type, question_number
            FROM question_occurrences
            WHERE question_id = ?
            ORDER BY year DESC, id ASC;
            """,
            (qid,),
        ).fetchall()
        d["occurrences"] = [dict(o) for o in occs]

        sols = conn.execute(
            """
            SELECT id, lesson_id, indicator_code, step_by_step_markdown,
                   final_answer, verification_type, verification_details, created_at
            FROM solutions
            WHERE question_id = ?
            ORDER BY created_at DESC;
            """,
            (qid,),
        ).fetchall()
        d["solutions"] = [dict(s) for s in sols]
        results.append(d)
    return results


def _format_questions_markdown(
    items: List[Dict[str, Any]],
    header: str,
    canonical_diagrams: Optional[List[Dict[str, Any]]] = None,
) -> str:
    lines: List[str] = [f"# {header}", f"**Total Questions Returned:** {len(items)}", ""]
    if canonical_diagrams:
        lines.append("### Canonical Diagram Templates Available:")
        for d in canonical_diagrams:
            png_abs = (REPO_ROOT / d["png_file"]).as_posix()
            skill_abs = (REPO_ROOT / d["skill_file"]).as_posix()
            lines.append(
                f"- **Diagram {d['id']:02d}:** [{d['name']}](file:///{png_abs}) — *{d['topic']}* | Skill: [{d['skill']}](file:///{skill_abs})"
            )
        lines.append("")
    for idx, q in enumerate(items, 1):
        ind_str = q.get("indicator_code") or "UNMAPPED"
        sub_title = q.get("substrand_title") or ""
        conf = q.get("confidence") or 0.0
        yr = q.get("year") or "N/A"
        pt = q.get("paper_type") or "N/A"
        lines.append(
            f"## {idx}. `{q['id']}` — [{q['subject']}] `{ind_str}` {f'({sub_title})' if sub_title else ''}"
        )
        lines.append(
            f"- **Year / Paper:** {yr} ({pt}) | **Tag Confidence:** `{conf:.2f}` (`{q.get('tag_method') or 'n/a'}`)"
        )
        if q.get("has_diagram") and q.get("diagram_path"):
            cand_diag = REPO_ROOT / q["diagram_path"]
            if not cand_diag.exists():
                cand_diag = REPO_ROOT / "data" / q["diagram_path"]
            abs_diag = cand_diag.as_posix()
            lines.append(f"- **Diagram:** [{Path(q['diagram_path']).name}](file:///{abs_diag})")
        if q.get("occurrences"):
            occ0 = q["occurrences"][0]
            lines.append(
                f"- **Provenance:** `{occ0['source_file']}` ({len(q['occurrences'])} occurrence(s) in bank)"
            )
        lines.append("")
        lines.append(q["question_text"])
        lines.append("")
        for letter, col in [("A", "option_a"), ("B", "option_b"), ("C", "option_c"), ("D", "option_d")]:
            if q.get(col):
                lines.append(f"- **{letter}.** {q[col]}")
        if q.get("correct_answer"):
            lines.append(f"\n**Official Key:** `{q['correct_answer']}`")
        if q.get("solutions"):
            for sol in q["solutions"]:
                lines.append(
                    f"\n### Cached Worked Solution (`{sol['lesson_id']}` — `{sol['verification_type']}`)"
                )
                lines.append(sol["step_by_step_markdown"])
                lines.append(f"\n**Verified Final Answer:** `{sol['final_answer']}`")
        lines.append("\n---\n")
    return "\n".join(lines)


def cmd_query(args: argparse.Namespace, db_path: Path = DATABASE_PATH) -> int:
    with _get_conn(db_path) as conn:
        target_codes: List[str] = []
        if args.indicator:
            code_in = args.indicator.strip().upper()
            # Match exact indicator or prefix (e.g. B9.1.1.2 matches B9.1.1.2.1, B9.1.1.2.2)
            sql_ind = "SELECT code, subject, prerequisite_codes FROM curriculum_indicators WHERE code = ? OR code LIKE ?"
            params_ind: List[Any] = [code_in, f"{code_in}.%"]
            if args.subject:
                sql_ind += " AND subject = ?"
                params_ind.append(args.subject)
            ind_rows = conn.execute(sql_ind, params_ind).fetchall()
            for r in ind_rows:
                if r["code"] not in target_codes:
                    target_codes.append(r["code"])
                if args.include_prerequisites and r["prerequisite_codes"]:
                    try:
                        prereqs = json.loads(r["prerequisite_codes"])
                        for p in prereqs:
                            if p not in target_codes:
                                target_codes.append(p)
                    except Exception:
                        pass
            if not target_codes:
                target_codes.append(code_in)

        sql = """
            SELECT q.*, ci.grade AS indicator_grade, ci.strand_title, ci.substrand_title, ci.indicator_text
            FROM questions q
            LEFT JOIN curriculum_indicators ci
              ON ci.subject = q.subject AND ci.code = q.indicator_code
        """
        clauses: List[str] = []
        params: List[Any] = []

        if target_codes:
            placeholders = ",".join("?" for _ in target_codes)
            clauses.append(f"q.indicator_code IN ({placeholders})")
            params.extend(target_codes)
        if args.subject:
            clauses.append("q.subject = ?")
            params.append(args.subject)
        if args.paper_type:
            clauses.append("q.paper_type LIKE ?")
            params.append(f"%{args.paper_type}%")
        else:
            clauses.append("COALESCE(q.paper_type, '') != 'Marking Scheme / Solutions'")
            clauses.append("COALESCE(q.confidence, 0.0) >= 0.50")
        if args.has_diagram is not None:
            clauses.append("q.has_diagram = ?")
            params.append(1 if args.has_diagram else 0)

        if clauses:
            sql += " WHERE " + " AND ".join(clauses)

        # Order exact requested indicator first, then highest confidence, then most recent year
        if args.indicator:
            sql += " ORDER BY CASE WHEN q.indicator_code LIKE ? THEN 0 ELSE 1 END, q.confidence DESC, COALESCE(q.year, 0) DESC LIMIT ?;"
            params.extend([f"{args.indicator.strip().upper()}%", args.limit])
        else:
            sql += " ORDER BY q.confidence DESC, COALESCE(q.year, 0) DESC LIMIT ?;"
            params.append(args.limit)

        rows = conn.execute(sql, params).fetchall()
        items = _enrich_questions(conn, rows)

    if args.format == "json":
        print(json.dumps({"target_indicators": target_codes, "count": len(items), "questions": items}, indent=2))
    else:
        diag_items = []
        if args.indicator:
            from src.curriculum_taxonomy import get_diagrams_for_indicator
            diag_items = get_diagrams_for_indicator(args.indicator, subject=args.subject or "Mathematics")

        hdr = f"BECE Question Bank Query ({', '.join(target_codes) if target_codes else (args.subject or 'All')})"
        print(_format_questions_markdown(items, hdr, canonical_diagrams=diag_items))
    return 0


def cmd_search(args: argparse.Namespace, db_path: Path = DATABASE_PATH) -> int:
    with _get_conn(db_path) as conn:
        has_emb = conn.execute(
            "SELECT COUNT(*) FROM questions WHERE embedding IS NOT NULL;"
        ).fetchone()[0]

    if has_emb > 0 and not args.fts_only:
        from src.tagger import CurriculumTagger

        tagger = CurriculumTagger(db_path=db_path)
        raw_hits = tagger.semantic_search(
            query=args.query_text,
            subject=args.subject,
            indicator_code=args.indicator,
            limit=args.limit,
        )
        with _get_conn(db_path) as conn:
            qids = [h["id"] for h in raw_hits]
            if qids:
                placeholders = ",".join("?" for _ in qids)
                rows_by_id = {
                    r["id"]: r
                    for r in conn.execute(
                        f"""
                        SELECT q.*, ci.grade AS indicator_grade, ci.strand_title, ci.substrand_title, ci.indicator_text
                        FROM questions q
                        LEFT JOIN curriculum_indicators ci
                          ON ci.subject = q.subject AND ci.code = q.indicator_code
                        WHERE q.id IN ({placeholders});
                        """,
                        qids,
                    ).fetchall()
                }
                ordered_rows = [rows_by_id[qid] for qid in qids if qid in rows_by_id]
                items = _enrich_questions(conn, ordered_rows)
                for item, hit in zip(items, raw_hits):
                    item["search_score"] = hit.get("search_score")
            else:
                items = []
    else:
        # Fast FTS5 / LIKE search fallback if embeddings haven't been computed yet
        with _get_conn(db_path) as conn:
            tokens = [t for t in args.query_text.strip().split() if len(t) >= 2]
            fts_expr = " OR ".join(f'"{t}"' for t in tokens) if tokens else args.query_text
            sql = """
                SELECT q.*, ci.grade AS indicator_grade, ci.strand_title, ci.substrand_title, ci.indicator_text
                FROM questions_fts f
                JOIN questions q ON q.rowid = f.rowid
                LEFT JOIN curriculum_indicators ci
                  ON ci.subject = q.subject AND ci.code = q.indicator_code
                WHERE questions_fts MATCH ?
            """
            params: List[Any] = [fts_expr]
            if args.subject:
                sql += " AND q.subject = ?"
                params.append(args.subject)
            if args.indicator:
                sql += " AND q.indicator_code = ?"
                params.append(args.indicator)
            sql += " ORDER BY rank LIMIT ?;"
            params.append(args.limit)
            rows = conn.execute(sql, params).fetchall()
            items = _enrich_questions(conn, rows)

    if args.format == "json":
        print(json.dumps({"query": args.query_text, "count": len(items), "questions": items}, indent=2))
    else:
        print(_format_questions_markdown(items, f"Search Results for: `{args.query_text}`"))
    return 0


def cmd_save_solution(args: argparse.Namespace, db_path: Path = DATABASE_PATH) -> int:
    steps_md = ""
    if args.file:
        steps_md = Path(args.file).read_text(encoding="utf-8")
    elif args.steps:
        steps_md = args.steps
    else:
        print("Error: Provide either --steps or --file with the worked solution markdown.", file=sys.stderr)
        return 2

    with _get_conn(db_path) as conn:
        q_row = conn.execute("SELECT * FROM questions WHERE id = ?;", (args.id,)).fetchone()
        if q_row is None:
            print(f"Error: Question ID '{args.id}' not found in `questions`.", file=sys.stderr)
            return 2

        q_dict = dict(q_row)
        ver = verify_solution(
            question_row=q_dict,
            step_by_step_markdown=steps_md,
            final_answer=args.answer,
            sympy_lhs=args.sympy_lhs,
            sympy_rhs=args.sympy_rhs,
        )

        if not ver.passed and not args.force:
            print(
                json.dumps(
                    {
                        "status": "verification_failed",
                        "question_id": args.id,
                        "verification_type": ver.verification_type,
                        "details": ver.details,
                    },
                    indent=2,
                ),
                file=sys.stderr,
            )
            return 1

        sol_id = "SOL_" + hashlib.sha256(f"{args.id}::{args.lesson}".encode("utf-8")).hexdigest()[:12]
        indicator_code = args.indicator or q_dict.get("indicator_code") or "UNMAPPED"

        conn.execute(
            """
            INSERT INTO solutions (
                id, question_id, lesson_id, indicator_code,
                step_by_step_markdown, final_answer,
                verification_type, verification_details
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(question_id, lesson_id) DO UPDATE SET
                indicator_code = excluded.indicator_code,
                step_by_step_markdown = excluded.step_by_step_markdown,
                final_answer = excluded.final_answer,
                verification_type = excluded.verification_type,
                verification_details = excluded.verification_details,
                created_at = CURRENT_TIMESTAMP;
            """,
            (
                sol_id,
                args.id,
                args.lesson,
                indicator_code,
                steps_md,
                ver.normalized_answer or args.answer.strip(),
                ver.verification_type,
                ver.details,
            ),
        )
        conn.commit()

    print(
        json.dumps(
            {
                "status": "saved",
                "solution_id": sol_id,
                "question_id": args.id,
                "lesson_id": args.lesson,
                "indicator_code": indicator_code,
                "verification_type": ver.verification_type,
                "verification_details": ver.details,
            },
            indent=2,
        )
    )
    return 0


def cmd_indicators(args: argparse.Namespace, db_path: Path = DATABASE_PATH) -> int:
    with _get_conn(db_path) as conn:
        sql = """
            SELECT ci.uid, ci.subject, ci.grade, ci.code, ci.strand_number, ci.strand_title,
                   ci.substrand_number, ci.substrand_title, ci.indicator_text, ci.prerequisite_codes,
                   COUNT(q.id) AS question_count
            FROM curriculum_indicators ci
            LEFT JOIN questions q ON q.subject = ci.subject AND q.indicator_code = ci.code
        """
        clauses: List[str] = []
        params: List[Any] = []
        if args.subject:
            clauses.append("ci.subject = ?")
            params.append(args.subject)
        if args.grade:
            clauses.append("ci.grade = ?")
            params.append(args.grade.upper())
        if args.search:
            clauses.append("(ci.code LIKE ? OR ci.substrand_title LIKE ? OR ci.indicator_text LIKE ?)")
            pat = f"%{args.search}%"
            params.extend([pat, pat, pat])
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " GROUP BY ci.uid ORDER BY ci.subject, ci.grade, ci.code;"
        rows = [dict(r) for r in conn.execute(sql, params).fetchall()]

    if args.format == "json":
        print(json.dumps({"count": len(rows), "indicators": rows}, indent=2))
    else:
        for r in rows:
            print(
                f"{r['uid']} ({r['grade']}) [{r['question_count']} q] — {r['strand_title']} > {r['substrand_title']}: {r['indicator_text'][:110]}"
            )
    return 0


def _resolve_topic_indicators(
    conn: sqlite3.Connection,
    topic: str,
    subject: Optional[str] = None,
) -> tuple[str, List[Dict[str, Any]]]:
    """Map a learning-topic name to curriculum indicator rows.

    Source of truth is the official substrand title (e.g. \"Algebraic Expressions\").
    Falls back to substring match on substrand / strand / indicator text.
    """
    where: List[str] = []
    params: List[Any] = []
    if subject:
        where.append("subject = ?")
        params.append(subject)

    def _run(match_sql: str, match_params: List[Any]) -> List[Dict[str, Any]]:
        sql = (
            "SELECT uid, code, grade, subject, strand_title, substrand_title, indicator_text "
            "FROM curriculum_indicators WHERE " + match_sql
        )
        if where:
            sql += " AND " + " AND ".join(where)
        sql += " ORDER BY grade, code"
        return [dict(r) for r in conn.execute(sql, [*match_params, *params]).fetchall()]

    rows = _run("substrand_title = ?", [topic])
    if rows:
        return "substrand_exact", rows
    rows = _run(
        "(substrand_title LIKE ? OR strand_title LIKE ? OR indicator_text LIKE ?)",
        [f"%{topic}%"] * 3,
    )
    return ("substring" if rows else "unresolved"), rows


def _list_topics(conn: sqlite3.Connection, subject: Optional[str] = None) -> List[Dict[str, Any]]:
    """List learning topics (substrands) with question/solution/review counts.

    Counts join on (subject, indicator_code) because NaCCA codes collide across
    subjects (e.g. B7.2.2.1.3 is Algebraic Expressions in Maths and Presentation
    Software in Computing).
    """
    sql = """
        SELECT ci.subject, ci.strand_title, ci.substrand_title,
               COUNT(DISTINCT ci.code) AS indicator_count,
               COUNT(q.id) AS question_count,
               COUNT(DISTINCT s.id) AS solutions_cached,
               SUM(CASE WHEN q.confidence < 0.70 THEN 1 ELSE 0 END) AS low_confidence_questions
        FROM curriculum_indicators ci
        LEFT JOIN questions q
          ON q.subject = ci.subject AND q.indicator_code = ci.code
        LEFT JOIN solutions s
          ON s.question_id = q.id
    """
    params: List[Any] = []
    if subject:
        sql += " WHERE ci.subject = ?"
        params.append(subject)
    sql += (
        " GROUP BY ci.subject, ci.strand_title, ci.substrand_title"
        " ORDER BY question_count DESC, ci.subject, ci.strand_title, ci.substrand_title"
    )
    return [dict(r) for r in conn.execute(sql, params).fetchall()]


def cmd_coverage(args: argparse.Namespace, db_path: Path = DATABASE_PATH) -> int:
    with _get_conn(db_path) as conn:
        if args.list_topics:
            topics = _list_topics(conn, subject=args.subject)
            if args.has_questions:
                topics = [t for t in topics if t["question_count"] > 0]
            payload = {"count": len(topics), "topics": topics}
            if args.format == "json":
                print(json.dumps(payload, indent=2))
            else:
                for t in topics:
                    print(
                        f"[{t['subject']}] {t['strand_title']} > {t['substrand_title']} "
                        f"— {t['question_count']} q, {t['solutions_cached']} sol, "
                        f"{t['low_confidence_questions']} low-conf ({t['indicator_count']} indicators)"
                    )
            return 0

        if not args.topic:
            print("error: --topic is required (or pass --list-topics)", file=sys.stderr)
            return 2

        resolution, indicators = _resolve_topic_indicators(
            conn, args.topic, subject=args.subject
        )
        if not indicators:
            print(
                json.dumps(
                    {
                        "topic": args.topic,
                        "resolution": resolution,
                        "indicators": [],
                        "error": "no curriculum indicators matched this topic",
                    },
                    indent=2,
                )
            )
            return 1

        codes = [i["code"] for i in indicators]
        placeholders = ",".join("?" * len(codes))
        # Match (subject, indicator_code) pairs so cross-subject mis-tags cannot inflate totals.
        pair_sql = " OR ".join("(subject = ? AND indicator_code = ?)" for _ in indicators)
        pair_params: List[Any] = []
        for ind in indicators:
            pair_params.extend([ind["subject"], ind["code"]])

        per_indicator: List[Dict[str, Any]] = []
        for ind in indicators:
            code = ind["code"]
            qrow = conn.execute(
                f"""
                SELECT COUNT(*) AS question_count,
                       ROUND(AVG(CASE WHEN confidence > 0 THEN confidence END), 4) AS avg_confidence,
                       SUM(CASE WHEN confidence < ? THEN 1 ELSE 0 END) AS low_confidence_questions,
                       SUM(CASE WHEN has_diagram = 1 THEN 1 ELSE 0 END) AS diagram_questions,
                       MIN(year) AS min_year,
                       MAX(year) AS max_year
                FROM questions
                WHERE subject = ? AND indicator_code = ?
                """,
                (args.confidence_threshold, ind["subject"], code),
            ).fetchone()
            sol_count = conn.execute(
                "SELECT COUNT(*) FROM solutions WHERE indicator_code = ?",
                (code,),
            ).fetchone()[0]
            open_rev = conn.execute(
                """
                SELECT COUNT(*)
                FROM tag_review_queue r
                JOIN questions q ON q.id = r.question_id
                WHERE r.status = 'open' AND q.indicator_code = ?
                """,
                (code,),
            ).fetchone()[0]
            per_indicator.append(
                {
                    **ind,
                    "question_count": qrow["question_count"] or 0,
                    "avg_confidence": qrow["avg_confidence"],
                    "low_confidence_questions": qrow["low_confidence_questions"] or 0,
                    "diagram_questions": qrow["diagram_questions"] or 0,
                    "min_year": qrow["min_year"],
                    "max_year": qrow["max_year"],
                    "solutions_cached": sol_count,
                    "open_reviews": open_rev,
                }
            )

        totals_row = conn.execute(
            f"""
            SELECT COUNT(*) AS questions,
                   ROUND(AVG(CASE WHEN confidence > 0 THEN confidence END), 4) AS avg_confidence,
                   SUM(CASE WHEN confidence < ? THEN 1 ELSE 0 END) AS low_confidence_questions,
                   SUM(CASE WHEN has_diagram = 1 THEN 1 ELSE 0 END) AS diagram_questions
            FROM questions
            WHERE {pair_sql}
            """,
            (args.confidence_threshold, *pair_params),
        ).fetchone()
        # solutions has no subject column — join questions for pair-safe counting
        solutions_cached = conn.execute(
            f"""
            SELECT COUNT(*)
            FROM solutions s
            JOIN questions q ON q.id = s.question_id
            WHERE {pair_sql.replace("subject =", "q.subject =").replace("indicator_code =", "q.indicator_code =")}
            """,
            pair_params,
        ).fetchone()[0]
        open_reviews = conn.execute(
            f"""
            SELECT COUNT(*)
            FROM tag_review_queue r
            JOIN questions q ON q.id = r.question_id
            WHERE r.status = 'open' AND ({pair_sql})
            """,
            pair_params,
        ).fetchone()[0]
        years = [
            r[0]
            for r in conn.execute(
                f"""
                SELECT DISTINCT year FROM questions
                WHERE ({pair_sql}) AND year IS NOT NULL AND year != ''
                ORDER BY year
                """,
                pair_params,
            ).fetchall()
        ]
        by_grade = [
            dict(r)
            for r in conn.execute(
                f"""
                SELECT ci.grade, COUNT(q.id) AS question_count
                FROM curriculum_indicators ci
                LEFT JOIN questions q
                  ON q.subject = ci.subject AND q.indicator_code = ci.code
                WHERE ci.code IN ({placeholders})
                GROUP BY ci.grade
                ORDER BY ci.grade
                """,
                codes,
            ).fetchall()
        ]
        # True orphans: (subject, indicator_code) pairs that do not exist in
        # curriculum_indicators. NaCCA codes collide across subjects, so a
        # Computing question on B7.2.2.1.3 is valid (Presentation Software),
        # not an Algebraic Expressions mis-tag.
        orphan_mistags = conn.execute(
            """
            SELECT COUNT(*)
            FROM questions q
            WHERE q.indicator_code IS NOT NULL
              AND NOT EXISTS (
                  SELECT 1 FROM curriculum_indicators ci
                  WHERE ci.subject = q.subject AND ci.code = q.indicator_code
              )
            """
        ).fetchone()[0]

        # Leakage: FTS hits for the topic keywords currently tagged outside the topic set.
        fts_terms = [t for t in re.findall(r"[A-Za-z0-9]+", args.topic) if len(t) > 2]
        fts_query = " OR ".join(fts_terms) if fts_terms else ""
        leakage_total = 0
        leakage_sample: List[Dict[str, Any]] = []
        if fts_query:
            not_in = ",".join("?" * len(codes))
            try:
                leakage_total = conn.execute(
                    f"""
                    SELECT COUNT(*)
                    FROM questions_fts f
                    WHERE questions_fts MATCH ?
                      AND f.indicator_code IS NOT NULL
                      AND f.indicator_code NOT IN ({not_in})
                    """,
                    (fts_query, *codes),
                ).fetchone()[0]
                leakage_sample = [
                    dict(r)
                    for r in conn.execute(
                        f"""
                        SELECT f.id, f.subject, f.indicator_code,
                               substr(f.question_text, 1, 120) AS snippet
                        FROM questions_fts f
                        WHERE questions_fts MATCH ?
                          AND f.indicator_code IS NOT NULL
                          AND f.indicator_code NOT IN ({not_in})
                        LIMIT 5
                        """,
                        (fts_query, *codes),
                    ).fetchall()
                ]
            except sqlite3.OperationalError:
                # Malformed FTS query — skip leakage rather than fail the report.
                pass

        bank_total = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
        questions_total = totals_row["questions"] or 0
        payload = {
            "topic": args.topic,
            "resolution": resolution,
            "subject_filter": args.subject,
            "confidence_threshold": args.confidence_threshold,
            "indicators": per_indicator,
            "by_grade": by_grade,
            "totals": {
                "indicators": len(indicators),
                "questions": questions_total,
                "avg_confidence": totals_row["avg_confidence"],
                "low_confidence_questions": totals_row["low_confidence_questions"] or 0,
                "diagram_questions": totals_row["diagram_questions"] or 0,
                "solutions_cached": solutions_cached,
                "solution_rate": round(solutions_cached / questions_total, 4) if questions_total else 0.0,
                "open_reviews": open_reviews,
                "years_covered": years,
                "bank_total_questions": bank_total,
                "topic_share_of_bank": round(questions_total / bank_total, 4) if bank_total else 0.0,
            },
            "completeness_check": {
                "tagged_to_topic": questions_total,
                "with_verified_solution": solutions_cached,
                "orphan_indicator_tags": orphan_mistags,
                "fts_keyword_hits_tagged_elsewhere": leakage_total,
                "fts_keyword_hits_sample": leakage_sample,
                "note": (
                    "orphan_indicator_tags counts questions whose (subject, indicator_code) "
                    "is missing from curriculum_indicators. Codes collide across subjects — "
                    "B7.2.2.1.3 is Algebraic Expressions in Maths and Presentation Software in "
                    "Computing; that is valid, not a mis-tag. "
                    "fts_keyword_hits_tagged_elsewhere > 0 means keyword-matching questions "
                    "exist outside this topic's indicators — review before claiming ALL."
                ),
            },
        }

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        t = payload["totals"]
        print(f"# Topic coverage: {payload['topic']} ({payload['resolution']})")
        if payload["subject_filter"]:
            print(f"Subject filter: {payload['subject_filter']}")
        print(
            f"Indicators: {t['indicators']} | Questions: {t['questions']} "
            f"| Solutions: {t['solutions_cached']} ({t['solution_rate']:.1%}) "
            f"| Open reviews: {t['open_reviews']} | Avg confidence: {t['avg_confidence']}"
        )
        print(f"Years: {', '.join(str(y) for y in t['years_covered']) or 'n/a'}")
        print("")
        for row in payload["indicators"]:
            print(
                f"  {row['code']} ({row['grade']}) [{row['question_count']} q, "
                f"sol={row['solutions_cached']}, conf={row['avg_confidence']}] "
                f"— {row['substrand_title']}: {(row['indicator_text'] or '')[:90]}"
            )
        print("")
        cc = payload["completeness_check"]
        print(
            f"Completeness: tagged={cc['tagged_to_topic']} solved={cc['with_verified_solution']} "
            f"orphan_tags={cc['orphan_indicator_tags']} "
            f"fts_hits_outside_topic={cc['fts_keyword_hits_tagged_elsewhere']}"
        )
        for s in cc["fts_keyword_hits_sample"]:
            print(f"  ? {s['id']} [{s['indicator_code']}] {s['snippet']}")
    return 0


def cmd_reject_content(args: argparse.Namespace, db_path: Path = DATABASE_PATH) -> int:
    """Permanently tombstone content hashes so junk is never re-downloaded."""
    from src.database import CatalogDatabase

    db = CatalogDatabase(db_path=db_path)

    if args.list:
        rows = db.list_rejected_content(reason=args.reason, limit=args.limit)
        payload = {"count": len(rows), "rejected": rows}
        if args.format == "json":
            print(json.dumps(payload, indent=2))
        else:
            for r in rows:
                print(f"{r['sha256'][:16]}… [{r['reason']}] {r['original_url'] or r['file_name']}")
        return 0

    if not args.sha256 and not args.file:
        print("error: provide --sha256 or --file (or --list)", file=sys.stderr)
        return 2

    sha = args.sha256
    if args.file:
        import hashlib

        p = Path(args.file)
        if not p.exists():
            print(f"error: file not found: {p}", file=sys.stderr)
            return 1
        sha = hashlib.sha256(p.read_bytes()).hexdigest()

    inserted = db.record_rejected_content(
        sha256=sha,
        reason=args.reason or "manual_reject",
        original_url=args.url or "",
        file_name=Path(args.file).name if args.file else "",
        file_type=Path(args.file).suffix if args.file else "",
        details=args.details or "manual tombstone via bece_cli reject-content",
    )
    print(json.dumps({"status": "inserted" if inserted else "already_rejected", "sha256": sha}, indent=2))
    return 0


def cmd_tag(args: argparse.Namespace, db_path: Path = DATABASE_PATH) -> int:
    from src.database import CatalogDatabase
    from src.tagger import CurriculumTagger, JinaListwiseRerankerBackend, LayaDecisionGateBackend

    reranker = JinaListwiseRerankerBackend() if args.use_reranker else None
    laya_gate = LayaDecisionGateBackend() if args.use_laya else None
    tagger = CurriculumTagger(
        db_path=db_path,
        reranker=reranker,
        laya_gate=laya_gate,
        truncate_dim=args.truncate_dim,
        enable_vision=args.enable_vision,
        confidence_threshold=args.confidence_threshold,
    )
    summary = tagger.tag_all_questions(
        subject=args.subject,
        only_untagged=args.only_untagged,
        use_reranker=args.use_reranker,
        use_laya=args.use_laya,
        batch_size=args.batch_size,
    )
    if db_path == DATABASE_PATH:
        exported = CatalogDatabase(db_path=db_path).export_questions_json()
        summary["exported_to_json"] = exported
    print(json.dumps(summary, indent=2))
    return 0


def cmd_stats(args: argparse.Namespace, db_path: Path = DATABASE_PATH) -> int:
    with _get_conn(db_path) as conn:
        q_total = conn.execute("SELECT COUNT(*) FROM questions;").fetchone()[0]
        q_tagged = conn.execute("SELECT COUNT(*) FROM questions WHERE indicator_code IS NOT NULL;").fetchone()[0]
        q_emb = conn.execute("SELECT COUNT(*) FROM questions WHERE embedding IS NOT NULL;").fetchone()[0]
        occ_total = conn.execute("SELECT COUNT(*) FROM question_occurrences;").fetchone()[0]
        ind_total = conn.execute("SELECT COUNT(*) FROM curriculum_indicators;").fetchone()[0]
        ind_emb = conn.execute("SELECT COUNT(*) FROM curriculum_indicators WHERE embedding IS NOT NULL;").fetchone()[0]
        sol_total = conn.execute("SELECT COUNT(*) FROM solutions;").fetchone()[0]
        rev_open = conn.execute("SELECT COUNT(*) FROM tag_review_queue WHERE status = 'open';").fetchone()[0]
        rej_total = conn.execute("SELECT COUNT(*) FROM rejected_content;").fetchone()[0]

        by_subj = [
            dict(r)
            for r in conn.execute(
                """
                SELECT subject,
                       COUNT(*) AS total_questions,
                       SUM(CASE WHEN indicator_code IS NOT NULL THEN 1 ELSE 0 END) AS tagged_questions,
                       ROUND(AVG(CASE WHEN confidence > 0 THEN confidence END), 4) AS avg_confidence
                FROM questions
                GROUP BY subject
                ORDER BY total_questions DESC;
                """
            ).fetchall()
        ]

    payload = {
        "canonical_questions": q_total,
        "questions_tagged": q_tagged,
        "questions_embedded": q_emb,
        "question_occurrences": occ_total,
        "curriculum_indicators": ind_total,
        "indicators_embedded": ind_emb,
        "cached_solutions": sol_total,
        "open_review_queue_items": rev_open,
        "rejected_content_hashes": rej_total,
        "by_subject": by_subj,
    }
    print(json.dumps(payload, indent=2))
    return 0


def cmd_diagrams(args: argparse.Namespace, db_path: Path = DATABASE_PATH) -> int:
    from src.curriculum_taxonomy import CANONICAL_DIAGRAMS, get_canonical_diagram

    diagrams = list(CANONICAL_DIAGRAMS)

    if args.id:
        d = get_canonical_diagram(args.id)
        diagrams = [d] if d else []
    else:
        if args.indicator:
            ind = args.indicator.strip().upper()
            diagrams = [d for d in diagrams if d["indicator_code"].upper().startswith(ind)]
        if args.grade:
            g = args.grade.strip().upper()
            diagrams = [d for d in diagrams if d["grade"].upper() == g]
        if args.subject:
            s = args.subject.strip().lower()
            diagrams = [d for d in diagrams if d["subject"].lower() == s]
        if args.search:
            q = args.search.strip().lower()
            diagrams = [
                d
                for d in diagrams
                if q in d["name"].lower()
                or q in d["topic"].lower()
                or q in d["skill"].lower()
                or q in d["indicator_code"].lower()
            ]

    if args.format == "json":
        print(json.dumps({"count": len(diagrams), "diagrams": diagrams}, indent=2))
        return 0

    if args.format == "text":
        for d in diagrams:
            print(
                f"[{d['id']:02d}] {d['indicator_code']} ({d['grade']}) — {d['name']} : {d['topic']} (Skill: {d['skill']})"
            )
        return 0

    # Markdown format
    print(f"# Canonical BECE Diagram Templates ({len(diagrams)} matching)\n")
    if not diagrams:
        print("_No canonical diagrams matched the filter criteria._")
        return 0

    print("| ID | Indicator | Grade | Topic / Title | Source (.tex) | Rendered (.png) | Skill |")
    print("|:---|:---|:---|:---|:---|:---|:---|")
    for d in diagrams:
        tex_abs = (REPO_ROOT / d["tex_file"]).as_posix()
        png_abs = (REPO_ROOT / d["png_file"]).as_posix()
        skill_abs = (REPO_ROOT / d["skill_file"]).as_posix()
        print(
            f"| `{d['id']:02d}` | `{d['indicator_code']}` | {d['grade']} | {d['topic']} | "
            f"[{Path(d['tex_file']).name}](file:///{tex_abs}) | "
            f"[{Path(d['png_file']).name}](file:///{png_abs}) | "
            f"[`{d['skill']}`](file:///{skill_abs}) |"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bece_cli", description="BECE Curriculum Question Bank CLI")
    parser.add_argument("--db", type=Path, default=DATABASE_PATH, help="Path to catalog.db")
    sub = parser.add_subparsers(dest="command", required=True)

    # query
    p_q = sub.add_parser("query", help="Fetch canonical questions by curriculum indicator code")
    p_q.add_argument("--indicator", "-i", type=str, help="NaCCA indicator code or prefix (e.g. B9.1.1.2.2 or B9.1.1.2)")
    p_q.add_argument("--subject", "-s", type=str, choices=["Mathematics", "Computing_ICT", "CDT_CAD"])
    p_q.add_argument("--include-prerequisites", action=argparse.BooleanOptionalAction, default=True)
    p_q.add_argument("--paper-type", type=str, help="Filter by Paper 1 or Paper 2")
    p_q.add_argument("--has-diagram", action=argparse.BooleanOptionalAction, default=None)
    p_q.add_argument("--limit", "-n", type=int, default=10)
    p_q.add_argument("--format", "-f", choices=["markdown", "json"], default="markdown")

    # search
    p_s = sub.add_parser("search", help="Hybrid EmbeddingGemma-2 + FTS5 semantic search over questions")
    p_s.add_argument("query_text", type=str, help="Natural language topic or question search string")
    p_s.add_argument("--subject", "-s", type=str, choices=["Mathematics", "Computing_ICT", "CDT_CAD"])
    p_s.add_argument("--indicator", "-i", type=str)
    p_s.add_argument("--fts-only", action="store_true", help="Use FTS5 lexical search only")
    p_s.add_argument("--limit", "-n", type=int, default=10)
    p_s.add_argument("--format", "-f", choices=["markdown", "json"], default="markdown")

    # save-solution
    p_sol = sub.add_parser("save-solution", help="Verify and cache a worked step-by-step solution")
    p_sol.add_argument("--id", required=True, help="Canonical question ID (e.g. Q_...)")
    p_sol.add_argument("--lesson", required=True, help="Lesson identifier (e.g. Strand-1-Number/Lesson-04-Surds)")
    p_sol.add_argument("--indicator", help="Optional override indicator code")
    p_sol.add_argument("--answer", required=True, help="Final canonical answer or option letter (A-D)")
    p_sol.add_argument("--steps", help="Inline markdown step-by-step worked solution")
    p_sol.add_argument("--file", help="Path to markdown file containing step-by-step worked solution")
    p_sol.add_argument("--sympy-lhs", help="Optional SymPy LHS expression to verify symbolic equivalence")
    p_sol.add_argument("--sympy-rhs", help="Optional SymPy RHS expression to verify symbolic equivalence")
    p_sol.add_argument("--force", action="store_true", help="Save even if automated verification flags a warning")

    # indicators
    p_ind = sub.add_parser("indicators", help="List or search official B7-B9 curriculum indicators")
    p_ind.add_argument("--subject", "-s", type=str, choices=["Mathematics", "Computing_ICT", "CDT_CAD"])
    p_ind.add_argument("--grade", "-g", type=str, choices=["B7", "B8", "B9", "b7", "b8", "b9"])
    p_ind.add_argument("--search", "-q", type=str, help="Substring filter on code, substrand, or text")
    p_ind.add_argument("--format", "-f", choices=["text", "json"], default="text")

    # tag
    p_tag = sub.add_parser("tag", help="Run the Phase 2 CurriculumTagger pipeline")
    p_tag.add_argument("--subject", "-s", type=str, choices=["Mathematics", "Computing_ICT", "CDT_CAD"])
    p_tag.add_argument("--only-untagged", action="store_true")
    p_tag.add_argument("--use-reranker", action="store_true", help="Enable Stage 2 jina-reranker-v3.5 listwise reranking")
    p_tag.add_argument("--use-laya", action="store_true", help="Enable Stage 3 Laya permutation-averaged decision gate")
    p_tag.add_argument("--enable-vision", action="store_true", help="Enable EmbeddingGemma-2 multimodal vision tower for diagrams")
    p_tag.add_argument("--truncate-dim", type=int, default=768, choices=[128, 256, 512, 768])
    p_tag.add_argument("--confidence-threshold", type=float, default=0.70)
    p_tag.add_argument("--batch-size", type=int, default=64)

    # coverage
    p_cov = sub.add_parser(
        "coverage",
        help="Topic→indicator question/solution coverage report (proves whether 'ALL' is true)",
    )
    p_cov.add_argument(
        "--topic",
        "-t",
        type=str,
        help='Learning topic name matched to official substrand (e.g. "Algebraic Expressions")',
    )
    p_cov.add_argument("--subject", "-s", type=str, choices=["Mathematics", "Computing_ICT", "CDT_CAD"])
    p_cov.add_argument("--list-topics", action="store_true", help="List available substrand topics")
    p_cov.add_argument(
        "--has-questions",
        action="store_true",
        help="With --list-topics, keep only topics that have at least one question",
    )
    p_cov.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.70,
        help="Tags below this confidence count as low_confidence_questions",
    )
    p_cov.add_argument("--format", "-f", choices=["text", "json"], default="text")

    # stats
    sub.add_parser("stats", help="Display question bank, tagging, and solution cache telemetry")

    # reject-content
    p_rej = sub.add_parser(
        "reject-content",
        help="Permanently tombstone a content hash so junk files are never re-downloaded",
    )
    p_rej.add_argument("--sha256", help="Content SHA-256 to reject")
    p_rej.add_argument("--file", help="Local file whose hash should be rejected")
    p_rej.add_argument("--url", help="Original URL (provenance)")
    p_rej.add_argument(
        "--reason",
        default="manual_reject",
        help="not_exam_paper | no_exam_signals | unclassified_wrong_subject | manual_reject | duplicate",
    )
    p_rej.add_argument("--details", help="Free-form note")
    p_rej.add_argument("--list", action="store_true", help="List rejected content")
    p_rej.add_argument("--limit", type=int, default=50)
    p_rej.add_argument("--format", "-f", choices=["text", "json"], default="text")

    # diagrams
    p_diag = sub.add_parser(
        "diagrams",
        help="List and inspect canonical BECE TikZ diagram templates and companion skills",
    )
    p_diag.add_argument("--id", help="Diagram ID (1-46), name, or skill name")
    p_diag.add_argument(
        "--indicator",
        "-i",
        type=str,
        help="Filter by curriculum indicator code or prefix (e.g. B9.1.1.2.2 or B9.1.1)",
    )
    p_diag.add_argument(
        "--grade",
        "-g",
        type=str,
        choices=["B7", "B8", "B9", "b7", "b8", "b9"],
        help="Filter by grade",
    )
    p_diag.add_argument(
        "--subject",
        "-s",
        type=str,
        choices=["Mathematics", "Computing_ICT", "CDT_CAD"],
        help="Filter by subject",
    )
    p_diag.add_argument(
        "--search",
        "-q",
        type=str,
        help="Substring search across name, topic, and skill",
    )
    p_diag.add_argument(
        "--format",
        "-f",
        choices=["markdown", "json", "text"],
        default="markdown",
    )

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args(argv)
    db_path = Path(args.db)

    dispatch = {
        "query": cmd_query,
        "search": cmd_search,
        "save-solution": cmd_save_solution,
        "indicators": cmd_indicators,
        "coverage": cmd_coverage,
        "tag": cmd_tag,
        "stats": cmd_stats,
        "reject-content": cmd_reject_content,
        "diagrams": cmd_diagrams,
    }
    return dispatch[args.command](args, db_path=db_path)


if __name__ == "__main__":
    raise SystemExit(main())
