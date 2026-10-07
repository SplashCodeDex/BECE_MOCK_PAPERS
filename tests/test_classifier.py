import pytest
from src.classifier import FileClassifier


def test_detect_subject_mathematics():
    text = "BECE 2023 Mathematics Paper 2 Section A Solve the quadratic equation 2x^2 + 5x - 3 = 0"
    subject = FileClassifier.detect_subject(text)
    assert subject == "Mathematics"


def test_detect_subject_computing_ict():
    text = "Basic Education Certificate Examination Information and Communications Technology ICT Computing CPU flowchart algorithm"
    subject = FileClassifier.detect_subject(text)
    assert subject == "Computing_ICT"


def test_detect_subject_cdt_cad():
    text = "Career Technology and Design Technical Drawing isometric drawing orthographic projection woodworking tools"
    subject = FileClassifier.detect_subject(text)
    assert subject == "CDT_CAD"


def test_detect_subject_unclassified():
    text = "General English Language Comprehension and Essay Writing 2022"
    subject = FileClassifier.detect_subject(text)
    assert subject == "General_Unclassified"


def test_sanitize_filename():
    raw_name = "Mock Exam 2024 (Maths & Science) / Final!.pdf"
    clean = FileClassifier.sanitize_filename(
        raw_name=raw_name,
        subject="Mathematics",
        sha256="abc12345def67890",
        extension=".pdf",
        context_text="2024 BECE Mock Examination"
    )
    assert clean.endswith(".pdf")
    assert "Mathematics" in clean
    assert "2024" in clean
    assert "/" not in clean
    assert "!" not in clean


def test_detect_subject_from_bytes():
    sample_text = b"Basic Education Certificate Examination Computing Information and Communications Technology"
    subj = FileClassifier.detect_subject_from_bytes(sample_text, ".txt", "bece mock")
    assert subj == "Computing_ICT"
