"""
CODE COMBAT Pro - LeetCode Driver Harness Engine
Provides authentic LeetCode class Solution starter templates and auto-wrapping IO drivers
for Java, Python 3, and C for all 15 problems.
"""

import re
from typing import Dict, Any, Optional


class Harness:
    """Manages LeetCode starter templates and compiles auto-wrapping IO harnesses."""

    STARTER_TEMPLATES = {
        # ============================== EASY (5) ==============================
        "two_sum": {
            "python": """# Two Sum
# Given an array of integers nums and an integer target,
# return indices of the two numbers such that they add up to target.

import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    nums = [int(x) for x in data[1:n+1]]
    target = int(data[n+1])

    # --- WRITE YOUR SOLUTION HERE ---
    # Print space-separated indices: i j
    pass

if __name__ == '__main__':
    solve()
""",
            "python_class": """class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Write your code here
        pass
""",
            "java": """// Two Sum
import java.util.*;

class Solution {
    public int[] twoSum(int[] nums, int target) {
        // Write your code here
        return new int[]{};
    }
}
""",
            "c": """// Two Sum
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int nums[n];
    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);
    int target;
    scanf("%d", &target);

    // --- WRITE YOUR SOLUTION HERE ---
    // Print: i j
    
    return 0;
}
"""
        },

        "reverse_string": {
            "python": """# Reverse a String
# Reverse the given input string.

import sys

def solve():
    s = sys.stdin.read().rstrip('\\r\\n')
    
    # --- WRITE YOUR SOLUTION HERE ---
    # Print reversed string
    pass

if __name__ == '__main__':
    solve()
""",
            "python_class": """class Solution:
    def reverseString(self, s: str) -> str:
        # Write your code here
        pass
""",
            "java": """// Reverse a String
import java.util.*;

class Solution {
    public String reverseString(String s) {
        // Write your code here
        return "";
    }
}
""",
            "c": """// Reverse a String
#include <stdio.h>
#include <string.h>

int main() {
    char s[100005];
    if (!fgets(s, sizeof(s), stdin)) return 0;
    
    // --- WRITE YOUR SOLUTION HERE ---
    // Print reversed string
    
    return 0;
}
"""
        },

        "find_duplicate": {
            "python": """# Find Duplicate in an Array
# Given an array of integers, find the duplicate number.

import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    nums = [int(x) for x in data[1:n+1]]

    # --- WRITE YOUR SOLUTION HERE ---
    # Print the duplicate number
    pass

if __name__ == '__main__':
    solve()
""",
            "python_class": """class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        # Write your code here
        pass
""",
            "java": """// Find Duplicate in an Array
import java.util.*;

class Solution {
    public int findDuplicate(int[] nums) {
        // Write your code here
        return 0;
    }
}
""",
            "c": """// Find Duplicate in an Array
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int nums[n];
    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);

    // --- WRITE YOUR SOLUTION HERE ---
    // Print duplicate number
    
    return 0;
}
"""
        },

        "valid_parentheses": {
            "python": """# Valid Parentheses
# Given a string containing '(', ')', '{', '}', '[' and ']',
# determine if the input string is valid.

import sys

def solve():
    s = sys.stdin.read().strip()

    # --- WRITE YOUR SOLUTION HERE ---
    # Print "true" or "false"
    pass

if __name__ == '__main__':
    solve()
""",
            "python_class": """class Solution:
    def isValid(self, s: str) -> bool:
        # Write your code here
        pass
""",
            "java": """// Valid Parentheses
import java.util.*;

class Solution {
    public boolean isValid(String s) {
        // Write your code here
        return false;
    }
}
""",
            "c": """// Valid Parentheses
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

int main() {
    char s[100005];
    if (scanf("%s", s) != 1) return 0;

    // --- WRITE YOUR SOLUTION HERE ---
    // Print "true" or "false"
    
    return 0;
}
"""
        },

        "reverse_linked_list": {
            "python": """# Reverse Linked List
# Reverse a singly linked list.

import sys

def solve():
    data = sys.stdin.read().split()
    if not data or int(data[0]) <= 0:
        return
    n = int(data[0])
    nums = [data[i] for i in range(1, n + 1)]

    # --- WRITE YOUR SOLUTION HERE ---
    # Print space-separated reversed elements
    pass

if __name__ == '__main__':
    solve()
""",
            "python_class": """# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Write your code here
        pass
""",
            "java": """// Reverse Linked List
// Definition for singly-linked list:
// class ListNode {
//     int val;
//     ListNode next;
//     ListNode(int val) { this.val = val; }
// }

class Solution {
    public ListNode reverseList(ListNode head) {
        // Write your code here
        return null;
    }
}
""",
            "c": """// Reverse Linked List
#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;
    int arr[n];
    for (int i = 0; i < n; i++) scanf("%d", &arr[i]);

    // --- WRITE YOUR SOLUTION HERE ---
    // Print space-separated reversed elements
    
    return 0;
}
"""
        },

        # ============================== MEDIUM (5) ==============================
        "longest_substring": {
            "python": """# Longest Substring Without Repeating Characters
# Given a string s, find the length of the longest substring without repeating characters.

import sys

def solve():
    s = sys.stdin.read().rstrip('\\r\\n')

    # --- WRITE YOUR SOLUTION HERE ---
    # Print length of longest substring without duplicates
    pass

if __name__ == '__main__':
    solve()
""",
            "python_class": """class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # Write your code here
        pass
""",
            "java": """// Longest Substring Without Repeating Characters
import java.util.*;

class Solution {
    public int lengthOfLongestSubstring(String s) {
        // Write your code here
        return 0;
    }
}
""",
            "c": """// Longest Substring Without Repeating Characters
#include <stdio.h>
#include <string.h>

int main() {
    char s[100005];
    if (!fgets(s, sizeof(s), stdin)) {
        printf("0\\n");
        return 0;
    }

    // --- WRITE YOUR SOLUTION HERE ---
    // Print length of longest substring
    
    return 0;
}
"""
        },

        "three_sum": {
            "python": """# 3Sum
# Given an integer array nums, return all unique triplets [nums[i], nums[j], nums[k]]
# such that nums[i] + nums[j] + nums[k] == 0.

import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    nums = [int(x) for x in data[1:n+1]]

    # --- WRITE YOUR SOLUTION HERE ---
    # Print each triplet on a new line (space-separated)
    pass

if __name__ == '__main__':
    solve()
""",
            "python_class": """class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # Write your code here
        pass
""",
            "java": """// 3Sum
import java.util.*;

class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        // Write your code here
        return new ArrayList<>();
    }
}
""",
            "c": """// 3Sum
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1 || n < 3) return 0;
    int nums[n];
    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);

    // --- WRITE YOUR SOLUTION HERE ---
    // Print each triplet on a new line
    
    return 0;
}
"""
        },

        "merge_intervals": {
            "python": """# Merge Intervals
# Given an array of intervals, merge all overlapping intervals.

import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    intervals = []
    idx = 1
    for _ in range(n):
        intervals.append([int(data[idx]), int(data[idx+1])])
        idx += 2

    # --- WRITE YOUR SOLUTION HERE ---
    # Print each merged interval start end on a new line
    pass

if __name__ == '__main__':
    solve()
""",
            "python_class": """class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # Write your code here
        pass
""",
            "java": """// Merge Intervals
import java.util.*;

class Solution {
    public int[][] merge(int[][] intervals) {
        // Write your code here
        return new int[][]{};
    }
}
""",
            "c": """// Merge Intervals
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;

    // --- WRITE YOUR SOLUTION HERE ---
    // Print each merged interval
    
    return 0;
}
"""
        },

        "number_of_islands": {
            "python": """# Number of Islands
# Given an m x n 2D binary grid which represents a map of '1's (land) and '0's (water),
# return the number of islands.

import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    m = int(data[0])
    n = int(data[1])
    grid = []
    idx = 2
    for _ in range(m):
        grid.append(list(data[idx:idx+n]))
        idx += n

    # --- WRITE YOUR SOLUTION HERE ---
    # Print count of islands
    pass

if __name__ == '__main__':
    solve()
""",
            "python_class": """class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        # Write your code here
        pass
""",
            "java": """// Number of Islands
import java.util.*;

class Solution {
    public int numIslands(char[][] grid) {
        // Write your code here
        return 0;
    }
}
""",
            "c": """// Number of Islands
#include <stdio.h>

int main() {
    int m, n;
    if (scanf("%d %d", &m, &n) != 2) return 0;
    char grid[m][n];
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            scanf(" %c", &grid[i][j]);
        }
    }

    // --- WRITE YOUR SOLUTION HERE ---
    // Print count of islands
    
    return 0;
}
"""
        },

        "top_k_frequent": {
            "python": """# Top K Frequent Elements
# Given an integer array nums and an integer k, return the k most frequent elements.

import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    k = int(data[1])
    nums = [int(x) for x in data[2:2+n]]

    # --- WRITE YOUR SOLUTION HERE ---
    # Print k most frequent elements space-separated
    pass

if __name__ == '__main__':
    solve()
""",
            "python_class": """class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # Write your code here
        pass
""",
            "java": """// Top K Frequent Elements
import java.util.*;

class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        // Write your code here
        return new int[]{};
    }
}
""",
            "c": """// Top K Frequent Elements
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    int nums[n];
    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);

    // --- WRITE YOUR SOLUTION HERE ---
    // Print k most frequent elements space-separated
    
    return 0;
}
"""
        },

        # ============================== HARD (5) ==============================
        "trapping_rain_water": {
            "python": """# Trapping Rain Water
# Given n non-negative integers representing an elevation map where the width of each bar is 1,
# compute how much water it can trap after raining.

import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    height = [int(x) for x in data[1:n+1]]

    # --- WRITE YOUR SOLUTION HERE ---
    # Print total water trapped
    pass

if __name__ == '__main__':
    solve()
""",
            "python_class": """class Solution:
    def trap(self, height: List[int]) -> int:
        # Write your code here
        pass
""",
            "java": """// Trapping Rain Water
import java.util.*;

class Solution {
    public int trap(int[] height) {
        // Write your code here
        return 0;
    }
}
""",
            "c": """// Trapping Rain Water
#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) {
        printf("0\\n");
        return 0;
    }
    int height[n];
    for (int i = 0; i < n; i++) scanf("%d", &height[i]);

    // --- WRITE YOUR SOLUTION HERE ---
    // Print total water trapped
    
    return 0;
}
"""
        },

        "minimum_window_substring": {
            "python": """# Minimum Window Substring
# Given two strings s and t, return the minimum window substring of s
# such that every character in t (including duplicates) is included in the window.

import sys

def solve():
    lines = sys.stdin.read().splitlines()
    if len(lines) < 2:
        return
    s, t = lines[0].strip(), lines[1].strip()

    # --- WRITE YOUR SOLUTION HERE ---
    # Print minimum window substring
    pass

if __name__ == '__main__':
    solve()
""",
            "python_class": """class Solution:
    def minWindow(self, s: str, t: str) -> str:
        # Write your code here
        pass
""",
            "java": """// Minimum Window Substring
import java.util.*;

class Solution {
    public String minWindow(String s, String t) {
        // Write your code here
        return "";
    }
}
""",
            "c": """// Minimum Window Substring
#include <stdio.h>
#include <string.h>

int main() {
    char s[100005], t[100005];
    if (scanf("%s %s", s, t) != 2) return 0;

    // --- WRITE YOUR SOLUTION HERE ---
    // Print minimum window substring
    
    return 0;
}
"""
        },

        "merge_k_sorted_lists": {
            "python": """# Merge k Sorted Lists
# You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
# Merge all the linked-lists into one sorted linked-list and return it.

import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    k = int(data[0])
    all_nums = []
    idx = 1
    for _ in range(k):
        length = int(data[idx])
        idx += 1
        for _ in range(length):
            all_nums.append(int(data[idx]))
            idx += 1

    # --- WRITE YOUR SOLUTION HERE ---
    # Print all sorted elements space-separated
    pass

if __name__ == '__main__':
    solve()
""",
            "python_class": """# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        # Write your code here
        pass
""",
            "java": """// Merge k Sorted Lists
// Definition for singly-linked list:
// class ListNode {
//     int val;
//     ListNode next;
//     ListNode(int val) { this.val = val; }
// }

class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        // Write your code here
        return null;
    }
}
""",
            "c": """// Merge k Sorted Lists
#include <stdio.h>
#include <stdlib.h>

int main() {
    int k;
    if (scanf("%d", &k) != 1 || k <= 0) return 0;

    // --- WRITE YOUR SOLUTION HERE ---
    // Print all sorted elements space-separated
    
    return 0;
}
"""
        },

        "word_ladder": {
            "python": """# Word Ladder
# Return the number of words in the shortest transformation sequence from beginWord to endWord.

import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    beginWord = data[0]
    endWord = data[1]
    n = int(data[2])
    wordList = data[3:3+n]

    # --- WRITE YOUR SOLUTION HERE ---
    # Print sequence length
    pass

if __name__ == '__main__':
    solve()
""",
            "python_class": """class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        # Write your code here
        pass
""",
            "java": """// Word Ladder
import java.util.*;

class Solution {
    public int ladderLength(String beginWord, String endWord, List<String> wordList) {
        // Write your code here
        return 0;
    }
}
""",
            "c": """// Word Ladder
#include <stdio.h>
#include <string.h>

int main() {
    char begin[105], end[105];
    if (scanf("%s %s", begin, end) != 2) return 0;
    int n; scanf("%d", &n);
    char words[n][105];
    for (int i = 0; i < n; i++) scanf("%s", words[i]);

    // --- WRITE YOUR SOLUTION HERE ---
    // Print sequence length
    
    return 0;
}
"""
        },

        "median_two_sorted_arrays": {
            "python": """# Median of Two Sorted Arrays
# Given two sorted arrays nums1 and nums2 of size m and n respectively,
# return the median of the two sorted arrays.

import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    m = int(data[0])
    n = int(data[1])
    nums1 = [int(x) for x in data[2:2+m]]
    nums2 = [int(x) for x in data[2+m:2+m+n]]

    # --- WRITE YOUR SOLUTION HERE ---
    # Print median as float (e.g. 2.0 or 2.5)
    pass

if __name__ == '__main__':
    solve()
""",
            "python_class": """class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # Write your code here
        pass
""",
            "java": """// Median of Two Sorted Arrays
import java.util.*;

class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        // Write your code here
        return 0.0;
    }
}
""",
            "c": """// Median of Two Sorted Arrays
#include <stdio.h>

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    int a[n], b[m];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 0; i < m; i++) scanf("%d", &b[i]);

    // --- WRITE YOUR SOLUTION HERE ---
    // Print median as float
    
    return 0;
}
"""
        }
    }

    @classmethod
    def get_starter_code(cls, problem_id: str) -> Dict[str, str]:
        """Returns map of language -> starter code string for a problem."""
        clean_id = (problem_id or "").strip().lower()
        return cls.STARTER_TEMPLATES.get(clean_id, {})

    @classmethod
    def has_standalone_main(cls, language: str, code: str) -> bool:
        """Determines if the submitted code already contains its own main / top-level runner."""
        lang = language.lower()
        if lang in ["python", "python3", "py", "python_normal", "python_script", "python_class", "python_leetcode"]:
            if "__run_test()" in code:
                return True
            if "class Solution" not in code:
                return True
            if "__name__ == '__main__'" in code or '__name__ == "__main__"' in code:
                return True
            return False
        elif lang == "java":
            if "public class MainRunner" in code:
                return True
            return bool(re.search(r'\bpublic\s+static\s+void\s+main\s*\(', code))
        elif lang in ["c", "c99", "c11"]:
            return bool(re.search(r'\bint\s+main\s*\(', code) or re.search(r'\bvoid\s+main\s*\(', code))
        return False

    @classmethod
    def wrap_code(cls, language: str, problem_id: str, user_code: str) -> str:
        """Wraps pure LeetCode class Solution / function code with problem IO harness."""
        if cls.has_standalone_main(language, user_code):
            return user_code

        clean_id = (problem_id or "").strip().lower()
        lang = language.lower()

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
        String s = sc.hasNextLine() ? sc.nextLine().replaceAll("[\\\\r\\\\n]", "") : "";
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
        String s = sc.hasNext() ? sc.next().trim() : "";
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
        if (n <= 0) return;
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
        String s = sc.hasNextLine() ? sc.nextLine().replaceAll("[\\\\r\\\\n]", "") : "";
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
    s = sys.stdin.read().rstrip('\\r\\n')
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
    s = sys.stdin.read().rstrip('\\r\\n')
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

        if not harness:
            return user_code
        return prefix + "\n" + user_code + "\n" + harness

    # ------------------- C WRAPPERS -------------------

    @classmethod
    def _wrap_c(cls, pid: str, user_code: str) -> str:
        # If user provided a complete main() function, use it directly
        return user_code
