import asyncio
import logging
from pathlib import Path
from typing import List, Optional, Set
from urllib.parse import urljoin, urlparse
from crawlee.crawlers import (
    BeautifulSoupCrawler,
    BeautifulSoupCrawlingContext,
    PlaywrightCrawler,
    PlaywrightCrawlingContext,
)
from src.classifier import FileClassifier
from src.config import (
    EXAM_KEYWORDS,
    MAX_CONCURRENT_REQUESTS,
    SEED_URLS,
    TARGET_DOMAINS,
    TARGET_EXTENSIONS,
)
from src.database import CatalogDatabase
from src.download_pipeline import DownloadPipeline

logger = logging.getLogger("CrawlerEngine")


class BECEMockCrawler:
    """Unified Crawlee crawler engine for BECE and Mock Examination papers."""

    def __init__(
        self,
        mode: str = "fast",  # "fast" (BeautifulSoup) or "stealth" (Playwright)
        max_requests: int = 500,
        max_depth: int = 4,
        subject_filter: Optional[str] = None,
        database: Optional[CatalogDatabase] = None,
    ):
        self.mode = mode
        self.max_requests = max_requests
        self.max_depth = max_depth
        self.subject_filter = subject_filter
        self.db = database or CatalogDatabase()
        self.pipeline = DownloadPipeline(database=self.db)
        self.seen_urls: Set[str] = set()

    def _is_allowed_domain(self, url: str) -> bool:
        netloc = urlparse(url).netloc.lower()
        if not netloc:
            return False
        # Allow targeted domains, educational subdomains, and media/content CDNs
        if any(target in netloc for target in TARGET_DOMAINS):
            return True
        if any(ext in netloc for ext in [".gh", "edu", "drive.google.com", "scribd.com"]):
            return True
        return False

    def _is_relevant_link(self, url: str, anchor_text: str = "") -> bool:
        combined = f"{url} {anchor_text}".lower()
        # Direct document matches are always relevant
        if any(combined.endswith(ext) or ext in combined for ext in TARGET_EXTENSIONS):
            return True
        # Check relevance signals
        return any(k in combined for k in EXAM_KEYWORDS)

    async def _handle_discovered_link(self, target_url: str, anchor_text: str, current_url: str) -> Optional[str]:
        """Examines a link: downloads if document, returns URL if it should be traversed."""
        full_url = urljoin(current_url, target_url).split("#")[0]
        parsed = urlparse(full_url)
        path_lower = parsed.path.lower()

        # Check if direct document
        is_doc = any(path_lower.endswith(ext) or ext in path_lower for ext in TARGET_EXTENSIONS)
        if is_doc:
            if not self.db.is_url_visited(full_url):
                logger.info(f"Target document found: {full_url}")
                await self.pipeline.download_file(
                    url=full_url,
                    context_text=f"{anchor_text} {current_url}",
                    forced_subject=self.subject_filter,
                )
            return None

        # Check for recursive traversal relevance
        if self._is_allowed_domain(full_url) and self._is_relevant_link(full_url, anchor_text):
            if full_url not in self.seen_urls and not self.db.is_url_visited(full_url):
                self.seen_urls.add(full_url)
                return full_url

        return None

    def build_fast_crawler(self) -> BeautifulSoupCrawler:
        crawler = BeautifulSoupCrawler(
            max_requests_per_crawl=self.max_requests,
            max_crawl_depth=self.max_depth,
        )

        @crawler.router.default_handler
        async def handler(context: BeautifulSoupCrawlingContext) -> None:
            url = context.request.url
            self.db.record_url_visited(url, 200)

            # Check if this HTML page is itself an exam question article
            title = context.soup.title.string.strip() if context.soup.title and context.soup.title.string else ""
            html_text = str(context.soup)
            self.pipeline.save_html_article_as_txt(
                url=url,
                title=title,
                html_content=html_text,
                context_text=title
            )

            # Discover links and collect document downloads
            urls_to_enqueue = []
            download_tasks = []
            for a_tag in context.soup.find_all("a", href=True):
                href = a_tag["href"]
                anchor_text = a_tag.get_text(strip=True)
                full_url = urljoin(url, href).split("#")[0]
                path_lower = urlparse(full_url).path.lower()

                # Check if direct document
                is_doc = any(path_lower.endswith(ext) or ext in path_lower for ext in TARGET_EXTENSIONS)
                if is_doc:
                    if not self.db.is_url_visited(full_url):
                        download_tasks.append(
                            self.pipeline.download_file(
                                url=full_url,
                                context_text=f"{anchor_text} {url}",
                                forced_subject=self.subject_filter,
                            )
                        )
                elif self._is_allowed_domain(full_url) and self._is_relevant_link(full_url, anchor_text):
                    if full_url not in self.seen_urls and not self.db.is_url_visited(full_url):
                        self.seen_urls.add(full_url)
                        urls_to_enqueue.append(full_url)

            if download_tasks:
                await asyncio.gather(*download_tasks, return_exceptions=True)

            if urls_to_enqueue:
                await context.add_requests(urls_to_enqueue)

        return crawler

    def build_stealth_crawler(self) -> PlaywrightCrawler:
        crawler = PlaywrightCrawler(
            max_requests_per_crawl=self.max_requests,
            max_crawl_depth=self.max_depth,
            headless=True,
            browser_type="chromium",
        )

        @crawler.router.default_handler
        async def handler(context: PlaywrightCrawlingContext) -> None:
            url = context.request.url
            self.db.record_url_visited(url, 200)

            page = context.page
            title = await page.title()
            content = await page.content()

            # Attempt TXT question extraction
            self.pipeline.save_html_article_as_txt(
                url=url,
                title=title,
                html_content=content,
                context_text=title
            )

            # Extract dynamic links via Playwright DOM
            links = await page.evaluate(
                """() => Array.from(document.querySelectorAll('a[href]')).map(a => ({
                    href: a.href,
                    text: a.innerText || a.textContent || ''
                }))"""
            )

            urls_to_enqueue = []
            download_tasks = []
            for item in links:
                full_url = urljoin(url, item["href"]).split("#")[0]
                path_lower = urlparse(full_url).path.lower()

                is_doc = any(path_lower.endswith(ext) or ext in path_lower for ext in TARGET_EXTENSIONS)
                if is_doc:
                    if not self.db.is_url_visited(full_url):
                        download_tasks.append(
                            self.pipeline.download_file(
                                url=full_url,
                                context_text=f"{item['text']} {url}",
                                forced_subject=self.subject_filter,
                            )
                        )
                elif self._is_allowed_domain(full_url) and self._is_relevant_link(full_url, item["text"]):
                    if full_url not in self.seen_urls and not self.db.is_url_visited(full_url):
                        self.seen_urls.add(full_url)
                        urls_to_enqueue.append(full_url)

            if download_tasks:
                await asyncio.gather(*download_tasks, return_exceptions=True)

            if urls_to_enqueue:
                await context.add_requests(urls_to_enqueue)

        return crawler

    async def run(self, initial_seeds: Optional[List[str]] = None) -> None:
        seeds = initial_seeds or list(SEED_URLS)
        logger.info(f"Starting BECEMockCrawler [{self.mode.upper()}] with {len(seeds)} seeds...")

        if self.mode == "stealth":
            crawler = self.build_stealth_crawler()
        else:
            crawler = self.build_fast_crawler()

        await crawler.run(seeds)
        self.db.export_catalog_json()
        logger.info("Crawl completed successfully. Catalog updated.")
