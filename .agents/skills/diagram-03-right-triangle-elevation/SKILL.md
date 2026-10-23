---
name: diagram-03-right-triangle-elevation
description: Instructions, geometric specs, and TikZ code to draw authentic BECE right-angled triangles with exact trigonometric scaling and elevation angle arcs.
---

# Diagram 03: Right-Angled Triangle with Angle of Elevation / Depression

## Provenance
- **Exam Context:** BECE Mathematics 2006 Paper 1, Question 22
- **Question ID:** `Q_25556e45208a`
- **Topic:** Geometry and Trigonometry / Bearings, Angles of Elevation and Depression
- **Curriculum Indicator:** B9.3.2.1 (Apply tangent, sine, and cosine ratios to solve right-angled triangle problems)

## Geometric & Visual Specification
- **Vertices:**
  - $G(0, 0)$: Right-angled vertex at the bottom-left.
  - $K(0, 3.0)$: Top vertex on the vertical leg.
  - $M(5.64, 0)$: Base endpoint on the horizontal leg ($GM = KG \times \tan 62^\circ \approx 5.64\,\text{cm}$).
- **Right Angle Indicator:**
  - Square marker at vertex $G$ spanning from $(0, 0.45)$ to $(0.45, 0.45)$ to $(0.45, 0)$.
- **Angle Arc at $K$:**
  - Arc centered at $K(0, 3.0)$, starting along vertical downward line ($270^\circ$) to hypotenuse ($332^\circ$, equivalent to $-28^\circ$), radius $0.85\,\text{cm}$.
  - Label: $62^\circ$ centered neatly inside the arc.
- **Labels:**
  - **K** placed left of $(0, 3.0)$.
  - **G** placed left of $(0, 0)$.
  - **M** placed right of $(5.64, 0)$.
  - Typography: Bold sans-serif `\sffamily\bfseries` for geometric points, math mode for angle values.

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** Exact trigonometric scaling ensures the visual drawing is mathematically faithful to the declared $62^\circ$ angle ($\tan 62^\circ = 1.8807$). TikZ's `calc` library enables clean polar arc offsets from vertex $K$.

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc}

\begin{document}
\begin{tikzpicture}[scale=1.3]
    % Triangle dimensions: KG = 3.0, GM = 3.0 * tan(62 deg) = 5.64
    \pgfmathsetmacro{\kg}{3.0}
    \pgfmathsetmacro{\gm}{5.64}
    
    \coordinate (G) at (0, 0);
    \coordinate (K) at (0, \kg);
    \coordinate (M) at (\gm, 0);
    
    % Draw triangle boundary
    \draw[line width=1.1pt] (G) -- (M) -- (K) -- cycle;
    
    % Vertices labels in bold sans-serif
    \node[left=4pt, font=\Large\sffamily\bfseries] at (G) {G};
    \node[left=4pt, font=\Large\sffamily\bfseries] at (K) {K};
    \node[right=4pt, font=\Large\sffamily\bfseries] at (M) {M};
    
    % Right angle symbol at G
    \draw[line width=1.0pt] (0, 0.45) -- (0.45, 0.45) -- (0.45, 0);
    
    % Angle arc at K: from vertical downward (270) towards hypotenuse (332)
    \draw[semithick] ($(K) + (270:0.85)$) arc (270:332:0.85);
    \node[font=\bfseries] at (0.35, {\kg - 0.48}) {$62^\circ$};
    
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other trigonometry / Pythagoras questions:
1. **Changing Given Angle:** If angle at $M$ is given as $\alpha$ instead of $K$, set $\gm = \kg / \tan(\alpha)$ and draw the arc at $M$ from $180 - \alpha$ to $180$.
2. **Adding Dimension Callouts:** Use `node[midway, left] {12\text{ cm}}` along $KG$ and `node[midway, below] {x}` along $GM$.
3. **Hypotenuse Label:** Add `node[midway, above right] {c}` along the diagonal segment $(K) -- (M)$.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] Geometric proportions strictly match $\tan 62^\circ \approx 1.88$.
- [x] Right angle symbol is a true square at vertex $G$.
- [x] Arc at $K$ begins and terminates exactly on the triangle legs.
- [x] Vertex letters are large, bold, and positioned outside the polygon boundary.
- [x] Crisp 300 DPI PNG with transparent/white canvas.
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
