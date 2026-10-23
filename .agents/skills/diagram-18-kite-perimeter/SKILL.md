---
name: diagram-18-kite-perimeter
description: Instructions, geometric specs, and TikZ code to draw authentic BECE geometric kites with sloped edge dimension callouts and scale notices.
---

# Diagram 18: Geometric Kite with Sloped Edge Dimension Labels

## Provenance
- **Exam Context:** BECE Mathematics 2003 Paper 1, Question 14
- **Question ID:** `Q_db9284ece8ab`
- **Topic:** Geometry and Measurement / Perimeter of Quadrilaterals (Kites)
- **Curriculum Indicator:** B7.3.1.3 / B8.3.1.3 (Identify quadrilateral properties and compute perimeter of kites)

## Geometric & Visual Specification
- **Kite Vertices:**
  - Left blunt vertex: $(-2.6, 0)$.
  - Top vertex: $(-0.6, 1.8)$.
  - Bottom vertex: $(-0.6, -1.8)$.
  - Right acute tail vertex: $(4.4, 0)$.
  - Line of symmetry along $y = 0$.
- **Side Congruence Properties:**
  - Top-left edge and bottom-left edge are congruent: length $16\,\text{cm}$.
  - Top-right edge and bottom-right edge are congruent: length $22\,\text{cm}$.
  - Perimeter $= 2(16 + 22) = 76\,\text{cm}$.
- **Sloped Dimension Callouts:**
  - Top-left edge: Label **16 cm** sloped at $+42^\circ$ directly parallel to the segment with $5\,\text{pt}$ clearance.
  - Top-right edge: Label **22 cm** sloped at $-19.8^\circ$ directly parallel to the segment with $5\,\text{pt}$ clearance.
- **Subtitle:**
  - **NOT DRAWN TO SCALE** in bold sans-serif (`\large\sffamily\bfseries`) centered beneath the lower apex at $(0.9, -1.8 - 0.5)$.

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** Embedding `node[sloped, above=...]` directly within the TikZ `\draw` path computes the tangent orientation angle automatically, ensuring labels remain strictly parallel to polygon edges without manual rotation angles.

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=15pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc}

\begin{document}
\begin{tikzpicture}[scale=1.2]
    % Kite vertices
    \coordinate (Left) at (-2.6, 0);
    \coordinate (Top) at (-0.6, 1.8);
    \coordinate (Bottom) at (-0.6, -1.8);
    \coordinate (Right) at (4.4, 0);
    
    % Draw kite perimeter with sloped labels embedded in the draw path
    \draw[line width=1.4pt] 
        (Left) -- node[above=5pt, font=\Large\sffamily\bfseries, sloped] {16 cm} 
        (Top) -- node[above=5pt, font=\Large\sffamily\bfseries, sloped] {22 cm} 
        (Right) -- (Bottom) -- cycle;
    
    % Subtitle
    \node[below=14pt, font=\large\sffamily\bfseries] at (0.9, -1.8) {NOT DRAWN TO SCALE};
    
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other quadrilateral problems:
1. **Rhombus Specialization:** Set left and right vertices equidistant from the vertical axis (e.g. $(-2.5, 0)$ and $(2.5, 0)$) so all four sides have equal length $s$.
2. **Diagonals Addition:** Draw dashed lines connecting `(Left) -- (Right)` and `(Top) -- (Bottom)` and add a right-angle square marker at the intersection $(-0.6, 0)$.
3. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] Sloped labels are strictly parallel to their respective edges.
- [x] Labels have consistent clearance above lines with zero overlapping strokes.
- [x] Horizontal axis of symmetry $y = 0$ is conserved.
- [x] Subtitle is centered cleanly beneath the figure.
- [x] Crisp 300 DPI PNG output.
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
