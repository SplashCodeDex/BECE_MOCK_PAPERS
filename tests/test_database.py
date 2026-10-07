import json
import pytest
from src.database import CatalogDatabase


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_catalog.db"
    return CatalogDatabase(db_path=db_file)


def test_db_initialization(temp_db):
    assert temp_db.db_path.exists()


def test_visited_urls(temp_db):
    url = "https://ghanaeducation.org/bece-mock-2024"
    assert not temp_db.is_url_visited(url)

    temp_db.record_url_visited(url, 200)
    assert temp_db.is_url_visited(url)


def test_save_harvested_file_and_deduplication(temp_db, tmp_path):
    fake_file = tmp_path / "math_mock.pdf"
    fake_file.write_bytes(b"dummy pdf content")

    sha256 = "11223344556677889900aabbccddeeff11223344556677889900aabbccddeeff"
    saved = temp_db.save_harvested_file(
        sha256=sha256,
        original_url="https://passco.com.gh/math.pdf",
        file_name="Mathematics_2024_Mock.pdf",
        file_type=".pdf",
        subject="Mathematics",
        file_size=fake_file.stat().st_size,
        local_path=str(fake_file),
        source_domain="passco.com.gh"
    )
    assert saved is True
    assert temp_db.is_hash_seen(sha256) is True

    # Duplicate save should be rejected (returns False)
    duplicate_saved = temp_db.save_harvested_file(
        sha256=sha256,
        original_url="https://passco.com.gh/math_copy.pdf",
        file_name="Mathematics_2024_Mock_copy.pdf",
        file_type=".pdf",
        subject="Mathematics",
        file_size=fake_file.stat().st_size,
        local_path=str(fake_file),
        source_domain="passco.com.gh"
    )
    assert duplicate_saved is False


def test_export_catalog_json(temp_db, tmp_path):
    json_path = tmp_path / "catalog.json"
    temp_db.save_harvested_file(
        sha256="aabbccddeeff00112233445566778899aabbccddeeff00112233445566778899",
        original_url="https://becezone.com/ict.docx",
        file_name="Computing_Mock.docx",
        file_type=".docx",
        subject="Computing_ICT",
        file_size=1024,
        local_path="/tmp/ict.docx",
        source_domain="becezone.com"
    )
    records = temp_db.export_catalog_json(export_path=json_path)
    assert len(records) == 1
    assert records[0]["subject"] == "Computing_ICT"
    assert json_path.exists()
