---
name: diagram-40-cone-mensuration
description: Replicate the authentic BECE 3D cone mensuration diagram showing slant height l, vertical altitude h, base radius r, and mensuration formulas using TikZ.
---

# Diagram 40: 3D Right Circular Cone Mensuration

## 1. Provenance & Curriculum Context
- **Curriculum Indicator:** `B9.3.1.1.2` (Calculate surface area and volume of a right circular cone; relate slant height $l$, vertical height $h$, and radius $r$ using the Pythagorean theorem)
- **Topic:** Solid Geometry / Mensuration / Cone
- **Mathematical Significance:** Demonstrates geometric properties and mensuration formulas of a right circular cone:
  1. **Pythagorean Relation:** The vertical altitude ($h$), horizontal radius ($r$), and slant contour ($l$) form a right-angled triangle:
     $$l^2 = r^2 + h^2 \implies l = \sqrt{r^2 + h^2}$$
     For $r = 5\,\text{cm}$ and $h = 12\,\text{cm}$: $l = \sqrt{5^2 + 12^2} = 13\,\text{cm}$.
  2. **Base Area:** Circular base of radius $r$:
     $$A = \pi r^2$$
  3. **Curved Surface Area (CSA):** Unrolled circular sector with arc length equal to base circumference $2\pi r$ and sector radius $l$:
     $$\text{CSA} = \pi r l$$
  4. **Total Surface Area (TSA):**
     $$\text{TSA} = \pi r^2 + \pi r l = \pi r(r + l)$$
  5. **Volume:** One-third of the enclosing cylinder's volume:
     $$V = \frac{1}{3}\pi r^2 h$$

---

## 2. Geometric Specifications & Coordinates
- **Dimensions:**
  - Base radius $r_x = 2.2\,\text{cm}$, compression $r_y = 0.65\,\text{cm}$.
  - Altitude $h = 4.4\,\text{cm}$ (Apex $V$ at $(0, 4.4)$).
- **Contour Hierarchy:**
  - Visible front base arc: Solid `very thick` line ($180^\circ \to 360^\circ$).
  - Hidden rear base arc: Dashed `thick` line in `gray!70` ($0^\circ \to 180^\circ$).
  - Slanted lateral boundary: Tangent lines from Apex $V(0, h)$ to $(-\rx, 0)$ and $(\rx, 0)$.
- **Internal Right Triangle:**
  - Vertical altitude: Dashed in `purple!80!black` from $V(0, h) \to O(0, 0)$ labeled $h = 12\,\text{cm}$.
  - Base radius: Solid in `blue!80!black` from $O(0, 0) \to B(\rx, 0)$ labeled $r = 5\,\text{cm}$ placed above the radius line.
  - Slant contour: Sloped path labeled $l = 13\,\text{cm}$ in `teal!80!black`.
  - Right angle marker at center $O(0, 0)$.
- **Formula Card:** Centered summary box detailing the Pythagorean relation, base area, CSA, TSA, and volume.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Guarantees strict geometric tangency and perspective consistency between the elliptical base and slant height contours.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]

  % Dimensions (proportions: rx = 2.2, ry = 0.65, height h = 4.4)
  \def\rx{2.2}
  \def\ry{0.65}
  \def\h{4.4}

  % Cone lateral body shading
  \fill[blue!7] (-\rx, 0) arc (180:360:\rx cm and \ry cm) -- (0, \h) -- cycle;

  % Hidden back half of base ellipse (dashed)
  \draw[thick, dashed, gray!70] (\rx, 0) arc (0:180:\rx cm and \ry cm);

  % Visible front half of base ellipse (solid)
  \draw[very thick] (-\rx, 0) arc (180:360:\rx cm and \ry cm);

  % Lateral contours
  \draw[very thick] (-\rx, 0) -- (0, \h);
  \draw[very thick] (\rx, 0) -- (0, \h);

  % Internal right triangle V-O-B:
  % Vertical altitude (dashed)
  \draw[thick, dashed, purple!80!black] (0, \h) -- (0, 0) node[midway, left=3pt, font=\small\bfseries] {$h = 12\,\text{cm}$};

  % Horizontal base radius (solid, label above to avoid base arc)
  \draw[thick, blue!80!black] (0, 0) -- (\rx, 0) node[midway, above=2pt, font=\small\bfseries] {$r = 5\,\text{cm}$};

  % Slant height callout on right contour
  \path (0, \h) -- (\rx, 0) node[midway, above right=3pt, font=\small\bfseries, teal!80!black] {$l = 13\,\text{cm}$};

  % Right angle indicator at center O
  \draw[thin] (0, 0.25) -- (0.25, 0.25) -- (0.25, 0);

  % Points
  \filldraw[black] (0, \h) circle (2pt) node[above=2pt, font=\small\bfseries] {$V$ (Apex)};
  \filldraw[black] (0, 0) circle (2pt) node[below left=2pt, font=\small\bfseries] {$O$};
  \filldraw[black] (\rx, 0) circle (2pt) node[below right=2pt, font=\small\bfseries] {$B$};

  % Formula Card below
  \node[align=left, font=\small, fill=white, inner sep=5pt, draw=gray!40, rounded corners=3pt, anchor=north] at (0, -1.2) {
    \textbf{Right Circular Cone Mensuration Formulas:}\\
    $\bullet$ \textbf{Pythagorean Relation:} $l^2 = r^2 + h^2 \implies l = \sqrt{5^2 + 12^2} = 13\,\text{cm}$\\
    $\bullet$ \textbf{Base Area:} $A = \pi r^2$\\
    $\bullet$ \textbf{Curved Surface Area:} $\text{CSA} = \pi r l$\\
    $\bullet$ \textbf{Total Surface Area (Closed):} $\text{TSA} = \pi r^2 + \pi r l = \pi r(r + l)$\\
    $\bullet$ \textbf{Volume:} $V = \frac{1}{3} \times \text{Base Area} \times h = \frac{1}{3}\pi r^2 h$
  };

\end{tikzpicture}
\end{document}
```

---

## 5. Visual Quality & Formatting Rules
- **No PDF / SVG Output:** Only the `.tex` source and 300 DPI `.png` raster render must be stored.
- **Label Clearance:** Node coordinates and vector rules have opaque background fills (`fill=white, inner sep=1.5pt`) to prevent grid and axis line clashes.
