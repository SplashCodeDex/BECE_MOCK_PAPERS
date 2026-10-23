import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.bank_schema import init_bank_schema
from src.config import CATALOG_JSON_PATH, DATABASE_PATH, METADATA_DIR


class CatalogDatabase:
    """SQLite Database manager for tracking harvested files, sources, canonical questions, taxonomy, and solutions."""

    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self._ensure_dir()
        self.init_db()

    def _ensure_dir(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        # Enable WAL mode for high performance concurrent writes
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    def init_db(self) -> None:
        with self.get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS harvested_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sha256 TEXT UNIQUE NOT NULL,
                    original_url TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    local_path TEXT NOT NULL,
                    source_domain TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_marking_scheme INTEGER DEFAULT 0
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS visited_urls (
                    url TEXT PRIMARY KEY,
                    status_code INTEGER,
                    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS rejected_content (
                    sha256 TEXT PRIMARY KEY,
                    original_url TEXT,
                    file_name TEXT,
                    file_type TEXT,
                    reason TEXT NOT NULL,
                    details TEXT,
                    decided_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_harvested_sha ON harvested_files(sha256);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_harvested_subject ON harvested_files(subject);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_harvested_type ON harvested_files(file_type);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_rejected_reason ON rejected_content(reason);")
        init_bank_schema(self.db_path)

    def is_hash_rejected(self, sha256_hash: str) -> bool:
        with self.get_connection() as conn:
            cur = conn.execute(
                "SELECT 1 FROM rejected_content WHERE sha256 = ? LIMIT 1;",
                (sha256_hash,),
            )
            return cur.fetchone() is not None

    def record_rejected_content(
        self,
        sha256: str,
        reason: str,
        original_url: str = "",
        file_name: str = "",
        file_type: str = "",
        details: str = "",
    ) -> bool:
        """Permanently tombstone a content hash so junk is never re-downloaded.

        These rows must outlive the files themselves — deleting a local copy must
        not allow a future crawl to fetch the same bytes again.
        """
        with self.get_connection() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO rejected_content (
                        sha256, original_url, file_name, file_type, reason, details, decided_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        sha256,
                        original_url,
                        file_name,
                        file_type,
                        reason,
                        details,
                        datetime.now(timezone.utc).isoformat(),
                    ),
                )
                return True
            except sqlite3.IntegrityError:
                return False

    def list_rejected_content(self, reason: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM rejected_content"
        params: List[Any] = []
        if reason:
            sql += " WHERE reason = ?"
            params.append(reason)
        sql += " ORDER BY decided_at DESC LIMIT ?"
        params.append(limit)
        with self.get_connection() as conn:
            return [dict(r) for r in conn.execute(sql, params).fetchall()]

    def is_content_known(self, sha256_hash: str) -> bool:
        """True if this content was kept or permanently rejected (never refetch)."""
        return self.is_hash_seen(sha256_hash) or self.is_hash_rejected(sha256_hash)

    def is_hash_seen(self, sha256_hash: str) -> bool:
        with self.get_connection() as conn:
            cur = conn.execute(
                "SELECT 1 FROM harvested_files WHERE sha256 = ? LIMIT 1;",
                (sha256_hash,),
            )
            return cur.fetchone() is not None

    def is_url_visited(self, url: str) -> bool:
        with self.get_connection() as conn:
            cur = conn.execute(
                "SELECT 1 FROM visited_urls WHERE url = ? LIMIT 1;",
                (url,),
            )
            return cur.fetchone() is not None

    def record_url_visited(self, url: str, status_code: int = 200) -> None:
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO visited_urls (url, status_code, discovered_at)
                VALUES (?, ?, ?);
                """,
                (url, status_code, datetime.now(timezone.utc).isoformat()),
            )

    def save_harvested_file(
        self,
        sha256: str,
        original_url: str,
        file_name: str,
        file_type: str,
        subject: str,
        file_size: int,
        local_path: str,
        source_domain: str,
    ) -> bool:
        """Saves a harvested file record. Returns True if inserted, False if duplicate."""
        if self.is_hash_seen(sha256):
            return False

        with self.get_connection() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO harvested_files (
                        sha256, original_url, file_name, file_type,
                        subject, file_size, local_path, source_domain, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        sha256,
                        original_url,
                        file_name,
                        file_type.lower().replace(".", ""),
                        subject,
                        file_size,
                        str(local_path),
                        source_domain,
                        datetime.now(timezone.utc).isoformat(),
                    ),
                )
                return True
            except sqlite3.IntegrityError:
                return False

    def get_canonical_questions(
        self,
        subject: Optional[str] = None,
        indicator_code: Optional[str] = None,
        paper_type: Optional[str] = None,
        has_diagram: Optional[int] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Queries canonical, deduplicated questions with optional filters."""
        query = "SELECT * FROM questions WHERE 1=1"
        params: List[Any] = []

        if subject:
            query += " AND subject = ?"
            params.append(subject)
        if indicator_code:
            query += " AND indicator_code = ?"
            params.append(indicator_code)
        if paper_type:
            query += " AND paper_type = ?"
            params.append(paper_type)
        if has_diagram is not None:
            query += " AND has_diagram = ?"
            params.append(has_diagram)

        query += " ORDER BY year DESC, subject, id LIMIT ? OFFSET ?;"
        params.extend([limit, offset])

        with self.get_connection() as conn:
            cur = conn.execute(query, params)
            return [dict(r) for r in cur.fetchall()]

    def get_occurrences(self, question_id: str) -> List[Dict[str, Any]]:
        """Returns all appearances of a question across past exams, mock papers, and files."""
        with self.get_connection() as conn:
            cur = conn.execute(
                """
                SELECT o.*, s.name as source_name, s.source_type, s.domain
                FROM question_occurrences o
                LEFT JOIN sources s ON o.source_id = s.id
                WHERE o.question_id = ?
                ORDER BY o.year DESC, o.id ASC;
                """,
                (question_id,)
            )
            return [dict(r) for r in cur.fetchall()]

    def search_questions(
        self,
        query_text: str,
        subject: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Full-text search over canonical questions using FTS5 index."""
        sql = """
            SELECT q.*, f.rank
            FROM questions_fts f
            JOIN questions q ON f.rowid = q.rowid
            WHERE questions_fts MATCH ?
        """
        params: List[Any] = [query_text]

        if subject:
            sql += " AND q.subject = ?"
            params.append(subject)

        sql += " ORDER BY f.rank LIMIT ?;"
        params.append(limit)

        with self.get_connection() as conn:
            cur = conn.execute(sql, params)
            return [dict(r) for r in cur.fetchall()]

    def get_question(self, question_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cur = conn.execute("SELECT * FROM questions WHERE id = ? LIMIT 1;", (question_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def get_curriculum_indicators(
        self,
        grade: Optional[str] = None,
        subject: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        query = "SELECT * FROM curriculum_indicators WHERE 1=1"
        params: List[Any] = []
        if grade:
            query += " AND grade = ?"
            params.append(grade)
        if subject:
            query += " AND subject = ?"
            params.append(subject)
        query += " ORDER BY strand_number, substrand_number, code;"

        with self.get_connection() as conn:
            cur = conn.execute(query, params)
            rows = []
            for r in cur.fetchall():
                d = dict(r)
                if d.get("prerequisite_codes"):
                    try:
                        d["prerequisite_codes"] = json.loads(d["prerequisite_codes"])
                    except Exception:
                        pass
                rows.append(d)
            return rows

    def save_solution(
        self,
        solution_id: str,
        question_id: str,
        lesson_id: str,
        indicator_code: str,
        step_by_step_markdown: str,
        final_answer: str,
        verification_type: str,
        verification_details: Optional[str] = None
    ) -> bool:
        """Saves a verified solution with UNIQUE(question_id, lesson_id)."""
        with self.get_connection() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO solutions (
                        id, question_id, lesson_id, indicator_code,
                        step_by_step_markdown, final_answer, verification_type, verification_details
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(question_id, lesson_id) DO UPDATE SET
                        step_by_step_markdown=excluded.step_by_step_markdown,
                        final_answer=excluded.final_answer,
                        verification_type=excluded.verification_type,
                        verification_details=excluded.verification_details,
                        created_at=CURRENT_TIMESTAMP;
                    """,
                    (
                        solution_id, question_id, lesson_id, indicator_code,
                        step_by_step_markdown, final_answer, verification_type, verification_details
                    )
                )
                return True
            except sqlite3.IntegrityError:
                return False

    def get_solution(self, question_id: str, lesson_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            if lesson_id:
                cur = conn.execute(
                    "SELECT * FROM solutions WHERE question_id = ? AND lesson_id = ? LIMIT 1;",
                    (question_id, lesson_id)
                )
            else:
                cur = conn.execute(
                    "SELECT * FROM solutions WHERE question_id = ? ORDER BY created_at DESC LIMIT 1;",
                    (question_id,)
                )
            row = cur.fetchone()
            return dict(row) if row else None

    def add_to_review_queue(
        self,
        question_id: str,
        reason: str,
        candidate_indicators: Optional[List[Dict[str, Any]]] = None,
        notes: Optional[str] = None
    ) -> bool:
        candidates_json = json.dumps(candidate_indicators or [])
        with self.get_connection() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO tag_review_queue (question_id, reason, candidate_indicators, notes)
                    VALUES (?, ?, ?, ?);
                    """,
                    (question_id, reason, candidates_json, notes)
                )
                return True
            except sqlite3.IntegrityError:
                return False

    def get_review_queue(self, status: str = "open", limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cur = conn.execute(
                """
                SELECT r.*, q.subject, q.question_text, q.paper_type
                FROM tag_review_queue r
                JOIN questions q ON r.question_id = q.id
                WHERE r.status = ?
                ORDER BY r.created_at ASC LIMIT ?;
                """,
                (status, limit)
            )
            return [dict(row) for row in cur.fetchall()]

    def get_stats(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            total_files = conn.execute("SELECT COUNT(*) FROM harvested_files;").fetchone()[0]
            cur_subjects = conn.execute(
                "SELECT subject, COUNT(*) as count FROM harvested_files GROUP BY subject ORDER BY count DESC;"
            )
            subjects = {row["subject"]: row["count"] for row in cur_subjects.fetchall()}
            cur_types = conn.execute(
                "SELECT file_type, COUNT(*) as count FROM harvested_files GROUP BY file_type ORDER BY count DESC;"
            )
            file_types = {row["file_type"]: row["count"] for row in cur_types.fetchall()}
            visited_urls = conn.execute("SELECT COUNT(*) FROM visited_urls;").fetchone()[0]

            total_q = conn.execute("SELECT COUNT(*) FROM questions;").fetchone()[0]
            total_occ = conn.execute("SELECT COUNT(*) FROM question_occurrences;").fetchone()[0]
            tagged_q = conn.execute("SELECT COUNT(*) FROM questions WHERE indicator_code IS NOT NULL;").fetchone()[0]
            solutions_count = conn.execute("SELECT COUNT(*) FROM solutions;").fetchone()[0]
            review_count = conn.execute("SELECT COUNT(*) FROM tag_review_queue WHERE status = 'open';").fetchone()[0]
            indicators_count = conn.execute("SELECT COUNT(*) FROM curriculum_indicators;").fetchone()[0]
            sources_count = conn.execute("SELECT COUNT(*) FROM sources;").fetchone()[0]

        return {
            "total_harvested_files": total_files,
            "subjects": subjects,
            "file_types": file_types,
            "visited_urls": visited_urls,
            "canonical_questions": total_q,
            "occurrences": total_occ,
            "duplicates_merged": max(0, total_occ - total_q),
            "tagged_questions": tagged_q,
            "solutions_count": solutions_count,
            "open_reviews": review_count,
            "curriculum_indicators": indicators_count,
            "registered_sources": sources_count,
        }

    def export_catalog_json(self, export_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        target_path = Path(export_path) if export_path else CATALOG_JSON_PATH
        with self.get_connection() as conn:
            cur = conn.execute(
                """
                SELECT id, sha256, original_url, file_name, file_type,
                       subject, file_size, local_path, source_domain, created_at
                FROM harvested_files ORDER BY id ASC;
                """
            )
            rows = [dict(r) for r in cur.fetchall()]

        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)

        return rows

    def export_questions_json(
        self,
        json_path: Optional[Path] = None,
        jsonl_path: Optional[Path] = None
    ) -> int:
        """Exports all canonical questions to questions_bank.json and questions_bank.jsonl."""
        default_json = self.db_path.parent.parent / "extracted_questions" / "questions_bank.json"
        default_jsonl = self.db_path.parent.parent / "extracted_questions" / "questions_bank.jsonl"
        out_json = Path(json_path) if json_path else default_json
        out_jsonl = Path(jsonl_path) if jsonl_path else default_jsonl

        with self.get_connection() as conn:
            cur = conn.execute(
                """
                SELECT id, subject, year, paper_type, question_text, option_a,
                       option_b, option_c, option_d, correct_answer, has_diagram,
                       diagram_path, indicator_code, confidence, tag_method, dedup_hash,
                       migrated_from, created_at
                FROM questions
                ORDER BY subject, year DESC, id;
                """
            )
            rows = [dict(r) for r in cur.fetchall()]

        out_json.parent.mkdir(parents=True, exist_ok=True)
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)

        with open(out_jsonl, "w", encoding="utf-8") as f:
            for item in rows:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        return len(rows)
