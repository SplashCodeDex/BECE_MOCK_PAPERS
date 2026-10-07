import asyncio
import logging
import re
from typing import Dict, List, Set
from urllib.parse import unquote, urlparse
import httpx
from bs4 import BeautifulSoup
from src.config import DORK_QUERIES, TARGET_EXTENSIONS, USER_AGENT

logger = logging.getLogger("DorkDiscovery")


class DorkDiscoveryEngine:
    """Discovers high-probability BECE mock document links using targeted dork queries."""

    def __init__(self):
        self.endpoint = "https://lite.duckduckgo.com/lite/"
        self.headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://lite.duckduckgo.com/",
        }

    async def search_query(self, query: str, max_results: int = 25) -> List[Dict[str, str]]:
        """Executes a single search query against DuckDuckGo Lite and returns extracted results."""
        discovered = []
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=20.0, verify=True) as client:
                response = await client.post(self.endpoint, data={"q": query})
                if response.status_code != 200:
                    return []

                soup = BeautifulSoup(response.text, "html.parser")
                rows = soup.select("table tbody tr")
                
                # In DuckDuckGo Lite, search results are formatted across table rows
                current_link = None
                current_title = None

                for link_elem in soup.select("a.result-link"):
                    href = link_elem.get("href", "")
                    if href:
                        if "uddg=" in href:
                            match = re.search(r"uddg=([^&]+)", href)
                            if match:
                                href = unquote(match.group(1))

                        title = link_elem.get_text(strip=True)
                        discovered.append({
                            "url": href,
                            "title": title,
                            "snippet": "",
                            "query": query,
                        })
                        if len(discovered) >= max_results:
                            break

        except Exception as e:
            logger.warning(f"Error querying dork '{query}': {e}")

        return discovered

    async def run_discovery(
        self,
        custom_queries: List[str] = None,
        subject_filter: str = None
    ) -> List[Dict[str, str]]:
        """Runs the discovery engine across pre-configured and custom queries."""
        from src.config import SUBJECTS
        queries_to_run = custom_queries or list(DORK_QUERIES)

        if subject_filter and subject_filter in SUBJECTS:
            keywords = SUBJECTS[subject_filter]
            queries_to_run = [
                q for q in queries_to_run
                if any(k.lower() in q.lower() for k in keywords)
            ]
            if not queries_to_run:
                queries_to_run = [
                    f'filetype:pdf "BECE" "mock" "{k}" ghana' for k in keywords[:3]
                ]

        all_results: List[Dict[str, str]] = []
        seen_urls: Set[str] = set()

        for q in queries_to_run:
            results = await self.search_query(q)
            for r in results:
                url = r["url"]
                if url not in seen_urls:
                    seen_urls.add(url)
                    all_results.append(r)
            # Polite delay between search requests
            await asyncio.sleep(0.5)

        return all_results

    @staticmethod
    def filter_direct_files(results: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Filters results down to direct binary files (.pdf, .docx, .txt)."""
        filtered = []
        for r in results:
            url_lower = r["url"].lower()
            if any(url_lower.endswith(ext) or ext in url_lower for ext in TARGET_EXTENSIONS):
                filtered.append(r)
        return filtered
