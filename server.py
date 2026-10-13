import http.server
import socketserver
import json
import sqlite3
import urllib.parse
from pathlib import Path
import os
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).parent.resolve()
DB_PATH = BASE_DIR / "imu_cet.db"
STATIC_DIR = BASE_DIR / "static"

def get_db_connection():
    # Use read-only mode to safeguard database integrity
    try:
        conn = sqlite3.connect(f"file:{DB_PATH.resolve()}?mode=ro", uri=True)
    except sqlite3.OperationalError:
        conn = sqlite3.connect(str(DB_PATH.resolve()))
    conn.row_factory = sqlite3.Row
    return conn

class MockTestRequestHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".json": "application/json",
        ".webmanifest": "application/manifest+json",
        ".js": "application/javascript",
        ".png": "image/png",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def end_headers(self):
        # Enable CORS and disable aggressive caching for API
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

        # PWA Service Worker headers
        if getattr(self, "path", "").endswith("sw.js"):
            self.send_header("Service-Worker-Allowed", "/")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")

        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/exams":
            self.handle_api_exams()
        elif path == "/api/questions":
            query_params = urllib.parse.parse_qs(parsed.query)
            self.handle_api_questions(query_params)
        elif path == "/api/health":
            self.send_json_response({"status": "healthy", "database": DB_PATH.name})
        else:
            # Fallback to serving static files or index.html for SPA routes
            file_path = STATIC_DIR / path.lstrip("/")
            if path == "/" or not file_path.exists() or file_path.is_dir():
                self.path = "/index.html"
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/submit":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
                self.handle_api_submit(data)
            except Exception as e:
                self.send_error_response(400, f"Invalid JSON payload: {str(e)}")
        else:
            self.send_error_response(404, "Endpoint not found")

    def send_json_response(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(body)

    def send_error_response(self, status, message):
        self.send_json_response({"error": message}, status=status)

    def handle_api_exams(self):
        """Returns distinct exam years, shifts, and sectional breakdowns."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Query active exams and counts
            cur.execute("""
            SELECT year, shift, section, COUNT(*) as question_count,
                   MIN(question_number) as min_q, MAX(question_number) as max_q
            FROM questions
            GROUP BY year, shift, section
            ORDER BY year DESC, COALESCE(shift, ''), min_q
            """)
            rows = cur.fetchall()
            conn.close()

            # Group into exam sessions
            exams_map = {}
            for r in rows:
                yr = r["year"]
                sh = r["shift"] or ""
                exam_key = f"{yr}_{sh}" if sh else str(yr)
                display_title = f"IMU CET {yr}" + (f" ({sh})" if sh else "")

                if exam_key not in exams_map:
                    exams_map[exam_key] = {
                        "id": exam_key,
                        "year": yr,
                        "shift": sh if sh else None,
                        "title": display_title,
                        "total_questions": 0,
                        "sections": []
                    }
                
                exams_map[exam_key]["total_questions"] += r["question_count"]
                exams_map[exam_key]["sections"].append({
                    "section": r["section"],
                    "count": r["question_count"],
                    "min_q": r["min_q"],
                    "max_q": r["max_q"]
                })

            exams_list = list(exams_map.values())
            self.send_json_response({"exams": exams_list})
        except Exception as e:
            self.send_error_response(500, f"Database error: {str(e)}")

    def handle_api_questions(self, query_params):
        """Fetches questions for a test attempt.
        For test security, correct_option and explanation are omitted during the attempt.
        """
        year = query_params.get("year", [None])[0]
        shift = query_params.get("shift", [None])[0]
        section = query_params.get("section", [None])[0]

        if not year:
            self.send_error_response(400, "Missing required parameter 'year'")
            return

        try:
            conn = get_db_connection()
            cur = conn.cursor()

            query = """
            SELECT id, year, shift, section, question_number, question_text,
                   option_a, option_b, option_c, option_d, topic, difficulty
            FROM questions
            WHERE year = ?
            """
            params = [int(year)]

            if shift and shift != "null" and shift != "None":
                query += " AND shift = ?"
                params.append(shift)
            else:
                query += " AND (shift IS NULL OR shift = '')"

            if section and section != "all" and section != "null":
                query += " AND section = ?"
                params.append(section)

            query += " ORDER BY question_number ASC"

            cur.execute(query, params)
            rows = cur.fetchall()
            conn.close()

            questions = [dict(r) for r in rows]
            self.send_json_response({
                "year": int(year),
                "shift": shift,
                "section": section,
                "count": len(questions),
                "questions": questions
            })
        except Exception as e:
            self.send_error_response(500, f"Database error: {str(e)}")

    def handle_api_submit(self, data):
        """Calculates score using official IMU CET marking scheme:
        +1.0 for Correct, -0.25 for Incorrect, 0.0 for Unattempted.
        Provides question-by-question review with verified answers and explanations.
        """
        year = data.get("year")
        shift = data.get("shift")
        section = data.get("section")
        user_responses = data.get("responses", {})  # { question_id: "A" | "B" | "C" | "D" }
        time_spent_seconds = data.get("time_spent_seconds", 0)

        if not year:
            self.send_error_response(400, "Missing required field 'year'")
            return

        try:
            conn = get_db_connection()
            cur = conn.cursor()

            query = """
            SELECT id, year, shift, section, question_number, question_text,
                   option_a, option_b, option_c, option_d, correct_option,
                   explanation, topic, difficulty
            FROM questions
            WHERE year = ?
            """
            params = [int(year)]

            if shift and shift != "null" and shift != "None":
                query += " AND shift = ?"
                params.append(shift)
            else:
                query += " AND (shift IS NULL OR shift = '')"

            if section and section != "all" and section != "null":
                query += " AND section = ?"
                params.append(section)

            query += " ORDER BY question_number ASC"

            cur.execute(query, params)
            rows = [dict(r) for r in cur.fetchall()]
            conn.close()

            total_questions = len(rows)
            attempted = 0
            correct = 0
            incorrect = 0
            unanswered = 0
            unverified_answers = 0

            section_stats = {}
            review_questions = []

            for q in rows:
                qid = q["id"]
                sec = q["section"]
                if sec not in section_stats:
                    section_stats[sec] = {
                        "section": sec,
                        "total": 0,
                        "attempted": 0,
                        "correct": 0,
                        "incorrect": 0,
                        "unanswered": 0,
                        "score": 0.0,
                        "max_score": 0.0
                    }
                
                section_stats[sec]["total"] += 1
                section_stats[sec]["max_score"] += 1.0

                candidate_answer = user_responses.get(qid)
                verified_answer = (q.get("correct_option") or "").strip().upper()
                is_verified = verified_answer in ["A", "B", "C", "D"]

                if not is_verified:
                    unverified_answers += 1

                status = "unanswered"
                marks_awarded = 0.0

                if candidate_answer and candidate_answer in ["A", "B", "C", "D"]:
                    attempted += 1
                    section_stats[sec]["attempted"] += 1

                    if is_verified and candidate_answer == verified_answer:
                        correct += 1
                        section_stats[sec]["correct"] += 1
                        marks_awarded = 1.0
                        status = "correct"
                    else:
                        incorrect += 1
                        section_stats[sec]["incorrect"] += 1
                        marks_awarded = -0.25
                        status = "incorrect"
                else:
                    unanswered += 1
                    section_stats[sec]["unanswered"] += 1
                    marks_awarded = 0.0
                    status = "unanswered"

                section_stats[sec]["score"] += marks_awarded

                review_questions.append({
                    "id": qid,
                    "section": sec,
                    "question_number": q["question_number"],
                    "question_text": q["question_text"],
                    "option_a": q["option_a"],
                    "option_b": q["option_b"],
                    "option_c": q["option_c"],
                    "option_d": q["option_d"],
                    "candidate_answer": candidate_answer,
                    "correct_option": verified_answer if is_verified else "UNVERIFIED",
                    "is_verified": is_verified,
                    "status": status,
                    "marks_awarded": marks_awarded,
                    "explanation": q.get("explanation") or "No explanation provided.",
                    "topic": q.get("topic") or "General",
                    "difficulty": q.get("difficulty") or "Medium"
                })

            total_score = round(correct * 1.0 - incorrect * 0.25, 2)
            max_marks = total_questions * 1.0
            accuracy = round((correct / attempted * 100), 2) if attempted > 0 else 0.0
            percentage = round((total_score / max_marks * 100), 2) if max_marks > 0 else 0.0

            proctoring = data.get("proctoring", {})

            result_summary = {
                "year": int(year),
                "shift": shift,
                "section": section,
                "time_spent_seconds": time_spent_seconds,
                "marking_scheme": {
                    "correct": 1.0,
                    "incorrect": -0.25,
                    "unanswered": 0.0
                },
                "total_questions": total_questions,
                "attempted": attempted,
                "correct": correct,
                "incorrect": incorrect,
                "unanswered": unanswered,
                "unverified_answers": unverified_answers,
                "total_score": total_score,
                "max_marks": max_marks,
                "percentage": percentage,
                "accuracy": accuracy,
                "sections": list(section_stats.values()),
                "review": review_questions,
                "proctoring": proctoring
            }

            self.send_json_response(result_summary)
        except Exception as e:
            self.send_error_response(500, f"Error processing submission: {str(e)}")

def run_server(port=None, host="0.0.0.0"):
    if port is None:
        port = int(os.environ.get("PORT", 10000))
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    server_address = (host, port)
    
    # Allow port reuse to prevent WinError 10048 during quick restarts
    socketserver.TCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.TCPServer(server_address, MockTestRequestHandler)
        print(f"==================================================")
        print(f"[IMU CET] Mock Test Server running at http://{host}:{port}")
        print(f"[STATIC] Serving static assets from: {STATIC_DIR}")
        print(f"[DATABASE] Database linked: {DB_PATH}")
        print(f"==================================================")
        httpd.serve_forever()
    except OSError as e:
        print(f"Could not bind to port {port} on {host}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
