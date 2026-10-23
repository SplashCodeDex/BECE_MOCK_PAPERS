# BECE & Mock Examination Paper Web Harvesting System

High-performance, production-grade focused crawler and document harvesting architecture tailored for Ghana WAEC and GES Junior High School (JHS) BECE and Mock Examination papers.

## Target Curriculum Subjects
1. **Mathematics** (Core Maths, JHS 1-3, WAEC Past Papers & Mock Exams)
2. **Computing / ICT** (Information and Communication Technology, New Curriculum Computing, WAEC Sample & Mock Sets)
3. **CDT / CAD / BDT** (Career Technology, Creative Arts and Design, Craft & Design, Pre-Technical Skills, Home Economics)

---

## Directory & Data Architecture

All harvested files are deduplicated using cryptographic **SHA-256** checksums and organized neatly by **Subject** and **Format**:

```
w:\StaralexSchoolStudies\BECE_MOCK_PAPERS\
├── data/
│   ├── harvested/
│   │   ├── Mathematics/
│   │   │   ├── pdf/
│   │   │   ├── docx/
│   │   │   ├── doc/
│   │   │   └── txt/
│   │   ├── Computing_ICT/
│   │   │   ├── pdf/
│   │   │   ├── docx/
│   │   │   ├── doc/
│   │   │   └── txt/
│   │   ├── CDT_CAD/
│   │   │   ├── pdf/
│   │   │   ├── docx/
│   │   │   └── txt/
│   │   └── General_Unclassified/
│   │       ├── pdf/
│   │       ├── docx/
│   │       └── txt/
│   └── metadata/
│       ├── catalog.db     # SQLite database tracking file hashes, original URLs, sizes & dates
│       └── catalog.json   # JSON export of all indexed papers
├── src/
│   ├── config.py             # Target portals, seeds, subjects, dork patterns
│   ├── database.py           # SQLite WAL connection manager & deduplication
│   ├── classifier.py         # Subject classification & filename sanitization
│   ├── download_pipeline.py  # Asynchronous document stream downloader (.pdf, .docx, .txt)
│   ├── dorker.py             # Targeted search engine discovery engine
│   └── crawler.py            # Crawlee-powered spider (Fast BeautifulSoup + Stealth Playwright)
├── run_harvester.py          # Unified CLI entry point with Rich terminal dashboard
└── requirements.txt
```

---

## Source Targets Included
- **Official Examination Portals:** WAEC Ghana (`waecgh.org`, `ghana.waecdirect.org`)
- **Curriculum & Syllabus Repositories:** GHSyllabus / GHStudents (`ghstudents.com`)
- **Mock & Past Paper Aggregators:**
  - GhLearner (`ghlearner.com`)
  - Passco Ghana (`passco.com.gh`)
  - Ghana Education News (`ghanaeducation.org`, `ghanaeducationnews.org`)
  - Mickinet Systems (`mickinetsystems.com`)
  - PB Pagez Limited (`pbpagezlimited.com`)
  - BECE Zone (`becezone.com`)
  - Kuulchat Educational Portal (`kuulchat.com`)
  - Best Brain Examinations (`bestbrainexams.com`)
  - GB Assessment / GBAT (`gbassessment.com`)

---

## Usage Commands

### 1. View Current Harvest Catalog & Statistics
```powershell
python run_harvester.py --mode stats
```

### 2. Run High-Speed Crawlee Spider
```powershell
# Crawl across high-yield seed targets (BeautifulSoup engine)
python run_harvester.py --mode crawl --max-requests 50

# Crawl with Playwright headless stealth browser (for Cloudflare / JS-rendered portals)
python run_harvester.py --mode crawl --crawler-mode stealth --max-requests 50
```

### 3. Run Targeted Dorking Discovery Engine
```powershell
# Discover and harvest across all subjects
python run_harvester.py --mode dork

# Target a specific subject
python run_harvester.py --mode dork --subject Computing_ICT
python run_harvester.py --mode dork --subject Mathematics
python run_harvester.py --mode dork --subject CDT_CAD
```

### 4. Full Pipeline (Dork Discovery + Deep Crawl)
```powershell
python run_harvester.py --mode full --max-requests 100
```

### 5. Topic Coverage Report (Lesson Agents)
Resolve a learning topic to NaCCA substrand indicators and measure whether "ALL questions for this topic" is actually true (tagged counts, solutions cached, review debt, mis-tags):

```powershell
python w:/StaralexSchoolStudies/BECE_MOCK_PAPERS/src/bece_cli.py coverage --list-topics --subject Mathematics
python w:/StaralexSchoolStudies/BECE_MOCK_PAPERS/src/bece_cli.py coverage --topic "Algebraic Expressions" --subject Mathematics
```

Use the project virtualenv so SymPy verification imports resolve:
```powershell
.venv\Scripts\python.exe w:/StaralexSchoolStudies/BECE_MOCK_PAPERS/src/bece_cli.py stats
```

### 6. Adding New Harvest Sources
Edit **`src/config.py` only** (then re-run crawl/dork):

1. `TARGET_DOMAINS` — add the host  
2. `SEED_URLS` — add listing / download pages  
3. `DORK_QUERIES` — add `site:... filetype:pdf ("bece" OR "mock")` lines  
4. Optional: insert a `sources` row (`name`, `domain`, `url`, `trusted`) for provenance  

```powershell
python run_harvester.py --mode crawl --max-requests 100
python run_harvester.py --mode dork --subject Mathematics
```

### 7. Permanent Reject Ledger (No Re-Downloads of Junk)
Content SHA-256s of non-exam junk (lesson notes, textbooks, wrong papers) are tombstoned in `rejected_content` **forever**. Deleting the local file does **not** allow a future crawl to fetch the same bytes again.

```powershell
# After deleting a junk file, permanently block its content hash
.venv\Scripts\python.exe src/bece_cli.py reject-content --file path/to/junk.pdf --reason not_exam_paper

# Or by hash / URL
.venv\Scripts\python.exe src/bece_cli.py reject-content --sha256 <hash> --url <original> --reason no_exam_signals

# Inspect
.venv\Scripts\python.exe src/bece_cli.py reject-content --list
```

Reasons: `not_exam_paper` | `no_exam_signals` | `unclassified_wrong_subject` | `manual_reject` | `duplicate`

---

## 8. Diagram Asset Standards & Policy

High-fidelity past-paper diagrams are authored in LaTeX / TikZ under [`data/diagrams/math_redrawn/`](file:///w:/StaralexSchoolStudies/BECE_MOCK_PAPERS/data/diagrams/math_redrawn).

- **Format Policy (PNG & TeX Only):** Diagrams exist strictly as 300 DPI `.png` alongside the master `.tex` source code.
- **Strict Prohibition (No PDF or SVG Diagrams):** Neither `.pdf` nor `.svg` files may be committed, retained, or generated for diagrams. Any intermediate `.pdf` or `.svg` files generated during compilation must be purged immediately after rasterizing to PNG.
- **Visual Verification Gate:** Every diagram must be inspected as a 300 DPI `.png` before being embedded into sample mock papers or curriculum lesson exercises.
