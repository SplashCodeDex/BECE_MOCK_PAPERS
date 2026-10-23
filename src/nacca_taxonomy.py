"""Deterministic taxonomy extractor for official NaCCA CCP curriculum PDFs.

The NaCCA B7-B9 curriculum PDFs (Mathematics, Computing) carry a text layer
with printed indicator codes (e.g. 'B9.1.1.1.1'). This module parses them into
the curriculum_indicators JSON shape without any vision-model involvement.

Code anatomy:  B<grade>.<strand>.<substrand>.<content_standard>[.<indicator>]
- 'B9.1.1.1'      -> content standard
- 'B9.1.1.1.1'    -> indicator (child of the preceding content standard)
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import pymupdf

CODE_RE = re.compile(r"B([789])\.(\d+)\.(\d+)\.(\d+)(?:\.(\d+))?")
# Some NaCCA pages render digit '1' as a capital-I glyph ('B9I.I.I.I.I')
# or drop the dot after the grade ('B91.1.1.1.1').
CODE_LOOSE_RE = re.compile(r"B([789])((?:\.[0-9ILl|]){2,}|[0-9ILl|](?:\.[0-9ILl|]+){2,})")
STRAND_RE = re.compile(r"^STRAND\s+(\d+)\s*:\s*(.+?)\s*$", re.I)
SUBSTRAND_RE = re.compile(r"^Sub-?\s*strand\s+(\d+)\s*:\s*(.+?)\s*$", re.I)
# Truncate indicator text at exemplars; they bloat the tagger's context.
EXEMPLAR_RE = re.compile(r"\bE\.?\s?g\.?\s*\d*", re.I)

# Known NaCCA PDF errata: printed code is wrong, correct code per hierarchy
# (verified against Grade9-Maths/LESSON_TRACKER.md).
ERRATA = {
    # Printed as B9.1.2.3.4 but sits under content standard B9.1.2.4
    # ("Approximate square roots of non-perfect squares with calculators").
    "B9.1.2.3.4": "B9.1.2.4.4",
}

# Indicators MISSING from the NaCCA text-layer PDF but required by the
# tracker / present in the scanned Grade9 curriculum. Tracker wins (Q3).
SUPPLEMENT = [
    {
        "code": "B9.1.2.1.2",
        "grade": "B9",
        "subject": "Mathematics",
        "strand_number": 1,
        "strand_title": "NUMBER",
        "substrand_number": 2,
        "substrand_title": "Number Operations",
        "content_standard": "B9.1.2.1",
        "content_standard_text": (
            "Apply the four basic operations on rational numbers and the "
            "order of operations to solve problems."
        ),
        "indicator_text": (
            "Demonstrate the ability to determine commutative properties "
            "of addition and multiplication"
        ),
        "source_file": "Grade9-Mathematics.pdf (scan; absent from NaCCA text PDF)",
        "page": None,
    },
]

# Core-competency column labels that bleed across the text layer.
COMPETENCY_RE = re.compile(
    r"\b(Communication\s+and\s+Collaboration\s*\(CC\)"
    r"|Creativity\s+and\s+Innovation\s*\(CI\)"
    r"|Personal\s+Development\s+and\s+Leadership\s*\(PL\)"
    r"|Critical\s+Thinking\s+and\s+Problem\s*solving\s*\(CP\)"
    r"|Cultural\s+Identity\s+and\s+Global\s*Citizenship\s*\(CG\)"
    r"|Integrity\s+and\s+Moral\s*Values\s*\(IM\)"
    r"|Self-?efficacy\s*\(SE\)"
    r"|Digital\s+Literacy\s*\(DL\)"
    r"|Diversity\s+and\s+Global\s*Citizenship\s*\(DG\))(?!\w)",
    re.I,
)


def _clean_text(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", " ", text)
    return text.strip()


def _normalize_glyph_codes(text: str) -> str:
    """Rewrite I-glyph indicator codes ('B9I.I.I.I.I') as canonical dotted form.

    Only touches tokens whose segments are all digits or I/l/| glyph variants
    of digits, so prose is never altered.
    """
    def repl(m: re.Match) -> str:
        # Skip a leading empty segment when the token starts with a dot.
        segs = [s for s in m.group(2).split(".") if s != ""]
        out = []
        for s in segs:
            s2 = s.replace("I", "1").replace("l", "1").replace("|", "1")
            if not s2.isdigit():
                return m.group(0)  # not a pure code token; leave untouched
            out.append(s2)
        if not out:
            return m.group(0)
        return f"B{m.group(1)}." + ".".join(out)

    return CODE_LOOSE_RE.sub(repl, text)


def extract_pdf(pdf_path: Path, subject: str) -> List[Dict]:
    doc = pymupdf.open(str(pdf_path))
    indicators: List[Dict] = []
    # code -> accumulated info; content_standard_text lives on the parent
    std_text: Dict[str, str] = {}
    strand_titles: Dict[int, str] = {}
    substrand_titles: Dict[tuple, str] = {}

    # Pass 1: collect strand/substrand titles (skip TOC pages with dot leaders).
    for page in doc:
        text = page.get_text()
        if "....." in text:  # table-of-contents page
            continue
        current_strand = None
        for line in text.split("\n"):
            stripped = line.strip()
            m = STRAND_RE.match(stripped)
            if m and "..." not in stripped:
                current_strand = int(m.group(1))
                strand_titles.setdefault(current_strand, m.group(2).strip().rstrip("."))
            m = SUBSTRAND_RE.match(stripped)
            if m and "..." not in stripped and current_strand is not None:
                substrand_titles.setdefault(
                    (current_strand, int(m.group(1))), m.group(2).strip().rstrip(".")
                )

    # Pass 2: anchor on indicator codes; text between anchors belongs to the
    # earlier anchor (multi-column layout handled by sorting anchors by position).
    for page_no, page in enumerate(doc, start=1):
        text = page.get_text()
        if "....." in text:
            continue
        text = _normalize_glyph_codes(text)
        anchors = [
            (m.start(), m.end(), m) for m in CODE_RE.finditer(text)
        ]
        for idx, (start, end, m) in enumerate(anchors):
            nxt = anchors[idx + 1][0] if idx + 1 < len(anchors) else len(text)
            body = text[end:nxt]
            grade, strand, substrand, std, ind = (
                int(m.group(1)), int(m.group(2)), int(m.group(3)),
                int(m.group(4)), m.group(5),
            )
            code_prefix = f"B{grade}.{strand}.{substrand}.{std}"
            if ind is None:
                # Content standard: capture its statement (before any child code).
                stmt = EXEMPLAR_RE.split(body)[0]
                std_text[code_prefix] = _clean_text(COMPETENCY_RE.sub("", stmt))[:600]
            else:
                code = f"{code_prefix}.{ind}"
                code = ERRATA.get(code, code)
                stmt = EXEMPLAR_RE.split(body)[0]
                stmt = COMPETENCY_RE.sub("", stmt)
                stmt = _clean_text(stmt)
                # Strip a trailing period-noise and exemplar fragments
                indicators.append({
                    "code": code,
                    "grade": f"B{grade}",
                    "subject": subject,
                    "strand_number": strand,
                    "strand_title": strand_titles.get(strand, ""),
                    "substrand_number": substrand,
                    "substrand_title": substrand_titles.get((strand, substrand), ""),
                    "content_standard": code_prefix,
                    "content_standard_text": std_text.get(code_prefix, ""),
                    "indicator_text": stmt[:800] or code,
                    "source_file": pdf_path.name,
                    "page": page_no,
                })

    # Dedup: keep first occurrence of each code (lowest page).
    seen: Dict[str, Dict] = {}
    for ind in indicators:
        seen.setdefault(ind["code"], ind)
    return sorted(seen.values(), key=lambda x: (
        x["subject"], x["strand_number"], x["substrand_number"],
        x["content_standard"], x["code"],
    ))


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    base = Path(__file__).resolve().parent.parent / "data" / "curriculum"
    jobs = [
        (base / "NACCA_MATHEMATICS_B7-B9.pdf", "Mathematics"),
        (base / "NACCA_COMPUTING_B7-B9.pdf", "Computing_ICT"),
    ]
    all_indicators: List[Dict] = []
    notes = []
    for pdf, subject in jobs:
        if not pdf.exists():
            notes.append(f"MISSING: {pdf}")
            continue
        inds = extract_pdf(pdf, subject)
        all_indicators.extend(inds)
        by_grade: Dict[str, int] = {}
        for i in inds:
            by_grade[i["grade"]] = by_grade.get(i["grade"], 0) + 1
        print(f"{pdf.name} [{subject}]: {len(inds)} indicators {by_grade}")

    # Merge supplements (tracker-required codes absent from the text PDFs),
    # skipping any code the deterministic parse already found.
    existing = {(i["subject"], i["code"]) for i in all_indicators}
    added = 0
    for sup in SUPPLEMENT:
        if (sup["subject"], sup["code"]) not in existing:
            all_indicators.append(dict(sup))
            added += 1
    if added:
        print(f"Supplemented {added} tracker-required indicator(s) absent from NaCCA text PDFs")
    all_indicators.sort(key=lambda x: (
        x["subject"], x["strand_number"], x["substrand_number"],
        x["content_standard"], x["code"],
    ))

    # Populate spiral-curriculum prerequisite_codes:
    # B9.<strand>.<substrand>.* links to B8 & B7 indicators in the same (subject, strand, substrand);
    # B8.<strand>.<substrand>.* links to B7 indicators in the same (subject, strand, substrand).
    by_sub: Dict[tuple, List[Dict]] = {}
    for ind in all_indicators:
        key = (ind["subject"], ind["strand_number"], ind["substrand_number"])
        by_sub.setdefault(key, []).append(ind)
    for key, group in by_sub.items():
        for ind in group:
            g = ind["grade"]
            if g == "B9":
                prereqs = [x["code"] for x in group if x["grade"] in ("B8", "B7")]
            elif g == "B8":
                prereqs = [x["code"] for x in group if x["grade"] == "B7"]
            else:
                prereqs = []
            ind["prerequisite_codes"] = prereqs

    out = Path(__file__).resolve().parent.parent / "data" / "taxonomy" / "nacca_b7_b9_indicators.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "source": "Official NaCCA CCP curriculum PDFs (text layer, deterministic parse)",
        "notes": "; ".join(notes),
        "indicators": all_indicators,
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(all_indicators)} indicators -> {out}")


if __name__ == "__main__":
    main()
