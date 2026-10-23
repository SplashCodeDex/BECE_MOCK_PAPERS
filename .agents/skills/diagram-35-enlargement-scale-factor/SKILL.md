---
name: diagram-35-enlargement-scale-factor
description: Replicate the authentic BECE transformation diagram showing geometric enlargement with a center of enlargement and scale factor k on a Cartesian grid using TikZ.
---

# Diagram 35: Geometric Enlargement on a Cartesian Grid

## 1. Provenance & Curriculum Context
- **Curriculum Indicator:** `B9.3.3.1.2` (Enlarge shapes with a given scale factor and center of enlargement, determining image coordinates and area/linear scale factors)
- **Topic:** Position and Transformation / Enlargement
- **Mathematical Significance:** Demonstrates geometric enlargement (dilation) in 2D Euclidean space:
  1. Dilation from center $O(0,0)$ by scale factor $k$ maps each vertex $(x, y) \longrightarrow (kx, ky)$.
  2. For $k = 2$:
     $$A(1, 1) \to A'(2, 2),\quad B(3, 1) \to B'(6, 2),\quad C(1, 2) \to C'(2, 4)$$
  3. All corresponding vertices lie on concurrent projection rays originating from the center of enlargement $O$.
  4. Linear dimensions scale by $k$: $\frac{|A'B'|}{|AB|} = \frac{4}{2} = 2$.
  5. Area scales by $k^2$: $\frac{\text{Area}(\triangle A'B'C')}{\text{Area}(\triangle ABC)} = k^2 = 4$.

---

## 2. Geometric Specifications & Coordinates
- **Grid Extent:** $[-1.2, 7.5] \times [-1.2, 5.5]$ with $1.0\,\text{cm}$ step size in `gray!25`.
- **Axes:** $x$-axis from $-1.5$ to $7.8$; $y$-axis from $-1.5$ to $5.8$ with directed arrowheads.
- **Center of Enlargement:** $O(0,0)$ with circular dot marker.
- **Object $\triangle ABC$:**
  - $A(1, 1)$, $B(3, 1)$, $C(1, 2)$ filled with `blue!20`.
- **Image $\triangle A'B'C'$:**
  - $A'(2, 2)$, $B'(6, 2)$, $C'(2, 4)$ filled with `teal!18`.
- **Projection Rays:** Dashed lines (`purple!80!black`) emanating from $O$ passing through $A \to A'$, $B \to B'$, and $C \to C'$.
- **Properties Callout Box:** Anchored in Quadrant I $(x=3.8, y=5.3)$ detailing center, scale factor $k$, side ratio $k$, and area ratio $k^2$.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Guarantees strict ray collinearity ($O-A-A'$, $O-B-B'$, $O-C-C'$) and clean rendering without raster artifacts.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]
  % Grid
  \draw[step=1cm, gray!25, thin] (-1.2, -1.2) grid (7.5, 5.5);

  % Axes
  \draw[thick, ->] (-1.5, 0) -- (7.8, 0) node[right, font=\normalsize] {$x$};
  \draw[thick, ->] (0, -1.5) -- (0, 5.8) node[above, font=\normalsize] {$y$};

  % Origin
  \node[below left=2pt, font=\small] at (0, 0) {$O$};

  % Integer ticks on x-axis
  \foreach \x in {-1,1,2,3,4,5,6,7} {
    \draw[thick] (\x, 0.1) -- (\x, -0.1);
    \node[below=3pt, font=\footnotesize, fill=white, inner sep=1pt] at (\x, -0.1) {$\x$};
  }
  % Integer ticks on y-axis
  \foreach \y in {-1,1,2,3,4,5} {
    \draw[thick] (0.1, \y) -- (-0.1, \y);
    \node[left=3pt, font=\footnotesize, fill=white, inner sep=1pt] at (-0.1, \y) {$\y$};
  }

  % Coordinates
  % Center of Enlargement
  \coordinate (O) at (0, 0);

  % Pre-image triangle ABC
  \coordinate (A) at (1, 1);
  \coordinate (B) at (3, 1);
  \coordinate (C) at (1, 2);

  % Image triangle A'B'C' (scale factor k = 2)
  \coordinate (A1) at (2, 2);
  \coordinate (B1) at (6, 2);
  \coordinate (C1) at (2, 4);

  % Projection rays from center O through object vertices to image vertices
  \draw[thick, dashed, purple!80!black] (O) -- (2.5, 2.5);
  \draw[thick, dashed, purple!80!black] (O) -- (6.6, 2.2);
  \draw[thick, dashed, purple!80!black] (O) -- (2.3, 4.6);

  % Image triangle A'B'C' (drawn first so object sits crisply)
  \draw[very thick, fill=teal!18] (A1) -- (B1) -- (C1) -- cycle;
  \filldraw[black] (A1) circle (2pt) node[below right=3pt, font=\footnotesize\bfseries, fill=white, inner sep=1pt] {$A'(2,2)$};
  \filldraw[black] (B1) circle (2pt) node[above=4pt, font=\footnotesize\bfseries, fill=white, inner sep=1pt] {$B'(6,2)$};
  \filldraw[black] (C1) circle (2pt) node[above left=3pt, font=\footnotesize\bfseries, fill=white, inner sep=1pt] {$C'(2,4)$};

  % Object triangle ABC
  \draw[very thick, fill=blue!20] (A) -- (B) -- (C) -- cycle;
  \filldraw[black] (A) circle (2pt) node[below=4pt, font=\footnotesize\bfseries, fill=white, inner sep=1pt] {$A(1,1)$};
  \filldraw[black] (B) circle (2pt) node[below=4pt, font=\footnotesize\bfseries, fill=white, inner sep=1pt] {$B(3,1)$};
  \filldraw[black] (C) circle (2pt) node[above=5pt, font=\footnotesize\bfseries, fill=white, inner sep=1pt] {$C(1,2)$};

  % Center point marker
  \filldraw[black] (O) circle (2pt);

  % Annotations block
  \node[align=left, font=\footnotesize, fill=white, inner sep=3pt, draw=gray!40, rounded corners=2pt, anchor=north west] at (3.8, 5.3) {
    \textbf{Geometric Enlargement:}\\
    $\bullet$ Center of enlargement: $O(0,0)$\\
    $\bullet$ Scale factor: $k = 2$\\
    $\bullet$ Side ratio: $\frac{A'B'}{AB} = \frac{4}{2} = 2$\\
    $\bullet$ Area ratio: $\frac{\text{Area}(A'B'C')}{\text{Area}(ABC)} = k^2 = 4$
  };

\end{tikzpicture}
\end{document}
```

---

## 5. Visual Quality & Formatting Rules
- **No PDF / SVG Output:** Only the `.tex` source and 300 DPI `.png` raster render must be stored.
- **Label Clearance:** Node coordinates and vector rules have opaque background fills (`fill=white, inner sep=1pt`) to prevent grid and axis line clashes.
