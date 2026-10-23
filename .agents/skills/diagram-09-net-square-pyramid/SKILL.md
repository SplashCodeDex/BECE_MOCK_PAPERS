---
name: diagram-09-net-square-pyramid
description: Instructions, geometric specs, and TikZ code to draw authentic BECE 2D nets of pyramids and prisms with exact polygonal symmetry.
---

# Diagram 09: Net of a 3D Solid (Square Pyramid)

## Provenance
- **Exam Context:** BECE Mathematics 2008 Paper 1, Question 26
- **Question ID:** `Q_d3f4b08df5e5`
- **Topic:** Geometry and Measurement / 3D Geometry and Nets of Solids
- **Curriculum Indicator:** B7.3.1.2 / B8.3.1.2 (Identify and construct 2D nets of prisms and pyramids)

## Geometric & Visual Specification
- **Base Polygon:**
  - Square base of side length $2s = 2.8\,\text{cm}$ centered at origin $(0, 0)$.
  - Vertices: $(-\s, -\s)$, $(\s, -\s)$, $(\s, \s)$, $(-\s, \s)$ with $\s = 1.4\,\text{cm}$.
- **Flap Geometry (4 Congruent Triangular Faces):**
  - Altitude of each triangular flap: $h_{\text{tri}} = 2.1\,\text{cm}$.
  - 4 symmetrical apex coordinates:
    - Top: $(0, \s + h_{\text{tri}}) = (0, 3.5)$.
    - Bottom: $(0, -\s - h_{\text{tri}}) = (0, -3.5)$.
    - Right: $(\s + h_{\text{tri}}, 0) = (3.5, 0)$.
    - Left: $(-\s - h_{\text{tri}}, 0) = (-3.5, 0)$.
  - Outer boundary forms a 4-pointed star envelope with total width and height $7.0\,\text{cm}$.
- **Line Style:** Uniform solid vector lines ($1.4\,\text{pt}$) for all internal fold lines and external cut boundaries.

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** 4-fold rotational symmetry ($D_4$ group) is guaranteed by parametric macro expansion `\def\s{1.4}` and `\def\htri{2.1}`, eliminating manual coordinate estimation.

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=15pt]{standalone}
\usepackage{amsmath,amssymb}

\begin{document}
\begin{tikzpicture}[scale=1.4]
    % Central square base
    \def\s{1.4} % half side of square, full base = 2.8 cm
    \def\htri{2.1} % altitude of the 4 congruent triangular faces
    
    \coordinate (BL) at (-\s, -\s);
    \coordinate (BR) at (\s, -\s);
    \coordinate (TR) at (\s, \s);
    \coordinate (TL) at (-\s, \s);
    
    % Draw central square base
    \draw[line width=1.4pt] (BL) -- (BR) -- (TR) -- (TL) -- cycle;
    
    % 4 symmetric apex points
    \coordinate (ApexTop) at (0, {\s + \htri});
    \coordinate (ApexBot) at (0, {-\s - \htri});
    \coordinate (ApexRight) at ({\s + \htri}, 0);
    \coordinate (ApexLeft) at ({-\s - \htri}, 0);
    
    % Draw 4 congruent triangular faces
    \draw[line width=1.4pt] (TL) -- (ApexTop) -- (TR);
    \draw[line width=1.4pt] (BL) -- (ApexBot) -- (BR);
    \draw[line width=1.4pt] (TR) -- (ApexRight) -- (BR);
    \draw[line width=1.4pt] (TL) -- (ApexLeft) -- (BL);
    
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other 3D solid nets:
1. **Triangular Prism Net:** Draw a central rectangle with two flanking rectangles (lateral faces) and two triangular end flaps attached to opposite sides of the central rectangle.
2. **Cylinder Net:** Draw a wide rectangle (lateral area, width $2\pi r$, height $h$) with two circular flaps (top and bottom bases, radius $r$) tangent to the upper and lower edges.
3. **Cone Net:** Draw a sector of a circle (lateral surface) with angle $\theta = \frac{r}{l} \times 360^\circ$ and a detached or tangent circle of radius $r$ at the arc perimeter.
4. **Cuboid Net:** Draw a cross or T-shaped arrangement of 6 rectangular faces.
5. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] Base is an exact square with perpendicular corners.
- [x] All 4 triangular faces are strictly congruent.
- [x] 4-fold rotational symmetry about origin $(0, 0)$.
- [x] Zero gap between square corners and triangle bases.
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
