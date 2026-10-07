import asyncio
import logging
import re
from typing import Dict, List, Set, Tuple
from urllib.parse import parse_qs, urljoin, urlparse
import httpx
from bs4 import BeautifulSoup
from src.config import (
    EXAM_KEYWORDS,
    MAX_CONCURRENT_REQUESTS,
    SUBJECTS,
    TARGET_EXTENSIONS,
    USER_AGENT,
)
from src.database import CatalogDatabase
from src.download_pipeline import DownloadPipeline

logger = logging.getLogger("SitemapHarvester")

SITEMAP_INDEXES: List[str] = [
    "https://ghanaeducation.org/sitemap_index.xml",
    "https://passco.com.gh/sitemap.xml",
    "https://ghlearner.com/sitemap.xml",
    "https://pbpagezlimited.com/sitemap_index.xml",
    "https://becezone.com/sitemap.xml",
    "https://ghstudents.com/sitemap_index.xml",
    "https://mickinetsystems.com/sitemap.xml",
]


class SitemapHarvester:
    """Discovers and downloads high-volume BECE mock papers directly from XML sitemaps and target posts."""

    def __init__(self, database: CatalogDatabase = None):
        self.db = database or CatalogDatabase()
        self.pipeline = DownloadPipeline(database=self.db)
        self.headers = {"User-Agent": USER_AGENT}

    @staticmethod
    def resolve_external_storage_url(url: str) -> str:
        """Converts Google Drive / Docs view links to direct downloadable streams."""
        # drive.google.com/file/d/<id>/view
        m = re.search(r"drive\.google\.com/file/d/([a-zA-Z0-9_-]+)", url)
        if m:
            return f"https://drive.google.com/uc?export=download&id={m.group(1)}"

        # drive.google.com/open?id=<id>
        if "drive.google.com/open" in url:
            qs = parse_qs(urlparse(url).query)
            if "id" in qs:
                return f"https://drive.google.com/uc?export=download&id={qs['id'][0]}"

        # docs.google.com/document/d/<id>
        m_doc = re.search(r"docs\.google\.com/document/d/([a-zA-Z0-9_-]+)", url)
        if m_doc:
            return f"https://docs.google.com/document/d/{m_doc.group(1)}/export?format=pdf"

        return url

    async def fetch_xml(self, client: httpx.AsyncClient, url: str) -> List[str]:
        """Fetches an XML sitemap and returns all <loc> values."""
        try:
            r = await client.get(url, timeout=15.0)
            if r.status_code != 200:
                return []
            soup = BeautifulSoup(r.text, "xml")
            return [loc.text.strip() for loc in soup.find_all("loc") if loc.text]
        except Exception as e:
            logger.warning(f"Failed to fetch XML sitemap {url}: {e}")
            return []

    async def get_all_target_urls(self, client: httpx.AsyncClient) -> Tuple[List[str], List[str]]:
        """
        Recursively unpacks sitemap indexes and extracts:
        1. Direct document links (.pdf, .docx, .doc)
        2. Relevant article/page URLs matching target exam subjects
        """
        direct_docs: Set[str] = set()
        target_articles: Set[str] = set()

        all_keywords = (
            SUBJECTS["Mathematics"]
            + SUBJECTS["Computing_ICT"]
            + SUBJECTS["CDT_CAD"]
        )

        for sitemap_url in SITEMAP_INDEXES:
            logger.info(f"Unpacking sitemap: {sitemap_url}")
            locs = await self.fetch_xml(client, sitemap_url)

            # Check if this is a sitemap index containing child sitemaps
            child_sitemaps = [l for l in locs if l.endswith(".xml")]
            if child_sitemaps:
                # Limit child sitemaps to post/page sitemaps
                relevant_children = [
                    cs for cs in child_sitemaps
                    if any(term in cs.lower() for term in ["post", "page", "upload", "passco", "bece"])
                ]
                for cs in relevant_children:
                    child_locs = await self.fetch_xml(client, cs)
                    locs.extend(child_locs)

            for u in locs:
                u_lower = u.lower()
                # Check for direct documents in sitemaps
                if any(u_lower.endswith(ext) or ext in u_lower for ext in TARGET_EXTENSIONS):
                    if not self.db.is_url_visited(u):
                        direct_docs.add(u)
                    continue

                # Filter articles relevant to our specific BECE subjects
                has_subject = any(k in u_lower for k in all_keywords)
                has_exam = any(e in u_lower for e in ["bece", "mock", "pasco", "past-question", "scheme", "question"])

                if has_subject and has_exam:
                    if not self.db.is_url_visited(u):
                        target_articles.add(u)

        return list(direct_docs), list(target_articles)

    async def extract_documents_from_article(self, client: httpx.AsyncClient, article_url: str) -> List[str]:
        """Extracts direct PDF/DOCX and cloud storage links embedded in an article."""
        found_links: List[str] = []
        try:
            r = await client.get(article_url, timeout=12.0)
            if r.status_code != 200:
                self.db.record_url_visited(article_url, r.status_code)
                return []

            self.db.record_url_visited(article_url, 200)
            soup = BeautifulSoup(r.text, "html.parser")

            # Also check if the article itself contains full questions and save as TXT
            title = soup.title.string.strip() if soup.title and soup.title.string else ""
            self.pipeline.save_html_article_as_txt(
                url=article_url,
                title=title,
                html_content=r.text,
                context_text=title
            )

            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                full_url = urljoin(article_url, href).split("#")[0]
                full_url_lower = full_url.lower()

                # Check if direct document
                if any(full_url_lower.endswith(ext) for ext in TARGET_EXTENSIONS):
                    found_links.append(full_url)
                # Check if Google Drive / Docs link
                elif "drive.google.com" in full_url_lower or "docs.google.com" in full_url_lower:
                    resolved = self.resolve_external_storage_url(full_url)
                    found_links.append(resolved)
                # Check if MediaFire link
                elif "mediafire.com/file" in full_url_lower:
                    found_links.append(full_url)

        except Exception as e:
            logger.debug(f"Error inspecting article {article_url}: {e}")

        return found_links

    async def harvest(self, max_articles: int = 150) -> int:
        """Runs the complete bulk sitemap harvest across all targets."""
        downloaded_count = 0
        semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

        async with httpx.AsyncClient(headers=self.headers, verify=False, follow_redirects=True) as client:
            direct_docs, target_articles = await self.get_all_target_urls(client)
            logger.info(f"Sitemap analysis found {len(direct_docs)} direct documents and {len(target_articles)} target articles.")

            # 1. Download all direct documents found in sitemaps
            async def download_doc(url: str):
                nonlocal downloaded_count
                async with semaphore:
                    res = await self.pipeline.download_file(url)
                    if res:
                        downloaded_count += 1
                        logger.info(f"Downloaded: {res[0].name} [{res[1]}]")

            doc_tasks = [download_doc(u) for u in direct_docs]
            if doc_tasks:
                logger.info(f"Starting batch download of {len(doc_tasks)} sitemap documents...")
                await asyncio.gather(*doc_tasks, return_exceptions=True)

            # 2. Process articles to uncover embedded documents
            articles_to_process = target_articles[:max_articles]
            logger.info(f"Processing {len(articles_to_process)} target articles for embedded mock papers...")

            async def process_article(art_url: str):
                async with semaphore:
                    embedded_links = await self.extract_documents_from_article(client, art_url)
                    for emb in embedded_links:
                        if not self.db.is_url_visited(emb):
                            await download_doc(emb)

            article_tasks = [process_article(u) for u in articles_to_process]
            if article_tasks:
                await asyncio.gather(*article_tasks, return_exceptions=True)

        self.db.export_catalog_json()
        logger.info(f"Sitemap harvest complete. Downloaded {downloaded_count} new papers.")
        return downloaded_count
