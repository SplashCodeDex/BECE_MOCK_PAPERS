from pathlib import Path
from typing import Dict, List

# Base Directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
HARVESTED_DIR = DATA_DIR / "harvested"
METADATA_DIR = DATA_DIR / "metadata"
STORAGE_DIR = DATA_DIR / "crawlee_storage"
DATABASE_PATH = METADATA_DIR / "catalog.db"
CATALOG_JSON_PATH = METADATA_DIR / "catalog.json"

# Supported target file extensions
TARGET_EXTENSIONS = [".pdf", ".docx", ".doc", ".txt"]

# Subject Taxonomy
SUBJECTS = {
    "Mathematics": [
        "math", "mathematics", "maths", "core maths", "general maths",
        "bece maths", "jhs maths", "arithmetic"
    ],
    "Computing_ICT": [
        "computing", "ict", "information and communication technology",
        "computer studies", "bece computing", "ict past questions", "ict mock"
    ],
    "CDT_CAD": [
        "career technology", "career tech", "creative arts", "creative arts and design",
        "craft and design", "cdt", "cad", "basic design and technology",
        "bdt", "pre-technical", "pretechnical", "pre-tech", "pretech",
        "technical skills", "home economics", "home-economics", "home econs",
        "pts", "visual arts", "performing arts", "craft"
    ],
    "General_Unclassified": [
        "mock", "bece", "past questions", "pasco", "exam", "marking scheme"
    ]
}

# High-Priority Ghana Educational Portals & Exam Repositories
TARGET_DOMAINS: List[str] = [
    "waecgh.org",
    "ghana.waecdirect.org",
    "ghstudents.com",
    "ghlearner.com",
    "passco.com.gh",
    "ghanaeducation.org",
    "mickinetsystems.com",
    "pbpagezlimited.com",
    "becezone.com",
    "kuulchat.com",
    "bestbrainexams.com",
    "gbassessment.com",
    "skulmanager.com",
    "teachersghana.com",
    "edunewsgh.com",
    "geshub.org",
    "becepastquestions.com"
]

# Primary Seed URLs across targets
SEED_URLS: List[str] = [
    "https://waecgh.org/bece-guidelines-scheme-and-structure",
    "https://ghstudents.com/bece-past-questions-and-answers/",
    "https://ghlearner.com/past-questions/bece",
    "https://ghlearner.com/mock-exams",
    "https://passco.com.gh/bece-past-questions",
    "https://passco.com.gh/mock-questions",
    "https://ghanaeducation.org/category/bece-questions/",
    "https://ghanaeducation.org/category/mock-papers/",
    "https://mickinetsystems.com/bece-past-questions/",
    "https://mickinetsystems.com/gbat-mock-questions/",
    "https://pbpagezlimited.com/bece-mock-questions/",
    "https://becezone.com/bece-past-questions/",
    "https://kuulchat.com/bece-questions",
    "https://bestbrainexams.com/downloads/",
    "https://gbassessment.com/resources/",
    # --- Computing / ICT multi-year (gap: bank is 2024-only) ---
    "https://ghlearner.com/bece/computing/exams",
    "https://passco.com.gh/bece-past-questions/ict",
    "https://mickinetsystems.com/bece-ict-past-questions/",
    "https://ghanaeducation.org/category/ict-questions/",
    "https://becezone.com/ict/",
    # --- CDT / Pre-tech / BDT after 2017 (gap: bank stops at 2017) ---
    "https://mickinetsystems.com/bece-pre-technical-skills-past-questions/",
    "https://mickinetsystems.com/bece-basic-design-technology-past-questions/",
    "https://passco.com.gh/bece-past-questions/basic-design-technology",
    "https://ghanaeducation.org/category/career-technology/",
    "https://ghlearner.com/bece/career-technology/exams",
    # --- Maths 2013-2025 gap ---
    "https://passco.com.gh/bece-past-questions/mathematics",
    "https://ghlearner.com/bece/mathematics/exams",
    "https://mickinetsystems.com/bece-mathematics-past-questions/",
]

# Common Examination Terms for Relevance Scoring
EXAM_KEYWORDS: List[str] = [
    "bece", "mock", "past questions", "pasco", "marking scheme",
    "chief examiner", "trial questions", "sample questions", "waec", "ges",
    "common core", "ccp", "standards-based"
]

# Dork Search Query Templates for Deep Web Discovery
DORK_QUERIES: List[str] = [
    'site:ghlearner.com (filetype:pdf OR filetype:docx) ("bece" OR "mock")',
    'site:passco.com.gh (filetype:pdf OR filetype:docx) ("bece" OR "mock")',
    'site:ghanaeducation.org "download" ("bece" OR "mock") (filetype:pdf OR filetype:docx)',
    'site:mickinetsystems.com ("bece" OR "mock") (filetype:pdf OR filetype:docx)',
    'site:pbpagezlimited.com ("bece" OR "mock") (filetype:pdf OR filetype:docx)',
    'filetype:pdf "BECE" "mock" "computing" ghana',
    'filetype:pdf "BECE" "mock" "mathematics" ghana',
    'filetype:pdf "BECE" "mock" "career technology" ghana',
    'filetype:pdf "BECE" "mock" "creative arts" ghana',
    'filetype:docx "BECE" "mock" ("maths" OR "computing" OR "career technology")',
    'filetype:pdf "best brain" "mock" "bece" questions',
    'filetype:pdf "gbat" "mock" "bece" marking scheme',
    'site:drive.google.com/file/d/ ("BECE" OR "mock") ("maths" OR "computing" OR "CDT")',
    # --- Computing / ICT multi-year harvest ---
    'filetype:pdf "BECE" "ICT" "past questions" ghana',
    'filetype:pdf "BECE" "computing" "2018" OR "2019" OR "2020" OR "2021" OR "2022" OR "2023"',
    'filetype:pdf "BECE" "computing" "Paper 1" "Paper 2" answers',
    'site:ghlearner.com (ICT OR computing) (bece OR mock) filetype:pdf',
    'site:passco.com.gh (ICT OR computing) filetype:pdf',
    # --- CDT / Pre-tech / BDT after 2017 ---
    'filetype:pdf "BECE" "pre-technical skills" OR "pre technical" past questions',
    'filetype:pdf "BECE" "basic design and technology" past questions',
    'filetype:pdf "BECE" "career technology" mock 2020 OR 2021 OR 2022 OR 2023 OR 2024',
    'filetype:pdf "home economics" "BECE" past questions ghana',
    'site:mickinetsystems.com ("pre-technical" OR "basic design" OR "career technology") filetype:pdf',
    # --- Maths 2013-2025 gap ---
    'filetype:pdf "BECE" "mathematics" "2018" OR "2019" OR "2020" OR "2021" past questions',
    'filetype:pdf "BECE" "mathematics" mock "2023" OR "2024" OR "2025" questions',
    'site:passco.com.gh mathematics BECE filetype:pdf',
    'site:ghlearner.com mathematics bece filetype:pdf',
]

# Crawler Settings
USER_AGENT: str = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

REQUEST_TIMEOUT_SECONDS: int = 30
MAX_CONCURRENT_REQUESTS: int = 10
MAX_DOWNLOAD_SIZE_BYTES: int = 150 * 1024 * 1024  # 150 MB safety limit
