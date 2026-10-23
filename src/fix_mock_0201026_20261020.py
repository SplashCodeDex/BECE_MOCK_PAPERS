#!/usr/bin/env python3
"""One-off corrections for mock 0201-026/27 (verified against user close-up photos 2026-10-20).

Fixes:
  1. P1 Q8  Kojo's age            -> C (10)   [was D]
  2. P1 Q10 12x + 9q               -> B (159)  [was C]
  3. P1 Q18 5 - 5(3 - y) <= 65    -> A ({5,10,15})  [was C]
  4. P1 Q27 XY = YZ, angle XYZ 42 -> D (69)   [was B]
  5. P2 4c text 1/4 -> 1 1/4 (mixed number per photo)
  6. P2 6c text garbled x/t -> numerals 4
Left intentionally unchanged (flagged, to revisit during lessons): P2 6d vector components,
P1 Q31 angle MON value.
"""
import sqlite3

DB = r"data/metadata/catalog.db"
conn = sqlite3.connect(DB)
conn.execute("PRAGMA foreign_keys=ON;")

# (text_like, field, old_value, new_value, label)
KEY_FIXES = [
    ("%Kojo%age%", "correct_answer", "D", "C", "P1 Q8 Kojo"),
    ("%12x + 9q%", "correct_answer", "C", "B", "P1 Q10 12x+9q"),
    ("%5(3 − y) ≤ 65%", "correct_answer", "C", "A", "P1 Q18 inequality"),
    ("%XY = YZ%", "correct_answer", "B", "D", "P1 Q27 isosceles"),
]
TEXT_FIXES = [
    ("%25x^(-4)%", "(25x^(-4)) / (5^(-3) × 10x × t^(-8))",
     "(25 × 4^(-4)) / (5^(-3) × 10 × 4^(-8))", "P2 6c simplify"),
    ("%Evaluate 2/3%", "× 1/4 +", "× 1¼ +", "P2 4c BODMAS"),
]


def show(text):
    return " | ".join(f"{k}={v}" for k, v in text.items() if v)


with conn:
    for like, field, old, new, label in KEY_FIXES:
        cur = conn.execute(
            f"UPDATE questions SET {field} = ? WHERE question_text LIKE ? AND {field} = ?",
            (new, like, old),
        )
        cur2 = conn.execute(
            f"UPDATE extracted_questions SET {field} = ? "
            "WHERE question_text LIKE ? AND source_file LIKE '%user_mock_0201026%' AND subject = 'Mathematics'",
            (new, like),
        )
        print(f"[key] {label}: canonical rows={cur.rowcount}, extracted rows={cur2.rowcount}")

    for like, old_frag, new_frag, label in TEXT_FIXES:
        cur = conn.execute(
            "UPDATE questions SET question_text = REPLACE(question_text, ?, ?) "
            "WHERE question_text LIKE ?",
            (old_frag, new_frag, like),
        )
        cur2 = conn.execute(
            "UPDATE extracted_questions SET question_text = REPLACE(question_text, ?, ?) "
            "WHERE question_text LIKE ? AND source_file LIKE '%user_mock_0201026%' AND subject = 'Mathematics'",
            (old_frag, new_frag, like),
        )
        print(f"[text] {label}: canonical rows={cur.rowcount}, extracted rows={cur2.rowcount}")

conn.execute("INSERT INTO questions_fts (questions_fts) VALUES ('rebuild');")

print("\n--- verification ---")
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
checks = [
    ("%Kojo%age%", "Kojo"),
    ("%12x + 9q%", "12x+9q"),
    ("%3 − y%", "ineq18"),
    ("%XY = YZ%", "isosceles27"),
    ("%25 × 4^(-4)%", "idx6c"),
    ("%1¼%", "frac4c"),
]
for like, label in checks:
    rows = conn.execute(
        "SELECT correct_answer, substr(question_text, 1, 90) FROM questions WHERE question_text LIKE ?",
        (like,),
    ).fetchall()
    for r in rows:
        print(f"{label}: key={r[0]!r} text={r[1]}")
conn.close()
print("done")
