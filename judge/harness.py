"""
CODE COMBAT Pro - LeetCode Driver Harness Engine
Provides authentic LeetCode class Solution starter templates and auto-wrapping IO drivers
for Java, Python 3, and C.
"""

import re
from typing import Dict, Any, Optional


class Harness:
    """Manages LeetCode starter templates and compiles auto-wrapping IO harnesses."""

    STARTER_TEMPLATES = {'two_sum': {'python': '# Two Sum\n# Given an array of integers and a target, print the two indices that add up to target.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:n+1]]\n    target = int(data[n+1])\n    \n    # --- WRITE YOUR SOLUTION HERE ---\n    # Find indices i and j such that nums[i] + nums[j] == target\n    \n    # Example: print(f"{i} {j}")\n\nif __name__ == \'__main__\':\n    solve()\n', 'java': '// Two Sum\n// Given an array of integers and a target, print the two indices that add up to target.\n\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int n = sc.nextInt();\n        int[] nums = new int[n];\n        for (int i = 0; i < n; i++) {\n            nums[i] = sc.nextInt();\n        }\n        int target = sc.nextInt();\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Find indices i and j such that nums[i] + nums[j] == target\n        \n\n        // Example: System.out.println(i + " " + j);\n    }\n}\n', 'c': '// Two Sum\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n    int nums[n];\n    for (int i = 0; i < n; i++) {\n        scanf("%d", &nums[i]);\n    }\n    int target;\n    scanf("%d", &target);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Find indices i and j such that nums[i] + nums[j] == target\n    \n\n    // Example: printf("%d %d\\n", i, j);\n    return 0;\n}\n'}, 'palindrome_number': {'python': "# Palindrome Number\n# Check if an integer reads the same forwards and backwards. Print 'true' or 'false'.\n\nimport sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    if not s:\n        return\n    x = int(s)\n    \n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print 'true' if x is palindrome, else 'false'\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Palindrome Number\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int x = sc.nextInt();\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print "true" if x is a palindrome, else "false"\n        \n    }\n}\n', 'c': '// Palindrome Number\n#include <stdio.h>\n#include <stdbool.h>\n\nint main() {\n    int x;\n    if (scanf("%d", &x) != 1) return 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print "true" or "false"\n    \n    return 0;\n}\n'}, 'reverse_string': {'python': "# Reverse String\n# Print the reversed string.\n\nimport sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    if not s:\n        return\n    \n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print reversed string\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Reverse String\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.hasNextLine() ? sc.nextLine().trim() : "";\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print the reversed string\n        \n    }\n}\n', 'c': '// Reverse String\n#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char s[100005];\n    if (scanf("%s", s) != 1) return 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print the reversed string\n    \n    return 0;\n}\n'}, 'count_vowels': {'python': "# Count Vowels\n# Count and print the total number of vowels (a, e, i, o, u - case insensitive) in string s.\n\nimport sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    \n    # --- WRITE YOUR SOLUTION HERE ---\n    # Count total vowels and print the count\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Count Vowels\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.hasNextLine() ? sc.nextLine().trim() : "";\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Count vowels (a, e, i, o, u) and print the total count\n        \n    }\n}\n', 'c': '// Count Vowels\n#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char s[100005];\n    if (!fgets(s, sizeof(s), stdin)) return 0;\n    s[strcspn(s, "\\r\\n")] = 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Count vowels and print result\n    \n    return 0;\n}\n'}, 'find_maximum': {'python': "# Find Maximum Element\n# Find and print the maximum integer in the array.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:n+1]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print the maximum number\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Find Maximum Element\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int n = sc.nextInt();\n        int[] nums = new int[n];\n        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print the largest number in nums\n        \n    }\n}\n', 'c': '// Find Maximum Element\n#include <stdio.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n    int nums[n];\n    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print the maximum element\n    \n    return 0;\n}\n'}, 'longest_substring': {'python': "# Longest Substring Without Repeating Characters\n# Find the length of the longest substring with all unique characters.\n\nimport sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print the length of the longest non-repeating substring\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Longest Substring Without Repeating Characters\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.hasNextLine() ? sc.nextLine().trim() : "";\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print the length of the longest substring without duplicate characters\n        \n    }\n}\n', 'c': '// Longest Substring Without Repeating Characters\n#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char s[100005];\n    if (scanf("%s", s) != 1) return 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print the maximum length\n    \n    return 0;\n}\n'}, 'maximum_subarray': {'python': "# Maximum Subarray (Kadane's Algorithm)\n# Find the contiguous subarray with the largest sum and print that sum.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:n+1]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print the maximum subarray sum\n\nif __name__ == '__main__':\n    solve()\n", 'java': "// Maximum Subarray (Kadane's Algorithm)\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int n = sc.nextInt();\n        int[] nums = new int[n];\n        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print the maximum subarray sum\n        \n    }\n}\n", 'c': '// Maximum Subarray\n#include <stdio.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n    int nums[n];\n    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print the maximum subarray sum\n    \n    return 0;\n}\n'}, 'merge_intervals': {'python': "# Merge Overlapping Intervals\n# Merge overlapping intervals and print each merged interval [start end] on a new line.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    intervals = []\n    idx = 1\n    for _ in range(n):\n        intervals.append([int(data[idx]), int(data[idx+1])])\n        idx += 2\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print each merged interval on a new line: print(start, end)\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Merge Overlapping Intervals\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int n = sc.nextInt();\n        int[][] intervals = new int[n][2];\n        for (int i = 0; i < n; i++) {\n            intervals[i][0] = sc.nextInt();\n            intervals[i][1] = sc.nextInt();\n        }\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print each merged interval: System.out.println(start + " " + end);\n        \n    }\n}\n', 'c': '// Merge Overlapping Intervals\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n    int intervals[n][2];\n    for (int i = 0; i < n; i++) {\n        scanf("%d %d", &intervals[i][0], &intervals[i][1]);\n    }\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print merged intervals\n    \n    return 0;\n}\n'}, 'rotate_array': {'python': "# Rotate Array\n# Rotate array to the right by k steps and print the space-separated elements.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    k = int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print rotated array space-separated: print(' '.join(map(str, nums)))\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Rotate Array\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int n = sc.nextInt();\n        int k = sc.nextInt();\n        int[] nums = new int[n];\n        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Rotate nums to the right by k steps and print space-separated\n        \n    }\n}\n', 'c': '// Rotate Array\n#include <stdio.h>\n\nint main() {\n    int n, k;\n    if (scanf("%d %d", &n, &k) != 2) return 0;\n    int nums[n];\n    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print rotated array elements\n    \n    return 0;\n}\n'}, 'valid_parentheses': {'python': "# Valid Parentheses\n# Check if brackets '()', '{}', '[]' are closed in correct order. Print 'true' or 'false'.\n\nimport sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    if not s:\n        return\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print 'true' if valid, else 'false'\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Valid Parentheses\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.hasNext() ? sc.next().trim() : "";\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print "true" if string is valid bracket sequence, else "false"\n        \n    }\n}\n', 'c': '// Valid Parentheses\n#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char s[100005];\n    if (scanf("%s", s) != 1) return 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print "true" or "false"\n    \n    return 0;\n}\n'}, 'binary_tree': {'python': "# Binary Tree Level Order Traversal\n# Print level-by-level traversal of the serialized tree.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    nodes = [int(x) for x in data[1:n+1]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print each level on a new line with space-separated values\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Binary Tree Level Order Traversal\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int n = sc.nextInt();\n        int[] nodes = new int[n];\n        for (int i = 0; i < n; i++) nodes[i] = sc.nextInt();\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print each level on a new line\n        \n    }\n}\n', 'c': '// Binary Tree Level Order Traversal\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n    int nodes[n];\n    for (int i = 0; i < n; i++) scanf("%d", &nodes[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print each level on a new line\n    \n    return 0;\n}\n'}, 'dijkstra_algorithm': {'python': "# Dijkstra's Shortest Path\n# Find shortest path from source vertex to all vertices in directed weighted graph.\n\nimport sys\nimport heapq\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    v = int(data[0])\n    e = int(data[1])\n    src = int(data[2])\n    \n    edges = []\n    idx = 3\n    for _ in range(e):\n        edges.append((int(data[idx]), int(data[idx+1]), int(data[idx+2])))\n        idx += 3\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print shortest distances to all vertices 0 to v-1 separated by spaces (-1 if unreachable)\n\nif __name__ == '__main__':\n    solve()\n", 'java': "// Dijkstra's Shortest Path\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int v = sc.nextInt();\n        int e = sc.nextInt();\n        int src = sc.nextInt();\n        int[][] edges = new int[e][3];\n        for (int i = 0; i < e; i++) {\n            edges[i][0] = sc.nextInt();\n            edges[i][1] = sc.nextInt();\n            edges[i][2] = sc.nextInt();\n        }\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print shortest distances from src to all 0..v-1 vertices (-1 if unreachable)\n        \n    }\n}\n", 'c': '// Dijkstra\'s Shortest Path\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int v, e, src;\n    if (scanf("%d %d %d", &v, &e, &src) != 3) return 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print shortest distances separated by spaces\n    \n    return 0;\n}\n'}, 'n_queens': {'python': "# N-Queens Solutions Count\n# Print the total number of distinct solutions to place N non-attacking queens on N×N board.\n\nimport sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    if not s:\n        return\n    n = int(s)\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print total count of valid board configurations\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// N-Queens Solutions Count\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int n = sc.nextInt();\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print total number of distinct N-Queens placements\n        \n    }\n}\n', 'c': '// N-Queens Solutions Count\n#include <stdio.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print the total number of distinct solutions\n    \n    return 0;\n}\n'}, 'shortest_path': {'python': "# Shortest Path in Unweighted Graph\n# Find the shortest distance between start and end node using BFS. Print -1 if no path.\n\nimport sys\nfrom collections import deque\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    e = int(data[1])\n    start = int(data[2])\n    end = int(data[3])\n    \n    edges = []\n    idx = 4\n    for _ in range(e):\n        edges.append((int(data[idx]), int(data[idx+1])))\n        idx += 2\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print shortest path distance or -1\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Shortest Path in Unweighted Graph (BFS)\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int n = sc.nextInt();\n        int e = sc.nextInt();\n        int start = sc.nextInt();\n        int end = sc.nextInt();\n        int[][] edges = new int[e][2];\n        for (int i = 0; i < e; i++) {\n            edges[i][0] = sc.nextInt();\n            edges[i][1] = sc.nextInt();\n        }\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print shortest distance from start to end (or -1)\n        \n    }\n}\n', 'c': '// Shortest Path in Unweighted Graph\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int n, e, start, end;\n    if (scanf("%d %d %d %d", &n, &e, &start, &end) != 4) return 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print shortest distance or -1\n    \n    return 0;\n}\n'}, 'word_ladder': {'python': "# Word Ladder (Shortest Transformation Sequence)\n# Find minimum words in transformation sequence from beginWord to endWord. Print 0 if impossible.\n\nimport sys\nfrom collections import deque\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    begin_word = data[0]\n    end_word = data[1]\n    n = int(data[2])\n    word_list = data[3:3+n]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print sequence length or 0\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Word Ladder\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNext()) return;\n        String beginWord = sc.next();\n        String endWord = sc.next();\n        int n = sc.nextInt();\n        List<String> wordList = new ArrayList<>();\n        for (int i = 0; i < n; i++) wordList.add(sc.next());\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print shortest ladder length (or 0)\n        \n    }\n}\n', 'c': '// Word Ladder\n#include <stdio.h>\n#include <string.h>\n#include <stdlib.h>\n\nint main() {\n    char beginWord[105], endWord[105];\n    if (scanf("%s %s", beginWord, endWord) != 2) return 0;\n    int n;\n    scanf("%d", &n);\n    char words[n][105];\n    for (int i = 0; i < n; i++) scanf("%s", words[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print transformation sequence length or 0\n    \n    return 0;\n}\n'}, 'climbing_stairs': {'python': "# Climbing Stairs\n# Distinct ways to climb n steps (can climb 1 or 2 steps each time).\n\nimport sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    if not s:\n        return\n    n = int(s)\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print total distinct ways\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Climbing Stairs\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int n = sc.nextInt();\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print number of distinct ways to climb n stairs\n        \n    }\n}\n', 'c': '// Climbing Stairs\n#include <stdio.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print total distinct ways\n    \n    return 0;\n}\n'}, 'majority_element': {'python': "# Majority Element\n# Find element appearing more than ⌊n / 2⌋ times.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:n+1]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print the majority element\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Majority Element\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int n = sc.nextInt();\n        int[] nums = new int[n];\n        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print the majority element\n        \n    }\n}\n', 'c': '// Majority Element\n#include <stdio.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n    int nums[n];\n    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print the majority element\n    \n    return 0;\n}\n'}, 'reverse_words': {'python': "# Reverse Words in a String\n# Reverse order of words in string s. Words should be separated by a single space.\n\nimport sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    if not s:\n        return\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print reversed words joined by space\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Reverse Words in a String\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.hasNextLine() ? sc.nextLine().trim() : "";\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print words reversed in order, separated by a single space\n        \n    }\n}\n', 'c': '// Reverse Words in a String\n#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char s[100005];\n    if (!fgets(s, sizeof(s), stdin)) return 0;\n    s[strcspn(s, "\\r\\n")] = 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print words reversed\n    \n    return 0;\n}\n'}, 'single_number': {'python': "# Single Number\n# Every element appears twice except for one. Find and print that single element.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:n+1]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print the single unique number\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Single Number\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int n = sc.nextInt();\n        int[] nums = new int[n];\n        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print the element that appears only once\n        \n    }\n}\n', 'c': '// Single Number\n#include <stdio.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n    int nums[n];\n    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print the unique number\n    \n    return 0;\n}\n'}, 'coin_change': {'python': "# Coin Change\n# Fewest number of coins needed to make up amount. Print -1 if impossible.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    coins = [int(x) for x in data[1:n+1]]\n    amount = int(data[n+1])\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print minimum coins needed (or -1)\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Coin Change\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int n = sc.nextInt();\n        int[] coins = new int[n];\n        for (int i = 0; i < n; i++) coins[i] = sc.nextInt();\n        int amount = sc.nextInt();\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print minimum coins needed (or -1)\n        \n    }\n}\n', 'c': '// Coin Change\n#include <stdio.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n    int coins[n];\n    for (int i = 0; i < n; i++) scanf("%d", &coins[i]);\n    int amount;\n    scanf("%d", &amount);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print minimum coins needed (or -1)\n    \n    return 0;\n}\n'}, 'container_with_most_water': {'python': "# Container With Most Water\n# Find two lines that together with x-axis form a container holding the most water.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    height = [int(x) for x in data[1:n+1]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print maximum water area\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Container With Most Water\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int n = sc.nextInt();\n        int[] height = new int[n];\n        for (int i = 0; i < n; i++) height[i] = sc.nextInt();\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print maximum water area\n        \n    }\n}\n', 'c': '// Container With Most Water\n#include <stdio.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n    int height[n];\n    for (int i = 0; i < n; i++) scanf("%d", &height[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print maximum water capacity\n    \n    return 0;\n}\n'}, 'group_anagrams': {'python': "# Group Anagrams Count\n# Group anagram words together and print the total number of distinct anagram groups.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    words = data[1:n+1]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print total count of distinct anagram groups\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Group Anagrams Count\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int n = sc.nextInt();\n        String[] words = new String[n];\n        for (int i = 0; i < n; i++) words[i] = sc.next();\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print number of distinct anagram groups\n        \n    }\n}\n', 'c': '// Group Anagrams Count\n#include <stdio.h>\n#include <string.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n    char words[n][105];\n    for (int i = 0; i < n; i++) scanf("%s", words[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print number of distinct anagram groups\n    \n    return 0;\n}\n'}, 'rotate_matrix': {'python': "# Rotate Matrix 90 Degrees Clockwise\n# Rotate N×N matrix 90 degrees clockwise and print row by row.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    matrix = []\n    idx = 1\n    for _ in range(n):\n        matrix.append([int(x) for x in data[idx:idx+n]])\n        idx += n\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print rotated matrix line by line with space-separated integers\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Rotate Matrix 90 Degrees\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int n = sc.nextInt();\n        int[][] matrix = new int[n][n];\n        for (int i = 0; i < n; i++) {\n            for (int j = 0; j < n; j++) {\n                matrix[i][j] = sc.nextInt();\n            }\n        }\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Rotate matrix 90 degrees clockwise and print row by row\n        \n    }\n}\n', 'c': '// Rotate Matrix 90 Degrees\n#include <stdio.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n    int matrix[n][n];\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n; j++) scanf("%d", &matrix[i][j]);\n    }\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print rotated matrix\n    \n    return 0;\n}\n'}, 'longest_valid_parentheses': {'python': "# Longest Valid Parentheses\n# Find length of longest valid (well-formed) parentheses substring.\n\nimport sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    if not s:\n        return\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print maximum valid length\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Longest Valid Parentheses\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.hasNext() ? sc.next().trim() : "";\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print maximum valid parentheses length\n        \n    }\n}\n', 'c': '// Longest Valid Parentheses\n#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char s[100005];\n    if (scanf("%s", s) != 1) return 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print maximum valid length\n    \n    return 0;\n}\n'}, 'median_two_sorted_arrays': {'python': "# Median of Two Sorted Arrays\n# Find the median of two sorted arrays. Print float formatted to 5 decimals or integer.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    m = int(data[1])\n    nums1 = [int(x) for x in data[2:2+n]]\n    nums2 = [int(x) for x in data[2+n:2+n+m]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print the median value\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Median of Two Sorted Arrays\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int n = sc.nextInt();\n        int m = sc.nextInt();\n        int[] nums1 = new int[n];\n        for (int i = 0; i < n; i++) nums1[i] = sc.nextInt();\n        int[] nums2 = new int[m];\n        for (int i = 0; i < m; i++) nums2[i] = sc.nextInt();\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print the median\n        \n    }\n}\n', 'c': '// Median of Two Sorted Arrays\n#include <stdio.h>\n\nint main() {\n    int n, m;\n    if (scanf("%d %d", &n, &m) != 2) return 0;\n    int nums1[n], nums2[m];\n    for (int i = 0; i < n; i++) scanf("%d", &nums1[i]);\n    for (int i = 0; i < m; i++) scanf("%d", &nums2[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print median\n    \n    return 0;\n}\n'}, 'merge_k_sorted_lists': {'python': "# Merge K Sorted Lists\n# Merge K sorted integer arrays into one sorted array. Print space-separated.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    k = int(data[0])\n    lists = []\n    idx = 1\n    for _ in range(k):\n        sz = int(data[idx])\n        lists.append([int(x) for x in data[idx+1:idx+1+sz]])\n        idx += 1 + sz\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print merged sorted elements separated by spaces\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Merge K Sorted Lists\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int k = sc.nextInt();\n        List<int[]> lists = new ArrayList<>();\n        for (int i = 0; i < k; i++) {\n            int sz = sc.nextInt();\n            int[] arr = new int[sz];\n            for (int j = 0; j < sz; j++) arr[j] = sc.nextInt();\n            lists.add(arr);\n        }\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print merged sorted array space-separated\n        \n    }\n}\n', 'c': '// Merge K Sorted Lists\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int k;\n    if (scanf("%d", &k) != 1) return 0;\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print merged sorted elements\n    \n    return 0;\n}\n'}, 'trapping_rain_water': {'python': "# Trapping Rain Water\n# Compute total units of rainwater trapped after raining.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    n = int(data[0])\n    height = [int(x) for x in data[1:n+1]]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print total water trapped\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Trapping Rain Water\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) return;\n        int n = sc.nextInt();\n        int[] height = new int[n];\n        for (int i = 0; i < n; i++) height[i] = sc.nextInt();\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print total trapped rainwater\n        \n    }\n}\n', 'c': '// Trapping Rain Water\n#include <stdio.h>\n\nint main() {\n    int n;\n    if (scanf("%d", &n) != 1) return 0;\n    int height[n];\n    for (int i = 0; i < n; i++) scanf("%d", &height[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print total trapped rainwater\n    \n    return 0;\n}\n'}, 'word_break': {'python': "# Word Break\n# Check if string s can be segmented into space-separated sequence of dictionary words. Print 'true' or 'false'.\n\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n    s = data[0]\n    n = int(data[1])\n    word_dict = data[2:2+n]\n\n    # --- WRITE YOUR SOLUTION HERE ---\n    # Print 'true' if possible, else 'false'\n\nif __name__ == '__main__':\n    solve()\n", 'java': '// Word Break\nimport java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNext()) return;\n        String s = sc.next();\n        int n = sc.nextInt();\n        List<String> wordDict = new ArrayList<>();\n        for (int i = 0; i < n; i++) wordDict.add(sc.next());\n\n        // --- WRITE YOUR SOLUTION HERE ---\n        // Print "true" or "false"\n        \n    }\n}\n', 'c': '// Word Break\n#include <stdio.h>\n#include <string.h>\n#include <stdbool.h>\n\nint main() {\n    char s[1005];\n    if (scanf("%s", s) != 1) return 0;\n    int n;\n    scanf("%d", &n);\n    char words[n][1005];\n    for (int i = 0; i < n; i++) scanf("%s", words[i]);\n\n    // --- WRITE YOUR SOLUTION HERE ---\n    // Print "true" or "false"\n    \n    return 0;\n}\n'}}

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
        String s = sc.hasNextLine() ? sc.nextLine().trim() : "";
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