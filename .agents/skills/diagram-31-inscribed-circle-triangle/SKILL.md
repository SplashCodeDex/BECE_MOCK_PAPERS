---
name: diagram-31-inscribed-circle-triangle
description: Replicate the authentic BECE construction diagram for the inscribed circle (incircle and incenter) of a triangle using TikZ.
---

# Diagram 31: Construction of the Inscribed Circle of a Triangle

## 1. Provenance & Curriculum Context
- **Curriculum Indicator:** `B9.3.1.2.1` (Draw inscribed and circumscribed circles for triangles under given conditions)
- **Topic:** Shape and Space / Geometric Constructions
- **Mathematical Significance:** Demonstrates Euclidean construction of the incircle and incenter $I$ of $\triangle ABC$:
  1. Bisect two interior angles ($\angle A$ and $\angle B$) using compass arcs.
  2. The intersection of the two angle bisectors locates the incenter $I$.
  3. Drop a perpendicular line from $I$ to base $AB$ to establish the inradius $r$.
  4. Draw the circle centered at $I$ with radius $r$, tangent to all three triangle sides.

---

## 2. Geometric Specifications & Coordinates
- **Triangle Vertices:** $A(0, 0)$, $B(6.0, 0)$, $C(2.0, 4.0)$.
- **Incenter $I(x_I, y_I)$:**
  - By barycentric side weighting: $x_I \approx 2.408\,\text{cm}$, $y_I \approx 1.488\,\text{cm}$.
- **Inradius $r$:** $r = \frac{\text{Area}}{\text{semiperimeter}} = \frac{12}{8.065} \approx 1.488\,\text{cm}$.
- **Incircle:** Circle centered at $I(2.408, 1.488)$ with radius $r = 1.488\,\text{cm}$, touching base $AB$ tangentially at $(2.408, 0)$.
- **Angle Bisectors:** Dashed rays passing from $A$ through $I$ and from $B$ through $I$.
- **Perpendicular Inradius:** Dashed vertical drop from $I$ to $(2.408, 0)$ with right-angle indicator $(0.25 \times 0.25\,\text{cm})$ and label $r$.
- **Clearance:** Incenter label $I$ positioned `above=8pt` in the open angular wedge.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Guarantees exact tangency between the incircle and all three linear segments ($AB$, $BC$, $CA$) through analytical incenter geometry, avoiding visual overlap or gaps.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]
  % Vertices of triangle ABC
  \coordinate (A) at (0, 0);
  \coordinate (B) at (6, 0);
  \coordinate (C) at (2, 4);

  % Calculated incenter and inradius:
  \coordinate (I) at (2.408, 1.488);
  \def\rIn{1.488}

  % Triangle ABC
  \draw[very thick] (A) -- (B) -- (C) -- cycle;

  % Vertices
  \filldraw[black] (A) circle (2pt) node[below left=3pt, font=\large\bfseries] {$A$};
  \filldraw[black] (B) circle (2pt) node[below right=3pt, font=\large\bfseries] {$B$};
  \filldraw[black] (C) circle (2pt) node[above=4pt, font=\large\bfseries] {$C$};

  % Inscribed circle
  \draw[very thick] (I) circle (\rIn);
  \filldraw[black] (I) circle (2pt);
  \node[above=8pt, font=\normalsize\bfseries] at (I) {$I$};

  % Dashed angle bisector lines through incenter I
  \draw[thick, dashed] (A) -- ($(A)!1.45!(I)$);
  \draw[thick] (0.9, 0) arc (0:63.4:0.9);

  \draw[thick, dashed] (B) -- ($(B)!1.35!(I)$);
  \draw[thick] ($(B) + (180:1.0)$) arc (180:135:1.0);

  % Inradius drop to base AB
  \coordinate (D) at (2.408, 0);
  \draw[thick, dashed] (I) -- (D) node[midway, left=2pt, font=\small] {$r$};
  \draw[thick] (2.408, 0.25) -- (2.658, 0.25) -- (2.658, 0); % Right angle symbol

\end{tikzpicture}
\end{document}
```

---

## Mandatory Visual Verification Gate (Strict Agent Protocol)
Before inserting this diagram into any exam paper, worksheet, or document:
1. **Compile & Rasterize to PNG Only (Strictly No Diagram PDFs or SVGs):** Diagrams must exist and be retained ONLY as `.png` (and source `.tex`). Never output, store, commit, or convert diagrams to `.pdf` or `.svg` files (high-DPI concerns do not justify keeping SVGs; 300 DPI PNG is the sole target). When compiling standalone `.tex` via `pdflatex`, rasterize immediately to 300 DPI `.png` (e.g. using PyMuPDF / `page.get_pixmap(dpi=300)`) and immediately delete any intermediate `.pdf`, `.svg`, or temporary `.aux`/`.log` build artifacts. Diagram assets must exist strictly as `.png`.
2. **Critical Visual Inspection:** The agent MUST explicitly load and view the rendered PNG image using visual tools (such as `read_file`). Critically analyze for:
   - Text or numerical label overlaps with geometric lines, arcs, or dimension callouts.
   - Proper clearance and breathing space around vertex letters and angle symbols.
   - Orthogonality and alignment of ticks, arrows, and hatching lines.
3. **Iterate Until Flawless:** If any visual collision or imperfection is detected, adjust the TikZ coordinates or node anchors, re-render to PNG, and re-inspect until perfection is reached.
4. **Insertion Approval:** Only embed the diagram into the mock paper or teaching module after the PNG passes this critical visual inspection.

## 5. Agent Replication Guide
1. Define triangle vertices $A, B, C$ and calculate side lengths $a, b, c$.
2. Compute incenter coordinates $I = \frac{aA + bB + cC}{a+b+c}$ and inradius $r = \frac{\text{Area}}{s}$.
3. Draw triangle, angle bisector lines through $I$, and incircle.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

---

## 6. Verification & Quality Checklist
- [x] Incircle is exactly tangent to all three sides of $\triangle ABC$.
- [x] Incenter $I$ lies precisely at the intersection of the angle bisectors.
- [x] Inradius line $r$ meets base $AB$ perpendicularly with square indicator.
- [x] Incenter label $I$ has complete clearance within the upper wedge.
- [x] Visual inspection gate passed (300 DPI PNG reviewed and verified critically).
