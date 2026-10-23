---
name: diagram-24-pythagoras-triangle
description: Replicate the authentic BECE right-angled triangle Pythagoras theorem diagram with 5-12-13 proportions and dimension callout arrows using TikZ.
---

# Diagram 24: Right-Angled Triangle Pythagoras Theorem ($5-12-13$)

## 1. Provenance & Pedagogical Context
- **Source Question:** `Q_cefd67e8a9c8` / `p325_2193.jpeg`
- **BECE Past Paper:** BECE Mathematics Past Paper (Pythagorean Theorem & Right Triangle Geometry)
- **Question:** *"In the diagram, MNO is a right-angled triangle. |MO| = 13cm and |MN| is 5cm. Find the value of x."*
  - A. $3$
  - B. $4$
  - C. $8$
  - **D. $12$** (Correct)
  - E. $18$
- **Mathematical Significance:** Direct application of the Pythagorean theorem:
  $$|MO|^2 = |MN|^2 + |NO|^2 \implies 13^2 = 5^2 + x^2 \implies 169 = 25 + x^2 \implies x^2 = 144 \implies x = 12\,\text{cm}$$

---

## 2. Geometric Specifications & Coordinates
- **Vertices:**
  - $N(0, 0)$: Right-angled vertex at bottom-left.
  - $M(0, 3.0)$: Top vertex of vertical leg (representing $5\,\text{cm}$).
  - $O(7.2, 0)$: Right vertex of horizontal leg (representing $x = 12\,\text{cm}$).
  - Hypotenuse $MO$ length $= 7.8\,\text{cm}$ (representing $13\,\text{cm}$, preserving the exact $5 : 12 : 13$ physical aspect ratio).
- **Right Angle Symbol:** Crisp $0.38\,\text{cm} \times 0.38\,\text{cm}$ square at $N$.
- **Dimension Lines (Double-headed `Stealth` arrows):**
  - Leg $MN$: Vertical arrow from $(-0.55, 0.05)$ to $(-0.55, 2.95)$, labeled $\mathbf{5cm}$ on left.
  - Leg $NO$: Horizontal arrow from $(0.05, -0.45)$ to $(7.15, -0.45)$, labeled $\boldsymbol{x}$ below.
  - Hypotenuse $MO$: Slanted arrow parallel to hypotenuse from $(0.35, 3.15)$ to $(7.35, 0.25)$, with horizontal label $\mathbf{13cm}$ cleanly floating above at $(4.0, 2.3)$.
- **Vertex Labels:** Bold serif $\mathbf{M}, \mathbf{N}, \mathbf{O}$ positioned outside all dimension vectors.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Ensures exact $5:12:13$ aspect ratio scaling, orthogonal dimension arrow offsets, and collision-free label typography.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=10pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]
  % Coordinates for exact 5:12:13 ratio (MN=3.0, NO=7.2, MO=7.8)
  \coordinate (N) at (0, 0);
  \coordinate (M) at (0, 3.0);
  \coordinate (O) at (7.2, 0);

  % Triangle boundary
  \draw[thick] (N) -- (M) -- (O) -- cycle;

  % Right-angle square at N
  \draw[thick] (0, 0.38) -- (0.38, 0.38) -- (0.38, 0);

  % Left vertical dimension line (5cm)
  \draw[{Stealth[length=6pt, width=5pt]}-{Stealth[length=6pt, width=5pt]}, thick] (-0.55, 0.05) -- (-0.55, 2.95);
  \node[left=3pt] at (-0.55, 1.5) {\Large $\mathbf{5cm}$};

  % Bottom horizontal dimension line (x)
  \draw[{Stealth[length=6pt, width=5pt]}-{Stealth[length=6pt, width=5pt]}, thick] (0.05, -0.45) -- (7.15, -0.45);
  \node[below=2pt] at (3.6, -0.45) {\Large $\boldsymbol{x}$};

  % Hypotenuse dimension line
  \coordinate (Mdim) at (0.35, 3.15);
  \coordinate (Odim) at (7.35, 0.25);
  \draw[{Stealth[length=6pt, width=5pt]}-{Stealth[length=6pt, width=5pt]}, thick] (Mdim) -- (Odim);

  % Horizontal label 13cm placed above the hypotenuse arrow
  \node at (4.0, 2.3) {\Large $\mathbf{13cm}$};

  % Vertex labels
  \node[above=4pt] at (M) {\huge $\mathbf{M}$};
  \node[below left=2pt] at (-0.05, -0.05) {\huge $\mathbf{N}$};
  \node[right=4pt] at (O) {\huge $\mathbf{O}$};

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
1. Set coordinates proportionally to $5, 12, 13$.
2. Maintain right angle square indicator at $(0, 0)$.
3. Offset dimension lines perpendicular to sides to prevent overlap.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

---

## 6. Verification & Quality Checklist
- [x] Exact right angle at vertex $N$.
- [x] $5:12:13$ aspect ratio strictly respected.
- [x] Dimension lines parallel to sides with dual-ended arrows.
- [x] Labels $M, N, O, 5\text{cm}, 13\text{cm}, x$ are crisp with no text collisions.
- [x] Visual inspection gate passed (300 DPI PNG reviewed and verified critically)
- [x] 300 DPI resolution raster render.
