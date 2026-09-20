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


class ProblemsManager:
    """Manages problem metadata, starter templates, visible samples, hints, and hidden test suites."""

    METADATA_REGISTRY = {
        # Set 1 (Classic Challenges)
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
        "palindrome_number": {
            "number": 9,
            "topics": ["Math", "Two Pointers"],
            "companies": ["Amazon", "Microsoft", "Adobe", "Apple"],
            "hints": [
                "Negative numbers cannot be palindromes: -121 reversed is 121-, which does not match -121.",
                "Numbers ending in 0 (except 0 itself) cannot be palindromes since leading digits cannot be 0.",
                "Revert half of the number mathematically: while x > reversed_num, reversed_num = reversed_num * 10 + x % 10; x //= 10. Then check x == reversed_num or x == reversed_num // 10."
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
                "The problem requires reversing the characters with O(1) extra memory in-place.",
                "Set two pointers: left at index 0 and right at index len(s) - 1.",
                "While left < right, swap s[left] and s[right], then advance left++ and decrement right--."
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
                "Vowels are 'a', 'e', 'i', 'o', 'u' (both lowercase and uppercase).",
                "Iterate character by character, converting each character to lowercase.",
                "Check if char is in {'a', 'e', 'i', 'o', 'u'} and maintain a running counter."
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
                "You need to find the largest value in an array of numbers in linear O(n) time.",
                "Initialize max_val with the first element nums[0].",
                "Iterate through the array: if nums[i] > max_val, update max_val = nums[i]. Return max_val."
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
                "Consider Kadane's Algorithm: at each position, decide whether to add nums[i] to the running subarray sum or start fresh at nums[i].",
                "Recurrence: current_max = max(nums[i], current_max + nums[i]).",
                "Maintain global max_so_far = max(max_so_far, current_max) across the loop and return it."
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
                "If the array is empty, return \"\".",
                "Scan vertically: compare characters of all strings at index 0, index 1, index 2...",
                "Use the first string as a template. If any string is shorter than i or has a mismatch at i, return first_str[0...i]."
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
                "Two strings are anagrams if and only if they have the exact same length and character frequency.",
                "You can sort both strings in O(n log n) or use a 26-element array / hash map in O(n) time.",
                "Increment counts for string s, decrement for string t. If all counts are 0, return true; else false."
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
                "The array is sorted in ascending order. You can divide the search interval in half each step.",
                "Initialize low = 0 and high = len(nums) - 1. Compute mid = low + (high - low) // 2.",
                "If nums[mid] == target, return mid. If nums[mid] < target, set low = mid + 1; else high = mid - 1. If low > high, return -1."
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
                "Sort the intervals based on their start values (interval[0]).",
                "Maintain a list of merged intervals. Initialize it with the first sorted interval.",
                "For each subsequent interval [s, e]: if s <= merged[-1][1], update merged[-1][1] = max(merged[-1][1], e); otherwise append [s, e]."
            ],
            "leetcode_examples": [
                {"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]", "explanation": "Since intervals [1,3] and [2,6] overlap, merge them into [1,6]."},
                {"input": "intervals = [[1,4],[4,5]]", "output": "[[1,5]]", "explanation": "Intervals [1,4] and [4,5] are considered overlapping."}
            ]
        },
        "trapping_rain_water": {
            "number": 42,
            "topics": ["Array", "Two Pointers", "Dynamic Programming", "Stack"],
            "companies": ["Amazon", "Google", "Meta", "Goldman Sachs", "Microsoft", "Apple"],
            "hints": [
                "The amount of water trapped at index i is max(0, min(max_left, max_right) - height[i]).",
                "You can precompute prefix max and suffix max in O(n) space, or use two pointers in O(1) space.",
                "Two Pointers: Maintain left = 0, right = n - 1, left_max, right_max. Move the pointer pointing to the smaller max inward and accumulate trapped water."
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
                "A palindrome expands symmetrically around its center. There are 2n - 1 possible centers.",
                "For each index i, expand around center (i, i) for odd-length palindromes, and (i, i + 1) for even-length palindromes.",
                "Expand while left >= 0 and right < len(s) and s[left] == s[right]. Track the longest substring found."
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
                "To achieve O(log(min(m, n))) time, partition the smaller array using binary search.",
                "Partition array A at i and array B at j such that i + j = (m + n + 1) // 2.",
                "Binary search i in [0, m] until A[i-1] <= B[j] and B[j-1] <= A[i]. If total length is odd, median = max(lefts); if even, median = (max(lefts) + min(rights)) / 2."
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
                "To find depth or level order traversal, represent tree nodes with left and right child pointers.",
                "For maximum depth: depth(root) = 1 + max(depth(root.left), depth(root.right)) with depth(null) = 0.",
                "For level order: use a FIFO queue (BFS). At each level, process len(queue) nodes and enqueue their non-null children."
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
                "You need O(1) get and put operations with eviction of the least recently used item.",
                "Combine a Hash Map for O(1) key-to-node lookup with a Doubly Linked List for O(1) node insertion/removal.",
                "When a node is accessed, move it to the head (most recent). When capacity is exceeded, evict the node at the tail (least recent)."
            ],
            "leetcode_examples": [
                {"input": "[\"LRUCache\",\"put\",\"put\",\"get\",\"put\",\"get\",\"put\",\"get\",\"get\",\"get\"]\n[[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]", "output": "[null,null,null,1,null,-1,null,-1,3,4]", "explanation": "LRUCache initialized with capacity 2. Key 2 is evicted when 3 is inserted."}
            ]
        },

        # Set 2 (Advanced Challenges)
        "valid_parentheses": {
            "number": 20,
            "topics": ["String", "Stack"],
            "companies": ["Amazon", "Google", "Meta", "Microsoft", "Apple", "Bloomberg"],
            "hints": [
                "Use a Stack (LIFO) to keep track of expected closing brackets.",
                "When you see an opening bracket '(', '{', '[', push it onto the stack.",
                "When you see a closing bracket, check if the stack is non-empty and top matches. If yes, pop; else invalid. At the end, stack must be empty."
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
                "Split the string by whitespace to extract individual words.",
                "Filter out empty tokens caused by multiple consecutive spaces.",
                "Reverse the array of words and join them with a single space separator."
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
                "You need O(n) time and O(1) space without extra memory.",
                "Recall XOR bitwise properties: x ^ x = 0 and x ^ 0 = x.",
                "XOR all numbers in the array. All duplicate elements cancel out to 0, leaving only the unique single number!"
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
                "To reach step n, you can take 1 step from step n-1, or 2 steps from step n-2.",
                "This gives recurrence: ways(n) = ways(n-1) + ways(n-2) with base cases ways(1) = 1, ways(2) = 2.",
                "This is the Fibonacci sequence! Compute iteratively in O(n) time and O(1) space with two variables."
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
                "The majority element is guaranteed to appear more than n // 2 times.",
                "Boyer-Moore Voting Algorithm achieves O(n) time and O(1) space.",
                "Maintain candidate and count. For each num: if count == 0, candidate = num. If num == candidate, count++ else count--. Return candidate."
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
        "container_with_most_water": {
            "number": 11,
            "topics": ["Array", "Two Pointers", "Greedy"],
            "companies": ["Amazon", "Google", "Meta", "Adobe", "Apple"],
            "hints": [
                "Area is (right - left) * min(height[left], height[right]).",
                "Start with two pointers at the maximum width: left = 0 and right = n - 1.",
                "Calculate area at each step. To find a potentially taller container, move the pointer pointing to the shorter line inward."
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
                "Let dp[i] be the minimum coins needed to make amount i.",
                "Initialize dp array of size amount + 1 with infinity, and dp[0] = 0.",
                "For each i from 1 to amount: for each coin in coins: if coin <= i, dp[i] = min(dp[i], dp[i - coin] + 1). If dp[amount] is infinity, return -1."
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
                "Rotating 90 degrees clockwise in-place can be done by combining two simple operations.",
                "Step 1: Transpose the matrix (swap matrix[i][j] with matrix[j][i]).",
                "Step 2: Reverse each row horizontally (swap matrix[i][j] with matrix[i][n - 1 - j])."
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
                "Strings that are anagrams share the same sorted string representation.",
                "Use a Hash Map: map sorted_word -> list of original words.",
                "For each word in strs, key = ''.join(sorted(word)), map[key].append(word). Return list(map.values())."
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
                "Merging k lists one-by-one is slow. We can maintain a Min-Heap of size k.",
                "Insert the head value of each of the k lists into the min-heap.",
                "Pop the smallest element to append to output, and push the next element from that list into the heap in O(log k) time."
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
                "Use a Stack storing indices of characters. Initialize stack with -1 as base index.",
                "When s[i] == '(', push i onto stack.",
                "When s[i] == ')', pop top. If stack is empty, push i as new base; else max_len = max(max_len, i - stack[-1])."
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
                "Let dp[i] be true if s[0...i] can be segmented into words from wordDict.",
                "Initialize boolean dp array of size len(s) + 1 with dp[0] = true.",
                "For each i from 1 to len(s): for j in range(0, i): if dp[j] and s[j:i] in wordDict: dp[i] = True; break. Return dp[len(s)]."
            ],
            "leetcode_examples": [
                {"input": "s = \"leetcode\", wordDict = [\"leet\",\"code\"]", "output": "true", "explanation": "Return true because \"leetcode\" can be segmented as \"leet code\"."},
                {"input": "s = \"applepenapple\", wordDict = [\"apple\",\"pen\"]", "output": "true", "explanation": "Return true because \"applepenapple\" can be segmented as \"apple pen apple\"."}
            ]
        }
    }

    def __init__(self, problems_dir: str, active_set: str = "set1"):
        self.problems_dir = problems_dir
        self.active_set = active_set
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

    def get_problem_detail(self, problem_id: str, participant_id: Optional[str] = None, storage: Optional[Any] = None) -> Optional[Dict[str, Any]]:
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

        return {
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