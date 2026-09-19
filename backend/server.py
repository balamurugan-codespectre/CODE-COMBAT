"""
CODE COMBAT - HTTP Server & REST API Router
Provides static file serving and JSON REST API without any external dependencies.
"""

import os
import json
import mimetypes
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from typing import Dict, Any, Optional

from .storage import Storage
from .problems_manager import ProblemsManager
from .auth import Auth
from judge.judge import Judge


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handles requests in separate threads for concurrent code executions."""
    daemon_threads = True


class CodeCombatHandler(BaseHTTPRequestHandler):
    """Custom HTTP Request Handler for CODE COMBAT."""

    # Injected references from main application
    storage: Storage = None
    problems_manager: ProblemsManager = None
    auth: Auth = None
    judge: Judge = None
    config: Dict[str, Any] = {}
    frontend_dir: str = ""

    def log_message(self, format, *args):
        """Custom concise logging format."""
        # print(f"[{self.log_date_time_string()}] {self.command} {self.path} -> {args[0]}")
        pass

    # ------------------- Utility Helpers -------------------

    def send_json(self, data: Any, status_code: int = 200):
        """Sends a JSON HTTP response."""
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, message: str, status_code: int = 400):
        """Sends a structured JSON error response."""
        self.send_json({"error": message, "success": False}, status_code=status_code)

    def parse_json_body(self) -> Dict[str, Any]:
        """Reads and parses incoming JSON payload."""
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length <= 0:
            return {}
        raw_body = self.rfile.read(content_length).decode("utf-8", errors="replace")
        try:
            return json.loads(raw_body)
        except Exception:
            return {}

    def do_OPTIONS(self):
        """Handles CORS preflight requests."""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.end_headers()

    # ------------------- Static File Serving -------------------

    def serve_static(self, req_path: str):
        """Serves frontend files from self.frontend_dir."""
        # Sanitize path to prevent directory traversal
        clean_path = os.path.normpath(req_path.lstrip("/"))
        if clean_path == "" or clean_path == ".":
            clean_path = "index.html"

        file_path = os.path.join(self.frontend_dir, clean_path)

        # Disallow access outside frontend_dir
        if not os.path.abspath(file_path).startswith(os.path.abspath(self.frontend_dir)):
            self.send_error(403, "Access Denied")
            return

        if not os.path.isfile(file_path):
            # Fallback to index.html for SPA client-side routes
            file_path = os.path.join(self.frontend_dir, "index.html")

        if not os.path.isfile(file_path):
            self.send_error(404, "File Not Found")
            return

        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type = mime_type or "application/octet-stream"

        try:
            with open(file_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", f"{mime_type}; charset=utf-8" if "text" in mime_type or "javascript" in mime_type or "json" in mime_type else mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-cache, must-revalidate")
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error reading file: {e}")

    # ------------------- Request Routing -------------------

    def do_GET(self):
        try:
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path
            query = urllib.parse.parse_qs(parsed.query)

            # API Endpoints
            if path.startswith("/api/"):
                self.handle_api_get(path, query)
            else:
                self.serve_static(path)
        except Exception as e:
            self.send_error_json(f"Internal server error: {e}", 500)

    def do_POST(self):
        try:
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path

            if path.startswith("/api/"):
                self.handle_api_post(path)
            else:
                self.send_error_json("Invalid POST endpoint", 404)
        except Exception as e:
            self.send_error_json(f"Internal server error: {e}", 500)

    def do_DELETE(self):
        try:
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path

            if path.startswith("/api/"):
                self.handle_api_delete(path)
            else:
                self.send_error_json("Invalid DELETE endpoint", 404)
        except Exception as e:
            self.send_error_json(f"Internal server error: {e}", 500)

    # ------------------- API Handlers -------------------

    def handle_api_get(self, path: str, query: Dict[str, list]):
        # GET /api/config
        if path == "/api/config":
            public_config = {
                "competition_name": self.config.get("competition_name", "CODE COMBAT"),
                "tagline": self.config.get("tagline", "Compete. Code. Conquer."),
                "description": self.config.get("description", ""),
                "competition_duration_minutes": self.config.get("competition_duration_minutes", 90),
                "supported_languages": self.config.get("supported_languages", [])
            }
            self.send_json(public_config)
            return

        # GET /api/problems
        if path == "/api/problems":
            participant_id = query.get("participant_id", [None])[0]
            solved_set = self.storage.get_solved_problems(participant_id) if participant_id else set()
            problems = self.problems_manager.get_problem_list(solved_set)
            self.send_json({"problems": problems})
            return

        # GET /api/problems/<id>
        if path.startswith("/api/problems/"):
            prob_id = path.replace("/api/problems/", "").strip()
            detail = self.problems_manager.get_problem_detail(prob_id)
            if detail:
                self.send_json(detail)
            else:
                self.send_error_json("Problem not found", 404)
            return

        # GET /api/leaderboard
        if path == "/api/leaderboard":
            leaderboard = self.storage.get_leaderboard()
            self.send_json({"leaderboard": leaderboard})
            return

        # GET /api/submissions
        if path == "/api/submissions":
            participant_id = query.get("participant_id", [None])[0]
            limit = int(query.get("limit", [100])[0])
            subs = self.storage.get_submissions(participant_id=participant_id, limit=limit)
            self.send_json({"submissions": subs})
            return

        # GET /api/participants (or /api/admin/participants)
        if path in ["/api/participants", "/api/admin/participants"]:
            parts = self.storage.get_participants()
            self.send_json({"participants": parts})
            return

        # GET /api/admin/export
        if path == "/api/admin/export":
            data = self.storage.export_all_data()
            self.send_json(data)
            return

        self.send_error_json("API route not found", 404)

    def handle_api_post(self, path: str):
        body = self.parse_json_body()

        # POST /api/register
        if path == "/api/register":
            name = body.get("name", "").strip()
            college = body.get("college", "").strip()
            reg_no = body.get("reg_no", "").strip()

            if not name:
                self.send_error_json("Participant name is required.", 400)
                return

            participant = self.storage.register_participant(name, college, reg_no)
            self.send_json({
                "success": True,
                "participant": participant,
                "message": "Registration successful"
            })
            return

        # POST /api/run (Sample tests or custom input)
        if path == "/api/run":
            problem_id = body.get("problem_id", "").strip()
            language = body.get("language", "python").strip()
            code = body.get("code", "").strip()
            custom_input = body.get("custom_input")
            is_custom = body.get("is_custom", False)

            if not code:
                self.send_error_json("No source code provided.", 400)
                return

            # Case 1: Custom Input execution
            if is_custom or custom_input is not None:
                custom_res = self.judge.run_custom_input(
                    language=language,
                    code=code,
                    custom_input=custom_input or "",
                    timeout=self.config.get("execution_timeout_seconds", 3.0)
                )
                self.send_json({
                    "is_custom": True,
                    "result": custom_res
                })
                return

            # Case 2: Run visible sample tests
            prob_detail = self.problems_manager.get_problem_detail(problem_id)
            if not prob_detail:
                self.send_error_json(f"Problem '{problem_id}' not found.", 404)
                return

            sample_tests = prob_detail.get("sample_tests", [])
            timeout = prob_detail.get("time_limit", self.config.get("execution_timeout_seconds", 3.0))

            sample_res = self.judge.run_sample_tests(
                language=language,
                code=code,
                sample_tests=sample_tests,
                timeout=timeout
            )
            self.send_json({
                "is_custom": False,
                "result": sample_res
            })
            return

        # POST /api/submit (Evaluate against hidden tests)
        if path == "/api/submit":
            participant_id = body.get("participant_id", "").strip()
            participant_name = body.get("participant_name", "Anonymous").strip()
            problem_id = body.get("problem_id", "").strip()
            language = body.get("language", "python").strip()
            code = body.get("code", "").strip()

            if not participant_id:
                self.send_error_json("Participant ID is required. Please register first.", 400)
                return

            if not code:
                self.send_error_json("No source code provided.", 400)
                return

            prob_detail = self.problems_manager.get_problem_detail(problem_id)
            if not prob_detail:
                self.send_error_json(f"Problem '{problem_id}' not found.", 404)
                return

            hidden_dir = self.problems_manager.get_hidden_tests_dir(problem_id)
            if not hidden_dir or not os.path.exists(hidden_dir):
                self.send_error_json("Hidden tests not configured for this problem.", 500)
                return

            points = prob_detail.get("points", 100)
            timeout = prob_detail.get("time_limit", self.config.get("execution_timeout_seconds", 3.0))

            # Run Hidden Tests
            judge_res = self.judge.run_hidden_tests(
                language=language,
                code=code,
                hidden_tests_dir=hidden_dir,
                problem_points=points,
                timeout=timeout
            )

            # Check if participant already solved this problem
            solved_problems = self.storage.get_solved_problems(participant_id)
            already_solved = problem_id in solved_problems

            # If already solved previously, award 0 additional points to prevent double scoring
            awarded_score = 0 if already_solved else judge_res["score"]

            # Save submission record
            submission = self.storage.add_submission(
                participant_id=participant_id,
                participant_name=participant_name,
                problem_id=problem_id,
                problem_title=prob_detail.get("title", problem_id),
                difficulty=prob_detail.get("difficulty", "Easy"),
                language=language,
                code=code,
                status=judge_res["status"],
                passed_count=judge_res["passed_count"],
                total_count=judge_res["total_count"],
                score=awarded_score,
                runtime=judge_res["runtime"]
            )

            # Return judgment verdict to client (No hidden inputs/outputs!)
            self.send_json({
                "submission_id": submission["id"],
                "status": judge_res["status"],
                "passed_count": judge_res["passed_count"],
                "total_count": judge_res["total_count"],
                "score_earned": awarded_score,
                "already_solved": already_solved,
                "runtime": judge_res["runtime"],
                "error_message": judge_res.get("error_message")
            })
            return

        # POST /api/admin/login
        if path == "/api/admin/login":
            password = body.get("password", "")
            if self.auth.verify_admin_password(password):
                self.send_json({"authenticated": True, "token": "admin_session_valid"})
            else:
                self.send_error_json("Invalid admin password", 401)
            return

        # POST /api/admin/problem (Create / Update)
        if path == "/api/admin/problem":
            problem_data = body.get("problem")
            hidden_tests = body.get("hidden_tests")
            if not problem_data or not problem_data.get("id"):
                self.send_error_json("Invalid problem data provided.", 400)
                return

            saved = self.problems_manager.save_problem(problem_data, hidden_tests)
            if saved:
                self.send_json({"success": True, "message": "Problem saved successfully."})
            else:
                self.send_error_json("Failed to save problem.", 500)
            return

        # POST /api/admin/reset
        if path == "/api/admin/reset":
            password = body.get("password", "")
            if not self.auth.verify_admin_password(password):
                self.send_error_json("Unauthorized", 401)
                return

            self.storage.reset_competition()
            self.send_json({"success": True, "message": "Competition data has been reset."})
            return

        self.send_error_json("API POST route not found", 404)

    def handle_api_delete(self, path: str):
        # DELETE /api/admin/problem/<id>
        if path.startswith("/api/admin/problem/"):
            prob_id = path.replace("/api/admin/problem/", "").strip()
            deleted = self.problems_manager.delete_problem(prob_id)
            if deleted:
                self.send_json({"success": True, "message": f"Problem '{prob_id}' deleted."})
            else:
                self.send_error_json("Problem not found or could not be deleted.", 404)
            return

        self.send_error_json("API DELETE route not found", 404)
