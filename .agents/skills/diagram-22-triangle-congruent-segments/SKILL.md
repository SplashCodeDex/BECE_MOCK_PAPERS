---
name: diagram-22-triangle-congruent-segments
description: Replicate the authentic BECE geometric diagram of composite equilateral and isosceles triangles with congruent segments and angle x using TikZ.
---

# Diagram 22: Composite Triangle with Congruent Segments & Unknown Angle $x$

## 1. Provenance & Pedagogical Context
- **Source Question:** `Q_6d000f0ad440` / `p476_2777.jpeg`
- **BECE Past Paper:** BECE Mathematics Past Paper (Plane Geometry & Triangle Angle Theorems)
- **Question:** *"In the diagram below, $|AE| = |ED| = |DC| = |CE|$. Calculate the size of the angle marked x."*
  - A. $150^\circ$
  - B. $120^\circ$
  - **C. $90^\circ$** (Correct)
  - D. $60^\circ$
  - E. $30^\circ$
- **Mathematical Significance:**
  1. Since $|ED| = |DC| = |CE|$, $\triangle EDC$ is equilateral $\implies \angle DEC = \angle ECD = \angle CDE = 60^\circ$.
  2. On straight line $AD$, $\angle AEC = 180^\circ - 60^\circ = 120^\circ$.
  3. In isosceles $\triangle AEC$ ($|AE| = |CE|$), base angles are $\angle EAC = \angle ECA = \frac{180^\circ - 120^\circ}{2} = 30^\circ$.
  4. On straight line $BD$, $\angle BCD = 180^\circ \implies x = 180^\circ - \angle ECD - \angle ECA = 180^\circ - 60^\circ - 30^\circ = 90^\circ$.

---

## 2. Geometric Specifications & Coordinates
- **Base Vertex $D$:** $(0, 0)$
- **Equilateral Base Vertices ($s = 3.0\,\text{cm}$):**
  - $E = (-1.5, 2.598)$ (at $120^\circ$)
  - $C = (1.5, 2.598)$ (at $60^\circ$)
- **Top Vertices:**
  - $A = (-3.0, 5.196)$ (collinear with $D-E-A$)
  - $B = (3.0, 5.196)$ (collinear with $D-C-B$)
- **Congruence Tick Marks (Single orthogonal dash of length $0.36\,\text{cm}$):**
  - Segment $AE$: midpoint $(-2.25, 3.897)$, normal direction $30^\circ/210^\circ$.
  - Segment $ED$: midpoint $(-0.75, 1.299)$, normal direction $30^\circ/210^\circ$.
  - Segment $EC$: midpoint $(0, 2.598)$, normal direction $90^\circ/270^\circ$.
  - Segment $DC$: midpoint $(0.75, 1.299)$, normal direction $150^\circ/330^\circ$.
- **Angle Arc & Label:**
  - Centered at $C(1.5, 2.598)$, radius $1.0\,\text{cm}$, swept from $60^\circ$ (ray $CB$) to $150^\circ$ (ray $CA$).
  - Label $\mathbf{x}$ placed at $(C) + (105^\circ: 0.6\,\text{cm})$.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Guarantees strict collinearity of $A-E-D$ and $B-C-D$, exact equilateral trigonometry, and perfectly orthogonal segment tick marks.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=10pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]
  % Coordinates
  \coordinate (D) at (0, 0);
  \coordinate (E) at (-1.5, 2.598);
  \coordinate (C) at (1.5, 2.598);
  \coordinate (A) at (-3.0, 5.196);
  \coordinate (B) at (3.0, 5.196);

  % Outer triangle and segments
  \draw[thick] (A) -- (B) -- (D) -- cycle;
  \draw[thick] (E) -- (C);
  \draw[thick] (A) -- (C);

  % Tick marks
  % AE tick
  \draw[thick] ($($(A)!0.5!(E)$) + (30:0.18)$) -- ($($(A)!0.5!(E)$) + (210:0.18)$);

  % ED tick
  \draw[thick] ($($(E)!0.5!(D)$) + (30:0.18)$) -- ($($(E)!0.5!(D)$) + (210:0.18)$);

  % EC tick
  \draw[thick] ($($(E)!0.5!(C)$) + (90:0.18)$) -- ($($(E)!0.5!(C)$) + (270:0.18)$);

  % DC tick
  \draw[thick] ($($(D)!0.5!(C)$) + (150:0.18)$) -- ($($(D)!0.5!(C)$) + (330:0.18)$);

  % Angle arc for x (from CB at 60 deg to CA at 150 deg)
  \draw[thick] ($(C) + (60:1.0)$) arc (60:150:1.0);
  \node at ($(C) + (105:0.6)$) {\large $\mathbf{x}$};

  % Vertex labels
  \node[left=3pt] at (A) {\large $\mathbf{A}$};
  \node[right=3pt] at (B) {\large $\mathbf{B}$};
  \node[left=3pt] at (E) {\large $\mathbf{E}$};
  \node[right=3pt] at (C) {\large $\mathbf{C}$};
  \node[below=3pt] at (D) {\large $\mathbf{D}$};

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
1. Position $D$ at the bottom, constructing $E$ and $C$ as an equilateral triangle base.
2. Extend rays $DE$ to $A$ and $DC$ to $B$ by exactly length $s$.
3. Compute perpendicular tick angles as $\theta \pm 90^\circ$ relative to the segment slope.
4. Center the angle arc at $C$ between lines $CA$ and $CB$.
5. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

---

## 6. Verification & Quality Checklist
- [x] All 4 segments $|AE|, |ED|, |DC|, |CE|$ have identical length.
- [x] Tick marks are centered and orthogonal to their segments.
- [x] Angle arc at $C$ is subtended between $CB$ and $CA$.
- [x] All vertex labels are crisp and distinct.
- [x] Visual inspection gate passed (300 DPI PNG reviewed and verified critically)
- [x] 300 DPI high-definition vector rendering.
