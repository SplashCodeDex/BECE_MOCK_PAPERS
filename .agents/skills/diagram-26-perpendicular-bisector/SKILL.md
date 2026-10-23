---
name: diagram-26-perpendicular-bisector
description: Replicate the authentic BECE compass and straightedge construction diagram for the perpendicular bisector of a line segment using TikZ.
---

# Diagram 26: Compass and Straightedge Construction of Perpendicular Bisector

## 1. Provenance & Curriculum Context
- **Curriculum Indicator:** `B7.3.1.2.2` (Construct the perpendicular bisector of a line segment) / `B8.3.1.2.1`
- **Topic:** Shape and Space / Geometric Constructions
- **Mathematical Significance:** Demonstrates Euclidean construction of the locus of points equidistant from two fixed points $A$ and $B$:
  1. Swing arcs of radius $R > \frac{1}{2}|AB|$ centered at endpoints $A$ and $B$.
  2. The pairs of arcs cross above and below the segment at points $P$ and $Q$.
  3. The straight line $PQ$ perpendicularly bisects $AB$ at midpoint $M$, establishing $AM = MB$ and $\angle PMA = 90^\circ$.

---

## 2. Geometric Specifications & Coordinates
- **Line Segment $AB$:** Horizontal baseline from $A(-3, 0)$ to $B(3, 0)$, extended slightly to $(-3.8, 0)$ and $(3.8, 0)$.
- **Midpoint $M$:** $(0, 0)$ with right-angle indicator $(0.35 \times 0.35\,\text{cm})$.
- **Congruence Ticks:** Centered at $x = -1.5$ and $x = +1.5$, spanning $y = -0.18$ to $y = +0.18$.
- **Compass Arcs:**
  - Radius $R = 4.0\,\text{cm}$.
  - Top crossing: centered at $A(-3, 0)$ swept $33^\circ$ to $50^\circ$; centered at $B(3, 0)$ swept $130^\circ$ to $147^\circ$.
  - Bottom crossing: centered at $A(-3, 0)$ swept $-50^\circ$ to $-33^\circ$; centered at $B(3, 0)$ swept $-147^\circ$ to $-130^\circ$.
  - Exact intersection ordinate: $y = \pm\sqrt{R^2 - 3^2} = \pm\sqrt{7} \approx \pm 2.646\,\text{cm}$.
- **Perpendicular Bisector Line:** Vertical dashed line through $x = 0$ spanning $y = -1.22 \times \sqrt{7}$ to $y = 1.22 \times \sqrt{7}$.
- **Labels:** $P$ and $Q$ positioned `right=10pt` from intersections for clear breathing space.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Guarantees coordinate math precision via `\pgfmathsetmacro{\yint}{sqrt(\R*\R - 3*3)}`, ensuring dashed bisector passes precisely through arc cross points with zero human drawing error.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]
  % Coordinates of segment AB
  \coordinate (A) at (-3, 0);
  \coordinate (B) at (3, 0);
  \coordinate (M) at (0, 0);
  
  \def\R{4.0} % Compass radius > half of AB (3.0)

  % Main line segment AB
  \draw[very thick] (-3.8, 0) -- (3.8, 0);
  \filldraw[black] (A) circle (2pt) node[below=5pt, font=\large\bfseries] {$A$};
  \filldraw[black] (B) circle (2pt) node[below=5pt, font=\large\bfseries] {$B$};

  % Equal segment ticks on AM and MB
  \draw[thick] (-1.5, -0.18) -- (-1.5, 0.18);
  \draw[thick] (1.5, -0.18) -- (1.5, 0.18);

  % Top intersection arcs
  \draw[thick] ($(A) + (33:\R)$) arc (33:50:\R);
  \draw[thick] ($(B) + (130:\R)$) arc (130:147:\R);

  % Bottom intersection arcs
  \draw[thick] ($(A) + (-50:\R)$) arc (-50:-33:\R);
  \draw[thick] ($(B) + (-147:\R)$) arc (-147:-130:\R);

  % Perpendicular bisector line
  \pgfmathsetmacro{\yint}{sqrt(\R*\R - 3*3)}
  \draw[very thick, dashed] (0, -\yint*1.22) -- (0, \yint*1.22);

  % Right angle indicator at midpoint M
  \draw[thick] (0, 0.35) -- (0.35, 0.35) -- (0.35, 0);
  \node[below left=4pt, font=\small] at (M) {$M$};

  % Labels for intersection points
  \coordinate (P) at (0, \yint);
  \coordinate (Q) at (0, -\yint);
  \node[right=10pt, font=\large] at (P) {$P$};
  \node[right=10pt, font=\large] at (Q) {$Q$};

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
1. Select segment length $2a$ (e.g. $6\,\text{cm}$) and compass radius $R > a$ (e.g. $4\,\text{cm}$).
2. Compute intersection angles via $\theta = \pm \arcsin(a / R)$.
3. Sweep symmetric arc cuts across intersection point $P(0, \sqrt{R^2 - a^2})$ and $Q(0, -\sqrt{R^2 - a^2})$.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

---

## 6. Verification & Quality Checklist
- [x] Top and bottom crossing arcs intersect symmetrically at $x = 0$.
- [x] Dashed perpendicular bisector passes precisely through points $P$, $M$, and $Q$.
- [x] Right angle symbol at midpoint $M$ shows strict $90^\circ$ orthogonality.
- [x] Congruence tick marks verify $AM = MB$.
- [x] Visual inspection gate passed (300 DPI PNG reviewed and verified critically).
