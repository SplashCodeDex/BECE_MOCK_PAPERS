---
name: diagram-10-running-track-mensuration
description: Instructions, geometric specs, and TikZ code to draw authentic BECE running tracks and composite rectangle-semicircle mensuration diagrams.
---

# Diagram 10: Running Track / Stadium Capsule Mensuration

## Provenance
- **Exam Context:** BECE Mathematics 2000 Paper 2, Question 3
- **Question ID:** `Q_d8f430165860`
- **Topic:** Geometry and Measurement / Perimeter and Area of Composite Plane Figures
- **Curriculum Indicator:** B8.3.1.4 / B9.3.1.4 (Calculate perimeter and area of composite shapes combining rectangles and semicircles)

## Geometric & Visual Specification
- **Central Rectangular Region:**
  - Length $|AB| = |ED| = 90\,\text{m}$ (rendered as $9.0\,\text{cm}$ in TikZ, half-width $w = 4.5\,\text{cm}$).
  - Height $|AE| = |BD| = 70\,\text{m}$ (rendered as $7.0\,\text{cm}$, radius $r = 3.5\,\text{cm}$).
  - Top horizontal segment: $(-\w, \r) \to (\w, \r)$.
  - Bottom horizontal segment: $(-\w, -\r) \to (\w, -\r)$.
  - Internal boundary lines: Vertical dashed lines connecting $(-\w, -\r) \to (-\w, \r)$ and $(\w, -\r) \to (\w, \r)$.
- **Semicircular Ends:**
  - Left semicircle $AFE$: Centered at $(-\w, 0)$ with radius $r = 3.5\,\text{cm}$, swept from $90^\circ$ to $270^\circ$, vertex **F** at $(-\w - \r, 0)$.
  - Right semicircle $BCD$: Centered at $(\w, 0)$ with radius $r = 3.5\,\text{cm}$, swept from $-90^\circ$ to $90^\circ$, vertex **C** at $(\w + \r, 0)$.
  - Semicircles are smoothly tangent ($C^1$ continuity) to the top and bottom straight lines.
- **Dimension Lines & Callouts:**
  - Top dimension: Vertical extension ticks at $A$ and $B$, outward-pointing arrows (`<-` and `->`) to $A$ and $B$ with centered label **90m** at $(0, \r + 0.45)$.
  - Internal vertical dimension: Vertical arrows along dashed line $AE$ pointing up and down with centered label **70m** at $(-\w + 0.65, 0)$.
- **Typography:** Bold sans-serif vertex labels **A**, **B**, **C**, **D**, **E**, **F** and dimension text in `\sffamily\bfseries`.

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** Smooth tangent continuity between circular arcs and straight lines requires exact radius-height matching (`\r = 3.5`), which TikZ executes with precision.

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=15pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{arrows.meta}

\begin{document}
\begin{tikzpicture}[>=Stealth, scale=0.95]
    % Running track: AB = 9.0 cm, diameter AE = 7.0 cm (radius R = 3.5 cm)
    \def\w{4.5} % half width, so AB = 9.0
    \def\r{3.5} % radius, so height = 7.0
    
    \coordinate (A) at (-\w, \r);
    \coordinate (B) at (\w, \r);
    \coordinate (D) at (\w, -\r);
    \coordinate (E) at (-\w, -\r);
    \coordinate (F) at ({-\w - \r}, 0);
    \coordinate (C) at ({\w + \r}, 0);
    
    % Outer boundary of running track
    \draw[line width=1.4pt] (A) -- (B);
    \draw[line width=1.4pt] (E) -- (D);
    \draw[line width=1.4pt] (D) arc (-90:90:\r);
    \draw[line width=1.4pt] (A) arc (90:270:\r);
    
    % Dashed internal divider lines
    \draw[line width=1.2pt, dashed] (A) -- (E);
    \draw[line width=1.2pt, dashed] (B) -- (D);
    
    % Vertices labels in bold sans-serif
    \node[above left=2pt, font=\huge\sffamily\bfseries] at (A) {A};
    \node[above right=2pt, font=\huge\sffamily\bfseries] at (B) {B};
    \node[right=4pt, font=\huge\sffamily\bfseries] at (C) {C};
    \node[below right=2pt, font=\huge\sffamily\bfseries] at (D) {D};
    \node[below left=2pt, font=\huge\sffamily\bfseries] at (E) {E};
    \node[left=4pt, font=\huge\sffamily\bfseries] at (F) {F};
    
    % Dimension callout for AB = 90m (above top line)
    \draw[line width=1.1pt] (-\w, {\r + 0.05}) -- (-\w, {\r + 0.7});
    \draw[line width=1.1pt] (\w, {\r + 0.05}) -- (\w, {\r + 0.7});
    \draw[line width=1.1pt, <-] (-\w, {\r + 0.45}) -- (-0.8, {\r + 0.45});
    \draw[line width=1.1pt, ->] (0.8, {\r + 0.45}) -- (\w, {\r + 0.45});
    \node[font=\Large\sffamily\bfseries] at (0, {\r + 0.45}) {90m};
    
    % Dimension callout for AE = 70m (inside vertical arrow adjacent to AE)
    \draw[line width=1.1pt, <-] ({-\w + 0.45}, {\r - 0.05}) -- ({-\w + 0.45}, 0.5);
    \draw[line width=1.1pt, ->] ({-\w + 0.45}, -0.5) -- ({-\w + 0.45}, {-\r + 0.05});
    \node[font=\Large\sffamily\bfseries] at ({-\w + 0.65}, 0) {70m};
    
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other composite mensuration problems:
1. **Lanes Addition:** Add concentric arcs and lines offset by lane width $w_{\text{lane}}$ (e.g. `\draw (A) ++(0, 0.4) -- ++(2*\w, 0);`).
2. **Semi-Circle Shading:** Fill regions using `\fill[gray!20] (A) arc (90:270:\r) -- cycle;` to indicate flower beds or grass verges.
3. **Inner Field Area:** Fill the rectangular infield with `\fill[green!10] (-\w, -\r) rectangle (\w, \r);`.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] Semicircular ends are tangent to horizontal straight edges with no kinks.
- [x] Dashed lines clearly demarcate composite shapes.
- [x] Dimension lines employ single outward-pointing arrowheads against boundaries.
- [x] Aspect ratio strictly matches $90\,\text{m} : 70\,\text{m}$.
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
