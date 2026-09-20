"""
CODE COMBAT - Problems Manager
Discovers, validates, and manages problems, LeetCode metadata, 3-tier hints, and test suites.
"""

import os
import json
import shutil
import glob
from typing import Dict, Any, List, Optional, Set

try:
    from judge.harness import Harness
except ImportError:
    try:
        from ..judge.harness import Harness
    except Exception:
        Harness = None

try:
    from .solutions_registry import SOLUTIONS_REGISTRY, get_all_solutions_for_problem
except ImportError:
    try:
        from backend.solutions_registry import SOLUTIONS_REGISTRY, get_all_solutions_for_problem
    except Exception:
        SOLUTIONS_REGISTRY = {}
        get_all_solutions_for_problem = lambda pid: {}


class ProblemsManager:
    """Manages problem metadata, starter templates, visible samples, hints, and hidden test suites."""

    METADATA_REGISTRY = {
        # ============================== EASY (5) ==============================
        "two_sum": {
            "number": 1,
            "topics": ["Array", "Hash Table"],
            "companies": ["Amazon", "Google", "Meta", "Microsoft", "Apple", "Bloomberg"],
            "hints": [
                "A brute-force solution checks all pairs of numbers, which requires O(n^2) time. We can do much better!",
                "If we fix the first number x, we need to find target - x in the array. What data structure allows O(1) average time lookups?",
                "Use a Hash Map! As you iterate through nums, check if target - nums[i] is already in the map. If so, return its index and i; otherwise insert nums[i] -> i."
            ],
            "leetcode_examples": [
                {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."},
                {"input": "nums = [3,2,4], target = 6", "output": "[1,2]", "explanation": "Because nums[1] + nums[2] == 6, we return [1, 2]."},
                {"input": "nums = [3,3], target = 6", "output": "[0,1]", "explanation": "Because nums[0] + nums[1] == 6, we return [0, 1]."}
            ]
        },

        "reverse_string": {
            "number": 344,
            "topics": ["Two Pointers", "String"],
            "companies": ["Amazon", "Google", "Apple", "Microsoft"],
            "hints": [
                "The problem requires reversing the characters with O(1) extra memory in-place.",
                "Set two pointers: left at index 0 and right at index len(s) - 1.",
                "While left < right, swap s[left] and s[right], then advance left++ and decrement right--."
            ],
            "leetcode_examples": [
                {"input": "s = [\"h\",\"e\",\"l\",\"l\",\"o\"]", "output": "[\"o\",\"l\",\"l\",\"e\",\"h\"]", "explanation": "Reverses the array of characters."},
                {"input": "s = [\"H\",\"a\",\"n\",\"n\",\"a\",\"h\"]", "output": "[\"h\",\"a\",\"n\",\"n\",\"a\",\"H\"]", "explanation": "Reverses the characters in place."}
            ]
        },

        "find_duplicate": {
            "number": 287,
            "topics": ["Array", "Two Pointers", "Binary Search", "Bit Manipulation"],
            "companies": ["Amazon", "Google", "Microsoft", "Meta"],
            "hints": [
                "You are given an array of numbers where at least one number repeats.",
                "You can use a frequency set or hash set to detect the first element that repeats.",
                "Floyd's Tortoise and Hare cycle detection algorithm can also find the duplicate in O(n) time and O(1) extra space."
            ],
            "leetcode_examples": [
                {"input": "nums = [1,3,4,2,2]", "output": "2", "explanation": "2 is the duplicate number."},
                {"input": "nums = [3,1,3,4,2]", "output": "3", "explanation": "3 appears twice."}
            ]
        },

        "valid_parentheses": {
            "number": 20,
            "topics": ["String", "Stack"],
            "companies": ["Amazon", "Meta", "Google", "Microsoft", "Bloomberg"],
            "hints": [
                "Use a LIFO (Last-In-First-Out) data structure to keep track of open brackets.",
                "When encountering an opening bracket '(', '{', or '[', push the corresponding closing bracket onto the stack.",
                "When encountering a closing bracket, pop from the stack and verify that it matches. The string is valid iff the stack is empty at the end."
            ],
            "leetcode_examples": [
                {"input": "s = \"()\"", "output": "true", "explanation": "Matching parentheses."},
                {"input": "s = \"()[]{}\"", "output": "true", "explanation": "All bracket pairs match in correct sequence."},
                {"input": "s = \"(]\"", "output": "false", "explanation": "Mismatched bracket pair."}
            ]
        },

        "reverse_linked_list": {
            "number": 206,
            "topics": ["Linked List", "Recursion"],
            "companies": ["Amazon", "Microsoft", "Google", "Apple", "Meta"],
            "hints": [
                "Maintain three pointers: prev (initially None), curr (initially head), and nxt.",
                "At each step, store curr.next in nxt, point curr.next to prev, then advance prev = curr and curr = nxt.",
                "When curr reaches null, prev is the new head of the reversed list."
            ],
            "leetcode_examples": [
                {"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]", "explanation": "Linked list reversed."},
                {"input": "head = [1,2]", "output": "[2,1]", "explanation": "Reversed two-node list."}
            ]
        },

        # ============================== MEDIUM (5) ==============================
        "longest_substring": {
            "number": 3,
            "topics": ["Hash Table", "String", "Sliding Window"],
            "companies": ["Amazon", "Google", "Bloomberg", "Meta", "Microsoft"],
            "hints": [
                "Use a sliding window with two pointers [left, right] to represent the current substring without duplicates.",
                "Store the last seen index of each character in a Hash Map.",
                "When right sees duplicate char at last_pos >= left, jump left = last_pos + 1. Update max_len = max(max_len, right - left + 1)."
            ],
            "leetcode_examples": [
                {"input": "s = \"abcabcbb\"", "output": "3", "explanation": "The answer is \"abc\", with the length of 3."},
                {"input": "s = \"bbbbb\"", "output": "1", "explanation": "The answer is \"b\", with the length of 1."},
                {"input": "s = \"pwwkew\"", "output": "3", "explanation": "The answer is \"wke\", with the length of 3."}
            ]
        },

        "three_sum": {
            "number": 15,
            "topics": ["Array", "Two Pointers", "Sorting"],
            "companies": ["Amazon", "Meta", "Apple", "Google", "Microsoft"],
            "hints": [
                "Sort the array in ascending order first. This makes duplicate elimination and two-pointer navigation easy.",
                "Iterate i through the array. If nums[i] == nums[i-1], skip to avoid duplicate triplets.",
                "For each i, use two pointers left = i + 1 and right = n - 1. If nums[i] + nums[left] + nums[right] == 0, record the triplet and skip identical adjacent values."
            ],
            "leetcode_examples": [
                {"input": "nums = [-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]", "explanation": "The distinct triplets are [-1,0,1] and [-1,-1,2]."},
                {"input": "nums = [0,1,1]", "output": "[]", "explanation": "No possible triplet sums to 0."}
            ]
        },

        "merge_intervals": {
            "number": 56,
            "topics": ["Array", "Sorting"],
            "companies": ["Amazon", "Google", "Meta", "Microsoft", "Bloomberg"],
            "hints": [
                "Sort the intervals by their start time intervals[i][0] in ascending order.",
                "Iterate through sorted intervals: maintain the current merged interval.",
                "If the next interval's start <= current merged end, extend current end = max(current end, next end); otherwise append next interval as new merged entry."
            ],
            "leetcode_examples": [
                {"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]", "explanation": "Since intervals [1,3] and [2,6] overlap, merge them into [1,6]."},
                {"input": "intervals = [[1,4],[4,5]]", "output": "[[1,5]]", "explanation": "Intervals [1,4] and [4,5] are considered overlapping."}
            ]
        },

        "number_of_islands": {
            "number": 200,
            "topics": ["Array", "Depth-First Search", "Breadth-First Search", "Union Find", "Matrix"],
            "companies": ["Amazon", "Google", "Microsoft", "Meta", "Bloomberg"],
            "hints": [
                "Treat the 2D grid as an undirected graph where adjacent '1' cells share an edge.",
                "Iterate through all grid cells (r, c). When you encounter a '1', increment the island count.",
                "Launch a DFS or BFS from (r, c) to visit and sink all connected land cells by changing '1' to '0'."
            ],
            "leetcode_examples": [
                {"input": "grid = [[\"1\",\"1\",\"1\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"0\",\"0\"]", "output": "1", "explanation": "1 large island."},
                {"input": "grid = [[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"1\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"1\",\"1\"]", "output": "3", "explanation": "3 distinct islands."}
            ]
        },

        "top_k_frequent": {
            "number": 347,
            "topics": ["Array", "Hash Table", "Divide and Conquer", "Sorting", "Heap", "Bucket Sort"],
            "companies": ["Amazon", "Meta", "Google", "Microsoft", "Apple"],
            "hints": [
                "Build a hash map / frequency counter of each unique element.",
                "Use a min-heap of size k to retain only the k most frequent elements in O(n log k) time.",
                "Alternatively, use Bucket Sort where the index represents frequency to achieve optimal O(n) linear time."
            ],
            "leetcode_examples": [
                {"input": "nums = [1,1,1,2,2,3], k = 2", "output": "[1,2]", "explanation": "1 appears 3 times, 2 appears 2 times."},
                {"input": "nums = [1], k = 1", "output": "[1]", "explanation": "Only element."}
            ]
        },

        # ============================== HARD (5) ==============================
        "trapping_rain_water": {
            "number": 42,
            "topics": ["Array", "Two Pointers", "Dynamic Programming", "Stack", "Monotonic Stack"],
            "companies": ["Amazon", "Google", "Meta", "Microsoft", "Goldman Sachs"],
            "hints": [
                "Water trapped above index i is max(0, min(max_left[i], max_right[i]) - height[i]).",
                "Two-pointer approach: left = 0, right = n - 1, left_max = 0, right_max = 0.",
                "If height[left] < height[right]: update left_max and add left_max - height[left] to water, left++; else update right_max and add right_max - height[right], right--."
            ],
            "leetcode_examples": [
                {"input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6", "explanation": "6 units of rain water are being trapped."},
                {"input": "height = [4,2,0,3,2,5]", "output": "9", "explanation": "9 units of rain water trapped."}
            ]
        },

        "minimum_window_substring": {
            "number": 76,
            "topics": ["Hash Table", "String", "Sliding Window"],
            "companies": ["Meta", "Amazon", "Google", "Microsoft", "LinkedIn"],
            "hints": [
                "Use a two-pointer sliding window [left, right] along with character count hash maps.",
                "Expand the right pointer until the current window contains all characters of t with the required frequencies.",
                "Once valid, contract the left pointer as much as possible while maintaining validity to find the minimum length window."
            ],
            "leetcode_examples": [
                {"input": "s = \"ADOBECODEBANC\", t = \"ABC\"", "output": "\"BANC\"", "explanation": "The minimum window substring \"BANC\" includes 'A', 'B', and 'C' from string t."},
                {"input": "s = \"a\", t = \"a\"", "output": "\"a\"", "explanation": "The entire string s is the minimum window."}
            ]
        },

        "merge_k_sorted_lists": {
            "number": 23,
            "topics": ["Linked List", "Divide and Conquer", "Heap (Priority Queue)", "Merge Sort"],
            "companies": ["Amazon", "Meta", "Google", "Microsoft", "Apple", "Uber"],
            "hints": [
                "You have k sorted linked lists. At each step, the next smallest node is the minimum among the heads of all active lists.",
                "Use a Min-Heap (PriorityQueue) of size k storing the current head node of each list.",
                "Pop the smallest node, attach it to the result list, and if that node has a next pointer, push node.next into the heap. Total time complexity: O(N log k)."
            ],
            "leetcode_examples": [
                {"input": "lists = [[1,4,5],[1,3,4],[2,6]]", "output": "[1,1,2,3,4,4,5,6]", "explanation": "The linked-lists are merged into one sorted list."},
                {"input": "lists = []", "output": "[]", "explanation": "Empty list of lists."}
            ]
        },

        "word_ladder": {
            "number": 127,
            "topics": ["Hash Table", "String", "Breadth-First Search"],
            "companies": ["Amazon", "Google", "Meta", "LinkedIn", "Microsoft"],
            "hints": [
                "Model this as an unweighted graph where words are vertices and an edge exists if two words differ by exactly 1 character.",
                "BFS (Breadth-First Search) guarantees finding the shortest transformation path length.",
                "Store wordList in a Hash Set. For the current word, try changing each character from 'a' to 'z'. If the new word is in the set, add to queue and remove from set to mark visited."
            ],
            "leetcode_examples": [
                {"input": "beginWord = \"hit\", endWord = \"cog\", wordList = [\"hot\",\"dot\",\"dog\",\"lot\",\"log\",\"cog\"]", "output": "5", "explanation": "One shortest transformation sequence is \"hit\" -> \"hot\" -> \"dot\" -> \"dog\" -> \"cog\", which is 5 words long."},
                {"input": "beginWord = \"hit\", endWord = \"cog\", wordList = [\"hot\",\"dot\",\"dog\",\"lot\",\"log\"]", "output": "0", "explanation": "The endWord \"cog\" is not in wordList, therefore there is no valid transformation sequence."}
            ]
        },

        "median_two_sorted_arrays": {
            "number": 4,
            "topics": ["Array", "Binary Search", "Divide and Conquer"],
            "companies": ["Amazon", "Google", "Microsoft", "Meta", "Apple", "Goldman Sachs"],
            "hints": [
                "A naive merge takes O(m + n) time, but binary search partition achieves the optimal O(log(min(m, n))) time.",
                "Partition both arrays such that the left half has (m + n + 1) // 2 elements and max(left) <= min(right).",
                "Binary search for the partition index i in the smaller array: compute j = (m + n + 1) // 2 - i. Check if nums1[i-1] <= nums2[j] and nums2[j-1] <= nums1[i]."
            ],
            "leetcode_examples": [
                {"input": "nums1 = [1,3], nums2 = [2]", "output": "2.00000", "explanation": "Merged array = [1,2,3] and median is 2.0."},
                {"input": "nums1 = [1,2], nums2 = [3,4]", "output": "2.50000", "explanation": "Merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5."}
            ]
        }
    }

    def __init__(self, problems_dir: str = "problems", active_set: str = "set1"):
        self.problems_dir = os.path.abspath(problems_dir)
        self.active_set = active_set.lower()
        self.problems: Dict[str, Dict[str, Any]] = {}
        self.hidden_dirs: Dict[str, str] = {}
        self.reload_problems()

    @staticmethod
    def get_hint_penalty(difficulty: str, hint_index: int) -> int:
        """Returns the point deduction penalty for a given hint index."""
        diff = (difficulty or "Easy").strip().capitalize()
        idx = int(hint_index)
        if diff == "Easy":
            return {1: 10, 2: 15, 3: 25}.get(idx, 10)
        elif diff == "Medium":
            return {1: 20, 2: 30, 3: 50}.get(idx, 20)
        else:  # Hard
            return {1: 30, 2: 45, 3: 75}.get(idx, 30)

    def get_available_sets(self) -> List[Dict[str, Any]]:
        """Lists available problem sets."""
        set_titles = {
            "set1": "Problem Set 1 (Classic Challenges - 15 Problems)",
            "set2": "Problem Set 2 (Advanced Challenges - 15 Problems)"
        }
        sets = []
        for s in ["set1", "set2"]:
            p = os.path.join(self.problems_dir, s)
            if os.path.isdir(p):
                sets.append({
                    "id": s,
                    "name": set_titles.get(s, f"Problem Set {s.upper()}"),
                    "active": (s == self.active_set)
                })
        return sets

    def switch_set(self, set_id: str) -> bool:
        """Switches the active problem set and reloads index."""
        clean_id = (set_id or "").strip().lower()
        target_path = os.path.join(self.problems_dir, clean_id)
        if os.path.isdir(target_path):
            self.active_set = clean_id
            self.reload_problems()
            return True
        return False

    def reload_problems(self):
        """Scans the active problems directory and indexes all problems."""
        self.problems.clear()
        self.hidden_dirs.clear()

        if not os.path.exists(self.problems_dir):
            os.makedirs(self.problems_dir, exist_ok=True)
            return

        set_path = os.path.join(self.problems_dir, self.active_set)
        search_root = set_path if os.path.isdir(set_path) else self.problems_dir

        for difficulty in ["easy", "medium", "hard"]:
            diff_dir = os.path.join(search_root, difficulty)
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
        """Returns problem catalog list for dashboard."""
        solved_set = solved_set or set()
        problem_list = []
        difficulty_order = {"Easy": 1, "Medium": 2, "Hard": 3}

        for prob_id, data in self.problems.items():
            diff = data.get("difficulty", "Easy")
            is_solved = prob_id in solved_set
            meta = self.METADATA_REGISTRY.get(prob_id, {})

            problem_list.append({
                "id": prob_id,
                "title": data.get("title", prob_id),
                "number": meta.get("number"),
                "difficulty": diff,
                "difficulty_rank": difficulty_order.get(diff, 1),
                "points": data.get("points", 100),
                "time_limit": data.get("time_limit", 2.0),
                "category": data.get("category", "General"),
                "status": "Solved" if is_solved else "Not Started",
                "solved": is_solved
            })

        problem_list.sort(key=lambda p: (p["difficulty_rank"], p["title"]))
        return problem_list

    def get_problem_detail(self, problem_id: str, participant_id: Optional[str] = None, storage: Optional[Any] = None, is_admin: bool = False) -> Optional[Dict[str, Any]]:
        """Returns problem details with 3 progressive hints and unlock status."""
        clean_id = (problem_id or "").strip().lower()
        if clean_id in self.problems:
            raw = self.problems[clean_id]
        else:
            raw = next((p for p in self.problems.values() if p.get("id", "").lower() == clean_id or p.get("slug", "").lower() == clean_id or p.get("title", "").lower().replace(" ", "_") == clean_id), None)

        if not raw:
            return None

        pid = raw.get("id", clean_id)
        meta = self.METADATA_REGISTRY.get(pid, {})
        diff = raw.get("difficulty", "Easy")
        base_points = int(raw.get("points", 100))

        raw_hints = meta.get("hints") or [
            f"Think about the edge cases for {raw.get('title', 'this problem')}.",
            "Can you optimize the time complexity using a suitable data structure?",
            "Look for mathematical invariants or a two-pointer / hash-map approach."
        ]
        while len(raw_hints) < 3:
            raw_hints.append("Break down the problem into smaller subproblems and handle boundary cases.")

        unlocked_indices = set()
        if participant_id and storage:
            try:
                unlocked_indices = set(storage.get_unlocked_hints(participant_id, pid))
            except Exception:
                unlocked_indices = set()

        hints_data = []
        total_penalty = 0
        for i in range(1, 4):
            hint_txt = raw_hints[i - 1]
            pen = self.get_hint_penalty(diff, i)
            is_unlocked = (i in unlocked_indices)
            if is_unlocked:
                total_penalty += pen
            hints_data.append({
                "index": i,
                "title": f"Hint {i}",
                "penalty": pen,
                "unlocked": is_unlocked,
                "text": hint_txt if is_unlocked else None
            })

        max_score = max(int(base_points * 0.25), base_points - total_penalty)

        res = {
            "id": pid,
            "title": raw.get("title"),
            "number": meta.get("number"),
            "difficulty": diff,
            "points": base_points,
            "max_score": max_score,
            "total_hint_penalty": total_penalty,
            "time_limit": raw.get("time_limit", 2.0),
            "category": raw.get("category", "General"),
            "description": raw.get("description", ""),
            "input_format": raw.get("input_format", ""),
            "output_format": raw.get("output_format", ""),
            "constraints": raw.get("constraints", ""),
            "topics": meta.get("topics") or [raw.get("category", "Algorithms")],
            "companies": meta.get("companies") or ["Amazon", "Google", "Microsoft", "Meta"],
            "hints": hints_data,
            "leetcode_examples": meta.get("leetcode_examples"),
            "sample_tests": raw.get("sample_tests", []),
            "starter_code": Harness.get_starter_code(pid) if Harness else raw.get("starter_code", {})
        }
        if is_admin:
            res["solutions"] = get_all_solutions_for_problem(pid)
        return res

    def get_solutions_for_problem(self, problem_id: str) -> Dict[str, str]:
        """Returns the dictionary of solutions for a problem."""
        clean_id = (problem_id or "").strip().lower()
        raw = self.problems.get(clean_id) or next((p for p in self.problems.values() if p.get("id", "").lower() == clean_id or p.get("slug", "").lower() == clean_id), None)
        pid = raw.get("id", clean_id) if raw else clean_id
        return get_all_solutions_for_problem(pid)

    def get_hint_text(self, problem_id: str, hint_index: int) -> Optional[str]:
        """Returns the specific raw hint string (1-indexed)."""
        clean_id = (problem_id or "").strip().lower()
        raw = self.problems.get(clean_id) or next((p for p in self.problems.values() if p.get("id", "").lower() == clean_id or p.get("slug", "").lower() == clean_id), None)
        if not raw:
            return None
        pid = raw.get("id", clean_id)
        meta = self.METADATA_REGISTRY.get(pid, {})
        hints = meta.get("hints") or [
            f"Think about the edge cases for {raw.get('title', 'this problem')}.",
            "Can you optimize the time complexity using a suitable data structure?",
            "Look for mathematical invariants or a two-pointer / hash-map approach."
        ]
        while len(hints) < 3:
            hints.append("Break down the problem into smaller subproblems and handle boundary cases.")
        if 1 <= hint_index <= len(hints):
            return hints[hint_index - 1]
        return None

    def get_hidden_tests_dir(self, problem_id: str) -> Optional[str]:
        """Locates the server-side hidden test directory."""
        clean_id = (problem_id or "").strip().lower()
        if clean_id in self.hidden_dirs:
            return self.hidden_dirs[clean_id]
        raw = next((p for p in self.problems.values() if p.get("id", "").lower() == clean_id or p.get("slug", "").lower() == clean_id), None)
        if raw and raw.get("id") in self.hidden_dirs:
            return self.hidden_dirs[raw["id"]]
        return None
