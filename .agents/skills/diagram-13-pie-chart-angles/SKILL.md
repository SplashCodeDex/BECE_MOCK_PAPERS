---
name: diagram-13-pie-chart-angles
description: Instructions, geometric specs, and TikZ code to draw authentic BECE pie charts with exact sector degree subdivisions and radial labels.
---

# Diagram 13: Pie Chart Sector Proportions and Unknown Angles

## Provenance
- **Exam Context:** BECE Mathematics 2007 Paper 1, Question 8
- **Question ID:** `Q_596d329644d8`
- **Topic:** Handling Data / Pie Charts and Frequency Distribution
- **Curriculum Indicator:** B7.4.1.2 / B8.4.1.2 (Interpret and construct pie charts by converting frequencies to central angles)

## Geometric & Visual Specification
- **Circular Boundary:**
  - Circle radius $R = 3.2\,\text{cm}$ centered at origin $(0, 0)$, line width $1.4\,\text{pt}$.
- **Sector Partitions:**
  - Total central angle sum = $360^\circ$.
  - **Red House:** $150^\circ$, swept from $20^\circ$ to $170^\circ$.
  - **Yellow House:** $100^\circ$, swept from $170^\circ$ to $270^\circ$.
  - **Green House:** $x^\circ = 40^\circ$, swept from $270^\circ$ to $310^\circ$.
  - **Blue House:** $70^\circ$, swept from $310^\circ$ to $380^\circ$ ($20^\circ$).
  - Boundary dividing lines drawn from $(0, 0)$ to $(20:R)$, $(170:R)$, $(270:R)$, $(310:R)$.
- **Central Angle Arcs & Labels:**
  - Continuous concentric arc ring of radius $r_{\text{arc}} = 0.65\,\text{cm}$ around the center.
  - Angular degree labels ($150^\circ, 100^\circ, x^\circ, 70^\circ$) positioned at radial distance $1.15\,\text{cm}$ to $1.25\,\text{cm}$ along the bisector of each sector.
- **Category Labels:**
  - Bold sans-serif text (`\Large\sffamily\bfseries`) in the outer ring of each sector (radius $2.25\,\text{cm}$).

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** Pie charts demand rigorous angular subdivisions totaling exactly $360^\circ$. TikZ's polar coordinate system `(angle:radius)` ensures exact sector partition lines and symmetric label centering.

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=15pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc}

\begin{document}
\begin{tikzpicture}[scale=1.45]
    \def\r{3.2} % radius of pie chart
    \def\rarc{0.65} % radius of central angle arcs
    
    % Circle boundary
    \draw[line width=1.4pt] (0, 0) circle (\r);
    
    % Radial dividing lines
    \draw[line width=1.3pt] (0, 0) -- (20:\r);
    \draw[line width=1.3pt] (0, 0) -- (170:\r);
    \draw[line width=1.3pt] (0, 0) -- (270:\r);
    \draw[line width=1.3pt] (0, 0) -- (310:\r);
    
    % Central angle arcs
    \draw[line width=0.9pt] (20:\rarc) arc (20:170:\rarc);
    \draw[line width=0.9pt] (170:\rarc) arc (170:270:\rarc);
    \draw[line width=0.9pt] (270:\rarc) arc (270:310:\rarc);
    \draw[line width=0.9pt] (310:\rarc) arc (310:380:\rarc);
    
    % Angle labels
    \node[font=\large\bfseries] at (95:1.15) {$150^\circ$};
    \node[font=\large\bfseries] at (220:1.15) {$100^\circ$};
    \node[font=\large\bfseries] at (290:1.25) {$x^\circ$};
    \node[font=\large\bfseries] at (345:1.15) {$70^\circ$};
    
    % Category labels
    \node[font=\Large\sffamily\bfseries, align=center] at (95:2.25) {Red\\House};
    \node[font=\Large\sffamily\bfseries, align=center] at (215:2.25) {Yellow\\House};
    \node[font=\Large\sffamily\bfseries, align=center] at (290:2.35) {Green\\House};
    \node[font=\Large\sffamily\bfseries, align=center] at (345:2.25) {Blue\\House};
    
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other data sets (percentages or counts):
1. **Converting Frequencies to Angles:** For categories with frequencies $f_i$ and total $N$, compute $\theta_i = \frac{f_i}{N} \times 360^\circ$.
2. **Color Shading:** Fill each sector using `\fill[fill=red!20] (0,0) -- (start:\r) arc (start:end:\r) -- cycle;`.
3. **Exploded Slice:** Shift a specific sector along its bisector vector `+(bisector:0.3)` to highlight an item.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] Sectors partition the full $360^\circ$ circle with zero overlap.
- [x] Boundary radii radiate from the true center $(0, 0)$.
- [x] Degree labels and category titles are spaced radially without collision.
- [x] Central angle arcs form a continuous concentric ring.
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
