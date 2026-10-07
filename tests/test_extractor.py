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


def test_table_to_markdown():
    import docx
    doc = docx.Document()
    tbl = doc.add_table(rows=2, cols=3)
    tbl.rows[0].cells[0].text = "Age"
    tbl.rows[0].cells[1].text = "12"
    tbl.rows[0].cells[2].text = "13"
    tbl.rows[1].cells[0].text = "Freq"
    tbl.rows[1].cells[1].text = "5"
    tbl.rows[1].cells[2].text = "8"

    md = QuestionExtractor.table_to_markdown(tbl)
    assert "| Age | 12 | 13 |" in md
    assert "| Freq | 5 | 8 |" in md
    assert "---" in md


def test_stimulus_pattern_matching():
    from src.question_extractor import STIMULUS_PATTERNS
    samples = [
        "Figure I show the pictorial view of a block. Use it to answer questions 3 and 4.",
        "Use the diagram below to answer questions 15 to 17.",
        "Study the table below carefully and answer questions 32 and 33."
    ]
    for s in samples:
        matched = any(p.search(s) for p in STIMULUS_PATTERNS)
        assert matched is True


def test_export_catalog(temp_extractor, tmp_path):
    temp_extractor.save_question({
        "id": "Math_2024_test_q1",
        "subject": "Mathematics",
        "year": 2024,
        "paper_type": "Objective",
        "question_number": 1,
        "question_text": "Export test question",
        "option_a": "A",
        "option_b": "B",
        "option_c": "C",
        "option_d": "D",
        "correct_answer": "A",
        "has_diagram": 0,
        "diagram_path": None,
        "source_file": "test.docx"
    })
    # Export and verify
    temp_extractor.export_catalog()
    from src.question_extractor import JSON_EXPORT_PATH
    assert JSON_EXPORT_PATH.exists()


def test_parse_pdf_questions(temp_extractor, tmp_path):
    import pymupdf
    pdf_path = tmp_path / "Test_Mock_2024.pdf"
    doc = pymupdf.open()
    page = doc.new_page()
    content = (
        "2024 BECE MOCK EXAMINATION\n"
        "PAPER 1 - OBJECTIVE TEST\n"
        "1. What is an algorithm?\n"
        "A. A step-by-step procedure\n"
        "B. A computer virus\n"
        "C. A programming language\n"
        "D. A monitor display\n"
        "2. Which device is used for output?\n"
        "A. Keyboard\n"
        "B. Mouse\n"
        "C. Printer\n"
        "D. Scanner\n"
    )
    # PyMuPDF expects 500+ chars to distinguish from scanned booklets, add padding comments
    padding = "Instructions: Read all questions carefully before answering. " * 15
    page.insert_text((50, 50), content + "\n" + padding)
    doc.save(pdf_path)
    doc.close()

    questions = temp_extractor.parse_pdf(pdf_path, "Computing_ICT")
    assert len(questions) == 2
    assert questions[0]["question_number"] == 1
    assert "algorithm" in questions[0]["question_text"]
    assert questions[0]["option_a"] == "A step-by-step procedure"
    assert questions[1]["question_number"] == 2
    assert questions[1]["option_c"] == "Printer"


