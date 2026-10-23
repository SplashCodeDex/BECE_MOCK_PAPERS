---
name: diagram-33-translation-vector-grid
description: Replicate the authentic BECE transformation diagram showing geometric translation by a column vector on a Cartesian grid using TikZ.
---

# Diagram 33: Geometric Translation by a Vector on a Cartesian Grid

## 1. Provenance & Curriculum Context
- **Curriculum Indicator:** `B8.3.3.1.1` (Perform a single translation on coordinate planes and determine the image coordinates using vector addition)
- **Topic:** Position and Transformation / Translation by Vector
- **Mathematical Significance:** Demonstrates geometric translation in the 2D coordinate plane:
  1. Translation vector $\mathbf{v} = \begin{pmatrix} a \\ b \end{pmatrix}$ maps every point $(x, y) \to (x + a, y + b)$.
  2. Every point shifts by the exact same distance in the exact same direction.
  3. Connecting displacement vectors $\vec{AA'}$, $\vec{BB'}$, and $\vec{CC'}$ are parallel, congruent, and point in the direction of $\mathbf{v}$.
  4. The shape maintains identical size, shape, and angular orientation ($|\triangle ABC| \cong |\triangle A'B'C'|$).

---

## 2. Geometric Specifications & Coordinates
- **Grid Extent:** $[-4.5, 4.5] \times [-4.5, 4.5]$ with $1.0\,\text{cm}$ step size in `gray!25`.
- **Axes:** $x$-axis and $y$-axis extending to $\pm 4.8$ with double-headed arrows.
- **Tick Labels:** Integer ticks $-4$ to $+4$ with opaque `fill=white` backgrounds.
- **Object $\triangle ABC$:**
  - $A(-3, -1)$, $B(-1, -1)$, $C(-2, 1)$ filled with `blue!12`.
- **Translation Vector:**
  - $\mathbf{v} = \begin{pmatrix} 4 \\ 2 \end{pmatrix}$.
- **Image $\triangle A'B'C'$:**
  - $A'(1, 1)$, $B'(3, 1)$, $C'(2, 3)$ filled with `teal!15`.
- **Vector Displacement Rays:** Directed arrows connecting corresponding vertices with $\vec{CC'}$ highlighted and labeled $\mathbf{v}$.
- **Rule Annotation:** Displayed in Quadrant II: $\mathbf{v} = \begin{pmatrix} 4 \\ 2 \end{pmatrix}$.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Guarantees strict mathematical vector consistency and clean Cartesian grid lines with zero rasterization artifacts.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]
  % Grid
  \draw[step=1cm, gray!25, thin] (-4.5, -4.5) grid (4.5, 4.5);

  % Axes
  \draw[thick, <->] (-4.8, 0) -- (4.8, 0) node[right, font=\normalsize] {$x$};
  \draw[thick, <->] (0, -4.8) -- (0, 4.8) node[above, font=\normalsize] {$y$};

  % Origin
  \node[below left=2pt, font=\small] at (0, 0) {$O$};

  % Integer ticks with opaque backgrounds to prevent line collision
  \foreach \x in {-4,-3,-2,-1,1,2,3,4} {
    \draw[thick] (\x, 0.1) -- (\x, -0.1);
    \node[below=3pt, font=\footnotesize, fill=white, inner sep=1pt] at (\x, -0.1) {$\x$};
  }
  \foreach \y in {-4,-3,-2,-1,1,2,3,4} {
    \draw[thick] (0.1, \y) -- (-0.1, \y);
    \node[left=3pt, font=\footnotesize, fill=white, inner sep=1pt] at (-0.1, \y) {$\y$};
  }

  % Object triangle ABC (Quadrant III)
  \coordinate (A) at (-3, -1);
  \coordinate (B) at (-1, -1);
  \coordinate (C) at (-2, 1);

  % Image triangle A'B'C' translated by vector (4, 2) (Quadrant I)
  \coordinate (A1) at (1, 1);
  \coordinate (B1) at (3, 1);
  \coordinate (C1) at (2, 3);

  % Translation displacement vectors
  \draw[very thick, ->, purple!80!black] (C) -- (C1) node[pos=0.35, above left=3pt, font=\small\bfseries, fill=white, inner sep=1pt] {$\mathbf{v}$};
  \draw[thick, dashed, ->, purple!80!black] (A) -- (A1);
  \draw[thick, dashed, ->, purple!80!black] (B) -- (B1);

  % Object triangle ABC
  \draw[very thick, fill=blue!12] (A) -- (B) -- (C) -- cycle;
  \filldraw[black] (A) circle (2pt) node[below left=3pt, font=\small\bfseries] {$A(-3,-1)$};
  \filldraw[black] (B) circle (2pt) node[below right=3pt, font=\small\bfseries] {$B(-1,-1)$};
  \filldraw[black] (C) circle (2pt) node[above left=3pt, font=\small\bfseries] {$C(-2,1)$};

  % Image triangle A'B'C'
  \draw[very thick, fill=teal!15] (A1) -- (B1) -- (C1) -- cycle;
  \filldraw[black] (A1) circle (2pt);
  \node[above right=2pt, font=\small\bfseries] at (A1) {$A'(1,1)$};
  \filldraw[black] (B1) circle (2pt) node[right=4pt, font=\small\bfseries] {$B'(3,1)$};
  \filldraw[black] (C1) circle (2pt) node[above=4pt, font=\small\bfseries] {$C'(2,3)$};

  % Translation Vector Rule Annotation in Quadrant II
  \node[font=\small\bfseries, fill=white, inner sep=2pt] at (-2.5, 3.8) {Translation by vector:};
  \node[font=\normalsize, fill=white, inner sep=2pt] at (-2.5, 2.9) {$\mathbf{v} = \begin{pmatrix} 4 \\ 2 \end{pmatrix}$};

\end{tikzpicture}
\end{document}
```

---

## 5. Visual Quality & Formatting Rules
- **No PDF / SVG Output:** Only the `.tex` source and 300 DPI `.png` raster render must be stored.
- **Label Clearance:** Node coordinates and vector rules have opaque background fills (`fill=white, inner sep=1pt`) to prevent grid and axis line clashes.
