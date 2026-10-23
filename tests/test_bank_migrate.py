import sqlite3

import pytest

from src.bank_migrate import dedup_hash, migrate, normalize_for_dedup
from src.bank_schema import init_bank_schema


@pytest.fixture
def seeded_legacy_db(tmp_path):
    """Legacy-format DB with harvested_files + extracted_questions."""
    db_file = tmp_path / "test_catalog.db"
    init_bank_schema(db_file)
    conn = sqlite3.connect(str(db_file))
    conn.executescript(
        """
        CREATE TABLE harvested_files (
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

        INSERT INTO harvested_files
            (sha256, original_url, file_name, file_type, subject, file_size,
             local_path, source_domain)
        VALUES
            ('abc111', 'https://mickinetsystems.com/maths2019.pdf',
             'Mathematics_2019_maths_a1b2c3.pdf', '.pdf', 'Mathematics', 100,
             'data/harvested/Mathematics/maths.pdf', 'mickinetsystems.com'),
            ('abc222', 'https://ghanaeducation.org/ict2020.pdf',
             'Computing_ICT_2020_ict_d4e5f6.pdf', '.pdf', 'Computing_ICT', 100,
             'data/harvested/Computing_ICT/ict.pdf', 'ghanaeducation.org');

        CREATE TABLE extracted_questions (
            id TEXT PRIMARY KEY,
            subject TEXT NOT NULL,
            year INTEGER,
            paper_type TEXT NOT NULL,
            question_number INTEGER,
            question_text TEXT NOT NULL,
            option_a TEXT, option_b TEXT, option_c TEXT, option_d TEXT,
            correct_answer TEXT,
            has_diagram INTEGER DEFAULT 0,
            diagram_path TEXT,
            source_file TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        INSERT INTO extracted_questions VALUES
            ('MATH_q1', 'Mathematics', 2019, 'Paper 1 - Objective', 1,
             'Simplify: 2x + 3x', '5x', '6x', 'x', '7x', 'A',
             0, NULL, 'Mathematics_2019_maths_a1b2c3.pdf', '2026-01-01'),
            ('MATH_q1_dup', 'Mathematics', NULL, 'Paper 1 - Objective', 1,
             '  simplify: 2x +  3x!! ', '5x', '6x', 'x', '7x', '',
             0, NULL, 'Mathematics_2019_maths_a1b2c3.pdf', '2026-01-02'),
            ('ICT_q1', 'Computing_ICT', 2020, 'Paper 2 - Theory', 3,
             'Explain three uses of a mouse.', NULL, NULL, NULL, NULL, '',
             0, NULL, 'Computing_ICT_2020_ict_d4e5f6.pdf', '2026-01-01');
        """
    )
    conn.commit()
    conn.close()
    return db_file


def test_dedup_normalization_and_hash():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE t (subject TEXT, question_text TEXT, paper_type TEXT,"
        " option_a TEXT, option_b TEXT, option_c TEXT, option_d TEXT)"
    )
    conn.execute(
        "INSERT INTO t VALUES ('Mathematics', 'Simplify:  2x + 3x', 'Paper 1 - Objective',"
        " '5x', '6x', 'x', '7x')"
    )
    conn.execute(
        "INSERT INTO t VALUES ('Mathematics', 'simplify: 2x+3x!!', 'Paper 1 - Objective',"
        " '5x', '6x', 'x', '7x')"
    )
    conn.execute(
        "INSERT INTO t VALUES ('Mathematics', 'simplify: 2x+3x!!', 'Paper 1 - Objective',"
        " '5y', '6x', 'x', '7x')"
    )
    rows = conn.execute("SELECT * FROM t").fetchall()
    assert normalize_for_dedup(rows[0]) == normalize_for_dedup(rows[1])
    assert dedup_hash(rows[0]) == dedup_hash(rows[1])
    # Different options on an objective paper => different question
    assert dedup_hash(rows[1]) != dedup_hash(rows[2])


def test_migrate_creates_canonical_and_occurrences(seeded_legacy_db):
    stats = migrate(db_path=seeded_legacy_db)
    assert stats["legacy_rows"] == 3
    assert stats["canonical_questions"] == 2  # MATH_q1 + MATH_q1_dup collapse
    assert stats["duplicates_merged"] == 1
    assert stats["occurrences"] == 3

    conn = sqlite3.connect(str(seeded_legacy_db))
    conn.row_factory = sqlite3.Row
    q = conn.execute("SELECT * FROM questions").fetchall()
    assert len(q) == 2
    occs = conn.execute("SELECT * FROM question_occurrences").fetchall()
    assert len(occs) == 3
    # Provenance: every occurrence links back to the harvested file + URL
    for oc in occs:
        assert oc["harvested_file_id"] is not None
        assert oc["original_url"].startswith("https://")


def test_migrate_preserves_best_data(seeded_legacy_db):
    migrate(db_path=seeded_legacy_db)
    conn = sqlite3.connect(str(seeded_legacy_db))
    conn.row_factory = sqlite3.Row
    math_q = conn.execute(
        "SELECT * FROM questions WHERE subject = 'Mathematics';"
    ).fetchone()
    # Answer from MATH_q1 kept even though the duplicate row had it empty
    assert math_q["correct_answer"] == "A"
    # Year backfilled from the row that had one
    assert math_q["year"] == 2019


def test_migrate_seeds_sources_registry(seeded_legacy_db):
    migrate(db_path=seeded_legacy_db)
    conn = sqlite3.connect(str(seeded_legacy_db))
    domains = {r[0] for r in conn.execute("SELECT domain FROM sources;")}
    assert domains == {"mickinetsystems.com", "ghanaeducation.org"}


def test_migrate_is_idempotent(seeded_legacy_db):
    migrate(db_path=seeded_legacy_db)
    stats2 = migrate(db_path=seeded_legacy_db)
    assert stats2["canonical_questions"] == 2
    assert stats2["occurrences"] == 3  # INSERT OR IGNORE, no growth


def test_dry_run_leaves_no_rows(seeded_legacy_db):
    migrate(db_path=seeded_legacy_db, dry_run=True)
    conn = sqlite3.connect(str(seeded_legacy_db))
    assert conn.execute("SELECT COUNT(*) FROM questions;").fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM question_occurrences;").fetchone()[0] == 0
