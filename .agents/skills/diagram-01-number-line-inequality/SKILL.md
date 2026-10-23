---
name: diagram-01-number-line-inequality
description: Instructions, geometric specs, and TikZ code to draw authentic BECE number line inequalities with open/closed circles and rays.
---

# Diagram 01: Number Line Inequality ($x \le -3$)

## Provenance
- **Exam Context:** BECE Mathematics 2002 Paper 1, Question 24
- **Question ID:** `Q_509d2c187914`
- **Topic:** Real Number System / Linear Inequalities in One Variable
- **Curriculum Indicator:** B8.1.2.1 / B9.1.2.1 (Representing solution sets of linear inequalities on a number line)

## Geometric & Visual Specification
- **Horizontal Axis:** Double-ended arrow line representing the real number continuum.
- **Tick Range:** Discrete integer ticks from $-6$ to $0$ with standard 1-unit spacing ($1.2\,\text{cm}$ in TikZ scale).
- **Tick Marks:** Vertical line segments spanning from $y = -0.15$ to $y = +0.15$ with integer math labels directly below.
- **Inequality Representation:**
  - Anchor point: $x = -3$.
  - Vertical stem extending from axis $(x=-3, y=0)$ up to elevation $y = 0.9$.
  - Boundary circle: Solid filled disc (radius $3.2\,\text{pt}$) at $(-3, 0.9)$, denoting inclusive inequality ($\le$ or $\ge$).
  - Directed ray: Horizontal line from $(-3, 0.9)$ directed leftward with `Stealth` arrowhead to $x = -6.6$, denoting numbers less than or equal to $-3$.

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** TikZ provides precise coordinate math, native LaTeX font rendering for negative numerals (proper minus sign $-$ rather than hyphen-minus), consistent tick spacing via `\foreach`, and standard `Stealth` arrowheads.

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{arrows.meta}

\begin{document}
\begin{tikzpicture}[>=Stealth, scale=1.2]
    % Number line with double arrows
    \draw[thick, <->] (-6.8, 0) -- (0.8, 0);
    
    % Integer ticks and labels
    \foreach \x in {-6,-5,-4,-3,-2,-1,0} {
        \draw[thick] (\x, 0.15) -- (\x, -0.15) node[below=3pt, font=\small] {$\x$};
    }
    
    % Stem and inequality boundary point
    \draw[very thick] (-3, 0) -- (-3, 0.9);
    \filldraw[black] (-3, 0.9) circle (3.2pt);
    
    % Directional ray pointing left for x <= -3
    \draw[very thick, ->] (-3, 0.9) -- (-6.6, 0.9);
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other inequality types:
1. **Strict Inequality ($<$ or $>$):** Replace `\filldraw[black]` with `\filldraw[fill=white, draw=black, thick]` to produce an open circle.
2. **Rightward Ray ($x \ge a$ or $x > a$):** Change ray target to rightwards (e.g., `\draw[very thick, ->] (a, 0.9) -- (max_x, 0.9);`).
3. **Bounded Interval ($a < x \le b$):** Place two stems at $a$ and $b$ (one open, one closed) and connect with a horizontal bar segment between $(a, 0.9)$ and $(b, 0.9)$.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] Minus signs formatted as mathematical minus (not hyphen).
- [x] Tick marks strictly perpendicular to the axis line.
- [x] Solid fill indicates inclusive inequality $\le$.
- [x] High-contrast black on transparent/white background.
- [x] Crisp 300 DPI output with zero pixelation.
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
