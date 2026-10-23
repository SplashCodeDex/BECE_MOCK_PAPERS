---
name: diagram-42-stem-and-leaf-plot
description: Replicate the authentic BECE statistics diagram showing an ordered stem-and-leaf plot with frequency column, key, mode, median, and range analysis using TikZ.
---

# Diagram 42: Ordered Stem-and-Leaf Plot

## 1. Provenance & Curriculum Context
- **Curriculum Indicator:** `B8.4.1.1.1` (Organize and display numerical data using stem-and-leaf plots; determine mode, median, range, and interpret the shape of the data distribution)
- **Topic:** Handling Data / Statistics / Stem-and-Leaf Displays
- **Mathematical Significance:** Demonstrates structured exploratory data analysis:
  1. **Structure:** Retains original raw data values while simultaneously grouping them into an ordered distribution:
     - **Stem (Tens Digit):** Displayed on the left of the heavy dividing rule.
     - **Leaf (Units Digit):** Displayed in increasing ascending order to the right.
     - **Frequency Column:** Displays row frequencies summing to sample size $N = 25$.
  2. **Key / Legend:** Essential for decoding magnitude:
     $$\text{Key: } 2 \mid 5 = 25\text{ marks}$$
  3. **Summary Statistics:**
     - **Minimum:** $14$, **Maximum:** $54$, **Range:** $54 - 14 = 40$.
     - **Mode:** $37$ (most frequent value, highlighted in red).
     - **Median:** 13th ordered value $= 34$ (highlighted in bold).

---

## 2. Geometric Specifications & Coordinates
- **Layout:** $x = 1\,\text{cm}$, $y = 0.7\,\text{cm}$ coordinate system.
- **Rules & Dividers:**
  - Header rule ($y = 5.4$) and bottom total rule ($y = -0.8$).
  - Vertical primary dividing line ($x = 1.6$) in `very thick` black.
  - Vertical secondary frequency divider ($x = 6.6$) in `gray!60`.
- **Text Alignment:**
  - Stems centered at $x = 0.8$.
  - Leaves left-anchored at $x = 2.2$ with uniform spacing.
  - Frequencies centered at $x = 7.4$.
- **Callout Cards:**
  - Shaded blue Key box at $y = -1.8$.
  - Formal statistical summary card at $y = -3.2$.

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Guarantees crisp typography and exact coordinate alignment across all stem rows and leaf digits.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc}

\begin{document}
\begin{tikzpicture}[x=1cm, y=0.7cm, line cap=round, line join=round]

  % Title banner
  \node[font=\large\bfseries] at (4.0, 7.2) {Mathematics Test Scores ($N = 25$)};

  % Header row (y = 6)
  \node[font=\normalsize\bfseries] at (0.8, 6.0) {Stem};
  \node[font=\normalsize\bfseries, anchor=west] at (2.2, 6.0) {Leaf};
  \node[font=\normalsize\bfseries] at (7.4, 6.0) {Freq ($f$)};

  % Horizontal dividing line under header
  \draw[thick] (0, 5.4) -- (8.2, 5.4);

  % Vertical dividing rule between Stem and Leaf
  \draw[very thick] (1.6, 5.4) -- (1.6, -0.4);
  % Vertical dividing rule between Leaf and Frequency (moved to 6.6 for ample clearance)
  \draw[thick, gray!60] (6.6, 5.4) -- (6.6, -0.4);

  % Data Rows
  % Row 1: Stem 1 (y = 4.5)
  \node[font=\normalsize\bfseries] at (0.8, 4.5) {1};
  \node[font=\normalsize, anchor=west] at (2.2, 4.5) {4 \ \ 7 \ \ 8 \ \ 9};
  \node[font=\normalsize] at (7.4, 4.5) {4};

  % Row 2: Stem 2 (y = 3.3)
  \node[font=\normalsize\bfseries] at (0.8, 3.3) {2};
  \node[font=\normalsize, anchor=west] at (2.2, 3.3) {0 \ \ 2 \ \ 3 \ \ 5 \ \ 5 \ \ 8};
  \node[font=\normalsize] at (7.4, 3.3) {6};

  % Row 3: Stem 3 (y = 2.1)
  \node[font=\normalsize\bfseries] at (0.8, 2.1) {3};
  \node[font=\normalsize, anchor=west] at (2.2, 2.1) {1 \ \ 2 \ \ \textbf{4} \ \ 5 \ \ \textcolor{red!80!black}{\textbf{7}} \ \ \textcolor{red!80!black}{\textbf{7}} \ \ \textcolor{red!80!black}{\textbf{7}} \ \ 9};
  \node[font=\normalsize] at (7.4, 2.1) {8};

  % Row 4: Stem 4 (y = 0.9)
  \node[font=\normalsize\bfseries] at (0.8, 0.9) {4};
  \node[font=\normalsize, anchor=west] at (2.2, 0.9) {0 \ \ 2 \ \ 3 \ \ 6 \ \ 8};
  \node[font=\normalsize] at (7.4, 0.9) {5};

  % Row 5: Stem 5 (y = -0.3)
  \node[font=\normalsize\bfseries] at (0.8, -0.3) {5};
  \node[font=\normalsize, anchor=west] at (2.2, -0.3) {1 \ \ 4};
  \node[font=\normalsize] at (7.4, -0.3) {2};

  % Bottom rule
  \draw[thick] (0, -0.8) -- (8.2, -0.8);

  % Total row (y = -1.3)
  \node[font=\small\bfseries] at (0.8, -1.3) {Total};
  \node[font=\small\bfseries] at (7.4, -1.3) {25};

  % Key / Legend Card (y = -1.8)
  \node[align=left, font=\small, fill=blue!5, inner sep=4pt, draw=blue!30, rounded corners=2pt, anchor=north west] at (0, -1.8) {
    \textbf{Key:} \ $2 \mid 5$ represents \textbf{25 marks} \quad (Stem = Tens digit, Leaf = Units digit)
  };

  % Statistical Summary Card below (y = -3.2)
  \node[align=left, font=\small, fill=white, inner sep=5pt, draw=gray!40, rounded corners=3pt, anchor=north west] at (0, -3.2) {
    \textbf{Statistical Analysis from Stem-and-Leaf Plot:}\\
    $\bullet$ \textbf{Minimum:} $14$ \quad $\bullet$ \textbf{Maximum:} $54$\\
    $\bullet$ \textbf{Range:} $\text{Max} - \text{Min} = 54 - 14 = 40$\\
    $\bullet$ \textbf{Mode:} $37$ (most frequent value: appears 3 times in stem 3)\\
    $\bullet$ \textbf{Median (13th ordered value):} $34$
  };

\end{tikzpicture}
\end{document}
```

---

## 5. Visual Quality & Formatting Rules
- **No PDF / SVG Output:** Only the `.tex` source and 300 DPI `.png` raster render must be stored.
- **Horizontal Clearance:** Leaf items must maintain minimum $0.4\,\text{cm}$ clearance before the frequency vertical rule.
