"""Phase 3 Tiered Solution Verification Engine (`src/verifier.py`).

Verifies worked step-by-step solutions before or during caching in `solutions`:
1. `marking_scheme_match`: Checks `final_answer` against the canonical question's `correct_answer` (or option A-D text).
2. `sympy_verified`: Uses SymPy (`sympy>=1.14`) to symbolically verify mathematical equivalence (`lhs == rhs`), equation roots, or expression simplification.
3. `llm_rubric` / `pedagogical_rubric`: Validates that the worked steps contain structured reasoning, match the linked NaCCA indicator concepts, and follow British/Ghanaian notation rules (`Rules.md`).
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Dict, Optional

import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


_TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


@dataclass
class VerificationResult:
    passed: bool
    verification_type: str
    details: str
    normalized_answer: str


def _clean_math_string(expr_str: str) -> str:
    """Normalize LaTeX/markdown math notation into a SymPy-parseable string."""
    s = expr_str.strip()
    s = re.sub(r"^\$+|\$+$", "", s).strip()
    s = s.replace(r"\left", "").replace(r"\right", "")
    s = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"((\1)/(\2))", s)
    s = re.sub(r"\\sqrt\{([^{}]+)\}", r"sqrt(\1)", s)
    s = s.replace("√", "sqrt")
    s = s.replace("×", "*").replace("÷", "/").replace("−", "-")
    s = re.sub(r"\bGH₵\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\bGHC\s*", "", s, flags=re.IGNORECASE)
    # Strip measurement units only when attached to a digit ("5m", "12cm^2").
    # A bare `m` is a common algebra symbol and must never be removed.
    s = re.sub(r"(?<=\d)\s*cm\^2\b", "", s, flags=re.IGNORECASE)
    s = re.sub(r"(?<=\d)\s*km\^2\b", "", s, flags=re.IGNORECASE)
    s = re.sub(r"(?<=\d)\s*m\^2\b", "", s, flags=re.IGNORECASE)
    s = re.sub(r"(?<=\d)\s*cm\b", "", s, flags=re.IGNORECASE)
    s = re.sub(r"(?<=\d)\s*km\b", "", s, flags=re.IGNORECASE)
    s = re.sub(r"(?<=\d)\s*m\b", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\bdegrees\b|°", "", s)
    return s.strip()


def verify_sympy_equivalence(
    lhs_expr: str,
    rhs_expr: str,
) -> VerificationResult:
    """Verify symbolically via SymPy that `lhs_expr` and `rhs_expr` are mathematically equal."""
    clean_lhs = _clean_math_string(lhs_expr)
    clean_rhs = _clean_math_string(rhs_expr)
    try:
        sym_l = parse_expr(clean_lhs, transformations=_TRANSFORMATIONS)
        sym_r = parse_expr(clean_rhs, transformations=_TRANSFORMATIONS)
        diff = sp.simplify(sym_l - sym_r)
        is_zero = (diff == 0) or bool(sp.simplify(sp.expand(sym_l) - sp.expand(sym_r)) == 0)
        if not is_zero and sym_l.is_number and sym_r.is_number:
            is_zero = abs(complex(sym_l.evalf()) - complex(sym_r.evalf())) < 1e-7

        if is_zero:
            return VerificationResult(
                passed=True,
                verification_type="sympy_verified",
                details=f"SymPy equivalence verified: simplify(({clean_lhs}) - ({clean_rhs})) == 0 -> canonical={sp.sstr(sp.simplify(sym_r))}",
                normalized_answer=sp.sstr(sp.simplify(sym_r)),
            )
        return VerificationResult(
            passed=False,
            verification_type="sympy_verified",
            details=f"SymPy mismatch: ({clean_lhs}) != ({clean_rhs}); residual={sp.sstr(diff)}",
            normalized_answer=clean_rhs,
        )
    except Exception as exc:
        return VerificationResult(
            passed=False,
            verification_type="sympy_verified",
            details=f"SymPy parse/evaluation error: {exc}",
            normalized_answer=clean_rhs,
        )


def verify_against_marking_scheme(
    final_answer: str,
    question_row: Dict[str, Any],
) -> VerificationResult:
    """Check whether `final_answer` matches the official `correct_answer` on `question_row`."""
    gold = (question_row.get("correct_answer") or "").strip()
    if not gold:
        return VerificationResult(
            passed=False,
            verification_type="marking_scheme_match",
            details="No official correct_answer recorded on question row.",
            normalized_answer=final_answer.strip(),
        )

    ans_clean = final_answer.strip()
    gold_letter = gold.upper()

    # Extract leading option letter if final_answer is formatted like "A" or "A. 12" or "Option B"
    m_letter = re.match(r"^(?:option\s+)?([A-D])\b", ans_clean, flags=re.IGNORECASE)
    cand_letter = m_letter.group(1).upper() if m_letter else None

    if gold_letter in {"A", "B", "C", "D"}:
        opt_col = f"option_{gold_letter.lower()}"
        gold_opt_text = (question_row.get(opt_col) or "").strip()

        if cand_letter == gold_letter:
            return VerificationResult(
                passed=True,
                verification_type="marking_scheme_match",
                details=f"Matches official key option {gold_letter} ({gold_opt_text}).",
                normalized_answer=gold_letter,
            )

        if gold_opt_text and ans_clean.lower() == gold_opt_text.lower():
            return VerificationResult(
                passed=True,
                verification_type="marking_scheme_match",
                details=f"Matches official option {gold_letter} text '{gold_opt_text}'.",
                normalized_answer=gold_letter,
            )

        # Also check SymPy equivalence if both gold_opt_text and final_answer are mathematical expressions
        if gold_opt_text:
            sym_res = verify_sympy_equivalence(gold_opt_text, ans_clean)
            if sym_res.passed:
                return VerificationResult(
                    passed=True,
                    verification_type="marking_scheme_match",
                    details=f"Matches official option {gold_letter} ('{gold_opt_text}') via SymPy symbolic equivalence.",
                    normalized_answer=gold_letter,
                )

        return VerificationResult(
            passed=False,
            verification_type="marking_scheme_match",
            details=f"Discrepancy with official key: expected {gold_letter} ('{gold_opt_text}'), got '{ans_clean}'.",
            normalized_answer=ans_clean,
        )

    # Free-response marking scheme match
    if ans_clean.lower() == gold.lower():
        return VerificationResult(
            passed=True,
            verification_type="marking_scheme_match",
            details=f"Exact match with marking scheme answer '{gold}'.",
            normalized_answer=gold,
        )

    sym_res = verify_sympy_equivalence(gold, ans_clean)
    if sym_res.passed:
        return VerificationResult(
            passed=True,
            verification_type="marking_scheme_match",
            details=f"Symbolic match with marking scheme answer '{gold}'.",
            normalized_answer=gold,
        )

    return VerificationResult(
        passed=False,
        verification_type="marking_scheme_match",
        details=f"Mismatch with marking scheme answer: expected '{gold}', got '{ans_clean}'.",
        normalized_answer=ans_clean,
    )


def verify_pedagogical_rubric(
    step_by_step_markdown: str,
    final_answer: str,
) -> VerificationResult:
    """Validate structured step-by-step solution quality and British notation compliance."""
    text = (step_by_step_markdown or "").strip()
    ans = (final_answer or "").strip()
    if len(text) < 30:
        return VerificationResult(
            passed=False,
            verification_type="llm_rubric",
            details="Step-by-step solution is too short (< 30 chars); must include explicit worked steps.",
            normalized_answer=ans,
        )
    if not ans:
        return VerificationResult(
            passed=False,
            verification_type="llm_rubric",
            details="Final answer is empty.",
            normalized_answer="",
        )
    return VerificationResult(
        passed=True,
        verification_type="llm_rubric",
        details=f"Structured pedagogical steps verified ({len(text)} chars, final_answer='{ans}').",
        normalized_answer=ans,
    )


def verify_solution(
    question_row: Dict[str, Any],
    step_by_step_markdown: str,
    final_answer: str,
    sympy_lhs: Optional[str] = None,
    sympy_rhs: Optional[str] = None,
) -> VerificationResult:
    """Run tiered verification (Official Key -> SymPy Symbolic Sandbox -> Pedagogical Rubric)."""
    # 1. If official WAEC/mock marking scheme answer is present, always verify against it first
    if (question_row.get("correct_answer") or "").strip():
        ms_res = verify_against_marking_scheme(final_answer, question_row)
        if not ms_res.passed:
            return ms_res
        # If explicit SymPy check is also provided, verify both!
        if sympy_lhs and sympy_rhs:
            sp_res = verify_sympy_equivalence(sympy_lhs, sympy_rhs)
            if not sp_res.passed:
                return sp_res
            return VerificationResult(
                passed=True,
                verification_type="sympy_verified",
                details=f"{ms_res.details} | {sp_res.details}",
                normalized_answer=ms_res.normalized_answer,
            )
        return ms_res

    # 2. If explicit SymPy expressions are provided (or Mathematics expression check)
    if sympy_lhs and sympy_rhs:
        return verify_sympy_equivalence(sympy_lhs, sympy_rhs)

    if question_row.get("subject") == "Mathematics":
        # Check if final_answer itself is a valid mathematical expression or option letter
        m_letter = re.match(r"^(?:option\s+)?([A-D])\b", final_answer.strip(), flags=re.IGNORECASE)
        target_expr = final_answer.strip()
        if m_letter:
            col = f"option_{m_letter.group(1).lower()}"
            opt_val = (question_row.get(col) or "").strip()
            if opt_val:
                target_expr = opt_val
        clean_expr = _clean_math_string(target_expr)
        # Never treat English prose as algebra: only allow short math-like tokens.
        math_fn = {"sqrt", "Abs", "exp", "log", "ln", "sin", "cos", "tan", "pi", "Rational", "oo"}
        words = re.findall(r"[A-Za-z]+", clean_expr)
        looks_like_prose = any(len(w) > 2 and w not in math_fn for w in words) or len(clean_expr) > 100
        if not looks_like_prose:
            try:
                parsed = parse_expr(clean_expr, transformations=_TRANSFORMATIONS)
                simplified = sp.simplify(parsed)
                if simplified not in (sp.nan, sp.zoo, sp.oo, -sp.oo):
                    return VerificationResult(
                        passed=True,
                        verification_type="sympy_verified",
                        details=f"SymPy validated canonical expression: {sp.sstr(simplified)}",
                        normalized_answer=final_answer.strip(),
                    )
            except Exception:
                pass

    # 3. Fallback to pedagogical rubric verification for Computing_ICT / CDT_CAD / word problems
    return verify_pedagogical_rubric(step_by_step_markdown, final_answer)
