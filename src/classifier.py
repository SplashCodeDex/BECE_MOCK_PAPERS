import re
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import unquote, urlparse
from src.config import HARVESTED_DIR, SUBJECTS


class FileClassifier:
    """Classifies files by examination subject, organizes target directory paths, and cleans filenames."""

    @staticmethod
    def is_exam_paper_or_scheme(text_context: str) -> bool:
        """Verifies that document is an exam paper (Paper 1/2) or marking scheme, and not notes/textbooks/reports."""
        text = text_context.lower()
        unwanted = [
            "examiner report", "examiners report", "chief examiner", "examiner remarks",
            "scheme of work", "scheme of learning", "schemes of work", "schemes of learning",
            "lesson plan", "lesson notes", "lesson note", "scheme of learning",
            "curriculum guide", "teaching syllabus", "textbook", "teachers guide",
            "termly scheme"
        ]
        return not any(u in text for u in unwanted)

    EXAM_SIGNALS = (
        "bece", "mock", "past questions", "pasco", "marking scheme",
        "paper 1", "paper 2", "objective", "theory", "waec", "ges",
        "chief examiner", "trial questions", "sample questions", "exam",
        "questions and answers", "question paper",
    )

    @classmethod
    def looks_like_exam_content(cls, text: str) -> bool:
        t = (text or "").lower()
        return any(s in t for s in cls.EXAM_SIGNALS)

    @classmethod
    def reject_reason(
        cls,
        content: bytes,
        extension: str,
        text_context: str = "",
        subject: Optional[str] = None,
    ) -> Optional[str]:
        """Return a reject reason if this download must NOT be kept, else None.

        Used to permanently tombstone junk (notes, textbooks, wrong papers) so a
        future crawl never refetches the same bytes after the file is deleted.
        """
        sample = text_context
        ext = (extension or "").lower()
        if content and ext == ".pdf":
            try:
                import pymupdf

                doc = pymupdf.open(stream=content, filetype="pdf")
                for p in range(min(len(doc), 3)):
                    sample += " " + doc[p].get_text()
            except Exception:
                pass
        elif content and ext in (".txt", ""):
            try:
                sample += " " + content[:4000].decode("utf-8", errors="ignore")
            except Exception:
                pass
        elif content and ext == ".docx":
            try:
                import io

                from docx import Document

                doc = Document(io.BytesIO(content))
                sample += " " + " ".join(p.text for p in doc.paragraphs[:20])
            except Exception:
                pass

        if not cls.is_exam_paper_or_scheme(sample):
            return "not_exam_paper"

        if not cls.looks_like_exam_content(sample):
            return "no_exam_signals"

        if subject == "General_Unclassified" and not cls.looks_like_exam_content(text_context):
            return "unclassified_wrong_subject"

        return None

    @classmethod
    def detect_subject(cls, text_context: str) -> str:
        """Determines subject based on text context (URL path, title, anchor text, headers)."""
        if not cls.is_exam_paper_or_scheme(text_context):
            return "General_Unclassified"

        text = text_context.lower()

        # Score matching
        scores = {"Mathematics": 0, "Computing_ICT": 0, "CDT_CAD": 0}
        other_scores = 0

        # Check for non-target subjects
        non_target_keywords = [
            "english", "french", "français", "social studies", "integrated science",
            "religious and moral education", "rme", "akuapem twi", "asante twi",
            "fante", "ga language", "ewe language"
        ]
        for keyword in non_target_keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", text):
                other_scores += 3

        for keyword in SUBJECTS["Mathematics"]:
            if re.search(rf"\b{re.escape(keyword)}\b", text):
                scores["Mathematics"] += 2
            elif keyword in text:
                scores["Mathematics"] += 1

        for keyword in SUBJECTS["Computing_ICT"]:
            if re.search(rf"\b{re.escape(keyword)}\b", text):
                scores["Computing_ICT"] += 2
            elif keyword in text:
                scores["Computing_ICT"] += 1

        for keyword in SUBJECTS["CDT_CAD"]:
            if re.search(rf"\b{re.escape(keyword)}\b", text):
                scores["CDT_CAD"] += 2
            elif keyword in text:
                scores["CDT_CAD"] += 1

        # Determine winner
        best_subject = max(scores, key=lambda k: scores[k])
        if scores[best_subject] > other_scores and scores[best_subject] >= 2:
            return best_subject

        return "General_Unclassified"

    @classmethod
    def detect_subject_from_bytes(
        cls,
        content: bytes,
        extension: str,
        text_context: str = ""
    ) -> str:
        """Inspects internal document text using PyMuPDF / python-docx to classify subject accurately."""
        extracted_sample = ""
        ext = extension.lower()

        if ext == ".pdf":
            try:
                import pymupdf
                doc = pymupdf.open(stream=content, filetype="pdf")
                pages_to_check = min(len(doc), 3)
                for p in range(pages_to_check):
                    extracted_sample += " " + doc[p].get_text()
            except Exception:
                pass
        elif ext in [".docx"]:
            try:
                import io
                from docx import Document
                doc = Document(io.BytesIO(content))
                for para in doc.paragraphs[:20]:
                    extracted_sample += " " + para.text
            except Exception:
                pass
        elif ext == ".txt":
            try:
                extracted_sample = content[:4000].decode("utf-8", errors="ignore")
            except Exception:
                pass

        if extracted_sample:
            detected = cls.detect_subject(extracted_sample)
            if detected != "General_Unclassified":
                return detected

        # Fallback to URL/filename text context if bytes yielded no text layer
        return cls.detect_subject(text_context)

    @staticmethod
    def extract_metadata_hints(text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extracts year and provider tags (e.g., BestBrain, GBAT, WAEC)."""
        text_lower = text.lower()
        
        # Detect Year (1990 - 2029)
        year_match = re.search(r"\b(199\d|20[0-2]\d)\b", text_lower)
        year = year_match.group(1) if year_match else None

        # Detect Provider
        provider = None
        if "bestbrain" in text_lower or "best brain" in text_lower:
            provider = "BestBrain"
        elif "gbat" in text_lower:
            provider = "GBAT"
        elif "pbpagez" in text_lower or "pb pagez" in text_lower:
            provider = "PBPagez"
        elif "passco" in text_lower:
            provider = "Passco"
        elif "ghlearner" in text_lower:
            provider = "GhLearner"
        elif "waec" in text_lower:
            provider = "WAEC"

        return year, provider

    @classmethod
    def sanitize_filename(
        cls,
        raw_name: str,
        subject: str,
        sha256: str,
        extension: str,
        context_text: str = ""
    ) -> str:
        """Constructs a clean, professional, readable filename."""
        raw_name = unquote(raw_name)
        # Strip query parameters or url fragments
        raw_name = raw_name.split("?")[0].split("#")[0]
        base_name = Path(raw_name).stem

        # Remove illegal Windows filename characters and noisy punctuation
        clean_base = re.sub(r'[^\w\-.]', "_", base_name)
        clean_base = re.sub(r"[\s_]+", "_", clean_base).strip("_")

        # Extract year and provider hints
        year, provider = cls.extract_metadata_hints(f"{context_text} {clean_base}")

        components = [subject]
        if year and year not in clean_base:
            components.append(year)
        if provider and provider.lower() not in clean_base.lower():
            components.append(provider)

        # Include sanitized original stem (truncated to 40 chars)
        if clean_base:
            components.append(clean_base[:40])

        # Suffix with short hash for collision guarantee
        short_hash = sha256[:8]
        components.append(short_hash)

        ext = extension.lower().strip()
        if not ext.startswith("."):
            ext = f".{ext}"

        return f"{'_'.join(components)}{ext}"

    @classmethod
    def get_destination_path(
        cls,
        subject: str,
        extension: str,
        clean_filename: str
    ) -> Path:
        """Returns the organized destination path: data/harvested/{Subject}/{ext}/{filename}."""
        ext_folder = extension.lower().replace(".", "").strip()
        target_dir = HARVESTED_DIR / subject / ext_folder
        target_dir.mkdir(parents=True, exist_ok=True)
        return target_dir / clean_filename
