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

    def __init__(self, problems_dir: str, active_set: str = "set1"):
        self.problems_dir = problems_dir
        self.active_set = active_set
        self.problems: Dict[str, Dict[str, Any]] = {}
        self.hidden_dirs: Dict[str, str] = {}
        self.reload_problems()

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

        # Determine target base directory (set1/set2 subfolder or root fallback)
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

    METADATA_REGISTRY = {
        "two_sum": {
            "number": 1,
            "topics": ["Array", "Hash Table"],
            "companies": ["Amazon", "Google", "Meta", "Microsoft", "Apple", "Bloomberg"],
            "hints": [
                "A really brute force way would be to search for all possible pairs of numbers but that would be too slow.",
                "So, if we fix one of the numbers, say x, we have to scan the entire array to find the next number y which is value - x. Can we change our array somehow so that this search becomes faster?",
                "The second train of thought is, without changing the array, can we use additional space like a hash map to look up if the complement already exists?"
            ],
            "leetcode_examples": [
                {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."},
                {"input": "nums = [3,2,4], target = 6", "output": "[1,2]", "explanation": "Because nums[1] + nums[2] == 6, we return [1, 2]."},
                {"input": "nums = [3,3], target = 6", "output": "[0,1]", "explanation": "Because nums[0] + nums[1] == 6, we return [0, 1]."}
            ]
        },
        "palindrome_number": {
            "number": 9,
            "topics": ["Math", "Two Pointers"],
            "companies": ["Amazon", "Microsoft", "Adobe", "Apple"],
            "hints": [
                "Beware of negative numbers! For example, -121 is not a palindrome because from left to right it reads -121, but right to left it reads 121-.",
                "Could you solve it without converting the integer to a string?",
                "Revert half of the number and compare it to the first half."
            ],
            "leetcode_examples": [
                {"input": "x = 121", "output": "true", "explanation": "121 reads as 121 from left to right and from right to left."},
                {"input": "x = -121", "output": "false", "explanation": "From left to right, it reads -121. From right to left, it becomes 121-."},
                {"input": "x = 10", "output": "false", "explanation": "Reads 01 from right to left. Therefore it is not a palindrome."}
            ]
        },
        "reverse_string": {
            "number": 344,
            "topics": ["Two Pointers", "String"],
            "companies": ["Amazon", "Google", "Apple", "Microsoft"],
            "hints": [
                "The entire logic can be performed with two pointers moving towards the center, swapping elements at each step.",
                "Ensure O(1) extra memory."
            ],
            "leetcode_examples": [
                {"input": "s = [\"h\",\"e\",\"l\",\"l\",\"o\"]", "output": "[\"o\",\"l\",\"l\",\"e\",\"h\"]", "explanation": "Reverses the array of characters."},
                {"input": "s = [\"H\",\"a\",\"n\",\"n\",\"a\",\"h\"]", "output": "[\"h\",\"a\",\"n\",\"n\",\"a\",\"H\"]", "explanation": "Reverses the characters in place."}
            ]
        },
        "count_vowels": {
            "number": 1456,
            "topics": ["String", "Hash Table", "Sliding Window"],
            "companies": ["Microsoft", "Adobe", "Amazon"],
            "hints": [
                "Iterate through the string and check if each character belongs to the set {'a', 'e', 'i', 'o', 'u'} (case-insensitive)."
            ],
            "leetcode_examples": [
                {"input": "s = \"abciiidef\", k = 3", "output": "3", "explanation": "Substring \"iii\" contains 3 vowel letters."},
                {"input": "s = \"aeiou\"", "output": "5", "explanation": "All characters are vowels."}
            ]
        },
        "find_maximum": {
            "number": 414,
            "topics": ["Array", "Sorting"],
            "companies": ["Amazon", "Oracle", "Microsoft"],
            "hints": [
                "Maintain the running maximum as you scan through the array elements in a single linear pass."
            ],
            "leetcode_examples": [
                {"input": "nums = [3,2,1,5,6,4]", "output": "6", "explanation": "6 is the largest element in the array."},
                {"input": "nums = [1,2]", "output": "2", "explanation": "2 is the maximum value."}
            ]
        },
        "maximum_subarray": {
            "number": 53,
            "topics": ["Array", "Divide and Conquer", "Dynamic Programming"],
            "companies": ["Amazon", "Apple", "Microsoft", "LinkedIn", "Google", "Meta"],
            "hints": [
                "Kadane's Algorithm: at each index, the max subarray ending at that index is max(nums[i], current_max + nums[i])."
            ],
            "leetcode_examples": [
                {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "The subarray [4,-1,2,1] has the largest sum 6."},
                {"input": "nums = [1]", "output": "1", "explanation": "The subarray [1] has the largest sum 1."},
                {"input": "nums = [5,4,-1,7,8]", "output": "23", "explanation": "The subarray [5,4,-1,7,8] has the largest sum 23."}
            ]
        },
        "longest_common_prefix": {
            "number": 14,
            "topics": ["String", "Trie"],
            "companies": ["Amazon", "Google", "Meta", "Adobe", "Apple"],
            "hints": [
                "Compare characters vertically across all strings at the same index.",
                "Stop at the first character mismatch or when the shortest string length is exceeded."
            ],
            "leetcode_examples": [
                {"input": "strs = [\"flower\",\"flow\",\"flight\"]", "output": "\"fl\"", "explanation": "Common prefix is \"fl\"."},
                {"input": "strs = [\"dog\",\"racecar\",\"car\"]", "output": "\"\"", "explanation": "There is no common prefix among the input strings."}
            ]
        },
        "valid_anagram": {
            "number": 242,
            "topics": ["Hash Table", "String", "Sorting"],
            "companies": ["Google", "Amazon", "Bloomberg", "Uber"],
            "hints": [
                "An anagram contains the exact same frequency of each character.",
                "Count frequencies with a fixed-size array of 26 integers or a hash map."
            ],
            "leetcode_examples": [
                {"input": "s = \"anagram\", t = \"nagaram\"", "output": "true", "explanation": "Both strings contain the same character counts."},
                {"input": "s = \"rat\", t = \"car\"", "output": "false", "explanation": "'r','a','t' cannot form 'c','a','r'."}
            ]
        },
        "binary_search": {
            "number": 704,
            "topics": ["Array", "Binary Search"],
            "companies": ["Google", "Meta", "Apple", "Microsoft", "Amazon"],
            "hints": [
                "Set low = 0 and high = nums.length - 1.",
                "Compute mid = low + (high - low) / 2 and narrow the search range."
            ],
            "leetcode_examples": [
                {"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4", "explanation": "9 exists in nums and its index is 4."},
                {"input": "nums = [-1,0,3,5,9,12], target = 2", "output": "-1", "explanation": "2 does not exist in nums so return -1."}
            ]
        },
        "merge_intervals": {
            "number": 56,
            "topics": ["Array", "Sorting"],
            "companies": ["Meta", "Amazon", "Google", "Microsoft", "Bloomberg"],
            "hints": [
                "Sort intervals based on their start times.",
                "Iterate through sorted intervals: if current start <= previous end, merge by updating previous end = max(prev.end, curr.end)."
            ],
            "leetcode_examples": [
                {"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]", "explanation": "Since intervals [1,3] and [2,6] overlap, merge them into [1,6]."},
                {"input": "intervals = [[1,4],[4,5]]", "output": "[[1,5]]", "explanation": "Intervals [1,4] and [4,5] are considered overlapping."}
            ]
        },
        "trapping_rain_water": {
            "number": 42,
            "topics": ["Array", "Two Pointers", "Dynamic Programming", "Stack", "Monotonic Stack"],
            "companies": ["Amazon", "Google", "Meta", "Goldman Sachs", "Microsoft", "Apple"],
            "hints": [
                "At each position i, trapped water = max(0, min(max_left, max_right) - height[i]).",
                "Optimize to O(1) auxiliary space using two pointers moving inwards."
            ],
            "leetcode_examples": [
                {"input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6", "explanation": "6 units of rain water are being trapped."},
                {"input": "height = [4,2,0,3,2,5]", "output": "9", "explanation": "9 units of rain water trapped between bars."}
            ]
        },
        "longest_palindromic_substring": {
            "number": 5,
            "topics": ["Two Pointers", "String", "Dynamic Programming"],
            "companies": ["Amazon", "Microsoft", "Adobe", "Meta", "Apple"],
            "hints": [
                "A palindrome mirrors around its center.",
                "There are 2N - 1 possible centers. Expand outward for each center."
            ],
            "leetcode_examples": [
                {"input": "s = \"babad\"", "output": "\"bab\"", "explanation": "\"aba\" is also a valid answer."},
                {"input": "s = \"cbbd\"", "output": "\"bb\"", "explanation": "The longest palindromic substring is \"bb\"."}
            ]
        },
        "median_two_sorted_arrays": {
            "number": 4,
            "topics": ["Array", "Binary Search", "Divide and Conquer"],
            "companies": ["Google", "Amazon", "Microsoft", "Apple", "Meta"],
            "hints": [
                "Perform binary search on the partition index of the smaller array.",
                "Ensure left partition size equals right partition size (or +1 for odd total length)."
            ],
            "leetcode_examples": [
                {"input": "nums1 = [1,3], nums2 = [2]", "output": "2.00000", "explanation": "merged array = [1,2,3] and median is 2."},
                {"input": "nums1 = [1,2], nums2 = [3,4]", "output": "2.50000", "explanation": "merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5."}
            ]
        },
        "binary_tree": {
            "number": 102,
            "topics": ["Tree", "Depth-First Search", "Breadth-First Search", "Binary Tree"],
            "companies": ["Amazon", "Meta", "Microsoft", "Google", "LinkedIn"],
            "hints": [
                "Use Breadth-First Search (BFS) with a queue to traverse level-by-level."
            ],
            "leetcode_examples": [
                {"input": "root = [3,9,20,null,null,15,7]", "output": "[[3],[9,20],[15,7]]", "explanation": "Nodes traversed level by level."},
                {"input": "root = [1]", "output": "[[1]]", "explanation": "Single node tree."}
            ]
        },
        "lru_cache": {
            "number": 146,
            "topics": ["Hash Table", "Linked List", "Design", "Doubly-Linked List"],
            "companies": ["Amazon", "Google", "Meta", "Microsoft", "Apple", "Bloomberg"],
            "hints": [
                "Combine a hash map for O(1) key-to-node lookup with a Doubly Linked List for O(1) node insertion/removal.",
                "Move accessed nodes to the head, and evict from the tail when capacity is reached."
            ],
            "leetcode_examples": [
                {"input": "[\"LRUCache\",\"put\",\"put\",\"get\",\"put\",\"get\",\"put\",\"get\",\"get\",\"get\"]\n[[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]", "output": "[null,null,null,1,null,-1,null,-1,3,4]", "explanation": "LRUCache initialized with capacity 2. Key 2 is evicted when 3 is inserted."}
            ]
        },
        "valid_parentheses": {
            "number": 20,
            "topics": ["String", "Stack"],
            "companies": ["Amazon", "Google", "Meta", "Microsoft", "Apple", "Bloomberg"],
            "hints": [
                "Use a stack of characters.",
                "When encountering an opening bracket, push it. When encountering a closing bracket, verify it matches the top of stack and pop."
            ],
            "leetcode_examples": [
                {"input": "s = \"()\"", "output": "true", "explanation": "Matching parentheses."},
                {"input": "s = \"()[]{}\"", "output": "true", "explanation": "All pairs properly opened and closed."},
                {"input": "s = \"(]\"", "output": "false", "explanation": "Mismatched bracket types."}
            ]
        },
        "reverse_words": {
            "number": 151,
            "topics": ["Two Pointers", "String"],
            "companies": ["Microsoft", "Amazon", "Apple", "Google"],
            "hints": [
                "Trim leading and trailing whitespace and reduce consecutive spaces to a single space.",
                "Reverse the order of words."
            ],
            "leetcode_examples": [
                {"input": "s = \"the sky is blue\"", "output": "\"blue is sky the\"", "explanation": "Reverses words order."},
                {"input": "s = \"  hello world  \"", "output": "\"world hello\"", "explanation": "Reversed string should not contain leading or trailing spaces."}
            ]
        },
        "single_number": {
            "number": 136,
            "topics": ["Array", "Bit Manipulation"],
            "companies": ["Amazon", "Google", "Apple"],
            "hints": [
                "Recall XOR bitwise properties: A ^ A = 0 and A ^ 0 = A.",
                "XOR all numbers in the array; duplicates cancel out leaving the unique number."
            ],
            "leetcode_examples": [
                {"input": "nums = [2,2,1]", "output": "1", "explanation": "1 appears only once."},
                {"input": "nums = [4,1,2,1,2]", "output": "4", "explanation": "4 appears only once."}
            ]
        },
        "climbing_stairs": {
            "number": 70,
            "topics": ["Math", "Dynamic Programming", "Memoization"],
            "companies": ["Amazon", "Google", "Adobe", "Apple"],
            "hints": [
                "To reach the n-th step, you could take 1 step from step n-1, or 2 steps from step n-2.",
                "dp[n] = dp[n-1] + dp[n-2]."
            ],
            "leetcode_examples": [
                {"input": "n = 2", "output": "2", "explanation": "There are two ways to climb to the top: 1 step + 1 step, or 2 steps."},
                {"input": "n = 3", "output": "3", "explanation": "There are three ways: (1+1+1), (1+2), (2+1)."}
            ]
        },
        "majority_element": {
            "number": 169,
            "topics": ["Array", "Hash Table", "Divide and Conquer", "Counting", "Boyer-Moore Voting"],
            "companies": ["Amazon", "Meta", "Microsoft", "Google"],
            "hints": [
                "Can you solve it in linear time and in O(1) space?",
                "Boyer-Moore Voting Algorithm: maintain a candidate and a count."
            ],
            "leetcode_examples": [
                {"input": "nums = [3,2,3]", "output": "3", "explanation": "3 appears more than n/2 times."},
                {"input": "nums = [2,2,1,1,1,2,2]", "output": "2", "explanation": "2 appears 4 times in an array of length 7."}
            ]
        },
        "longest_substring": {
            "number": 3,
            "topics": ["Hash Table", "String", "Sliding Window"],
            "companies": ["Amazon", "Google", "Bloomberg", "Meta", "Microsoft"],
            "hints": [
                "Use a sliding window with two pointers [left, right] and a hash map of last seen indices."
            ],
            "leetcode_examples": [
                {"input": "s = \"abcabcbb\"", "output": "3", "explanation": "The answer is \"abc\", with the length of 3."},
                {"input": "s = \"bbbbb\"", "output": "1", "explanation": "The answer is \"b\", with the length of 1."},
                {"input": "s = \"pwwkew\"", "output": "3", "explanation": "The answer is \"wke\", with the length of 3."}
            ]
        },
        "container_with_most_water": {
            "number": 11,
            "topics": ["Array", "Two Pointers", "Greedy"],
            "companies": ["Amazon", "Google", "Meta", "Adobe", "Apple"],
            "hints": [
                "Area = min(height[left], height[right]) * (right - left).",
                "Always move the pointer pointing to the shorter line inward."
            ],
            "leetcode_examples": [
                {"input": "height = [1,8,6,2,5,4,8,3,7]", "output": "49", "explanation": "The max area of water the container can contain is 49."},
                {"input": "height = [1,1]", "output": "1", "explanation": "Max area is 1 * 1 = 1."}
            ]
        },
        "coin_change": {
            "number": 322,
            "topics": ["Array", "Dynamic Programming", "Breadth-First Search"],
            "companies": ["Amazon", "Microsoft", "Google", "Bloomberg", "Meta"],
            "hints": [
                "dp[i] is the minimum coins needed to make amount i.",
                "dp[i] = min(dp[i], dp[i - coin] + 1) for each coin <= i."
            ],
            "leetcode_examples": [
                {"input": "coins = [1,2,5], amount = 11", "output": "3", "explanation": "11 = 5 + 5 + 1."},
                {"input": "coins = [2], amount = 3", "output": "-1", "explanation": "Cannot make amount 3 with only 2-cent coins."}
            ]
        },
        "rotate_matrix": {
            "number": 48,
            "topics": ["Array", "Math", "Matrix"],
            "companies": ["Amazon", "Microsoft", "Apple", "Google"],
            "hints": [
                "To rotate 90 degrees clockwise in-place: Transpose matrix (swap matrix[i][j] and matrix[j][i]), then reverse each row."
            ],
            "leetcode_examples": [
                {"input": "matrix = [[1,2,3],[4,5,6],[7,8,9]]", "output": "[[7,4,1],[8,5,2],[9,6,3]]", "explanation": "Matrix rotated 90 degrees clockwise."},
                {"input": "matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]", "output": "[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]", "explanation": "Rotated 4x4 matrix."}
            ]
        },
        "group_anagrams": {
            "number": 49,
            "topics": ["Array", "Hash Table", "String", "Sorting"],
            "companies": ["Amazon", "Google", "Uber", "Apple", "Meta", "Bloomberg"],
            "hints": [
                "Two strings are anagrams if and only if their sorted strings are equal, or character frequency tuples match."
            ],
            "leetcode_examples": [
                {"input": "strs = [\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]", "output": "[[\"bat\"],[\"nat\",\"tan\"],[\"ate\",\"eat\",\"tea\"]]", "explanation": "Grouped words that are anagrams of each other."},
                {"input": "strs = [\"\"]", "output": "[[\"\"]]", "explanation": "Single empty string."}
            ]
        },
        "merge_k_sorted_lists": {
            "number": 23,
            "topics": ["Linked List", "Divide and Conquer", "Heap (Priority Queue)", "Merge Sort"],
            "companies": ["Meta", "Amazon", "Google", "Microsoft", "Apple", "ByteDance"],
            "hints": [
                "Use a min-heap / PriorityQueue of size k to always extract the smallest element.",
                "Alternatively, merge pairs of lists divide-and-conquer style in O(N log k) time."
            ],
            "leetcode_examples": [
                {"input": "lists = [[1,4,5],[1,3,4],[2,6]]", "output": "[1,1,2,3,4,4,5,6]", "explanation": "Merged into one sorted list."},
                {"input": "lists = []", "output": "[]", "explanation": "Empty input."}
            ]
        },
        "longest_valid_parentheses": {
            "number": 32,
            "topics": ["String", "Dynamic Programming", "Stack"],
            "companies": ["Google", "Amazon", "Meta", "Microsoft"],
            "hints": [
                "Push index onto stack. Initialize stack with -1.",
                "When encountering ')', pop from stack. If stack is empty, push current index. Otherwise, max_len = max(max_len, current_index - stack.top())."
            ],
            "leetcode_examples": [
                {"input": "s = \"(()\"", "output": "2", "explanation": "The longest valid parentheses substring is \"()\"."},
                {"input": "s = \")()())\"", "output": "4", "explanation": "The longest valid parentheses substring is \"()()\"."}
            ]
        },
        "word_break": {
            "number": 139,
            "topics": ["Hash Table", "String", "Dynamic Programming", "Trie", "Memoization"],
            "companies": ["Amazon", "Google", "Meta", "Bloomberg", "Apple"],
            "hints": [
                "dp[i] is true if s[0...i] can be segmented into dictionary words.",
                "dp[i] = any(dp[j] and s[j...i] in wordDict for j in 0...i)."
            ],
            "leetcode_examples": [
                {"input": "s = \"leetcode\", wordDict = [\"leet\",\"code\"]", "output": "true", "explanation": "Return true because \"leetcode\" can be segmented as \"leet code\"."},
                {"input": "s = \"applepenapple\", wordDict = [\"apple\",\"pen\"]", "output": "true", "explanation": "Return true because \"applepenapple\" can be segmented as \"apple pen apple\"."}
            ]
        }
    }

    def get_problem_detail(self, problem_id: str) -> Optional[Dict[str, Any]]:
        """
        Returns sanitized problem details including visible sample tests and starter codes.
        NEVER returns hidden tests.
        """
        clean_id = (problem_id or "").strip().lower()
        if clean_id in self.problems:
            raw = self.problems[clean_id]
        else:
            raw = next((p for p in self.problems.values() if p.get("id", "").lower() == clean_id or p.get("slug", "").lower() == clean_id or p.get("title", "").lower().replace(" ", "_") == clean_id), None)

        if not raw:
            return None

        pid = raw.get("id", clean_id)
        meta = self.METADATA_REGISTRY.get(pid, {})

        # Default fallbacks
        topics = meta.get("topics") or ([raw.get("category")] if raw.get("category") else ["Algorithms", "Problem Solving"])
        companies = meta.get("companies") or ["Amazon", "Google", "Microsoft", "Meta"]
        hints = meta.get("hints") or [
            f"Think about the edge cases for {raw.get('title', 'this problem')}.",
            "Can you optimize the time complexity using a suitable data structure?"
        ]
        leetcode_examples = meta.get("leetcode_examples")

        return {
            "id": pid,
            "title": raw.get("title"),
            "number": meta.get("number"),
            "difficulty": raw.get("difficulty"),
            "points": raw.get("points"),
            "time_limit": raw.get("time_limit", 2.0),
            "category": raw.get("category", "General"),
            "description": raw.get("description", ""),
            "input_format": raw.get("input_format", ""),
            "output_format": raw.get("output_format", ""),
            "constraints": raw.get("constraints", ""),
            "topics": topics,
            "companies": companies,
            "hints": hints,
            "leetcode_examples": leetcode_examples,
            "sample_tests": raw.get("sample_tests", []),
            "starter_code": raw.get("starter_code", {})
        }

    def get_hidden_tests_dir(self, problem_id: str) -> Optional[str]:
        """Internal judge accessor to locate the server-side hidden test directory."""
        clean_id = (problem_id or "").strip().lower()
        if clean_id in self.hidden_dirs:
            return self.hidden_dirs[clean_id]
        raw = next((p for p in self.problems.values() if p.get("id", "").lower() == clean_id or p.get("slug", "").lower() == clean_id), None)
        if raw and raw.get("id") in self.hidden_dirs:
            return self.hidden_dirs[raw["id"]]
        return None

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
