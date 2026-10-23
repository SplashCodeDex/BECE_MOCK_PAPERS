---
name: diagram-30-triangle-construction-sss
description: Replicate the authentic BECE compass and straightedge construction diagram for a triangle with given side lengths (SSS) using TikZ.
---

# Diagram 30: Compass and Straightedge Construction of a Triangle (SSS)

## 1. Provenance & Curriculum Context
- **Curriculum Indicator:** `B8.3.1.2.3` / `B9.3.1.2.2` (Construct triangles given three side lengths using ruler and compasses)
- **Topic:** Shape and Space / Geometric Constructions
- **Mathematical Significance:** Demonstrates Euclidean construction of triangle $\triangle ABC$ given three side lengths $a = 4\,\text{cm}$, $b = 5\,\text{cm}$, and $c = 6\,\text{cm}$:
  1. Draw horizontal base segment $AB = c = 6\,\text{cm}$.
  2. With compass opened to radius $b = 5\,\text{cm}$, swing an arc centered at vertex $A$.
  3. With compass opened to radius $a = 4\,\text{cm}$, swing an arc centered at vertex $B$ intersecting the first arc at apex $C$.
  4. Connect $A$ to $C$ and $B$ to $C$ with straight line segments to complete the triangle.

---

## 2. Geometric Specifications & Coordinates
- **Baseline:** Horizontal line segment from $(-0.8, 0)$ to $(6.8, 0)$.
- **Base Vertices:** $A(0, 0)$ and $B(6.0, 0)$ with solid points and labels below.
- **Apex Coordinates $C(x_C, y_C)$:**
  - By the Law of Cosines: $x_C = \frac{b^2 - a^2 + c^2}{2c} = \frac{25 - 16 + 36}{12} = \frac{45}{12} = 3.75\,\text{cm}$.
  - Ordinate: $y_C = \sqrt{b^2 - x_C^2} = \sqrt{25 - 14.0625} = \sqrt{10.9375} \approx 3.307\,\text{cm}$.
- **Construction Arcs:**
  - Arc 1 centered at $A(0, 0)$ with radius $b = 5.0\,\text{cm}$ swept $\angA \pm 9^\circ$ where $\angA = \operatorname{atan2}(3.307, 3.75) \approx 41.4^\circ$.
  - Arc 2 centered at $B(6.0, 0)$ with radius $a = 4.0\,\text{cm}$ swept $\angB \pm 10^\circ$ where $\angB = \operatorname{atan2}(3.307, 3.75 - 6.0) \approx 124.2^\circ$.
- **Dimension Labels:**
  - Base $AB$: `$6\text{ cm}$` centered below midpoint.
  - Side $AC$: `$5\text{ cm}$` positioned `above left=3pt`.
  - Side $BC$: `$4\text{ cm}$` positioned `above right=3pt`.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** The Law of Cosines coordinate math (`\pgfmathsetmacro{\xC}{(\b*\b - \a*\a + \c*\c) / (2*\c)}`) guarantees that both compass arcs and side segments meet at apex $C$ with mathematical precision.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]
  % Side lengths: c = 6.0, b = 5.0, a = 4.0
  \def\c{6.0}
  \def\b{5.0}
  \def\a{4.0}

  % Coordinates
  \coordinate (A) at (0, 0);
  \coordinate (B) at (\c, 0);

  % Apex C: x = 3.75, y = sqrt(25 - 3.75^2) = 3.307
  \pgfmathsetmacro{\xC}{(\b*\b - \a*\a + \c*\c) / (2*\c)}
  \pgfmathsetmacro{\yC}{sqrt(\b*\b - \xC*\xC)}
  \coordinate (C) at (\xC, \yC);

  % Baseline extension
  \draw[thick] (-0.8, 0) -- ({\c + 0.8}, 0);

  % Triangle ABC
  \draw[very thick] (A) -- (B) node[midway, below=5pt, font=\normalsize] {$6\text{ cm}$};
  \draw[very thick] (A) -- (C) node[midway, above left=3pt, font=\normalsize] {$5\text{ cm}$};
  \draw[very thick] (B) -- (C) node[midway, above right=3pt, font=\normalsize] {$4\text{ cm}$};

  % Vertices
  \filldraw[black] (A) circle (2pt) node[below=5pt, font=\large\bfseries] {$A$};
  \filldraw[black] (B) circle (2pt) node[below=5pt, font=\large\bfseries] {$B$};
  \filldraw[black] (C) circle (2pt) node[above=6pt, font=\large\bfseries] {$C$};

  % Construction arc from A (radius b) through C
  \pgfmathsetmacro{\angA}{atan2(\yC, \xC)}
  \draw[thick] ($(A) + ({\angA - 9}:\b)$) arc ({\angA - 9}:{\angA + 9}:\b);

  % Construction arc from B (radius a) through C
  \pgfmathsetmacro{\angB}{atan2(\yC, \xC - \c)}
  \draw[thick] ($(B) + ({\angB - 10}:\a)$) arc ({\angB - 10}:{\angB + 10}:\a);

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
1. Establish base side $AB = c$ along the horizontal line.
2. Calculate apex coordinates using the cosine rule: $x_C = \frac{b^2 - a^2 + c^2}{2c}, y_C = \sqrt{b^2 - x_C^2}$.
3. Draw compass arcs of radius $b$ from $A$ and radius $a$ from $B$ crossing at $C$.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

---

## 6. Verification & Quality Checklist
- [x] Side lengths $c=6, b=5, a=4$ form mathematically accurate triangle proportions.
- [x] Arcs centered at $A$ and $B$ cross precisely at apex $C$.
- [x] Dimension callouts are unobstructed on all three sides.
- [x] Baseline extends past $A$ and $B$ on both sides.
- [x] Visual inspection gate passed (300 DPI PNG reviewed and verified critically).
