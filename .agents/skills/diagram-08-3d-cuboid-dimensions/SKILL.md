---
name: diagram-08-3d-cuboid-dimensions
description: Instructions, geometric specs, and TikZ code to draw authentic BECE 3D cuboids and rectangular prisms with perspective projection and dimension callouts.
---

# Diagram 08: 3D Cuboid / Rectangular Prism with Dimensions

## Provenance
- **Exam Context:** BECE Mathematics 2002 Paper 1, Question 27
- **Question ID:** `Q_f1f3dd2a90d3`
- **Topic:** Geometry and Measurement / 3D Solids, Surface Area and Volume
- **Curriculum Indicator:** B8.3.1.3 / B9.3.1.3 (Calculate surface area and volume of prisms and cuboids)

## Geometric & Visual Specification
- **Oblique Cavalier / Cabinet Projection:**
  - Front rectangular face $PQRV$ parallel to the projection plane:
    - $P(0, 0)$ [bottom-left], $Q(4.4, 0)$ [bottom-right], $R(4.4, 2.9)$ [top-right], $V(0, 2.9)$ [top-left].
  - Rear rectangular face $OTSU$ translated by depth vector $(\Delta x, \Delta y) = (1.9, 1.3)$:
    - $O(1.9, 1.3)$ [bottom-left], $T(6.3, 1.3)$ [bottom-right], $S(6.3, 4.2)$ [top-right], $U(1.9, 4.2)$ [top-left].
  - 4 depth connecting edges: $PO$, $QT$, $RS$, $VU$.
  - Line style: All 12 edges solid $1.4\,\text{pt}$ (wireframe perspective format typical of BECE objective exams).
- **Dimension Labels:**
  - Length along front base $PQ$: **$x$ cm** centered at $(2.2, -0.35)$.
  - Depth along bottom-right edge $QT$: **$y$ cm** centered at $(5.35, 0.65)$.
  - Height along left front edge $PV$: **$z$ cm** centered at $(-0.4, 1.45)$.
- **Vertex Labels:**
  - **P**, **Q**, **R**, **V**, **O**, **T**, **S**, **U** in bold sans-serif (`\huge\sffamily\bfseries`) with optimal clearance from vertex junctions.

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** 3D oblique projections require rigid parallel translation of 2D faces. TikZ coordinates make projecting front-to-back faces with exact vector offsets $(\Delta x, \Delta y)$ straightforward and mathematically exact.

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=15pt]{standalone}
\usepackage{amsmath,amssymb}

\begin{document}
\begin{tikzpicture}[scale=1.2]
    % Front face coordinates
    \coordinate (P) at (0, 0);
    \coordinate (Q) at (4.4, 0);
    \coordinate (R) at (4.4, 2.9);
    \coordinate (V) at (0, 2.9);
    
    % Rear face coordinates (oblique offset: dx=1.9, dy=1.3)
    \coordinate (O) at (1.9, 1.3);
    \coordinate (T) at (6.3, 1.3);
    \coordinate (S) at (6.3, 4.2);
    \coordinate (U) at (1.9, 4.2);
    
    % Draw front and back faces
    \draw[line width=1.4pt] (P) -- (Q) -- (R) -- (V) -- cycle;
    \draw[line width=1.4pt] (O) -- (T) -- (S) -- (U) -- cycle;
    
    % Draw connecting depth edges
    \draw[line width=1.4pt] (P) -- (O);
    \draw[line width=1.4pt] (Q) -- (T);
    \draw[line width=1.4pt] (R) -- (S);
    \draw[line width=1.4pt] (V) -- (U);
    
    % Vertices labels in bold sans-serif
    \node[below=4pt, font=\huge\sffamily\bfseries] at (P) {P};
    \node[below=4pt, font=\huge\sffamily\bfseries] at (Q) {Q};
    \node[above=4pt, font=\huge\sffamily\bfseries] at (R) {R};
    \node[above left=3pt, font=\huge\sffamily\bfseries] at (V) {V};
    
    \node[above right=3pt, font=\huge\sffamily\bfseries] at (O) {O};
    \node[right=4pt, font=\huge\sffamily\bfseries] at (T) {T};
    \node[above=4pt, font=\huge\sffamily\bfseries] at (S) {S};
    \node[above=4pt, font=\huge\sffamily\bfseries] at (U) {U};
    
    % Dimension callouts
    \node[below=4pt, font=\Large\sffamily\bfseries] at (2.2, 0) {\textit{x} cm};
    \node[below right=2pt, font=\Large\sffamily\bfseries] at (5.35, 0.65) {\textit{y} cm};
    \node[left=5pt, font=\Large\sffamily\bfseries] at (0, 1.45) {\textit{z} cm};
    
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other 3D prism problems:
1. **Hidden/Dashed Edges:** Change hidden back edges ($PO$, $OT$, $OU$) to `\draw[dashed, line width=1.2pt]` to represent opaque solid rendering.
2. **Cube Specialization:** Set width $w = 3.5$, height $h = 3.5$, depth offset $(1.5, 1.5)$, and single dimension label $s\text{ cm}$.
3. **Face Shading:** Use `\fill[fill=gray!20, draw=black]` on a target face like $PQRV$ to highlight the specific face under question.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] Front face and rear face are identical congruent rectangles.
- [x] All 4 depth edges are parallel with identical length and angle.
- [x] Vertex letters are large, distinct, and positioned outside line crossings.
- [x] Dimensions $x\text{ cm}, y\text{ cm}, z\text{ cm}$ are aligned along the primary axes.
- [x] Crisp 300 DPI PNG with zero jaggedness.
- [x] Visual inspection gate passed (300 DPI PNG reviewed and verified critically)


## Mandatory Visual Verification Gate (Strict Agent Protocol)
Before inserting this diagram into any exam paper, worksheet, or document:
1. **Compile & Rasterize to PNG Only (Strictly No Diagram PDFs or SVGs):** Diagrams must exist and be retained ONLY as `.png` (and source `.tex`). Never output, store, commit, or convert diagrams to `.pdf` or `.svg` files (high-DPI concerns do not justify keeping SVGs; 300 DPI PNG is the sole target). When compiling standalone `.tex` via `pdflatex`, rasterize immediately to 300 DPI `.png` (e.g. using PyMuPDF / `page.get_pixmap(dpi=300)`) and immediately delete any intermediate `.pdf`, `.svg`, or temporary `.aux`/`.log` build artifacts. Diagram assets must exist strictly as `.png`.
2. **Critical Visual Inspection:** The agent MUST explicitly load and view the rendered PNG image using visual tools (such as 
`read_file`). Critically analyze for:
   - Text or numerical label overlaps with geometric lines, arcs, or dimension callouts.
   - Proper clearance and breathing space around vertex letters and angle symbols.
   - Orthogonality and alignment of ticks, arrows, and hatching lines.
3. **Iterate Until Flawless:** If any visual collision or imperfection is detected, adjust the TikZ coordinates or node anchors, re-render to PNG, and re-inspect until perfection is reached.
4. **Insertion Approval:** Only embed the diagram into the mock paper or teaching module after the PNG passes this critical visual inspection.
