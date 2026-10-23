---
name: diagram-14-straight-line-angles
description: Instructions, geometric specs, and TikZ code to draw authentic BECE supplementary angles on a straight line with exact angular rays.
---

# Diagram 14: Angles on a Straight Line ($180^\circ$ Supplementary Angles)

## Provenance
- **Exam Context:** BECE Mathematics 2006 Paper 1, Question 21
- **Question ID:** `Q_d047ab2fc14e`
- **Topic:** Geometry and Measurement / Angles on a Straight Line
- **Curriculum Indicator:** B7.3.1.1 / B8.3.1.1 (Use supplementary angle properties to solve linear equations)

## Geometric & Visual Specification
- **Baseline Segment ($PQR$):**
  - Continuous horizontal line spanning from $P(-4.2, 0)$ to $R(4.2, 0)$ through vertex $Q(0, 0)$, line width $1.4\,\text{pt}$.
- **Rays ($QT$ and $QS$):**
  - Algebraic solution: $x^\circ + 102^\circ + 2x^\circ = 180^\circ \implies 3x = 78^\circ \implies x = 26^\circ$.
  - Ray $QS$: Inclination angle $\theta_S = 2x = 52^\circ$, length $4.2\,\text{cm}$.
  - Ray $QT$: Inclination angle $\theta_T = 52^\circ + 102^\circ = 154^\circ$ ($180^\circ - x$), length $4.0\,\text{cm}$.
- **Angle Arcs & Labels:**
  - Right angle arc: $0^\circ \to 52^\circ$, radius $1.0\,\text{cm}$, label $2x^\circ$ at polar $(26^\circ : 1.45\,\text{cm})$.
  - Middle angle arc: $52^\circ \to 154^\circ$, radius $0.75\,\text{cm}$, label $102^\circ$ at $(0, 1.15)$.
  - Left angle arc: $154^\circ \to 180^\circ$, radius $1.0\,\text{cm}$, label $x^\circ$ at polar $(167^\circ : 1.45\,\text{cm})$.
- **Typography:** Bold sans-serif vertex labels **P**, **Q**, **R**, **T**, **S** in `\huge\sffamily\bfseries`.

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** Strict collinearity of the baseline $PQR$ and exact trigonometric rays ($52^\circ$ and $154^\circ$) ensure the drawn angles are mathematically true to the algebraic solution ($x = 26$).

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=15pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc}

\begin{document}
\begin{tikzpicture}[scale=1.3]
    % Straight line PQR
    \coordinate (Q) at (0, 0);
    \coordinate (P) at (-4.2, 0);
    \coordinate (R) at (4.2, 0);
    
    \draw[line width=1.4pt] (P) -- (R);
    
    % Rays QT and QS
    % x = 26 deg: angle of QS = 52 deg, angle of QT = 154 deg
    \def\lenT{4.0}
    \def\lenS{4.2}
    \coordinate (T) at ({154:\lenT});
    \coordinate (S) at ({52:\lenS});
    
    \draw[line width=1.3pt] (Q) -- (T);
    \draw[line width=1.3pt] (Q) -- (S);
    
    % Vertices labels
    \node[left=3pt, font=\huge\sffamily\bfseries] at (P) {P};
    \node[right=3pt, font=\huge\sffamily\bfseries] at (R) {R};
    \node[below=4pt, font=\huge\sffamily\bfseries] at (Q) {Q};
    \node[above left=2pt, font=\huge\sffamily\bfseries] at (T) {T};
    \node[above right=2pt, font=\huge\sffamily\bfseries] at (S) {S};
    
    % Angle arcs
    \draw[line width=1.0pt] ($(Q) + (154:1.0)$) arc (154:180:1.0);
    \node[font=\Large\bfseries] at ($(Q) + (167:1.45)$) {$x^\circ$};
    
    \draw[line width=1.0pt] ($(Q) + (52:0.75)$) arc (52:154:0.75);
    \node[font=\Large\bfseries] at (0, 1.15) {$102^\circ$};
    
    \draw[line width=1.0pt] ($(Q) + (0:1.0)$) arc (0:52:1.0);
    \node[font=\Large\bfseries] at ($(Q) + (26:1.45)$) {$2x^\circ$};
    
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other straight line angle questions:
1. **Two Angles (Linear Pair):** Single ray at angle $\theta$, left arc $(180 - \theta)^\circ$, right arc $\theta^\circ$.
2. **Four or More Angles:** Add additional rays and calculate intermediate arc bounds sequentially: `arc (start:end:radius)`.
3. **Vertically Opposite Angles:** Extend rays $QT$ and $QS$ past vertex $Q$ into the lower half-plane (`(Q) -- (-T)`).
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] Baseline $PQR$ is strictly collinear and horizontal.
- [x] Angles $26^\circ + 102^\circ + 52^\circ = 180^\circ$ strictly sum to a straight angle.
- [x] Arcs do not collide with adjacent rays or labels.
- [x] Vertex $Q$ label sits directly below the intersection junction.
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
