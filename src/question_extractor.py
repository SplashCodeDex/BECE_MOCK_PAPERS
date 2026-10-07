import hashlib
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

    def extract_image_from_paragraph(self, p, doc: docx.Document, file_stem: str, q_num: int) -> Optional[str]:
        """Extracts embedded diagram/figure image directly associated with a specific paragraph."""
        try:
            r_ids = p._p.xpath('.//a:blip/@r:embed')
            if r_ids:
                r_id = r_ids[0]
                if r_id in doc.part.related_parts:
                    rel = doc.part.related_parts[r_id]
                    if "image" in rel.content_type:
                        ext = rel.content_type.split("/")[-1].replace("jpeg", "jpg")
                        img_name = f"{file_stem}_q{q_num}_{r_id}.{ext}"
                        out_path = IMAGES_DIR / img_name
                        out_path.write_bytes(rel.blob)
                        return str(out_path.relative_to(EXTRACTED_DIR.parent))
        except Exception as e:
            logger.debug(f"Image extraction error for {file_stem} q{q_num}: {e}")
        return None

    def parse_docx(self, file_path: Path, subject: str) -> List[Dict[str, Any]]:
        """Parses objective and theory questions from a DOCX file."""
        questions = []
        try:
            doc = docx.Document(file_path)
        except (zipfile.BadZipFile, Exception) as e:
            return []

        file_stem = file_path.stem
        file_hash = hashlib.md5(file_stem.encode("utf-8")).hexdigest()[:8]

        # Detect year from filename or text
        year_match = re.search(r"\b(199\d|20[0-2]\d)\b", file_stem)
        year = int(year_match.group(1)) if year_match else None

        paras = [p for p in doc.paragraphs if p.text.strip() or p._p.xpath('.//a:blip/@r:embed')]
        if not paras:
            return []

        # Find answer key section if present at the end of paper
        answer_key = {}
        for p in paras:
            ak_matches = re.findall(r"\b(\d{1,2})\s*[\.\-\)]\s*([A-D])\b", p.text)
            for num_str, opt in ak_matches:
                answer_key[int(num_str)] = opt

        # Parse Objective Questions (Questions 1 to 40)
        current_q_num = None
        current_q_text = []
        current_options = {"A": "", "B": "", "C": "", "D": ""}
        current_diagram_path = None
        in_objective_section = True

        for p in paras:
            p_text = p.text.strip()
            # Check for Section B / Theory transition
            if any(term in p_text.lower() for term in ["section b", "paper two", "paper 2", "part ii", "theory"]):
                in_objective_section = False

            # Check if paragraph starts a new question: e.g. "1.", "2.", "15."
            q_start_match = re.match(r"^(\d{1,2})\s*[\.\)]\s*(.*)", p_text)
            if q_start_match and in_objective_section:
                # Save previous question if valid
                if current_q_num and (current_q_text or any(current_options.values())):
                    q_id = f"{subject}_{year or 'GEN'}_{file_hash}_q{current_q_num}"
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
                        "has_diagram": 1 if current_diagram_path else 0,
                        "diagram_path": current_diagram_path,
                        "source_file": file_path.name
                    })

                current_q_num = int(q_start_match.group(1))
                current_q_text = [q_start_match.group(2).strip()]
                current_options = {"A": "", "B": "", "C": "", "D": ""}
                current_diagram_path = self.extract_image_from_paragraph(p, doc, file_stem, current_q_num)
                continue

            # Check if this paragraph contains an image for the current question
            if current_q_num and not current_diagram_path:
                img_found = self.extract_image_from_paragraph(p, doc, file_stem, current_q_num)
                if img_found:
                    current_diagram_path = img_found

            # Check for options: "A. ...", "B. ...", "C. ...", "D. ..."
            opt_matches = re.findall(r"([A-D])\s*[\.\)]\s*([^A-D\n]+)", p_text)
            if opt_matches and current_q_num:
                for opt_letter, opt_text in opt_matches:
                    current_options[opt_letter] = opt_text.strip()
                continue

            # Single option lines like "A.   {1, 2, 3}"
            single_opt = re.match(r"^([A-D])\s*[\.\)]\s*(.*)", p_text)
            if single_opt and current_q_num:
                current_options[single_opt.group(1)] = single_opt.group(2).strip()
                continue

            # Continuation of question text
            if current_q_num and in_objective_section and not any(current_options.values()) and p_text:
                current_q_text.append(p_text)

        # Append last question
        if current_q_num and (current_q_text or any(current_options.values())):
            q_id = f"{subject}_{year or 'GEN'}_{file_hash}_q{current_q_num}"
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
                "has_diagram": 1 if current_diagram_path else 0,
                "diagram_path": current_diagram_path,
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
        file_hash = hashlib.md5(file_stem.encode("utf-8")).hexdigest()[:8]
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
                    q_id = f"{subject}_{year or 'TXT'}_{file_hash}_q{current_q_num}"
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

        # Append last question
        if current_q_num and (current_q_text or any(current_options.values())):
            q_id = f"{subject}_{year or 'TXT'}_{file_hash}_q{current_q_num}"
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
                    if items:
                        self.save_questions_batch(items)
                        total_extracted += len(items)

            # 2. Parse TXT papers
            txt_dir = subject_dir / "txt"
            if txt_dir.exists():
                for f in txt_dir.glob("*.txt"):
                    items = self.parse_txt(f, subject)
                    if items:
                        self.save_questions_batch(items)
                        total_extracted += len(items)

        self.export_catalog()
        return total_extracted

    def save_questions_batch(self, questions: List[Dict[str, Any]]) -> None:
        """Saves or updates a batch of questions in SQLite database in a single transaction."""
        if not questions:
            return
        rows = [
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
                q["source_file"],
            )
            for q in questions
        ]
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.executemany(
                """
                INSERT OR REPLACE INTO extracted_questions (
                    id, subject, year, paper_type, question_number, question_text,
                    option_a, option_b, option_c, option_d, correct_answer,
                    has_diagram, diagram_path, source_file
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                rows,
            )

    def save_question(self, q: Dict[str, Any]) -> None:
        """Saves or updates a single question in SQLite database."""
        self.save_questions_batch([q])

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
