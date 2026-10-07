import io
import json
import logging
import re
import sqlite3
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional
import docx
from src.config import DATABASE_PATH, HARVESTED_DIR

logger = logging.getLogger("QuestionExtractor")

EXTRACTED_DIR = Path(__file__).resolve().parent.parent / "data" / "extracted_questions"
IMAGES_DIR = EXTRACTED_DIR / "images"
JSON_EXPORT_PATH = EXTRACTED_DIR / "questions_bank.json"
JSONL_EXPORT_PATH = EXTRACTED_DIR / "questions_bank.jsonl"


class QuestionExtractor:
    """Extracts itemized questions, options, marking schemes, and diagrams from harvested papers."""

    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self._ensure_dirs()
        self.init_db()

    def _ensure_dirs(self) -> None:
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    def init_db(self) -> None:
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS extracted_questions (
                    id TEXT PRIMARY KEY,
                    subject TEXT NOT NULL,
                    year INTEGER,
                    paper_type TEXT NOT NULL,
                    question_number INTEGER,
                    question_text TEXT NOT NULL,
                    option_a TEXT,
                    option_b TEXT,
                    option_c TEXT,
                    option_d TEXT,
                    correct_answer TEXT,
                    has_diagram INTEGER DEFAULT 0,
                    diagram_path TEXT,
                    source_file TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_questions_subject ON extracted_questions(subject);"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_questions_year ON extracted_questions(year);"
            )

    def extract_images_from_docx(self, doc: docx.Document, file_stem: str) -> List[str]:
        """Extracts all embedded diagram/figure images from a DOCX file to disk."""
        image_paths = []
        try:
            for idx, rel in enumerate(doc.part.related_parts.values()):
                if "image" in rel.content_type:
                    ext = rel.content_type.split("/")[-1]
                    if ext == "jpeg":
                        ext = "jpg"
                    img_name = f"{file_stem}_fig_{idx}.{ext}"
                    out_path = IMAGES_DIR / img_name
                    out_path.write_bytes(rel.blob)
                    image_paths.append(str(out_path.relative_to(EXTRACTED_DIR.parent)))
        except Exception as e:
            logger.debug(f"Image extraction error for {file_stem}: {e}")
        return image_paths

    def parse_docx(self, file_path: Path, subject: str) -> List[Dict[str, Any]]:
        """Parses objective and theory questions from a DOCX file."""
        questions = []
        try:
            doc = docx.Document(file_path)
        except (zipfile.BadZipFile, Exception) as e:
            return []

        file_stem = file_path.stem
        # Extract embedded diagrams
        diagram_paths = self.extract_images_from_docx(doc, file_stem)

        # Detect year from filename or text
        year_match = re.search(r"\b(199\d|20[0-2]\d)\b", file_stem)
        year = int(year_match.group(1)) if year_match else None

        paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        if not paras:
            return []

        # Find answer key section if present at the end of paper
        answer_key = {}
        for p in paras:
            # Pattern like "1. A  2. B  3. C" or "1. A"
            ak_matches = re.findall(r"\b(\d{1,2})\s*[\.\-\)]\s*([A-D])\b", p)
            for num_str, opt in ak_matches:
                answer_key[int(num_str)] = opt

        # Parse Objective Questions (Questions 1 to 40)
        current_q_num = None
        current_q_text = []
        current_options = {"A": "", "B": "", "C": "", "D": ""}
        in_objective_section = True

        for p in paras:
            # Check for Section B / Theory transition
            if any(term in p.lower() for term in ["section b", "paper two", "paper 2", "part ii", "theory"]):
                in_objective_section = False

            # Check if paragraph starts a new question: e.g. "1.", "2.", "15."
            q_start_match = re.match(r"^(\d{1,2})\s*[\.\)]\s*(.*)", p)
            if q_start_match and in_objective_section:
                # Save previous question if valid
                if current_q_num and (current_q_text or any(current_options.values())):
                    q_id = f"{subject}_{year or 'GEN'}_{current_q_num}_{file_stem[:10]}"
                    questions.append({
                        "id": q_id,
                        "subject": subject,
                        "year": year,
                        "paper_type": "Objective",
                        "question_number": current_q_num,
                        "question_text": " ".join(current_q_text).strip(),
                        "option_a": current_options["A"],
                        "option_b": current_options["B"],
                        "option_c": current_options["C"],
                        "option_d": current_options["D"],
                        "correct_answer": answer_key.get(current_q_num, ""),
                        "has_diagram": 1 if diagram_paths else 0,
                        "diagram_path": diagram_paths[0] if diagram_paths else None,
                        "source_file": file_path.name
                    })

                current_q_num = int(q_start_match.group(1))
                current_q_text = [q_start_match.group(2).strip()]
                current_options = {"A": "", "B": "", "C": "", "D": ""}
                continue

            # Check for options: "A. ...", "B. ...", "C. ...", "D. ..."
            opt_matches = re.findall(r"([A-D])\s*[\.\)]\s*([^A-D\n]+)", p)
            if opt_matches and current_q_num:
                for opt_letter, opt_text in opt_matches:
                    current_options[opt_letter] = opt_text.strip()
                continue

            # Single option lines like "A.   {1, 2, 3}"
            single_opt = re.match(r"^([A-D])\s*[\.\)]\s*(.*)", p)
            if single_opt and current_q_num:
                current_options[single_opt.group(1)] = single_opt.group(2).strip()
                continue

            # Continuation of question text
            if current_q_num and in_objective_section and not any(current_options.values()):
                current_q_text.append(p)

        # Append last question
        if current_q_num and (current_q_text or any(current_options.values())):
            q_id = f"{subject}_{year or 'GEN'}_{current_q_num}_{file_stem[:10]}"
            questions.append({
                "id": q_id,
                "subject": subject,
                "year": year,
                "paper_type": "Objective",
                "question_number": current_q_num,
                "question_text": " ".join(current_q_text).strip(),
                "option_a": current_options["A"],
                "option_b": current_options["B"],
                "option_c": current_options["C"],
                "option_d": current_options["D"],
                "correct_answer": answer_key.get(current_q_num, ""),
                "has_diagram": 1 if diagram_paths else 0,
                "diagram_path": diagram_paths[0] if diagram_paths else None,
                "source_file": file_path.name
            })

        return questions

    def parse_txt(self, file_path: Path, subject: str) -> List[Dict[str, Any]]:
        """Parses questions from a clean text exam paper."""
        questions = []
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []

        file_stem = file_path.stem
        year_match = re.search(r"\b(199\d|20[0-2]\d)\b", file_stem)
        year = int(year_match.group(1)) if year_match else None

        lines = [line.strip() for line in content.split("\n") if line.strip()]

        current_q_num = None
        current_q_text = []
        current_options = {"A": "", "B": "", "C": "", "D": ""}

        for line in lines:
            q_match = re.match(r"^(\d{1,2})\s*[\.\)]\s*(.*)", line)
            if q_match:
                if current_q_num and (current_q_text or any(current_options.values())):
                    q_id = f"{subject}_{year or 'TXT'}_{current_q_num}_{file_stem[:8]}"
                    questions.append({
                        "id": q_id,
                        "subject": subject,
                        "year": year,
                        "paper_type": "Objective",
                        "question_number": current_q_num,
                        "question_text": " ".join(current_q_text).strip(),
                        "option_a": current_options["A"],
                        "option_b": current_options["B"],
                        "option_c": current_options["C"],
                        "option_d": current_options["D"],
                        "correct_answer": "",
                        "has_diagram": 0,
                        "diagram_path": None,
                        "source_file": file_path.name
                    })

                current_q_num = int(q_match.group(1))
                current_q_text = [q_match.group(2).strip()]
                current_options = {"A": "", "B": "", "C": "", "D": ""}
                continue

            opt_matches = re.findall(r"([A-D])\s*[\.\)]\s*([^A-D\n]+)", line)
            if opt_matches and current_q_num:
                for opt_letter, opt_text in opt_matches:
                    current_options[opt_letter] = opt_text.strip()
                continue

            single_opt = re.match(r"^([A-D])\s*[\.\)]\s*(.*)", line)
            if single_opt and current_q_num:
                current_options[single_opt.group(1)] = single_opt.group(2).strip()
                continue

            if current_q_num and not any(current_options.values()):
                current_q_text.append(line)

        return questions

    def run_batch_extraction(self) -> int:
        """Runs the extraction across all harvested DOCX and TXT files."""
        total_extracted = 0

        # Process Mathematics, Computing_ICT, and CDT_CAD
        for subject_dir in HARVESTED_DIR.iterdir():
            if not subject_dir.is_dir() or subject_dir.name == "General_Unclassified":
                continue

            subject = subject_dir.name

            # 1. Parse DOCX papers
            docx_dir = subject_dir / "docx"
            if docx_dir.exists():
                for f in docx_dir.glob("*.docx"):
                    items = self.parse_docx(f, subject)
                    for item in items:
                        self.save_question(item)
                        total_extracted += 1

            # 2. Parse TXT papers
            txt_dir = subject_dir / "txt"
            if txt_dir.exists():
                for f in txt_dir.glob("*.txt"):
                    items = self.parse_txt(f, subject)
                    for item in items:
                        self.save_question(item)
                        total_extracted += 1

        self.export_catalog()
        return total_extracted

    def save_question(self, q: Dict[str, Any]) -> None:
        """Saves or updates question in SQLite database."""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO extracted_questions (
                    id, subject, year, paper_type, question_number, question_text,
                    option_a, option_b, option_c, option_d, correct_answer,
                    has_diagram, diagram_path, source_file
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    q["id"],
                    q["subject"],
                    q.get("year"),
                    q["paper_type"],
                    q["question_number"],
                    q["question_text"],
                    q["option_a"],
                    q["option_b"],
                    q["option_c"],
                    q["option_d"],
                    q.get("correct_answer", ""),
                    q["has_diagram"],
                    q.get("diagram_path"),
                    q["source_file"]
                ),
            )

    def export_catalog(self) -> None:
        """Exports extracted questions to JSON and JSONL."""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM extracted_questions ORDER BY subject, year, question_number;").fetchall()
            data = [dict(r) for r in rows]

        with open(JSON_EXPORT_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        with open(JSONL_EXPORT_PATH, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    extractor = QuestionExtractor()
    count = extractor.run_batch_extraction()
    print(f"Extraction complete! Extracted {count} question records.")
