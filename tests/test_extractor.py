import json
import pytest
from src.question_extractor import QuestionExtractor


@pytest.fixture
def temp_extractor(tmp_path):
    db_file = tmp_path / "test_questions.db"
    return QuestionExtractor(db_path=db_file)


def test_parse_txt_questions(temp_extractor, tmp_path):
    txt_content = """
    MATHEMATICS MOCK EXAMINATION 2024
    PAPER 1 - OBJECTIVE TEST

    1. Which of the following is a prime number?
    A. 4
    B. 7
    C. 9
    D. 12

    2. Evaluate 3x + 5 = 20. Find x.
    A. 3
    B. 5
    C. 7
    D. 15

    3. Calculate the area of a circle with radius 7 cm.
    A. 154 cm^2
    B. 44 cm^2
    C. 88 cm^2
    D. 308 cm^2
    """
    exam_file = tmp_path / "Mathematics_2024_Mock_Paper.txt"
    exam_file.write_text(txt_content, encoding="utf-8")

    questions = temp_extractor.parse_txt(exam_file, "Mathematics")
    assert len(questions) == 3
    assert questions[0]["question_number"] == 1
    assert "prime number" in questions[0]["question_text"]
    assert questions[0]["option_a"] == "4"
    assert questions[0]["option_b"] == "7"

    assert questions[1]["question_number"] == 2
    assert questions[1]["option_b"] == "5"

    assert questions[2]["question_number"] == 3
    assert questions[2]["option_a"] == "154 cm^2"


def test_save_questions_batch(temp_extractor):
    mock_batch = [
        {
            "id": "Math_2024_q1",
            "subject": "Mathematics",
            "year": 2024,
            "paper_type": "Objective",
            "question_number": 1,
            "question_text": "Sample test question 1",
            "option_a": "1",
            "option_b": "2",
            "option_c": "3",
            "option_d": "4",
            "correct_answer": "B",
            "has_diagram": 0,
            "diagram_path": None,
            "source_file": "sample.docx"
        },
        {
            "id": "Math_2024_q2",
            "subject": "Mathematics",
            "year": 2024,
            "paper_type": "Objective",
            "question_number": 2,
            "question_text": "Sample test question 2 with diagram",
            "option_a": "10",
            "option_b": "20",
            "option_c": "30",
            "option_d": "40",
            "correct_answer": "C",
            "has_diagram": 1,
            "diagram_path": "extracted_questions/images/fig1.png",
            "source_file": "sample.docx"
        }
    ]

    temp_extractor.save_questions_batch(mock_batch)

    import sqlite3
    with sqlite3.connect(str(temp_extractor.db_path)) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM extracted_questions ORDER BY question_number;").fetchall()
        assert len(rows) == 2
        assert rows[0]["id"] == "Math_2024_q1"
        assert rows[0]["correct_answer"] == "B"
        assert rows[1]["has_diagram"] == 1
