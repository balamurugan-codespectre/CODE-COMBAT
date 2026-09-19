"""
CODE COMBAT - Local JSON Database & Storage Manager
Handles participants, submissions, and live leaderboard calculations locally.
"""

import os
import json
import uuid
import datetime
import threading
from typing import Dict, Any, List, Optional, Set


class Storage:
    """Thread-safe JSON persistence for offline competition data."""

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.lock = threading.Lock()
        os.makedirs(self.data_dir, exist_ok=True)

        self.participants_file = os.path.join(self.data_dir, "participants.json")
        self.submissions_file = os.path.join(self.data_dir, "submissions.json")
        self.leaderboard_file = os.path.join(self.data_dir, "leaderboard.json")

        self._init_files()

    def _init_files(self):
        """Initializes empty JSON files if they don't already exist."""
        for file_path in [self.participants_file, self.submissions_file, self.leaderboard_file]:
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=2)

    def _read_json(self, file_path: str) -> List[Dict[str, Any]]:
        try:
            if not os.path.exists(file_path):
                return []
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _write_json(self, file_path: str, data: Any):
        temp_file = file_path + ".tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        if os.path.exists(file_path):
            os.remove(file_path)
        os.rename(temp_file, file_path)

    # ------------------- Participants -------------------

    def register_participant(self, name: str, college: str, reg_no: str) -> Dict[str, Any]:
        with self.lock:
            participants = self._read_json(self.participants_file)
            
            # Check for existing registration with same reg_no or name
            clean_reg = reg_no.strip().upper()
            clean_name = name.strip()

            for p in participants:
                if p.get("reg_no", "").strip().upper() == clean_reg and clean_reg:
                    # Return existing participant
                    return p

            participant = {
                "id": str(uuid.uuid4())[:8],
                "name": clean_name,
                "college": college.strip(),
                "reg_no": clean_reg,
                "registered_at": datetime.datetime.now().isoformat(),
                "score": 0,
                "solved_problems": []
            }
            participants.append(participant)
            self._write_json(self.participants_file, participants)
            return participant

    def get_participants(self) -> List[Dict[str, Any]]:
        with self.lock:
            return self._read_json(self.participants_file)

    def get_participant(self, participant_id: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            participants = self._read_json(self.participants_file)
            for p in participants:
                if p.get("id") == participant_id:
                    return p
            return None

    def get_solved_problems(self, participant_id: str) -> Set[str]:
        with self.lock:
            submissions = self._read_json(self.submissions_file)
            solved = set()
            for sub in submissions:
                if sub.get("participant_id") == participant_id and sub.get("status") == "ACCEPTED":
                    solved.add(sub.get("problem_id"))
            return solved

    # ------------------- Submissions -------------------

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
            submissions = self._read_json(self.submissions_file)
            participants = self._read_json(self.participants_file)

            submission_id = f"SUB-{len(submissions) + 1:04d}"
            timestamp = datetime.datetime.now().isoformat()

            submission = {
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
                "timestamp": timestamp
            }
            submissions.insert(0, submission)  # Newest first
            self._write_json(self.submissions_file, submissions)

            # Update participant record if solved
            for p in participants:
                if p.get("id") == participant_id:
                    if status == "ACCEPTED" and problem_id not in p.get("solved_problems", []):
                        p.setdefault("solved_problems", []).append(problem_id)
                        p["score"] = p.get("score", 0) + score
            self._write_json(self.participants_file, participants)

            # Recalculate leaderboard
            self._recalculate_leaderboard_locked()

            return submission

    def get_submissions(self, participant_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        with self.lock:
            submissions = self._read_json(self.submissions_file)
            if participant_id:
                filtered = [s for s in submissions if s.get("participant_id") == participant_id]
                return filtered[:limit]
            return submissions[:limit]

    # ------------------- Leaderboard -------------------

    def recalculate_leaderboard(self) -> List[Dict[str, Any]]:
        with self.lock:
            return self._recalculate_leaderboard_locked()

    def _recalculate_leaderboard_locked(self) -> List[Dict[str, Any]]:
        participants = self._read_json(self.participants_file)
        submissions = self._read_json(self.submissions_file)

        # Map participant stats
        stats = {}
        for p in participants:
            pid = p["id"]
            stats[pid] = {
                "participant_id": pid,
                "name": p.get("name", "Anonymous"),
                "college": p.get("college", "-"),
                "reg_no": p.get("reg_no", "-"),
                "score": 0,
                "solved_count": 0,
                "easy_solved": 0,
                "medium_solved": 0,
                "hard_solved": 0,
                "solved_set": set(),
                "total_runtime": 0.0,
                "last_submission_time": p.get("registered_at", "")
            }

        # Scan submissions in chronological order (reverse of newest-first)
        for sub in reversed(submissions):
            pid = sub.get("participant_id")
            if pid not in stats:
                continue

            prob_id = sub.get("problem_id")
            status = sub.get("status")
            diff = sub.get("difficulty", "easy").lower()
            score = sub.get("score", 0)
            runtime = sub.get("runtime", 0.0)
            ts = sub.get("timestamp", "")

            if status == "ACCEPTED" and prob_id not in stats[pid]["solved_set"]:
                stats[pid]["solved_set"].add(prob_id)
                stats[pid]["score"] += score
                stats[pid]["solved_count"] += 1
                stats[pid]["total_runtime"] += runtime
                stats[pid]["last_submission_time"] = ts

                if diff == "easy":
                    stats[pid]["easy_solved"] += 1
                elif diff == "medium":
                    stats[pid]["medium_solved"] += 1
                elif diff == "hard":
                    stats[pid]["hard_solved"] += 1

        leaderboard = list(stats.values())
        # Remove internal set
        for item in leaderboard:
            del item["solved_set"]
            item["total_runtime"] = round(item["total_runtime"], 3)

        # Sort rules: Score DESC -> Solved count DESC -> Total runtime ASC -> Last submission time ASC
        leaderboard.sort(key=lambda x: (
            -x["score"],
            -x["solved_count"],
            x["total_runtime"],
            x["last_submission_time"]
        ))

        # Assign ranks
        for idx, entry in enumerate(leaderboard, start=1):
            entry["rank"] = idx

        self._write_json(self.leaderboard_file, leaderboard)
        return leaderboard

    def get_leaderboard(self) -> List[Dict[str, Any]]:
        with self.lock:
            data = self._read_json(self.leaderboard_file)
            if not data:
                return self._recalculate_leaderboard_locked()
            return data

    # ------------------- Administration -------------------

    def reset_competition(self):
        """Wipes participants, submissions, and leaderboard."""
        with self.lock:
            self._write_json(self.participants_file, [])
            self._write_json(self.submissions_file, [])
            self._write_json(self.leaderboard_file, [])

    def export_all_data(self) -> Dict[str, Any]:
        with self.lock:
            return {
                "exported_at": datetime.datetime.now().isoformat(),
                "participants": self._read_json(self.participants_file),
                "submissions": self._read_json(self.submissions_file),
                "leaderboard": self._read_json(self.leaderboard_file)
            }
