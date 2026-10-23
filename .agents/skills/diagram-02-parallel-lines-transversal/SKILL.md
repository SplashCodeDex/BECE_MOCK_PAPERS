---
name: diagram-02-parallel-lines-transversal
description: Instructions, geometric specs, and TikZ code to draw authentic BECE parallel lines with transversal, angle arcs, and parallel indicator arrows.
---

# Diagram 02: Parallel Lines with Transversal (Alternate & Interior Angles)

## Provenance
- **Exam Context:** BECE Mathematics 1996 Paper 1, Question 37
- **Question ID:** `Q_204ab089e1d4`
- **Topic:** Geometry and Measurement / Angles on Parallel Lines
- **Curriculum Indicator:** B8.3.1.1 / B9.3.1.1 (Calculate unknown angles using parallel line angle relationships)

## Geometric & Visual Specification
- **Parallel Rails ($LM \parallel PQ$):**
  - Two horizontal lines spanning from $x = -3.4$ to $x = 3.4$ separated by vertical gap $y = 2.3$.
  - Endpoints labeled in bold sans-serif: **L**, **M** on top, **P**, **Q** on bottom.
  - Mid-line rightward solid arrowheads (`Latex` arrow style) indicating parallelism.
- **Transversal Line:**
  - Slanted line at angle $\theta = 64^\circ$.
  - Intersection points: bottom at $(0, 0)$, top at $(\xtop, \ytop) \approx (1.12, 2.3)$.
  - Extends past both rails by $1.3\,\text{units}$ along the slope.
- **Angles & Labels:**
  - $148^\circ$ arc: Obtuse angle at bottom intersection between negative x-axis ($180^\circ$) and transversal ($\theta = 64^\circ$), radius $0.85\,\text{cm}$.
  - $u$ arc: Acute angle at bottom intersection between positive x-axis ($0^\circ$) and transversal ($\theta = 64^\circ$), radius $0.50\,\text{cm}$.
  - $v$ arc: Alternate interior angle at top intersection, subtended between top rail going left ($180^\circ$) and transversal going downward ($180^\circ + \theta = 244^\circ$), radius $0.60\,\text{cm}$.

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** TikZ enables trigonometric calculations (`\pgfmathsetmacro`), coordinate math via `calc` library (`$(Ibot) + (\ang:0.85)$`), precise arc definitions, and consistent LaTeX math symbols ($148^\circ, u, v$).

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{arrows.meta,calc}

\begin{document}
\begin{tikzpicture}[scale=1.2]
    \pgfmathsetmacro{\ang}{64}
    \pgfmathsetmacro{\ytop}{2.3}
    \pgfmathsetmacro{\xtop}{\ytop / tan(\ang)}
    
    \coordinate (Ibot) at (0, 0);
    \coordinate (Itop) at (\xtop, \ytop);
    
    % Horizontal parallel lines
    \draw[thick] (-3.4, \ytop) node[left=3pt, font=\large\sffamily\bfseries] {L} -- (3.4, \ytop) node[right=3pt, font=\large\sffamily\bfseries] {M};
    \draw[thick] (-3.4, 0) node[left=3pt, font=\large\sffamily\bfseries] {P} -- (3.4, 0) node[right=3pt, font=\large\sffamily\bfseries] {Q};
    
    % Parallel indicator arrows
    \draw[-{Latex[length=3.2mm, width=2.2mm]}] (1.7, \ytop) -- (1.95, \ytop);
    \draw[-{Latex[length=3.2mm, width=2.2mm]}] (1.7, 0) -- (1.95, 0);
    
    % Transversal line extending symmetrically
    \draw[thick] ($(Ibot) - ({1.3*cos(\ang)}, {1.3*sin(\ang)})$) -- ($(Itop) + ({1.3*cos(\ang)}, {1.3*sin(\ang)})$);
    
    % Arc for 148 degrees (obtuse angle at Ibot, from ang to 180)
    \draw[semithick] ($(Ibot) + (\ang:0.85)$) arc (\ang:180:0.85);
    \node[font=\bfseries] at (-0.45, 0.32) {$148^\circ$};
    
    % Arc for u (acute angle at Ibot, from 0 to ang)
    \draw[semithick] ($(Ibot) + (0:0.5)$) arc (0:\ang:0.5);
    \node[font=\large\itshape] at (0.32, 0.22) {$u$};
    
    % Arc for v (alternate interior angle under line LM, from 180 to 180+ang = 244)
    \draw[semithick] ($(Itop) + (180:0.6)$) arc (180:{180+\ang}:0.6);
    \node[font=\large\itshape] at ({\xtop - 0.28}, {\ytop - 0.28}) {$v$};
    
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other parallel angle questions:
1. **Corresponding Angles:** Move arc $v$ to the top-right acute sector (from $0^\circ$ to $\ang$).
2. **Consecutive Interior Angles:** Place angle arc on bottom right ($u$) and top right below rail (from $0^\circ$ to $\ang$ or $270^\circ$).
3. **Multiple Transversals:** Add a second slanted line with different base coordinates $(x_2, 0)$ and angle $\beta$.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] Parallel lines strictly horizontal with identical length.
- [x] Parallel arrowheads clearly visible on both lines pointing right.
- [x] Transversal extends well past top and bottom lines.
- [x] Arcs neatly bounded by the intersecting lines with no overshoot or gaps.
- [x] Labels placed cleanly inside or beside arcs without collision.
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
