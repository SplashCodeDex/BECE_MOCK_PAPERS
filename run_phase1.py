"""Phase 1 runner: schema init, legacy migration, taxonomy seed, quality report.

Usage:
    python run_phase1.py init                      # create v2 tables only
    python run_phase1.py migrate [--dry-run]       # migrate + dedup extracted_questions
    python run_phase1.py seed-taxonomy --file data/taxonomy/b9_indicators.json
    python run_phase1.py report                    # bank quality overview
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.bank_migrate import migrate
from src.bank_schema import init_bank_schema
from src.config import BASE_DIR, DATABASE_PATH

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console(force_terminal=True)


def cmd_init(_args: argparse.Namespace) -> None:
    init_bank_schema(DATABASE_PATH)
    console.print(Panel("Phase 1 schema created (idempotent).", style="bold green"))


def cmd_migrate(args: argparse.Namespace) -> None:
    stats = migrate(db_path=DATABASE_PATH, dry_run=args.dry_run)
    title = "Migration DRY RUN (rolled back)" if args.dry_run else "Migration complete"
    table = Table(title=title, show_header=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    for k, v in stats.items():
        table.add_row(k.replace("_", " ").title(), str(v))
    console.print(table)
    if stats["answer_conflicts"]:
        console.print(
            "[yellow]Answer conflicts were routed to tag_review_queue "
            "(reason='answer_conflict').[/yellow]"
        )


def cmd_seed_taxonomy(args: argparse.Namespace) -> None:
    path = Path(args.file)
    if not path.is_absolute():
        path = BASE_DIR / path
    if not path.exists():
        console.print(f"[red]Taxonomy file not found: {path}[/red]")
        sys.exit(1)

    payload = json.loads(path.read_text(encoding="utf-8"))
    indicators = payload["indicators"] if isinstance(payload, dict) else payload
    init_bank_schema(DATABASE_PATH)

    conn = sqlite3.connect(str(DATABASE_PATH))
    inserted = 0
    try:
        with conn:
            for ind in indicators:
                prereqs = ind.get("prerequisite_codes")
                prereqs_json = json.dumps(prereqs) if prereqs is not None else None
                cur = conn.execute(
                    """
                    INSERT INTO curriculum_indicators (
                        uid, code, grade, subject, strand_number, strand_title,
                        substrand_number, substrand_title, content_standard,
                        content_standard_text, indicator_text, prerequisite_codes,
                        source_file, page
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(uid) DO UPDATE SET
                        code = excluded.code,
                        grade = excluded.grade,
                        subject = excluded.subject,
                        strand_number = excluded.strand_number,
                        strand_title = excluded.strand_title,
                        substrand_number = excluded.substrand_number,
                        substrand_title = excluded.substrand_title,
                        content_standard = excluded.content_standard,
                        content_standard_text = excluded.content_standard_text,
                        indicator_text = excluded.indicator_text,
                        prerequisite_codes = COALESCE(excluded.prerequisite_codes, curriculum_indicators.prerequisite_codes),
                        source_file = excluded.source_file,
                        page = excluded.page;
                    """,
                    (
                        f"{ind['subject']}:{ind['code']}",
                        ind["code"], ind["grade"], ind["subject"],
                        ind["strand_number"], ind["strand_title"],
                        ind["substrand_number"], ind["substrand_title"],
                        ind["content_standard"], ind.get("content_standard_text"),
                        ind["indicator_text"], prereqs_json,
                        ind.get("source_file"), ind.get("page"),
                    ),
                )
                inserted += cur.rowcount
        total = conn.execute("SELECT COUNT(*) FROM curriculum_indicators;").fetchone()[0]
    finally:
        conn.close()

    console.print(
        Panel(
            f"Inserted/updated {inserted} indicators from {path.name}.\n"
            f"curriculum_indicators now holds {total} rows.",
            style="bold green",
        )
    )
    notes = payload.get("notes") if isinstance(payload, dict) else None
    if notes:
        console.print(f"[yellow]Extractor notes:[/yellow] {notes}")


def cmd_report(_args: argparse.Namespace) -> None:
    conn = sqlite3.connect(f"file:{DATABASE_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        def one(sql: str) -> int:
            return conn.execute(sql).fetchone()[0]

        table = Table(title="Question Bank Quality Report", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        n_q = one("SELECT COUNT(*) FROM questions;")
        n_occ = one("SELECT COUNT(*) FROM question_occurrences;")
        table.add_row("Canonical questions", str(n_q))
        table.add_row("Occurrences (raw appearances)", str(n_occ))
        table.add_row("Duplicates merged", str(max(0, n_occ - n_q)))
        table.add_row("Sources registered", str(one("SELECT COUNT(*) FROM sources;")))
        table.add_row("Curriculum indicators", str(one("SELECT COUNT(*) FROM curriculum_indicators;")))
        table.add_row("Tagged questions", str(one("SELECT COUNT(*) FROM questions WHERE indicator_code IS NOT NULL;")))
        table.add_row("Open review items", str(one("SELECT COUNT(*) FROM tag_review_queue WHERE status='open';")))
        table.add_row("Verified solutions", str(one("SELECT COUNT(*) FROM solutions;")))
        table.add_row("Questions with answer", str(one("SELECT COUNT(*) FROM questions WHERE correct_answer IS NOT NULL AND trim(correct_answer) <> '';")))
        console.print(table)

        by_subject = conn.execute(
            "SELECT subject, COUNT(*) AS n FROM questions GROUP BY subject ORDER BY n DESC;"
        ).fetchall()
        st = Table(title="Canonical questions by subject", show_header=True)
        st.add_column("Subject", style="cyan")
        st.add_column("Count", style="magenta")
        for r in by_subject:
            st.add_row(r["subject"], str(r["n"]))
        console.print(st)

        open_reasons = conn.execute(
            "SELECT reason, COUNT(*) AS n FROM tag_review_queue WHERE status='open' GROUP BY reason;"
        ).fetchall()
        if open_reasons:
            rt = Table(title="Open review queue by reason", show_header=True)
            rt.add_column("Reason", style="cyan")
            rt.add_column("Count", style="magenta")
            for r in open_reasons:
                rt.add_row(r["reason"], str(r["n"]))
            console.print(rt)
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="BECE question bank Phase 1 tooling")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Create Phase 1 tables (idempotent)")

    p_migrate = sub.add_parser("migrate", help="Migrate + dedup legacy extracted_questions")
    p_migrate.add_argument("--dry-run", action="store_true", help="Roll back after counting")

    p_seed = sub.add_parser("seed-taxonomy", help="Load curriculum indicators from JSON")
    p_seed.add_argument("--file", required=True, help="Path to b9_indicators.json")

    sub.add_parser("report", help="Bank quality overview")

    args = parser.parse_args()
    {
        "init": cmd_init,
        "migrate": cmd_migrate,
        "seed-taxonomy": cmd_seed_taxonomy,
        "report": cmd_report,
    }[args.command](args)


if __name__ == "__main__":
    main()
