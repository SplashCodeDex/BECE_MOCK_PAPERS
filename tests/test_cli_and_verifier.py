"""Tests for `src/verifier.py` and `src/bece_cli.py`."""

import json
from pathlib import Path
import sqlite3

from src.bank_schema import init_bank_schema
from src.bece_cli import main as cli_main
from src.verifier import (
    verify_against_marking_scheme,
    verify_solution,
    verify_sympy_equivalence,
)


def test_sympy_equivalence_surds_and_algebra():
    # 1 / (sqrt(3) - 1) == (sqrt(3) + 1) / 2
    res = verify_sympy_equivalence("1 / (sqrt(3) - 1)", "(sqrt(3) + 1) / 2")
    assert res.passed is True
    assert res.verification_type == "sympy_verified"

    # Algebraic expansion: (x + 2)*(x - 3) == x^2 - x - 6
    res2 = verify_sympy_equivalence("(x + 2)*(x - 3)", "x^2 - x - 6")
    assert res2.passed is True

    # Mismatch check
    res_bad = verify_sympy_equivalence("1 / (sqrt(3) - 1)", "(sqrt(3) - 1) / 2")
    assert res_bad.passed is False


def test_sympy_preserves_algebraic_m():
    """Unit cleanup must not strip the symbol m (regression: metre filter ate it)."""
    res = verify_sympy_equivalence("(m + n)*(2*x - y) - x*(m + n)", "(m + n)*(x - y)")
    assert res.passed is True
    assert "m" in res.normalized_answer
    assert res.normalized_answer.replace(" ", "") in {"(m+n)*(x-y)", "(x-y)*(m+n)"}

    # Digit-attached unit m is still stripped without breaking equality
    res_unit = verify_sympy_equivalence("5m", "5")
    assert res_unit.passed is True

    # And a true mismatch involving m must still fail
    res_fail = verify_sympy_equivalence("(m + n)*(x - y)", "m*n")
    assert res_fail.passed is False


def test_prose_answers_not_treated_as_algebra():
    """English answers on Maths questions must not 'verify' as symbol products."""
    q = {"subject": "Mathematics", "correct_answer": ""}
    res = verify_solution(
        q,
        steps := "P = {3, 6, 9, 12, 15} are multiples of 3 less than 18.",
        "The set of multiples of 3 less than 18",
    )
    assert res.verification_type != "sympy_verified"
    assert res.passed is True  # still passes the pedagogical rubric
    assert "e**4" not in res.details


def test_marking_scheme_verification():
    q_row = {
        "id": "Q_math01",
        "subject": "Mathematics",
        "question_text": "Simplify 1 / (sqrt(3) - 1).",
        "option_a": "(sqrt(3) + 1) / 2",
        "option_b": "(sqrt(3) - 1) / 2",
        "option_c": "sqrt(3)",
        "option_d": "2",
        "correct_answer": "A",
    }
    assert verify_against_marking_scheme("A", q_row).passed is True
    assert verify_against_marking_scheme("Option A", q_row).passed is True
    assert verify_against_marking_scheme("1 / (sqrt(3) - 1)", q_row).passed is True
    assert verify_against_marking_scheme("B", q_row).passed is False


def test_bece_cli_query_and_save_solution(tmp_path: Path, capsys):
    db_path = tmp_path / "cli_test.db"
    init_bank_schema(db_path)

    conn = sqlite3.connect(str(db_path))
    conn.executemany(
        """
        INSERT INTO curriculum_indicators (
            uid, code, grade, subject, strand_number, strand_title,
            substrand_number, substrand_title, content_standard,
            content_standard_text, indicator_text, prerequisite_codes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        [
            (
                "Mathematics:B9.1.1.2.2",
                "B9.1.1.2.2",
                "B9",
                "Mathematics",
                1,
                "NUMBER",
                1,
                "Number Operations",
                "B9.1.1.2",
                "Operations on surds",
                "Simplify and rationalise surds",
                json.dumps(["B8.1.1.2.1"]),
            ),
            (
                "Mathematics:B8.1.1.2.1",
                "B8.1.1.2.1",
                "B8",
                "Mathematics",
                1,
                "NUMBER",
                1,
                "Number Operations",
                "B8.1.1.2",
                "Roots and powers",
                "Evaluate square roots and cube roots",
                json.dumps([]),
            ),
        ],
    )
    conn.executemany(
        """
        INSERT INTO questions (
            id, subject, question_text, option_a, option_b, option_c, option_d,
            correct_answer, indicator_code, confidence, tag_method, dedup_hash, year, paper_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        [
            (
                "Q_cli_surd01",
                "Mathematics",
                "Rationalise the denominator of 2 / (sqrt(5) - 1).",
                "(sqrt(5)+1)/2",
                "(sqrt(5)-1)/2",
                "sqrt(5)",
                "4",
                "A",
                "B9.1.1.2.2",
                0.92,
                "embeddinggemma2+lexical",
                "hash_cli_1",
                2023,
                "Paper 1",
            ),
            (
                "Q_cli_prereq1",
                "Mathematics",
                "Find the positive square root of 144.",
                "10",
                "12",
                "14",
                "16",
                "B",
                "B8.1.1.2.1",
                0.89,
                "embeddinggemma2+lexical",
                "hash_cli_2",
                2021,
                "Paper 1",
            ),
        ],
    )
    conn.commit()
    conn.close()

    # 1. Query with prerequisite expansion
    rc = cli_main(["--db", str(db_path), "query", "--indicator", "B9.1.1.2.2", "--format", "json"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["count"] == 2
    assert set(out["target_indicators"]) == {"B9.1.1.2.2", "B8.1.1.2.1"}

    # 2. Save a SymPy-verified worked solution
    rc_sol = cli_main(
        [
            "--db",
            str(db_path),
            "save-solution",
            "--id",
            "Q_cli_surd01",
            "--lesson",
            "Strand-1-Number/Lesson-04-Surds",
            "--answer",
            "A",
            "--sympy-lhs",
            "2 / (sqrt(5) - 1)",
            "--sympy-rhs",
            "(sqrt(5) + 1) / 2",
            "--steps",
            "Step 1: Multiply top and bottom by the conjugate (sqrt(5) + 1).\nStep 2: 2*(sqrt(5)+1)/(5-1) = (sqrt(5)+1)/2.",
        ]
    )
    assert rc_sol == 0
    sol_out = json.loads(capsys.readouterr().out)
    assert sol_out["status"] == "saved"
    assert sol_out["verification_type"] == "sympy_verified"

    # 3. Verify solution is returned when querying the question again
    rc_q2 = cli_main(["--db", str(db_path), "query", "--indicator", "B9.1.1.2.2", "--no-include-prerequisites", "--format", "json"])
    assert rc_q2 == 0
    out2 = json.loads(capsys.readouterr().out)
    assert out2["count"] == 1
    assert len(out2["questions"][0]["solutions"]) == 1
    assert out2["questions"][0]["solutions"][0]["final_answer"] == "A"


def test_bece_cli_coverage_topic_resolution(tmp_path: Path, capsys):
    db_path = tmp_path / "coverage_test.db"
    init_bank_schema(db_path)

    conn = sqlite3.connect(str(db_path))
    conn.executemany(
        """
        INSERT INTO curriculum_indicators (
            uid, code, grade, subject, strand_number, strand_title,
            substrand_number, substrand_title, content_standard,
            content_standard_text, indicator_text, prerequisite_codes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        [
            (
                "Mathematics:B7.2.2.1.2",
                "B7.2.2.1.2",
                "B7",
                "Mathematics",
                2,
                "ALGEBRA",
                2,
                "Algebraic Expressions",
                "B7.2.2.1",
                "Algebraic Expressions",
                "Perform addition and subtraction of algebraic expressions.",
                json.dumps([]),
            ),
            (
                "Mathematics:B9.2.2.1.3",
                "B9.2.2.1.3",
                "B9",
                "Mathematics",
                2,
                "ALGEBRA",
                2,
                "Algebraic Expressions",
                "B9.2.2.1",
                "Algebraic Expressions",
                "Factorise expressions that have simple binomial.",
                json.dumps([]),
            ),
            (
                "Computing_ICT:B7.2.2.1.2",
                "B7.2.2.1.2",
                "B7",
                "Computing_ICT",
                2,
                "PRODUCTIVITY SOFTWARE",
                2,
                "INTRODUCTION TO PRESENTATION SOFTWARE",
                "B7.2.2.1",
                "Presentation Software",
                "Explore features of MS-PowerPoint interface. Code collides with Maths Algebraic Expressions.",
                json.dumps([]),
            ),
        ],
    )
    conn.executemany(
        """
        INSERT INTO questions (
            id, subject, question_text, option_a, option_b, option_c, option_d,
            correct_answer, indicator_code, confidence, tag_method, dedup_hash, year, paper_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        [
            (
                "Q_cov_ae01",
                "Mathematics",
                "Simplify 3x + 5x.",
                "8x",
                "2x",
                "15x",
                "x",
                "A",
                "B7.2.2.1.2",
                0.9,
                "embeddinggemma2+lexical",
                "hash_cov_1",
                2020,
                "Paper 1",
            ),
            (
                "Q_cov_ae02",
                "Mathematics",
                "Factorise x^2 + 5x + 6.",
                "(x+2)(x+3)",
                "(x+1)(x+6)",
                "(x-2)(x-3)",
                "x(x+5)",
                "A",
                "B9.2.2.1.3",
                0.4,
                "embeddinggemma2+lexical",
                "hash_cov_2",
                2021,
                "Paper 2",
            ),
            (
                "Q_cov_code_collide",
                "Computing_ICT",
                "Which pane shows slide thumbnails in PowerPoint?",
                "Slide pane",
                "Notes pane",
                "Ribbon",
                "Status bar",
                "A",
                "B7.2.2.1.2",
                0.95,
                "embeddinggemma2+lexical",
                "hash_cov_3",
                2022,
                "Paper 1",
            ),
            (
                "Q_cov_orphan",
                "Mathematics",
                "Question tagged with a code missing from curriculum_indicators.",
                "A",
                "B",
                "C",
                "D",
                "A",
                "B9.9.9.9.9",
                0.5,
                "manual",
                "hash_cov_4",
                2023,
                "Paper 1",
            ),
        ],
    )
    conn.commit()
    conn.close()

    rc = cli_main(
        [
            "--db",
            str(db_path),
            "coverage",
            "--topic",
            "Algebraic Expressions",
            "--subject",
            "Mathematics",
            "--format",
            "json",
        ]
    )
    assert rc == 0
    out = json.loads(capsys.readouterr().out)

    assert out["resolution"] == "substrand_exact"
    assert out["totals"]["indicators"] == 2
    assert out["totals"]["questions"] == 2
    assert out["totals"]["low_confidence_questions"] == 1
    assert out["totals"]["years_covered"] == [2020, 2021]
    # Computing B7.2.2.1.2 is a valid Presentation Software tag (code collision),
    # not a mis-tag. Only the B9.9.9.9.9 pair is a true orphan.
    assert out["completeness_check"]["orphan_indicator_tags"] == 1
    assert {i["code"] for i in out["indicators"]} == {"B7.2.2.1.2", "B9.2.2.1.3"}

    rc_topics = cli_main(
        ["--db", str(db_path), "coverage", "--list-topics", "--has-questions", "--format", "json"]
    )
    assert rc_topics == 0
    topics_out = json.loads(capsys.readouterr().out)
    topic_rows = {
        (t["subject"], t["substrand_title"]): t["question_count"] for t in topics_out["topics"]
    }
    assert topic_rows[("Mathematics", "Algebraic Expressions")] == 2
    assert topic_rows[("Computing_ICT", "INTRODUCTION TO PRESENTATION SOFTWARE")] == 1


def test_bece_cli_diagrams(capsys):
    # Test list all canonical diagrams in json format
    rc = cli_main(["diagrams", "--format", "json"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["count"] == 46
    assert len(out["diagrams"]) == 46

    # Test filter by ID
    rc = cli_main(["diagrams", "--id", "5", "--format", "json"])
    assert rc == 0
    out_id = json.loads(capsys.readouterr().out)
    assert out_id["count"] == 1
    assert out_id["diagrams"][0]["id"] == 5
    assert out_id["diagrams"][0]["skill"] == "diagram-05-angle-bisector-construction"

    # Test filter by indicator prefix
    rc = cli_main(["diagrams", "--indicator", "B9.3.3", "--format", "json"])
    assert rc == 0
    out_ind = json.loads(capsys.readouterr().out)
    assert out_ind["count"] >= 2
    for d in out_ind["diagrams"]:
        assert d["indicator_code"].startswith("B9.3.3")

    # Test text format
    rc = cli_main(["diagrams", "--grade", "B8", "--format", "text"])
    assert rc == 0
    text_out = capsys.readouterr().out
    assert "diagram_06_bearing_three_figure" in text_out
    assert "(B8)" in text_out
