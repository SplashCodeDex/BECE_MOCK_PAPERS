---
name: diagram-36-vector-addition-laws
description: Replicate the authentic BECE vector diagram illustrating Triangle and Parallelogram Laws of vector addition using TikZ.
---

# Diagram 36: Vector Addition (Triangle and Parallelogram Laws)

## 1. Provenance & Curriculum Context
- **Curriculum Indicator:** `B8.3.2.1.2` / `B9.3.2.1.1` (Add and subtract vectors in 2D, solve geometric problems using triangle and parallelogram laws of vectors)
- **Topic:** Vectors / Vector Addition Laws
- **Mathematical Significance:** Demonstrates the foundational principles of vector composition:
  1. **Triangle Law of Vectors:** If two vectors are represented in magnitude and direction by two sides of a triangle taken in order ($\vec{AB} = \mathbf{u}$ and $\vec{BC} = \mathbf{v}$), their resultant is represented by the third closing side taken in reverse order ($\vec{AC} = \mathbf{u} + \mathbf{v}$).
  2. **Parallelogram Law of Vectors:** If two vectors are represented in magnitude and direction by two adjacent sides of a parallelogram originating from a common vertex ($\vec{AB} = \mathbf{u}$ and $\vec{AD} = \mathbf{v}$), the diagonal passing through their common point represents the resultant vector ($\vec{AC} = \mathbf{u} + \mathbf{v}$).
  3. Vectors maintain translation invariance ($\vec{AD} \parallel \vec{BC} = \mathbf{v}$ and $\vec{AB} \parallel \vec{DC} = \mathbf{u}$).

---

## 2. Geometric Specifications & Coordinates
- **Vertices:**
  - $A(0, 0)$ (Common origin).
  - $B(4.8, 0)$ (Base horizontal vector $\mathbf{u}$).
  - $D(2.0, 3.2)$ (Sloped adjacent vector $\mathbf{v}$).
  - $C(6.8, 3.2)$ (Opposite vertex / Resultant tip).
- **Styling & Arrows:**
  - Midway directed arrows (`Stealth[length=6pt]`) on edges to avoid vertex crowding.
  - Double arrowhead (`Stealth[length=6pt]Stealth[length=6pt]`) along the resultant diagonal $\vec{AC}$.
  - Shaded interior in `blue!6` to emphasize the 2D plane spanned by the vectors.
  - Dashed completion edges for $\vec{BC}$ and $\vec{DC}$.
  - Sloped label $\mathbf{R} = \mathbf{u} + \mathbf{v}$ parallel to the resultant diagonal.
- **Summary Card:** Boxed annotation detailing both laws with standard mathematical notation.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** The `decorations.markings` library allows precise midway arrow positioning, ensuring vertices remain clear point markers without arrow collision.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta,decorations.markings}

\tikzset{
  midarrow/.style={decoration={markings, mark=at position 0.55 with {\arrow{Stealth[length=6pt]}}}, postaction={decorate}},
  midarrow2/.style={decoration={markings, mark=at position 0.65 with {\arrow{Stealth[length=6pt]Stealth[length=6pt]}}}, postaction={decorate}}
}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]

  % Coordinates of the Parallelogram of Vectors
  \coordinate (A) at (0, 0);
  \coordinate (B) at (4.8, 0);
  \coordinate (D) at (2.0, 3.2);
  \coordinate (C) at (6.8, 3.2);

  % Shading of the parallelogram
  \fill[blue!6] (A) -- (B) -- (C) -- (D) -- cycle;

  % Parallelogram completion lines (dashed with midway arrows)
  \draw[thick, dashed, purple!80!black, midarrow] (B) -- (C) node[midway, right=4pt, font=\small\bfseries] {$\mathbf{v}$};
  \draw[thick, dashed, blue!70!black, midarrow] (D) -- (C) node[midway, above=4pt, font=\small\bfseries] {$\mathbf{u}$};

  % Primary vectors u and v from origin A (with midway arrows)
  \draw[very thick, blue!80!black, midarrow] (A) -- (B) node[midway, below=5pt, font=\normalsize\bfseries] {$\mathbf{u}$};
  \draw[very thick, purple!80!black, midarrow] (A) -- (D) node[midway, left=5pt, font=\normalsize\bfseries] {$\mathbf{v}$};

  % Resultant diagonal vector R = u + v with double arrowhead midway and sloped label
  \draw[line width=1.5pt, teal!80!black, midarrow2] (A) -- (C) node[pos=0.38, sloped, below=5pt, font=\normalsize\bfseries, teal!80!black] {$\mathbf{R} = \mathbf{u} + \mathbf{v}$};

  % Vertex points
  \filldraw[black] (A) circle (2.2pt) node[below left=3pt, font=\small\bfseries] {$A$};
  \filldraw[black] (B) circle (2.2pt) node[below right=3pt, font=\small\bfseries] {$B$};
  \filldraw[black] (C) circle (2.2pt) node[above right=3pt, font=\small\bfseries] {$C$};
  \filldraw[black] (D) circle (2.2pt) node[above left=3pt, font=\small\bfseries] {$D$};

  % Explanatory Card / Annotation below
  \node[align=left, font=\small, fill=white, inner sep=4pt, draw=gray!40, rounded corners=3pt, anchor=north] at (3.4, -0.9) {
    \textbf{Vector Addition Laws:}\\
    $\bullet$ \textbf{Triangle Law:} $\vec{AC} = \vec{AB} + \vec{BC} = \mathbf{u} + \mathbf{v}$\\
    $\bullet$ \textbf{Parallelogram Law:} If adjacent sides represent $\vec{AB} = \mathbf{u}$ and $\vec{AD} = \mathbf{v}$,\\
    \hspace*{3.2mm}the diagonal co-initial with them represents the resultant: $\vec{AC} = \mathbf{u} + \mathbf{v}$.
  };

\end{tikzpicture}
\end{document}
```

---

## 5. Visual Quality & Formatting Rules
- **No PDF / SVG Output:** Only the `.tex` source and 300 DPI `.png` raster render must be stored.
- **Midway Arrowheads:** Arrows must be drawn midway along segments via TikZ decorations to maintain unoccluded vertices.
