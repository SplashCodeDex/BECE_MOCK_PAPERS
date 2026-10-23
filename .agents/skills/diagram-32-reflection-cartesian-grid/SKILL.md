---
name: diagram-32-reflection-cartesian-grid
description: Replicate the authentic BECE transformation diagram showing geometric reflection across coordinate axes on a Cartesian grid using TikZ.
---

# Diagram 32: Geometric Reflection in the $x$-axis on a Cartesian Grid

## 1. Provenance & Curriculum Context
- **Curriculum Indicator:** `B7.3.3.1.2` / `B8.3.3.1.2` (Plot points and shapes in a coordinate plane and determine their reflected images across given mirror lines)
- **Topic:** Position and Transformation / Reflection
- **Mathematical Significance:** Demonstrates coordinate reflection of a 2D polygonal shape across the horizontal mirror line ($x$-axis):
  1. The reflection mapping rule maps each point $(x, y) \to (x, -y)$.
  2. Each vertex and its corresponding image vertex lie on a line perpendicular to the mirror line.
  3. The mirror line perpendicularly bisects each connecting line segment ($AA'$, $BB'$, $CC'$).
  4. The object and image are congruent figures ($|\triangle ABC| \cong |\triangle A'B'C'|$) with reversed orientation.

---

## 2. Geometric Specifications & Coordinates
- **Grid Extent:** $[-4.5, 4.5] \times [-4.5, 4.5]$ with $1.0\,\text{cm}$ step size in `gray!25`.
- **Axes:** $x$-axis from $-4.8$ to $4.8$; $y$-axis from $-4.8$ to $4.8$ with double-headed arrows.
- **Tick Labels:** Integer ticks $-4$ to $+4$ with opaque `fill=white` backgrounds to prevent gridline interference.
- **Object $\triangle ABC$ (Quadrant I):**
  - $A(2, 1)$, $B(4, 1)$, $C(2, 3)$ filled with `blue!12`.
- **Image $\triangle A'B'C'$ (Quadrant IV):**
  - $A'(2, -1)$, $B'(4, -1)$, $C'(2, -3)$ filled with `red!12`.
- **Projection Lines:** Dashed vertical segments connecting $A \leftrightarrow A'$, $B \leftrightarrow B'$, $C \leftrightarrow C'$ with right-angle symbols on the $x$-axis.
- **Rule Annotation:** Centered in Quadrant II: $(x, y) \to (x, -y)$.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** PGF/TikZ coordinate arithmetic ensures that grid lines, tick numbers, coordinate points, and perpendicular reflection lines align with pixel-perfect mathematical symmetry.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]
  % Grid
  \draw[step=1cm, gray!25, thin] (-4.5, -4.5) grid (4.5, 4.5);

  % Axes
  \draw[thick, <->] (-4.8, 0) -- (4.8, 0) node[right, font=\normalsize] {$x$};
  \draw[thick, <->] (0, -4.8) -- (0, 4.8) node[above, font=\normalsize] {$y$};

  % Origin
  \node[below left=2pt, font=\small] at (0, 0) {$O$};

  % Integer ticks with opaque backgrounds to prevent line collision
  \foreach \x in {-4,-3,-2,-1,1,2,3,4} {
    \draw[thick] (\x, 0.1) -- (\x, -0.1);
    \node[below=3pt, font=\footnotesize, fill=white, inner sep=1pt] at (\x, -0.1) {$\x$};
  }
  \foreach \y in {-4,-3,-2,-1,1,2,3,4} {
    \draw[thick] (0.1, \y) -- (-0.1, \y);
    \node[left=3pt, font=\footnotesize, fill=white, inner sep=1pt] at (-0.1, \y) {$\y$};
  }

  % Object triangle ABC (Quadrant I)
  \coordinate (A) at (2, 1);
  \coordinate (B) at (4, 1);
  \coordinate (C) at (2, 3);

  % Dashed reflection projection lines across x-axis
  \draw[thick, dashed, blue!70!black] (A) -- (2, -1);
  \draw[thick, dashed, blue!70!black] (B) -- (4, -1);
  \draw[thick, dashed, blue!70!black] (C) -- (2, -3);

  % Triangles
  \draw[very thick, fill=blue!12] (A) -- (B) -- (C) -- cycle;
  \filldraw[black] (A) circle (2pt) node[above left=3pt, font=\small\bfseries] {$A(2,1)$};
  \filldraw[black] (B) circle (2pt) node[right=4pt, font=\small\bfseries] {$B(4,1)$};
  \filldraw[black] (C) circle (2pt) node[above=4pt, font=\small\bfseries] {$C(2,3)$};

  % Reflected image triangle A'B'C' across x-axis (Quadrant IV)
  \coordinate (A1) at (2, -1);
  \coordinate (B1) at (4, -1);
  \coordinate (C1) at (2, -3);

  \draw[very thick, fill=red!12] (A1) -- (B1) -- (C1) -- cycle;
  \filldraw[black] (A1) circle (2pt) node[below left=3pt, font=\small\bfseries] {$A'(2,-1)$};
  \filldraw[black] (B1) circle (2pt) node[right=4pt, font=\small\bfseries] {$B'(4,-1)$};
  \filldraw[black] (C1) circle (2pt) node[below=4pt, font=\small\bfseries] {$C'(2,-3)$};

  % Right angle markers on mirror line
  \draw[thick] (2, 0.25) -- (2.25, 0.25) -- (2.25, 0);
  \draw[thick] (4, 0.25) -- (3.75, 0.25) -- (3.75, 0);

  % Annotations cleanly positioned in Quadrant II & III
  \node[above=4pt, font=\small\bfseries, fill=white, inner sep=2pt] at (-2.5, 3.8) {Object $\triangle ABC$};
  \node[below=4pt, font=\small\bfseries, fill=white, inner sep=2pt] at (-2.5, -3.8) {Image $\triangle A'B'C'$};
  \node[font=\footnotesize\bfseries, fill=white, inner sep=2pt] at (-2.5, 1.5) {Reflection in $x$-axis:};
  \node[font=\footnotesize, fill=white, inner sep=2pt] at (-2.5, 0.8) {$(x, y) \to (x, -y)$};

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
1. Create coordinate grid with opaque tick number boxes (`fill=white`).
2. Plot object vertices $(x_i, y_i)$ and compute image vertices under mirror rule (e.g. $(x_i, -y_i)$ for $x$-axis, $(-x_i, y_i)$ for $y$-axis, or $(y_i, x_i)$ for $y = x$).
3. Draw dashed projection segments with right-angle indicators at mirror line crossings.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

---

## 6. Verification & Quality Checklist
- [x] Grid lines render lightly in background with zero aliasing.
- [x] Axis ticks are unobstructed and cleanly numbered.
- [x] Reflected vertices $A', B', C'$ are symmetric across the $x$-axis.
- [x] Right angle indicators verify orthogonality to the mirror line.
- [x] Visual inspection gate passed (300 DPI PNG reviewed and verified critically).
