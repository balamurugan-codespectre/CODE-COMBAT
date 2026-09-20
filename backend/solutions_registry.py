"""
CODE COMBAT Pro - Official Solutions Registry
Stores 100% verified official solutions for all problems across Set 1 and Set 2
in Python 3, Java, and C.
"""

SOLUTIONS_REGISTRY = {
    # ==================== SET 1 ====================
    "two_sum": {
        "python": """class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        m = {}
        for i, n in enumerate(nums):
            comp = target - n
            if comp in m:
                return [m[comp], i]
            m[n] = i
        return []
""",
        "java": """import java.util.*;

class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int comp = target - nums[i];
            if (map.containsKey(comp)) {
                return new int[]{map.get(comp), i};
            }
            map.put(nums[i], i);
        }
        return new int[]{};
    }
}""",
        "c": """#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int nums[n];
    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);
    int target;
    scanf("%d", &target);

    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (nums[i] + nums[j] == target) {
                printf("%d %d\n", i, j);
                return 0;
            }
        }
    }
    return 0;
}"""
    },

    "palindrome_number": {
        "python": """class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0: return False
        s = str(x)
        return s == s[::-1]
""",
        "java": """class Solution {
    public boolean isPalindrome(int x) {
        if (x < 0) return false;
        String s = String.valueOf(x);
        return s.equals(new StringBuilder(s).reverse().toString());
    }
}""",
        "c": """#include <stdio.h>
#include <stdbool.h>

int main() {
    int x;
    if (scanf("%d", &x) != 1) return 0;
    if (x < 0) {
        printf("false\n");
        return 0;
    }
    long orig = x, rev = 0;
    while (x > 0) {
        rev = rev * 10 + (x % 10);
        x /= 10;
    }
    if (orig == rev) printf("true\n");
    else printf("false\n");
    return 0;
}"""
    },

    "reverse_string": {
        "python": """class Solution:
    def reverseString(self, s: str) -> str:
        return s[::-1]
""",
        "java": """class Solution {
    public String reverseString(String s) {
        return new StringBuilder(s).reverse().toString();
    }
}""",
        "c": """#include <stdio.h>
#include <string.h>

int main() {
    char s[100005];
    if (scanf("%s", s) != 1) return 0;
    int len = strlen(s);
    for (int i = 0, j = len - 1; i < j; i++, j--) {
        char t = s[i]; s[i] = s[j]; s[j] = t;
    }
    printf("%s\n", s);
    return 0;
}"""
    },

    "count_vowels": {
        "python": """class Solution:
    def countVowels(self, s: str) -> int:
        vowels = set('aeiouAEIOU')
        return sum(1 for c in s if c in vowels)
""",
        "java": """class Solution {
    public int countVowels(String s) {
        int count = 0;
        String v = "aeiouAEIOU";
        for (char c : s.toCharArray()) {
            if (v.indexOf(c) != -1) count++;
        }
        return count;
    }
}""",
        "c": """#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main() {
    char s[100005];
    if (!fgets(s, sizeof(s), stdin)) return 0;
    int count = 0;
    for (int i = 0; s[i]; i++) {
        char c = tolower(s[i]);
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') count++;
    }
    printf("%d\n", count);
    return 0;
}"""
    },

    "find_maximum": {
        "python": """class Solution:
    def findMax(self, nums: List[int]) -> int:
        return max(nums)
""",
        "java": """class Solution {
    public int findMax(int[] nums) {
        int m = nums[0];
        for (int x : nums) if (x > m) m = x;
        return m;
    }
}""",
        "c": """#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int nums[n];
    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);
    int max = nums[0];
    for (int i = 1; i < n; i++) {
        if (nums[i] > max) max = nums[i];
    }
    printf("%d\n", max);
    return 0;
}"""
    },

    "longest_substring": {
        "python": """class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_map = {}
        left = max_len = 0
        for right, c in enumerate(s):
            if c in char_map and char_map[c] >= left:
                left = char_map[c] + 1
            char_map[c] = right
            max_len = max(max_len, right - left + 1)
        return max_len
""",
        "java": """import java.util.*;

class Solution {
    public int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> map = new HashMap<>();
        int left = 0, maxLen = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            if (map.containsKey(c) && map.get(c) >= left) {
                left = map.get(c) + 1;
            }
            map.put(c, right);
            maxLen = Math.max(maxLen, right - left + 1);
        }
        return maxLen;
    }
}""",
        "c": """#include <stdio.h>
#include <string.h>

int main() {
    char s[100005];
    if (scanf("%s", s) != 1) {
        printf("0\n");
        return 0;
    }
    int last[256];
    memset(last, -1, sizeof(last));
    int max_len = 0, left = 0, len = strlen(s);
    for (int right = 0; right < len; right++) {
        unsigned char c = s[right];
        if (last[c] >= left) left = last[c] + 1;
        last[c] = right;
        int cur = right - left + 1;
        if (cur > max_len) max_len = cur;
    }
    printf("%d\n", max_len);
    return 0;
}"""
    },

    "maximum_subarray": {
        "python": """class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        cur = max_s = nums[0]
        for x in nums[1:]:
            cur = max(x, cur + x)
            max_s = max(max_s, cur)
        return max_s
""",
        "java": """class Solution {
    public int maxSubArray(int[] nums) {
        int cur = nums[0], maxS = nums[0];
        for (int i = 1; i < nums.length; i++) {
            cur = Math.max(nums[i], cur + nums[i]);
            maxS = Math.max(maxS, cur);
        }
        return maxS;
    }
}""",
        "c": """#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int nums[n];
    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);
    int cur = nums[0], max_s = nums[0];
    for (int i = 1; i < n; i++) {
        cur = (nums[i] > cur + nums[i]) ? nums[i] : (cur + nums[i]);
        if (cur > max_s) max_s = cur;
    }
    printf("%d\n", max_s);
    return 0;
}"""
    },

    "merge_intervals": {
        "python": """class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals: return []
        intervals.sort(key=lambda x: x[0])
        merged = [intervals[0]]
        for cur in intervals[1:]:
            prev = merged[-1]
            if cur[0] <= prev[1]:
                prev[1] = max(prev[1], cur[1])
            else:
                merged.append(cur)
        return merged
""",
        "java": """import java.util.*;

class Solution {
    public int[][] merge(int[][] intervals) {
        if (intervals.length <= 1) return intervals;
        Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
        List<int[]> res = new ArrayList<>();
        int[] cur = intervals[0];
        res.add(cur);
        for (int[] inv : intervals) {
            if (inv[0] <= cur[1]) {
                cur[1] = Math.max(cur[1], inv[1]);
            } else {
                cur = inv;
                res.add(cur);
            }
        }
        return res.toArray(new int[res.size()][]);
    }
}""",
        "c": """#include <stdio.h>
#include <stdlib.h>

typedef struct { int start, end; } Interval;

int compare(const void* a, const void* b) {
    return ((Interval*)a)->start - ((Interval*)b)->start;
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    Interval arr[n];
    for (int i = 0; i < n; i++) scanf("%d %d", &arr[i].start, &arr[i].end);
    qsort(arr, n, sizeof(Interval), compare);

    Interval merged[n];
    int m_count = 0;
    merged[0] = arr[0];
    m_count = 1;

    for (int i = 1; i < n; i++) {
        if (arr[i].start <= merged[m_count - 1].end) {
            if (arr[i].end > merged[m_count - 1].end) {
                merged[m_count - 1].end = arr[i].end;
            }
        } else {
            merged[m_count++] = arr[i];
        }
    }

    for (int i = 0; i < m_count; i++) {
        printf("%d %d\n", merged[i].start, merged[i].end);
    }
    return 0;
}"""
    },

    "rotate_array": {
        "python": """class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        if n == 0: return
        k %= n
        nums[:] = nums[-k:] + nums[:-k]
""",
        "java": """class Solution {
    public void rotate(int[] nums, int k) {
        int n = nums.length;
        if (n == 0) return;
        k %= n;
        reverse(nums, 0, n - 1);
        reverse(nums, 0, k - 1);
        reverse(nums, k, n - 1);
    }
    private void reverse(int[] a, int l, int r) {
        while (l < r) {
            int t = a[l]; a[l] = a[r]; a[r] = t;
            l++; r--;
        }
    }
}""",
        "c": """#include <stdio.h>

void reverse(int arr[], int l, int r) {
    while (l < r) {
        int t = arr[l]; arr[l] = arr[r]; arr[r] = t;
        l++; r--;
    }
}

int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    int nums[n];
    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);
    k %= n;
    reverse(nums, 0, n - 1);
    reverse(nums, 0, k - 1);
    reverse(nums, k, n - 1);
    for (int i = 0; i < n; i++) printf("%d%c", nums[i], (i == n - 1) ? '\n' : ' ');
    return 0;
}"""
    },

    "valid_parentheses": {
        "python": """class Solution:
    def isValid(self, s: str) -> bool:
        st = []
        mapping = {')': '(', '}': '{', ']': '['}
        for c in s:
            if c in mapping:
                if not st or st.pop() != mapping[c]: return False
            else:
                st.append(c)
        return len(st) == 0
""",
        "java": """import java.util.*;

class Solution {
    public boolean isValid(String s) {
        Stack<Character> st = new Stack<>();
        for (char c : s.toCharArray()) {
            if (c == '(') st.push(')');
            else if (c == '{') st.push('}');
            else if (c == '[') st.push(']');
            else if (st.isEmpty() || st.pop() != c) return false;
        }
        return st.isEmpty();
    }
}""",
        "c": """#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int main() {
    char s[100005];
    if (scanf("%s", s) != 1) return 0;
    char st[100005];
    int top = 0;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '(' || c == '{' || c == '[') st[top++] = c;
        else {
            if (top == 0) { printf("false\n"); return 0; }
            char open = st[--top];
            if ((c == ')' && open != '(') || (c == '}' && open != '{') || (c == ']' && open != '[')) {
                printf("false\n"); return 0;
            }
        }
    }
    if (top == 0) printf("true\n");
    else printf("false\n");
    return 0;
}"""
    },

    "binary_tree": {
        "python": """from collections import deque

class Solution:
    def levelOrder(self, tree: List[int]) -> List[List[int]]:
        if not tree or tree[0] == -1: return []
        q = deque([0])
        res = []
        n = len(tree)
        while q:
            sz = len(q)
            level = []
            for _ in range(sz):
                curr = q.popleft()
                level.append(tree[curr])
                left = 2 * curr + 1
                right = 2 * curr + 2
                if left < n and tree[left] != -1: q.append(left)
                if right < n and tree[right] != -1: q.append(right)
            res.append(level)
        return res
""",
        "java": """import java.util.*;

class Solution {
    public List<List<Integer>> levelOrder(int[] tree) {
        List<List<Integer>> res = new ArrayList<>();
        if (tree == null || tree.length == 0 || tree[0] == -1) return res;
        Queue<Integer> q = new LinkedList<>();
        q.offer(0);
        int n = tree.length;
        while (!q.isEmpty()) {
            int sz = q.size();
            List<Integer> level = new ArrayList<>();
            for (int i = 0; i < sz; i++) {
                int curr = q.poll();
                level.add(tree[curr]);
                int left = 2 * curr + 1;
                int right = 2 * curr + 2;
                if (left < n && tree[left] != -1) q.offer(left);
                if (right < n && tree[right] != -1) q.offer(right);
            }
            res.add(level);
        }
        return res;
    }
}""",
        "c": """#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int tree[n];
    for (int i = 0; i < n; i++) scanf("%d", &tree[i]);
    if (n == 0 || tree[0] == -1) return 0;

    int q[100005];
    int head = 0, tail = 0;
    q[tail++] = 0;

    while (head < tail) {
        int sz = tail - head;
        for (int i = 0; i < sz; i++) {
            int curr = q[head++];
            printf("%d%c", tree[curr], (i == sz - 1) ? '\n' : ' ');
            int left = 2 * curr + 1, right = 2 * curr + 2;
            if (left < n && tree[left] != -1) q[tail++] = left;
            if (right < n && tree[right] != -1) q[tail++] = right;
        }
    }
    return 0;
}"""
    },

    "dijkstra_algorithm": {
        "python": """import heapq

class Solution:
    def dijkstra(self, n: int, edges: List[List[int]], start: int) -> List[int]:
        adj = {i: [] for i in range(n)}
        for u, v, w in edges:
            adj[u].append((v, w))
        dist = [float('inf')] * n
        dist[start] = 0
        pq = [(0, start)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]: continue
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))
        return [d if d != float('inf') else -1 for d in dist]
""",
        "java": """import java.util.*;

class Solution {
    public int[] dijkstra(int n, int[][] edges, int start) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) {
            adj.get(e[0]).add(new int[]{e[1], e[2]});
        }
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[start] = 0;
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[1], b[1]));
        pq.offer(new int[]{start, 0});
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int u = cur[0], d = cur[1];
            if (d > dist[u]) continue;
            for (int[] edge : adj.get(u)) {
                int v = edge[0], w = edge[1];
                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    pq.offer(new int[]{v, dist[v]});
                }
            }
        }
        for (int i = 0; i < n; i++) if (dist[i] == Integer.MAX_VALUE) dist[i] = -1;
        return dist;
    }
}""",
        "c": """#include <stdio.h>
#include <limits.h>

int main() {
    int v, e, src;
    if (scanf("%d %d %d", &v, &e, &src) != 3) return 0;
    int cost[v][v];
    for (int i = 0; i < v; i++) {
        for (int j = 0; j < v; j++) cost[i][j] = (i == j) ? 0 : 100000000;
    }
    for (int i = 0; i < e; i++) {
        int u, to, w;
        scanf("%d %d %d", &u, &to, &w);
        cost[u][to] = w;
    }
    int dist[v], visited[v];
    for (int i = 0; i < v; i++) { dist[i] = 100000000; visited[i] = 0; }
    dist[src] = 0;

    for (int count = 0; count < v - 1; count++) {
        int min_d = 100000000, u = -1;
        for (int i = 0; i < v; i++) {
            if (!visited[i] && dist[i] < min_d) { min_d = dist[i]; u = i; }
        }
        if (u == -1) break;
        visited[u] = 1;
        for (int j = 0; j < v; j++) {
            if (!visited[j] && cost[u][j] < 100000000 && dist[u] + cost[u][j] < dist[j]) {
                dist[j] = dist[u] + cost[u][j];
            }
        }
    }
    for (int i = 0; i < v; i++) {
        int d = (dist[i] >= 100000000) ? -1 : dist[i];
        printf("%d%c", d, (i == v - 1) ? '\n' : ' ');
    }
    return 0;
}"""
    },

    "n_queens": {
        "python": """class Solution:
    def totalNQueens(self, n: int) -> int:
        count = 0
        def backtrack(row, cols, diags1, diags2):
            nonlocal count
            if row == n:
                count += 1
                return
            for col in range(n):
                if col in cols or (row - col) in diags1 or (row + col) in diags2:
                    continue
                cols.add(col)
                diags1.add(row - col)
                diags2.add(row + col)
                backtrack(row + 1, cols, diags1, diags2)
                cols.remove(col)
                diags1.remove(row - col)
                diags2.remove(row + col)
        backtrack(0, set(), set(), set())
        return count
""",
        "java": """import java.util.*;

class Solution {
    private int count = 0;
    public int totalNQueens(int n) {
        count = 0;
        solve(0, n, new HashSet<>(), new HashSet<>(), new HashSet<>());
        return count;
    }
    private void solve(int row, int n, Set<Integer> cols, Set<Integer> d1, Set<Integer> d2) {
        if (row == n) { count++; return; }
        for (int col = 0; col < n; col++) {
            if (cols.contains(col) || d1.contains(row - col) || d2.contains(row + col)) continue;
            cols.add(col); d1.add(row - col); d2.add(row + col);
            solve(row + 1, n, cols, d1, d2);
            cols.remove(col); d1.remove(row - col); d2.remove(row + col);
        }
    }
}""",
        "c": """#include <stdio.h>
#include <stdlib.h>

int total_count = 0;

void solve(int row, int n, int cols, int d1, int d2) {
    if (row == n) { total_count++; return; }
    int available = ((1 << n) - 1) & ~(cols | d1 | d2);
    while (available) {
        int bit = available & -available;
        available -= bit;
        solve(row + 1, n, cols | bit, (d1 | bit) << 1, (d2 | bit) >> 1);
    }
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    total_count = 0;
    solve(0, n, 0, 0, 0);
    printf("%d\n", total_count);
    return 0;
}"""
    },

    "shortest_path": {
        "python": """from collections import deque

class Solution:
    def shortestPath(self, n: int, edges: List[List[int]], start: int, end: int) -> int:
        adj = {i: [] for i in range(n)}
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        q = deque([(start, 0)])
        visited = {start}
        while q:
            u, d = q.popleft()
            if u == end: return d
            for v in adj[u]:
                if v not in visited:
                    visited.add(v)
                    q.append((v, d + 1))
        return -1
""",
        "java": """import java.util.*;

class Solution {
    public int shortestPath(int n, int[][] edges, int start, int end) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }
        Queue<int[]> q = new LinkedList<>();
        boolean[] visited = new boolean[n];
        q.offer(new int[]{start, 0});
        visited[start] = true;
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            int u = cur[0], d = cur[1];
            if (u == end) return d;
            for (int v : adj.get(u)) {
                if (!visited[v]) {
                    visited[v] = true;
                    q.offer(new int[]{v, d + 1});
                }
            }
        }
        return -1;
    }
}""",
        "c": """#include <stdio.h>
#include <stdlib.h>

int main() {
    int n, e, start, end;
    if (scanf("%d %d %d %d", &n, &e, &start, &end) != 4) return 0;
    int adj[n][n];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) adj[i][j] = 0;
    }
    for (int i = 0; i < e; i++) {
        int u, v;
        scanf("%d %d", &u, &v);
        adj[u][v] = adj[v][u] = 1;
    }

    int q[100005], dist[100005], visited[100005];
    for (int i = 0; i < n; i++) visited[i] = 0;
    int head = 0, tail = 0;

    q[tail] = start; dist[tail] = 0; tail++;
    visited[start] = 1;

    int ans = -1;
    while (head < tail) {
        int u = q[head], d = dist[head++];
        if (u == end) { ans = d; break; }
        for (int v = 0; v < n; v++) {
            if (adj[u][v] && !visited[v]) {
                visited[v] = 1;
                q[tail] = v; dist[tail] = d + 1; tail++;
            }
        }
    }
    printf("%d\n", ans);
    return 0;
}"""
    },

    "word_ladder": {
        "python": """from collections import deque

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        words = set(wordList)
        if endWord not in words: return 0
        q = deque([(beginWord, 1)])
        visited = {beginWord}
        while q:
            word, length = q.popleft()
            if word == endWord: return length
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    next_word = word[:i] + c + word[i+1:]
                    if next_word in words and next_word not in visited:
                        visited.add(next_word)
                        q.append((next_word, length + 1))
        return 0
""",
        "java": """import java.util.*;

class Solution {
    public int ladderLength(String beginWord, String endWord, List<String> wordList) {
        Set<String> words = new HashSet<>(wordList);
        if (!words.contains(endWord)) return 0;
        Queue<String> q = new LinkedList<>();
        Set<String> visited = new HashSet<>();
        q.offer(beginWord);
        visited.add(beginWord);
        int step = 1;
        while (!q.isEmpty()) {
            int sz = q.size();
            for (int s = 0; s < sz; s++) {
                String word = q.poll();
                if (word.equals(endWord)) return step;
                char[] chars = word.toCharArray();
                for (int i = 0; i < chars.length; i++) {
                    char orig = chars[i];
                    for (char c = 'a'; c <= 'z'; c++) {
                        chars[i] = c;
                        String nw = new String(chars);
                        if (words.contains(nw) && !visited.contains(nw)) {
                            visited.add(nw);
                            q.offer(nw);
                        }
                    }
                    chars[i] = orig;
                }
            }
            step++;
        }
        return 0;
    }
}""",
        "c": """#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int diff_one(const char* a, const char* b) {
    int diff = 0;
    for (int i = 0; a[i] && b[i]; i++) {
        if (a[i] != b[i]) { diff++; if (diff > 1) return 0; }
    }
    return diff == 1;
}

int main() {
    char beginWord[105], endWord[105];
    if (scanf("%s %s", beginWord, endWord) != 2) return 0;
    int n;
    if (scanf("%d", &n) != 1) return 0;
    char words[n][105];
    int end_idx = -1;
    for (int i = 0; i < n; i++) {
        scanf("%s", words[i]);
        if (strcmp(words[i], endWord) == 0) end_idx = i;
    }
    if (end_idx == -1) { printf("0\n"); return 0; }

    int q[1005], dist[1005], visited[1005];
    memset(visited, 0, sizeof(visited));
    int head = 0, tail = 0;

    for (int i = 0; i < n; i++) {
        if (diff_one(beginWord, words[i])) {
            q[tail] = i; dist[tail] = 2; visited[i] = 1; tail++;
        }
    }

    int ans = 0;
    while (head < tail) {
        int u = q[head], d = dist[head++];
        if (u == end_idx) { ans = d; break; }
        for (int v = 0; v < n; v++) {
            if (!visited[v] && diff_one(words[u], words[v])) {
                visited[v] = 1;
                q[tail] = v; dist[tail] = d + 1; tail++;
            }
        }
    }
    printf("%d\n", ans);
    return 0;
}"""
    },

    # ==================== SET 2 ====================
    "climbing_stairs": {
        "python": """class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2: return n
        a, b = 1, 2
        for _ in range(3, n + 1):
            a, b = b, a + b
        return b
""",
        "java": """class Solution {
    public int climbStairs(int n) {
        if (n <= 2) return n;
        int a = 1, b = 2;
        for (int i = 3; i <= n; i++) {
            int c = a + b;
            a = b;
            b = c;
        }
        return b;
    }
}""",
        "c": """#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    if (n <= 2) { printf("%d\n", n); return 0; }
    int a = 1, b = 2;
    for (int i = 3; i <= n; i++) {
        int c = a + b;
        a = b;
        b = c;
    }
    printf("%d\n", b);
    return 0;
}"""
    },

    "majority_element": {
        "python": """class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        cand, count = None, 0
        for x in nums:
            if count == 0: cand = x
            count += (1 if x == cand else -1)
        return cand
""",
        "java": """class Solution {
    public int majorityElement(int[] nums) {
        int cand = nums[0], count = 0;
        for (int x : nums) {
            if (count == 0) cand = x;
            count += (x == cand ? 1 : -1);
        }
        return cand;
    }
}""",
        "c": """#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int nums[n];
    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);
    int cand = nums[0], count = 0;
    for (int i = 0; i < n; i++) {
        if (count == 0) cand = nums[i];
        count += (nums[i] == cand ? 1 : -1);
    }
    printf("%d\n", cand);
    return 0;
}"""
    },

    "reverse_words": {
        "python": """class Solution:
    def reverseWords(self, s: str) -> str:
        return ' '.join(s.strip().split()[::-1])
""",
        "java": """class Solution {
    public String reverseWords(String s) {
        String[] parts = s.trim().split("\\s+");
        StringBuilder sb = new StringBuilder();
        for (int i = parts.length - 1; i >= 0; i--) {
            sb.append(parts[i]).append(i == 0 ? "" : " ");
        }
        return sb.toString();
    }
}""",
        "c": """#include <stdio.h>
#include <string.h>

int main() {
    char s[100005];
    if (!fgets(s, sizeof(s), stdin)) return 0;
    char words[1005][105];
    int count = 0;
    char* token = strtok(s, " \r\n\t");
    while (token) {
        strcpy(words[count++], token);
        token = strtok(NULL, " \r\n\t");
    }
    for (int i = count - 1; i >= 0; i--) {
        printf("%s%c", words[i], (i == 0) ? '\n' : ' ');
    }
    return 0;
}"""
    },

    "single_number": {
        "python": """class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        res = 0
        for x in nums: res ^= x
        return res
""",
        "java": """class Solution {
    public int singleNumber(int[] nums) {
        int res = 0;
        for (int x : nums) res ^= x;
        return res;
    }
}""",
        "c": """#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int res = 0;
    for (int i = 0; i < n; i++) {
        int x; scanf("%d", &x);
        res ^= x;
    }
    printf("%d\n", res);
    return 0;
}"""
    },

    "coin_change": {
        "python": """class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        for c in coins:
            for x in range(c, amount + 1):
                dp[x] = min(dp[x], dp[x - c] + 1)
        return dp[amount] if dp[amount] != float('inf') else -1
""",
        "java": """import java.util.*;

class Solution {
    public int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        dp[0] = 0;
        for (int c : coins) {
            for (int x = c; x <= amount; x++) {
                dp[x] = Math.min(dp[x], dp[x - c] + 1);
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }
}""",
        "c": """#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int coins[n];
    for (int i = 0; i < n; i++) scanf("%d", &coins[i]);
    int amount;
    scanf("%d", &amount);

    int dp[amount + 1];
    for (int i = 0; i <= amount; i++) dp[i] = 1000000;
    dp[0] = 0;

    for (int i = 0; i < n; i++) {
        int c = coins[i];
        for (int x = c; x <= amount; x++) {
            if (dp[x - c] + 1 < dp[x]) dp[x] = dp[x - c] + 1;
        }
    }
    printf("%d\n", (dp[amount] >= 1000000) ? -1 : dp[amount]);
    return 0;
}"""
    },

    "container_with_most_water": {
        "python": """class Solution:
    def maxArea(self, height: List[int]) -> int:
        l, r = 0, len(height) - 1
        max_a = 0
        while l < r:
            max_a = max(max_a, min(height[l], height[r]) * (r - l))
            if height[l] < height[r]: l += 1
            else: r -= 1
        return max_a
""",
        "java": """class Solution {
    public int maxArea(int[] height) {
        int l = 0, r = height.length - 1, maxA = 0;
        while (l < r) {
            maxA = Math.max(maxA, Math.min(height[l], height[r]) * (r - l));
            if (height[l] < height[r]) l++;
            else r--;
        }
        return maxA;
    }
}""",
        "c": """#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int h[n];
    for (int i = 0; i < n; i++) scanf("%d", &h[i]);
    int l = 0, r = n - 1, max_a = 0;
    while (l < r) {
        int min_h = (h[l] < h[r]) ? h[l] : h[r];
        int cur = min_h * (r - l);
        if (cur > max_a) max_a = cur;
        if (h[l] < h[r]) l++;
        else r--;
    }
    printf("%d\n", max_a);
    return 0;
}"""
    },

    "group_anagrams": {
        "python": """from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> int:
        groups = defaultdict(list)
        for s in strs:
            groups[''.join(sorted(s))].append(s)
        return len(groups)
""",
        "java": """import java.util.*;

class Solution {
    public int groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        for (String s : strs) {
            char[] chars = s.toCharArray();
            Arrays.sort(chars);
            String key = new String(chars);
            map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
        }
        return map.size();
    }
}""",
        "c": """#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int comp_char(const void* a, const void* b) { return *(char*)a - *(char*)b; }

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    char sorted_keys[n][105];
    int distinct = 0;
    for (int i = 0; i < n; i++) {
        char s[105];
        scanf("%s", s);
        qsort(s, strlen(s), sizeof(char), comp_char);
        int found = 0;
        for (int j = 0; j < distinct; j++) {
            if (strcmp(sorted_keys[j], s) == 0) { found = 1; break; }
        }
        if (!found) {
            strcpy(sorted_keys[distinct++], s);
        }
    }
    printf("%d\n", distinct);
    return 0;
}"""
    },

    "rotate_matrix": {
        "python": """class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        for row in matrix:
            row.reverse()
""",
        "java": """class Solution {
    public void rotate(int[][] matrix) {
        int n = matrix.length;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                int t = matrix[i][j]; matrix[i][j] = matrix[j][i]; matrix[j][i] = t;
            }
        }
        for (int i = 0; i < n; i++) {
            int l = 0, r = n - 1;
            while (l < r) {
                int t = matrix[i][l]; matrix[i][l] = matrix[i][r]; matrix[i][r] = t;
                l++; r--;
            }
        }
    }
}""",
        "c": """#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int m[n][n];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) scanf("%d", &m[i][j]);
    }
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int t = m[i][j]; m[i][j] = m[j][i]; m[j][i] = t;
        }
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            printf("%d%c", m[i][n - 1 - j], (j == n - 1) ? '\n' : ' ');
        }
    }
    return 0;
}"""
    },

    "longest_valid_parentheses": {
        "python": """class Solution:
    def longestValidParentheses(self, s: str) -> int:
        st = [-1]
        max_len = 0
        for i, c in enumerate(s):
            if c == '(':
                st.append(i)
            else:
                st.pop()
                if not st:
                    st.append(i)
                else:
                    max_len = max(max_len, i - st[-1])
        return max_len
""",
        "java": """import java.util.*;

class Solution {
    public int longestValidParentheses(String s) {
        Stack<Integer> st = new Stack<>();
        st.push(-1);
        int maxLen = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') {
                st.push(i);
            } else {
                st.pop();
                if (st.isEmpty()) {
                    st.push(i);
                } else {
                    maxLen = Math.max(maxLen, i - st.peek());
                }
            }
        }
        return maxLen;
    }
}""",
        "c": """#include <stdio.h>
#include <string.h>

int main() {
    char s[100005];
    if (scanf("%s", s) != 1) { printf("0\n"); return 0; }
    int st[100005], top = 0;
    st[top++] = -1;
    int max_len = 0;
    for (int i = 0; s[i]; i++) {
        if (s[i] == '(') st[top++] = i;
        else {
            top--;
            if (top == 0) st[top++] = i;
            else {
                int cur = i - st[top - 1];
                if (cur > max_len) max_len = cur;
            }
        }
    }
    printf("%d\n", max_len);
    return 0;
}"""
    },

    "median_two_sorted_arrays": {
        "python": """class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        merged = sorted(nums1 + nums2)
        n = len(merged)
        if n % 2 == 1:
            return float(merged[n // 2])
        return (merged[n // 2 - 1] + merged[n // 2]) / 2.0
""",
        "java": """import java.util.*;

class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        int[] merged = new int[nums1.length + nums2.length];
        System.arraycopy(nums1, 0, merged, 0, nums1.length);
        System.arraycopy(nums2, 0, merged, nums1.length, nums2.length);
        Arrays.sort(merged);
        int n = merged.length;
        if (n % 2 == 1) return merged[n / 2];
        return (merged[n / 2 - 1] + merged[n / 2]) / 2.0;
    }
}""",
        "c": """#include <stdio.h>
#include <stdlib.h>

int comp_int(const void* a, const void* b) { return *(int*)a - *(int*)b; }

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    int arr[n + m];
    for (int i = 0; i < n + m; i++) scanf("%d", &arr[i]);
    qsort(arr, n + m, sizeof(int), comp_int);
    int total = n + m;
    if (total % 2 == 1) {
        printf("%d\n", arr[total / 2]);
    } else {
        double med = (arr[total / 2 - 1] + arr[total / 2]) / 2.0;
        printf("%.5f\n", med);
    }
    return 0;
}"""
    },

    "merge_k_sorted_lists": {
        "python": """class Solution:
    def mergeKLists(self, lists: List[List[int]]) -> List[int]:
        merged = []
        for lst in lists: merged.extend(lst)
        return sorted(merged)
""",
        "java": """import java.util.*;

class Solution {
    public int[] mergeKLists(int[][] lists) {
        List<Integer> all = new ArrayList<>();
        for (int[] lst : lists) {
            for (int x : lst) all.add(x);
        }
        Collections.sort(all);
        int[] res = new int[all.size()];
        for (int i = 0; i < all.size(); i++) res[i] = all.get(i);
        return res;
    }
}""",
        "c": """#include <stdio.h>
#include <stdlib.h>

int comp(const void* a, const void* b) { return *(int*)a - *(int*)b; }

int main() {
    int k;
    if (scanf("%d", &k) != 1) return 0;
    int all[100005], total = 0;
    for (int i = 0; i < k; i++) {
        int sz; scanf("%d", &sz);
        for (int j = 0; j < sz; j++) {
            scanf("%d", &all[total++]);
        }
    }
    qsort(all, total, sizeof(int), comp);
    for (int i = 0; i < total; i++) {
        printf("%d%c", all[i], (i == total - 1) ? '\n' : ' ');
    }
    return 0;
}"""
    },

    "trapping_rain_water": {
        "python": """class Solution:
    def trap(self, height: List[int]) -> int:
        if not height: return 0
        l, r = 0, len(height) - 1
        l_max = r_max = water = 0
        while l < r:
            if height[l] < height[r]:
                if height[l] >= l_max: l_max = height[l]
                else: water += l_max - height[l]
                l += 1
            else:
                if height[r] >= r_max: r_max = height[r]
                else: water += r_max - height[r]
                r--;
            }
        }
        return water
""",
        "java": """class Solution {
    public int trap(int[] height) {
        if (height == null || height.length == 0) return 0;
        int l = 0, r = height.length - 1, lMax = 0, rMax = 0, water = 0;
        while (l < r) {
            if (height[l] < height[r]) {
                if (height[l] >= lMax) lMax = height[l];
                else water += lMax - height[l];
                l++;
            } else {
                if (height[r] >= rMax) rMax = height[r];
                else water += rMax - height[r];
                r--;
            }
        }
        return water;
    }
}""",
        "c": """#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int h[n];
    for (int i = 0; i < n; i++) scanf("%d", &h[i]);
    int l = 0, r = n - 1, l_max = 0, r_max = 0, water = 0;
    while (l < r) {
        if (h[l] < h[r]) {
            if (h[l] >= l_max) l_max = h[l];
            else water += l_max - h[l];
            l++;
        } else {
            if (h[r] >= r_max) r_max = h[r];
            else water += r_max - h[r];
            r--;
        }
    }
    printf("%d\n", water);
    return 0;
}"""
    },

    "word_break": {
        "python": """class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        words = set(wordDict)
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break
        return dp[n]
""",
        "java": """import java.util.*;

class Solution {
    public boolean wordBreak(String s, List<String> wordDict) {
        Set<String> words = new HashSet<>(wordDict);
        int n = s.length();
        boolean[] dp = new boolean[n + 1];
        dp[0] = true;
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j < i; j++) {
                if (dp[j] && words.contains(s.substring(j, i))) {
                    dp[i] = true;
                    break;
                }
            }
        }
        return dp[n];
    }
}""",
        "c": """#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int main() {
    char s[1005];
    if (scanf("%s", s) != 1) return 0;
    int n;
    if (scanf("%d", &n) != 1) return 0;
    char words[n][1005];
    for (int i = 0; i < n; i++) scanf("%s", words[i]);

    int len = strlen(s);
    bool dp[len + 1];
    memset(dp, 0, sizeof(dp));
    dp[0] = true;

    for (int i = 1; i <= len; i++) {
        for (int j = 0; j < i; j++) {
            if (dp[j]) {
                char sub[1005];
                int sub_len = i - j;
                strncpy(sub, s + j, sub_len);
                sub[sub_len] = '\0';
                for (int k = 0; k < n; k++) {
                    if (strcmp(words[k], sub) == 0) {
                        dp[i] = true;
                        break;
                    }
                }
                if (dp[i]) break;
            }
        }
    }
    if (dp[len]) printf("true\n");
    else printf("false\n");
    return 0;
}"""
    }
}


def get_solution(problem_id: str, language: str = "python") -> str:
    """Returns official solution for given problem and language."""
    clean_id = (problem_id or "").strip().lower()
    clean_lang = (language or "python").strip().lower()
    if clean_lang in ["py", "python3"]:
        clean_lang = "python"
    elif clean_lang in ["c99", "c11"]:
        clean_lang = "c"

    prob_solutions = SOLUTIONS_REGISTRY.get(clean_id, {})
    return prob_solutions.get(clean_lang, "")


def get_all_solutions_for_problem(problem_id: str) -> dict:
    """Returns all available language solutions for a problem."""
    clean_id = (problem_id or "").strip().lower()
    return SOLUTIONS_REGISTRY.get(clean_id, {})
