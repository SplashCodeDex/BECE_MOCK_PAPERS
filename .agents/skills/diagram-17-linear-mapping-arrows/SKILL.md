---
name: diagram-17-linear-mapping-arrows
description: Instructions, geometric specs, and TikZ code to draw authentic BECE linear mapping diagrams with vertical mapping arrows and column alignment.
---

# Diagram 17: Linear Function Mapping and Arrow Diagram

## Provenance
- **Exam Context:** BECE Mathematics 2013 Paper 1, Question 9
- **Question ID:** `Q_b346cac44e5b`
- **Topic:** Patterns and Relationships / Linear Functions and Mappings
- **Curriculum Indicator:** B7.2.2.1 / B8.2.2.1 (Determine the rule of a linear mapping $x \to ax + b$)

## Geometric & Visual Specification
- **Column Array Layout:**
  - 6 evenly spaced vertical columns with horizontal pitch $\Delta x = 1.6\,\text{cm}$.
  - Top row (Domain values): $x \in \{1, 2, 3, 4, 5, x\}$ at elevation $y = 1.2\,\text{cm}$.
  - Bottom row (Co-domain values): $y \in \{5, 8, 11, 14, 17, y\}$ at elevation $y = -0.4\,\text{cm}$.
- **Directed Relation Arrows:**
  - Vertical downward vector segment in each column from $y = 0.8\,\text{cm}$ down to $y = 0.0\,\text{cm}$.
  - Arrowhead style: `Stealth` arrowheads ($1.3\,\text{pt}$ line width).
- **Rule Verification:**
  - First difference $\Delta y = 8 - 5 = 3 \implies a = 3$.
  - Constant term: $c = y_1 - 3(x_1) = 5 - 3(1) = 2$.
  - Rule: $y = 3x + 2$ (or $x \to 3x + 2$).

## Tool Selection Rationale
- **Tool Used:** **LaTeX / TikZ**
- **Rationale:** Mapping columns require strict horizontal alignment and identical vertical arrow lengths across all terms. TikZ's `\foreach` loop automates column placement with zero positioning jitter.

## Exact Reproducible Source Code
```latex
\documentclass[tikz,border=15pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{arrows.meta}

\begin{document}
\begin{tikzpicture}[>=Stealth, scale=1.2]
    % Mapping diagram columns
    \foreach \topval/\botval/\i in {1/5/0, 2/8/1.6, 3/11/3.2, 4/14/4.8, 5/17/6.4, x/y/8.0} {
        % Top element (domain)
        \node[font=\huge\bfseries] at (\i, 1.2) {$\topval$};
        % Downward arrow
        \draw[line width=1.3pt, ->] (\i, 0.8) -- (\i, 0.0);
        % Bottom element (co-domain)
        \node[font=\huge\bfseries] at (\i, -0.4) {$\botval$};
    }
\end{tikzpicture}
\end{document}
```

## Agent Replication Guide
To adapt this diagram for other mapping problems:
1. **Oval Set Mapping:** Wrap domain elements in a left vertical ellipse and co-domain elements in a right vertical ellipse, with curved or diagonal arrows connecting specific elements.
2. **Missing Middle Term:** Replace a specific numeral in the bottom row with a question mark `$?$` or variable `$k$`.
3. **Quadratic Mapping ($x \to x^2$):** Change co-domain list to $\{1, 4, 9, 16, 25, y\}$ with rule $y = x^2$.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

## Quality Verification Checklist
- [x] All 6 columns are horizontally equidistant.
- [x] Vertical arrows are parallel and of uniform length.
- [x] Variables $x$ and $y$ are formatted in math italic.
- [x] Common difference $\Delta y = 3$ is consistent across all consecutive pairs.
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
