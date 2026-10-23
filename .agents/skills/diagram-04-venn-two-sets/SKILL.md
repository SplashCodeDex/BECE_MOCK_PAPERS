---
name: diagram-04-venn-two-sets
description: Instructions, geometric specs, and TikZ code to draw authentic BECE 2-set Venn diagrams with universal set rectangles and regional cardinalities.
---

# Diagram 04: Two-Set Venn Diagram with Universal Boundary

## Provenance
- **Exam Context:** BECE Mathematics 2002 Paper 1, Question 23
- **Question ID:** `Q_efaa984b2f33`
- **Topic:** Set Theory / Two-Set Cardinality and Intersection
- **Curriculum Indicator:** B7.1.1.1 / B8.1.1.1 (Find union, intersection, and complements of two sets)

## Geometric & Visual Specification
- **Universal Set Boundary:**
  - Outer rectangle from $(-3.4, -2.0)$ to $(3.4, 1.8)$, line width $1.5\,\text{pt}$.
  - Top-right external label: $\boldsymbol{\mu = 40}$ (or $U = 40$) placed above the boundary at $(2.4, 1.8)$.
- **Set Shapes:**
  - Two overlapping ellipses:
    - Left ellipse center at $(-1.1, -0.1)$, radii $(2.0\,\text{cm}, 1.25\,\text{cm})$, line width $1.3\,\text{pt}$.
    - Right ellipse center at $(1.1, -0.1)$, radii $(2.0\,\text{cm}, 1.25\,\text{cm})$, line width $1.3\,\text{pt}$.
- **Labels & Cardinalities:**
  - Left set label **Ga** inside top-left corner at $(-2.8, 1.3)$.
  - Right set label **Twi** inside top-right corner at $(2.6, 1.3)$.
  - Only Ga ($A \setminus B$): **11** centered at $(-1.7, -0.1)$.
  - Both Ga and Twi ($A \cap B$): **17** centered at $(0.0, -0.1)$.
  - Only Twi ($B \setminus A$): **7** centered at $(1.7, -0.1)$.
  - Neither ($(A \cup B)'$): **5** placed in the lower-right margin at $(2.7, -1.4)$.
- **Typography:** Bold sans-serif numerals and letters (`\sffamily\bfseries`) matching official BECE typography.

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** TikZ enables exact geometric ellipse placement, symmetrical intersection overlap, clean rectangular framing, and precise placement of cardinal numerals without region clipping.

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usepackage{bm}

\begin{document}
\begin{tikzpicture}[scale=1.2]
    % Universal set rectangle
    \draw[line width=1.5pt] (-3.4, -2.0) rectangle (3.4, 1.8);
    
    % Universal set label above top right
    \node[above=3pt, font=\Large\sffamily\bfseries] at (2.4, 1.8) {\boldmath$\mu = 40$};
    
    % Two overlapping ellipses
    \draw[line width=1.3pt] (-1.1, -0.1) ellipse (2.0cm and 1.25cm);
    \draw[line width=1.3pt] (1.1, -0.1) ellipse (2.0cm and 1.25cm);
    
    % Set labels inside top corners of rectangle
    \node[font=\Large\sffamily\bfseries] at (-2.8, 1.3) {Ga};
    \node[font=\Large\sffamily\bfseries] at (2.6, 1.3) {Twi};
    
    % Regional counts in clean bold sans-serif
    \node[font=\huge\sffamily\bfseries] at (-1.7, -0.1) {11};
    \node[font=\huge\sffamily\bfseries] at (0, -0.1) {17};
    \node[font=\huge\sffamily\bfseries] at (1.7, -0.1) {7};
    \node[font=\huge\sffamily\bfseries] at (2.7, -1.4) {5};
    
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other Venn diagram questions:
1. **Algebraic Unknowns:** Replace numeral strings with variables (e.g. `$x$`, `$2x - 3$`, `$15 - x$`).
2. **Shading Regions:** Use `\begin{scope} \clip ... \fill[gray!30] ... \end{scope}` to shade specific regions such as $(A \cap B)'$ or $A \cup B$.
3. **Disjoint Sets:** Increase separation between ellipse centers (e.g. centers at $(-1.5, 0)$ and $(1.5, 0)$ with radius $1.2\,\text{cm}$) so they do not overlap.
4. **Subset ($B \subset A$):** Draw outer ellipse with radii $(2.2, 1.4)$ and nested inner ellipse with radii $(1.0, 0.7)$ completely inside.
5. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] Ellipses overlap symmetrically across $x = 0$.
- [x] Sum of regions matches declared universal set: $11 + 17 + 7 + 5 = 40$.
- [x] Universal set label $\mu = 40$ sits strictly above the frame.
- [x] Numbers are large, bold, and centered in each region without touching borders.
- [x] Crisp 300 DPI PNG with zero blurriness.
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
