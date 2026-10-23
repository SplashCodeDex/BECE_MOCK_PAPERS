---
name: diagram-19-bar-chart-frequency
description: Replicate the authentic BECE frequency distribution bar chart on millimeter graph paper grid using TikZ.
---

# Diagram 19: Frequency Distribution Bar Chart on Millimeter Graph Paper

## 1. Provenance & Pedagogical Context
- **Source Question:** `Q_6460e408ec21` / `pdf_Mathematics_2022_BECE-MATHEMATICS-1990-2013_ee6bb659_p207_1495.jpeg`
- **BECE Past Paper:** BECE Mathematics Past Paper (Statistics & Data Representation)
- **Question:** *"The bar chart shows the distribution of marks scored by pupils in a test. How many pupils took the test?"*
- **Mathematical Significance:** Tests reading values from a statistical frequency bar chart rendered against a precision graph paper grid.
  - Total pupils $= \sum \text{frequency} = 0 + 3 + 2 + 1 + 4 + 5 + 4 + 1 + 2 + 3 = 25$ pupils.

---

## 2. Geometric Specifications & Coordinates
- **Grid Frame:** $(0, 0)$ to $(10.5, 5.0)$ with outer border `line width=1.4pt`.
- **Minor Grid:** Fine graph paper subdivisions of step $0.2\,\text{cm}$ in `gray!35`, `line width=0.4pt`.
- **Major Grid:** Standard grid lines every $1.0\,\text{cm}$ in `black!80`, `line width=0.8pt`.
- **Bars:**
  - Bar width: $0.8\,\text{cm}$ centered on mark integers $x \in \{2, 3, 4, 5, 6, 7, 8, 9, 10\}$.
  - Bar heights: $(2, 3), (3, 2), (4, 1), (5, 4), (6, 5), (7, 4), (8, 1), (9, 2), (10, 3)$.
  - Fill style: `black!60` with sharp `black!90` stroke.
- **Labels:**
  - Y-axis (Frequency): Integers $0$ to $5$ on left, title `FREQUENCY` rotated $90^\circ$ at $x = -1.1$.
  - X-axis (Marks): Integers $1$ to $10$ below, title `MARKS` placed below mark $10$.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Essential for exact grid line alignment and mathematical consistency with dual minor/major grid steps ($0.2$ and $1.0$).

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=15pt]{standalone}
\usepackage{amsmath,amssymb}

\begin{document}
\begin{tikzpicture}[scale=1.2]
    % Fine graph paper grid (subdivisions of 0.2)
    \draw[step=0.2, gray!35, line width=0.4pt] (0, 0) grid (10.5, 5.0);
    
    % Major grid lines (every 1.0 unit)
    \draw[step=1.0, black!80, line width=0.8pt] (0, 0) grid (10.5, 5.0);
    
    % Solid bars (width 0.8 centered on mark integer)
    \foreach \m/\f in {2/3, 3/2, 4/1, 5/4, 6/5, 7/4, 8/1, 9/2, 10/3} {
        \fill[black!60, draw=black!90, line width=0.6pt] ({\m - 0.4}, 0) rectangle ({\m + 0.4}, \f);
    }
    
    % Outer boundary frame
    \draw[line width=1.4pt] (0, 0) rectangle (10.5, 5.0);
    
    % Y-axis labels (0 to 5)
    \foreach \y in {0, 1, 2, 3, 4, 5} {
        \node[left=3pt, font=\Large\sffamily\bfseries] at (0, \y) {\y};
    }
    
    % X-axis labels (1 to 10)
    \foreach \x in {1, 2, 3, 4, 5, 6, 7, 8, 9, 10} {
        \node[below=4pt, font=\Large\sffamily\bfseries] at (\x, 0) {\x};
    }
    
    % Axis Titles
    \node[rotate=90, font=\LARGE\sffamily\bfseries] at (-1.1, 2.5) {FREQUENCY};
    \node[below=18pt, font=\LARGE\sffamily\bfseries] at (9.6, 0) {MARKS};
    
\end{tikzpicture}
\end{document}
```

---

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

## 5. Agent Replication Guide
1. Draw the $0.2$ minor grid first in light gray, then overlay the $1.0$ major grid in darker line weight.
2. Render bars as filled rectangles from $x - 0.4$ to $x + 0.4$ with height $f$.
3. Keep bold sans-serif lettering for examination style typography.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

---

## 6. Verification & Quality Checklist
- [x] Dual-frequency graph grid (2mm / 10mm) rendered without aliasing.
- [x] Bars match frequency distribution table exactly.
- [x] Axis titles and mark coordinates aligned with zero overlap.
- [x] Visual inspection gate passed (300 DPI PNG reviewed and verified critically)
- [x] 300 DPI vector clarity.
