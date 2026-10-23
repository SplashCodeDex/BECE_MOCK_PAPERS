---
name: diagram-07-similar-triangles-enlargement
description: Instructions, geometric specs, and TikZ code to draw authentic BECE similar right triangles and scale factor enlargements.
---

# Diagram 07: Similar Right Triangles & Enlargement ($k = 3$)

## Provenance
- **Exam Context:** BECE Mathematics 2002 Paper 1, Question 29
- **Question ID:** `Q_7a361bc4c302`
- **Topic:** Geometry and Transformation / Enlargement and Similar Shapes
- **Curriculum Indicator:** B8.3.2.1 / B9.3.2.1 (Determine scale factors of enlargement and find missing lengths in similar triangles)

## Geometric & Visual Specification
- **Base Line $TR$:**
  - $T(0, 0)$ to $R(12, 0)$, horizontal baseline.
  - Subdivided at point $Q(8, 0)$ such that $|TQ| = 8\,\text{cm}$ and $|QR| = 4\,\text{cm}$ ($|TR| = 12\,\text{cm}$).
- **Vertical Perpendiculars:**
  - Left vertical leg $ST$: from $T(0, 0)$ to $S(0, 7.2)$.
  - Intermediate vertical segment $PQ$: from $Q(8, 0)$ to $P(8, 2.4)$.
- **Hypotenuse Alignment:**
  - Line from $S(0, 7.2)$ to $R(12, 0)$ passes continuously through point $P(8, 2.4)$ with uniform slope $m = -0.60$.
  - Triangle $\Delta PQR$ is an enlargement of $\Delta STR$ about center $R$ with linear scale factor $k = \frac{|TR|}{|QR|} = \frac{12}{4} = 3$.
  - Corresponding altitude $|ST| = 3 \times |PQ| = 3 \times 2.4 = 7.2\,\text{cm}$.
- **Labels & Callouts:**
  - Vertices: **S**, **T**, **P**, **Q**, **R** in bold sans-serif (`\huge\sffamily\bfseries`).
  - Dimension `8cm` centered beneath $TQ$ at $(4, -0.45)$.
  - Dimension `4cm` centered beneath $QR$ at $(10, -0.45)$.
  - Dimension `2.4cm` positioned to the left of segment $PQ$ at $(8, 1.2)$.

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** Linear scale factors demand collinear alignment ($S$, $P$, $R$ strictly collinear). TikZ's coordinate geometry guarantees exact geometric slope and zero alignment breaks between the inner and outer triangles.

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}

\begin{document}
\begin{tikzpicture}[scale=0.85]
    % Coordinate definitions matching scale factor k = 3
    \coordinate (T) at (0, 0);
    \coordinate (Q) at (8, 0);
    \coordinate (R) at (12, 0);
    \coordinate (S) at (0, 7.2);
    \coordinate (P) at (8, 2.4);
    
    % Draw large outer triangle STR
    \draw[line width=1.3pt] (T) -- (R) -- (S) -- cycle;
    
    % Draw internal vertical segment PQ
    \draw[line width=1.2pt] (P) -- (Q);
    
    % Vertices labels
    \node[above=2pt, font=\huge\sffamily\bfseries] at (S) {S};
    \node[below=4pt, font=\huge\sffamily\bfseries] at (T) {T};
    \node[above=4pt, font=\huge\sffamily\bfseries] at (P) {P};
    \node[below=4pt, font=\huge\sffamily\bfseries] at (Q) {Q};
    \node[below=4pt, font=\huge\sffamily\bfseries] at (R) {R};
    
    % Dimension labels
    \node[below=5pt, font=\Large\sffamily\bfseries] at (4.0, 0) {8cm};
    \node[below=5pt, font=\Large\sffamily\bfseries] at (10.0, 0) {4cm};
    \node[left=4pt, font=\Large\sffamily\bfseries] at (8.0, 1.2) {2.4cm};
    
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other similar triangle problems:
1. **Arbitrary Scale Factor $k$:** Set $|QR| = d$, $|TR| = k \cdot d$, $|PQ| = h$, and $|ST| = k \cdot h$.
2. **Right-Angle Markers:** Add square markers at $T$ and $Q$ using `\draw (0, 0.4) -- (0.4, 0.4) -- (0.4, 0);` and `\draw (8, 0.4) -- (8.4, 0.4) -- (8.4, 0);`.
3. **Parallel Indicator Arrows:** Add corresponding arrows on $ST$ and $PQ$ to indicate $ST \parallel PQ$.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] Hypotenuse line $SR$ passes exactly through intermediate vertex $P$.
- [x] $ST$ and $PQ$ are strictly perpendicular to baseline $TR$.
- [x] Dimension text sizes and spacing prevent line collision.
- [x] Proportions $8 : 4 = 2 : 1$ and $7.2 : 2.4 = 3 : 1$ are mathematically exact.
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
