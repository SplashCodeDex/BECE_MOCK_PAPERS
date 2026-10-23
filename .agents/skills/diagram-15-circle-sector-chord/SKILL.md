---
name: diagram-15-circle-sector-chord
description: Instructions, geometric specs, and TikZ code to draw authentic BECE circle geometry diagrams featuring chords, sectors, and center points.
---

# Diagram 15: Circle Geometry (Chord and Shaded Sector)

## Provenance
- **Exam Context:** BECE Mathematics 1999 Paper 1, Questions 11 & 12
- **Question ID:** `Q_636409a71512`
- **Topic:** Geometry and Measurement / Circle Properties (Chords, Sectors, Segments)
- **Curriculum Indicator:** B7.3.1.4 / B8.3.1.4 (Identify parts of a circle: chord, sector, segment, arc, radius)

## Geometric & Visual Specification
- **Circle Geometry:**
  - Circle radius $R = 3.0\,\text{cm}$ centered at origin $O(0, 0)$, line width $1.5\,\text{pt}$.
- **Horizontal Chord ($ST$):**
  - Height: $y = 1.8\,\text{cm}$ above center.
  - Endpoints: $S(-\sqrt{R^2 - y^2}, y) = (-2.4, 1.8)$ and $T(2.4, 1.8)$.
  - Line width: $1.5\,\text{pt}$.
  - Labels: **S** placed left of $(-2.4, 1.8)$, **T** placed right of $(2.4, 1.8)$.
- **Shaded Sector:**
  - Radial bounds: Two radii from $O(0, 0)$ to $(-135^\circ : R)$ and $(-45^\circ : R)$ (angular span $90^\circ$ in the lower quadrant).
  - Shading: Horizontal line hatching using TikZ `patterns` library (`pattern=horizontal lines, pattern color=black`).
  - Perimeter: Solid radii and arc boundary ($1.4\,\text{pt}$).
- **Center Label:**
  - **O** in bold sans-serif (`\huge\sffamily\bfseries`) positioned at $(0, 0.4)$ directly above the sector apex.

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** Native circle intersection math ($\sqrt{R^2 - y^2}$) guarantees the chord endpoints meet the circumference, and TikZ's `patterns` library provides vector hatching for the sector.

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=15pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{patterns}

\begin{document}
\begin{tikzpicture}[scale=1.3]
    \def\r{3.0} % circle radius
    \def\yChord{1.8}
    \pgfmathsetmacro{\xChord}{sqrt(\r*\r - \yChord*\yChord)} % 2.4
    
    \coordinate (O) at (0, 0);
    \coordinate (S) at (-\xChord, \yChord);
    \coordinate (T) at (\xChord, \yChord);
    
    % Shaded sector in the bottom quadrant (-135 to -45)
    \fill[pattern=horizontal lines, pattern color=black] (O) -- (-135:\r) arc (-135:-45:\r) -- cycle;
    \draw[line width=1.4pt] (O) -- (-135:\r);
    \draw[line width=1.4pt] (O) -- (-45:\r);
    
    % Circle boundary
    \draw[line width=1.5pt] (O) circle (\r);
    
    % Horizontal chord ST
    \draw[line width=1.5pt] (S) -- (T);
    
    % Labels
    \node[above=3pt, font=\huge\sffamily\bfseries] at (O) {O};
    \node[left=4pt, font=\huge\sffamily\bfseries] at (S) {S};
    \node[right=4pt, font=\huge\sffamily\bfseries] at (T) {T};
    
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other circle geometry questions:
1. **Shaded Segment:** To shade a circular segment bounded by chord $ST$, fill between chord and arc: `\fill[pattern=horizontal lines] (S) arc (143:37:\r) -- cycle;`.
2. **Tangent Line:** Draw a tangent at point $P(0, -R)$ perpendicular to the radius: `\draw (-2, -\r) -- (2, -\r);`.
3. **Inscribed Angle / Cyclic Quadrilateral:** Connect points on circumference to form an inscribed triangle or quadrilateral.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] Chord endpoints $S$ and $T$ terminate exactly on the circle circumference.
- [x] Sector radii radiate directly from the center point $O$.
- [x] Hatching pattern lines are evenly spaced and strictly confined to the sector.
- [x] Labels **O**, **S**, **T** are bold sans-serif with zero overlap.
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
