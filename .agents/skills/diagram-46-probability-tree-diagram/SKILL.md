---
name: diagram-46-probability-tree-diagram
description: Replicate the authentic BECE probability tree diagram illustrating two-stage selection without replacement, branch probabilities, outcomes, and combined event rules using TikZ.
---

# Diagram 46: Probability Tree Diagram (Two-Stage Selection)

## 1. Provenance & Curriculum Context
- **Curriculum Indicator:** `B9.4.2.1.1` (Construct and use probability tree diagrams to determine outcomes and calculate probabilities of combined independent and dependent events)
- **Topic:** Handling Data / Probability / Tree Diagrams
- **Mathematical Significance:** Demonstrates multi-stage probability calculation (exemplified by selecting 2 counters without replacement from a bag of 3 Red and 2 Blue counters):
  1. **Branch Structure:**
     - **Stage 1 (First Pick, $N = 5$):** $P(R) = \frac{3}{5}$, $P(B) = \frac{2}{5}$.
     - **Stage 2 (Second Pick, $N = 4$):** Conditional branch probabilities reflect dependency (no replacement).
  2. **Multiplication Rule (Path Along Branches):**
     $$P(R \cap R) = \frac{3}{5} \times \frac{2}{4} = \frac{6}{20} = \frac{3}{10}$$
     $$P(R \cap B) = \frac{3}{5} \times \frac{2}{4} = \frac{6}{20} = \frac{3}{10}$$
     $$P(B \cap R) = \frac{2}{5} \times \frac{3}{4} = \frac{6}{20} = \frac{3}{10}$$
     $$P(B \cap B) = \frac{2}{5} \times \frac{1}{4} = \frac{2}{20} = \frac{1}{10}$$
  3. **Exhaustive Outcomes:** Sum of all branch path probabilities equals unity:
     $$\frac{6}{20} + \frac{6}{20} + \frac{6}{20} + \frac{2}{20} = \frac{20}{20} = 1$$
  4. **Addition Rule (Mutually Exclusive Outcomes):**
     $$P(\text{At least one Red}) = P(RR) + P(RB) + P(BR) = \frac{18}{20} = \frac{9}{10}$$
  5. **Complement Rule:**
     $$P(\text{At least one Red}) = 1 - P(BB) = 1 - \frac{2}{20} = \frac{18}{20} = \frac{9}{10}$$

---

## 2. Geometric Specifications & Coordinates
- **Column Header Positions ($y = 3.8$):**
  - "1st Pick" ($x = 2.6$).
  - "2nd Pick" ($x = 5.6$).
  - "Outcome" ($x = 7.6$).
  - "Probability" ($x = 10.0$).
- **Node Geometry:**
  - Root at $(0, 0)$.
  - Stage 1 at $x = 2.6$: $R(2.6, 1.8)$ and $B(2.6, -1.8)$ with labels placed above and below nodes to preserve clear branch departures.
  - Stage 2 terminal nodes at $x = 5.6$: $(5.6, 2.7), (5.6, 0.9), (5.6, -0.9), (5.6, -2.7)$.
- **Branch Styling:**
  - Red branches in `red!85!black`.
  - Blue branches in `blue!85!black`.
  - Mid-branch probability fractions.
- **Summary Box:** Centered card detailing the multiplication rule, outcome sum, and complementary event calculation.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Guarantees precise horizontal column alignment and clean vector rendering without fractional text distortion.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]

  % Column Headers
  \node[font=\small\bfseries] at (2.6, 3.8) {1st Pick};
  \node[font=\small\bfseries] at (5.6, 3.8) {2nd Pick};
  \node[font=\small\bfseries] at (7.6, 3.8) {Outcome};
  \node[font=\small\bfseries] at (10.0, 3.8) {Probability};

  % Dividing guide header line
  \draw[thick, gray!40] (1.0, 3.4) -- (11.5, 3.4);

  % Root
  \coordinate (Root) at (0, 0);
  \filldraw[black] (Root) circle (2.2pt) node[left=3pt, font=\small\bfseries] {Start};

  % Stage 1 Coordinates
  \coordinate (R1) at (2.6, 1.8);
  \coordinate (B1) at (2.6, -1.8);

  % Stage 2 Coordinates
  \coordinate (RR) at (5.6, 2.7);
  \coordinate (RB) at (5.6, 0.9);
  \coordinate (BR) at (5.6, -0.9);
  \coordinate (BB) at (5.6, -2.7);

  % Stage 1 Branches
  \draw[very thick, red!85!black] (Root) -- (R1) node[midway, above left=1pt, font=\small\bfseries] {$\frac{3}{5}$};
  \draw[very thick, blue!85!black] (Root) -- (B1) node[midway, below left=1pt, font=\small\bfseries] {$\frac{2}{5}$};

  % Stage 2 Branches from R1
  \draw[thick, red!85!black] (R1) -- (RR) node[midway, above left=1pt, font=\footnotesize\bfseries] {$\frac{2}{4}$};
  \draw[thick, blue!85!black] (R1) -- (RB) node[midway, below left=1pt, font=\footnotesize\bfseries] {$\frac{2}{4}$};

  % Stage 2 Branches from B1
  \draw[thick, red!85!black] (B1) -- (BR) node[midway, above left=1pt, font=\footnotesize\bfseries] {$\frac{3}{4}$};
  \draw[thick, blue!85!black] (B1) -- (BB) node[midway, below left=1pt, font=\footnotesize\bfseries] {$\frac{1}{4}$};

  % Node circles and labels
  % Stage 1 (placed above/below vertex to clear departing branches)
  \filldraw[red!85!black] (R1) circle (2.2pt) node[above=3pt, font=\small\bfseries] {$R$};
  \filldraw[blue!85!black] (B1) circle (2.2pt) node[below=3pt, font=\small\bfseries] {$B$};

  % Stage 2
  \filldraw[red!85!black] (RR) circle (2.2pt) node[right=4pt, font=\small\bfseries] {$R$};
  \filldraw[blue!85!black] (RB) circle (2.2pt) node[right=4pt, font=\small\bfseries] {$B$};
  \filldraw[red!85!black] (BR) circle (2.2pt) node[right=4pt, font=\small\bfseries] {$R$};
  \filldraw[blue!85!black] (BB) circle (2.2pt) node[right=4pt, font=\small\bfseries] {$B$};

  % Outcomes & Probabilities
  \node[font=\small\bfseries] at (7.6, 2.7) {$(R, R)$};
  \node[font=\small] at (10.0, 2.7) {$\frac{3}{5} \times \frac{2}{4} = \frac{6}{20}$};

  \node[font=\small\bfseries] at (7.6, 0.9) {$(R, B)$};
  \node[font=\small] at (10.0, 0.9) {$\frac{3}{5} \times \frac{2}{4} = \frac{6}{20}$};

  \node[font=\small\bfseries] at (7.6, -0.9) {$(B, R)$};
  \node[font=\small] at (10.0, -0.9) {$\frac{2}{5} \times \frac{3}{4} = \frac{6}{20}$};

  \node[font=\small\bfseries] at (7.6, -2.7) {$(B, B)$};
  \node[font=\small] at (10.0, -2.7) {$\frac{2}{5} \times \frac{1}{4} = \frac{2}{20}$};

  % Summary Card below
  \node[align=left, font=\small, fill=white, inner sep=5pt, draw=gray!40, rounded corners=3pt, anchor=north] at (5.5, -3.8) {
    \textbf{Probability Tree Diagram (Picking without Replacement, 3 Red, 2 Blue):}\\
    $\bullet$ \textbf{Multiplication Rule (Branches):} Multiply probabilities along a branch path\\
    $\bullet$ \textbf{Sum of All Outcomes:} $\frac{6}{20} + \frac{6}{20} + \frac{6}{20} + \frac{2}{20} = \frac{20}{20} = 1$\\
    $\bullet$ \textbf{$P(\text{At least one Red}):$} $P(RR) + P(RB) + P(BR) = \frac{6 + 6 + 6}{20} = \frac{18}{20} = \frac{9}{10}$\\
    $\bullet$ \textbf{Complementary Event:} $1 - P(BB) = 1 - \frac{2}{20} = \frac{18}{20} = \frac{9}{10}$
  };

\end{tikzpicture}
\end{document}
```

---

## 5. Visual Quality & Formatting Rules
- **No PDF / SVG Output:** Only the `.tex` source and 300 DPI `.png` raster render must be stored.
- **Label Clearance:** Node coordinates and vector rules have opaque background fills (`fill=white, inner sep=1.5pt`) to prevent grid and axis line clashes.
