---
name: diagram-11-polygon-interior-angles
description: Instructions, geometric specs, and TikZ code to draw authentic BECE irregular convex polygons with interior angle arcs and algebraic labels.
---

# Diagram 11: Convex Polygon with Interior Angle Expressions

## Provenance
- **Exam Context:** BECE Mathematics 2004 Paper 1, Question 25
- **Question ID:** `Q_c057c1472c8f`
- **Topic:** Geometry and Measurement / Polygons and Angle Sum
- **Curriculum Indicator:** B8.3.1.1 / B9.3.1.1 (Calculate interior and exterior angles of convex polygons)

## Geometric & Visual Specification
- **Polygon Classification:** Convex pentagon ($n = 5$), total interior angle sum:
  $$(n - 2) \times 180^\circ = 3 \times 180^\circ = 540^\circ$$
- **Vertex Coordinates:**
  - $V_1(0, 3.0)$: Top vertex (angle $4x$).
  - $V_2(-2.6, 1.4)$: Left vertex (angle $2x$).
  - $V_3(-1.8, -1.8)$: Bottom-left vertex (angle $3x$).
  - $V_4(1.7, -2.0)$: Bottom-right vertex (angle $5x$).
  - $V_5(2.8, 1.4)$: Right vertex (angle $x$).
- **Algebraic Verification:**
  $$4x + 2x + 3x + 5x + x = 15x = 540^\circ \implies x = 36^\circ$$
- **Internal Angle Arcs:**
  - Placed at each vertex spanning between adjacent edges.
  - Arc radii tuned between $0.85\,\text{cm}$ and $1.05\,\text{cm}$ depending on interior angle aperture.
  - Labels: **4X**, **2X**, **3X**, **5X**, **X** in bold sans-serif (`\Large\sffamily\bfseries`) centered inside each arc sector with balanced margins.

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** Polygon angle arcs require exact directional angles computed via $\arctan2(\Delta y, \Delta x)$ to guarantee that arc endpoints land directly on polygon edges without gaps or overshoots.

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc}

\begin{document}
\begin{tikzpicture}[scale=1.2]
    % 5 vertices of the pentagon
    \coordinate (V1) at (0, 3.0);       % 4X (top)
    \coordinate (V2) at (-2.6, 1.4);    % 2X (left)
    \coordinate (V3) at (-1.8, -1.8);   % 3X (bottom-left)
    \coordinate (V4) at (1.7, -2.0);    % 5X (bottom-right)
    \coordinate (V5) at (2.8, 1.4);     % X (right)
    
    % Draw polygon boundary
    \draw[line width=1.4pt] (V1) -- (V2) -- (V3) -- (V4) -- (V5) -- cycle;
    
    % Arcs at each vertex
    \draw[line width=1.0pt] ($(V1) + (212:0.9)$) arc (212:330:0.9);
    \node[font=\Large\sffamily\bfseries] at (0, 2.3) {4X};
    
    \draw[line width=1.0pt] ($(V2) + (284:0.85)$) arc (284:391.6:0.85);
    \node[font=\Large\sffamily\bfseries] at (-1.9, 1.25) {2X};
    
    \draw[line width=1.0pt] ($(V3) + (-3.3:0.95)$) arc (-3.3:104:0.95);
    \node[font=\Large\sffamily\bfseries] at (-1.3, -1.25) {3X};
    
    \draw[line width=1.0pt] ($(V4) + (72:1.05)$) arc (72:176.7:1.05);
    \node[font=\Large\sffamily\bfseries] at (1.0, -1.35) {5X};
    
    \draw[line width=1.0pt] ($(V5) + (150.3:0.9)$) arc (150.3:252:0.9);
    \node[font=\Large\sffamily\bfseries] at (2.05, 1.25) {X};
    
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other polygons (quadrilaterals, hexagons):
1. **$n$-gon Coordinates:** For regular $n$-gon, use polar loop: `\coordinate (V\i) at ({\i*360/n}: \R);`.
2. **Exterior Angles:** Extend edge segments past vertices using `\draw (V1) -- ($(V2)!1.3!(V1)$);` and draw exterior arcs between the extended edge and the adjacent polygon side.
3. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] All 5 polygon edges are continuous with solid line joins.
- [x] Angle arcs terminate precisely on their respective bounding edges.
- [x] Angle expressions are centered inside their arcs without edge clipping.
- [x] Sum of interior angles conforms to $540^\circ$.
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
