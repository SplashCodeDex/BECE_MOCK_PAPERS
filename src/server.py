"""
BECE & Mock Examination Portal - Dedicated Local Web Server
Provides root redirect to the viewer, /health status endpoint, live SQLite API endpoints
(/api/stats, /api/indicators, /api/questions), and proper static asset streaming.
"""

import http.server
import json
import logging
import os
from pathlib import Path
import socketserver
import sqlite3
import sys
from urllib.parse import parse_qs, urlparse

# Workspace root
WORKSPACE_DIR = Path(__file__).resolve().parent.parent
if str(WORKSPACE_DIR) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_DIR))

from src.config import DATABASE_PATH

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BECEServer")


class BECEPortalHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WORKSPACE_DIR), **kwargs)

    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        route = parsed.path.rstrip("/") or "/"
        qs = parse_qs(parsed.query)

        # Health check endpoint
        if route == "/health":
            q_count = 0
            ind_count = 0
            sol_count = 0
            if DATABASE_PATH.exists():
                try:
                    with sqlite3.connect(str(DATABASE_PATH)) as conn:
                        q_count = conn.execute("SELECT COUNT(*) FROM questions;").fetchone()[0]
                        ind_count = conn.execute("SELECT COUNT(*) FROM curriculum_indicators;").fetchone()[0]
                        sol_count = conn.execute("SELECT COUNT(*) FROM solutions;").fetchone()[0]
                except Exception:
                    pass
            if q_count == 0:
                q_file = WORKSPACE_DIR / "data" / "extracted_questions" / "questions_bank.json"
                if q_file.exists():
                    try:
                        q_count = len(json.loads(q_file.read_text(encoding="utf-8")))
                    except Exception:
                        pass

            self._send_json(
                {
                    "status": "healthy",
                    "service": "BECE & Mock Papers Hub",
                    "workspace": str(WORKSPACE_DIR),
                    "questions_count": q_count,
                    "indicators_count": ind_count,
                    "solutions_count": sol_count,
                    "version": "2.0.0",
                }
            )
            return

        # Live Curriculum Indicators API
        if route == "/api/indicators" and DATABASE_PATH.exists():
            subject = qs.get("subject", [None])[0]
            grade = qs.get("grade", [None])[0]
            with sqlite3.connect(str(DATABASE_PATH)) as conn:
                conn.row_factory = sqlite3.Row
                sql = """
                    SELECT ci.uid, ci.subject, ci.grade, ci.code, ci.strand_number, ci.strand_title,
                           ci.substrand_number, ci.substrand_title, ci.content_standard,
                           ci.indicator_text, ci.prerequisite_codes,
                           COUNT(q.id) AS question_count
                    FROM curriculum_indicators ci
                    LEFT JOIN questions q ON q.subject = ci.subject AND q.indicator_code = ci.code
                """
                clauses, params = [], []
                if subject:
                    clauses.append("ci.subject = ?")
                    params.append(subject)
                if grade:
                    clauses.append("ci.grade = ?")
                    params.append(grade.upper())
                if clauses:
                    sql += " WHERE " + " AND ".join(clauses)
                sql += " GROUP BY ci.uid ORDER BY ci.subject, ci.grade, ci.code;"
                rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
            self._send_json({"count": len(rows), "indicators": rows})
            return

        # Live Canonical Questions + Worked Solutions API
        if route == "/api/questions" and DATABASE_PATH.exists():
            subject = qs.get("subject", [None])[0]
            indicator = qs.get("indicator", [None])[0]
            search = qs.get("q", [None])[0]
            limit = min(500, int(qs.get("limit", ["100"])[0]))

            with sqlite3.connect(str(DATABASE_PATH)) as conn:
                conn.row_factory = sqlite3.Row
                sql = """
                    SELECT q.id, q.subject, q.question_text, q.option_a, q.option_b, q.option_c, q.option_d,
                           q.correct_answer, q.has_diagram, q.diagram_path, q.year, q.paper_type,
                           q.indicator_code, q.confidence, q.tag_method,
                           ci.grade AS indicator_grade, ci.strand_title, ci.substrand_title, ci.indicator_text
                    FROM questions q
                    LEFT JOIN curriculum_indicators ci
                      ON ci.subject = q.subject AND ci.code = q.indicator_code
                """
                clauses, params = [], []
                if subject:
                    clauses.append("q.subject = ?")
                    params.append(subject)
                if indicator:
                    clauses.append("(q.indicator_code = ? OR q.indicator_code LIKE ?)")
                    params.extend([indicator, f"{indicator}.%"])
                if search:
                    clauses.append("q.question_text LIKE ?")
                    params.append(f"%{search}%")
                if clauses:
                    sql += " WHERE " + " AND ".join(clauses)
                sql += " ORDER BY q.confidence DESC, COALESCE(q.year, 0) DESC LIMIT ?;"
                params.append(limit)
                rows = [dict(r) for r in conn.execute(sql, params).fetchall()]

                for r in rows:
                    sols = conn.execute(
                        """
                        SELECT id, lesson_id, indicator_code, step_by_step_markdown,
                               final_answer, verification_type, verification_details, created_at
                        FROM solutions
                        WHERE question_id = ?
                        ORDER BY created_at DESC;
                        """,
                        (r["id"],),
                    ).fetchall()
                    r["solutions"] = [dict(s) for s in sols]

            self._send_json({"count": len(rows), "questions": rows})
            return

        # Root endpoint redirect to viewer
        if route == "/":
            self.send_response(302)
            self.send_header("Location", "/viewer/index.html")
            self.end_headers()
            return

        # Default static file serving
        return super().do_GET()

    def end_headers(self):
        # Add CORS headers for local development
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def run_server(port: int = 8000, host: str = "127.0.0.1") -> None:
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((host, port), BECEPortalHandler) as httpd:
        logger.info(f"BECE Portal Server running at http://{host}:{port}/")
        logger.info(f"Viewer available at http://{host}:{port}/viewer/index.html")
        logger.info(f"Health status available at http://{host}:{port}/health")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("Server shutting down.")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port=port)

