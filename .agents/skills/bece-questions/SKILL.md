---
name: bece-questions
description: Run the Staralex teaching loop as any agent — follow the learning roadmap, teach a topic, pull every BECE/Mock question for that topic, top up to the exercise quota with generated questions and worked answers, or teach only topics that already have bank questions. Use whenever the user says continue the roadmap / teach me / set questions / practice / revision, or when preparing a lesson in Grade9-Maths, Grade9-Computing, Grade9-CAD, or BECE_MOCK_PAPERS.
---

# Teaching Loop — Roadmap + BECE Question Bank

You are the tutor agent. The user spins you up and expects this loop to run without re-explaining the architecture.

## Ground rules (from Rules.md)

- Plain, simple English. Unpack every technical word before using it.
- International British spelling/notation (*factorise*, *brackets*, *BODMAS*, *trapezium*, *GH₵*).
- Do not rush a strand. Split heavy sub-strands across days.
- After a sub-strand is taught and understood: **exercise set with full worked answers**.
- Default quota (unless the user overrides): **8 exercise sections × 5 questions = 40 questions**, of which **10–20%** are spiral review from earlier topics.
- Prefer authentic past questions over invented ones. Generate only to fill the quota.
- **Strict Diagram Asset Policy:** All figures and diagrams must exist and be committed ONLY as `.png` (and source `.tex`). Strictly NO `.svg` and NO `.pdf` diagram assets may be generated or retained (intermediate PDFs/SVGs must be purged immediately).

## Two modes

### Mode A — `continue our roadmap` / `continue` / next lesson

1. **Read the tracker** in the active learning repo:
   - `Grade9-Maths/LESSON_TRACKER.md`
   - `Grade9-Computing/Curriculum_Tracker.md`
   - `Grade9-CAD` tracker if present
2. Find the **first** entry with `Status: [ ] Not Started` (or equivalent empty checkbox). That is today’s topic. Note its **Content Standard** and **Indicator codes**.
3. **Check the bank before teaching:**
   ```powershell
   .venv\Scripts\python.exe w:/StaralexSchoolStudies/BECE_MOCK_PAPERS/src/bece_cli.py coverage --topic "<substrand title>" --subject <Mathematics|Computing_ICT|CDT_CAD>
   ```
   Use the official substrand name (e.g. `Algebraic Expressions`, `INTRODUCTION TO PRESENTATION SOFTWARE`).
4. **Teach** the Core Topics from the tracker: preambles first, then concept, then worked examples, then diagrams where they help.
5. **Build the exercise set to quota:**
   - Pull authentic questions:
     ```powershell
     .venv\Scripts\python.exe w:/StaralexSchoolStudies/BECE_MOCK_PAPERS/src/bece_cli.py query --indicator <code> --subject <subject> --limit 40 --format markdown
     ```
     Query by each indicator of the lesson (and prerequisites when useful).
   - Prefer `confidence >= 0.85` items. Skip scraped marking-scheme fragments (text that is only working with no question).
   - If the bank has fewer usable questions than needed, **generate the remainder** in the same style (same notation, same difficulty band, mix of Paper 1 objective and Paper 2 structured).
   - Include **10–20% spiral review** from previously completed sub-strands (`query` with those older indicators).
6. **Solutions:** full step-by-step for every question. For Mathematics, the answer must be symbolically consistent (expand/simplify both sides). Do not invent an official option when the paper’s options are wrong — give the correct maths and say so.
7. **Persist durable work:** cache every authentic solved question back to the bank so the next agent does not redo it:
   ```powershell
   .venv\Scripts\python.exe w:/StaralexSchoolStudies/BECE_MOCK_PAPERS/src/bece_cli.py save-solution --id Q_... --lesson "<Strand-.../Substrand-.../Lesson-...>" --answer "..." --steps "..." [--sympy-lhs "..." --sympy-rhs "..."]
   ```
8. **Update the tracker** status only after the lesson + exercises + answers are actually delivered (e.g. `Status: [x] Done — 40 Qs`).

### Mode B — `check available questions and teach from those` / `what can we revise?`

1. List topics that already have bank questions:
   ```powershell
   .venv\Scripts\python.exe w:/StaralexSchoolStudies/BECE_MOCK_PAPERS/src/bece_cli.py coverage --list-topics --has-questions
   ```
   Output is sorted by question count. That is your revision menu.
2. Pick the next useful topic (user choice if they want; else highest-value unfinished topic in the tracker that also has questions).
3. Run the same teach → questions → solutions loop as Mode A, step 3–8.

## Coverage honesty

Before you claim “these are ALL the questions for this topic”:

- `totals.questions` — what is tagged today
- `totals.solutions_cached` / `solution_rate` — how many already have worked answers
- `completeness_check.fts_keyword_hits_tagged_elsewhere` — keyword hits outside the topic (review before claiming ALL)

If coverage is thin, say the number out loud and fill with generated questions. Never pretend the bank is complete.

## NaCCA codes collide across subjects

`B7.2.2.1.3` = Algebraic Expressions (Mathematics) **and** Presentation Software (Computing). Always pass `--subject`. Treat `(subject, code)` as the key.

## CLI (project venv)

```powershell
.venv\Scripts\python.exe w:/StaralexSchoolStudies/BECE_MOCK_PAPERS/src/bece_cli.py <cmd>
```

| Command | Use |
|---|---|
| `coverage --list-topics --has-questions` | Topics that have questions (Mode B) |
| `coverage --topic "..." --subject ...` | Honest completeness for one topic |
| `query --indicator B9.2.2.1.3 --subject Mathematics` | Authentic questions for a lesson |
| `search "factorise by grouping"` | Keyword/semantic hunt when the indicator is vague |
| `indicators --subject ... --search "factor"` | Resolve indicator codes and text |
| `diagrams --indicator B9.3.1.2.1` | Find canonical TikZ diagram templates and companion skills |
| `save-solution --id Q_...` | Cache a worked answer |
| `stats` | Bank-wide telemetry |

Bank DB: `w:/StaralexSchoolStudies/BECE_MOCK_PAPERS/data/metadata/catalog.db`

## Canonical TikZ Diagrams & Visual Assets

The repository contains 46 canonical BECE Mathematics diagram templates (covering Basic 7, 8, and 9) located in `data/diagrams/math_redrawn/` and mapped 1:1 to companion skills in `.agents/skills/diagram-XX-.../SKILL.md`.

- **Strict Asset Format Policy:** All diagrams must exist and be committed **ONLY as `.tex` (source) and 300 DPI `.png` (raster)**. Strictly **NO `.pdf`** and **NO `.svg`** files may be stored or retained. All intermediate compilation files (`.pdf`, `.aux`, `.log`) must be immediately unlinked.
- **Automated Lookup:** When calling `bece_cli.py query --indicator <code>`, matching canonical diagram templates and clickable links to `.png` and skill files are automatically output in the header.
- **Direct CLI Inspection:**
  ```powershell
  # List all diagrams
  .venv\Scripts\python.exe w:/StaralexSchoolStudies/BECE_MOCK_PAPERS/src/bece_cli.py diagrams --format markdown
  # Query diagrams by indicator, grade, or topic search
  .venv\Scripts\python.exe w:/StaralexSchoolStudies/BECE_MOCK_PAPERS/src/bece_cli.py diagrams --indicator B7.3.1.2.3
  .venv\Scripts\python.exe w:/StaralexSchoolStudies/BECE_MOCK_PAPERS/src/bece_cli.py diagrams --search "circle"
  ```
- **Diagram Adaptation in Lessons:** When teaching a topic or generating new exercises with diagrams, use the relevant canonical TikZ template as the base geometry to guarantee authentic BECE styling, 0.8 pt line weights, Computer Modern font matching, proper label clearance, and standard dimensions.
