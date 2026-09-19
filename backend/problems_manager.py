"""
CODE COMBAT - Problems Manager
Discovers, validates, and manages problems and test suites across difficulty tiers.
"""

import os
import json
import shutil
import glob
from typing import Dict, Any, List, Optional, Set


class ProblemsManager:
    """Manages problem metadata, starter templates, visible samples, and hidden test suites."""

    def __init__(self, problems_dir: str):
        self.problems_dir = problems_dir
        self.problems: Dict[str, Dict[str, Any]] = {}
        self.hidden_dirs: Dict[str, str] = {}
        self.reload_problems()

    def reload_problems(self):
        """Scans the problems directory and indexes all problems."""
        self.problems.clear()
        self.hidden_dirs.clear()

        if not os.path.exists(self.problems_dir):
            os.makedirs(self.problems_dir, exist_ok=True)
            return

        for difficulty in ["easy", "medium", "hard"]:
            diff_dir = os.path.join(self.problems_dir, difficulty)
            if not os.path.isdir(diff_dir):
                continue

            for prob_slug in os.listdir(diff_dir):
                prob_path = os.path.join(diff_dir, prob_slug)
                if not os.path.isdir(prob_path):
                    continue

                json_file = os.path.join(prob_path, "problem.json")
                if os.path.exists(json_file):
                    try:
                        with open(json_file, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            prob_id = data.get("id", prob_slug)
                            data["id"] = prob_id
                            data["difficulty"] = data.get("difficulty", difficulty.capitalize())
                            data["slug"] = prob_slug
                            data["dir_path"] = prob_path

                            hidden_dir = os.path.join(prob_path, "hidden_tests")
                            self.hidden_dirs[prob_id] = hidden_dir
                            self.problems[prob_id] = data
                    except Exception as e:
                        print(f"[ProblemsManager] Error loading {json_file}: {e}")

    def get_problem_list(self, solved_set: Optional[Set[str]] = None) -> List[Dict[str, Any]]:
        """
        Returns a list of problems for the dashboard.
        Guarantees hidden tests are never exposed.
        """
        solved_set = solved_set or set()
        problem_list = []

        difficulty_order = {"Easy": 1, "Medium": 2, "Hard": 3}

        for prob_id, data in self.problems.items():
            diff = data.get("difficulty", "Easy")
            is_solved = prob_id in solved_set

            problem_list.append({
                "id": prob_id,
                "title": data.get("title", prob_id),
                "difficulty": diff,
                "difficulty_rank": difficulty_order.get(diff, 1),
                "points": data.get("points", 100),
                "time_limit": data.get("time_limit", 2.0),
                "category": data.get("category", "General"),
                "status": "Solved" if is_solved else "Not Started",
                "solved": is_solved
            })

        # Sort: Easy -> Medium -> Hard, then Title
        problem_list.sort(key=lambda p: (p["difficulty_rank"], p["title"]))
        return problem_list

    def get_problem_detail(self, problem_id: str) -> Optional[Dict[str, Any]]:
        """
        Returns sanitized problem details including visible sample tests and starter codes.
        NEVER returns hidden tests.
        """
        if problem_id not in self.problems:
            return None

        raw = self.problems[problem_id]
        return {
            "id": raw.get("id"),
            "title": raw.get("title"),
            "difficulty": raw.get("difficulty"),
            "points": raw.get("points"),
            "time_limit": raw.get("time_limit", 2.0),
            "category": raw.get("category", "General"),
            "description": raw.get("description", ""),
            "input_format": raw.get("input_format", ""),
            "output_format": raw.get("output_format", ""),
            "constraints": raw.get("constraints", ""),
            "sample_tests": raw.get("sample_tests", []),
            "starter_code": raw.get("starter_code", {})
        }

    def get_hidden_tests_dir(self, problem_id: str) -> Optional[str]:
        """Internal judge accessor to locate the server-side hidden test directory."""
        return self.hidden_dirs.get(problem_id)

    def save_problem(self, problem_data: Dict[str, Any], hidden_tests: Optional[List[Dict[str, str]]] = None) -> bool:
        """Admin helper to create or update a problem and its test cases."""
        prob_id = problem_data.get("id", "").strip().lower().replace(" ", "_")
        difficulty = problem_data.get("difficulty", "Easy").lower()

        if difficulty not in ["easy", "medium", "hard"]:
            difficulty = "easy"

        target_dir = os.path.join(self.problems_dir, difficulty, prob_id)
        os.makedirs(target_dir, exist_ok=True)

        json_path = os.path.join(target_dir, "problem.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(problem_data, f, indent=2)

        if hidden_tests:
            hidden_dir = os.path.join(target_dir, "hidden_tests")
            os.makedirs(hidden_dir, exist_ok=True)
            for idx, ht in enumerate(hidden_tests, start=1):
                test_file = os.path.join(hidden_dir, f"test{idx}.txt")
                with open(test_file, "w", encoding="utf-8") as f:
                    f.write(f"INPUT:\n{ht.get('input', '').strip()}\nEXPECTED:\n{ht.get('output', '').strip()}\n")

        self.reload_problems()
        return True

    def delete_problem(self, problem_id: str) -> bool:
        """Admin helper to delete a problem from the disk."""
        if problem_id not in self.problems:
            return False
        prob_dir = self.problems[problem_id].get("dir_path")
        if prob_dir and os.path.exists(prob_dir):
            shutil.rmtree(prob_dir, ignore_errors=True)
            self.reload_problems()
            return True
        return False
