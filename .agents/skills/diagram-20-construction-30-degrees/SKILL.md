---
name: diagram-20-construction-30-degrees
description: Replicate the authentic BECE compass and straightedge construction diagram for a 30-degree angle using TikZ.
---

# Diagram 20: Compass and Straightedge Construction of a $30^\circ$ Angle

## 1. Provenance & Pedagogical Context
- **Source Question:** `Q_3d392d0a9561`
- **BECE Past Paper:** BECE Mathematics Past Paper (Compass & Straightedge Constructions)
- **Question:** *"Which of the following statements best describes the construction above?"*
  - **A. Constructing $30^\circ$** (Correct)
  - B. Constructing $60^\circ$
  - C. Constructing $120^\circ$
  - D. Constructing $135^\circ$
- **Mathematical Significance:** Demonstrates the classical two-stage geometric construction:
  1. Setting up an initial $60^\circ$ angle by swinging an arc of radius $r$ from baseline cut point $P_1(r, 0)$ across the primary arc.
  2. Bisecting the $60^\circ$ sector by swinging two intersecting arcs of equal radius $R$ from $P_1(r, 0)$ and $P_2(r \cos 60^\circ, r \sin 60^\circ)$, then connecting the vertex $O(0, 0)$ through their intersection to yield exactly $30^\circ$.

---

## 2. Geometric Specifications & Coordinates
- **Vertex $O$:** $(0, 0)$
- **Baseline:** Horizontal segment from $(-3.6, 0)$ to $(3.8, 0)$ (extending past the primary arc on the left and slightly past cut point P1 on the right)
- **Primary Arc:** Centered at $O(0, 0)$ with radius $r = 3.0\,\text{cm}$, swept from $0^\circ$ to $180^\circ$ (complete semicircle connecting to the baseline on both sides).
- **$60^\circ$ Construction Mark:** Centered at $P_1(3.0, 0)$ with radius $r = 3.0\,\text{cm}$, swept from $110^\circ$ to $130^\circ$, cleanly crossing the primary arc at $(1.5, 2.598)$.
- **Bisection Arcs:**
  - Radius $R = 4.2\,\text{cm}$.
  - Arc 1 centered at $P_1(3.0, 0)$ through intersection $X$.
  - Arc 2 centered at $P_2(1.5, 2.598)$ through intersection $X$.
  - Intersection $X$ lies exactly along the $30^\circ$ ray at distance $d = r \cos 30^\circ + \sqrt{R^2 - (r \sin 30^\circ)^2} \approx 6.521\,\text{cm}$.
- **Constructed Ray:** Straight line from $O(0, 0)$ through $X$ to $1.07 \times d$.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Essential for exact Euclidean compass constructions. TikZ's coordinate math engine (`\pgfmathsetmacro`) calculates exact trigonometric intersections, ensuring arcs cross with mathematical precision without visual offsets.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=10pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]
  % Define origin and parameters
  \coordinate (O) at (0,0);
  \def\r{3.0}     % radius of main arc
  \def\R{4.2}     % radius of bisector arcs

  % Baseline
  \draw[thick] (-3.6, 0) -- (3.8, 0);

  % Main arc from O(0,0), radius r, from 0 deg to 180 deg
  \draw[thick] (\r, 0) arc (0:180:\r);

  % Intersection on baseline: P1 = (r, 0)
  \coordinate (P1) at (\r, 0);

  % 60-degree point: P2 = (r*cos 60, r*sin 60)
  \coordinate (P2) at ({\r*cos(60)}, {\r*sin(60)});

  % Arc cutting at 60 deg, centered at P1, radius r (angle 120 deg from P1)
  \draw[thick] ($(P1) + (110:\r)$) arc (110:130:\r);

  % Bisector intersection point at 30 deg
  \pgfmathsetmacro{\dmid}{\r*cos(30)}
  \pgfmathsetmacro{\h}{sqrt(\R*\R - (\r*sin(30))*(\r*sin(30)))}
  \pgfmathsetmacro{\dtotal}{\dmid + \h}
  \coordinate (X) at ({\dtotal*cos(30)}, {\dtotal*sin(30)});

  % Arc from P1 through X (radius R)
  \pgfmathsetmacro{\angOne}{atan2(\dtotal*sin(30), \dtotal*cos(30) - \r)}
  \draw[thick] ($(P1) + ({\angOne - 11}:\R)$) arc ({\angOne - 11}:{\angOne + 11}:\R);

  % Arc from P2 through X (radius R)
  \pgfmathsetmacro{\angTwo}{atan2(\dtotal*sin(30) - \r*sin(60), \dtotal*cos(30) - \r*cos(60))}
  \draw[thick] ($(P2) + ({\angTwo - 11}:\R)$) arc ({\angTwo - 11}:{\angTwo + 11}:\R);

  % Constructed 30-degree ray through X
  \draw[thick] (O) -- ({\dtotal*1.07*cos(30)}, {\dtotal*1.07*sin(30)});

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
1. Ensure `\usetikzlibrary{calc}` is loaded.
2. Use exact compass coordinates rather than freehand arc placement.
3. Compute angles of intersecting bisector arcs via `atan2` so the cross is symmetrically centered on the constructed ray.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

---

## 6. Verification & Quality Checklist
- [x] Primary arc sweeps from $0^\circ$ to $180^\circ$ cleanly intersecting the baseline on both left and right.
- [x] $60^\circ$ tick mark centered precisely on the main arc at $60^\circ$.
- [x] Crossing bisector arcs intersect exactly on the $30^\circ$ ray.
- [x] Constructed ray extends slightly past the intersection cross.
- [x] High-resolution 300 DPI vector clarity with zero raster artifacts.
- [x] Visual inspection gate passed (300 DPI PNG reviewed and verified critically)
