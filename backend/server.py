"""
CODE COMBAT Pro - HTTP Server & REST API Router
Provides static file serving, rate limiting, security headers, and JSON REST API without external dependencies.
"""

import os
import json
import mimetypes
import urllib.parse
import time
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from typing import Dict, Any, Optional

from .storage import Storage
from .problems_manager import ProblemsManager
from .auth import Auth
from judge.judge import Judge
from judge.compiler import Compiler


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handles requests in separate threads for concurrent code executions."""
    daemon_threads = True


class RateLimiter:
    """Sliding-window in-memory rate limiter per IP address."""

    def __init__(self, max_requests: int = 120, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    def is_allowed(self, ip: str) -> bool:
        now = time.time()
        timestamps = self.requests.get(ip, [])
        # Prune old timestamps
        timestamps = [t for t in timestamps if now - t < self.window_seconds]
        if len(timestamps) >= self.max_requests:
            self.requests[ip] = timestamps
            return False
        timestamps.append(now)
        self.requests[ip] = timestamps
        return True


class CodeCombatHandler(BaseHTTPRequestHandler):
    """Custom HTTP Request Handler for CODE COMBAT Pro."""

    # Injected references from main application
    storage: Storage = None
    problems_manager: ProblemsManager = None
    auth: Auth = None
    judge: Judge = None
    config: Dict[str, Any] = {}
    frontend_dir: str = ""
    start_time: float = time.time()
    rate_limiter = RateLimiter(max_requests=240, window_seconds=60)

    def log_message(self, format, *args):
        """Silent concise logging."""
        pass

    # ------------------- Utility Helpers -------------------

    def send_json(self, data: Any, status_code: int = 200):
        """Sends a JSON HTTP response with security headers."""
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
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
        """Serves frontend files safely from self.frontend_dir."""
        clean_path = os.path.normpath(req_path.lstrip("/"))
        if clean_path == "" or clean_path == ".":
            clean_path = "index.html"

        file_path = os.path.join(self.frontend_dir, clean_path)

        if not os.path.abspath(file_path).startswith(os.path.abspath(self.frontend_dir)):
            self.send_error(403, "Access Denied")
            return

        if not os.path.isfile(file_path):
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
            self.send_header("Content-Type", f"{mime_type}; charset=utf-8" if ("text" in mime_type or "javascript" in mime_type or "json" in mime_type) else mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "no-cache, must-revalidate")
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error reading file: {e}")

    # ------------------- Request Routing -------------------

    def do_GET(self):
        client_ip = self.client_address[0]
        if not self.rate_limiter.is_allowed(client_ip):
            self.send_error_json("Rate limit exceeded. Please slow down.", 429)
            return

        try:
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path
            query = urllib.parse.parse_qs(parsed.query)

            if path.startswith("/api/"):
                self.handle_api_get(path, query)
            else:
                self.serve_static(path)
        except Exception as e:
            self.send_error_json(f"Internal server error: {e}", 500)

    def do_POST(self):
        client_ip = self.client_address[0]
        if not self.rate_limiter.is_allowed(client_ip):
            self.send_error_json("Rate limit exceeded. Please slow down.", 429)
            return

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

    def is_admin_authenticated(self, body: Dict[str, Any] = None) -> bool:
        """Checks admin authorization via Authorization header token, body token, or password/id."""
        auth_header = self.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "").strip()
            verified = self.auth.verify_session_token(token)
            if verified and verified.get("pid") == self.auth.admin_id:
                return True

        if body:
            token = body.get("token")
            if token:
                verified = self.auth.verify_session_token(token)
                if verified and verified.get("pid") == self.auth.admin_id:
                    return True

            admin_id = body.get("admin_id") or body.get("username")
            password = body.get("password") or body.get("admin_password") or body.get("old_password")
            if password:
                if admin_id:
                    return self.auth.verify_admin_credentials(admin_id, password)
                return self.auth.verify_admin_password(password)
        return False

    def handle_api_get(self, path: str, query: Dict[str, list]):
        # GET /api/health
        if path == "/api/health":
            uptime = round(time.time() - self.start_time, 2)
            c_comp = Compiler.detect_c_compiler()
            java_comp = Compiler.detect_java_compiler()
            self.send_json({
                "status": "healthy",
                "uptime_seconds": uptime,
                "compilers": {
                    "python": True,
                    "c": bool(c_comp),
                    "c_compiler": c_comp or "None",
                    "java": bool(java_comp),
                    "java_compiler": java_comp or "None"
                },
                "active_problem_set": self.problems_manager.active_set,
                "total_problems": len(self.problems_manager.problems),
                "timestamp": datetime.datetime.now().isoformat()
            })
            return

        # GET /api/config
        if path == "/api/config":
            tier_locks = self.config.get("tier_locks", {"easy": False, "medium": False, "hard": False})
            public_config = {
                "competition_name": self.config.get("competition_name", "CODE COMBAT Pro"),
                "tagline": self.config.get("tagline", "Compete. Code. Conquer."),
                "description": self.config.get("description", "An offline competitive programming platform."),
                "competition_duration_minutes": self.config.get("competition_duration_minutes", 60),
                "tier_locks": tier_locks,
                "supported_languages": self.config.get("supported_languages", [
                    {"id": "python", "name": "Python 3 (Normal / Script)", "extension": "py"},
                    {"id": "python_class", "name": "Python 3 (Class / LeetCode)", "extension": "py"},
                    {"id": "java", "name": "Java (Solution.java)", "extension": "java"},
                    {"id": "c", "name": "C (solution.c)", "extension": "c"}
                ])
            }
            self.send_json(public_config)
            return

        # GET /api/problems
        if path == "/api/problems":
            participant_id = query.get("participant_id", [None])[0]
            solved_set = self.storage.get_solved_problems(participant_id) if participant_id else set()
            tier_locks = self.config.get("tier_locks", {"easy": False, "medium": False, "hard": False})
            problems = self.problems_manager.get_problem_list(solved_set, tier_locks=tier_locks)
            self.send_json({
                "problems": problems,
                "tier_locks": tier_locks
            })
            return

        # GET /api/problems/<id>
        if path.startswith("/api/problems/"):
            prob_id = path.replace("/api/problems/", "").strip()
            participant_id = query.get("participant_id", [None])[0]
            tier_locks = self.config.get("tier_locks", {"easy": False, "medium": False, "hard": False})
            detail = self.problems_manager.get_problem_detail(prob_id, participant_id=participant_id, storage=self.storage, tier_locks=tier_locks)
            if detail:
                self.send_json(detail)
            else:
                self.send_error_json("Problem not found", 404)
            return

        # GET /api/admin/tier-locks or /api/tier-locks
        if path in ["/api/admin/tier-locks", "/api/tier-locks"]:
            tier_locks = self.config.get("tier_locks", {"easy": False, "medium": False, "hard": False})
            self.send_json({
                "success": True,
                "tier_locks": tier_locks
            })
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

        # GET /api/participants
        if path in ["/api/participants", "/api/admin/participants"]:
            parts = self.storage.get_participants()
            self.send_json({"participants": parts})
            return

        # GET /api/participant/<id>
        if path.startswith("/api/participant/"):
            pid = path.replace("/api/participant/", "").strip()
            p = self.storage.get_participant(pid)
            if p:
                self.send_json({"participant": p})
            else:
                self.send_error_json("Participant not found", 404)
            return

        # GET /api/admin/sets
        if path in ["/api/admin/sets", "/api/sets"]:
            sets = self.problems_manager.get_available_sets()
            self.send_json({
                "sets": sets,
                "active_set": self.problems_manager.active_set
            })
            return

        # GET /api/admin/export
        if path == "/api/admin/export":
            data = self.storage.export_all_data()
            self.send_json(data)
            return

        # GET /api/admin/export/csv
        if path == "/api/admin/export/csv":
            leaderboard = self.storage.get_leaderboard()
            lines = ["Rank,Participant Name,Register No,College,Score,Problems Solved,Easy,Medium,Hard,Total Runtime (s),Last Submission"]
            for row in leaderboard:
                name = str(row['name']).replace('"', '""')
                reg_no = str(row['reg_no']).replace('"', '""')
                college = str(row['college']).replace('"', '""')
                last_sub = str(row['last_submission_time']).replace('"', '""')
                lines.append(f'{row["rank"]},"{name}","{reg_no}","{college}",{row["score"]},{row["solved_count"]},{row["easy_solved"]},{row["medium_solved"]},{row["hard_solved"]},{row["total_runtime"]},"{last_sub}"')
            csv_content = "\n".join(lines).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Disposition", "attachment; filename=leaderboard.csv")
            self.send_header("Content-Length", str(len(csv_content)))
            self.end_headers()
            self.wfile.write(csv_content)
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
            session_token = self.auth.create_session_token(participant["id"], participant["name"])
            self.send_json({
                "success": True,
                "participant": participant,
                "token": session_token,
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
                    problem_id=problem_id or None,
                    timeout=float(self.config.get("execution_timeout_seconds", 3.0))
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

            diff_key = prob_detail.get("difficulty", "Easy").lower()
            tier_locks = self.config.get("tier_locks", {})
            if tier_locks.get(diff_key, False) and not self.is_admin_authenticated(body):
                round_name = prob_detail.get("round_name", f"Round ({diff_key.capitalize()})")
                self.send_error_json(f"Access Denied: {round_name} is currently locked by the event administrator.", 403)
                return

            pid = prob_detail.get("id", problem_id)
            sample_tests = prob_detail.get("sample_tests", [])
            timeout = float(prob_detail.get("time_limit", self.config.get("execution_timeout_seconds", 3.0)))

            sample_res = self.judge.run_sample_tests(
                language=language,
                code=code,
                sample_tests=sample_tests,
                problem_id=pid,
                timeout=timeout
            )
            self.send_json({
                "is_custom": False,
                "result": sample_res
            })
            return

        # POST /api/problems/unlock-hint
        if path == "/api/problems/unlock-hint":
            participant_id = body.get("participant_id", "").strip()
            problem_id = body.get("problem_id", "").strip()
            try:
                hint_index = int(body.get("hint_index", 1))
            except (ValueError, TypeError):
                self.send_error_json("Invalid hint index. Must be 1, 2, or 3.", 400)
                return

            if not participant_id:
                self.send_error_json("Participant ID is required to unlock hints.", 400)
                return
            if not problem_id:
                self.send_error_json("Problem ID is required.", 400)
                return
            if hint_index not in [1, 2, 3]:
                self.send_error_json("Invalid hint index. Must be 1, 2, or 3.", 400)
                return

            prob_detail = self.problems_manager.get_problem_detail(problem_id)
            if not prob_detail:
                self.send_error_json("Problem not found.", 404)
                return

            pid = prob_detail["id"]
            difficulty = prob_detail.get("difficulty", "Easy")
            base_points = int(prob_detail.get("points", 100))
            penalty = self.problems_manager.get_hint_penalty(difficulty, hint_index)

            # Record unlock in database and recalculate live score
            unlock_res = self.storage.unlock_hint(participant_id, pid, hint_index, penalty)
            total_penalty = self.storage.get_total_hint_penalty(participant_id, pid)
            max_score = max(int(base_points * 0.25), base_points - total_penalty)
            hint_text = self.problems_manager.get_hint_text(pid, hint_index)

            self.send_json({
                "success": True,
                "already_unlocked": not unlock_res.get("unlocked", True),
                "problem_id": pid,
                "hint_index": hint_index,
                "hint_text": hint_text,
                "penalty": penalty,
                "total_hint_penalty": total_penalty,
                "max_score": max_score,
                "participant_score": unlock_res.get("participant_score", 0),
                "message": f"Hint {hint_index} unlocked (-{penalty} pts penalty applied)."
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

            diff_key = prob_detail.get("difficulty", "Easy").lower()
            tier_locks = self.config.get("tier_locks", {})
            if tier_locks.get(diff_key, False) and not self.is_admin_authenticated(body):
                round_name = prob_detail.get("round_name", f"Round ({diff_key.capitalize()})")
                self.send_error_json(f"Submission Rejected: {round_name} is currently locked by the event administrator.", 403)
                return

            hidden_dir = self.problems_manager.get_hidden_tests_dir(problem_id)
            if not hidden_dir or not os.path.exists(hidden_dir):
                self.send_error_json("Hidden tests not configured for this problem.", 500)
                return

            pid = prob_detail.get("id", problem_id)
            base_points = int(prob_detail.get("points", 100))
            hint_penalty = self.storage.get_total_hint_penalty(participant_id, pid)
            effective_max_points = max(int(base_points * 0.25), base_points - hint_penalty)
            timeout = float(prob_detail.get("time_limit", self.config.get("execution_timeout_seconds", 3.0)))

            judge_res = self.judge.run_hidden_tests(
                language=language,
                code=code,
                hidden_tests_dir=hidden_dir,
                problem_points=effective_max_points,
                problem_id=pid,
                timeout=timeout
            )

            solved_problems = self.storage.get_solved_problems(participant_id)
            already_solved = (problem_id in solved_problems) or (pid in solved_problems)
            awarded_score = 0 if already_solved else judge_res["score"]

            submission = self.storage.add_submission(
                participant_id=participant_id,
                participant_name=participant_name,
                problem_id=pid,
                problem_title=prob_detail.get("title", pid),
                difficulty=prob_detail.get("difficulty", "Easy"),
                language=language,
                code=code,
                status=judge_res["status"],
                passed_count=judge_res["passed_count"],
                total_count=judge_res["total_count"],
                score=awarded_score,
                runtime=judge_res["runtime"]
            )

            self.send_json({
                "submission_id": submission["id"],
                "status": judge_res["status"],
                "passed_count": judge_res["passed_count"],
                "total_count": judge_res["total_count"],
                "score_earned": awarded_score,
                "effective_max_points": effective_max_points,
                "hint_penalty": hint_penalty,
                "already_solved": already_solved,
                "participant_score": submission.get("participant_score", 0),
                "runtime": judge_res["runtime"],
                "error_message": judge_res.get("error_message")
            })
            return

        # POST /api/admin/login
        if path == "/api/admin/login":
            admin_id = body.get("admin_id") or body.get("username")
            password = body.get("password", "")

            valid = False
            if admin_id:
                valid = self.auth.verify_admin_credentials(admin_id, password)
            else:
                valid = self.auth.verify_admin_password(password)

            if valid:
                token = self.auth.create_session_token(self.auth.admin_id, "Administrator", expiry_hours=24)
                self.send_json({
                    "success": True,
                    "authenticated": True,
                    "token": token,
                    "admin_id": self.auth.admin_id,
                    "message": "Admin authenticated successfully."
                })
            else:
                self.send_error_json("Invalid Admin ID or Password.", 401)
            return

        # POST /api/admin/get-solution or /api/problems/unlock-solution
        if path in ["/api/admin/get-solution", "/api/problems/unlock-solution"]:
            if not self.is_admin_authenticated(body):
                self.send_error_json("Access denied. Invalid Admin ID or Password.", 401)
                return

            problem_id = (body.get("problem_id") or "").strip().lower()
            language = (body.get("language") or "python").strip().lower()

            prob_detail = self.problems_manager.get_problem_detail(problem_id)
            if not prob_detail:
                self.send_error_json("Problem not found.", 404)
                return

            pid = prob_detail["id"]
            solutions = self.problems_manager.get_solutions_for_problem(pid)
            sol_code = solutions.get(language) or solutions.get("python") or ""

            if not sol_code:
                self.send_error_json(f"No solution found for problem '{pid}' in {language.upper()}.", 404)
                return

            token = body.get("token")
            if not token:
                token = self.auth.create_session_token(self.auth.admin_id, "Administrator", expiry_hours=24)

            self.send_json({
                "success": True,
                "problem_id": pid,
                "language": language,
                "solution": sol_code,
                "solutions": solutions,
                "token": token,
                "admin_id": self.auth.admin_id,
                "message": f"Solution for {prob_detail.get('title', pid)} unlocked successfully."
            })
            return

        # POST /api/admin/reset
        if path == "/api/admin/reset":
            if not self.is_admin_authenticated(body):
                self.send_error_json("Unauthorized. Admin credentials or active session required.", 401)
                return

            self.storage.reset_competition()
            self.send_json({"success": True, "message": "Competition data has been completely reset."})
            return

        # POST /api/admin/switch-set
        if path == "/api/admin/switch-set":
            if not self.is_admin_authenticated(body):
                self.send_error_json("Unauthorized. Invalid admin password or token.", 401)
                return

            set_id = body.get("set_id", "set1").strip().lower()
            reset_data = body.get("reset_data", True)

            switched = self.problems_manager.switch_set(set_id)
            if not switched:
                self.send_error_json(f"Problem set '{set_id}' not found.", 404)
                return

            self.config["active_problem_set"] = set_id
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
            if os.path.exists(config_path):
                try:
                    with open(config_path, "w", encoding="utf-8") as f:
                        json.dump(self.config, f, indent=2)
                except Exception:
                    pass

            if reset_data:
                self.storage.reset_competition()

            self.send_json({
                "success": True,
                "active_set": set_id,
                "total_problems": len(self.problems_manager.problems),
                "message": f"Successfully activated {set_id.upper()} ({len(self.problems_manager.problems)} problems)."
            })
            return

        # POST /api/admin/change-password
        if path == "/api/admin/change-password":
            old_password = body.get("old_password", "")
            current_id = body.get("current_admin_id") or body.get("admin_id")
            new_id = body.get("new_admin_id") or body.get("new_id")
            new_password = body.get("new_password", "").strip()

            auth_valid = False
            if current_id:
                auth_valid = self.auth.verify_admin_credentials(current_id, old_password)
            elif old_password:
                auth_valid = self.auth.verify_admin_password(old_password)
            elif self.is_admin_authenticated(body):
                auth_valid = True

            if not auth_valid:
                self.send_error_json("Current admin credentials are incorrect.", 401)
                return

            if new_password and len(new_password) < 4:
                self.send_error_json("New password must be at least 4 characters long.", 400)
                return

            if new_id or new_password:
                self.auth.update_admin_credentials(new_id=new_id, new_password=new_password if new_password else None)

            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
            if os.path.exists(config_path):
                try:
                    with open(config_path, "w", encoding="utf-8") as f:
                        json.dump(self.config, f, indent=2)
                except Exception:
                    pass

            self.send_json({
                "success": True,
                "admin_id": self.auth.admin_id,
                "message": "Admin credentials updated successfully."
            })
            return

        # POST /api/admin/toggle-tier-lock or /api/admin/tier-locks or /api/admin/unlock-round
        if path in ["/api/admin/toggle-tier-lock", "/api/admin/tier-locks", "/api/admin/unlock-round"]:
            if not self.is_admin_authenticated(body):
                self.send_error_json("Unauthorized. Admin ID & Password or active session required.", 401)
                return

            tier_locks = dict(self.config.get("tier_locks", {"easy": False, "medium": False, "hard": False}))
            preset = body.get("preset")
            tier = (body.get("tier") or "").strip().lower()
            locked = body.get("locked")
            custom_locks = body.get("tier_locks")

            msg = "Round locks updated successfully."
            if preset:
                preset = preset.lower().strip()
                if preset in ["round1", "round1_only", "easy_only"]:
                    tier_locks = {"easy": False, "medium": True, "hard": True}
                    msg = "Preset applied: Round 1 Only (Easy Active, Medium & Hard Locked)."
                elif preset in ["round1_2", "round2", "easy_medium"]:
                    tier_locks = {"easy": False, "medium": False, "hard": True}
                    msg = "Preset applied: Round 1 & 2 Active (Easy & Medium Active, Hard Locked)."
                elif preset in ["all", "round1_2_3", "unlock_all", "all_unlocked"]:
                    tier_locks = {"easy": False, "medium": False, "hard": False}
                    msg = "Preset applied: All Rounds Active (Easy, Medium & Hard Unlocked)."
                elif preset in ["lock_all", "all_locked"]:
                    tier_locks = {"easy": True, "medium": True, "hard": True}
                    msg = "Preset applied: All Rounds Locked."
            elif tier in ["easy", "medium", "hard"] and locked is not None:
                tier_locks[tier] = bool(locked)
                status_str = "Locked 🔒" if bool(locked) else "Unlocked 🔓"
                msg = f"Round ({tier.capitalize()}) has been {status_str}."
            elif isinstance(custom_locks, dict):
                for k in ["easy", "medium", "hard"]:
                    if k in custom_locks:
                        tier_locks[k] = bool(custom_locks[k])

            self.config["tier_locks"] = tier_locks

            # Persist to config.json
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
            if os.path.exists(config_path):
                try:
                    with open(config_path, "w", encoding="utf-8") as f:
                        json.dump(self.config, f, indent=2)
                except Exception as e:
                    print(f"[Server] Error saving config.json: {e}")

            token = body.get("token")
            if not token and (body.get("admin_id") or body.get("password")):
                token = self.auth.create_session_token(self.auth.admin_id, "Administrator", expiry_hours=24)

            self.send_json({
                "success": True,
                "tier_locks": tier_locks,
                "token": token,
                "message": msg
            })
            return

        self.send_error_json("API route not found", 404)

    def handle_api_delete(self, path: str):
        if path == "/api/admin/reset":
            self.storage.reset_competition()
            self.send_json({"success": True, "message": "Competition data reset."})
            return
        self.send_error_json("Invalid DELETE route", 404)
