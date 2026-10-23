---
name: diagram-12-trapezium-area-composite
description: Instructions, geometric specs, and TikZ code to draw authentic BECE right trapeziums with dimension callouts and perpendicular altitudes.
---

# Diagram 12: Right Trapezium (Trapezoid) with Area Decomposition

## Provenance
- **Exam Context:** BECE Mathematics 2007 Paper 1, Question 20
- **Question ID:** `Q_1d388aa2a406`
- **Topic:** Geometry and Measurement / Area of Quadrilaterals and Trapeziums
- **Curriculum Indicator:** B7.3.1.3 / B8.3.1.3 (Calculate area of trapeziums using formula and composite decomposition)

## Geometric & Visual Specification
- **Parallel Bases:**
  - Lower base $CB$: Horizontal segment from $C(0, 0)$ to $B(18, 0)$, length $18\,\text{cm}$.
  - Upper base $DA$: Horizontal segment from $D(0, 6)$ to $A(12, 6)$, length $12\,\text{cm}$.
  - Slanted leg $AB$: Straight line from $A(12, 6)$ to $B(18, 0)$, run $\Delta x = 6\,\text{cm}$, drop $\Delta y = -6\,\text{cm}$.
- **Perpendicular Height:**
  - Left vertical side $DC$: Segment from $C(0, 0)$ to $D(0, 6)$, height $h = 6\,\text{cm}$.
  - Right angle symbols: True squares ($0.8 \times 0.8\,\text{cm}$ in scale units) at corners $D$ and $C$.
  - Internal altitude: Vertical dashed line from $A(12, 6)$ to $(12, 0)$, partitioning the shape into a $12 \times 6$ rectangle and a $6 \times 6$ right triangle.
  - Formula: $\text{Area} = \frac{12 + 18}{2} \times 6 = 90\,\text{cm}^2$.
- **Dimension Callouts:**
  - Top: Outward pointing arrows with centered label **12cm**.
  - Bottom: Outward pointing arrows with centered label **18cm**.
  - Left: Outward pointing vertical arrows with label **6cm**.
- **Typography:** Bold sans-serif vertex labels **D**, **A**, **C**, **B** (`\huge\sffamily\bfseries`).

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** Technical drafting dimensions require collinear arrow segments and exact right-angle markers. TikZ provides native coordinate geometry for exact dimension matching without manual pixel nudging.

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=15pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{arrows.meta}

\begin{document}
\begin{tikzpicture}[>=Stealth, scale=0.65]
    % Trapezium coordinates: C(0,0), B(18,0), A(12,6), D(0,6)
    \coordinate (C) at (0, 0);
    \coordinate (B) at (18, 0);
    \coordinate (A) at (12, 6);
    \coordinate (D) at (0, 6);
    
    % Draw boundary
    \draw[line width=1.4pt] (C) -- (B) -- (A) -- (D) -- cycle;
    
    % Dashed vertical altitude from A to base
    \draw[line width=1.2pt, dashed] (A) -- (12, 0);
    
    % Right angle symbols at D and C
    \draw[line width=1.0pt] (0, 5.2) -- (0.8, 5.2) -- (0.8, 6);
    \draw[line width=1.0pt] (0, 0.8) -- (0.8, 0.8) -- (0.8, 0);
    
    % Vertex labels in bold sans-serif
    \node[above left=3pt, font=\huge\sffamily\bfseries] at (D) {D};
    \node[above right=3pt, font=\huge\sffamily\bfseries] at (A) {A};
    \node[below left=3pt, font=\huge\sffamily\bfseries] at (C) {C};
    \node[right=4pt, font=\huge\sffamily\bfseries] at (B) {B};
    
    % Dimension callout for DA = 12cm (above)
    \draw[line width=1.1pt, <-] (0, 6.7) -- (4.2, 6.7);
    \draw[line width=1.1pt, ->] (7.8, 6.7) -- (12, 6.7);
    \node[font=\Large\sffamily\bfseries] at (6, 6.7) {12cm};
    
    % Dimension callout for CB = 18cm (below)
    \draw[line width=1.1pt, <-] (0, -0.7) -- (7.2, -0.7);
    \draw[line width=1.1pt, ->] (10.8, -0.7) -- (18, -0.7);
    \node[font=\Large\sffamily\bfseries] at (9, -0.7) {18cm};
    
    % Dimension callout for DC = 6cm (left)
    \draw[line width=1.1pt, <-] (-0.8, 6) -- (-0.8, 3.8);
    \draw[line width=1.1pt, ->] (-0.8, 2.2) -- (-0.8, 0);
    \node[left=2pt, font=\Large\sffamily\bfseries] at (-0.8, 3) {6cm};
    
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other trapezium problems:
1. **Isosceles Trapezium:** Set $D(3, 6)$, $A(15, 6)$, $C(0, 0)$, $B(18, 0)$ and drop two dashed altitudes from $D$ and $A$.
2. **Finding Unknown Base or Altitude:** Replace one dimension with an algebraic variable (e.g. `$x\text{ cm}$` or `$h\text{ cm}$`).
3. **Internal Angle Arc:** Add acute angle arc at vertex $B$ or obtuse angle arc at vertex $A$.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] Upper and lower bases are strictly horizontal and parallel.
- [x] Vertical side $DC$ is perpendicular with dual square markers.
- [x] Dashed altitude drops perpendicular to baseline at $x = 12$.
- [x] Dimension lines are clearly separated from polygon edges.
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
