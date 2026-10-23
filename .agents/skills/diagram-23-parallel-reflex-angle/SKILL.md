---
name: diagram-23-parallel-reflex-angle
description: Replicate the authentic BECE parallel lines diagram with zigzag transversal and reflex angle y using TikZ.
---

# Diagram 23: Parallel Lines with Zigzag Transversal & Reflex Angle $y$

## 1. Provenance & Pedagogical Context
- **Source Question:** `Q_4d06681dd516` / `p479_2787.jpeg`
- **BECE Past Paper:** BECE Mathematics Past Paper (Parallel Lines & Transversals)
- **Question:** *"In the diagram below AC // DF. Angle CBT is 40° and angle DET is 140° Find the value of the reflex angle marked y."*
  - A. $320^\circ$
  - **B. $280^\circ$** (Correct)
  - C. $220^\circ$
  - D. $100^\circ$
  - E. $80^\circ$
- **Mathematical Significance:**
  - Drawing an auxiliary parallel line through $T$ parallel to $AC$ and $DF$:
  - Upper interior angle = alternate angle to $\angle CBT = 40^\circ$.
  - Lower interior angle = alternate angle to $\angle TEF = (180^\circ - 140^\circ) = 40^\circ$.
  - Total interior angle $\angle BTE = 40^\circ + 40^\circ = 80^\circ$.
  - Reflex angle $y = 360^\circ - 80^\circ = 280^\circ$.

---

## 2. Geometric Specifications & Coordinates
- **Parallel Line $AC$:** Horizontal segment from $A(0, 3.5)$ to $C(6.5, 3.5)$.
- **Parallel Line $DF$:** Horizontal segment from $D(0, 0)$ to $F(6.5, 0)$.
- **Intermediate Points:**
  - $B = (2.8, 3.5)$ on line $AC$.
  - $E = (2.8, 0)$ on line $DF$.
- **Apex Vertex $T$:** $(4.9, 1.75)$, creating exact equal slopes of $\pm 39.8^\circ \approx \pm 40^\circ$.
- **Parallel Arrows:** Stealth arrows of length $6\,\text{pt}$ placed along $AB$ and $EF$.
- **Angle Arcs & Labels:**
  - $\angle CBT$: Arc at $B$, radius $0.65\,\text{cm}$, swept from $0^\circ$ down to $-39.8^\circ$, labeled $40^\circ$.
  - $\angle DET$: Arc at $E$, radius $0.65\,\text{cm}$, swept from $180^\circ$ down to $39.8^\circ$, labeled $140^\circ$.
  - Reflex angle $y$: Arc at $T$, radius $0.36\,\text{cm}$, swept around the exterior from $-140.2^\circ$ through $0^\circ$ to $140.2^\circ$ (total sweep $280.4^\circ \approx 280^\circ$).

---

## 3. Tool Choice Rationale
- **LaTeX / TikZ:** Guarantees parallel alignment of horizontal lines and precise reflex angle sweeping without visual gaps or distortion.

---

## 4. Reproducible TikZ Source Code

```latex
\documentclass[tikz,border=10pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,arrows.meta}

\begin{document}
\begin{tikzpicture}[>=latex, line cap=round, line join=round]
  % Baseline coordinates
  \coordinate (A) at (0, 3.5);
  \coordinate (C) at (6.5, 3.5);
  \coordinate (D) at (0, 0);
  \coordinate (F) at (6.5, 0);

  % Vertex coordinates for exact 40-degree angles
  \coordinate (B) at (2.8, 3.5);
  \coordinate (E) at (2.8, 0);
  \coordinate (T) at (4.9, 1.75);

  % Parallel lines
  \draw[thick] (A) -- (C);
  \draw[thick] (D) -- (F);

  % Zigzag transversal segments
  \draw[thick] (B) -- (T) -- (E);

  % Parallel indicator arrows
  \draw[-{Stealth[length=6pt, width=5pt]}] (2.2, 3.5) -- (2.65, 3.5);
  \draw[-{Stealth[length=6pt, width=5pt]}] (3.3, 0) -- (3.75, 0);

  % Angle 40 deg at B
  \draw[thick] ($(B) + (0:0.65)$) arc (0:-39.8:0.65);
  \node at ($(B) + (-20:1.15)$) {\large $40^\circ$};

  % Angle 140 deg at E
  \draw[thick] ($(E) + (180:0.65)$) arc (180:39.8:0.65);
  \node at ($(E) + (115:1.05)$) {\large $140^\circ$};

  % Reflex angle y at T
  \draw[thick] ($(T) + (-140.2:0.36)$) arc (-140.2:140.2:0.36);
  \node[right=4pt] at ($(T) + (0:0.38)$) {\large $\mathbf{y}$};
  \node[left=4pt] at (T) {\large $\mathbf{T}$};

  % Vertex labels
  \node[left=3pt] at (A) {\large $\mathbf{A}$};
  \node[above=3pt] at (B) {\large $\mathbf{B}$};
  \node[right=3pt] at (C) {\large $\mathbf{C}$};
  \node[left=3pt] at (D) {\large $\mathbf{D}$};
  \node[below=3pt] at (E) {\large $\mathbf{E}$};
  \node[right=3pt] at (F) {\large $\mathbf{F}$};

\end{tikzpicture}
\end{document}
```

---

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

## 5. Agent Replication Guide
1. Position parallel lines horizontally at identical x-intervals.
2. Calculate apex $T$ such that $\angle CBT = 40^\circ$ and $\angle DET = 140^\circ$.
3. Swept angle for reflex $y$ must pass around the outer angle from ray $TE$ to ray $TB$.
4. **Compilation & Output (PNG Only — Strictly No PDF/SVG):** Compile the standalone `.tex` via `pdflatex -interaction=nonstopmode <filename>.tex`, rasterize directly to 300 DPI `.png` via PyMuPDF (`page.get_pixmap(dpi=300)`), and immediately delete any intermediate `.pdf`, `.svg`, and LaTeX temp files (`.aux`, `.log`). Diagram assets must exist ONLY as `.png` (and source `.tex`)—never retain, generate, or convert diagrams to `.pdf` or `.svg` files.

---

## 6. Verification & Quality Checklist
- [x] Top and bottom lines are strictly parallel.
- [x] Transversal segments $BT$ and $ET$ form $40^\circ$ alternate angles.
- [x] Reflex arc $y$ correctly envelopes exterior angle of $280^\circ$.
- [x] Parallel indicators are clearly visible and correctly oriented.
- [x] High-resolution 300 DPI vector clarity.
- [x] Visual inspection gate passed (300 DPI PNG reviewed and verified critically)
