import logging
import shutil
from pathlib import Path
from src.classifier import FileClassifier
from src.config import HARVESTED_DIR
from src.database import CatalogDatabase

logger = logging.getLogger("CatalogOrganizer")


def reclassify_and_reorganize() -> int:
    """
    Scans files across HARVESTED_DIR, inspects their text content
    using PyMuPDF / python-docx, and places any detected Mathematics, Computing,
    CDT/CAD, or non-target subjects into their proper directory while updating the database.
    """
    db = CatalogDatabase()
    if not HARVESTED_DIR.exists():
        return 0

    reclassified_count = 0

    for file_path in list(HARVESTED_DIR.rglob("*.*")):
        if not file_path.is_file():
            continue

        ext = file_path.suffix.lower()
        current_subject = file_path.parts[len(HARVESTED_DIR.parts)]

        try:
            content = file_path.read_bytes()
        except Exception:
            continue

        detected_subject = FileClassifier.detect_subject_from_bytes(
            content=content,
            extension=ext,
            text_context=file_path.name
        )

        if detected_subject != current_subject:
            # Determine new path
            clean_name = FileClassifier.sanitize_filename(
                raw_name=file_path.name,
                subject=detected_subject,
                sha256=file_path.name.split("_")[-1].split(".")[0],
                extension=ext
            )
            dest_path = FileClassifier.get_destination_path(
                subject=detected_subject,
                extension=ext,
                clean_filename=clean_name
            )

            # Move file
            shutil.move(str(file_path), str(dest_path))

            # Update database record
            with db.get_connection() as conn:
                conn.execute(
                    """
                    UPDATE harvested_files 
                    SET subject = ?, local_path = ?, file_name = ?
                    WHERE local_path = ? OR file_name = ?;
                    """,
                    (detected_subject, str(dest_path), clean_name, str(file_path), file_path.name)
                )

            reclassified_count += 1
            logger.info(f"Reclassified: {file_path.name} [{current_subject}] -> [{detected_subject}] {dest_path.name}")

    db.export_catalog_json()
    return reclassified_count


if __name__ == "__main__":
    count = reclassify_and_reorganize()
    print(f"Reclassified {count} files successfully.")
