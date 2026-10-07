import argparse
import asyncio
import logging
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.crawler import BECEMockCrawler
from src.database import CatalogDatabase
from src.dorker import DorkDiscoveryEngine
from src.download_pipeline import DownloadPipeline

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console(force_terminal=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)


def print_banner() -> None:
    banner = """
    +================================================================+
    |       BECE & MOCK EXAMINATION PAPER HARVESTING SYSTEM          |
    |       Curriculum: Mathematics | Computing/ICT | CDT/CAD        |
    |       Targets: WAEC, GHSyllabus, GhLearner, Passco & Hubs      |
    |       Formats: PDF | DOCX | TXT                                |
    +================================================================+
    """
    console.print(Panel(banner, style="bold cyan"))


def display_stats(db: CatalogDatabase) -> None:
    stats = db.get_stats()
    
    table = Table(title="[bold green]Harvested Documents Catalog Status[/bold green]", show_header=True)
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    table.add_row("Total Files Harvested", str(stats["total_harvested_files"]))
    table.add_row("Total URLs Indexed / Visited", str(stats["visited_urls"]))

    # Subject breakdown
    subj_lines = [f"{k}: {v}" for k, v in stats["subjects"].items()]
    table.add_row("By Subject", "\n".join(subj_lines) if subj_lines else "None")

    # Format breakdown
    type_lines = [f".{k}: {v}" for k, v in stats["file_types"].items()]
    table.add_row("By Format", "\n".join(type_lines) if type_lines else "None")

    console.print(table)


async def run_dork_mode(subject_filter: str = None) -> None:
    console.print("[bold yellow]Starting Targeted Dork Discovery Engine...[/bold yellow]")
    dorker = DorkDiscoveryEngine()
    db = CatalogDatabase()
    pipeline = DownloadPipeline(database=db)

    results = await dorker.run_discovery(subject_filter=subject_filter)
    console.print(f"[green]Discovered {len(results)} potential examination links.[/green]")

    direct_files = dorker.filter_direct_files(results)
    console.print(f"[cyan]Found {len(direct_files)} direct PDF / DOCX / TXT documents. Downloading...[/cyan]")

    downloaded = 0
    for item in direct_files:
        url = item["url"]
        context_text = f"{item['title']} {item['snippet']}"
        res = await pipeline.download_file(url, context_text=context_text)
        if res:
            saved_path, subject, _ = res
            console.print(f"  [bold green][OK][/bold green] [{subject}] {saved_path.name}")
            downloaded += 1

    console.print(f"[bold green]Successfully downloaded {downloaded} new unique files.[/bold green]")
    db.export_catalog_json()


async def run_crawler_mode(
    crawler_mode: str = "fast",
    max_requests: int = 200,
    max_depth: int = 3,
    subject_filter: str = None,
) -> None:
    console.print(f"[bold yellow]Initializing Crawlee Spider [{crawler_mode.upper()}]...[/bold yellow]")
    db = CatalogDatabase()
    crawler = BECEMockCrawler(
        mode=crawler_mode,
        max_requests=max_requests,
        max_depth=max_depth,
        subject_filter=subject_filter,
        database=db,
    )
    await crawler.run()


async def main() -> None:
    parser = argparse.ArgumentParser(description="BECE & Mock Paper Web Harvesting System")
    parser.add_argument(
        "--mode",
        choices=["dork", "crawl", "sitemap", "full", "bulk", "reorganize", "stats"],
        default="bulk",
        help="Operation mode: dork, crawl, sitemap, full, bulk (all combined), reorganize (reclassify), stats",
    )
    parser.add_argument(
        "--crawler-mode",
        choices=["fast", "stealth"],
        default="fast",
        help="Crawlee engine: fast (BeautifulSoup) or stealth (Playwright)",
    )
    parser.add_argument(
        "--subject",
        choices=["Mathematics", "Computing_ICT", "CDT_CAD", "all"],
        default="all",
        help="Filter specific target subject",
    )
    parser.add_argument(
        "--max-requests",
        type=int,
        default=100,
        help="Maximum requests for Crawlee deep crawling",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=3,
        help="Maximum link recursion depth",
    )

    args = parser.parse_args()
    print_banner()

    db = CatalogDatabase()
    subj_filter = None if args.subject == "all" else args.subject

    if args.mode == "stats":
        display_stats(db)
        return

    if args.mode == "reorganize":
        from src.organizer import reclassify_and_reorganize
        console.print("[bold yellow]Reclassifying harvested documents using content inspection...[/bold yellow]")
        cnt = reclassify_and_reorganize()
        console.print(f"[bold green]Reclassified {cnt} files.[/bold green]")
        display_stats(db)
        return

    if args.mode in ["sitemap", "bulk"]:
        from src.sitemap_harvester import SitemapHarvester
        console.print("[bold yellow]Starting High-Volume Sitemap Harvester...[/bold yellow]")
        s_harvester = SitemapHarvester(database=db)
        await s_harvester.harvest(max_articles=args.max_requests)

    if args.mode in ["dork", "full", "bulk"]:
        await run_dork_mode(subject_filter=subj_filter)

    if args.mode in ["crawl", "full", "bulk"]:
        await run_crawler_mode(
            crawler_mode=args.crawler_mode,
            max_requests=args.max_requests,
            max_depth=args.max_depth,
            subject_filter=subj_filter,
        )

    # Automatically reclassify any unclassified files after harvest
    from src.organizer import reclassify_and_reorganize
    reclassify_and_reorganize()

    console.print("\n")
    display_stats(db)


if __name__ == "__main__":
    asyncio.run(main())
