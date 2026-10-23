#!/usr/bin/env python3
"""Add Lesson 1 generated exercise questions to the BECE bank."""
from __future__ import annotations

import hashlib
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(r"W:\StaralexSchoolStudies\BECE_MOCK_PAPERS\data\metadata\catalog.db")
SOURCE_FILE = "Lesson_01_Place_Value_and_Standard_Form_generated_exercises"
LESSON = "Strand-1-Number/Substrand-1-Numeration-Systems/Lesson-01-Place-Value-And-Standard-Form"
YEAR = 2026
SUBJECT = "Mathematics"
NOW = datetime.now(timezone.utc).isoformat()


def norm(text: str) -> str:
    t = (text or "").lower()
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


# Generated questions (non-authentic) from Exercises 1–8 of Lesson 1.
# Paper 2 style = structured; Paper 1 style = objective with options where useful.
GENERATED = [
    # Ex1
    ("P2", "In the number 9 463 285, state the value of the digit 6.", "B9.1.1.1.1"),
    ("P2", "Write the place-value name of the digit 4 in 40 508 216.", "B9.1.1.1.1"),
    ("P2", "The digit 9 in 7 904 512 stands for what value?", "B9.1.1.1.1"),
    # Ex2
    ("P2", "Write 5 040 007 in words.", "B9.1.1.1.1"),
    ("P2", "Write three million, fifty thousand, eighty-two in figures.", "B9.1.1.1.1"),
    ("P2", "Arrange these in ascending order: 3 050 082; 3 005 820; 3 500 082; 3 050 802.", "B9.1.1.1.1"),
    ("P2", "A country's road network measures 38 040 km. Write this number in words.", "B9.1.1.1.1"),
    ("P1", "Which is larger: 4.7 million or 4 070 000?", "B9.1.1.1.1"),
    # Ex3
    ("P1", "Find the value of 124.3 + 0.275 + 74.06, correct to one decimal place.", "B9.1.2.2.1"),
    ("P2", "Round 12.473 to (i) 1 d.p. (ii) 2 d.p. (iii) 3 d.p.", "B9.1.1.1.1"),
    ("P2", "Round 0.997 84 to 2 d.p.", "B9.1.1.1.1"),
    ("P2", "Round 99.95 to 1 d.p.", "B9.1.1.1.1"),
    ("P2", "Calculate 18.4 × 1.27 and give the answer to 2 d.p.", "B9.1.2.2.1"),
    # Ex4
    ("P2", "Round 0.006 845 to (i) 1 s.f. (ii) 2 s.f. (iii) 3 s.f.", "B9.1.1.1.1"),
    ("P2", "Round 84 730 to (i) 1 s.f. (ii) 2 s.f. (iii) 3 s.f.", "B9.1.1.1.1"),
    ("P2", "Express 0.000 090 5 to 2 s.f.", "B9.1.1.1.1"),
    ("P2", "A bacterium measures 0.000 004 7 m across. Write this length to 1 s.f.", "B9.1.1.1.1"),
    # Ex5
    ("P2", "Write 47 300 in standard form.", "B9.1.1.1.1"),
    ("P2", "Write 0.000 56 in standard form.", "B9.1.1.1.1"),
    ("P2", "Write 602 000 000 000 000 in standard form.", "B9.1.1.1.1"),
    ("P2", "Write 0.000 000 034 in standard form.", "B9.1.1.1.1"),
    # Ex6
    ("P2", "Write 7.4 × 10^6 as an ordinary number.", "B9.1.1.1.1"),
    ("P2", "Write 9.05 × 10^-4 as an ordinary number.", "B9.1.1.1.1"),
    ("P2", "Write 2.16 × 10^4 as an ordinary number.", "B9.1.1.1.1"),
    ("P2", "Write 3.4 × 10^-8 as an ordinary number.", "B9.1.1.1.1"),
    # Ex7
    ("P2", "Find (5.2 × 10^4) − (1.8 × 10^4).", "B9.1.1.1.1"),
    ("P2", "Find (4.5 × 10^3) + (2.2 × 10^2).", "B9.1.1.1.1"),
    ("P2", "Find (3 × 10^4) × (2 × 10^3).", "B9.1.1.1.1"),
    ("P2", "Find (6.2 × 10^5) × (4 × 10^3).", "B9.1.1.1.1"),
    # Ex8
    ("P2", "Convert 2 days 3 hours into minutes and express the answer in standard form.", "B9.1.1.1.1"),
    ("P2", "The wavelength of green light is about 0.000 000 55 m. Write this in standard form.", "B9.1.1.1.1"),
    ("P2", "A town has 2.4 × 10^5 people. Write the population as an ordinary number.", "B9.1.1.1.1"),
    ("P2", "A company earns GH₵ 4 750 000 in a year. Write this in standard form and state the value of the digit 7.", "B9.1.1.1.1"),
]


def main() -> None:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON;")

    conn.execute(
        "INSERT OR IGNORE INTO sources (name, domain, source_type, acquisition, tos_notes, trusted) "
        "VALUES (?, ?, 'mock_compilation', 'generated_lesson', ?, 1);",
        (
            "Generated Lesson 1 exercises (Place Value & Standard Form)",
            "local://generated",
            "Original questions written for Staralex lesson packages. Free for study use.",
        ),
    )
    source_id = conn.execute(
        "SELECT id FROM sources WHERE domain = 'local://generated';"
    ).fetchone()[0]

    stats = {"new": 0, "dupe": 0, "occurrences": 0}
    with conn:
        for idx, (paper, text, ind) in enumerate(GENERATED, start=1):
            paper_type = "Paper 1 - Objective" if paper == "P1" else "Paper 2 - Essay"
            h = hashlib.sha256(
                f"mathematics|{norm(text)}".encode("utf-8")
            ).hexdigest()
            qid = f"Q_{h[:12]}"
            raw_id = f"{SOURCE_FILE}_q{idx}"

            cur = conn.execute("SELECT id FROM questions WHERE id = ?;", (qid,)).fetchone()
            if cur:
                stats["dupe"] += 1
            else:
                conn.execute(
                    """
                    INSERT INTO questions (
                        id, subject, question_text, option_a, option_b, option_c, option_d,
                        correct_answer, has_diagram, diagram_path, year, paper_type,
                        indicator_code, confidence, tag_method, dedup_hash, migrated_from, created_at
                    ) VALUES (?, ?, ?, '', '', '', '', '', 0, NULL, ?, ?, ?, 1.0, 'generated_lesson_exercises', ?, ?, ?);
                    """,
                    (qid, SUBJECT, text, YEAR, paper_type, ind, h, raw_id, NOW),
                )
                stats["new"] += 1

            conn.execute(
                """
                INSERT OR IGNORE INTO question_occurrences (
                    question_id, original_id, source_file, harvested_file_id,
                    source_id, original_url, year, paper_type, question_number, created_at
                ) VALUES (?, ?, ?, NULL, ?, ?, ?, ?, ?, ?);
                """,
                (
                    qid,
                    raw_id,
                    SOURCE_FILE,
                    source_id,
                    f"local://generated/{LESSON}",
                    YEAR,
                    paper_type,
                    idx,
                    NOW,
                ),
            )
            stats["occurrences"] += 1

        conn.execute("INSERT INTO questions_fts (questions_fts) VALUES ('rebuild');")

    conn.close()
    print("Generated-question ingest:", stats)


if __name__ == "__main__":
    main()
