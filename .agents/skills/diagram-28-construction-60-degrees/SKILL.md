---
name: diagram-28-construction-60-degrees
description: Replicate the authentic BECE compass and straightedge construction diagram for a 60-degree angle using TikZ.
---

# Diagram 28: Compass and Straightedge Construction of a $60^\circ$ Angle

## 1. Provenance & Curriculum Context
- **Curriculum Indicator:** `B8.3.1.2.2` / `B9.3.1.2.2` (Perform compass and straightedge constructions of basic angles: $60^\circ$, $30^\circ$, $90^\circ$, $45^\circ$)
- **Topic:** Shape and Space / Geometric Constructions
- **Mathematical Significance:** Demonstrates Euclidean construction of a fundamental $60^\circ$ angle using an equilateral triangle principle:
  1. Swing a primary arc of radius $r$ centered at vertex $O(0, 0)$ cutting the baseline at $A(r, 0)$.
  2. With the same compass radius $r$, swing an arc centered at $A$ intersecting the primary arc at $B$.
  3. Draw the straight ray from $O$ through $B$, producing an exact $60^\circ$ angle with the baseline.

---

## 2. Geometric Specifications & Coordinates
- **Baseline:** Horizontal segment from $(-1.0, 0)$ to $(4.2, 0)$.
- **Vertex $O$:** Origin $(0, 0)$ marked with solid disc.
- **Primary Arc:** Radius $r = 3.0\,\text{cm}$, swept from $0^\circ$ to $75^\circ$.
- **Base Intersection $A$:** $(3.0, 0)$ with label below.
- **Crossing Arc:** Radius $r = 3.0\,\text{cm}$ centered at $A(3.0, 0)$, swept $113^\circ$ to $127^\circ$.
- **Intersection $B$:** Exactly at $(r \cos 60^\circ, r \sin 60^\circ) = (1.5, 2.598\,\text{cm})$, with label $B$ positioned `right=12pt` in open space.
- **Constructed Ray:** Straight line with arrowhead from $O(0, 0)$ through $B$ to $(1.25 \times 1.5, 1.25 \times 2.598) \approx (1.875, 3.248)$.
- **Angle Arc:** Radius $0.8\,\text{cm}$ swept $0^\circ$ to $60^\circ$ with label $60^\circ$ centered at $(30^\circ : 1.3\,\text{cm})$.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Equilateral symmetry ($OA = OB = AB = r$) is guaranteed via exact trigonometric functions (`cos(60)`, `sin(60)`), ensuring the ray passes through the arc cross with zero visual error.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]
  % Parameters
  \def\r{3.0}     % Radius of compass opening

  % Baseline
  \draw[thick] (-1.0, 0) -- (4.2, 0);

  % Vertex O
  \coordinate (O) at (0, 0);
  \filldraw[black] (O) circle (2pt) node[below=5pt, font=\large\bfseries] {$O$};

  % Primary arc centered at O from 0 to 75 degrees
  \draw[thick] (\r, 0) arc (0:75:\r);

  % Base intersection point A
  \coordinate (A) at (\r, 0);
  \node[below=5pt, font=\normalsize] at (A) {$A$};

  % Arc centered at A(r, 0) with radius r cutting primary arc at 60 degrees
  \draw[thick] ($(A) + (113:\r)$) arc (113:127:\r);

  % Intersection point B at 60 degrees placed right of the ray with generous space
  \coordinate (B) at ({\r*cos(60)}, {\r*sin(60)});
  \node[right=12pt, font=\large] at (B) {$B$};

  % Constructed 60-degree ray from O through B
  \draw[very thick, ->] (O) -- ({1.25*\r*cos(60)}, {1.25*\r*sin(60)});

  % 60-degree angle arc and label
  \draw[thick] (0.8, 0) arc (0:60:0.8);
  \node at (30:1.3) [font=\small\bfseries] {$60^\circ$};

\end{tikzpicture}
\end{document}
```

---

## Mandatory Visual Verification Gate (Strict Agent Protocol)
Before inserting this diagram into any exam paper, worksheet, or document:
1. **Compile & Rasterize to PNG Only (Strictly No Diagram PDFs or SVGs):** Diagrams must exist and be retained ONLY as `.png` (and source `.tex`). Never output, store, commit, or convert diagrams to `.pdf` or `.svg` files (high-DPI concerns do not justify keeping SVGs; 300 DPI PNG is the sole target). When compiling standalone `.tex` via `pdflatex`, rasterize immediately to 300 DPI `.png` (e.g. using PyMuPDF / `page.get_pixmap(dpi=300)`) and immediately delete any intermediate `.pdf`, `.svg`, or temporary `.aux`/`.log` build artifacts. Diagram assets must exist strictly as `.png`.
2. **Critical Visual Inspection:** The agent MUST explicitly load and view the rendered PNG image using visual tools (such as `read_file`). Critically analyze for:
   - Text or numerical label overlaps with geometric lines, arcs, or dimension callouts.
   - Proper clearance and breathing space around vertex letters and angle symbols.
   - Orthogonality and alignment of ticks, arrows, and hatching lines.
3. **Iterate Until Flawless:** If any visual collision or imperfection is detected, adjust the TikZ coordinates or node anchors, re-render to PNG, and re-inspect until perfection is reached.
4. **Insertion Approval:** Only embed the diagram into the mock paper or teaching module after the PNG passes this critical visual inspection.

## 5. Agent Replication Guide
1. Draw baseline and establish vertex $O$.
2. Sweep primary arc of radius $r$ from $0^\circ$ to $75^\circ$.
3. With equal radius $r$, strike arc from $(r, 0)$ across $60^\circ$.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

---

## 6. Verification & Quality Checklist
- [x] Primary arc and cutting arc have identical radius $r$.
- [x] Ray passes precisely through intersection point $B(1.5, 2.598)$.
- [x] Angle arc measures exactly $60^\circ$.
- [x] Label $B$ has complete breathing clearance to the right of the ray.
- [x] Visual inspection gate passed (300 DPI PNG reviewed and verified critically).
