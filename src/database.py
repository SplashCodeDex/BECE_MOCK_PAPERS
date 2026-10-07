import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from src.config import CATALOG_JSON_PATH, DATABASE_PATH, METADATA_DIR


class CatalogDatabase:
    """SQLite Database manager for tracking harvested files, deduplication, and visited URLs."""

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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                "CREATE INDEX IF NOT EXISTS idx_harvested_sha ON harvested_files(sha256);"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_harvested_subject ON harvested_files(subject);"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_harvested_type ON harvested_files(file_type);"
            )

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
                (url, status_code, datetime.utcnow().isoformat()),
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
                        datetime.utcnow().isoformat(),
                    ),
                )
                return True
            except sqlite3.IntegrityError:
                return False

    def get_stats(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cur_total = conn.execute("SELECT COUNT(*) FROM harvested_files;")
            total_files = cur_total.fetchone()[0]

            cur_subjects = conn.execute(
                "SELECT subject, COUNT(*) as count FROM harvested_files GROUP BY subject ORDER BY count DESC;"
            )
            subjects = {row["subject"]: row["count"] for row in cur_subjects.fetchall()}

            cur_types = conn.execute(
                "SELECT file_type, COUNT(*) as count FROM harvested_files GROUP BY file_type ORDER BY count DESC;"
            )
            file_types = {row["file_type"]: row["count"] for row in cur_types.fetchall()}

            cur_visited = conn.execute("SELECT COUNT(*) FROM visited_urls;")
            visited_urls = cur_visited.fetchone()[0]

        return {
            "total_harvested_files": total_files,
            "subjects": subjects,
            "file_types": file_types,
            "visited_urls": visited_urls,
        }

    def export_catalog_json(self) -> Path:
        with self.get_connection() as conn:
            cur = conn.execute(
                """
                SELECT id, sha256, original_url, file_name, file_type,
                       subject, file_size, local_path, source_domain, created_at
                FROM harvested_files ORDER BY id ASC;
                """
            )
            rows = [dict(r) for r in cur.fetchall()]

        CATALOG_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CATALOG_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)

        return CATALOG_JSON_PATH
