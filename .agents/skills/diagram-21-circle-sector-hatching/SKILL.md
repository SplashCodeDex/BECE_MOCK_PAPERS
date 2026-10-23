---
name: diagram-21-circle-sector-hatching
description: Replicate the authentic BECE mensuration diagram of a circle sector with 60-degree central angle and horizontal hatching using TikZ.
---

# Diagram 21: Circle Minor Sector with $60^\circ$ Central Angle & Horizontal Hatching

## 1. Provenance & Pedagogical Context
- **Source Question:** `Q_d56a32870df3` / `p478_2784.jpeg`
- **BECE Past Paper:** BECE Mathematics Past Paper (Circle Geometry & Mensuration)
- **Question:** *"In the diagram, O is the centre of the circle and r is its radius. Calculate the area of the shaded region."*
  - **A. $\frac{1}{6} \pi r^2$** (Correct, since $\frac{60^\circ}{360^\circ} = \frac{1}{6}$)
  - B. $\frac{1}{5} \pi r^2$
  - C. $\frac{1}{3} \pi r^2$
  - D. $\frac{5}{6} \pi r^2$
- **Mathematical Significance:** Evaluates student understanding of the area of a circle sector:
  $$\text{Area} = \frac{\theta}{360^\circ} \times \pi r^2$$

---

## 2. Geometric Specifications & Coordinates
- **Center $O$:** $(0, 0)$
- **Radius:** $R = 2.8\,\text{cm}$
- **Radial Rays:**
  - $OA$: from $(0, 0)$ at $-128^\circ$ to the circle boundary.
  - $OB$: from $(0, 0)$ at $-52^\circ$ to the circle boundary.
- **Angle Arc & Label:**
  - Arc at radius $0.95\,\text{cm}$ from $-128^\circ$ to $-52^\circ$.
  - Label $60^\circ$ placed at $(-90^\circ: 0.52\,\text{cm})$, floating cleanly between $O$ and the arc.
- **Hatching:** Explicit horizontal vector lines spaced by $0.20\,\text{cm}$ clipped strictly to the sector region below $y \le -1.05\,\text{cm}$ to preserve pristine whitespace for the angle label.
- **Labels:** $O$ above origin, $A$ below left of boundary point, $B$ below right.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Vector clipping paths (`\clip`) allow clean horizontal hatching within circular sector boundaries without fuzzy edges or pattern scaling artifacts.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=10pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]
  \def\R{2.8}

  % Coordinates
  \coordinate (O) at (0,0);
  \coordinate (A) at (-128:\R);
  \coordinate (B) at (-52:\R);

  % Shading / horizontal hatching inside sector AOB strictly BELOW the angle arc
  \begin{scope}
    \clip (O) -- (A) arc (-128:-52:\R) -- cycle;
    \foreach \y in {-1.08,-1.28,...,-2.8} {
      \draw[semithick] (-\R-0.2, \y) -- (\R+0.2, \y);
    }
  \end{scope}

  % Sector boundary lines
  \draw[thick] (O) -- (A);
  \draw[thick] (O) -- (B);

  % Circle outline
  \draw[thick] (O) circle (\R);

  % Central angle arc and label
  \draw[thick] (-128:0.95) arc (-128:-52:0.95);
  \node at (-90:0.52) {\large $60^\circ$};

  % Center node O
  \node[above=3pt] at (O) {\large $\mathbf{O}$};

  % Sector points A and B
  \node[below left=2pt] at (A) {\large $\mathbf{A}$};
  \node[below right=2pt] at (B) {\large $\mathbf{B}$};

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
1. Create the circle path and save the sector boundary path $(O) -- (A) \text{ arc } (B) -- \text{cycle}$ for clipping.
2. Separate the central angle display from the hatching so lines never strike through the numerical angle label.
3. Use a step size of $0.20\,\text{cm}$ for the horizontal hatching lines to maintain authentic examination hatching density.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

---

## 6. Verification & Quality Checklist
- [x] Circle boundary is smooth and continuous.
- [x] Sector radii intersect circle and origin precisely.
- [x] Central angle arc and label are fully readable with no hatching interference.
- [x] Horizontal hatching conforms exactly to sector curved perimeter.
- [x] Output is high-resolution 300 DPI vector graphic.
- [x] Visual inspection gate passed (300 DPI PNG reviewed and verified critically)
