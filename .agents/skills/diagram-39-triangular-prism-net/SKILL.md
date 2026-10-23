---
name: diagram-39-triangular-prism-net
description: Replicate the authentic BECE 2D net diagram of a right triangular prism with dimension callouts, fold lines, and total surface area calculations using TikZ.
---

# Diagram 39: Triangular Prism 2D Net and Surface Area

## 1. Provenance & Curriculum Context
- **Curriculum Indicator:** `B7.3.1.2.1` / `B8.3.1.1.2` (Draw nets of 3D solids including triangular prisms; calculate total surface area from composite 2D faces)
- **Topic:** Solid Geometry / Nets of Solids / Triangular Prism
- **Mathematical Significance:** Demonstrates unrolling and surface mensuration of a right triangular prism:
  1. **Polyhedral Composition:**
     - 5 Faces (2 congruent right-triangular bases + 3 rectangular lateral faces).
     - 6 Vertices.
     - 9 Edges.
  2. **Base Area:** Two right-angled triangles with perpendicular legs $a = 3\,\text{cm}$ and $b = 4\,\text{cm}$:
     $$\text{Base Area} = \frac{1}{2} \times 4 \times 3 = 6\,\text{cm}^2$$
  3. **Lateral Surface Area:** Sum of three rectangular faces of common length $L = 10\,\text{cm}$:
     $$\text{LSA} = (a + b + c) \times L = (3 + 4 + 5) \times 10 = 120\,\text{cm}^2$$
  4. **Total Surface Area (TSA):**
     $$\text{TSA} = 2 \times \text{Base Area} + \text{LSA} = 2(6) + 120 = 132\,\text{cm}^2$$

---

## 2. Geometric Specifications & Coordinates
- **Dimensions:**
  - Scaled right triangle: $a = 1.8\,\text{cm}$ ($3\,\text{cm}$), $b = 2.4\,\text{cm}$ ($4\,\text{cm}$), $c = 3.0\,\text{cm}$ ($5\,\text{cm}$).
  - Prism length $L = 5.5\,\text{cm}$ ($10\,\text{cm}$).
- **Face Arrangement:**
  - Central rectangle: $[0, L] \times [0, b]$ ($4 \times 10\,\text{cm}$).
  - Top rectangle: $[0, L] \times [b, b+a]$ ($3 \times 10\,\text{cm}$).
  - Bottom rectangle: $[0, L] \times [-c, 0]$ ($5 \times 10\,\text{cm}$).
  - Triangular end flaps attached along left ($x=0$) and right ($x=L$) edges of the central rectangle.
- **Line Hierarchy:**
  - Outer boundary: Solid `very thick` lines.
  - Interior fold lines: Dashed `gray!70` lines.
- **Annotations & Right Angles:**
  - Right angle markers on both triangular flaps.
  - Dimension lines for length $L$ and widths $3, 4, 5\,\text{cm}$.
- **Summary Box:** Formal card detailing face counts, vertices, edges, and step-by-step TSA calculation.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Guarantees strict geometric closure ($a^2 + b^2 = c^2$) so the net folds with zero edge overlap or deficiency.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]

  % Dimensions (3-4-5 right triangle, length L = 5.5)
  % Scale: a = 1.8 (represents 3 cm), b = 2.4 (represents 4 cm), c = 3.0 (represents 5 cm), L = 5.5 (represents 10 cm)
  \def\a{1.8}
  \def\b{2.4}
  \def\c{3.0}
  \def\L{5.5}

  % Shading of faces
  % Lateral rectangular faces (teal!8)
  \fill[teal!8] (0, -\c) rectangle (\L, \b + \a);
  % Triangular base flaps (blue!18)
  \fill[blue!18] (0, 0) -- (-\a, 0) -- (0, \b) -- cycle;
  \fill[blue!18] (\L, 0) -- (\L + \a, 0) -- (\L, \b) -- cycle;

  % Outer boundary (solid thick lines)
  \draw[very thick] (0, \b + \a) -- (\L, \b + \a) -- (\L, \b) -- (\L + \a, 0) -- (\L, 0) -- (\L, -\c) -- (0, -\c) -- (0, 0) -- (-\a, 0) -- (0, \b) -- cycle;

  % Interior fold lines (dashed)
  \draw[thick, dashed, gray!70] (0, \b) -- (\L, \b);
  \draw[thick, dashed, gray!70] (0, 0) -- (\L, 0);
  \draw[thick, dashed, gray!70] (0, 0) -- (0, \b);
  \draw[thick, dashed, gray!70] (\L, 0) -- (\L, \b);

  % Right angle symbols on triangular flaps
  \draw[thin] (0, 0.25) -- (-0.25, 0.25) -- (-0.25, 0);
  \draw[thin] (\L, 0.25) -- (\L + 0.25, 0.25) -- (\L + 0.25, 0);

  % Face labels inside regions
  \node[font=\footnotesize\bfseries, teal!70!black] at (\L/2, \b + \a/2) {Rectangular Face $1$ ($3\,\text{cm} \times 10\,\text{cm}$)};
  \node[font=\footnotesize\bfseries, teal!70!black] at (\L/2, \b/2) {Base Rectangle ($4\,\text{cm} \times 10\,\text{cm}$)};
  \node[font=\footnotesize\bfseries, teal!70!black] at (\L/2, -\c/2) {Rectangular Face $3$ ($5\,\text{cm} \times 10\,\text{cm}$)};
  \node[font=\scriptsize\bfseries, blue!80!black] at (-0.5, 0.85) {Base};
  \node[font=\scriptsize\bfseries, blue!80!black] at (\L + 0.5, 0.85) {Base};

  % Dimension callouts
  % Length of prism (top dimension)
  \draw[thick, <->] (0, \b + \a + 0.4) -- (\L, \b + \a + 0.4) node[midway, above=2pt, font=\small\bfseries] {$L = 10\,\text{cm}$};
  \draw[thin, gray!60] (0, \b + \a) -- (0, \b + \a + 0.55);
  \draw[thin, gray!60] (\L, \b + \a) -- (\L, \b + \a + 0.55);

  % Side lengths on left triangular flap
  \node[below=2pt, font=\footnotesize\bfseries] at (-\a/2, 0) {$3\,\text{cm}$};
  \node[left=3pt, font=\footnotesize\bfseries, fill=white, inner sep=1pt] at (-0.95, 1.25) {$5\,\text{cm}$};

  % Central rectangle width
  \draw[thick, <->] (-\a - 0.5, 0) -- (-\a - 0.5, \b) node[midway, left=2pt, font=\footnotesize\bfseries] {$4\,\text{cm}$};
  \draw[thin, gray!60] (-\a, 0) -- (-\a - 0.65, 0);
  \draw[thin, gray!60] (0, \b) -- (-\a - 0.65, \b);

  % Formula Card below
  \node[align=left, font=\small, fill=white, inner sep=5pt, draw=gray!40, rounded corners=3pt, anchor=north] at (\L/2, -\c - 0.7) {
    \textbf{Right Triangular Prism (2D Net \& Surface Area):}\\
    $\bullet$ \textbf{Number of Faces:} 5 (2 congruent triangular bases + 3 rectangular lateral faces)\\
    $\bullet$ \textbf{Number of Vertices:} 6 \quad $\bullet$ \textbf{Number of Edges:} 9\\
    $\bullet$ \textbf{Base Area (each):} $\frac{1}{2} \times 4 \times 3 = 6\,\text{cm}^2$\\
    $\bullet$ \textbf{Total Surface Area (TSA):} $2 \times \text{Base Area} + (a + b + c) \times L$\\
    \hspace*{38mm} $= 2(6) + (3 + 4 + 5) \times 10 = 12 + 120 = 132\,\text{cm}^2$
  };

\end{tikzpicture}
\end{document}
```

---

## 5. Visual Quality & Formatting Rules
- **No PDF / SVG Output:** Only the `.tex` source and 300 DPI `.png` raster render must be stored.
- **Fold vs Boundary Distinction:** Solid thick boundary line with dashed interior fold lines.
