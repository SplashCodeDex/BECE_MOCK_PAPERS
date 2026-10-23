---
name: diagram-29-construction-45-degrees
description: Replicate the authentic BECE compass and straightedge construction diagram for a 45-degree angle via bisection of a right angle using TikZ.
---

# Diagram 29: Compass and Straightedge Construction of a $45^\circ$ Angle

## 1. Provenance & Curriculum Context
- **Curriculum Indicator:** `B8.3.1.2.2` / `B9.3.1.2.2` (Perform compass and straightedge constructions of basic angles: $60^\circ$, $30^\circ$, $90^\circ$, $45^\circ$)
- **Topic:** Shape and Space / Geometric Constructions
- **Mathematical Significance:** Demonstrates Euclidean construction of a $45^\circ$ angle by bisecting a constructed $90^\circ$ right angle:
  1. Set up a $90^\circ$ perpendicular ray at vertex $O(0, 0)$.
  2. Swing a base quadrant arc of radius $r$ centered at $O$, intersecting the baseline at $A(r, 0)$ and the vertical arm at $D(0, r)$.
  3. Using compass radius $R$, swing intersecting arcs from $A$ and $D$ crossing at apex $E$ along the $45^\circ$ bisector direction.
  4. Draw the straight ray from $O$ through $E$, establishing an exact $45^\circ$ angle.

---

## 2. Geometric Specifications & Coordinates
- **Baseline:** Horizontal segment from $(-1.0, 0)$ to $(4.2, 0)$.
- **Vertex $O$:** Origin $(0, 0)$ with solid disc and right-angle indicator $(0.35 \times 0.35\,\text{cm})$.
- **Perpendicular Guideline:** Vertical dashed segment from $(0, 0)$ to $(0, 3.8\,\text{cm})$.
- **Quadrant Arc:** Radius $r = 3.0\,\text{cm}$, swept from $0^\circ$ to $90^\circ$ terminating at $D(0, 3.0)$.
- **Intersection Points on Arms:** $A(3.0, 0)$ on baseline and $D(0, 3.0)$ on perpendicular line.
- **Bisection Arcs:**
  - Radius $R = 3.2\,\text{cm}$.
  - Apex distance $d = r \cos 45^\circ + \sqrt{R^2 - (r \sin 45^\circ)^2} \approx 4.514\,\text{cm}$.
  - Apex coordinates: $E(d \cos 45^\circ, d \sin 45^\circ) \approx (3.192, 3.192\,\text{cm})$.
  - Arc 1 centered at $A(3.0, 0)$ swept $\pm 8^\circ$ around $E$.
  - Arc 2 centered at $D(0, 3.0)$ swept from $-8^\circ$ to $+4^\circ$ around $E$.
- **Constructed Ray:** Directed ray from $O(0, 0)$ through $E$ to $(1.12 \times 3.192, 1.12 \times 3.192) \approx (3.575, 3.575)$.
- **Angle Arc:** Radius $1.0\,\text{cm}$ swept $0^\circ$ to $45^\circ$ with label $45^\circ$ at $(22.5^\circ : 1.55\,\text{cm})$.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Guarantees exact angular bisection ($\theta = 45.0^\circ$) via trigonometric calculation of apex $E$, ensuring the ray passes through the arc cross without approximation error.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]
  % Parameters
  \def\r{3.0}     % Radius of base quadrant arc
  \def\R{3.2}     % Radius of bisector arcs
  
  % Baseline
  \draw[thick] (-1.0, 0) -- (4.2, 0);

  % Vertex O
  \coordinate (O) at (0, 0);
  \filldraw[black] (O) circle (2pt) node[below=5pt, font=\large\bfseries] {$O$};

  % Perpendicular 90-degree dashed guideline
  \draw[thick, dashed] (0, 0) -- (0, 3.8);
  \draw[thick] (0, 0.35) -- (0.35, 0.35) -- (0.35, 0); % Right angle symbol

  % Quadrant arc centered at O from 0 to exactly 90 degrees
  \draw[thick] (\r, 0) arc (0:90:\r);

  % Intersections on arms: A on baseline, D on 90-degree vertical
  \coordinate (A) at (\r, 0);
  \coordinate (D) at (0, \r);
  \node[below=5pt, font=\normalsize] at (A) {$A$};
  \node[left=6pt, font=\normalsize] at (D) {$D$};

  % Bisector crossing arcs from A(r, 0) and D(0, r)
  \pgfmathsetmacro{\dmid}{\r*cos(45)}
  \pgfmathsetmacro{\h}{sqrt(\R*\R - (\r*sin(45))*(\r*sin(45)))}
  \pgfmathsetmacro{\dtotal}{\dmid + \h}
  \coordinate (E) at ({\dtotal*cos(45)}, {\dtotal*sin(45)});

  % Arc from A(r, 0) through E
  \pgfmathsetmacro{\angA}{atan2(\dtotal*sin(45), \dtotal*cos(45) - \r)}
  \draw[thick] ($(A) + ({\angA - 8}:\R)$) arc ({\angA - 8}:{\angA + 8}:\R);

  % Arc from D(0, r) through E
  \pgfmathsetmacro{\angD}{atan2(\dtotal*sin(45) - \r, \dtotal*cos(45))}
  \draw[thick] ($(D) + ({\angD - 8}:\R)$) arc ({\angD - 8}:{\angD + 4}:\R);

  % Label E positioned above-right in wide open space
  \node[above right=8pt, font=\large] at (E) {$E$};

  % Constructed 45-degree ray from O through E
  \draw[very thick, ->] (O) -- ({1.12*\dtotal*cos(45)}, {1.12*\dtotal*sin(45)});

  % 45-degree angle arc and label
  \draw[thick] (1.0, 0) arc (0:45:1.0);
  \node at (22.5:1.55) [font=\small\bfseries] {$45^\circ$};

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
1. Establish origin $O$ and construct dashed $90^\circ$ perpendicular ray.
2. Sweep quadrant arc $0^\circ$ to $90^\circ$ of radius $r$.
3. Swing equal radius arcs from $(r, 0)$ and $(0, r)$ to intersect along the $45^\circ$ line.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

---

## 6. Verification & Quality Checklist
- [x] Quadrant arc connects baseline at $A$ to vertical guideline at $D$.
- [x] Crossing arcs intersect precisely on the $45^\circ$ ray.
- [x] Dashed perpendicular ray forms exact $90^\circ$ square at vertex $O$.
- [x] Label $E$ has complete clearance to the above-right of the bisection cross.
- [x] Visual inspection gate passed (300 DPI PNG reviewed and verified critically).
