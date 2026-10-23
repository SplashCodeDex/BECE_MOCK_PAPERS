---
name: diagram-05-angle-bisector-construction
description: Instructions, geometric specs, and TikZ code to draw authentic BECE compass-and-ruler angle bisector constructions with exact arc intersections.
---

# Diagram 05: Geometric Construction of Angle Bisector

## Provenance
- **Exam Context:** BECE Mathematics 1990 Paper 1, Question 20
- **Question ID:** `Q_c850691b7838`
- **Topic:** Geometric Constructions / Bisecting an Angle
- **Curriculum Indicator:** B8.3.1.2 / B9.3.1.2 (Perform compass and ruler constructions of angle bisectors and perpendiculars)

## Geometric & Visual Specification
- **Initial Angle:**
  - Vertex $V$ at the origin $(0, 0)$.
  - Top arm inclined at $\theta = +24^\circ$, extending to length $4.32\,\text{cm}$.
  - Bottom arm inclined at $\theta = -24^\circ$, extending to length $4.32\,\text{cm}$.
- **Compass Marks on Arms:**
  - Points $A$ and $B$ placed at equal radius $r_{\text{arm}} = 3.2\,\text{cm}$ from $V$.
  - Perpendicular tick marks (length $0.44\,\text{cm}$) crossing each arm to indicate compass cut marks.
- **Interior Compass Arcs:**
  - Radius $r_{\text{arc}} = 2.7\,\text{cm}$ struck from centers $A$ and $B$.
  - Both arcs intersect at point $P\left(r_{\text{arm}}\cos\theta + \sqrt{r_{\text{arc}}^2 - (r_{\text{arm}}\sin\theta)^2},\; 0\right) \approx (5.14, 0)$.
  - Arc spans centered on the intersection angle with angular width $\pm 25^\circ$.
- **Bisector Ray:**
  - Straight line starting from vertex $V(0, 0)$ passing directly through arc intersection $P$ and extending slightly beyond to $x \approx 5.6\,\text{cm}$.

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** Geometric constructions require exact Euclidean circle-circle intersection equations (`\pgfmathsetmacro`) to guarantee that the compass arcs intersect precisely on the straight line drawn from the vertex.

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=15pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc}

\begin{document}
\begin{tikzpicture}[scale=1.4]
    \def\ang{24}
    \def\rarm{3.2}
    \def\rarc{2.7}
    
    \coordinate (V) at (0, 0);
    \coordinate (A) at ({\rarm*cos(\ang)}, {\rarm*sin(\ang)});
    \coordinate (B) at ({\rarm*cos(-\ang)}, {\rarm*sin(-\ang)});
    
    % The two arms of the original angle
    \draw[line width=1.1pt] (V) -- ({\rarm*1.35*cos(\ang)}, {\rarm*1.35*sin(\ang)});
    \draw[line width=1.1pt] (V) -- ({\rarm*1.35*cos(-\ang)}, {\rarm*1.35*sin(-\ang)});
    
    % Tick marks on the arms at distance rarm from vertex
    \draw[line width=0.9pt] ($(A) + ({\ang+90}:0.22)$) -- ($(A) + ({\ang-90}:0.22)$);
    \draw[line width=0.9pt] ($(B) + ({-\ang+90}:0.22)$) -- ($(B) + ({-\ang-90}:0.22)$);
    
    % Intersecting compass arcs from A and B
    \pgfmathsetmacro{\midangA}{-asin((\rarm*sin(\ang))/\rarc)}
    \pgfmathsetmacro{\midangB}{asin((\rarm*sin(\ang))/\rarc)}
    
    \draw[line width=0.9pt] ($(A) + ({\midangA - 25}:\rarc)$) arc ({\midangA - 25}:{\midangA + 25}:\rarc);
    \draw[line width=0.9pt] ($(B) + ({\midangB - 25}:\rarc)$) arc ({\midangB - 25}:{\midangB + 25}:\rarc);
    
    % Bisector line passing through vertex and the arc intersection
    \pgfmathsetmacro{\xP}{{\rarm*cos(\ang) + sqrt(\rarc*\rarc - (\rarm*sin(\ang))*(\rarm*sin(\ang)))}}
    \draw[line width=1.1pt] (V) -- ({\xP + 0.45}, 0);
    
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other construction problems:
1. **Perpendicular Bisector of Line:** Place $A(-d, 0)$ and $B(d, 0)$, strike arcs above and below the segment, and draw the vertical bisector line through both intersections.
2. **$60^\circ$ Angle Construction:** Draw horizontal baseline, strike large arc from vertex $V$ intersecting baseline at $A$, strike equal radius arc from $A$ intersecting the main arc at $B$, and connect $V$ to $B$.
3. **$30^\circ$ Angle Construction:** Construct $60^\circ$ ray, then apply this angle bisector construction between the $60^\circ$ ray and the horizontal baseline.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] Compass tick marks on arms are equidistant from vertex $V$.
- [x] Compass arcs intersect exactly along the bisector line $y = 0$.
- [x] Bisector line passes cleanly through the intersection cross.
- [x] Crisp 300 DPI PNG with zero blur or jaggedness.
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
