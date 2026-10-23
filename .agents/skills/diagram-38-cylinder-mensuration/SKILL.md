---
name: diagram-38-cylinder-mensuration
description: Replicate the authentic BECE 3D cylinder mensuration diagram showing radius, height, and surface area/volume formulas using TikZ.
---

# Diagram 38: 3D Cylinder Mensuration (Radius, Height, and Surface Area)

## 1. Provenance & Curriculum Context
- **Curriculum Indicator:** `B8.3.1.1.2` / `B9.3.1.1.1` (Calculate surface area and volume of cylinders; identify radius $r$, diameter $d$, and height $h$)
- **Topic:** Mensuration / Solid Geometry / Cylinder
- **Mathematical Significance:** Demonstrates geometric properties of a right circular cylinder:
  1. **Base Area:** Circular cross-section of radius $r$:
     $$A = \pi r^2$$
  2. **Curved Surface Area (CSA):** Unrolled rectangular jacket of length $2\pi r$ (circumference) and height $h$:
     $$\text{CSA} = 2\pi r h$$
  3. **Total Surface Area (Closed Cylinder):** Sum of two circular bases plus the curved lateral area:
     $$\text{TSA} = 2\pi r^2 + 2\pi r h = 2\pi r(r + h)$$
  4. **Volume:** Uniform cross-sectional area multiplied by perpendicular height:
     $$V = \pi r^2 h$$

---

## 2. Geometric Specifications & Coordinates
- **Base Dimensions:**
  - Radius $r_x = 2.2\,\text{cm}$, perspective compression $r_y = 0.65\,\text{cm}$.
  - Cylinder height $h = 4.2\,\text{cm}$.
- **Elliptical Bases:**
  - Top base fully visible with lighter fill `blue!15`.
  - Bottom base drawn with solid front arc (`180:360`) and dashed hidden rear arc (`0:180`) in `gray!70`.
- **Axis & Contours:**
  - Vertical contours connecting leftmost and rightmost points.
  - Dashed central vertical axis between base centers $(0, 0) \to (0, h)$.
- **Dimension Callouts:**
  - Horizontal directed radius on top base labeled $r = 7\,\text{cm}$.
  - Parallel offset dimension line with extension bars on right labeled $h = 10\,\text{cm}$.
- **Formula Card:** Centered summary box detailing base area, CSA, TSA, and volume.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Elliptical arc primitives ensure correct perspective projection with mathematically exact tangency between base arcs and lateral contours.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]

  % Geometric parameters
  \def\rx{2.2}
  \def\ry{0.65}
  \def\h{4.2}

  % Cylinder body shading
  \fill[blue!7] (-\rx, 0) arc (180:360:\rx cm and \ry cm) -- (\rx, \h) arc (0:180:\rx cm and \ry cm) -- cycle;

  % Hidden bottom ellipse (dashed)
  \draw[thick, dashed, gray!70] (\rx, 0) arc (0:180:\rx cm and \ry cm);

  % Visible bottom ellipse (solid)
  \draw[very thick] (-\rx, 0) arc (180:360:\rx cm and \ry cm);

  % Vertical contours (left and right edges)
  \draw[very thick] (-\rx, 0) -- (-\rx, \h);
  \draw[very thick] (\rx, 0) -- (\rx, \h);

  % Top ellipse (solid, shaded slightly lighter)
  \fill[blue!15] (0, \h) ellipse (\rx cm and \ry cm);
  \draw[very thick] (0, \h) ellipse (\rx cm and \ry cm);

  % Central vertical axis (dashed)
  \draw[thick, dash pattern=on 4pt off 3pt, gray!80] (0, 0) -- (0, \h);

  % Center point on top base
  \filldraw[black] (0, \h) circle (2pt);
  \filldraw[black] (0, 0) circle (2pt);

  % Radius callout on top face
  \draw[thick, -{Stealth[length=5pt]}] (0, \h) -- (\rx, \h) node[midway, above=2pt, font=\small\bfseries] {$r = 7\,\text{cm}$};

  % Height callout with extension lines on right
  \draw[thin, gray!70] (\rx, \h) -- (\rx + 0.9, \h);
  \draw[thin, gray!70] (\rx, 0) -- (\rx + 0.9, 0);
  \draw[thick, <->] (\rx + 0.7, 0) -- (\rx + 0.7, \h) node[midway, right=3pt, font=\small\bfseries] {$h = 10\,\text{cm}$};

  % Mensuration Formula Card below
  \node[align=left, font=\small, fill=white, inner sep=5pt, draw=gray!40, rounded corners=3pt, anchor=north] at (0.35, -1.2) {
    \textbf{Solid Cylinder Mensuration Formulas:}\\
    $\bullet$ \textbf{Base Area:} $A = \pi r^2$\\
    $\bullet$ \textbf{Curved Surface Area:} $\text{CSA} = 2\pi r h$\\
    $\bullet$ \textbf{Total Surface Area (Closed):} $\text{TSA} = 2\pi r^2 + 2\pi r h = 2\pi r(r + h)$\\
    $\bullet$ \textbf{Volume:} $V = \text{Base Area} \times h = \pi r^2 h$
  };

\end{tikzpicture}
\end{document}
```

---

## 5. Visual Quality & Formatting Rules
- **No PDF / SVG Output:** Only the `.tex` source and 300 DPI `.png` raster render must be stored.
- **Perspective Tangency:** The vertical side contours must strictly match the leftmost and rightmost points ($-\text{rx}, \text{rx}$) of the elliptical bases.
