---
name: diagram-27-construction-90-degrees
description: Replicate the authentic BECE compass and straightedge construction diagram for a 90-degree angle / perpendicular at a point on a line using TikZ.
---

# Diagram 27: Compass and Straightedge Construction of a $90^\circ$ Angle

## 1. Provenance & Curriculum Context
- **Curriculum Indicator:** `B7.3.1.2.1` / `B8.3.1.2.1` (Construct a line segment perpendicular to another line segment at a given point)
- **Topic:** Shape and Space / Geometric Constructions
- **Mathematical Significance:** Demonstrates Euclidean construction of a right angle ($90^\circ$) at a given point $P$ on a straight line:
  1. Swing a base semicircle of radius $r$ centered at $P(0, 0)$ cutting the baseline at $A(-r, 0)$ and $B(r, 0)$.
  2. With compass opened to radius $R > r$, swing intersecting arcs centered at $A$ and $B$ crossing above $P$ at apex $C$.
  3. Draw the ray from $P$ through $C$ to establish an exact $90^\circ$ perpendicular ray.

---

## 2. Geometric Specifications & Coordinates
- **Baseline:** Horizontal line segment from $(-3.8, 0)$ to $(3.8, 0)$.
- **Given Point $P$:** Marked at origin $(0, 0)$ with solid disc.
- **Base Semicircle:** Radius $r = 2.0\,\text{cm}$, swept from $0^\circ$ to $180^\circ$ connecting $B(2, 0)$ and $A(-2, 0)$.
- **Crossing Arcs:**
  - Radius $R = 3.2\,\text{cm}$.
  - Arc 1 centered at $A(-2, 0)$ swept $\angA \pm 12^\circ$ where $\angA = \operatorname{atan2}(\sqrt{R^2 - r^2}, r) \approx 51.3^\circ$.
  - Arc 2 centered at $B(2, 0)$ swept $(180^\circ - \angA) \pm 12^\circ$.
  - Exact intersection apex: $C(0, \sqrt{R^2 - r^2}) = (0, \sqrt{6.24}) \approx (0, 2.498\,\text{cm})$.
- **Perpendicular Ray:** Directed line segment with arrow from $P(0, 0)$ through $C$ to $(0, 1.3 \times y_C)$.
- **Right Angle Indicator:** Square symbol $(0.35 \times 0.35\,\text{cm})$ in quadrant I at $P$.
- **Labels:** $A, P, B$ positioned below baseline; $C$ positioned `right=8pt` from intersection.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Guarantees trigonometric accuracy via `\pgfmathsetmacro{\yint}{sqrt(\R*\R - \r*\r)}`, ensuring the perpendicular ray aligns with mathematical precision without visual offsets.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]
  % Parameters
  \def\r{2.0}     % Radius of base semicircle from P
  \def\R{3.2}     % Radius of crossing arcs
  
  % Baseline
  \draw[thick] (-3.8, 0) -- (3.8, 0);

  % Given point P on baseline
  \coordinate (P) at (0, 0);
  \filldraw[black] (P) circle (2pt) node[below=5pt, font=\large\bfseries] {$P$};

  % Semicircle centered at P cutting baseline at A and B
  \draw[thick] (\r, 0) arc (0:180:\r);
  
  \coordinate (A) at (-\r, 0);
  \coordinate (B) at (\r, 0);
  \node[below=4pt, font=\normalsize] at (A) {$A$};
  \node[below=4pt, font=\normalsize] at (B) {$B$};

  % Crossing arcs from A and B above P
  \pgfmathsetmacro{\yint}{sqrt(\R*\R - \r*\r)}
  \pgfmathsetmacro{\angA}{atan2(\yint, \r)}
  \pgfmathsetmacro{\angB}{180 - \angA}

  \draw[thick] ($(A) + ({\angA - 12}:\R)$) arc ({\angA - 12}:{\angA + 12}:\R);
  \draw[thick] ($(B) + ({\angB - 12}:\R)$) arc ({\angB - 12}:{\angB + 12}:\R);

  \coordinate (C) at (0, \yint);
  \node[right=8pt, font=\large] at (C) {$C$};

  % Perpendicular ray from P through C
  \draw[very thick, ->] (P) -- (0, {\yint * 1.3});

  % Right angle indicator at P
  \draw[thick] (0, 0.35) -- (0.35, 0.35) -- (0.35, 0);

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
1. Position point $P$ along a horizontal baseline.
2. Draw a base semicircle of radius $r$ centered at $P$.
3. Compute apex coordinates $C(0, \sqrt{R^2 - r^2})$ for crossing radius $R > r$.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

---

## 6. Verification & Quality Checklist
- [x] Semicircle cleanly lands on baseline at points $A$ and $B$.
- [x] Crossing arcs intersect symmetrically along the vertical axis $x = 0$.
- [x] Perpendicular ray passes exactly through apex $C$ with directional arrowhead.
- [x] Square indicator at $P$ confirms $90^\circ$ right angle.
- [x] Visual inspection gate passed (300 DPI PNG reviewed and verified critically).
