---
name: diagram-06-bearing-three-figure
description: Instructions, geometric specs, and TikZ code to draw authentic BECE compass bearing diagrams with cardinal axes and directional rays.
---

# Diagram 06: Bearing and Direction Vectors

## Provenance
- **Exam Context:** BECE Mathematics 1997 Paper 1, Question 28
- **Question ID:** `Q_e58f0b2d0e81`
- **Topic:** Geometry and Measurement / Bearings and Vectors
- **Curriculum Indicator:** B9.3.2.1 / B9.3.2.2 (Determine three-figure bearings and compass directions from diagrams)

## Geometric & Visual Specification
- **Reference Axes:**
  - Vertical North-South line passing through origin $P(0, 0)$ from $y = -1.2$ to $y = 2.6$ with bidirectional `Stealth` arrowheads.
  - Direction label **North** positioned above the top arrow.
  - Horizontal East axis from $(0, 0)$ to $(4.0, 0)$ with rightward `Stealth` arrowhead and direction label **East**.
- **Reference Point $P$:**
  - Placed at $(0, 0)$, label **P** in large bold sans-serif (`\huge\sffamily\bfseries`) to the left of the vertical axis.
- **Target Point $Q$:**
  - Direction: $30^\circ$ counter-clockwise from East (equivalent to bearing $060^\circ$ clockwise from North).
  - Position: $(r\cos 30^\circ, r\sin 30^\circ) \approx (3.29, 1.90)$ with $r = 3.8\,\text{cm}$.
  - Marker: Solid filled black circle (radius $3.5\,\text{pt}$) with label **Q** to the right.
- **Angle Indicator:**
  - Arc centered at $P(0, 0)$ spanning from $0^\circ$ to $30^\circ$, radius $1.3\,\text{cm}$.
  - Label: $30^\circ$ centered inside the sector.

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** Navigation diagrams require exact compass direction vectors and trigonometric angle alignment. TikZ provides native polar coordinates `(ang:radius)` and standard directional arrowheads.

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{arrows.meta,calc}

\begin{document}
\begin{tikzpicture}[>=Stealth, scale=1.3]
    \coordinate (P) at (0, 0);
    
    % North-South vertical axis
    \draw[line width=1.3pt, <->] (0, -1.2) -- (0, 2.6) node[above=2pt, font=\Large\sffamily\bfseries] {North};
    
    % East horizontal axis
    \draw[line width=1.3pt, ->] (0, 0) -- (4.0, 0) node[right=3pt, font=\Large\sffamily\bfseries] {East};
    
    % Point P label
    \node[left=4pt, font=\huge\sffamily\bfseries] at (P) {P};
    
    % Ray to Q at 30 degrees elevation from East
    \def\ang{30}
    \def\len{3.8}
    \coordinate (Q) at ({\len*cos(\ang)}, {\len*sin(\ang)});
    
    \draw[line width=1.3pt] (P) -- (Q);
    \filldraw[black] (Q) circle (3.5pt) node[right=5pt, font=\huge\sffamily\bfseries] {Q};
    
    % Angle arc for 30 degrees (from 0 to 30)
    \draw[line width=0.9pt] ($(P) + (0:1.3)$) arc (0:\ang:1.3);
    \node[font=\large\bfseries] at (0.9, 0.25) {$30^\circ$};
    
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other bearing problems:
1. **Clockwise Bearing Arc from North:** Draw arc from $90^\circ$ clockwise to $90 - \beta$ with arrow pointing clockwise: `\draw[->] (90:1.6) arc (90:30:1.6) node[midway, above right] {060^\circ};`.
2. **Back Bearing (from Q to P):** Add a mini North-South compass cross at point $Q$ and draw the reflex arc from North at $Q$ to line $QP$.
3. **South/West Quadrants:** Use negative angles or quadrant angles (e.g. angle $220^\circ$ for South-West).
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] North axis is strictly vertical; East axis is strictly horizontal.
- [x] Three-figure bearing relation $060^\circ = 90^\circ - 30^\circ$ is geometrically exact.
- [x] Point $Q$ is clearly marked with a solid bullet.
- [x] Labels are bold sans-serif with zero overlap.
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
