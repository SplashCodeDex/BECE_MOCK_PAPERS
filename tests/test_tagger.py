"""Unit and integration tests for Phase 2 CurriculumTagger (`src/tagger.py`)."""

from pathlib import Path
from typing import List, Optional, Sequence
import numpy as np
import pytest

from src.bank_schema import init_bank_schema
from src.tagger import (
    CandidateScore,
    CurriculumTagger,
    build_typellm_indicator_schema,
    build_typellm_scanned_page_boxes_schema,
    compute_lexical_anchor_boost,
    cyclic_permutations,
    deserialize_vector,
    format_indicator_document,
    format_question_query_text,
    serialize_vector,
)


class DeterministicFakeEmbedder:
    """Deterministic keyword-aware fake embedder for fast unit testing of the CurriculumTagger."""

    def __init__(self, dim: int = 16) -> None:
        self.dim = dim

    def _text_to_vec(self, text: str) -> np.ndarray:
        low = text.lower()
        vec = np.full(self.dim, 0.01, dtype=np.float32)
        if any(k in low for k in ["surd", "sqrt", "√", "rationalise", "conjugate"]):
            vec[0] = 1.0
        if any(k in low for k in ["venn", "subset", "union", "intersection", "set"]):
            vec[1] = 1.0
        if any(k in low for k in ["spreadsheet", "excel", "=sum", "worksheet", "cell"]):
            vec[2] = 1.0
        if any(k in low for k in ["network", "topology", "lan", "router", "osi"]):
            vec[3] = 1.0
        if any(k in low for k in ["isometric", "orthographic", "projection", "drawing"]):
            vec[4] = 1.0
        norm = np.linalg.norm(vec)
        return vec / norm

    def encode_documents(self, docs: Sequence[str], batch_size: int = 32) -> np.ndarray:
        return np.vstack([self._text_to_vec(d) for d in docs]).astype(np.float32)

    def encode_queries(
        self,
        queries: Sequence[str],
        diagram_paths: Optional[Sequence[Optional[Path]]] = None,
        batch_size: int = 32,
    ) -> np.ndarray:
        return np.vstack([self._text_to_vec(q) for q in queries]).astype(np.float32)


class FakeListwiseReranker:
    """Fake Jina v3.5 listwise reranker for verifying Stage 2 integration."""

    def rerank(self, query: str, documents: Sequence[str], top_n: Optional[int] = None) -> List[dict]:
        q_low = query.lower()
        scored = []
        for idx, doc in enumerate(documents):
            d_low = doc.lower()
            score = 0.85 if ("surd" in q_low and "surd" in d_low) else 0.25
            scored.append({"index": idx, "document": doc, "relevance_score": score})
        scored.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored[: (top_n or len(scored))]


class FakeLayaGate:
    """Fake Laya System-1 decision gate for verifying Stage 3 permutation averaging."""

    def evaluate_candidates(
        self,
        question_text: str,
        subject: str,
        candidates: Sequence[CandidateScore],
        num_permutations: int = 2,
    ):
        perms = cyclic_permutations(candidates, num_permutations=num_permutations)
        assert len(perms) >= 1
        return candidates[0].code, 1.0, 0.92


def test_vector_serialization_roundtrip():
    raw = np.array([3.0, 4.0, 0.0, 0.0], dtype=np.float32)
    blob = serialize_vector(raw)
    restored = deserialize_vector(blob)
    assert restored.shape == (4,)
    assert np.isclose(np.linalg.norm(restored), 1.0, atol=1e-5)
    assert np.allclose(restored, np.array([0.6, 0.8, 0.0, 0.0], dtype=np.float32))


def test_formatting_and_lexical_anchor_boost():
    ind = {
        "code": "B9.1.1.2.2",
        "grade": "B9",
        "strand_title": "NUMBER",
        "substrand_title": "Number Operations (Surds)",
        "content_standard_text": "Perform operations on surds",
        "indicator_text": "Simplify and rationalise surds with conjugate denominators.",
    }
    doc = format_indicator_document(ind)
    assert doc.startswith("title: B9.1.1.2.2 (B9 NUMBER - Number Operations (Surds)) | text:")

    q_row = {
        "question_text": "Simplify 1 / (sqrt(3) - 1) leaving your answer in surd form.",
        "option_a": "(sqrt(3)+1)/2",
        "option_b": "(sqrt(3)-1)/2",
        "option_c": "sqrt(3)",
        "option_d": "2",
    }
    q_fmt = format_question_query_text(q_row)
    assert "Options: A." in q_fmt

    boost = compute_lexical_anchor_boost(q_fmt, ind)
    assert boost >= 0.08


def test_typellm_permutations_and_schemas():
    items = ["B9.1.1.1.1", "B9.1.1.2.2", "B9.1.2.1.1", "B9.2.1.1.1"]
    perms = cyclic_permutations(items, num_permutations=2)
    assert len(perms) == 2
    assert perms[0] != perms[1]
    assert set(perms[0]) == set(items)

    schema = build_typellm_indicator_schema(items, min_confidence=0.70)
    assert "UNMAPPED" in schema["properties"]["indicator_code"]["enum"]
    assert schema["properties"]["committed_indicator"]["when"]["indicator_code"]["confidence"]["gte"] == 0.70

    box_schema = build_typellm_scanned_page_boxes_schema()
    assert "diagram_boxes" in box_schema["properties"]["questions"]["items"]["properties"]


def test_curriculum_tagger_end_to_end(tmp_path: Path):
    db_path = tmp_path / "test_catalog.db"
    init_bank_schema(db_path)

    import sqlite3
    conn = sqlite3.connect(str(db_path))
    conn.executemany(
        """
        INSERT INTO curriculum_indicators (
            uid, code, grade, subject, strand_number, strand_title,
            substrand_number, substrand_title, content_standard,
            content_standard_text, indicator_text
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        [
            (
                "Mathematics:B9.1.1.2.2",
                "B9.1.1.2.2",
                "B9",
                "Mathematics",
                1,
                "NUMBER",
                1,
                "Number Operations",
                "B9.1.1.2",
                "Operations on surds",
                "Simplify and rationalise surds and conjugate denominators",
            ),
            (
                "Mathematics:B8.1.1.2.1",
                "B8.1.1.2.1",
                "B8",
                "Mathematics",
                1,
                "NUMBER",
                1,
                "Sets",
                "B8.1.1.2",
                "Sets and Venn diagrams",
                "Use Venn diagrams to solve two-set union and intersection problems",
            ),
            (
                "Computing_ICT:B9.2.3.1.1",
                "B9.2.3.1.1",
                "B9",
                "Computing_ICT",
                2,
                "PRODUCTIVITY SOFTWARE",
                3,
                "Introduction to Electronic Spreadsheet",
                "B9.2.3.1",
                "Spreadsheet formulas",
                "Perform calculations in Excel worksheet cells using =SUM and =AVERAGE formulas",
            ),
        ],
    )
    conn.executemany(
        """
        INSERT INTO questions (
            id, subject, question_text, option_a, option_b, option_c, option_d, dedup_hash
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """,
        [
            (
                "Q_test_surd01",
                "Mathematics",
                "Rationalise the surd expression 4 / (sqrt(5) - 1).",
                "sqrt(5)+1",
                "sqrt(5)-1",
                "2",
                "5",
                "hash_surd_01",
            ),
            (
                "Q_test_excel1",
                "Computing_ICT",
                "Which spreadsheet formula in Excel calculates the total of cells A1 to A10 in a worksheet?",
                "=SUM(A1:A10)",
                "=ADD(A1:A10)",
                "=TOTAL(A1:A10)",
                "=COUNT(A1:A10)",
                "hash_excel_01",
            ),
            (
                "Q_test_ambig1",
                "Mathematics",
                "Unrelated mystery puzzle with no matching math keywords at all.",
                "1",
                "2",
                "3",
                "4",
                "hash_ambig_01",
            ),
        ],
    )
    conn.commit()
    conn.close()

    tagger = CurriculumTagger(
        db_path=db_path,
        embedder=DeterministicFakeEmbedder(dim=16),
        reranker=FakeListwiseReranker(),
        laya_gate=FakeLayaGate(),
        truncate_dim=16,
        confidence_threshold=0.70,
        auto_commit_margin=0.05,
    )

    summary = tagger.tag_all_questions(use_reranker=True, use_laya=True)
    assert summary["indicators_embedded"] == 3
    assert summary["questions_embedded"] == 3
    assert summary["questions_tagged"] == 3
    assert summary["routed_to_review"] >= 1

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    q_surd = conn.execute("SELECT * FROM questions WHERE id = 'Q_test_surd01';").fetchone()
    q_excel = conn.execute("SELECT * FROM questions WHERE id = 'Q_test_excel1';").fetchone()
    review_rows = conn.execute("SELECT * FROM tag_review_queue WHERE question_id = 'Q_test_ambig1';").fetchall()
    conn.close()

    assert q_surd["indicator_code"] == "B9.1.1.2.2"
    assert q_surd["confidence"] >= 0.75
    assert q_excel["indicator_code"] == "B9.2.3.1.1"
    assert q_excel["confidence"] >= 0.75
    assert len(review_rows) == 1
    assert review_rows[0]["reason"] == "low_confidence"

    # Verify hybrid semantic + FTS5 search
    hits = tagger.semantic_search("rationalise surd denominator", subject="Mathematics", limit=2)
    assert len(hits) == 2
    assert hits[0]["id"] == "Q_test_surd01"
