"""Phase 2 Curriculum Indicator Tagging Engine (2026 Multimodal + Listwise Hybrid).

Architecture:
1. Stage 1 — Multimodal + Text Vector Retrieval (`google/embeddinggemma-2`):
   - Gemma 4 architecture (270M text backbone + 170M vision encoder = 440M active params, audio tower unloaded).
   - Native 768d (or MRL 512d/256d) L2-normalized float32 embeddings cached in SQLite (`curriculum_indicators.embedding` & `questions.embedding`).
   - Combined with a Ghanaian BECE domain lexical-anchor booster within the same subject.
2. Stage 2 — Single-Pass Listwise Reranking (`jinaai/jina-reranker-v3.5`):
   - 0.6B Qwen3-based 3L2G hybrid-attention listwise reranker (LBNL) scoring top-15 candidates in one forward pass.
3. Stage 3 — Calibrated System-1 Decision Gate (`NandhaKishorM/laya`) & TypeLLM Permutation-Averaged Enum:
   - Uses `laya` (`convaiinnovations/laya`) single-pass RLCD calibrated choice + `noul` (yes/no syllabus fit) scoring.
   - Applies TypeLLM-style cyclic permutation averaging over candidate options to eliminate position bias, with conditional confidence gating (`confidence >= 0.70`) routing low-confidence or unmapped items to `tag_review_queue`.
"""

from __future__ import annotations

import json
import math
import os
import re
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np

from src.bank_schema import fts_rebuild, init_bank_schema
from src.config import BASE_DIR, DATABASE_PATH

EMBEDDING_MODEL_ID = "google/embeddinggemma-2"
RERANKER_MODEL_ID = "jinaai/jina-reranker-v3.5"
LAYA_MODEL_ID = "convaiinnovations/laya"


@dataclass
class CandidateScore:
    code: str
    uid: str
    grade: str
    strand_title: str
    substrand_title: str
    indicator_text: str
    embedding_score: float
    lexical_boost: float
    rerank_score: Optional[float] = None
    laya_score: Optional[float] = None
    llm_score: Optional[float] = None
    combined_score: float = 0.0


@dataclass
class TagDecision:
    question_id: str
    subject: str
    indicator_code: Optional[str]
    confidence: float
    tag_method: str
    top_candidates: List[Dict[str, Any]] = field(default_factory=list)
    needs_review: bool = False
    review_reason: Optional[str] = None


# ---------------------------------------------------------------------------
# Formatting helpers (official EmbeddingGemma 2 task instructions)
# ---------------------------------------------------------------------------

def format_indicator_document(row: MappingOrRow) -> str:
    """Format a curriculum_indicators row using EmbeddingGemma 2's titled document syntax."""
    code = row["code"]
    grade = row["grade"]
    strand = row["strand_title"]
    substrand = row["substrand_title"]
    cs_text = (row["content_standard_text"] or "").strip()
    ind_text = (row["indicator_text"] or "").strip()
    body = f"{cs_text}. {ind_text}".strip(". ")
    return f"title: {code} ({grade} {strand} - {substrand}) | text: {body}"


from src.question_extractor import decode_symbol_pua


def format_question_query_text(row: MappingOrRow) -> str:
    """Format a canonical question (stem + options) for retrieval."""
    q_text = decode_symbol_pua((row["question_text"] or "").strip())
    opts = []
    for label, col in [("A", "option_a"), ("B", "option_b"), ("C", "option_c"), ("D", "option_d")]:
        val = row[col] if col in row.keys() else None
        if val and str(val).strip():
            opts.append(f"{label}. {decode_symbol_pua(str(val).strip())}")
    if opts:
        return f"{q_text} Options: {' ; '.join(opts)}"
    return q_text


def resolve_diagram_path(diagram_path: Optional[str], base_dir: Path = BASE_DIR) -> Optional[Path]:
    """Resolve a relative or absolute diagram_path to an existing image file on disk."""
    if not diagram_path:
        return None
    p = Path(diagram_path)
    if p.is_file():
        return p
    candidate = base_dir / diagram_path
    if candidate.is_file():
        return candidate
    candidate2 = base_dir / "data" / "extracted_questions" / diagram_path
    if candidate2.is_file():
        return candidate2
    return None


def serialize_vector(vec: np.ndarray) -> bytes:
    """Serialize a 1D numpy vector to float32 bytes for SQLite BLOB storage."""
    arr = np.asarray(vec, dtype=np.float32).reshape(-1)
    norm = np.linalg.norm(arr)
    if norm > 0:
        arr = arr / norm
    return arr.tobytes()


def deserialize_vector(blob: bytes) -> np.ndarray:
    """Deserialize float32 bytes from SQLite BLOB into a 1D numpy array."""
    return np.frombuffer(blob, dtype=np.float32).copy()


# ---------------------------------------------------------------------------
# Domain Lexical-Anchor Booster for Ghana BECE / NaCCA B7–B9 Syllabus
# ---------------------------------------------------------------------------

_WORD_RE = re.compile(r"[a-z0-9]{3,}")
_RATIO_RE = re.compile(r"\b[a-z0-9]+\s*:\s*[a-z0-9]+\b", re.IGNORECASE)
_TIME_RE = re.compile(r"\b\d{1,2}:\d{2}\s*(?:am|pm|a\.m|p\.m)\b", re.IGNORECASE)
_PUA_RE = re.compile(r"[\uf000-\uf8ff]")

# High-precision syllabus keyword anchors mapped to substrand/indicator themes
_DOMAIN_SYNONYM_ANCHORS: Dict[str, List[str]] = {
    "surd": ["surd", "sqrt", "√", "rationalise", "rationalize", "conjugate", "irrational"],
    "set": ["venn", "subset", "union", "intersection", "complement", "universal set", "n(a", "∪", "∩", "⊂", "elements", "null set", "empty set", "disjoint"],
    "base": ["numeration", "base two", "base five", "base ten", "binary", "quinary", "octal", "roman numeral", "place value", "significant figure", "decimal place", "nearest"],
    "index": ["indices", "exponent", "power of", "standard form", "10^", "logarithm", "2^", "3^", "5^", "laws of indices"],
    "fraction": ["fraction", "bodmas", "mixed number", "improper", "numerator", "denominator", "decimal", "reciprocal", "lowest term"],
    "ratio": ["ratio", "proportion", "rate", "scale", "sharing", "shared", "direct proportion", "inverse proportion", "km/h", "m/s"],
    "percentage": ["percentage", "percent", "%", "discount", "commission", "profit", "loss", "simple interest", "vat", "tax", "depreciation", "gh₵", "ghc", "¢", "cedis", "cost price", "selling price", "principal", "per annum"],
    "algebra": ["factorise", "factorize", "expand", "algebraic", "simplify", "expression", "binomial", "quadratic", "like terms", "coefficient", "product of"],
    "equation": ["solve for", "truth set", "solution set", "inequality", "simultaneous", "linear equation", "find x", "find the value of", "make", "the subject", "subject of the relation"],
    "relation": ["mapping", "function", "gradient", "slope", "intercept", "linear graph", "cartesian", "coordinates", "ordered pair", "rule of the mapping"],
    "polygon_angles": ["polygon", "pentagon", "hexagon", "heptagon", "octagon", "nonagon", "decagon", "regular polygon", "exterior angle", "interior angle of a regular", "sum of interior angles", "sum of angles in any polygon", "missing angles in polygons"],
    "congruence_similarity": ["congruent", "congruence", "similar", "similarity", "corresponding sides", "identify similar and congruent"],
    "parallel_angles": ["alternate angle", "corresponding angle", "co-interior", "allied angle", "transversal", "parallel to", "parallel lines"],
    "triangle_angles": ["isosceles", "equilateral", "scalene", "angles in a triangle", "interior angles of a triangle", "triangle abc", "triangle xyz", "triangle pqr"],
    "basic_angles": ["complementary", "supplementary", "vertically opposite", "adjacent angle", "acute", "obtuse", "reflex", "right angle", "complete revolution", "bearing", "clockwise", "anti-clockwise"],
    "pythagoras": ["pythagoras", "hypotenuse", "right-angled", "elevation", "depression", "trigonometric", "sin ", "cos ", "tan ", "diagonal"],
    "vector": ["vector", "column vector", "magnitude", "direction", "translation vector", "mid-point", "position vector"],
    "transformation": ["reflection", "rotation", "enlargement", "rigid motion", "scale factor", "image of", "mirror line", "origin", "anticlockwise", "translate"],
    "construction": ["locus", "bisector", "perpendicular", "compass", "ruler", "construct", "equidistant", "mediator"],
    "mensuration": ["perimeter", "circumference", "area", "volume", "surface area", "cylinder", "cone", "sphere", "prism", "pyramid", "cuboid", "cube", "sector", "arc", "radius", "diameter", "trapezium", "rhombus", "parallelogram", "rectangle"],
    "statistics": ["mean", "median", "mode", "modal", "average", "frequency", "histogram", "pie chart", "bar chart", "stem and leaf", "quartile", "range", "distribution"],
    "probability": ["probability", "die", "dice", "coin", "random", "picked at random", "bag contains", "likely", "chance", "sample space", "outcome", "event"],
    "hardware": ["input device", "output device", "storage", "cpu", "motherboard", "ram", "rom", "printer", "scanner", "monitor", "keyboard", "mouse", "peripherals", "quantum", "qubit", "supercomputer", "fifth generation", "fifth-generation", "transistor", "microprocessor", "vacuum tube", "generation", "wearable", "optical", "hdd", "ssd", "pen drive", "system unit"],
    "software": ["operating system", "windows", "linux", "application software", "system software", "utility", "file management", "desktop", "icon", "folder", "taskbar", "recycle bin", "booting", "gui"],
    "word": ["word processing", "ms word", "microsoft word", "formatting", "font", "bold", "italic", "paragraph", "alignment", "spell check", "header", "footer", "ribbon", "ctrl+", "clipboard", "undo", "redo"],
    "spreadsheet": ["spreadsheet", "excel", "cell", "workbook", "worksheet", "formula", "=sum", "=average", "row", "column", "active cell", "autofill", "function"],
    "presentation": ["powerpoint", "presentation", "slide", "transition", "animation", "slide show", "placeholder"],
    "network": ["network", "lan", "wan", "pan", "man", "topology", "star topology", "bus topology", "ring topology", "router", "switch", "modem", "internet", "ip address", "protocol", "osi", "email", "browser", "url", "website", "webpage", "hyperlink", "search engine", "social media", "blog"],
    "algorithm": ["algorithm", "flowchart", "pseudocode", "variable", "loop", "iteration", "conditional", "debugging", "python", "scratch", "html", "programming", "code", "operator", "data type", "Boolean", "integer", "string", "robot", "sensor", "artificial intelligence"],
    "security": ["cyber", "virus", "malware", "phishing", "password", "firewall", "encryption", "copyright", "plagiarism", "ergonomics", "posture", "repetitive strain", "safety", "health", "hazard", "e-waste", "digital footprint"],
    "drawing": ["isometric", "orthographic", "oblique", "perspective", "projection", "plan", "elevation", "drawing instrument", "tee square", "set square", "protractor", "freehand", "sketch", "shading", "colour", "color", "primary colour", "secondary colour", "design process", "brief", "artifact"],
    "tools": ["cutting tool", "holding tool", "measuring tool", "marking out", "cutting", "shaping", "saw", "chisel", "plane", "file", "vice", "hammer", "mallet", "calliper", "try square", "hacksaw", "tenon saw", "scrib", "punch", "gauge", "spokeshave"],
    "materials": ["timber", "wood", "metal", "ferrous", "non-ferrous", "plastic", "thermoplastic", "thermosetting", "aggregate", "cement", "mortar", "brick", "block", "concrete", "seasoning", "adhesive", "solder", "fastener", "finish", "varnish", "paint", "lacquer", "sandpaper", "joint", "halving", "mortise", "dovetail", "butt joint"],
    "nutrition": ["nutrient", "protein", "carbohydrate", "vitamin", "mineral", "balanced diet", "cooking", "boiling", "steaming", "frying", "baking", "roasting", "stewing", "food preservation", "hygiene", "kitchen", "sewing", "seam", "stitch", "fabric", "garment", "crocheting", "knitting", "fibre", "cotton", "wool", "entrepreneur", "business"],
}


_VALID_SHORT_MATH_RE = re.compile(
    r"^(?:simplify|evaluate|solve|factori[sz]e|expand|find|express|convert|calculate|if|given)\b",
    re.IGNORECASE,
)
_MARKING_SCHEME_NOISE_RE = re.compile(
    r"(?:\bM1\s*A1\b|\bM1\b[\s\S]{1,60}\bA1\b|Approach\s+\d+\s*\(|Method\s+\d+\s+Sum\s+of)",
)
_SCRAMBLED_EQUATION_RE = re.compile(
    r"(?:(?:[+\-×÷=<>≤≥]\s+){2,}|^\.\s*\d+\s*[×÷+\-=])",
)


def is_malformed_question_text(question_text: str) -> bool:
    """Detect corrupted Private-Use-Area font strings, raw marking-scheme fragments, or truncated option fragments."""
    s = decode_symbol_pua((question_text or "").strip())
    if not s:
        return True
    pua_count = len(_PUA_RE.findall(s))
    alpha_count = len(re.findall(r"[A-Za-z]", s))
    if pua_count >= 2:
        return True
    if re.match(r"^[⇒∴=+\-×÷<>≤≥]", s):
        return True
    if _SCRAMBLED_EQUATION_RE.search(s):
        return True
    if _MARKING_SCHEME_NOISE_RE.search(s):
        return True
    if re.match(r"^[A-E][\)\.]\s+", s) and len(s) < 55:
        return True
    if alpha_count < 10 and not _VALID_SHORT_MATH_RE.match(s):
        return True
    return False


def compute_lexical_anchor_boost(question_text: str, indicator_row: MappingOrRow) -> float:
    """Compute a bounded [0.0, 0.24] lexical + curriculum-anchor overlap score.

    Weights `indicator_text` + `substrand_title` (specific to the indicator) higher than
    `content_standard_text` (shared across sibling indicators).
    """
    q_low = question_text.lower()
    specific_str = f"{indicator_row['substrand_title']} {indicator_row['indicator_text']}".lower()
    broad_str = f"{indicator_row['strand_title']} {indicator_row['content_standard_text'] or ''}".lower()

    q_tokens = set(_WORD_RE.findall(q_low))
    spec_tokens = set(_WORD_RE.findall(specific_str))
    broad_tokens = set(_WORD_RE.findall(broad_str))
    if not q_tokens or not (spec_tokens or broad_tokens):
        return 0.0

    stop = {
        "the", "and", "for", "with", "that", "this", "from", "are", "was", "were",
        "use", "using", "solve", "find", "given", "which", "following", "what",
        "demonstrate", "understanding", "apply", "identify", "describe", "explain",
        "problems", "involving", "real", "life", "concept", "concepts", "operations",
        "determine", "values", "value", "size", "sizes", "calculate", "calculating",
    }
    q_sig = q_tokens - stop
    spec_sig = spec_tokens - stop
    broad_sig = (broad_tokens - stop) - spec_sig

    spec_overlap = len(q_sig & spec_sig)
    broad_overlap = len(q_sig & broad_sig)
    token_score = min(0.10, spec_overlap * 0.028 + broad_overlap * 0.010)

    anchor_bonus = 0.0
    for cluster_name, terms in _DOMAIN_SYNONYM_ANCHORS.items():
        q_hit = any(t in q_low for t in terms)
        if not q_hit and cluster_name == "ratio":
            if _RATIO_RE.search(q_low) and not _TIME_RE.search(q_low):
                q_hit = True
        if q_hit:
            if any(t in specific_str for t in terms):
                anchor_bonus += 0.075
            elif any(t in broad_str for t in terms):
                anchor_bonus += 0.020

    grade_bonus = 0.015 if indicator_row["grade"] == "B9" else 0.0
    return min(0.24, token_score + min(0.14, anchor_bonus) + grade_bonus)


# ---------------------------------------------------------------------------
# Stage 1 Backend: google/embeddinggemma-2
# ---------------------------------------------------------------------------

class EmbeddingGemma2Backend:
    """Wrapper around `google/embeddinggemma-2` (Gemma 4 multimodal + text embedder).

    Supports selective encoder loading (`audio_config=None` for text+image 440M, or
    `vision_config=None, audio_config=None` for text-only 270M) and MRL truncation.
    Always runs in `float32` / `bfloat16` (never `float16`, per model spec).
    """

    def __init__(
        self,
        model_id: str = EMBEDDING_MODEL_ID,
        truncate_dim: int = 768,
        enable_vision: bool = False,
        device: str = "cpu",
    ) -> None:
        self.model_id = model_id
        self.truncate_dim = truncate_dim
        self.enable_vision = enable_vision
        self.device = device
        self._model: Any = None

    def _load(self) -> Any:
        if self._model is not None:
            return self._model
        import torch
        from sentence_transformers import SentenceTransformer

        torch.set_num_threads(os.cpu_count() or 8)
        config_kwargs: Dict[str, Any] = {"audio_config": None}
        if not self.enable_vision:
            config_kwargs["vision_config"] = None

        self._model = SentenceTransformer(
            self.model_id,
            device=self.device,
            model_kwargs={"dtype": torch.bfloat16 if self.device == "cpu" else torch.float32},
            config_kwargs=config_kwargs,
        )
        self._model.max_seq_length = 96
        return self._model

    def encode_documents(self, docs: Sequence[str], batch_size: int = 32) -> np.ndarray:
        """Encode already-prefixed indicator documents (`title: ... | text: ...`)."""
        model = self._load()
        vecs = model.encode(
            [d[:420] for d in docs],
            batch_size=batch_size,
            truncate_dim=self.truncate_dim,
            normalize_embeddings=True,
            show_progress_bar=False,
            convert_to_numpy=True,
        )
        return np.asarray(vecs, dtype=np.float32)

    def encode_queries(
        self,
        queries: Sequence[str],
        diagram_paths: Optional[Sequence[Optional[Path]]] = None,
        batch_size: int = 32,
    ) -> np.ndarray:
        """Encode search queries or exam questions (with optional multimodal diagram fusion)."""
        model = self._load()
        if not self.enable_vision or diagram_paths is None:
            prefixed = [f"task: search result | query: {q[:360]}" for q in queries]
            vecs = model.encode(
                prefixed,
                batch_size=batch_size,
                truncate_dim=self.truncate_dim,
                normalize_embeddings=True,
                show_progress_bar=False,
                convert_to_numpy=True,
            )
            return np.asarray(vecs, dtype=np.float32)

        # Multimodal path: interleave `<|image|>` when a valid diagram image exists
        from PIL import Image

        inputs: List[Any] = []
        for q, img_path in zip(queries, diagram_paths):
            if img_path is not None and img_path.is_file():
                try:
                    img = Image.open(img_path).convert("RGB")
                    inputs.append(
                        {
                            "text": f"task: search result | query: {q} <|image|>",
                            "image": [img],
                        }
                    )
                    continue
                except Exception:
                    pass
            inputs.append(f"task: search result | query: {q}")

        vecs = model.encode(
            inputs,
            batch_size=max(4, batch_size // 4),
            truncate_dim=self.truncate_dim,
            normalize_embeddings=True,
            show_progress_bar=False,
            convert_to_numpy=True,
        )
        return np.asarray(vecs, dtype=np.float32)


# ---------------------------------------------------------------------------
# Stage 2 Backend: jinaai/jina-reranker-v3.5 (Listwise LBNL Reranker)
# ---------------------------------------------------------------------------

class JinaListwiseRerankerBackend:
    """Wrapper around `jinaai/jina-reranker-v3.5` (0.6B 3L2G hybrid-attention listwise reranker)."""

    def __init__(self, model_id: str = RERANKER_MODEL_ID, device: str = "cpu") -> None:
        self.model_id = model_id
        self.device = device
        self._model: Any = None

    def _load(self) -> Any:
        if self._model is not None:
            return self._model
        import torch
        from transformers import AutoModel

        self._model = AutoModel.from_pretrained(
            self.model_id,
            dtype=torch.float32 if self.device == "cpu" else "auto",
            trust_remote_code=True,
        )
        self._model.to(self.device)
        self._model.eval()
        return self._model

    def rerank(
        self,
        query: str,
        documents: Sequence[str],
        top_n: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Score a query against multiple candidate indicator documents in a single listwise pass."""
        if not documents:
            return []
        model = self._load()
        results = model.rerank(
            query=query,
            documents=list(documents),
            top_n=top_n or len(documents),
        )
        return list(results)


# ---------------------------------------------------------------------------
# Stage 3 Backend: NandhaKishorM/laya + TypeLLM Permutation Averaging
# ---------------------------------------------------------------------------

def cyclic_permutations(items: Sequence[Any], num_permutations: int = 2) -> List[List[Any]]:
    """Generate evenly spaced cyclic shifts of `items` for TypeLLM permutation averaging.

    Averaging predictions across cyclic shifts eliminates positional preference bias
    in multiple-choice / enum selection.
    """
    n = len(items)
    if n <= 1 or num_permutations <= 1:
        return [list(items)]
    shifts: List[List[Any]] = []
    seen_offsets = set()
    for i in range(num_permutations):
        offset = (i * max(1, n // num_permutations)) % n
        if offset in seen_offsets:
            offset = (offset + 1) % n
        seen_offsets.add(offset)
        shifted = list(items[offset:]) + list(items[:offset])
        shifts.append(shifted)
    return shifts


class LayaDecisionGateBackend:
    """Wrapper around `NandhaKishorM/laya` (`convaiinnovations/laya`) non-autoregressive
    System-1 decision engine with TypeLLM permutation averaging.
    """

    def __init__(self, preload: bool = False) -> None:
        self.preload = preload
        self._router: Any = None

    def _load(self) -> Any:
        if self._router is not None:
            return self._router
        from laya import Router

        self._router = Router(preload=self.preload)
        return self._router

    def evaluate_candidates(
        self,
        question_text: str,
        subject: str,
        candidates: Sequence[CandidateScore],
        num_permutations: int = 2,
    ) -> Tuple[Optional[str], float, float]:
        """Run permutation-averaged Laya `"choice"` + `"noul"` decision over top candidates.

        Returns `(best_code, choice_agreement_score, in_syllabus_probability)`.
        """
        if not candidates:
            return None, 0.0, 0.0

        router = self._load()
        perms = cyclic_permutations(list(candidates), num_permutations=num_permutations)
        vote_weights: Dict[str, float] = {c.code: 0.0 for c in candidates}
        noul_probs: List[float] = []

        for perm in perms:
            criteria = {
                c.code: f"{c.grade} {c.substrand_title}: {c.indicator_text[:180]}"
                for c in perm
            }
            spec = {
                "indicator": {
                    "type": "choice",
                    "instructions": f"Which Ghana GES {subject} curriculum indicator best matches this exam question?",
                    "criteria": criteria,
                },
                "in_syllabus": {
                    "type": "noul",
                    "instructions": "Does this question clearly test one of the listed curriculum indicators?",
                },
            }
            res = router.predict(question_text[:1000], spec)
            ans = res.get("answers", {})
            chosen = ans.get("indicator", {}).get("choice")
            if chosen in vote_weights:
                vote_weights[chosen] += 1.0 / len(perms)

            noul_val = ans.get("in_syllabus", {}).get("noul")
            if isinstance(noul_val, (int, float)):
                noul_probs.append(float(noul_val))
            elif isinstance(noul_val, dict) and "yes" in noul_val:
                noul_probs.append(float(noul_val["yes"]))
            else:
                noul_probs.append(0.75)

        best_code = max(vote_weights.items(), key=lambda kv: kv[1])[0]
        agreement = vote_weights[best_code]
        in_syllabus_prob = float(np.mean(noul_probs)) if noul_probs else 0.75
        return best_code, agreement, in_syllabus_prob


# ---------------------------------------------------------------------------
# TypeLLM Conditional Confidence & Bounding-Box Schema Helpers
# ---------------------------------------------------------------------------

def build_typellm_indicator_schema(
    candidate_codes: Sequence[str],
    min_confidence: float = 0.70,
) -> Dict[str, Any]:
    """Build a TypeLLM-compatible structured JSON schema with conditional confidence gating."""
    enum_options = list(dict.fromkeys(list(candidate_codes) + ["UNMAPPED"]))
    return {
        "type": "object",
        "properties": {
            "indicator_code": {
                "type": "string",
                "enum": enum_options,
                "description": "Exact Ghana NaCCA curriculum indicator code from the candidate list, or UNMAPPED.",
            },
            "confidence": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0,
                "description": "Calibrated confidence in [0.0, 1.0] that the question tests this exact indicator.",
            },
            "committed_indicator": {
                "type": "string",
                "enum": enum_options,
                "when": {"indicator_code": {"confidence": {"gte": min_confidence}}},
            },
        },
        "required": ["indicator_code", "confidence"],
        "additionalProperties": False,
    }


def build_typellm_scanned_page_boxes_schema() -> Dict[str, Any]:
    """Build a TypeLLM `boxes` schema (2026-10-15 spec) for extracting questions + diagram crops from scanned PDFs."""
    return {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question_number": {"type": "integer"},
                        "question_text": {"type": "string"},
                        "option_a": {"type": ["string", "null"]},
                        "option_b": {"type": ["string", "null"]},
                        "option_c": {"type": ["string", "null"]},
                        "option_d": {"type": ["string", "null"]},
                        "diagram_boxes": {
                            "type": "array",
                            "description": "Bounding boxes [ymin, xmin, ymax, xmax] normalized 0..1000 for any figures/diagrams belonging to this question.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "label": {"type": "string"},
                                    "box_2d": {
                                        "type": "array",
                                        "items": {"type": "number"},
                                        "minItems": 4,
                                        "maxItems": 4,
                                    },
                                },
                                "required": ["label", "box_2d"],
                            },
                        },
                    },
                    "required": ["question_number", "question_text", "diagram_boxes"],
                },
            }
        },
        "required": ["questions"],
    }


# ---------------------------------------------------------------------------
# Main CurriculumTagger Orchestrator
# ---------------------------------------------------------------------------

MappingOrRow = Any


class CurriculumTagger:
    """Hybrid Retrieve-Rerank-Decide Curriculum Tagging Engine for `catalog.db`."""

    def __init__(
        self,
        db_path: Path = DATABASE_PATH,
        embedder: Optional[Any] = None,
        reranker: Optional[Any] = None,
        laya_gate: Optional[Any] = None,
        truncate_dim: int = 768,
        enable_vision: bool = False,
        confidence_threshold: float = 0.70,
        auto_commit_margin: float = 0.035,
    ) -> None:
        self.db_path = Path(db_path)
        init_bank_schema(self.db_path)
        self.truncate_dim = truncate_dim
        self.confidence_threshold = confidence_threshold
        self.auto_commit_margin = auto_commit_margin
        self._embedder = embedder or EmbeddingGemma2Backend(
            truncate_dim=truncate_dim,
            enable_vision=enable_vision,
        )
        self._reranker = reranker
        self._laya_gate = laya_gate

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    def repair_symbol_pua_in_db(self) -> int:
        """Decode single-glyph Microsoft Symbol / Wingdings PUA codepoints in questions table."""
        with self._connect() as conn:
            has_q = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='questions';").fetchone()
            if not has_q:
                return 0
            rows = conn.execute("SELECT id, question_text, option_a, option_b, option_c, option_d FROM questions;").fetchall()
            updates = []
            for r in rows:
                qid = r["id"]
                qt = r["question_text"] or ""
                oa = r["option_a"] or ""
                ob = r["option_b"] or ""
                oc = r["option_c"] or ""
                od = r["option_d"] or ""

                n_qt = decode_symbol_pua(qt)
                n_oa = decode_symbol_pua(oa)
                n_ob = decode_symbol_pua(ob)
                n_oc = decode_symbol_pua(oc)
                n_od = decode_symbol_pua(od)

                if (n_qt != qt) or (n_oa != oa) or (n_ob != ob) or (n_oc != oc) or (n_od != od):
                    updates.append((n_qt, n_oa, n_ob, n_oc, n_od, qid))

            if updates:
                conn.executemany(
                    """
                    UPDATE questions
                    SET question_text = ?, option_a = ?, option_b = ?, option_c = ?, option_d = ?
                    WHERE id = ?;
                    """,
                    updates,
                )
                conn.commit()
            return len(updates)

    def ensure_indicator_embeddings(self, force: bool = False, batch_size: int = 32) -> int:
        """Compute and store `google/embeddinggemma-2` embeddings for `curriculum_indicators`."""
        with self._connect() as conn:
            if force:
                rows = conn.execute(
                    "SELECT * FROM curriculum_indicators ORDER BY subject, code;"
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM curriculum_indicators WHERE embedding IS NULL ORDER BY subject, code;"
                ).fetchall()

            if not rows:
                return 0

            docs = [format_indicator_document(r) for r in rows]
            vecs = self._embedder.encode_documents(docs, batch_size=batch_size)

            updates = [
                (serialize_vector(vec), row["uid"])
                for row, vec in zip(rows, vecs)
            ]
            conn.executemany(
                "UPDATE curriculum_indicators SET embedding = ? WHERE uid = ?;",
                updates,
            )
            conn.commit()
            return len(updates)

    def ensure_question_embeddings(
        self,
        force: bool = False,
        batch_size: int = 64,
        subject: Optional[str] = None,
    ) -> int:
        """Compute and store `google/embeddinggemma-2` embeddings for canonical `questions`."""
        with self._connect() as conn:
            sql = "SELECT * FROM questions"
            params: List[Any] = []
            clauses: List[str] = []
            if not force:
                clauses.append("embedding IS NULL")
            if subject:
                clauses.append("subject = ?")
                params.append(subject)
            if clauses:
                sql += " WHERE " + " AND ".join(clauses)
            sql += " ORDER BY id;"

            rows = conn.execute(sql, params).fetchall()
            if not rows:
                return 0

            # Sort by formatted text length so each batch has uniform token length (minimizes CPU padding)
            prepared = [
                (
                    r,
                    format_question_query_text(r),
                    resolve_diagram_path(r["diagram_path"]) if r["has_diagram"] else None,
                )
                for r in rows
            ]
            prepared.sort(key=lambda item: len(item[1]))

            checkpoint_size = max(batch_size, 256)
            total_updated = 0
            for start in range(0, len(prepared), checkpoint_size):
                chunk = prepared[start : start + checkpoint_size]
                queries = [item[1] for item in chunk]
                diag_paths = [item[2] for item in chunk]
                vecs = self._embedder.encode_queries(
                    queries,
                    diagram_paths=diag_paths,
                    batch_size=batch_size,
                )
                updates = [
                    (serialize_vector(vec), item[0]["id"])
                    for item, vec in zip(chunk, vecs)
                ]
                conn.executemany(
                    "UPDATE questions SET embedding = ? WHERE id = ?;",
                    updates,
                )
                conn.commit()
                total_updated += len(updates)

            return total_updated

    def _load_indicators_by_subject(
        self, conn: sqlite3.Connection
    ) -> Dict[str, Tuple[List[sqlite3.Row], np.ndarray]]:
        """Load all curriculum_indicators grouped by subject with their normalized vector matrix."""
        rows = conn.execute(
            "SELECT * FROM curriculum_indicators WHERE embedding IS NOT NULL ORDER BY subject, code;"
        ).fetchall()
        grouped_rows: Dict[str, List[sqlite3.Row]] = {}
        grouped_vecs: Dict[str, List[np.ndarray]] = {}
        for r in rows:
            subj = r["subject"]
            vec = deserialize_vector(r["embedding"])
            grouped_rows.setdefault(subj, []).append(r)
            grouped_vecs.setdefault(subj, []).append(vec)

        result: Dict[str, Tuple[List[sqlite3.Row], np.ndarray]] = {}
        for subj, r_list in grouped_rows.items():
            mat = np.vstack(grouped_vecs[subj]).astype(np.float32)
            result[subj] = (r_list, mat)
        return result

    @staticmethod
    def _calibrate_confidence(top1: float, top2: float, has_lexical_hit: bool) -> float:
        """Map raw hybrid cosine + lexical score and top1-top2 margin to a calibrated [0.0, 0.99] confidence."""
        margin = max(0.0, top1 - top2)
        z = (top1 - 0.655) * 14.0 + margin * 22.0 + (0.65 if has_lexical_hit else -0.15)
        prob = 1.0 / (1.0 + math.exp(-z))
        return round(min(0.99, max(0.05, prob)), 4)

    def score_question_candidates(
        self,
        question_row: MappingOrRow,
        q_vec: np.ndarray,
        ind_rows: Sequence[MappingOrRow],
        ind_matrix: np.ndarray,
        top_k: int = 10,
        use_reranker: bool = False,
        use_laya: bool = False,
    ) -> List[CandidateScore]:
        """Run Stage 1 (and optional Stage 2/3) candidate scoring for a single question."""
        q_text = format_question_query_text(question_row)
        cos_scores = np.dot(ind_matrix, q_vec).astype(np.float64)

        candidates: List[CandidateScore] = []
        for idx, ind_row in enumerate(ind_rows):
            emb_s = float(cos_scores[idx])
            lex_b = compute_lexical_anchor_boost(q_text, ind_row)
            comb = emb_s + lex_b
            candidates.append(
                CandidateScore(
                    code=ind_row["code"],
                    uid=ind_row["uid"],
                    grade=ind_row["grade"],
                    strand_title=ind_row["strand_title"],
                    substrand_title=ind_row["substrand_title"],
                    indicator_text=ind_row["indicator_text"],
                    embedding_score=round(emb_s, 4),
                    lexical_boost=round(lex_b, 4),
                    combined_score=round(comb, 4),
                )
            )

        candidates.sort(key=lambda c: c.combined_score, reverse=True)
        shortlist = candidates[:top_k]

        if len(shortlist) < 2:
            return shortlist

        margin = shortlist[0].combined_score - shortlist[1].combined_score

        # Stage 2: Optional listwise reranking (`jinaai/jina-reranker-v3.5`) for low-margin items
        if use_reranker and self._reranker is not None and margin < self.auto_commit_margin:
            docs = [
                f"{c.code} ({c.grade} {c.strand_title} - {c.substrand_title}): {c.indicator_text}"
                for c in shortlist
            ]
            reranked = self._reranker.rerank(q_text, docs, top_n=min(5, len(shortlist)))
            for item in reranked:
                orig_idx = int(item["index"])
                r_score = float(item["relevance_score"])
                shortlist[orig_idx].rerank_score = round(r_score, 4)
                shortlist[orig_idx].combined_score = round(
                    0.55 * shortlist[orig_idx].combined_score + 0.45 * r_score,
                    4,
                )
            shortlist.sort(key=lambda c: c.combined_score, reverse=True)
            margin = shortlist[0].combined_score - shortlist[1].combined_score

        # Stage 3: Optional Laya System-1 calibrated permutation-averaged gate for borderline items
        if use_laya and self._laya_gate is not None and margin < self.auto_commit_margin:
            top5 = shortlist[:5]
            best_code, agreement, in_syl_prob = self._laya_gate.evaluate_candidates(
                q_text,
                question_row["subject"],
                top5,
                num_permutations=2,
            )
            for c in top5:
                if c.code == best_code:
                    c.laya_score = round(agreement * in_syl_prob, 4)
                    c.combined_score = round(c.combined_score + 0.08 * c.laya_score, 4)
                else:
                    c.laya_score = 0.0
            shortlist.sort(key=lambda c: c.combined_score, reverse=True)

        return shortlist

    def tag_all_questions(
        self,
        subject: Optional[str] = None,
        only_untagged: bool = False,
        use_reranker: bool = False,
        use_laya: bool = False,
        batch_size: int = 64,
    ) -> Dict[str, Any]:
        """Embed and tag all canonical questions in `catalog.db`, routing `< 0.70` confidence items to `tag_review_queue`."""
        repaired_pua = self.repair_symbol_pua_in_db()
        ind_embedded = self.ensure_indicator_embeddings(batch_size=batch_size)
        q_embedded = self.ensure_question_embeddings(subject=subject, batch_size=batch_size)

        with self._connect() as conn:
            ind_by_subj = self._load_indicators_by_subject(conn)

            sql = "SELECT * FROM questions"
            clauses: List[str] = []
            params: List[Any] = []
            if subject:
                clauses.append("subject = ?")
                params.append(subject)
            if only_untagged:
                clauses.append("indicator_code IS NULL")
            if clauses:
                sql += " WHERE " + " AND ".join(clauses)
            sql += " ORDER BY id;"

            q_rows = conn.execute(sql, params).fetchall()

            tagged_count = 0
            review_count = 0
            by_subject: Dict[str, int] = {}

            q_updates: List[Tuple[Optional[str], float, str, str]] = []
            review_inserts: List[Tuple[str, str, str]] = []

            for q_row in q_rows:
                subj = q_row["subject"]
                if subj not in ind_by_subj or not q_row["embedding"]:
                    review_inserts.append(
                        (
                            q_row["id"],
                            "unmapped",
                            json.dumps({"error": f"No indicators or embedding for subject {subj}"}),
                        )
                    )
                    review_count += 1
                    continue

                ind_rows, ind_mat = ind_by_subj[subj]
                q_vec = deserialize_vector(q_row["embedding"])
                shortlist = self.score_question_candidates(
                    q_row,
                    q_vec,
                    ind_rows,
                    ind_mat,
                    top_k=8,
                    use_reranker=use_reranker,
                    use_laya=use_laya,
                )

                if not shortlist:
                    review_inserts.append(
                        (q_row["id"], "unmapped", json.dumps({"candidates": []}))
                    )
                    review_count += 1
                    continue

                top1 = shortlist[0]
                diff_sub_scores = [
                    c.combined_score
                    for c in shortlist[1:]
                    if c.substrand_title != top1.substrand_title
                ]
                if diff_sub_scores:
                    top2_score = diff_sub_scores[0]
                elif len(shortlist) > 1:
                    top2_score = shortlist[1].combined_score - 0.025
                else:
                    top2_score = top1.combined_score - 0.15

                malformed = is_malformed_question_text(q_row["question_text"])
                conf = self._calibrate_confidence(
                    top1.combined_score,
                    top2_score,
                    has_lexical_hit=(top1.lexical_boost >= 0.035),
                )
                if malformed:
                    conf = round(min(conf, 0.45), 4)

                method_parts = ["embeddinggemma2"]
                if top1.lexical_boost > 0:
                    method_parts.append("lexical")
                if top1.rerank_score is not None:
                    method_parts.append("jina_rerank_v3.5")
                if top1.laya_score is not None:
                    method_parts.append("laya_perm")
                tag_method = "+".join(method_parts)

                q_updates.append((top1.code, conf, tag_method, q_row["id"]))
                tagged_count += 1
                by_subject[subj] = by_subject.get(subj, 0) + 1

                if malformed or conf < self.confidence_threshold:
                    reason = "malformed_extraction" if malformed else "low_confidence"
                    details = json.dumps(
                        {
                            "assigned_code": top1.code,
                            "confidence": conf,
                            "top_candidates": [
                                {
                                    "code": c.code,
                                    "grade": c.grade,
                                    "substrand": c.substrand_title,
                                    "score": c.combined_score,
                                }
                                for c in shortlist[:5]
                            ],
                        }
                    )
                    review_inserts.append((q_row["id"], reason, details))
                    review_count += 1

            conn.executemany(
                "UPDATE questions SET indicator_code = ?, confidence = ?, tag_method = ? WHERE id = ?;",
                q_updates,
            )
            # Clear previously open low_confidence / malformed_extraction entries for re-evaluated questions
            evaluated_ids = [(qid,) for _, _, _, qid in q_updates]
            if evaluated_ids:
                conn.executemany(
                    """
                    UPDATE tag_review_queue
                    SET status = 'resolved', resolved_at = CURRENT_TIMESTAMP
                    WHERE question_id = ? AND reason IN ('low_confidence', 'malformed_extraction') AND status = 'open';
                    """,
                    evaluated_ids,
                )
            if review_inserts:
                conn.executemany(
                    """
                    INSERT INTO tag_review_queue (question_id, reason, details, status)
                    VALUES (?, ?, ?, 'open')
                    ON CONFLICT(question_id, reason) DO UPDATE SET
                        details = excluded.details,
                        status = 'open',
                        resolved_at = NULL;
                    """,
                    review_inserts,
                )
            fts_rebuild(conn)
            conn.commit()

        return {
            "indicators_embedded": ind_embedded,
            "questions_embedded": q_embedded,
            "questions_tagged": tagged_count,
            "routed_to_review": review_count,
            "by_subject": by_subject,
        }

    def semantic_search(
        self,
        query: str,
        subject: Optional[str] = None,
        indicator_code: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Hybrid dense (`google/embeddinggemma-2`) + FTS5 search over canonical questions."""
        q_vec = self._embedder.encode_queries([query], batch_size=1)[0]

        with self._connect() as conn:
            sql = """
                SELECT q.*, ci.grade AS indicator_grade, ci.strand_title, ci.substrand_title, ci.indicator_text
                FROM questions q
                LEFT JOIN curriculum_indicators ci
                  ON ci.subject = q.subject AND ci.code = q.indicator_code
                WHERE q.embedding IS NOT NULL
            """
            params: List[Any] = []
            if subject:
                sql += " AND q.subject = ?"
                params.append(subject)
            if indicator_code:
                sql += " AND q.indicator_code = ?"
                params.append(indicator_code)

            rows = conn.execute(sql, params).fetchall()
            if not rows:
                return []

            # Optional FTS5 boost set
            fts_hits: Dict[str, int] = {}
            safe_tokens = [t for t in _WORD_RE.findall(query.lower()) if len(t) >= 3]
            if safe_tokens:
                fts_q = " OR ".join(safe_tokens[:6])
                try:
                    fts_rows = conn.execute(
                        "SELECT id, rank FROM questions_fts WHERE questions_fts MATCH ? LIMIT 100;",
                        (fts_q,),
                    ).fetchall()
                    for rank_idx, fr in enumerate(fts_rows):
                        fts_hits[fr["id"]] = rank_idx + 1
                except sqlite3.Error:
                    pass

            scored: List[Tuple[float, sqlite3.Row]] = []
            for r in rows:
                vec = deserialize_vector(r["embedding"])
                dense_sim = float(np.dot(vec, q_vec))
                fts_rank = fts_hits.get(r["id"])
                fts_bonus = (1.0 / (20.0 + fts_rank)) if fts_rank is not None else 0.0
                total_score = dense_sim + fts_bonus
                scored.append((total_score, r))

            scored.sort(key=lambda item: item[0], reverse=True)
            results: List[Dict[str, Any]] = []
            for score, r in scored[:limit]:
                d = dict(r)
                d.pop("embedding", None)
                d["search_score"] = round(score, 4)
                results.append(d)
            return results
