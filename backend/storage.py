"""
CODE COMBAT Pro - Dual Persistence Storage Engine (SQLite WAL + JSON Auto-Sync)
Provides ACID transactions, reentrant thread safety (RLock), and live leaderboard calculation.
"""

import os
import json
import sqlite3
import datetime
import threading
from typing import Dict, Any, List, Optional, Set


class Storage:
    """Thread-safe SQLite database with WAL mode and automatic JSON mirrors."""

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.lock = threading.RLock()
        os.makedirs(self.data_dir, exist_ok=True)

        self.db_path = os.path.join(self.data_dir, "code_combat.db")
        self.participants_file = os.path.join(self.data_dir, "participants.json")
        self.submissions_file = os.path.join(self.data_dir, "submissions.json")
        self.leaderboard_file = os.path.join(self.data_dir, "leaderboard.json")
        self.audit_file = os.path.join(self.data_dir, "audit_log.json")

        self._init_sqlite()
        self._sync_json_mirrors()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=20.0, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_sqlite(self):
        with self.lock:
            conn = self._get_connection()
            try:
                with conn:
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS participants (
                            id TEXT PRIMARY KEY,
                            name TEXT NOT NULL,
                            college TEXT NOT NULL,
                            reg_no TEXT NOT NULL UNIQUE,
                            score INTEGER DEFAULT 0,
                            registered_at TEXT NOT NULL
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS submissions (
                            id TEXT PRIMARY KEY,
                            participant_id TEXT NOT NULL,
                            participant_name TEXT NOT NULL,
                            problem_id TEXT NOT NULL,
                            problem_title TEXT NOT NULL,
                            difficulty TEXT NOT NULL,
                            language TEXT NOT NULL,
                            code TEXT NOT NULL,
                            status TEXT NOT NULL,
                            passed_count INTEGER NOT NULL,
                            total_count INTEGER NOT NULL,
                            score INTEGER NOT NULL,
                            runtime REAL NOT NULL,
                            timestamp TEXT NOT NULL,
                            FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS solved_problems (
                            participant_id TEXT NOT NULL,
                            problem_id TEXT NOT NULL,
                            score INTEGER NOT NULL,
                            solved_at TEXT NOT NULL,
                            PRIMARY KEY (participant_id, problem_id),
                            FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS hint_unlocks (
                            participant_id TEXT NOT NULL,
                            problem_id TEXT NOT NULL,
                            hint_index INTEGER NOT NULL,
                            penalty INTEGER NOT NULL,
                            unlocked_at TEXT NOT NULL,
                            PRIMARY KEY (participant_id, problem_id, hint_index),
                            FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS audit_logs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            action TEXT NOT NULL,
                            details TEXT NOT NULL,
                            ip_address TEXT,
                            timestamp TEXT NOT NULL
                        );
                    """)
            finally:
                conn.close()

    def _write_json(self, file_path: str, data: Any):
        temp_file = file_path + ".tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        if os.path.exists(file_path):
            os.remove(file_path)
        os.rename(temp_file, file_path)

    def _sync_json_mirrors(self):
        """Dumps latest database tables to JSON mirrors for offline transparency."""
        try:
            participants = self.get_participants()
            submissions = self.get_submissions(limit=1000)
            leaderboard = self.get_leaderboard()

            self._write_json(self.participants_file, participants)
            self._write_json(self.submissions_file, submissions)
            self._write_json(self.leaderboard_file, leaderboard)
        except Exception:
            pass

    # ------------------- Participants -------------------

    def register_participant(self, name: str, college: str, reg_no: str) -> Dict[str, Any]:
        with self.lock:
            clean_name = name.strip()
            clean_college = college.strip() or "N/A"
            clean_reg = reg_no.strip().upper()

            conn = self._get_connection()
            try:
                # Check for existing registration
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM participants WHERE reg_no = ?", (clean_reg,))
                row = cursor.fetchone()
                if row:
                    p = dict(row)
                    p["solved_problems"] = list(self.get_solved_problems(p["id"]))
                    return p

                import uuid
                pid = f"user_{uuid.uuid4().hex[:8]}"
                now = datetime.datetime.now().isoformat()

                with conn:
                    conn.execute(
                        "INSERT INTO participants (id, name, college, reg_no, score, registered_at) VALUES (?, ?, ?, ?, ?, ?)",
                        (pid, clean_name, clean_college, clean_reg, 0, now)
                    )
                    conn.execute(
                        "INSERT INTO audit_logs (action, details, timestamp) VALUES (?, ?, ?)",
                        ("REGISTER", f"Participant registered: {clean_name} ({clean_reg})", now)
                    )

                new_p = {
                    "id": pid,
                    "name": clean_name,
                    "college": clean_college,
                    "reg_no": clean_reg,
                    "score": 0,
                    "registered_at": now,
                    "solved_problems": []
                }
                self._sync_json_mirrors()
                return new_p
            finally:
                conn.close()

    def get_participants(self) -> List[Dict[str, Any]]:
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM participants ORDER BY registered_at ASC")
                rows = cursor.fetchall()
                results = []
                for r in rows:
                    item = dict(r)
                    item["solved_problems"] = list(self.get_solved_problems(item["id"]))
                    results.append(item)
                return results
            finally:
                conn.close()

    def get_participant(self, participant_id: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM participants WHERE id = ?", (participant_id,))
                row = cursor.fetchone()
                if not row:
                    return None
                p = dict(row)
                p["solved_problems"] = list(self.get_solved_problems(participant_id))
                return p
            finally:
                conn.close()

    # ------------------- Submissions & Scoring -------------------

    def add_submission(
        self,
        participant_id: str,
        participant_name: str,
        problem_id: str,
        problem_title: str,
        difficulty: str,
        language: str,
        code: str,
        status: str,
        passed_count: int,
        total_count: int,
        score: int,
        runtime: float
    ) -> Dict[str, Any]:
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM submissions")
                count = cursor.fetchone()[0]
                submission_id = f"SUB-{count + 1:04d}"
                now = datetime.datetime.now().isoformat()

                with conn:
                    # Guarantee participant existence
                    conn.execute("""
                        INSERT OR IGNORE INTO participants (id, name, college, reg_no, score, registered_at)
                        VALUES (?, ?, 'N/A', 'N/A', 0, ?)
                    """, (participant_id, participant_name or "Anonymous", now))

                    conn.execute("""
                        INSERT INTO submissions (
                            id, participant_id, participant_name, problem_id, problem_title,
                            difficulty, language, code, status, passed_count, total_count,
                            score, runtime, timestamp
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        submission_id, participant_id, participant_name, problem_id, problem_title,
                        difficulty, language, code, status, passed_count, total_count,
                        score, runtime, now
                    ))

                    if status == "ACCEPTED":
                        # Insert or update solved problems with max score
                        conn.execute("""
                            INSERT INTO solved_problems (participant_id, problem_id, score, solved_at)
                            VALUES (?, ?, ?, ?)
                            ON CONFLICT(participant_id, problem_id) DO UPDATE SET
                            score = MAX(score, excluded.score);
                        """, (participant_id, problem_id, score, now))

                        # Recalculate participant total score
                        conn.execute("""
                            UPDATE participants
                            SET score = (
                                SELECT COALESCE(SUM(score), 0)
                                FROM solved_problems
                                WHERE participant_id = ?
                            )
                            WHERE id = ?;
                        """, (participant_id, participant_id))

                sub = {
                    "id": submission_id,
                    "participant_id": participant_id,
                    "participant_name": participant_name,
                    "problem_id": problem_id,
                    "problem_title": problem_title,
                    "difficulty": difficulty,
                    "language": language,
                    "code": code,
                    "status": status,
                    "passed_count": passed_count,
                    "total_count": total_count,
                    "score": score,
                    "runtime": runtime,
                    "timestamp": now
                }
                self._sync_json_mirrors()
                return sub
            finally:
                conn.close()

    def get_solved_problems(self, participant_id: str) -> Set[str]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT problem_id FROM solved_problems WHERE participant_id = ?", (participant_id,))
            rows = cursor.fetchall()
            return {r[0] for r in rows}
        finally:
            conn.close()

    def get_submissions(self, participant_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                if participant_id:
                    cursor.execute("SELECT * FROM submissions WHERE participant_id = ? ORDER BY timestamp DESC LIMIT ?", (participant_id, limit))
                else:
                    cursor.execute("SELECT * FROM submissions ORDER BY timestamp DESC LIMIT ?", (limit,))
                rows = cursor.fetchall()
                return [dict(r) for r in rows]
            finally:
                conn.close()

    # ------------------- Leaderboard -------------------

    def get_leaderboard(self) -> List[Dict[str, Any]]:
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT
                        p.id as participant_id,
                        p.name,
                        p.college,
                        p.reg_no,
                        p.score,
                        p.registered_at,
                        COUNT(sp.problem_id) as solved_count,
                        COALESCE(SUM(CASE WHEN LOWER(s.difficulty) = 'easy' THEN 1 ELSE 0 END), 0) as easy_solved,
                        COALESCE(SUM(CASE WHEN LOWER(s.difficulty) = 'medium' THEN 1 ELSE 0 END), 0) as medium_solved,
                        COALESCE(SUM(CASE WHEN LOWER(s.difficulty) = 'hard' THEN 1 ELSE 0 END), 0) as hard_solved,
                        COALESCE(SUM(s.runtime), 0.0) as total_runtime,
                        COALESCE(MAX(s.timestamp), p.registered_at) as last_submission_time
                    FROM participants p
                    LEFT JOIN solved_problems sp ON p.id = sp.participant_id
                    LEFT JOIN (
                        SELECT participant_id, problem_id, difficulty, runtime, timestamp
                        FROM submissions
                        WHERE status = 'ACCEPTED'
                        GROUP BY participant_id, problem_id
                    ) s ON sp.participant_id = s.participant_id AND sp.problem_id = s.problem_id
                    GROUP BY p.id
                    ORDER BY
                        p.score DESC,
                        solved_count DESC,
                        total_runtime ASC,
                        last_submission_time ASC;
                """)
                rows = cursor.fetchall()
                leaderboard = []
                for idx, r in enumerate(rows, start=1):
                    item = dict(r)
                    item["rank"] = idx
                    item["total_runtime"] = round(item["total_runtime"], 3)
                    leaderboard.append(item)
                return leaderboard
            finally:
                conn.close()

    # ------------------- Hint Management & Penalties -------------------

    def unlock_hint(self, participant_id: str, problem_id: str, hint_index: int, penalty: int) -> Dict[str, Any]:
        """Records that a participant unlocked a hint and stores the penalty."""
        with self.lock:
            conn = self._get_connection()
            try:
                now = datetime.datetime.now().isoformat()
                with conn:
                    conn.execute("""
                        INSERT OR IGNORE INTO hint_unlocks (participant_id, problem_id, hint_index, penalty, unlocked_at)
                        VALUES (?, ?, ?, ?, ?);
                    """, (participant_id, problem_id, int(hint_index), int(penalty), now))
                return {
                    "participant_id": participant_id,
                    "problem_id": problem_id,
                    "hint_index": hint_index,
                    "penalty": penalty,
                    "unlocked": True
                }
            finally:
                conn.close()

    def get_unlocked_hints(self, participant_id: str, problem_id: str) -> List[int]:
        """Returns the list of unlocked hint indices (e.g. [1, 2]) for a participant on a problem."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT hint_index FROM hint_unlocks
                WHERE participant_id = ? AND problem_id = ?
                ORDER BY hint_index ASC;
            """, (participant_id, problem_id))
            rows = cursor.fetchall()
            return [int(r[0]) for r in rows]
        finally:
            conn.close()

    def get_total_hint_penalty(self, participant_id: str, problem_id: str) -> int:
        """Returns the total point deduction for unlocked hints on a problem."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COALESCE(SUM(penalty), 0) FROM hint_unlocks
                WHERE participant_id = ? AND problem_id = ?;
            """, (participant_id, problem_id))
            row = cursor.fetchone()
            return int(row[0]) if row else 0
        finally:
            conn.close()

    # ------------------- Administration -------------------

    def reset_competition(self):
        """Wipes participants, submissions, solved problems, hint unlocks, and audit logs."""
        with self.lock:
            conn = self._get_connection()
            try:
                with conn:
                    conn.execute("DELETE FROM submissions;")
                    conn.execute("DELETE FROM solved_problems;")
                    conn.execute("DELETE FROM hint_unlocks;")
                    conn.execute("DELETE FROM participants;")
                    conn.execute("DELETE FROM audit_logs;")
                self._sync_json_mirrors()
            finally:
                conn.close()

    def export_all_data(self) -> Dict[str, Any]:
        with self.lock:
            return {
                "exported_at": datetime.datetime.now().isoformat(),
                "participants": self.get_participants(),
                "submissions": self.get_submissions(limit=5000),
                "leaderboard": self.get_leaderboard()
            }

    def get_audit_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
                return [dict(r) for r in cursor.fetchall()]
            finally:
                conn.close()
