"""
CODE COMBAT Pro - LeetCode Driver Harness Engine
Provides authentic LeetCode class Solution starter templates and auto-wrapping IO drivers
for Java, Python 3, and C for all 30 problems across Set 1 and Set 2.
"""

import re
from typing import Dict, Any, Optional


class Harness:
    """Manages LeetCode starter templates and compiles auto-wrapping IO harnesses."""

    STARTER_TEMPLATES = {'two_sum': {'python': "# Two Sum\n# Given an array of integers nums and an integer target,\n# return indices of the two numbers such that they add up to target.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:n+1]]\n    target = int(data[n+1])\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print space-separated indices: i j\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        # Write your code here\n        pass\n', 'java': '// Two Sum\nimport java.util.*;\n\nclass Solution {\n    public int[] twoSum(int[] nums, int target) {\n        // Write your code here\n        return new int[]{};\n    }\n}\n', 'c': '// Two Sum\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n    int nums[n];\n    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);\n    int target;\n    scanf("%d", &target);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print: i j\n    \n    return 0;\n}\n'}, 'reverse_string': {'python': "# Reverse a String\n# Reverse the given input string.\n\nimport sys\n\ndef solve():\n    s = sys.stdin.read().rstrip('\\r\\n')\n    \n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print reversed string\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def reverseString(self, s: str) -> str:\n        # Write your code here\n        pass\n', 'java': '// Reverse a String\nimport java.util.*;\n\nclass Solution {\n    public String reverseString(String s) {\n        // Write your code here\n        return "";\n    }\n}\n', 'c': "// Reverse a String\n#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char s[100005];\n    if (!fgets(s, sizeof(s), stdin)) return 0;\n    int len = strlen(s);\n    while (len > 0 && (s[len - 1] == '\\n' || s[len - 1] == '\\r')) {\n        s[--len] = '\\0';\n    }\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print reversed string\n    \n    return 0;\n}\n"}, 'find_duplicate': {'python': "# Find Duplicate in an Array\n# Find the repeated integer in an array of size n containing numbers from 1 to n-1.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:n+1]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print the duplicate number\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def findDuplicate(self, nums: List[int]) -> int:\n        # Write your code here\n        pass\n', 'java': '// Find Duplicate in an Array\nimport java.util.*;\n\nclass Solution {\n    public int findDuplicate(int[] nums) {\n        // Write your code here\n        return 0;\n    }\n}\n', 'c': '// Find Duplicate in an Array\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n    int nums[n];\n    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print duplicate number\n    \n    return 0;\n}\n'}, 'valid_parentheses': {'python': "# Valid Parentheses\n# Given a string containing '(', ')', '{', '}', '[' and ']',\n# determine if the input string is valid.\n\nimport sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print: true or false\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def isValid(self, s: str) -> bool:\n        # Write your code here\n        pass\n', 'java': '// Valid Parentheses\nimport java.util.*;\n\nclass Solution {\n    public boolean isValid(String s) {\n        // Write your code here\n        return false;\n    }\n}\n', 'c': '// Valid Parentheses\n#include <stdio.h>\n#include <stdbool.h>\n#include <string.h>\n\nint main() {\n    char s[100005];\n    if (scanf("%s", s) != 1) {\n        printf("false\\n");\n        return 0;\n    }\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print: true or false\n    \n    return 0;\n}\n'}, 'reverse_linked_list': {'python': "# Reverse Linked List\n# Given the head of a singly linked list, reverse the list, and return the reversed list.\n\nimport sys\n\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data or int(data[0]) <= 0:\n        return\n    n = int(data[0])\n    nums = [int(data[i]) for i in range(1, n + 1)]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print space-separated values of reversed list\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': '# Definition for singly-linked list.\n# class ListNode:\n#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\nclass Solution:\n    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:\n        # Write your code here\n        pass\n', 'java': '// Reverse Linked List\n/**\n * Definition for singly-linked list.\n * public class ListNode {\n *     int val;\n *     ListNode next;\n *     ListNode() {}\n *     ListNode(int val) { this.val = val; }\n *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }\n * }\n */\nclass Solution {\n    public ListNode reverseList(ListNode head) {\n        // Write your code here\n        return null;\n    }\n}\n', 'c': '// Reverse Linked List\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1 || n <= 0) return 0;\n    int arr[n];\n    for (int i = 0; i < n; i++) scanf("%d", &arr[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print space-separated reversed elements\n    \n    return 0;\n}\n'}, 'longest_substring': {'python': "# Longest Substring Without Repeating Characters\n# Given a string s, find the length of the longest substring without repeating characters.\n\nimport sys\n\ndef solve():\n    s = sys.stdin.read().rstrip('\\r\\n')\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print length integer\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def lengthOfLongestSubstring(self, s: str) -> int:\n        # Write your code here\n        pass\n', 'java': '// Longest Substring Without Repeating Characters\nimport java.util.*;\n\nclass Solution {\n    public int lengthOfLongestSubstring(String s) {\n        // Write your code here\n        return 0;\n    }\n}\n', 'c': '// Longest Substring Without Repeating Characters\n#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char s[100005];\n    if (!fgets(s, sizeof(s), stdin)) {\n        printf("0\\n");\n        return 0;\n    }\n    int len = strlen(s);\n    while (len > 0 && (s[len - 1] == \'\\n\' || s[len - 1] == \'\\r\')) {\n        s[--len] = \'\\0\';\n    }\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print max length\n    \n    return 0;\n}\n'}, 'three_sum': {'python': "# 3Sum\n# Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]]\n# such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:n+1]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print each triplet on a new line: a b c\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def threeSum(self, nums: List[int]) -> List[List[int]]:\n        # Write your code here\n        pass\n', 'java': '// 3Sum\nimport java.util.*;\n\nclass Solution {\n    public List<List<Integer>> threeSum(int[] nums) {\n        // Write your code here\n        return new ArrayList<>();\n    }\n}\n', 'c': '// 3Sum\n#include <stdio.h>\n#include <stdlib.h>\n\nint cmp(const void* a, const void* b) { return (*(int*)a - *(int*)b); }\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1 || n < 3) return 0;\n    int nums[n];\n    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print triplets\n    \n    return 0;\n}\n'}, 'merge_intervals': {'python': "# Merge Intervals\n# Given an array of intervals where intervals[i] = [start_i, end_i],\n# merge all overlapping intervals.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    intervals = []\n    idx = 1\n    for _ in range(n):\n        intervals.append([int(data[idx]), int(data[idx+1])])\n        idx += 2\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print merged intervals: start end\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def merge(self, intervals: List[List[int]]) -> List[List[int]]:\n        # Write your code here\n        pass\n', 'java': '// Merge Intervals\nimport java.util.*;\n\nclass Solution {\n    public int[][] merge(int[][] intervals) {\n        // Write your code here\n        return new int[][]{};\n    }\n}\n', 'c': '// Merge Intervals\n#include <stdio.h>\n#include <stdlib.h>\n\ntypedef struct { int start; int end; } Interval;\nint cmp(const void* a, const void* b) { return ((Interval*)a)->start - ((Interval*)b)->start; }\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1 || n <= 0) return 0;\n    Interval iv[n];\n    for (int i = 0; i < n; i++) scanf("%d %d", &iv[i].start, &iv[i].end);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print merged intervals\n    \n    return 0;\n}\n'}, 'number_of_islands': {'python': "# Number of Islands\n# Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water),\n# return the number of islands.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    m = int(data[0])\n    n = int(data[1])\n    grid = []\n    idx = 2\n    for _ in range(m):\n        grid.append(list(data[idx:idx+n]))\n        idx += n\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print number of islands\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def numIslands(self, grid: List[List[str]]) -> int:\n        # Write your code here\n        pass\n', 'java': '// Number of Islands\nimport java.util.*;\n\nclass Solution {\n    public int numIslands(char[][] grid) {\n        // Write your code here\n        return 0;\n    }\n}\n', 'c': '// Number of Islands\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int m, n;\n    if (scanf("%d %d", &m, &n) != 2) return 0;\n    char grid[m][n];\n    for (int i = 0; i < m; i++) {\n        for (int j = 0; j < n; j++) {\n            scanf(" %c", &grid[i][j]);\n        }\n    }\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print number of islands\n    \n    return 0;\n}\n'}, 'top_k_frequent': {'python': "# Top K Frequent Elements\n# Given an integer array nums and an integer k, return the k most frequent elements.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    k = int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print space-separated k elements\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def topKFrequent(self, nums: List[int], k: int) -> List[int]:\n        # Write your code here\n        pass\n', 'java': '// Top K Frequent Elements\nimport java.util.*;\n\nclass Solution {\n    public int[] topKFrequent(int[] nums, int k) {\n        // Write your code here\n        return new int[]{};\n    }\n}\n', 'c': '// Top K Frequent Elements\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int n, k;\n    if (scanf("%d %d", &n, &k) != 2) return 0;\n    int nums[n];\n    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print space-separated top k frequent elements\n    \n    return 0;\n}\n'}, 'trapping_rain_water': {'python': "# Trapping Rain Water\n# Given n non-negative integers representing an elevation map where the width of each bar is 1,\n# compute how much water it can trap after raining.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    height = [int(x) for x in data[1:n+1]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print trapped water units\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def trap(self, height: List[int]) -> int:\n        # Write your code here\n        pass\n', 'java': '// Trapping Rain Water\nimport java.util.*;\n\nclass Solution {\n    public int trap(int[] height) {\n        // Write your code here\n        return 0;\n    }\n}\n', 'c': '// Trapping Rain Water\n#include <stdio.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n    int height[n];\n    for (int i = 0; i < n; i++) scanf("%d", &height[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print trapped water\n    \n    return 0;\n}\n'}, 'minimum_window_substring': {'python': "# Minimum Window Substring\n# Given two strings s and t of lengths m and n respectively, return the minimum window substring\n# of s such that every character in t (including duplicates) is included in the window.\n\nimport sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    if len(lines) < 2:\n        return\n    s, t = lines[0].strip(), lines[1].strip()\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print min window substring\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def minWindow(self, s: str, t: str) -> str:\n        # Write your code here\n        pass\n', 'java': '// Minimum Window Substring\nimport java.util.*;\n\nclass Solution {\n    public String minWindow(String s, String t) {\n        // Write your code here\n        return "";\n    }\n}\n', 'c': '// Minimum Window Substring\n#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char s[100005], t[100005];\n    if (scanf("%s %s", s, t) != 2) return 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print min window substring\n    \n    return 0;\n}\n'}, 'merge_k_sorted_lists': {'python': "# Merge k Sorted Lists\n# You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.\n# Merge all the linked-lists into one sorted linked-list and return it.\n\nimport sys\n\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    k = int(data[0])\n    lists = []\n    idx = 1\n    for _ in range(k):\n        length = int(data[idx])\n        idx += 1\n        dummy = ListNode(0)\n        cur = dummy\n        for _ in range(length):\n            cur.next = ListNode(int(data[idx]))\n            cur = cur.next\n            idx += 1\n        lists.append(dummy.next)\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print space-separated merged list values\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': '# Definition for singly-linked list.\n# class ListNode:\n#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\nclass Solution:\n    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:\n        # Write your code here\n        pass\n', 'java': '// Merge k Sorted Lists\n/**\n * Definition for singly-linked list.\n * public class ListNode {\n *     int val;\n *     ListNode next;\n *     ListNode() {}\n *     ListNode(int val) { this.val = val; }\n *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }\n * }\n */\nimport java.util.*;\n\nclass Solution {\n    public ListNode mergeKLists(ListNode[] lists) {\n        // Write your code here\n        return null;\n    }\n}\n', 'c': '// Merge k Sorted Lists\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int k;\n    if (scanf("%d", &k) != 1) return 0;\n    \n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print space-separated sorted list\n    \n    return 0;\n}\n'}, 'word_ladder': {'python': "# Word Ladder\n# Given two words, beginWord and endWord, and a dictionary wordList, return the number\n# of words in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    beginWord = data[0]\n    endWord = data[1]\n    n = int(data[2])\n    wordList = data[3:3+n]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print shortest sequence length\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:\n        # Write your code here\n        pass\n', 'java': '// Word Ladder\nimport java.util.*;\n\nclass Solution {\n    public int ladderLength(String beginWord, String endWord, List<String> wordList) {\n        // Write your code here\n        return 0;\n    }\n}\n', 'c': '// Word Ladder\n#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char begin[100], end[100];\n    int n;\n    if (scanf("%s %s %d", begin, end, &n) != 3) return 0;\n    char words[n][100];\n    for (int i = 0; i < n; i++) scanf("%s", words[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print shortest sequence length\n    \n    return 0;\n}\n'}, 'median_two_sorted_arrays': {'python': "# Median of Two Sorted Arrays\n# Given two sorted arrays nums1 and nums2 of size m and n respectively,\n# return the median of the two sorted arrays.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    m = int(data[0])\n    n = int(data[1])\n    nums1 = [int(x) for x in data[2:2+m]]\n    nums2 = [int(x) for x in data[2+m:2+m+n]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print median formatted to 1 decimal place (e.g. 2.5)\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:\n        # Write your code here\n        pass\n', 'java': '// Median of Two Sorted Arrays\nimport java.util.*;\n\nclass Solution {\n    public double findMedianSortedArrays(int[] nums1, int[] nums2) {\n        // Write your code here\n        return 0.0;\n    }\n}\n', 'c': '// Median of Two Sorted Arrays\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int m, n;\n    if (scanf("%d %d", &m, &n) != 2) return 0;\n    int a[m], b[n];\n    for (int i = 0; i < m; i++) scanf("%d", &a[i]);\n    for (int i = 0; i < n; i++) scanf("%d", &b[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print: %.1f\n    \n    return 0;\n}\n'}, 'palindrome_number': {'python': "# Palindrome Number\n# Given an integer x, return true if x is a palindrome, and false otherwise.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    x = int(data[0])\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print: true or false\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def isPalindrome(self, x: int) -> bool:\n        # Write your code here\n        pass\n', 'java': '// Palindrome Number\nimport java.util.*;\n\nclass Solution {\n    public boolean isPalindrome(int x) {\n        // Write your code here\n        return false;\n    }\n}\n', 'c': '// Palindrome Number\n#include <stdio.h>\n#include <stdbool.h>\n\nint main() {\n    int x;\n    if (scanf("%d", &x) != 1) return 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print: true or false\n    \n    return 0;\n}\n'}, 'fizz_buzz': {'python': '# Fizz Buzz\n# Given an integer n, return a string array answer (1-indexed) where:\n# answer[i] == "FizzBuzz" if i is divisible by 3 and 5.\n# answer[i] == "Fizz" if i is divisible by 3.\n# answer[i] == "Buzz" if i is divisible by 5.\n# answer[i] == i (as a string) if none of the above conditions are true.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print space-separated results\n    pass\n\nif __name__ == \'__main__\':\n    solve()\n', 'python_class': 'class Solution:\n    def fizzBuzz(self, n: int) -> List[str]:\n        # Write your code here\n        pass\n', 'java': '// Fizz Buzz\nimport java.util.*;\n\nclass Solution {\n    public List<String> fizzBuzz(int n) {\n        // Write your code here\n        return new ArrayList<>();\n    }\n}\n', 'c': '// Fizz Buzz\n#include <stdio.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print space-separated answers\n    \n    return 0;\n}\n'}, 'length_of_last_word': {'python': "# Length of Last Word\n# Given a string s consisting of words and spaces, return the length of the last word in the string.\n\nimport sys\n\ndef solve():\n    s = sys.stdin.read().rstrip('\\r\\n')\n    \n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print length of last word\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def lengthOfLastWord(self, s: str) -> int:\n        # Write your code here\n        pass\n', 'java': '// Length of Last Word\nimport java.util.*;\n\nclass Solution {\n    public int lengthOfLastWord(String s) {\n        // Write your code here\n        return 0;\n    }\n}\n', 'c': '// Length of Last Word\n#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char s[100005];\n    if (!fgets(s, sizeof(s), stdin)) return 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print integer length\n    \n    return 0;\n}\n'}, 'move_zeroes': {'python': "# Move Zeroes\n# Given an integer array nums, move all 0's to the end of it while maintaining\n# the relative order of the non-zero elements in-place.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:n+1]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print space-separated elements\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def moveZeroes(self, nums: List[int]) -> None:\n        # Modify nums in-place\n        pass\n', 'java': '// Move Zeroes\nimport java.util.*;\n\nclass Solution {\n    public void moveZeroes(int[] nums) {\n        // Modify nums in-place\n    }\n}\n', 'c': '// Move Zeroes\n#include <stdio.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n    int nums[n];\n    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print space-separated elements\n    \n    return 0;\n}\n'}, 'merge_sorted_array': {'python': "# Merge Sorted Array\n# You are given two integer arrays nums1 and nums2, sorted in non-decreasing order,\n# and two integers m and n, representing the number of elements in nums1 and nums2 respectively.\n# Merge nums2 into nums1 in-place as one sorted array.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    m = int(data[0])\n    n = int(data[1])\n    nums1 = [int(x) for x in data[2:2+m]] + [0] * n\n    nums2 = [int(x) for x in data[2+m:2+m+n]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print space-separated merged array\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:\n        # Modify nums1 in-place\n        pass\n', 'java': '// Merge Sorted Array\nimport java.util.*;\n\nclass Solution {\n    public void merge(int[] nums1, int m, int[] nums2, int n) {\n        // Modify nums1 in-place\n    }\n}\n', 'c': '// Merge Sorted Array\n#include <stdio.h>\n\nint main() {\n    int m, n;\n    if (scanf("%d %d", &m, &n) != 2) return 0;\n    int nums1[m + n];\n    for (int i = 0; i < m; i++) scanf("%d", &nums1[i]);\n    int nums2[n];\n    for (int i = 0; i < n; i++) scanf("%d", &nums2[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print space-separated merged array\n    \n    return 0;\n}\n'}, 'add_two_numbers': {'python': "# Add Two Numbers\n# You are given two non-empty linked lists representing two non-negative integers.\n# The digits are stored in reverse order, and each of their nodes contains a single digit.\n# Add the two numbers and return the sum as a linked list.\n\nimport sys\n\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n1 = int(data[0])\n    idx = 1\n    nums1 = [int(data[idx + i]) for i in range(n1)]\n    idx += n1\n    n2 = int(data[idx])\n    idx += 1\n    nums2 = [int(data[idx + i]) for i in range(n2)]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print space-separated digits of the sum\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': '# Definition for singly-linked list.\n# class ListNode:\n#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\nclass Solution:\n    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:\n        # Write your code here\n        pass\n', 'java': '// Add Two Numbers\n/**\n * Definition for singly-linked list.\n * public class ListNode {\n *     int val;\n *     ListNode next;\n *     ListNode() {}\n *     ListNode(int val) { this.val = val; }\n *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }\n * }\n */\nclass Solution {\n    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {\n        // Write your code here\n        return null;\n    }\n}\n', 'c': '// Add Two Numbers\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int n1;\n    if (scanf("%d", &n1) != 1) return 0;\n    int l1[n1];\n    for (int i = 0; i < n1; i++) scanf("%d", &l1[i]);\n    int n2;\n    scanf("%d", &n2);\n    int l2[n2];\n    for (int i = 0; i < n2; i++) scanf("%d", &l2[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print space-separated digits\n    \n    return 0;\n}\n'}, 'rotate_array': {'python': "# Rotate Array\n# Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    k = int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print space-separated rotated array\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def rotate(self, nums: List[int], k: int) -> None:\n        # Modify nums in-place\n        pass\n', 'java': '// Rotate Array\nimport java.util.*;\n\nclass Solution {\n    public void rotate(int[] nums, int k) {\n        // Modify nums in-place\n    }\n}\n', 'c': '// Rotate Array\n#include <stdio.h>\n\nint main() {\n    int n, k;\n    if (scanf("%d %d", &n, &k) != 2) return 0;\n    int nums[n];\n    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print space-separated rotated array\n    \n    return 0;\n}\n'}, 'coin_change': {'python': "# Coin Change\n# You are given an integer array coins representing coins of different denominations\n# and an integer amount representing a total amount of money.\n# Return the fewest number of coins that you need to make up that amount.\n# If that amount of money cannot be made up by any combination of the coins, return -1.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    amount = int(data[1])\n    coins = [int(x) for x in data[2:2+n]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print fewest number of coins or -1\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def coinChange(self, coins: List[int], amount: int) -> int:\n        # Write your code here\n        pass\n', 'java': '// Coin Change\nimport java.util.*;\n\nclass Solution {\n    public int coinChange(int[] coins, int amount) {\n        // Write your code here\n        return -1;\n    }\n}\n', 'c': '// Coin Change\n#include <stdio.h>\n\nint main() {\n    int n, amount;\n    if (scanf("%d %d", &n, &amount) != 2) return 0;\n    int coins[n];\n    for (int i = 0; i < n; i++) scanf("%d", &coins[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print integer result\n    \n    return 0;\n}\n'}, 'binary_tree': {'python': "# Binary Tree Level Order Traversal\n# Given the root of a binary tree, return the level order traversal of its nodes' values.\n# (i.e., from left to right, level by level).\n\nimport sys\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    vals = [int(x) for x in data[1:n+1]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print each level on a new line with space-separated values\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': '# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\nclass Solution:\n    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:\n        # Write your code here\n        pass\n', 'java': '// Binary Tree Level Order Traversal\n/**\n * Definition for a binary tree node.\n * public class TreeNode {\n *     int val;\n *     TreeNode left;\n *     TreeNode right;\n *     TreeNode(int val) { this.val = val; }\n * }\n */\nimport java.util.*;\n\nclass Solution {\n    public List<List<Integer>> levelOrder(TreeNode root) {\n        // Write your code here\n        return new ArrayList<>();\n    }\n}\n', 'c': '// Binary Tree Level Order Traversal\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1 || n == 0) return 0;\n    int vals[n];\n    for (int i = 0; i < n; i++) scanf("%d", &vals[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print each level on a new line\n    \n    return 0;\n}\n'}, 'combination_sum': {'python': "# Combination Sum\n# Given an array of distinct integers candidates and a target integer target,\n# return a list of all unique combinations of candidates where the chosen numbers sum to target.\n# You may return the combinations in any order. The same number may be chosen unlimited times.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    target = int(data[1])\n    cands = [int(x) for x in data[2:2+n]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print each combination on a new line with space-separated integers\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:\n        # Write your code here\n        pass\n', 'java': '// Combination Sum\nimport java.util.*;\n\nclass Solution {\n    public List<List<Integer>> combinationSum(int[] candidates, int target) {\n        // Write your code here\n        return new ArrayList<>();\n    }\n}\n', 'c': '// Combination Sum\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int n, target;\n    if (scanf("%d %d", &n, &target) != 2) return 0;\n    int cands[n];\n    for (int i = 0; i < n; i++) scanf("%d", &cands[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print combinations\n    \n    return 0;\n}\n'}, 'largest_rectangle_histogram': {'python': "# Largest Rectangle in Histogram\n# Given an array of integers heights representing the histogram's bar height\n# where the width of each bar is 1, return the area of the largest rectangle in the histogram.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    heights = [int(x) for x in data[1:n+1]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print max rectangle area integer\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def largestRectangleArea(self, heights: List[int]) -> int:\n        # Write your code here\n        pass\n', 'java': '// Largest Rectangle in Histogram\nimport java.util.*;\n\nclass Solution {\n    public int largestRectangleArea(int[] heights) {\n        // Write your code here\n        return 0;\n    }\n}\n', 'c': '// Largest Rectangle in Histogram\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n    int heights[n];\n    for (int i = 0; i < n; i++) scanf("%d", &heights[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print max area integer\n    \n    return 0;\n}\n'}, 'serialize_deserialize_tree': {'python': "# Serialize and Deserialize Binary Tree\n# Design an algorithm to serialize and deserialize a binary tree.\n# There is no restriction on how your serialization/deserialization algorithm should work.\n\nimport sys\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef solve():\n    data = sys.stdin.read().strip()\n    if not data:\n        return\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print space-separated level order representation\n    print(data)\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': '# Definition for a binary tree node.\n# class TreeNode(object):\n#     def __init__(self, x):\n#         self.val = x\n#         self.left = None\n#         self.right = None\n\nclass Codec:\n    def serialize(self, root: Optional[TreeNode]) -> str:\n        # Encodes a tree to a single string.\n        pass\n\n    def deserialize(self, data: str) -> Optional[TreeNode]:\n        # Decodes your encoded data to tree.\n        pass\n', 'java': '// Serialize and Deserialize Binary Tree\n/**\n * Definition for a binary tree node.\n * public class TreeNode {\n *     int val;\n *     TreeNode left;\n *     TreeNode right;\n *     TreeNode(int val) { val = x; }\n * }\n */\nimport java.util.*;\n\npublic class Codec {\n    // Encodes a tree to a single string.\n    public String serialize(TreeNode root) {\n        return "";\n    }\n\n    // Decodes your encoded data to tree.\n    public TreeNode deserialize(String data) {\n        return null;\n    }\n}\n', 'c': '// Serialize and Deserialize Binary Tree\n#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char buf[10000];\n    if (!fgets(buf, sizeof(buf), stdin)) return 0;\n    int len = strlen(buf);\n    while (len > 0 && (buf[len-1] == \'\\n\' || buf[len-1] == \'\\r\')) buf[--len] = \'\\0\';\n    printf("%s\\n", buf);\n    return 0;\n}\n'}, 'edit_distance': {'python': '# Edit Distance\n# Given two strings word1 and word2, return the minimum number of operations\n# required to convert word1 to word2 (insert, delete, or replace a character).\n\nimport sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    word1 = lines[0].strip() if len(lines) > 0 else ""\n    word2 = lines[1].strip() if len(lines) > 1 else ""\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print minimum edit operations integer\n    pass\n\nif __name__ == \'__main__\':\n    solve()\n', 'python_class': 'class Solution:\n    def minDistance(self, word1: str, word2: str) -> int:\n        # Write your code here\n        pass\n', 'java': '// Edit Distance\nimport java.util.*;\n\nclass Solution {\n    public int minDistance(String word1, String word2) {\n        // Write your code here\n        return 0;\n    }\n}\n', 'c': '// Edit Distance\n#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char w1[1005], w2[1005];\n    if (scanf("%s %s", w1, w2) < 1) return 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print integer min distance\n    \n    return 0;\n}\n'}, 'word_search_ii': {'python': "# Word Search II\n# Given an m x n board of characters and a list of strings words,\n# return all words on the board. Each word must be constructed from letters of sequentially adjacent cells.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    m = int(data[0])\n    n = int(data[1])\n    board = []\n    idx = 2\n    for _ in range(m):\n        board.append(data[idx:idx+n])\n        idx += n\n    w = int(data[idx])\n    idx += 1\n    words = data[idx:idx+w]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print space-separated found words (sorted)\n    pass\n\nif __name__ == '__main__':\n    solve()\n", 'python_class': 'class Solution:\n    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:\n        # Write your code here\n        pass\n', 'java': '// Word Search II\nimport java.util.*;\n\nclass Solution {\n    public List<String> findWords(char[][] board, String[] words) {\n        // Write your code here\n        return new ArrayList<>();\n    }\n}\n', 'c': '// Word Search II\n#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n\nint main() {\n    int m, n;\n    if (scanf("%d %d", &m, &n) != 2) return 0;\n    char board[m][n];\n    for (int i = 0; i < m; i++) {\n        for (int j = 0; j < n; j++) {\n            scanf(" %c", &board[i][j]);\n        }\n    }\n    int w;\n    scanf("%d", &w);\n    char words[w][100];\n    for (int i = 0; i < w; i++) scanf("%s", words[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print space-separated found words\n    \n    return 0;\n}\n'}, 'regular_expression_matching': {'python': '# Regular Expression Matching\n# Given an input string s and a pattern p, implement regular expression matching\n# with support for \'.\' and \'*\' where \'.\' matches any single character, and \'*\' matches zero or more of preceding element.\n\nimport sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    s = lines[0].strip() if len(lines) > 0 else ""\n    p = lines[1].strip() if len(lines) > 1 else ""\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print: true or false\n    pass\n\nif __name__ == \'__main__\':\n    solve()\n', 'python_class': 'class Solution:\n    def isMatch(self, s: str, p: str) -> bool:\n        # Write your code here\n        pass\n', 'java': '// Regular Expression Matching\nimport java.util.*;\n\nclass Solution {\n    public boolean isMatch(String s, String p) {\n        // Write your code here\n        return false;\n    }\n}\n', 'c': '// Regular Expression Matching\n#include <stdio.h>\n#include <stdbool.h>\n#include <string.h>\n\nint main() {\n    char s[1005], p[1005];\n    if (scanf("%s %s", s, p) < 1) return 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print: true or false\n    \n    return 0;\n}\n'}}

    @classmethod
    def get_starter_code(cls, problem_id: str) -> Dict[str, str]:
        """Returns starter code templates for all 4 tracks for a problem."""
        clean_id = (problem_id or "").strip().lower()
        if clean_id in cls.STARTER_TEMPLATES:
            return cls.STARTER_TEMPLATES[clean_id]
        
        # Generic fallback
        return {
            "python": "# Python 3 Solution\nimport sys\n\ndef solve():\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            "python_class": "class Solution:\n    # Write your solution methods here\n    pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    // Write your solution methods here\n}\n",
            "c": "#include <stdio.h>\n\nint main() {\n    // Write your solution here\n    return 0;\n}\n"
        }

    @classmethod
    def has_standalone_main(cls, language: str, user_code: str) -> bool:
        """Determines if the user code already contains an IO driver."""
        lang = language.lower()
        if lang in ["python", "python3", "py", "python_normal", "python_script"]:
            return ("if __name__ ==" in user_code or "sys.stdin" in user_code or "input(" in user_code)
        elif lang == "java":
            return ("public static void main" in user_code or "static public void main" in user_code)
        elif lang in ["c", "c99", "c11"]:
            return ("main(" in user_code)
        return False

    @classmethod
    def wrap_code(cls, arg1: str, arg2: str, user_code: str) -> str:
        """Wraps pure LeetCode class Solution / function code with problem IO harness."""
        known_langs = {"python", "python3", "py", "python_class", "python_leetcode", "python_normal", "python_script", "java", "c", "c99", "c11"}
        if (arg1 or "").lower() in known_langs:
            lang = (arg1 or "").lower()
            clean_id = (arg2 or "").strip().lower()
        else:
            clean_id = (arg1 or "").strip().lower()
            lang = (arg2 or "").lower()

        if cls.has_standalone_main(lang, user_code):
            return user_code

        if lang == "java":
            return cls._wrap_java(clean_id, user_code)
        elif lang in ["python", "python3", "py", "python_class", "python_leetcode", "python_normal", "python_script"]:
            return cls._wrap_python(clean_id, user_code)
        elif lang in ["c", "c99", "c11"]:
            return cls._wrap_c(clean_id, user_code)
        return user_code

    # ------------------- JAVA WRAPPERS -------------------

    @classmethod
    def _wrap_java(cls, pid: str, user_code: str) -> str:
        user_imports = []
        clean_lines = []
        for line in user_code.splitlines():
            if line.strip().startswith("import "):
                user_imports.append(line.strip())
            else:
                clean_lines.append(line)
        clean_code = "\n".join(clean_lines)
        clean_code = re.sub(r'public\s+class\s+Solution', 'class Solution', clean_code)
        clean_code = re.sub(r'public\s+class\s+Codec', 'class Codec', clean_code)
        
        prefix = "import java.util.*;\nimport java.io.*;\nimport java.math.*;\n" + "\n".join(user_imports) + """

class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
"""
        harness = ""
        # SET 1
        if pid == "two_sum":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        int target = sc.nextInt();
        Solution sol = new Solution();
        int[] res = sol.twoSum(nums, target);
        if (res != null && res.length >= 2) {
            System.out.println(res[0] + " " + res[1]);
        }
    }
}"""
        elif pid == "reverse_string":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNextLine() ? sc.nextLine().replaceAll("[\\r\\n]", "") : "";
        Solution sol = new Solution();
        System.out.println(sol.reverseString(s));
    }
}"""
        elif pid == "find_duplicate":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.findDuplicate(nums));
    }
}"""
        elif pid == "valid_parentheses":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNext() ? sc.next() : "";
        Solution sol = new Solution();
        System.out.println(sol.isValid(s) ? "true" : "false");
    }
}"""
        elif pid == "reverse_linked_list":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        ListNode dummy = new ListNode(0);
        ListNode cur = dummy;
        for (int i = 0; i < n; i++) {
            cur.next = new ListNode(sc.nextInt());
            cur = cur.next;
        }
        Solution sol = new Solution();
        ListNode head = sol.reverseList(dummy.next);
        while (head != null) {
            System.out.print(head.val + (head.next == null ? "" : " "));
            head = head.next;
        }
        System.out.println();
    }
}"""
        elif pid == "longest_substring":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNextLine() ? sc.nextLine().replaceAll("[\\r\\n]", "") : "";
        Solution sol = new Solution();
        System.out.println(sol.lengthOfLongestSubstring(s));
    }
}"""
        elif pid == "three_sum":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        List<List<Integer>> res = sol.threeSum(nums);
        if (res != null) {
            for (List<Integer> triplet : res) {
                System.out.println(triplet.get(0) + " " + triplet.get(1) + " " + triplet.get(2));
            }
        }
    }
}"""
        elif pid == "merge_intervals":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[][] intervals = new int[n][2];
        for (int i = 0; i < n; i++) {
            intervals[i][0] = sc.nextInt();
            intervals[i][1] = sc.nextInt();
        }
        Solution sol = new Solution();
        int[][] res = sol.merge(intervals);
        if (res != null) {
            for (int[] iv : res) {
                System.out.println(iv[0] + " " + iv[1]);
            }
        }
    }
}"""
        elif pid == "number_of_islands":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int m = sc.nextInt();
        int n = sc.nextInt();
        char[][] grid = new char[m][n];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                grid[i][j] = sc.next().charAt(0);
            }
        }
        Solution sol = new Solution();
        System.out.println(sol.numIslands(grid));
    }
}"""
        elif pid == "top_k_frequent":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int k = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        int[] res = sol.topKFrequent(nums, k);
        if (res != null) {
            for (int i = 0; i < res.length; i++) {
                System.out.print(res[i] + (i == res.length - 1 ? "" : " "));
            }
            System.out.println();
        }
    }
}"""
        elif pid == "trapping_rain_water":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] height = new int[n];
        for (int i = 0; i < n; i++) height[i] = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.trap(height));
    }
}"""
        elif pid == "minimum_window_substring":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextLine()) return;
        String s = sc.nextLine().trim();
        if (!sc.hasNextLine()) return;
        String t = sc.nextLine().trim();
        Solution sol = new Solution();
        System.out.println(sol.minWindow(s, t));
    }
}"""
        elif pid == "merge_k_sorted_lists":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int k = sc.nextInt();
        ListNode[] lists = new ListNode[k];
        for (int i = 0; i < k; i++) {
            int len = sc.nextInt();
            ListNode dummy = new ListNode(0);
            ListNode cur = dummy;
            for (int j = 0; j < len; j++) {
                cur.next = new ListNode(sc.nextInt());
                cur = cur.next;
            }
            lists[i] = dummy.next;
        }
        Solution sol = new Solution();
        ListNode head = sol.mergeKLists(lists);
        while (head != null) {
            System.out.print(head.val + (head.next == null ? "" : " "));
            head = head.next;
        }
        System.out.println();
    }
}"""
        elif pid == "word_ladder":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNext()) return;
        String begin = sc.next();
        String end = sc.next();
        int n = sc.nextInt();
        List<String> list = new ArrayList<>();
        for (int i = 0; i < n; i++) list.add(sc.next());
        Solution sol = new Solution();
        System.out.println(sol.ladderLength(begin, end, list));
    }
}"""
        elif pid == "median_two_sorted_arrays":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int m = sc.nextInt();
        int n = sc.nextInt();
        int[] nums1 = new int[m];
        for (int i = 0; i < m; i++) nums1[i] = sc.nextInt();
        int[] nums2 = new int[n];
        for (int i = 0; i < n; i++) nums2[i] = sc.nextInt();
        Solution sol = new Solution();
        System.out.printf(Locale.US, "%.1f\\n", sol.findMedianSortedArrays(nums1, nums2));
    }
}"""

        # SET 2
        elif pid == "palindrome_number":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int x = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.isPalindrome(x) ? "true" : "false");
    }
}"""
        elif pid == "fizz_buzz":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        Solution sol = new Solution();
        List<String> res = sol.fizzBuzz(n);
        if (res != null) {
            System.out.println(String.join(" ", res));
        }
    }
}"""
        elif pid == "length_of_last_word":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNextLine() ? sc.nextLine() : "";
        Solution sol = new Solution();
        System.out.println(sol.lengthOfLastWord(s));
    }
}"""
        elif pid == "move_zeroes":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        sol.moveZeroes(nums);
        for (int i = 0; i < n; i++) {
            System.out.print(nums[i] + (i == n - 1 ? "" : " "));
        }
        System.out.println();
    }
}"""
        elif pid == "merge_sorted_array":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int m = sc.nextInt();
        int n = sc.nextInt();
        int[] nums1 = new int[m + n];
        for (int i = 0; i < m; i++) nums1[i] = sc.nextInt();
        int[] nums2 = new int[n];
        for (int i = 0; i < n; i++) nums2[i] = sc.nextInt();
        Solution sol = new Solution();
        sol.merge(nums1, m, nums2, n);
        for (int i = 0; i < m + n; i++) {
            System.out.print(nums1[i] + (i == m + n - 1 ? "" : " "));
        }
        System.out.println();
    }
}"""
        elif pid == "add_two_numbers":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n1 = sc.nextInt();
        ListNode dummy1 = new ListNode(0);
        ListNode cur1 = dummy1;
        for (int i = 0; i < n1; i++) {
            cur1.next = new ListNode(sc.nextInt());
            cur1 = cur1.next;
        }
        int n2 = sc.nextInt();
        ListNode dummy2 = new ListNode(0);
        ListNode cur2 = dummy2;
        for (int i = 0; i < n2; i++) {
            cur2.next = new ListNode(sc.nextInt());
            cur2 = cur2.next;
        }
        Solution sol = new Solution();
        ListNode res = sol.addTwoNumbers(dummy1.next, dummy2.next);
        while (res != null) {
            System.out.print(res.val + (res.next == null ? "" : " "));
            res = res.next;
        }
        System.out.println();
    }
}"""
        elif pid == "rotate_array":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int k = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        sol.rotate(nums, k);
        for (int i = 0; i < n; i++) {
            System.out.print(nums[i] + (i == n - 1 ? "" : " "));
        }
        System.out.println();
    }
}"""
        elif pid == "coin_change":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int amount = sc.nextInt();
        int[] coins = new int[n];
        for (int i = 0; i < n; i++) coins[i] = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.coinChange(coins, amount));
    }
}"""
        elif pid == "binary_tree":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        if (n == 0) return;
        int[] vals = new int[n];
        for (int i = 0; i < n; i++) vals[i] = sc.nextInt();
        TreeNode[] nodes = new TreeNode[n];
        for (int i = 0; i < n; i++) nodes[i] = new TreeNode(vals[i]);
        for (int i = 0; i < n; i++) {
            if (2 * i + 1 < n) nodes[i].left = nodes[2 * i + 1];
            if (2 * i + 2 < n) nodes[i].right = nodes[2 * i + 2];
        }
        Solution sol = new Solution();
        List<List<Integer>> res = sol.levelOrder(nodes[0]);
        if (res != null) {
            for (List<Integer> level : res) {
                for (int j = 0; j < level.size(); j++) {
                    System.out.print(level.get(j) + (j == level.size() - 1 ? "" : " "));
                }
                System.out.println();
            }
        }
    }
}"""
        elif pid == "combination_sum":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int target = sc.nextInt();
        int[] cands = new int[n];
        for (int i = 0; i < n; i++) cands[i] = sc.nextInt();
        Solution sol = new Solution();
        List<List<Integer>> res = sol.combinationSum(cands, target);
        if (res != null) {
            for (List<Integer> comb : res) {
                for (int j = 0; j < comb.size(); j++) {
                    System.out.print(comb.get(j) + (j == comb.size() - 1 ? "" : " "));
                }
                System.out.println();
            }
        }
    }
}"""
        elif pid == "largest_rectangle_histogram":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] heights = new int[n];
        for (int i = 0; i < n; i++) heights[i] = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.largestRectangleArea(heights));
    }
}"""
        elif pid == "serialize_deserialize_tree":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextLine()) return;
        String line = sc.nextLine().trim();
        if (line.isEmpty() || line.equals("null")) return;
        Codec codec = new Codec();
        TreeNode root = codec.deserialize(line);
        if (root == null) return;
        List<Integer> out = new ArrayList<>();
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root);
        while (!q.isEmpty()) {
            TreeNode node = q.poll();
            if (node != null) {
                out.add(node.val);
                if (node.left != null) q.offer(node.left);
                if (node.right != null) q.offer(node.right);
            }
        }
        for (int i = 0; i < out.size(); i++) {
            System.out.print(out.get(i) + (i == out.size() - 1 ? "" : " "));
        }
        System.out.println();
    }
}"""
        elif pid == "edit_distance":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String word1 = sc.hasNextLine() ? sc.nextLine().trim() : "";
        String word2 = sc.hasNextLine() ? sc.nextLine().trim() : "";
        Solution sol = new Solution();
        System.out.println(sol.minDistance(word1, word2));
    }
}"""
        elif pid == "word_search_ii":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int m = sc.nextInt();
        int n = sc.nextInt();
        char[][] board = new char[m][n];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                board[i][j] = sc.next().charAt(0);
            }
        }
        int w = sc.nextInt();
        String[] words = new String[w];
        for (int i = 0; i < w; i++) words[i] = sc.next();
        Solution sol = new Solution();
        List<String> res = sol.findWords(board, words);
        if (res != null) {
            Collections.sort(res);
            System.out.println(String.join(" ", res));
        }
    }
}"""
        elif pid == "regular_expression_matching":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNextLine() ? sc.nextLine().trim() : "";
        String p = sc.hasNextLine() ? sc.nextLine().trim() : "";
        Solution sol = new Solution();
        System.out.println(sol.isMatch(s, p) ? "true" : "false");
    }
}"""

        if not harness:
            return user_code
        return prefix + "\n" + clean_code + "\n" + harness

    # ------------------- PYTHON WRAPPERS -------------------

    @classmethod
    def _wrap_python(cls, pid: str, user_code: str) -> str:
        prefix = """import sys
import math
import heapq
from typing import List, Dict, Optional, Tuple, Set, Any
from collections import Counter, defaultdict, deque

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
"""
        harness = ""
        # SET 1
        if pid == "two_sum":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    nums = [int(x) for x in data[1:n+1]]
    target = int(data[n+1])
    sol = Solution()
    res = sol.twoSum(nums, target)
    if res is not None and len(res) >= 2:
        print(f"{res[0]} {res[1]}")

__run_test()
"""
        elif pid == "reverse_string":
            harness = """
def __run_test():
    lines = sys.stdin.read().splitlines()
    s = lines[0] if lines else ""
    sol = Solution()
    print(sol.reverseString(s))

__run_test()
"""
        elif pid == "find_duplicate":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    nums = [int(x) for x in data[1:n+1]]
    sol = Solution()
    print(sol.findDuplicate(nums))

__run_test()
"""
        elif pid == "valid_parentheses":
            harness = """
def __run_test():
    s = sys.stdin.read().strip()
    sol = Solution()
    print("true" if sol.isValid(s) else "false")

__run_test()
"""
        elif pid == "reverse_linked_list":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data or int(data[0]) <= 0: return
    n = int(data[0])
    nums = [int(data[i]) for i in range(1, n + 1)]
    dummy = ListNode(0)
    cur = dummy
    for x in nums:
        cur.next = ListNode(x)
        cur = cur.next
    sol = Solution()
    head = sol.reverseList(dummy.next)
    out = []
    while head:
        out.append(str(head.val))
        head = head.next
    print(" ".join(out))

__run_test()
"""
        elif pid == "longest_substring":
            harness = """
def __run_test():
    lines = sys.stdin.read().splitlines()
    s = lines[0] if lines else ""
    sol = Solution()
    print(sol.lengthOfLongestSubstring(s))

__run_test()
"""
        elif pid == "three_sum":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    nums = [int(x) for x in data[1:n+1]]
    sol = Solution()
    res = sol.threeSum(nums)
    if res:
        for t in sorted([sorted(x) for x in res]):
            print(f"{t[0]} {t[1]} {t[2]}")

__run_test()
"""
        elif pid == "merge_intervals":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    intervals = []
    idx = 1
    for _ in range(n):
        intervals.append([int(data[idx]), int(data[idx+1])])
        idx += 2
    sol = Solution()
    res = sol.merge(intervals)
    if res:
        for iv in sorted(res, key=lambda x: x[0]):
            print(f"{iv[0]} {iv[1]}")

__run_test()
"""
        elif pid == "number_of_islands":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    m = int(data[0])
    n = int(data[1])
    grid = []
    idx = 2
    for _ in range(m):
        grid.append(list(data[idx:idx+n]))
        idx += n
    sol = Solution()
    print(sol.numIslands(grid))

__run_test()
"""
        elif pid == "top_k_frequent":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    k = int(data[1])
    nums = [int(x) for x in data[2:2+n]]
    sol = Solution()
    res = sol.topKFrequent(nums, k)
    if res is not None:
        print(" ".join(map(str, res)))

__run_test()
"""
        elif pid == "trapping_rain_water":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    height = [int(x) for x in data[1:n+1]]
    sol = Solution()
    print(sol.trap(height))

__run_test()
"""
        elif pid == "minimum_window_substring":
            harness = """
def __run_test():
    lines = sys.stdin.read().splitlines()
    if len(lines) < 2: return
    s, t = lines[0].strip(), lines[1].strip()
    sol = Solution()
    print(sol.minWindow(s, t))

__run_test()
"""
        elif pid == "merge_k_sorted_lists":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    k = int(data[0])
    lists = []
    idx = 1
    for _ in range(k):
        length = int(data[idx])
        idx += 1
        dummy = ListNode(0)
        cur = dummy
        for _ in range(length):
            cur.next = ListNode(int(data[idx]))
            cur = cur.next
            idx += 1
        lists.append(dummy.next)
    sol = Solution()
    head = sol.mergeKLists(lists)
    out = []
    while head:
        out.append(str(head.val))
        head = head.next
    print(" ".join(out))

__run_test()
"""
        elif pid == "word_ladder":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    beginWord = data[0]
    endWord = data[1]
    n = int(data[2])
    wordList = data[3:3+n]
    sol = Solution()
    print(sol.ladderLength(beginWord, endWord, wordList))

__run_test()
"""
        elif pid == "median_two_sorted_arrays":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    m = int(data[0])
    n = int(data[1])
    nums1 = [int(x) for x in data[2:2+m]]
    nums2 = [int(x) for x in data[2+m:2+m+n]]
    sol = Solution()
    print(f"{sol.findMedianSortedArrays(nums1, nums2):.1f}")

__run_test()
"""

        # SET 2
        elif pid == "palindrome_number":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    x = int(data[0])
    sol = Solution()
    print("true" if sol.isPalindrome(x) else "false")

__run_test()
"""
        elif pid == "fizz_buzz":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    sol = Solution()
    res = sol.fizzBuzz(n)
    if res is not None:
        print(" ".join(map(str, res)))

__run_test()
"""
        elif pid == "length_of_last_word":
            harness = """
def __run_test():
    lines = sys.stdin.read().splitlines()
    s = lines[0] if lines else ""
    sol = Solution()
    print(sol.lengthOfLastWord(s))

__run_test()
"""
        elif pid == "move_zeroes":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    nums = [int(x) for x in data[1:n+1]]
    sol = Solution()
    sol.moveZeroes(nums)
    print(" ".join(map(str, nums)))

__run_test()
"""
        elif pid == "merge_sorted_array":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    m = int(data[0])
    n = int(data[1])
    nums1 = [int(x) for x in data[2:2+m]] + [0] * n
    nums2 = [int(x) for x in data[2+m:2+m+n]]
    sol = Solution()
    sol.merge(nums1, m, nums2, n)
    print(" ".join(map(str, nums1)))

__run_test()
"""
        elif pid == "add_two_numbers":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n1 = int(data[0])
    idx = 1
    dummy1 = ListNode(0)
    cur1 = dummy1
    for _ in range(n1):
        cur1.next = ListNode(int(data[idx]))
        cur1 = cur1.next
        idx += 1
    n2 = int(data[idx])
    idx += 1
    dummy2 = ListNode(0)
    cur2 = dummy2
    for _ in range(n2):
        cur2.next = ListNode(int(data[idx]))
        cur2 = cur2.next
        idx += 1
    sol = Solution()
    res = sol.addTwoNumbers(dummy1.next, dummy2.next)
    out = []
    while res:
        out.append(str(res.val))
        res = res.next
    print(" ".join(out))

__run_test()
"""
        elif pid == "rotate_array":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    k = int(data[1])
    nums = [int(x) for x in data[2:2+n]]
    sol = Solution()
    sol.rotate(nums, k)
    print(" ".join(map(str, nums)))

__run_test()
"""
        elif pid == "coin_change":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    amount = int(data[1])
    coins = [int(x) for x in data[2:2+n]]
    sol = Solution()
    print(sol.coinChange(coins, amount))

__run_test()
"""
        elif pid == "binary_tree":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    if n == 0: return
    vals = [int(x) for x in data[1:n+1]]
    nodes = [TreeNode(v) for v in vals]
    for i in range(n):
        if 2 * i + 1 < n: nodes[i].left = nodes[2 * i + 1]
        if 2 * i + 2 < n: nodes[i].right = nodes[2 * i + 2]
    sol = Solution()
    res = sol.levelOrder(nodes[0])
    if res:
        for lvl in res:
            print(" ".join(map(str, lvl)))

__run_test()
"""
        elif pid == "combination_sum":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    target = int(data[1])
    cands = [int(x) for x in data[2:2+n]]
    sol = Solution()
    res = sol.combinationSum(cands, target)
    if res:
        for comb in res:
            print(" ".join(map(str, comb)))

__run_test()
"""
        elif pid == "largest_rectangle_histogram":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    heights = [int(x) for x in data[1:n+1]]
    sol = Solution()
    print(sol.largestRectangleArea(heights))

__run_test()
"""
        elif pid == "serialize_deserialize_tree":
            harness = """
def __run_test():
    data = sys.stdin.read().strip()
    if not data or data == "null": return
    codec = Codec()
    root = codec.deserialize(data)
    if not root: return
    out = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node:
            out.append(str(node.val))
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
    print(" ".join(out))

__run_test()
"""
        elif pid == "edit_distance":
            harness = """
def __run_test():
    lines = sys.stdin.read().splitlines()
    w1 = lines[0].strip() if len(lines) > 0 else ""
    w2 = lines[1].strip() if len(lines) > 1 else ""
    sol = Solution()
    print(sol.minDistance(w1, w2))

__run_test()
"""
        elif pid == "word_search_ii":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    m = int(data[0])
    n = int(data[1])
    board = []
    idx = 2
    for _ in range(m):
        board.append(data[idx:idx+n])
        idx += n
    w = int(data[idx])
    idx += 1
    words = data[idx:idx+w]
    sol = Solution()
    res = sol.findWords(board, words)
    if res:
        print(" ".join(sorted(res)))

__run_test()
"""
        elif pid == "regular_expression_matching":
            harness = """
def __run_test():
    lines = sys.stdin.read().splitlines()
    s = lines[0].strip() if len(lines) > 0 else ""
    p = lines[1].strip() if len(lines) > 1 else ""
    sol = Solution()
    print("true" if sol.isMatch(s, p) else "false")

__run_test()
"""

        if not harness:
            return user_code
        return prefix + "\n" + user_code + "\n" + harness

    # ------------------- C WRAPPERS -------------------

    @classmethod
    def _wrap_c(cls, pid: str, user_code: str) -> str:
        return user_code
