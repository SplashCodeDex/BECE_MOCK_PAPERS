---
name: diagram-16-isosceles-exterior-angle
description: Instructions, geometric specs, and TikZ code to draw authentic BECE isosceles triangles with congruence ticks, exterior angle arcs, and collinear baseline extensions.
---

# Diagram 16: Isosceles Triangle with Exterior Angle Theorem

## Provenance
- **Exam Context:** BECE Mathematics 1995 Paper 1, Question 38
- **Question ID:** `Q_66181d91498c`
- **Topic:** Geometry and Measurement / Properties of Triangles (Isosceles, Exterior Angles)
- **Curriculum Indicator:** B7.3.1.1 / B8.3.1.1 (Calculate unknown angles using base angle congruence and exterior angle theorem)

## Geometric & Visual Specification
- **Base Line ($DBC$):**
  - Collinear horizontal segment from $D(-3.4, 0)$ through vertex $B(0, 0)$ to vertex $C(3.2, 0)$, line width $1.3\,\text{pt}$.
- **Isosceles Triangle ($\Delta ABC$):**
  - Base length $|BC| = 3.2\,\text{cm}$.
  - Side congruence: $|AB| = |AC|$ marked with perpendicular congruence tick marks at side midpoints.
  - Exterior angle at $B$: $\angle ABD = 108^\circ \implies \angle ABC = 180^\circ - 108^\circ = 72^\circ$.
  - By base angle theorem, $\angle ACB = 72^\circ$.
  - Apex coordinates $A$: Midpoint $x = 1.6\,\text{cm}$, altitude $h = 1.6 \times \tan 72^\circ \approx 4.92\,\text{cm}$.
  - Apex angle: $y^\circ = 180^\circ - 2(72^\circ) = 36^\circ$.
- **Angle Arcs & Labels:**
  - Exterior angle arc: Centered at $B(0, 0)$ from $72^\circ$ to $180^\circ$, radius $0.9\,\text{cm}$, label **108°**.
  - Apex angle arc: Centered at $A(1.6, 4.92)$ from $252^\circ$ to $288^\circ$ (span $36^\circ$), radius $1.0\,\text{cm}$, label **$y^\circ$**.
- **Typography:** Bold sans-serif vertex labels **A**, **B**, **C**, **D** (`\Large\sffamily\bfseries`).

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** Strict congruence $|AB| = |AC|$ and trigonometry ($h = 1.6 \tan 72^\circ$) ensure the drawn triangle is mathematically authentic, with congruence ticks strictly perpendicular to the respective sides.

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=15pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc}

\begin{document}
\begin{tikzpicture}[scale=1.1]
    % Isosceles triangle with base angles 72 deg, apex angle 36 deg
    \coordinate (D) at (-3.4, 0);
    \coordinate (B) at (0, 0);
    \coordinate (C) at (3.2, 0);
    \coordinate (A) at (1.6, 4.92);
    
    % Draw extended baseline DBC
    \draw[line width=1.3pt] (D) -- (C);
    
    % Draw triangle sides AB and AC
    \draw[line width=1.3pt] (B) -- (A) -- (C);
    
    % Congruence tick marks on AB and AC
    \coordinate (MidAB) at ($(A)!0.5!(B)$);
    \coordinate (MidAC) at ($(A)!0.5!(C)$);
    \draw[line width=1.1pt] ($(MidAB) + ({72+90}:0.22)$) -- ($(MidAB) + ({72-90}:0.22)$);
    \draw[line width=1.1pt] ($(MidAC) + ({108+90}:0.22)$) -- ($(MidAC) + ({108-90}:0.22)$);
    
    % Exterior angle 108 deg at B (72 to 180)
    \draw[line width=0.9pt] ($(B) + (72:0.9)$) arc (72:180:0.9);
    \node[font=\bfseries] at (-0.45, 0.38) {$108^\circ$};
    
    % Apex angle y deg at A (252 to 288)
    \draw[line width=0.9pt] ($(A) + (252:1.0)$) arc (252:288:1.0);
    \node[font=\large\bfseries] at (1.6, 4.35) {$y^\circ$};
    
    % Vertices labels in bold sans-serif
    \node[above=3pt, font=\Large\sffamily\bfseries] at (A) {A};
    \node[below=4pt, font=\Large\sffamily\bfseries] at (B) {B};
    \node[right=3pt, font=\Large\sffamily\bfseries] at (C) {C};
    \node[left=3pt, font=\Large\sffamily\bfseries] at (D) {D};
    
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other triangle angle questions:
1. **Arbitrary Exterior Angle $\theta$:** Set base angle $\alpha = 180^\circ - \theta$, apex angle $y = 180^\circ - 2\alpha$, and apex height $h = \frac{|BC|}{2} \tan\alpha$.
2. **Equilateral Specialization:** Set base angle to $60^\circ$, apex to $60^\circ$, and place tick marks on all 3 sides.
3. **Right Isosceles Triangle:** Set base angles to $45^\circ$, apex to $90^\circ$, and add a right-angle square symbol at apex $A$.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] Baseline $DBC$ is strictly horizontal with no slope discontinuities.
- [x] Triangle $\Delta ABC$ is symmetrical across the vertical centerline $x = 1.6$.
- [x] Congruence tick marks are centered on the legs and strictly perpendicular.
- [x] Angular values $108^\circ + 72^\circ = 180^\circ$ and $2(72^\circ) + 36^\circ = 180^\circ$ are conserved.
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
