---
name: diagram-37-bearing-back-bearing
description: Replicate the authentic BECE compass bearing diagram illustrating forward and back bearings between two stations using TikZ.
---

# Diagram 37: Compass Bearing and Back Bearing Between Two Stations

## 1. Provenance & Curriculum Context
- **Curriculum Indicator:** `B9.3.1.2.2` (Solve bearing problems involving forward and back bearings between two points $A$ and $B$)
- **Topic:** Bearings / Back Bearing
- **Mathematical Significance:** Demonstrates navigation and angular geometry between two stations:
  1. **Three-Figure Forward Bearing:** Measured strictly clockwise from geographic North ($000^\circ$) to the line of sight.
     $$\text{Bearing of } B \text{ from } A = 065^\circ$$
  2. **Back Bearing:** The bearing of the origin station viewed from the destination station:
     $$\text{Bearing of } A \text{ from } B = 065^\circ + 180^\circ = 245^\circ$$
  3. **Parallel Line Transversal Property:** Because the North lines at $A$ and $B$ are parallel ($N_A \parallel N_B$), the alternate interior angle at $B$ equals the forward bearing angle ($65^\circ$), proving geometrically that:
     $$\text{Back Bearing} = 180^\circ + \theta \quad (\text{for } 0^\circ \le \theta < 180^\circ)$$
     $$\text{Back Bearing} = \theta - 180^\circ \quad (\text{for } 180^\circ \le \theta \le 360^\circ)$$

---

## 2. Geometric Specifications & Coordinates
- **Stations:**
  - Station $A(0, 0)$ (Origin).
  - Station $B(5.2, 2.425)$ (Direction $065^\circ$, angle $25^\circ$ with $+x$ axis).
- **North Rays:**
  - Upward directed rays ($+{y}$ direction) with label $N$ at $(0, 2.6)$ and $(5.2, 5.025)$.
  - Dashed cross hairs (South/East/West guides) in light gray.
- **Angular Arcs:**
  - **Forward Bearing Arc at $A$:** Clockwise arc from $90^\circ$ down to $25^\circ$ (sweep $-65^\circ$) at radius $1.3\,\text{cm}$ in `purple!80!black` labeled $065^\circ$.
  - **Back Bearing Reflex Arc at $B$:** Clockwise reflex arc from North ($90^\circ$) sweeping $-245^\circ$ down to the line of sight ($205^\circ / -155^\circ$) at radius $1.4\,\text{cm}$ in `teal!80!black` labeled $245^\circ$.
  - **Alternate Interior Arc at $B$:** Clockwise arc from South ($-90^\circ$) to line of sight ($-155^\circ$) at radius $0.5\,\text{cm}$ labeled $65^\circ$.
- **Summary Box:** Formal BECE formula card centered beneath the diagram.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Guarantees parallel North axes ($N_A \parallel N_B$) and exact angular trigonometry ($90^\circ - 65^\circ = 25^\circ$).

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]

  % Stations A and B
  \coordinate (A) at (0, 0);
  % Bearing 065 deg -> angle from positive x is 90 - 65 = 25 deg
  \coordinate (B) at (5.2, 2.425);

  % Connecting line of sight between stations A and B
  \draw[very thick, blue!85!black] (A) -- (B) node[pos=0.45, below right=4pt, font=\small\bfseries] {Line of sight};

  % --- Station A ---
  \draw[thick, ->] (A) -- ++(0, 2.6) node[above, font=\small\bfseries] {$N$};
  \draw[thin, dashed, gray!60] (A) -- ++(0, -0.8);
  \draw[thin, dashed, gray!60] (A) -- ++(1.5, 0);

  % Forward bearing arc at A (sweep clockwise 65 deg from North)
  \draw[thick, ->, purple!80!black] ([shift=(90:1.3)]A) arc[start angle=90, delta angle=-65, radius=1.3];
  \node[font=\small\bfseries, purple!80!black, fill=white, inner sep=1.5pt] at ($(A) + (57.5:1.75)$) {$065^\circ$};

  % --- Station B ---
  \draw[thick, ->] (B) -- ++(0, 2.6) node[above, font=\small\bfseries] {$N$};
  \draw[thin, dashed, gray!60] (B) -- ++(0, -2.0);
  \draw[thin, dashed, gray!60] (B) -- ++(-1.6, 0);

  % Back bearing reflex arc at B (sweep clockwise 245 deg from North to line BA)
  \draw[thick, ->, teal!80!black] ([shift=(90:1.4)]B) arc[start angle=90, delta angle=-245, radius=1.4];
  \node[font=\small\bfseries, teal!80!black, fill=white, inner sep=1.5pt] at ($(B) + (1.9, 0.3)$) {$245^\circ$};

  % Alternate interior angle arc at B (sweep clockwise 65 deg from South to line BA)
  \draw[thin, gray!70] ([shift=(-90:0.5)]B) arc[start angle=-90, delta angle=-65, radius=0.5];
  \node[font=\footnotesize, gray!70!black, fill=white, inner sep=1pt] at ($(B) + (-0.3, -0.75)$) {$65^\circ$};

  % Station points and labels
  \filldraw[black] (A) circle (2.2pt) node[below left=3pt, font=\normalsize\bfseries] {$A$};
  \filldraw[black] (B) circle (2.2pt) node[above left=3pt, font=\normalsize\bfseries] {$B$};

  % Explanatory Card / Summary below
  \node[align=left, font=\small, fill=white, inner sep=4pt, draw=gray!40, rounded corners=3pt, anchor=north] at (2.6, -1.2) {
    \textbf{Three-Figure Bearing \& Back Bearing:}\\
    $\bullet$ \textbf{Forward Bearing of $B$ from $A$:} $065^\circ$\\
    $\bullet$ \textbf{Back Bearing of $A$ from $B$:} $065^\circ + 180^\circ = 245^\circ$\\
    $\bullet$ \textbf{General Rule:} $\text{Back Bearing} = \theta \pm 180^\circ$ ($+180^\circ$ if $\theta < 180^\circ$; $-180^\circ$ if $\theta > 180^\circ$)
  };

\end{tikzpicture}
\end{document}
```

---

## 5. Visual Quality & Formatting Rules
- **No PDF / SVG Output:** Only the `.tex` source and 300 DPI `.png` raster render must be stored.
- **Label Clearance:** Node coordinates and vector rules have opaque background fills (`fill=white, inner sep=1.5pt`) to prevent grid and axis line clashes.
