import hashlib
import io
import json
import logging
import re
import sqlite3
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import docx
from PIL import Image
from src.config import DATABASE_PATH, HARVESTED_DIR

logger = logging.getLogger("QuestionExtractor")

EXTRACTED_DIR = Path(__file__).resolve().parent.parent / "data" / "extracted_questions"
IMAGES_DIR = EXTRACTED_DIR / "images"
JSON_EXPORT_PATH = EXTRACTED_DIR / "questions_bank.json"
JSONL_EXPORT_PATH = EXTRACTED_DIR / "questions_bank.jsonl"

STIMULUS_PATTERNS = [
    re.compile(r"(?:figure|fig\.?|diagram|illustration|table|chart)\s*([ivx\d]+)?\s*.*?(?:answer\s+questions?\s+(\d{1,2})(?:\s*(?:and|to|-|,)\s*(\d{1,2}))?)", re.I),
    re.compile(r"use\s+(?:the\s+)?(?:diagram|figure|illustration|table|chart|information|data)\s+(?:below\s+)?to\s+answer\s+questions?\s+(\d{1,2})(?:\s*(?:and|to|-|,)\s*(\d{1,2}))?", re.I),
    re.compile(r"study\s+(?:the\s+)?(?:diagram|figure|illustration|table)\s+(?:below\s+)?(?:carefully\s+)?(?:and\s+)?(?:to\s+)?answer\s+questions?\s+(\d{1,2})(?:\s*(?:and|to|-|,)\s*(\d{1,2}))?", re.I),
    re.compile(r"the\s+diagram\s+below\s+illustrates\s+.*?(?:answer\s+questions?\s+(\d{1,2})(?:\s*(?:and|to|-|,)\s*(\d{1,2}))?)", re.I),
]


class QuestionExtractor:
    """Extracts itemized Paper 1 (Objective) and Paper 2 (Theory) questions, marking schemes, and diagrams."""

    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS extracted_questions (
                    id TEXT PRIMARY KEY,
                    subject TEXT NOT NULL,
                    year INTEGER,
                    paper_type TEXT NOT NULL,
                    question_number INTEGER NOT NULL,
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
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_questions_type ON extracted_questions(paper_type);"
            )

    @staticmethod
    def get_paragraph_text(p) -> str:
        """Extracts text in document order across standard text (w:t) and equation (m:t) nodes."""
        nodes = p._p.xpath(".//w:t | .//m:t")
        return "".join(n.text for n in nodes if n.text).strip()

    @staticmethod
    def table_to_markdown(tbl) -> str:
        """Converts a Word table into a readable markdown table."""
        rows_data = []
        for row in tbl.rows:
            row_cells = [cell.text.strip().replace("\n", " ") for cell in row.cells]
            if any(row_cells):
                rows_data.append(row_cells)
        if not rows_data:
            return ""
        col_count = len(rows_data[0])
        lines = []
        lines.append("| " + " | ".join(rows_data[0]) + " |")
        lines.append("| " + " | ".join(["---"] * col_count) + " |")
        for r in rows_data[1:]:
            padded = r + [""] * (col_count - len(r))
            lines.append("| " + " | ".join(padded[:col_count]) + " |")
        return "\n".join(lines)

    def extract_image_from_element(self, elem, doc: docx.Document, file_stem: str, q_num: int) -> Optional[str]:
        """
        Extracts embedded diagram/figure image associated with an OpenXML element.
        Supports DrawingML (a:blip) and VML (imagedata). Filters micro-icons and converts WMF to PNG.
        """
        try:
            r_ids = elem.xpath(".//a:blip/@r:embed | .//*[local-name()='imagedata']/@*[local-name()='id']")
            for r_id in r_ids:
                if r_id not in doc.part.related_parts:
                    continue
                rel = doc.part.related_parts[r_id]
                if "image" not in rel.content_type:
                    continue

                raw_bytes = rel.blob
                if len(raw_bytes) < 400:
                    continue

                content_type = rel.content_type.lower()
                try:
                    im = Image.open(io.BytesIO(raw_bytes))
                    w, h = im.size
                    if w < 70 or h < 70 or (w * h) < 5000:
                        continue

                    img_name = f"{file_stem}_q{q_num}_{r_id}.png"
                    out_path = IMAGES_DIR / img_name
                    im.save(out_path, "PNG")
                    return str(out_path.relative_to(EXTRACTED_DIR.parent))
                except Exception:
                    if any(t in content_type for t in ["jpeg", "jpg", "png", "webp"]):
                        ext = "jpg" if "jpeg" in content_type else "png"
                        img_name = f"{file_stem}_q{q_num}_{r_id}.{ext}"
                        out_path = IMAGES_DIR / img_name
                        out_path.write_bytes(raw_bytes)
                        return str(out_path.relative_to(EXTRACTED_DIR.parent))
        except Exception as e:
            logger.debug(f"Image extraction error for {file_stem} q{q_num}: {e}")
        return None

    def extract_image_from_paragraph(self, p, doc: docx.Document, file_stem: str, q_num: int) -> Optional[str]:
        return self.extract_image_from_element(p._p, doc, file_stem, q_num)

    def parse_docx(self, file_path: Path, subject: str) -> List[Dict[str, Any]]:
        """Parses both Paper 1 (Objective) and Paper 2 (Theory) questions from a DOCX file."""
        questions: List[Dict[str, Any]] = []
        try:
            doc = docx.Document(file_path)
        except (zipfile.BadZipFile, Exception) as e:
            logger.debug(f"Failed to open DOCX {file_path}: {e}")
            return []

        file_stem = file_path.stem
        file_hash = hashlib.md5(file_stem.encode("utf-8")).hexdigest()[:8]

        year_match = re.search(r"\b(199\d|20[0-2]\d)\b", file_stem)
        year = int(year_match.group(1)) if year_match else None

        # Build answer key from paragraph text
        answer_key: Dict[int, str] = {}
        for p in doc.paragraphs:
            p_txt = self.get_paragraph_text(p)
            ak_matches = re.findall(r"\b(\d{1,2})\s*[\.\-\)]\s*([A-D])\b", p_txt)
            for num_str, opt in ak_matches:
                answer_key[int(num_str)] = opt

        current_paper_type = "Paper 1 - Objective"
        current_q_num: Optional[int] = None
        current_q_text: List[str] = []
        current_options = {"A": "", "B": "", "C": "", "D": ""}
        current_diagram: Optional[str] = None
        active_stimulus: Optional[Dict[str, Any]] = None
        auto_num_counter = 0

        def save_current_question() -> None:
            nonlocal current_q_num, current_q_text, current_options, current_diagram
            if current_q_num and (current_q_text or any(current_options.values())):
                tag = "P1" if "Paper 1" in current_paper_type else "P2"
                q_id = f"{subject}_{year or 'GEN'}_{file_hash}_{tag}_q{current_q_num}"
                questions.append({
                    "id": q_id,
                    "subject": subject,
                    "year": year,
                    "paper_type": current_paper_type,
                    "question_number": current_q_num,
                    "question_text": " ".join(current_q_text).strip(),
                    "option_a": current_options["A"],
                    "option_b": current_options["B"],
                    "option_c": current_options["C"],
                    "option_d": current_options["D"],
                    "correct_answer": answer_key.get(current_q_num, "") if "Paper 1" in current_paper_type else "",
                    "has_diagram": 1 if current_diagram else 0,
                    "diagram_path": current_diagram,
                    "source_file": file_path.name
                })
            current_q_num = None
            current_q_text = []
            current_options = {"A": "", "B": "", "C": "", "D": ""}
            current_diagram = None

        for child in doc.element.body:
            if child.tag.endswith("p"):
                p = docx.text.paragraph.Paragraph(child, doc)
                p_text = self.get_paragraph_text(p)
                if not p_text:
                    continue

                p_text_lower = p_text.lower()

                # Transition to Paper 2 / Theory / Essay / Section B
                if any(term in p_text_lower for term in ["section b", "paper two", "paper 2", "part ii", "part 2", "theory", "essay"]) and not any(p1 in p_text_lower for p1 in ["paper 1", "paper one"]):
                    save_current_question()
                    current_paper_type = "Paper 2 - Theory"
                    active_stimulus = None
                    auto_num_counter = 0
                    continue

                # Transition to Paper 1 / Objective Test / Section A
                if any(term in p_text_lower for term in ["paper one", "paper 1", "objective test", "part i", "part 1"]) and not any(p2 in p_text_lower for p2 in ["paper 2", "paper two"]):
                    save_current_question()
                    current_paper_type = "Paper 1 - Objective"
                    active_stimulus = None
                    auto_num_counter = 0
                    continue

                # Stimulus block detection (e.g. "Figure 1 shows... Use to answer Questions 3 and 4")
                is_stimulus = False
                for pat in STIMULUS_PATTERNS:
                    m = pat.search(p_text)
                    if m:
                        save_current_question()
                        g = m.groups()
                        digits = [int(d) for d in g if d and d.isdigit()]
                        q_start = digits[0] if digits else None
                        q_end = digits[1] if len(digits) > 1 else q_start
                        target_range = set(range(q_start, q_end + 1)) if q_start else set()

                        stim_diag = self.extract_image_from_element(child, doc, file_stem, q_start or 0)
                        active_stimulus = {
                            "text": p_text,
                            "diagram": stim_diag,
                            "target_questions": target_range
                        }
                        is_stimulus = True
                        break

                if is_stimulus:
                    continue

                # Check if paragraph starts a new question
                # Pattern A: Explicit number prefix (e.g., "1.", "Question 1", "1)")
                q_start_match = re.match(r"^(?:Question\s+)?(\d{1,2})\s*[\.\)]\s*(.*)", p_text, re.I)
                # Pattern B: Automatic Word list (<w:numPr> with ilvl=0)
                has_numpr = bool(child.xpath(".//*[local-name()='ilvl' and @*[local-name()='val']='0']"))
                is_option = bool(re.match(r"^[A-D]\s*[\.\)]", p_text))

                if q_start_match:
                    save_current_question()
                    current_q_num = int(q_start_match.group(1))
                    q_body = q_start_match.group(2).strip()
                    current_q_text = [q_body] if q_body else []

                    if active_stimulus and current_q_num in active_stimulus["target_questions"]:
                        current_diagram = active_stimulus["diagram"]
                        current_q_text.insert(0, f"[{active_stimulus['text']}]")

                    direct_img = self.extract_image_from_element(child, doc, file_stem, current_q_num)
                    if direct_img:
                        current_diagram = direct_img
                    continue
                elif has_numpr and not is_option:
                    save_current_question()
                    auto_num_counter += 1
                    current_q_num = auto_num_counter
                    current_q_text = [p_text]

                    if active_stimulus and current_q_num in active_stimulus["target_questions"]:
                        current_diagram = active_stimulus["diagram"]
                        current_q_text.insert(0, f"[{active_stimulus['text']}]")

                    direct_img = self.extract_image_from_element(child, doc, file_stem, current_q_num)
                    if direct_img:
                        current_diagram = direct_img
                    continue

                # Check intermediate image attachment
                if current_q_num:
                    intermediate_img = self.extract_image_from_element(child, doc, file_stem, current_q_num)
                    if intermediate_img and not current_diagram:
                        current_diagram = intermediate_img

                # Options for Paper 1
                if "Paper 1" in current_paper_type:
                    opt_matches = re.findall(r"([A-D])\s*[\.\)]\s*([^A-D\n]+)", p_text)
                    if opt_matches and current_q_num:
                        for opt_letter, opt_text in opt_matches:
                            current_options[opt_letter] = opt_text.strip()
                        continue

                    single_opt = re.match(r"^([A-D])\s*[\.\)]\s*(.*)", p_text)
                    if single_opt and current_q_num:
                        current_options[single_opt.group(1)] = single_opt.group(2).strip()
                        continue

                # Continuation of question text or Paper 2 sub-parts e.g. (a), (b), [4 marks]
                if current_q_num:
                    current_q_text.append(p_text)

            elif child.tag.endswith("tbl"):
                tbl = docx.table.Table(child, doc)
                tbl_md = self.table_to_markdown(tbl)
                if not tbl_md:
                    continue

                # Check if table represents rows of questions
                table_has_questions = False
                for r in tbl.rows:
                    row_cells = [c.text.strip() for c in r.cells]
                    if not row_cells:
                        continue
                    first_cell = row_cells[0]
                    tq_match = re.match(r"^(\d{1,2})\s*[\.\)]\s*(.*)", first_cell)
                    if tq_match:
                        table_has_questions = True
                        save_current_question()
                        t_q_num = int(tq_match.group(1))
                        t_text = tq_match.group(2) or (row_cells[1] if len(row_cells) > 1 else "")
                        t_opts = {"A": "", "B": "", "C": "", "D": ""}
                        if "Paper 1" in current_paper_type:
                            for cell_val in row_cells[1:]:
                                c_opts = re.findall(r"([A-D])\s*[\.\)]\s*([^A-D]+)", cell_val)
                                for o_let, o_txt in c_opts:
                                    t_opts[o_let] = o_txt.strip()

                        tag = "P1" if "Paper 1" in current_paper_type else "P2"
                        t_q_id = f"{subject}_{year or 'GEN'}_{file_hash}_{tag}_q{t_q_num}"
                        questions.append({
                            "id": t_q_id,
                            "subject": subject,
                            "year": year,
                            "paper_type": current_paper_type,
                            "question_number": t_q_num,
                            "question_text": t_text.strip(),
                            "option_a": t_opts["A"],
                            "option_b": t_opts["B"],
                            "option_c": t_opts["C"],
                            "option_d": t_opts["D"],
                            "correct_answer": answer_key.get(t_q_num, "") if "Paper 1" in current_paper_type else "",
                            "has_diagram": 0,
                            "diagram_path": None,
                            "source_file": file_path.name
                        })

                if not table_has_questions:
                    if current_q_num:
                        current_q_text.append(f"\n{tbl_md}\n")
                    elif active_stimulus:
                        active_stimulus["text"] += f"\n{tbl_md}\n"

        save_current_question()
        return questions

    def parse_txt(self, file_path: Path, subject: str) -> List[Dict[str, Any]]:
        """Parses both Paper 1 (Objective) and Paper 2 (Theory) questions from a clean text exam paper."""
        questions: List[Dict[str, Any]] = []
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []

        file_stem = file_path.stem
        file_hash = hashlib.md5(file_stem.encode("utf-8")).hexdigest()[:8]
        year_match = re.search(r"\b(199\d|20[0-2]\d)\b", file_stem)
        year = int(year_match.group(1)) if year_match else None

        lines = [line.strip() for line in content.split("\n") if line.strip()]

        current_paper_type = "Paper 1 - Objective"
        current_q_num = None
        current_q_text: List[str] = []
        current_options = {"A": "", "B": "", "C": "", "D": ""}

        def save_current_txt_question() -> None:
            nonlocal current_q_num, current_q_text, current_options
            if current_q_num and (current_q_text or any(current_options.values())):
                tag = "P1" if "Paper 1" in current_paper_type else "P2"
                q_id = f"{subject}_{year or 'TXT'}_{file_hash}_{tag}_q{current_q_num}"
                questions.append({
                    "id": q_id,
                    "subject": subject,
                    "year": year,
                    "paper_type": current_paper_type,
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
            current_q_num = None
            current_q_text = []
            current_options = {"A": "", "B": "", "C": "", "D": ""}

        for line in lines:
            line_lower = line.lower()

            # Transition to Paper 2 / Theory / Essay / Section B
            if any(term in line_lower for term in ["section b", "paper two", "paper 2", "part ii", "part 2", "theory", "essay"]) and not any(p1 in line_lower for p1 in ["paper 1", "paper one"]):
                save_current_txt_question()
                current_paper_type = "Paper 2 - Theory"
                continue

            # Transition to Paper 1 / Objective Test / Section A
            if any(term in line_lower for term in ["paper one", "paper 1", "objective test", "part i", "part 1"]) and not any(p2 in line_lower for p2 in ["paper 2", "paper two"]):
                save_current_txt_question()
                current_paper_type = "Paper 1 - Objective"
                continue

            q_match = re.match(r"^(?:Question\s+)?(\d{1,2})\s*[\.\)]\s*(.*)", line, re.I)
            if q_match:
                save_current_txt_question()
                current_q_num = int(q_match.group(1))
                q_body = q_match.group(2).strip()
                current_q_text = [q_body] if q_body else []
                continue

            if "Paper 1" in current_paper_type:
                opt_matches = re.findall(r"([A-D])\s*[\.\)]\s*([^A-D\n]+)", line)
                if opt_matches and current_q_num:
                    for opt_letter, opt_text in opt_matches:
                        current_options[opt_letter] = opt_text.strip()
                    continue

                single_opt = re.match(r"^([A-D])\s*[\.\)]\s*(.*)", line)
                if single_opt and current_q_num:
                    current_options[single_opt.group(1)] = single_opt.group(2).strip()
                    continue

            if current_q_num:
                current_q_text.append(line)

        save_current_txt_question()
        return questions

    def run_batch_extraction(self) -> int:
        """Runs the complete extraction across all retained exam papers with a clean slate."""
        total_extracted = 0

        # Reset database table for clean, deduplicated indexing
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("DELETE FROM extracted_questions;")

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
            rows = conn.execute("SELECT * FROM extracted_questions ORDER BY subject, year, paper_type, question_number;").fetchall()
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
