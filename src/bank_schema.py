"""Phase 1 schema for the BECE question bank (v2 tables).

Adds the following tables alongside the legacy harvester tables
(harvested_files, visited_urls, extracted_questions):

- sources:                curated-first source registry (Q6)
- curriculum_indicators:  full GES B7-B9 taxonomy with prerequisite links (Q3)
- questions:              canonical, deduplicated question bank with provenance
- question_occurrences:   every raw appearance of a question (dedup audit trail)
- solutions:              worked solutions cached per (question, lesson) (Q5)
- tag_review_queue:       unmapped / conflicted items routed for human review (Q3)
- questions_fts:          FTS5 external-content index kept in sync by triggers
"""

import sqlite3
from pathlib import Path

from src.config import DATABASE_PATH

# --- DDL ---------------------------------------------------------------------

SOURCES_DDL = """
CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    domain TEXT NOT NULL,
    url TEXT,
    source_type TEXT NOT NULL,          -- 'waec_official', 'ges_curriculum',
                                       -- 'teacher_site', 'mock_compilation',
                                       -- 'legacy_harvest', 'user_upload'
    acquisition TEXT NOT NULL DEFAULT 'curated',  -- 'curated' | 'legacy_crawl' | 'upload'
    tos_notes TEXT,
    trusted INTEGER NOT NULL DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (domain, name)
);
"""

CURRICULUM_INDICATORS_DDL = """
CREATE TABLE IF NOT EXISTS curriculum_indicators (
    uid TEXT PRIMARY KEY,               -- '<subject>:<code>', e.g. 'Mathematics:B9.1.2.4.1'
    code TEXT NOT NULL,                 -- e.g. 'B9.1.2.4.1' (unique per subject only)
    grade TEXT NOT NULL,                 -- 'B7', 'B8', 'B9'
    subject TEXT NOT NULL,               -- 'Mathematics', 'Computing_ICT', 'CDT_CAD'
    strand_number INTEGER NOT NULL,
    strand_title TEXT NOT NULL,
    substrand_number INTEGER NOT NULL,
    substrand_title TEXT NOT NULL,
    content_standard TEXT NOT NULL,      -- e.g. 'B9.1.2.4'
    content_standard_text TEXT,
    indicator_text TEXT NOT NULL,
    prerequisite_codes TEXT,             -- JSON array of linked B7/B8 foundation codes
    source_file TEXT,
    page INTEGER,
    embedding BLOB,                      -- float32 vector; populated by Phase 2 tagger
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (subject, code)
);
"""

QUESTIONS_DDL = """
CREATE TABLE IF NOT EXISTS questions (
    id TEXT PRIMARY KEY,                 -- canonical: 'Q_' + dedup_hash[:12]
    subject TEXT NOT NULL,
    question_text TEXT NOT NULL,         -- markdown, inline math as $...$ (Phase 2 cleans)
    option_a TEXT,
    option_b TEXT,
    option_c TEXT,
    option_d TEXT,
    correct_answer TEXT,
    has_diagram INTEGER DEFAULT 0,
    diagram_path TEXT,
    year INTEGER,
    paper_type TEXT,
    indicator_code TEXT,                 -- code within this question's subject
    confidence REAL DEFAULT 0.0,
    tag_method TEXT,                     -- 'embedding+llm' | 'rule' | 'manual'
    dedup_hash TEXT NOT NULL UNIQUE,
    migrated_from TEXT,                  -- original extracted_questions.id of first occurrence
    embedding BLOB,                      -- float32 vector cached by Phase 2 tagger
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(subject, indicator_code)
        REFERENCES curriculum_indicators(subject, code)
);
"""

QUESTION_OCCURRENCES_DDL = """
CREATE TABLE IF NOT EXISTS question_occurrences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT NOT NULL,           -- canonical questions.id
    original_id TEXT NOT NULL,           -- legacy extracted_questions.id
    source_file TEXT NOT NULL,
    harvested_file_id INTEGER,
    source_id INTEGER,
    original_url TEXT,
    year INTEGER,
    paper_type TEXT NOT NULL,
    question_number INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(question_id) REFERENCES questions(id),
    FOREIGN KEY(harvested_file_id) REFERENCES harvested_files(id),
    FOREIGN KEY(source_id) REFERENCES sources(id)
);
"""

SOLUTIONS_DDL = """
CREATE TABLE IF NOT EXISTS solutions (
    id TEXT PRIMARY KEY,
    question_id TEXT NOT NULL,
    lesson_id TEXT NOT NULL,             -- e.g. 'Strand-1-Number/Lesson-04-Surds'
    indicator_code TEXT,
    step_by_step_markdown TEXT NOT NULL,
    final_answer TEXT NOT NULL,
    verification_type TEXT NOT NULL,     -- 'sympy_verified' | 'marking_scheme_match' | 'llm_rubric'
    verification_details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (question_id, lesson_id),
    FOREIGN KEY(question_id) REFERENCES questions(id)
);
"""

TAG_REVIEW_QUEUE_DDL = """
CREATE TABLE IF NOT EXISTS tag_review_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT NOT NULL,
    reason TEXT NOT NULL,                -- 'unmapped' | 'low_confidence' | 'answer_conflict'
    details TEXT,
    status TEXT NOT NULL DEFAULT 'open', -- 'open' | 'resolved'
    resolution TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY(question_id) REFERENCES questions(id)
);
"""

QUESTIONS_FTS_DDL = """
CREATE VIRTUAL TABLE IF NOT EXISTS questions_fts USING fts5(
    id UNINDEXED,
    question_text,
    subject,
    indicator_code,
    content='questions',
    content_rowid='rowid'
);
"""

# External-content FTS5 requires manual sync triggers.
FTS_TRIGGERS = [
    "DROP TRIGGER IF EXISTS questions_fts_ai;",
    """
    CREATE TRIGGER questions_fts_ai AFTER INSERT ON questions BEGIN
        INSERT INTO questions_fts (rowid, id, question_text, subject, indicator_code)
        VALUES (new.rowid, new.id, new.question_text, new.subject, new.indicator_code);
    END;
    """,
    "DROP TRIGGER IF EXISTS questions_fts_ad;",
    """
    CREATE TRIGGER questions_fts_ad AFTER DELETE ON questions BEGIN
        INSERT INTO questions_fts (questions_fts, rowid, id, question_text, subject, indicator_code)
        VALUES ('delete', old.rowid, old.id, old.question_text, old.subject, old.indicator_code);
    END;
    """,
    "DROP TRIGGER IF EXISTS questions_fts_au;",
    """
    CREATE TRIGGER questions_fts_au AFTER UPDATE ON questions BEGIN
        INSERT INTO questions_fts (questions_fts, rowid, id, question_text, subject, indicator_code)
        VALUES ('delete', old.rowid, old.id, old.question_text, old.subject, old.indicator_code);
        INSERT INTO questions_fts (rowid, id, question_text, subject, indicator_code)
        VALUES (new.rowid, new.id, new.question_text, new.subject, new.indicator_code);
    END;
    """,
]

INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_questions_subject ON questions(subject);",
    "CREATE INDEX IF NOT EXISTS idx_questions_year ON questions(year);",
    "CREATE INDEX IF NOT EXISTS idx_questions_indicator ON questions(indicator_code);",
    "CREATE INDEX IF NOT EXISTS idx_occurrences_question ON question_occurrences(question_id);",
    "CREATE INDEX IF NOT EXISTS idx_occurrences_source ON question_occurrences(source_id);",
    "CREATE INDEX IF NOT EXISTS idx_indicators_subject ON curriculum_indicators(subject, grade);",
    "CREATE INDEX IF NOT EXISTS idx_review_open ON tag_review_queue(status);",
]

# Unique guards keep re-runs idempotent; created only AFTER dedupe cleanup.
UNIQUE_INDEXES = [
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_occurrences_unique "
    "ON question_occurrences(question_id, original_id);",
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_review_unique "
    "ON tag_review_queue(question_id, reason);",
]

# Cleanup for DBs created before the unique guards existed.
DEDUPE_QUERIES = [
    "DELETE FROM question_occurrences WHERE rowid NOT IN "
    "(SELECT MIN(rowid) FROM question_occurrences GROUP BY question_id, original_id);",
    "DELETE FROM tag_review_queue WHERE rowid NOT IN "
    "(SELECT MIN(rowid) FROM tag_review_queue GROUP BY question_id, reason);",
]

ALL_DDL = [
    SOURCES_DDL,
    CURRICULUM_INDICATORS_DDL,
    QUESTIONS_DDL,
    QUESTION_OCCURRENCES_DDL,
    SOLUTIONS_DDL,
    TAG_REVIEW_QUEUE_DDL,
    QUESTIONS_FTS_DDL,
] + FTS_TRIGGERS + INDEXES


def init_bank_schema(db_path: Path = DATABASE_PATH) -> None:
    """Create all Phase 1 tables/indexes/triggers (idempotent)."""
    conn = sqlite3.connect(str(db_path))
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        # Repair: tables created before the composite-key fix
        # ('code' as sole PK collapses same-named codes across subjects;
        # questions carried the matching old FK clause).
        cur = conn.execute(
            "PRAGMA table_info(curriculum_indicators);"
        ).fetchall()
        cols = {row[1] for row in cur}
        q_sql = conn.execute(
            "SELECT sql FROM sqlite_master WHERE name='questions' AND type='table';"
        ).fetchone()
        stale = (cols and "uid" not in cols) or (
            q_sql and "REFERENCES curriculum_indicators(code)" in (q_sql[0] or "")
        )
        if stale:
            conn.execute("PRAGMA foreign_keys=OFF;")
            conn.execute("DROP TABLE IF EXISTS questions_fts;")
            conn.execute("DROP TABLE IF EXISTS questions;")
            conn.execute("DROP TABLE IF EXISTS curriculum_indicators;")
            conn.execute("PRAGMA foreign_keys=ON;")
        for ddl in ALL_DDL:
            conn.execute(ddl)
        q_cols = {row[1] for row in conn.execute("PRAGMA table_info(questions);").fetchall()}
        if "embedding" not in q_cols:
            conn.execute("ALTER TABLE questions ADD COLUMN embedding BLOB;")
        # Clean pre-existing duplicates, then apply unique guards.
        # FK checks off: question_occurrences.parent (harvested_files) may not
        # exist yet in fresh DBs — the legacy tables are created by CatalogDatabase.
        conn.execute("PRAGMA foreign_keys=OFF;")
        for dedupe in DEDUPE_QUERIES:
            conn.execute(dedupe)
        for ddl in UNIQUE_INDEXES:
            conn.execute(ddl)
        conn.execute("PRAGMA foreign_keys=ON;")
        conn.commit()
    finally:
        conn.close()


def fts_rebuild(conn: sqlite3.Connection) -> None:
    """Rebuild the external-content FTS index from the questions table."""
    conn.execute(
        "INSERT INTO questions_fts (questions_fts) VALUES ('rebuild');"
    )
