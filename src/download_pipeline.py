import hashlib
import logging
import re
import ssl
from pathlib import Path
from typing import Optional, Set, Tuple
from urllib.parse import urlparse
import httpx
from bs4 import BeautifulSoup
from src.classifier import FileClassifier
from src.config import (
    MAX_DOWNLOAD_SIZE_BYTES,
    REQUEST_TIMEOUT_SECONDS,
    TARGET_EXTENSIONS,
    USER_AGENT,
)
from src.database import CatalogDatabase

logger = logging.getLogger("DownloadPipeline")


class DownloadPipeline:
    """Asynchronous downloading, deduplication, content extraction, and file saving pipeline."""

    def __init__(self, database: Optional[CatalogDatabase] = None):
        self.db = database or CatalogDatabase()
        self.in_flight_urls: Set[str] = set()
        self.headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml,application/pdf,*/*",
            "Accept-Language": "en-US,en;q=0.9",
        }

    async def _fetch_url(self, url: str) -> Optional[httpx.Response]:
        """Fetches URL with standard SSL verification first, falling back to unverified if SSL handshake fails."""
        try:
            async with httpx.AsyncClient(
                headers=self.headers,
                timeout=REQUEST_TIMEOUT_SECONDS,
                follow_redirects=True,
                verify=True,
            ) as client:
                return await client.get(url)
        except (httpx.ConnectError, ssl.SSLError) as ssl_err:
            logger.warning(f"SSL verification failed for {url} ({ssl_err}); falling back to unverified request.")
            try:
                async with httpx.AsyncClient(
                    headers=self.headers,
                    timeout=REQUEST_TIMEOUT_SECONDS,
                    follow_redirects=True,
                    verify=False,
                ) as fallback_client:
                    return await fallback_client.get(url)
            except Exception as e:
                logger.debug(f"Unverified fetch also failed for {url}: {e}")
                return None
        except Exception as e:
            logger.debug(f"Failed to fetch {url}: {e}")
            return None

    async def download_file(
        self,
        url: str,
        context_text: str = "",
        forced_subject: Optional[str] = None
    ) -> Optional[Tuple[Path, str, str]]:
        """
        Downloads a document (PDF/DOCX/TXT), deduplicates via SHA-256,
        organizes into subject directory, and logs into database.
        Returns (saved_path, subject, sha256) or None if skipped/failed.
        """
        if url in self.in_flight_urls or self.db.is_url_visited(url):
            return None

        self.in_flight_urls.add(url)
        try:
            parsed = urlparse(url)
            path_lower = parsed.path.lower()
            domain = parsed.netloc

            # Determine file extension
            extension = None
            for ext in TARGET_EXTENSIONS:
                if path_lower.endswith(ext):
                    extension = ext
                    break

            if not extension:
                for ext in TARGET_EXTENSIONS:
                    if ext in url.lower():
                        extension = ext
                        break

            if not extension:
                extension = ".pdf"  # default document assumption if routed here

            response = await self._fetch_url(url)
            if not response or response.status_code != 200:
                if response:
                    self.db.record_url_visited(url, response.status_code)
                return None

            content = response.content
            if not content or len(content) > MAX_DOWNLOAD_SIZE_BYTES:
                return None

            # Calculate SHA-256 Hash
            sha256 = hashlib.sha256(content).hexdigest()

            # Deduplication / permanent reject ledger (survives local file deletion)
            if self.db.is_content_known(sha256):
                self.db.record_url_visited(url, 200)
                return None

            # Detect subject (via URL context + deep document byte inspection)
            subject = forced_subject or FileClassifier.detect_subject_from_bytes(
                content=content,
                extension=extension,
                text_context=f"{url} {context_text}"
            )

            # Tombstone non-exam junk so it is never fetched again after delete
            reject_reason = FileClassifier.reject_reason(
                content=content,
                extension=extension,
                text_context=f"{url} {context_text}",
                subject=subject,
            )
            if reject_reason:
                self.db.record_rejected_content(
                    sha256=sha256,
                    reason=reject_reason,
                    original_url=url,
                    file_name=Path(parsed.path).name or "",
                    file_type=extension,
                    details=f"subject={subject}; {context_text[:180]}",
                )
                self.db.record_url_visited(url, 200)
                logger.debug(f"Rejected content {sha256[:12]} ({reject_reason}) from {url}")
                return None

            # Extract raw file name
            raw_filename = Path(parsed.path).name or f"document{extension}"
            clean_filename = FileClassifier.sanitize_filename(
                raw_name=raw_filename,
                subject=subject,
                sha256=sha256,
                extension=extension,
                context_text=f"{url} {context_text}"
            )

            dest_path = FileClassifier.get_destination_path(
                subject=subject,
                extension=extension,
                clean_filename=clean_filename
            )

            # Save file to disk
            dest_path.write_bytes(content)

            # Log to database
            self.db.save_harvested_file(
                sha256=sha256,
                original_url=url,
                file_name=clean_filename,
                file_type=extension,
                subject=subject,
                file_size=len(content),
                local_path=str(dest_path),
                source_domain=domain
            )
            self.db.record_url_visited(url, 200)

            return dest_path, subject, sha256

        except Exception as e:
            logger.debug(f"Download pipeline error for {url}: {e}")
            return None
        finally:
            self.in_flight_urls.discard(url)

    def save_html_article_as_txt(
        self,
        url: str,
        title: str,
        html_content: str,
        context_text: str = ""
    ) -> Optional[Tuple[Path, str, str]]:
        """
        Extracts questions and answers text from an educational blog/article
        and saves it neatly as a .txt document if it contains exam questions.
        """
        soup = BeautifulSoup(html_content, "html.parser")

        # Strip navigation, script, style, comments
        for elem in soup(["script", "style", "nav", "footer", "header", "aside"]):
            elem.decompose()

        main_text = soup.get_text(separator="\n", strip=True)
        if len(main_text) < 300:
            return None

        # Verify it has question indicators
        text_lower = main_text.lower()
        question_signals = ["question", "section a", "section b", "paper 1", "paper 2", "objective", "marks", "answer"]
        if sum(1 for s in question_signals if s in text_lower) < 2:
            return None

        sha256 = hashlib.sha256(main_text.encode("utf-8")).hexdigest()
        if self.db.is_content_known(sha256):
            return None

        if not FileClassifier.looks_like_exam_content(main_text):
            self.db.record_rejected_content(
                sha256=sha256,
                reason="no_exam_signals",
                original_url=url,
                file_name=title or "",
                file_type=".txt",
                details="HTML article without exam signals",
            )
            return None

        subject = FileClassifier.detect_subject(f"{url} {title} {context_text} {main_text[:2000]}")
        clean_filename = FileClassifier.sanitize_filename(
            raw_name=title or "exam_questions",
            subject=subject,
            sha256=sha256,
            extension=".txt",
            context_text=f"{url} {title}"
        )

        dest_path = FileClassifier.get_destination_path(
            subject=subject,
            extension=".txt",
            clean_filename=clean_filename
        )

        formatted_content = (
            f"SOURCE URL: {url}\n"
            f"TITLE: {title}\n"
            f"SUBJECT: {subject}\n"
            f"{'='*60}\n\n"
            f"{main_text}\n"
        )

        dest_path.write_text(formatted_content, encoding="utf-8")

        domain = urlparse(url).netloc
        self.db.save_harvested_file(
            sha256=sha256,
            original_url=url,
            file_name=clean_filename,
            file_type="txt",
            subject=subject,
            file_size=len(formatted_content.encode("utf-8")),
            local_path=str(dest_path),
            source_domain=domain
        )
        self.db.record_url_visited(url, 200)

        return dest_path, subject, sha256
