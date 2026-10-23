"""Tests for permanent reject ledger + download skip logic."""

from pathlib import Path

from src.classifier import FileClassifier
from src.database import CatalogDatabase


def test_rejected_content_is_permanent_and_blocks_refetch(tmp_path: Path):
    db = CatalogDatabase(db_path=tmp_path / "cat.db")
    sha = "a" * 64

    assert db.is_hash_rejected(sha) is False
    assert db.is_content_known(sha) is False

    assert db.record_rejected_content(
        sha256=sha,
        reason="not_exam_paper",
        original_url="https://example.com/lesson-notes.pdf",
        file_name="lesson-notes.pdf",
        file_type=".pdf",
        details="scheme of work",
    ) is True

    # Second insert is a no-op (same hash never duplicated)
    assert db.record_rejected_content(sha256=sha, reason="not_exam_paper") is False

    assert db.is_hash_rejected(sha) is True
    assert db.is_content_known(sha) is True

    # Even after any local file is deleted, the hash stays known
    rows = db.list_rejected_content(reason="not_exam_paper")
    assert any(r["sha256"] == sha for r in rows)


def test_kept_file_hash_is_also_known(tmp_path: Path):
    db = CatalogDatabase(db_path=tmp_path / "cat.db")
    sha = "b" * 64
    db.save_harvested_file(
        sha256=sha,
        original_url="https://example.com/bece-maths.pdf",
        file_name="bece-maths.pdf",
        file_type="pdf",
        subject="Mathematics",
        file_size=10,
        local_path="x/bece-maths.pdf",
        source_domain="example.com",
    )
    assert db.is_content_known(sha) is True
    assert db.is_hash_rejected(sha) is False


def test_reject_reason_lesson_notes_vs_exam_paper():
    notes = b"Scheme of work for term one lesson notes curriculum guide textbook"
    exam = b"BECE MOCK MATHEMATICS Paper 1 Objective questions and answers 2024"

    assert FileClassifier.reject_reason(notes, ".txt", "lesson notes scheme of work") == "not_exam_paper"
    assert FileClassifier.reject_reason(exam, ".txt", "BECE mock paper 1") is None
