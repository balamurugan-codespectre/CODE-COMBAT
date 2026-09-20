"""
CODE COMBAT Pro - LeetCode Driver Harness Engine
Provides authentic LeetCode class Solution starter templates and auto-wrapping IO drivers
for Java, Python 3, and C.
"""

import re
from typing import Dict, Any, Optional


class Harness:
    """Manages LeetCode starter templates and compiles auto-wrapping IO harnesses."""

    STARTER_TEMPLATES = {
        # ------------------- SET 1 -------------------
        "two_sum": {
            "java": """class Solution {
    public int[] twoSum(int[] nums, int target) {
        
    }
}""",
            "python": """class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        pass""",
            "c": """/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    
}"""
        },
        "palindrome_number": {
            "java": """class Solution {
    public boolean isPalindrome(int x) {
        
    }
}""",
            "python": """class Solution:
    def isPalindrome(self, x: int) -> bool:
        pass""",
            "c": """bool isPalindrome(int x) {
    
}"""
        },
        "reverse_string": {
            "java": """class Solution {
    public String reverseString(String s) {
        
    }
}""",
            "python": """class Solution:
    def reverseString(self, s: str) -> str:
        pass""",
            "c": """char* reverseString(char* s) {
    
}"""
        },
        "count_vowels": {
            "java": """class Solution {
    public int countVowels(String s) {
        
    }
}""",
            "python": """class Solution:
    def countVowels(self, s: str) -> int:
        pass""",
            "c": """int countVowels(char* s) {
    
}"""
        },
        "find_maximum": {
            "java": """class Solution {
    public int findMax(int[] nums) {
        
    }
}""",
            "python": """class Solution:
    def findMax(self, nums: List[int]) -> int:
        pass""",
            "c": """int findMax(int* nums, int numsSize) {
    
}"""
        },
        "maximum_subarray": {
            "java": """class Solution {
    public int maxSubArray(int[] nums) {
        
    }
}""",
            "python": """class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        pass""",
            "c": """int maxSubArray(int* nums, int numsSize) {
    
}"""
        },
        "longest_substring": {
            "java": """class Solution {
    public int lengthOfLongestSubstring(String s) {
        
    }
}""",
            "python": """class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        pass""",
            "c": """int lengthOfLongestSubstring(char* s) {
    
}"""
        },
        "valid_parentheses": {
            "java": """class Solution {
    public boolean isValid(String s) {
        
    }
}""",
            "python": """class Solution:
    def isValid(self, s: str) -> bool:
        pass""",
            "c": """bool isValid(char* s) {
    
}"""
        },
        "merge_intervals": {
            "java": """class Solution {
    public int[][] merge(int[][] intervals) {
        
    }
}""",
            "python": """class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        pass""",
            "c": """int** merge(int** intervals, int intervalsSize, int* intervalsColSize, int* returnSize, int** returnColumnSizes) {
    
}"""
        },
        "rotate_array": {
            "java": """class Solution {
    public void rotate(int[] nums, int k) {
        
    }
}""",
            "python": """class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        pass""",
            "c": """void rotate(int* nums, int numsSize, int k) {
    
}"""
        },
        "binary_tree": {
            "java": """class Solution {
    public List<List<Integer>> levelOrder(int[] tree) {
        
    }
}""",
            "python": """class Solution:
    def levelOrder(self, tree: List[int]) -> List[List[int]]:
        pass""",
            "c": """void levelOrder(int* tree, int treeSize) {
    
}"""
        },
        "dijkstra_algorithm": {
            "java": """class Solution {
    public int[] dijkstra(int n, int[][] edges, int start) {
        
    }
}""",
            "python": """class Solution:
    def dijkstra(self, n: int, edges: List[List[int]], start: int) -> List[int]:
        pass""",
            "c": """int* dijkstra(int n, int edgesCount, int** edges, int start) {
    
}"""
        },
        "n_queens": {
            "java": """class Solution {
    public int totalNQueens(int n) {
        
    }
}""",
            "python": """class Solution:
    def totalNQueens(self, n: int) -> int:
        pass""",
            "c": """int totalNQueens(int n) {
    
}"""
        },
        "shortest_path": {
            "java": """class Solution {
    public int shortestPath(int n, int[][] edges, int start, int end) {
        
    }
}""",
            "python": """class Solution:
    def shortestPath(self, n: int, edges: List[List[int]], start: int, end: int) -> int:
        pass""",
            "c": """int shortestPath(int n, int edgesCount, int** edges, int start, int end) {
    
}"""
        },
        "word_ladder": {
            "java": """class Solution {
    public int ladderLength(String beginWord, String endWord, List<String> wordList) {
        
    }
}""",
            "python": """class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        pass""",
            "c": """int ladderLength(char* beginWord, char* endWord, char** wordList, int wordListSize) {
    
}"""
        },

        # ------------------- SET 2 -------------------
        "climbing_stairs": {
            "java": """class Solution {
    public int climbStairs(int n) {
        
    }
}""",
            "python": """class Solution:
    def climbStairs(self, n: int) -> int:
        pass""",
            "c": """int climbStairs(int n) {
    
}"""
        },
        "majority_element": {
            "java": """class Solution {
    public int majorityElement(int[] nums) {
        
    }
}""",
            "python": """class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        pass""",
            "c": """int majorityElement(int* nums, int numsSize) {
    
}"""
        },
        "reverse_words": {
            "java": """class Solution {
    public String reverseWords(String s) {
        
    }
}""",
            "python": """class Solution:
    def reverseWords(self, s: str) -> str:
        pass""",
            "c": """char* reverseWords(char* s) {
    
}"""
        },
        "single_number": {
            "java": """class Solution {
    public int singleNumber(int[] nums) {
        
    }
}""",
            "python": """class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        pass""",
            "c": """int singleNumber(int* nums, int numsSize) {
    
}"""
        },
        "coin_change": {
            "java": """class Solution {
    public int coinChange(int[] coins, int amount) {
        
    }
}""",
            "python": """class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        pass""",
            "c": """int coinChange(int* coins, int coinsSize, int amount) {
    
}"""
        },
        "container_with_most_water": {
            "java": """class Solution {
    public int maxArea(int[] height) {
        
    }
}""",
            "python": """class Solution:
    def maxArea(self, height: List[int]) -> int:
        pass""",
            "c": """int maxArea(int* height, int heightSize) {
    
}"""
        },
        "group_anagrams": {
            "java": """class Solution {
    public int groupAnagrams(String[] strs) {
        
    }
}""",
            "python": """class Solution:
    def groupAnagrams(self, strs: List[str]) -> int:
        pass""",
            "c": """int groupAnagrams(char** strs, int strsSize) {
    
}"""
        },
        "rotate_matrix": {
            "java": """class Solution {
    public void rotate(int[][] matrix) {
        
    }
}""",
            "python": """class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        pass""",
            "c": """void rotate(int** matrix, int matrixSize, int* matrixColSize) {
    
}"""
        },
        "longest_valid_parentheses": {
            "java": """class Solution {
    public int longestValidParentheses(String s) {
        
    }
}""",
            "python": """class Solution:
    def longestValidParentheses(self, s: str) -> int:
        pass""",
            "c": """int longestValidParentheses(char* s) {
    
}"""
        },
        "median_two_sorted_arrays": {
            "java": """class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        
    }
}""",
            "python": """class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        pass""",
            "c": """double findMedianSortedArrays(int* nums1, int nums1Size, int* nums2, int nums2Size) {
    
}"""
        },
        "merge_k_sorted_lists": {
            "java": """class Solution {
    public int[] mergeKLists(int[][] lists) {
        
    }
}""",
            "python": """class Solution:
    def mergeKLists(self, lists: List[List[int]]) -> List[int]:
        pass""",
            "c": """int* mergeKLists(int** lists, int listsSize, int* listsColSize, int* returnSize) {
    
}"""
        },
        "trapping_rain_water": {
            "java": """class Solution {
    public int trap(int[] height) {
        
    }
}""",
            "python": """class Solution:
    def trap(self, height: List[int]) -> int:
        pass""",
            "c": """int trap(int* height, int heightSize) {
    
}"""
        },
        "word_break": {
            "java": """class Solution {
    public boolean wordBreak(String s, List<String> wordDict) {
        
    }
}""",
            "python": """class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        pass""",
            "c": """bool wordBreak(char* s, char** wordDict, int wordDictSize) {
    
}"""
        }
    }

    @classmethod
    def get_starter_code(cls, problem_id: str) -> Dict[str, str]:
        clean_id = (problem_id or "").strip().lower()
        if clean_id in cls.STARTER_TEMPLATES:
            return cls.STARTER_TEMPLATES[clean_id]
        return {
            "java": "class Solution {\\n    // Write your solution here\\n}",
            "python": "class Solution:\\n    # Write your solution here\\n    pass",
            "c": "// Write your solution here"
        }

    @classmethod
    def has_standalone_main(cls, language: str, code: str) -> bool:
        """Determines if the submission contains its own IO driver / main method."""
        lang = language.lower()
        if lang in ["java"]:
            return bool(re.search(r'public\s+static\s+void\s+main', code) or re.search(r'static\s+void\s+main', code))
        elif lang in ["python", "python3", "py"]:
            return bool("__main__" in code or "sys.stdin" in code or re.search(r'\binput\s*\(', code))
        elif lang in ["c", "c99", "c11"]:
            return bool(re.search(r'\bint\s+main\s*\(', code) or re.search(r'\bvoid\s+main\s*\(', code))
        return False

    @classmethod
    def wrap_code(cls, language: str, problem_id: str, user_code: str) -> str:
        """
        Wraps pure LeetCode class Solution / function code with problem IO harness.
        If user code already contains its own main(), returns user_code directly.
        """
        if cls.has_standalone_main(language, user_code):
            return user_code

        clean_id = (problem_id or "").strip().lower()
        lang = language.lower()

        if lang == "java":
            return cls._wrap_java(clean_id, user_code)
        elif lang in ["python", "python3", "py"]:
            return cls._wrap_python(clean_id, user_code)
        elif lang in ["c", "c99", "c11"]:
            return cls._wrap_c(clean_id, user_code)
        return user_code

    # ------------------- JAVA WRAPPERS -------------------

    @classmethod
    def _wrap_java(cls, pid: str, user_code: str) -> str:
        # If user wrote "public class Solution", make it non-public so MainRunner can be public
        clean_code = re.sub(r'public\s+class\s+Solution', 'class Solution', user_code)
        
        prefix = """import java.util.*;
import java.io.*;
import java.math.*;

"""
        # Specific problem harness
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
}
"""
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
}
"""
        elif pid == "reverse_string":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNext() ? sc.next() : "";
        Solution sol = new Solution();
        System.out.println(sol.reverseString(s));
    }
}
"""
        elif pid == "count_vowels":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNextLine() ? sc.nextLine().trim() : "";
        Solution sol = new Solution();
        System.out.println(sol.countVowels(s));
    }
}
"""
        elif pid == "find_maximum":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.findMax(nums));
    }
}
"""
        elif pid == "maximum_subarray":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.maxSubArray(nums));
    }
}
"""
        elif pid == "longest_substring":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNextLine() ? sc.nextLine().trim() : "";
        Solution sol = new Solution();
        System.out.println(sol.lengthOfLongestSubstring(s));
    }
}
"""
        elif pid == "valid_parentheses":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNext() ? sc.next().trim() : "";
        Solution sol = new Solution();
        System.out.println(sol.isValid(s) ? "true" : "false");
    }
}
"""
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
            for (int[] inv : res) {
                System.out.println(inv[0] + " " + inv[1]);
            }
        }
    }
}
"""
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
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            sb.append(nums[i]).append(i == n - 1 ? "" : " ");
        }
        System.out.println(sb.toString());
    }
}
"""
        elif pid == "binary_tree":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] tree = new int[n];
        for (int i = 0; i < n; i++) tree[i] = sc.nextInt();
        Solution sol = new Solution();
        List<List<Integer>> res = sol.levelOrder(tree);
        if (res != null) {
            for (List<Integer> level : res) {
                for (int i = 0; i < level.size(); i++) {
                    System.out.print(level.get(i) + (i == level.size() - 1 ? "" : " "));
                }
                System.out.println();
            }
        }
    }
}
"""
        elif pid == "dijkstra_algorithm":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int v = sc.nextInt();
        int e = sc.nextInt();
        int s = sc.nextInt();
        int[][] edges = new int[e][3];
        for (int i = 0; i < e; i++) {
            edges[i][0] = sc.nextInt();
            edges[i][1] = sc.nextInt();
            edges[i][2] = sc.nextInt();
        }
        Solution sol = new Solution();
        int[] dist = sol.dijkstra(v, edges, s);
        if (dist != null) {
            for (int i = 0; i < v; i++) {
                System.out.print(dist[i] + (i == v - 1 ? "" : " "));
            }
            System.out.println();
        }
    }
}
"""
        elif pid == "n_queens":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.totalNQueens(n));
    }
}
"""
        elif pid == "shortest_path":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int v = sc.nextInt();
        int e = sc.nextInt();
        int s = sc.nextInt();
        int d = sc.nextInt();
        int[][] edges = new int[e][2];
        for (int i = 0; i < e; i++) {
            edges[i][0] = sc.nextInt();
            edges[i][1] = sc.nextInt();
        }
        Solution sol = new Solution();
        System.out.println(sol.shortestPath(v, edges, s, d));
    }
}
"""
        elif pid == "word_ladder":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNext()) return;
        String beginWord = sc.next();
        String endWord = sc.next();
        int n = sc.nextInt();
        List<String> wordList = new ArrayList<>();
        for (int i = 0; i < n; i++) wordList.add(sc.next());
        Solution sol = new Solution();
        System.out.println(sol.ladderLength(beginWord, endWord, wordList));
    }
}
"""
        elif pid == "climbing_stairs":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.climbStairs(n));
    }
}
"""
        elif pid == "majority_element":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.majorityElement(nums));
    }
}
"""
        elif pid == "reverse_words":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNextLine() ? sc.nextLine().trim() : "";
        Solution sol = new Solution();
        System.out.println(sol.reverseWords(s));
    }
}
"""
        elif pid == "single_number":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.singleNumber(nums));
    }
}
"""
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
}
"""
        elif pid == "container_with_most_water":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] height = new int[n];
        for (int i = 0; i < n; i++) height[i] = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.maxArea(height));
    }
}
"""
        elif pid == "group_anagrams":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        String[] strs = new String[n];
        for (int i = 0; i < n; i++) strs[i] = sc.next();
        Solution sol = new Solution();
        System.out.println(sol.groupAnagrams(strs));
    }
}
"""
        elif pid == "rotate_matrix":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[][] matrix = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) matrix[i][j] = sc.nextInt();
        }
        Solution sol = new Solution();
        sol.rotate(matrix);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                System.out.print(matrix[i][j] + (j == n - 1 ? "" : " "));
            }
            System.out.println();
        }
    }
}
"""
        elif pid == "longest_valid_parentheses":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNext() ? sc.next().trim() : "";
        Solution sol = new Solution();
        System.out.println(sol.longestValidParentheses(s));
    }
}
"""
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
}
"""
        elif pid == "merge_k_sorted_lists":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int k = sc.nextInt();
        int[][] lists = new int[k][];
        for (int i = 0; i < k; i++) {
            int len = sc.nextInt();
            lists[i] = new int[len];
            for (int j = 0; j < len; j++) lists[i][j] = sc.nextInt();
        }
        Solution sol = new Solution();
        int[] res = sol.mergeKLists(lists);
        if (res != null) {
            for (int i = 0; i < res.length; i++) {
                System.out.print(res[i] + (i == res.length - 1 ? "" : " "));
            }
            System.out.println();
        }
    }
}
"""
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
}
"""
        elif pid == "word_break":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNext()) return;
        String s = sc.next();
        int n = sc.nextInt();
        List<String> wordDict = new ArrayList<>();
        for (int i = 0; i < n; i++) wordDict.add(sc.next());
        Solution sol = new Solution();
        System.out.println(sol.wordBreak(s, wordDict) ? "true" : "false");
    }
}
"""
        else:
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Solution sol = new Solution();
    }
}
"""
        return prefix + clean_code + "\n" + harness

    # ------------------- PYTHON WRAPPERS -------------------

    @classmethod
    def _wrap_python(cls, pid: str, user_code: str) -> str:
        prefix = """import sys
import math
import collections
import heapq
import bisect
from typing import List, Dict, Set, Optional, Tuple

"""
        if pid == "two_sum":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _n = int(_data[0])
        _nums = [int(x) for x in _data[1:_n+1]]
        _target = int(_data[_n+1])
        _sol = Solution()
        _res = _sol.twoSum(_nums, _target)
        if _res:
            print(f"{_res[0]} {_res[1]}")
"""
        elif pid == "palindrome_number":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _x = int(_data[0])
        _sol = Solution()
        print("true" if _sol.isPalindrome(_x) else "false")
"""
        elif pid == "reverse_string":
            harness = """
if __name__ == '__main__':
    _s = sys.stdin.read().strip()
    if _s is not None:
        _sol = Solution()
        print(_sol.reverseString(_s))
"""
        elif pid == "count_vowels":
            harness = """
if __name__ == '__main__':
    _s = sys.stdin.read().rstrip('\\r\\n')
    _sol = Solution()
    print(_sol.countVowels(_s))
"""
        elif pid == "find_maximum":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _n = int(_data[0])
        _nums = [int(x) for x in _data[1:_n+1]]
        _sol = Solution()
        print(_sol.findMax(_nums))
"""
        elif pid == "maximum_subarray":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _n = int(_data[0])
        _nums = [int(x) for x in _data[1:_n+1]]
        _sol = Solution()
        print(_sol.maxSubArray(_nums))
"""
        elif pid == "longest_substring":
            harness = """
if __name__ == '__main__':
    _s = sys.stdin.read().strip()
    _sol = Solution()
    print(_sol.lengthOfLongestSubstring(_s))
"""
        elif pid == "valid_parentheses":
            harness = """
if __name__ == '__main__':
    _s = sys.stdin.read().strip()
    _sol = Solution()
    print("true" if _sol.isValid(_s) else "false")
"""
        elif pid == "merge_intervals":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _n = int(_data[0])
        _invs = []
        _idx = 1
        for _ in range(_n):
            _invs.append([int(_data[_idx]), int(_data[_idx+1])])
            _idx += 2
        _sol = Solution()
        _res = _sol.merge(_invs)
        if _res:
            for _iv in _res:
                print(f"{_iv[0]} {_iv[1]}")
"""
        elif pid == "rotate_array":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _n = int(_data[0])
        _k = int(_data[1])
        _nums = [int(x) for x in _data[2:_n+2]]
        _sol = Solution()
        _sol.rotate(_nums, _k)
        print(" ".join(str(x) for x in _nums))
"""
        elif pid == "binary_tree":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _n = int(_data[0])
        _tree = [int(x) for x in _data[1:_n+1]]
        _sol = Solution()
        _res = _sol.levelOrder(_tree)
        if _res:
            for _lvl in _res:
                print(" ".join(str(x) for x in _lvl))
"""
        elif pid == "dijkstra_algorithm":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _v = int(_data[0])
        _e = int(_data[1])
        _s = int(_data[2])
        _edges = []
        _idx = 3
        for _ in range(_e):
            _edges.append([int(_data[_idx]), int(_data[_idx+1]), int(_data[_idx+2])])
            _idx += 3
        _sol = Solution()
        _dist = _sol.dijkstra(_v, _edges, _s)
        if _dist is not None:
            print(" ".join(str(x) for x in _dist))
"""
        elif pid == "n_queens":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _n = int(_data[0])
        _sol = Solution()
        print(_sol.totalNQueens(_n))
"""
        elif pid == "shortest_path":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _v = int(_data[0])
        _e = int(_data[1])
        _s = int(_data[2])
        _d = int(_data[3])
        _edges = []
        _idx = 4
        for _ in range(_e):
            _edges.append([int(_data[_idx]), int(_data[_idx+1])])
            _idx += 2
        _sol = Solution()
        print(_sol.shortestPath(_v, _edges, _s, _d))
"""
        elif pid == "word_ladder":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _begin = _data[0]
        _end = _data[1]
        _n = int(_data[2])
        _wlist = _data[3:3+_n]
        _sol = Solution()
        print(_sol.ladderLength(_begin, _end, _wlist))
"""
        elif pid == "climbing_stairs":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _n = int(_data[0])
        _sol = Solution()
        print(_sol.climbStairs(_n))
"""
        elif pid == "majority_element":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _n = int(_data[0])
        _nums = [int(x) for x in _data[1:_n+1]]
        _sol = Solution()
        print(_sol.majorityElement(_nums))
"""
        elif pid == "reverse_words":
            harness = """
if __name__ == '__main__':
    _s = sys.stdin.read().strip()
    if _s:
        _sol = Solution()
        print(_sol.reverseWords(_s))
"""
        elif pid == "single_number":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _n = int(_data[0])
        _nums = [int(x) for x in _data[1:_n+1]]
        _sol = Solution()
        print(_sol.singleNumber(_nums))
"""
        elif pid == "coin_change":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _n = int(_data[0])
        _amt = int(_data[1])
        _coins = [int(x) for x in _data[2:_n+2]]
        _sol = Solution()
        print(_sol.coinChange(_coins, _amt))
"""
        elif pid == "container_with_most_water":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _n = int(_data[0])
        _height = [int(x) for x in _data[1:_n+1]]
        _sol = Solution()
        print(_sol.maxArea(_height))
"""
        elif pid == "group_anagrams":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _n = int(_data[0])
        _strs = _data[1:_n+1]
        _sol = Solution()
        print(_sol.groupAnagrams(_strs))
"""
        elif pid == "rotate_matrix":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _n = int(_data[0])
        _mat = []
        _idx = 1
        for _ in range(_n):
            _mat.append([int(x) for x in _data[_idx:_idx+_n]])
            _idx += _n
        _sol = Solution()
        _sol.rotate(_mat)
        for _row in _mat:
            print(" ".join(str(x) for x in _row))
"""
        elif pid == "longest_valid_parentheses":
            harness = """
if __name__ == '__main__':
    _s = sys.stdin.read().strip()
    _sol = Solution()
    print(_sol.longestValidParentheses(_s))
"""
        elif pid == "median_two_sorted_arrays":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _m = int(_data[0])
        _n = int(_data[1])
        _nums1 = [int(x) for x in _data[2:2+_m]]
        _nums2 = [int(x) for x in _data[2+_m:2+_m+_n]]
        _sol = Solution()
        _res = _sol.findMedianSortedArrays(_nums1, _nums2)
        print(f"{_res:.1f}")
"""
        elif pid == "merge_k_sorted_lists":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _k = int(_data[0])
        _lists = []
        _idx = 1
        for _ in range(_k):
            _len = int(_data[_idx])
            _lists.append([int(x) for x in _data[_idx+1:_idx+1+_len]])
            _idx += 1 + _len
        _sol = Solution()
        _res = _sol.mergeKLists(_lists)
        if _res is not None:
            print(" ".join(str(x) for x in _res))
"""
        elif pid == "trapping_rain_water":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _n = int(_data[0])
        _height = [int(x) for x in _data[1:_n+1]]
        _sol = Solution()
        print(_sol.trap(_height))
"""
        elif pid == "word_break":
            harness = """
if __name__ == '__main__':
    _data = sys.stdin.read().split()
    if _data:
        _s = _data[0]
        _n = int(_data[1])
        _wdict = _data[2:2+_n]
        _sol = Solution()
        print("true" if _sol.wordBreak(_s, _wdict) else "false")
"""
        else:
            harness = """
if __name__ == '__main__':
    _sol = Solution()
"""
        return prefix + user_code + "\n" + harness

    # ------------------- C WRAPPERS -------------------

    @classmethod
    def _wrap_c(cls, pid: str, user_code: str) -> str:
        prefix = """#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

"""
        if pid == "two_sum":
            harness = """
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int *nums = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);
    int target;
    scanf("%d", &target);
    int retSize = 0;
    int *res = twoSum(nums, n, target, &retSize);
    if (res && retSize >= 2) {
        printf("%d %d\\n", res[0], res[1]);
        free(res);
    }
    free(nums);
    return 0;
}
"""
        elif pid == "palindrome_number":
            harness = """
int main() {
    int x;
    if (scanf("%d", &x) != 1) return 0;
    printf("%s\\n", isPalindrome(x) ? "true" : "false");
    return 0;
}
"""
        elif pid == "reverse_string":
            harness = """
int main() {
    char buf[100005];
    if (scanf("%s", buf) != 1) return 0;
    char* res = reverseString(buf);
    printf("%s\\n", res ? res : buf);
    return 0;
}
"""
        elif pid == "count_vowels":
            harness = """
int main() {
    char buf[100005];
    if (!fgets(buf, sizeof(buf), stdin)) return 0;
    buf[strcspn(buf, "\\r\\n")] = 0;
    printf("%d\\n", countVowels(buf));
    return 0;
}
"""
        elif pid == "find_maximum":
            harness = """
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int *nums = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);
    printf("%d\\n", findMax(nums, n));
    free(nums);
    return 0;
}
"""
        elif pid == "maximum_subarray":
            harness = """
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int *nums = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);
    printf("%d\\n", maxSubArray(nums, n));
    free(nums);
    return 0;
}
"""
        elif pid == "longest_substring":
            harness = """
int main() {
    char buf[100005];
    if (scanf("%s", buf) != 1) {
        printf("0\\n");
        return 0;
    }
    printf("%d\\n", lengthOfLongestSubstring(buf));
    return 0;
}
"""
        elif pid == "valid_parentheses":
            harness = """
int main() {
    char buf[100005];
    if (scanf("%s", buf) != 1) return 0;
    printf("%s\\n", isValid(buf) ? "true" : "false");
    return 0;
}
"""
        elif pid == "merge_intervals":
            harness = """
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int **intervals = (int**)malloc(n * sizeof(int*));
    int *colSize = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) {
        intervals[i] = (int*)malloc(2 * sizeof(int));
        colSize[i] = 2;
        scanf("%d %d", &intervals[i][0], &intervals[i][1]);
    }
    int retSize = 0;
    int *retColSizes = NULL;
    int **res = merge(intervals, n, colSize, &retSize, &retColSizes);
    if (res) {
        for (int i = 0; i < retSize; i++) {
            printf("%d %d\\n", res[i][0], res[i][1]);
            free(res[i]);
        }
        free(res);
    }
    for (int i = 0; i < n; i++) free(intervals[i]);
    free(intervals);
    free(colSize);
    return 0;
}
"""
        elif pid == "rotate_array":
            harness = """
int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    int *nums = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);
    rotate(nums, n, k);
    for (int i = 0; i < n; i++) {
        printf("%d%s", nums[i], i == n - 1 ? "" : " ");
    }
    printf("\\n");
    free(nums);
    return 0;
}
"""
        elif pid == "binary_tree":
            harness = """
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int *tree = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) scanf("%d", &tree[i]);
    levelOrder(tree, n);
    free(tree);
    return 0;
}
"""
        elif pid == "dijkstra_algorithm":
            harness = """
int main() {
    int v, e, s;
    if (scanf("%d %d %d", &v, &e, &s) != 3) return 0;
    int **edges = (int**)malloc(e * sizeof(int*));
    for (int i = 0; i < e; i++) {
        edges[i] = (int*)malloc(3 * sizeof(int));
        scanf("%d %d %d", &edges[i][0], &edges[i][1], &edges[i][2]);
    }
    int *dist = dijkstra(v, e, edges, s);
    if (dist) {
        for (int i = 0; i < v; i++) {
            printf("%d%s", dist[i], i == v - 1 ? "" : " ");
        }
        printf("\\n");
        free(dist);
    }
    for (int i = 0; i < e; i++) free(edges[i]);
    free(edges);
    return 0;
}
"""
        elif pid == "n_queens":
            harness = """
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    printf("%d\\n", totalNQueens(n));
    return 0;
}
"""
        elif pid == "shortest_path":
            harness = """
int main() {
    int v, e, s, d;
    if (scanf("%d %d %d %d", &v, &e, &s, &d) != 4) return 0;
    int **edges = (int**)malloc(e * sizeof(int*));
    for (int i = 0; i < e; i++) {
        edges[i] = (int*)malloc(2 * sizeof(int));
        scanf("%d %d", &edges[i][0], &edges[i][1]);
    }
    printf("%d\\n", shortestPath(v, e, edges, s, d));
    for (int i = 0; i < e; i++) free(edges[i]);
    free(edges);
    return 0;
}
"""
        elif pid == "word_ladder":
            harness = """
int main() {
    char beginWord[100], endWord[100];
    if (scanf("%s %s", beginWord, endWord) != 2) return 0;
    int n;
    scanf("%d", &n);
    char **wordList = (char**)malloc(n * sizeof(char*));
    for (int i = 0; i < n; i++) {
        wordList[i] = (char*)malloc(100 * sizeof(char));
        scanf("%s", wordList[i]);
    }
    printf("%d\\n", ladderLength(beginWord, endWord, wordList, n));
    for (int i = 0; i < n; i++) free(wordList[i]);
    free(wordList);
    return 0;
}
"""
        elif pid == "climbing_stairs":
            harness = """
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    printf("%d\\n", climbStairs(n));
    return 0;
}
"""
        elif pid == "majority_element":
            harness = """
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int *nums = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);
    printf("%d\\n", majorityElement(nums, n));
    free(nums);
    return 0;
}
"""
        elif pid == "reverse_words":
            harness = """
int main() {
    char buf[100005];
    if (!fgets(buf, sizeof(buf), stdin)) return 0;
    buf[strcspn(buf, "\\r\\n")] = 0;
    char *res = reverseWords(buf);
    printf("%s\\n", res ? res : buf);
    return 0;
}
"""
        elif pid == "single_number":
            harness = """
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int *nums = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);
    printf("%d\\n", singleNumber(nums, n));
    free(nums);
    return 0;
}
"""
        elif pid == "coin_change":
            harness = """
int main() {
    int n, amount;
    if (scanf("%d %d", &n, &amount) != 2) return 0;
    int *coins = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) scanf("%d", &coins[i]);
    printf("%d\\n", coinChange(coins, n, amount));
    free(coins);
    return 0;
}
"""
        elif pid == "container_with_most_water":
            harness = """
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int *height = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) scanf("%d", &height[i]);
    printf("%d\\n", maxArea(height, n));
    free(height);
    return 0;
}
"""
        elif pid == "group_anagrams":
            harness = """
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    char **strs = (char**)malloc(n * sizeof(char*));
    for (int i = 0; i < n; i++) {
        strs[i] = (char*)malloc(100 * sizeof(char));
        scanf("%s", strs[i]);
    }
    printf("%d\\n", groupAnagrams(strs, n));
    for (int i = 0; i < n; i++) free(strs[i]);
    free(strs);
    return 0;
}
"""
        elif pid == "rotate_matrix":
            harness = """
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int **matrix = (int**)malloc(n * sizeof(int*));
    int *colSize = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) {
        matrix[i] = (int*)malloc(n * sizeof(int));
        colSize[i] = n;
        for (int j = 0; j < n; j++) scanf("%d", &matrix[i][j]);
    }
    rotate(matrix, n, colSize);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            printf("%d%s", matrix[i][j], j == n - 1 ? "" : " ");
        }
        printf("\\n");
    }
    for (int i = 0; i < n; i++) free(matrix[i]);
    free(matrix);
    free(colSize);
    return 0;
}
"""
        elif pid == "longest_valid_parentheses":
            harness = """
int main() {
    char buf[100005];
    if (scanf("%s", buf) != 1) return 0;
    printf("%d\\n", longestValidParentheses(buf));
    return 0;
}
"""
        elif pid == "median_two_sorted_arrays":
            harness = """
int main() {
    int m, n;
    if (scanf("%d %d", &m, &n) != 2) return 0;
    int *nums1 = (int*)malloc((m > 0 ? m : 1) * sizeof(int));
    for (int i = 0; i < m; i++) scanf("%d", &nums1[i]);
    int *nums2 = (int*)malloc((n > 0 ? n : 1) * sizeof(int));
    for (int i = 0; i < n; i++) scanf("%d", &nums2[i]);
    printf("%.1f\\n", findMedianSortedArrays(nums1, m, nums2, n));
    free(nums1);
    free(nums2);
    return 0;
}
"""
        elif pid == "merge_k_sorted_lists":
            harness = """
int main() {
    int k;
    if (scanf("%d", &k) != 1) return 0;
    int **lists = (int**)malloc(k * sizeof(int*));
    int *colSize = (int*)malloc(k * sizeof(int));
    for (int i = 0; i < k; i++) {
        scanf("%d", &colSize[i]);
        lists[i] = (int*)malloc(colSize[i] * sizeof(int));
        for (int j = 0; j < colSize[i]; j++) scanf("%d", &lists[i][j]);
    }
    int retSize = 0;
    int *res = mergeKLists(lists, k, colSize, &retSize);
    if (res) {
        for (int i = 0; i < retSize; i++) {
            printf("%d%s", res[i], i == retSize - 1 ? "" : " ");
        }
        printf("\\n");
        free(res);
    }
    for (int i = 0; i < k; i++) free(lists[i]);
    free(lists);
    free(colSize);
    return 0;
}
"""
        elif pid == "trapping_rain_water":
            harness = """
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int *height = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) scanf("%d", &height[i]);
    printf("%d\\n", trap(height, n));
    free(height);
    return 0;
}
"""
        elif pid == "word_break":
            harness = """
int main() {
    char s[1005];
    if (scanf("%s", s) != 1) return 0;
    int n;
    scanf("%d", &n);
    char **wordDict = (char**)malloc(n * sizeof(char*));
    for (int i = 0; i < n; i++) {
        wordDict[i] = (char*)malloc(1005 * sizeof(char));
        scanf("%s", wordDict[i]);
    }
    printf("%s\\n", wordBreak(s, wordDict, n) ? "true" : "false");
    for (int i = 0; i < n; i++) free(wordDict[i]);
    free(wordDict);
    return 0;
}
"""
        else:
            harness = """
int main() {
    return 0;
}
"""
        return prefix + user_code + "\n" + harness