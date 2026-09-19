# CODE COMBAT — Offline Competitive Programming Platform

> **"Compete. Code. Conquer."**  
> A high-performance, 100% offline competitive coding challenge website prototype inspired by the workflow of HackerRank and LeetCode, built with an original developer dark UI, zero external web/CDN dependencies, and a real local judge engine.

---

## Key Features

- **100% Offline**: Requires zero internet connection, external APIs, CDNs, or external npm/pip dependencies at runtime. Runs purely on Python 3 standard library and custom CSS3/ES6 JavaScript.
- **Real Multi-Language Judge**:
  - **Python 3** (`python`)
  - **Java** (`javac` / `java`)
  - **C** (`gcc` / `clang`)
- **Three-Panel Coding Studio**:
  - *Left*: Rich problem statement, constraints, input/output format, and sample test cases.
  - *Center*: Interactive code editor with line numbers, auto-indentation, bracket completion, and language templates.
  - *Right*: Dual-mode test runner (Sample Tests, Custom Input sandbox, and Server-Side Hidden Test Case Judging).
- **15 Built-in Competitive Challenges**:
  - **5 Easy** (100 pts): *Two Sum*, *Reverse String*, *Palindrome Number*, *Find Maximum*, *Count Vowels*
  - **5 Medium** (200 pts): *Valid Parentheses*, *Maximum Subarray*, *Merge Intervals*, *Longest Substring*, *Rotate Array*
  - **5 Hard** (300 pts): *Binary Tree Traversal*, *Shortest Path in Graph*, *N-Queens*, *Word Ladder*, *Dijkstra's Algorithm*
- **Server-Side Hidden Test Cases**: 5+ hidden test files per problem. Secret test data is never leaked or sent to the client browser.
- **Live Leaderboard**: Real-time scoreboard with rank medals, difficulty breakdowns, submission speed tie-breaking, and duplicate submission prevention.
- **Competition Timer**: Persistent countdown timer with visual warning states (amber < 10 mins, pulsing red < 3 mins) and automatic submission expiration.
- **Admin Control Center**: Password-protected management dashboard for viewing participants, inspecting submissions, adding/deleting challenges, resetting competition data, and exporting results to JSON.

---

## System Requirements

- **Operating System**: Windows 10/11, Linux, or macOS.
- **Python**: Python 3.8 or higher.
- **Java (Optional)**: OpenJDK / Oracle JDK (for compiling Java solutions via `javac`).
- **C Compiler (Optional)**: GCC / MinGW-w64 or Clang (for compiling C solutions).

---

## Quickstart Guide

### 1. Launch the Server
Open your terminal inside the `code_combat` directory and run:

```bash
python main.py
```

The terminal will display the startup banner and server URL:

```
======================================================================
   CODE COMBAT - OFFLINE CODING CHALLENGE PLATFORM
   "Compete. Code. Conquer."
======================================================================
 [+] Offline Judge Engine : Ready (Python 3, Java, C)
 [+] Loaded Problems     : 15 challenges (Easy/Medium/Hard)
 [+] Competition Timer   : 90 minutes
 [+] Storage Database    : Local JSON in 'data/'
 [+] Admin Password      : 'admin123'
----------------------------------------------------------------------
 >> CODE COMBAT running at: http://127.0.0.1:8000
 >> Press Ctrl+C in this terminal to stop the server.
======================================================================
```

### 2. Access the Platform
Open your browser (Chrome, Edge, Firefox) and navigate to:
**[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## Participant Workflow

```
       [Home Landing Page]
                │
                ▼
      [Click "START CODING"]
                │
                ▼
   [Register Name, College, Reg No]
                │
                ▼
    [Problem Dashboard (Filters)]
                │
                ▼
    [Open Problem in Coding Studio]
                │
        ┌───────┴───────┐
        ▼               ▼
   [Run Code]     [Submit Code]
  (Sample Tests)  (Hidden Test Judge)
                        │
                        ▼
                [Passed: 5 / 5 ✓]
               [Score: +100 Points]
                        │
                        ▼
           [Live Leaderboard Updated]
```

---

## Project Structure

```
CODE_COMBAT/
├── main.py                     # Server entry point & ASCII banner launcher
├── config.json                 # Competition configuration & settings
├── test_suite.py               # Automated integration verification suite
├── generate_problems.py        # Problem generation utility
│
├── backend/                    # Core backend modules (Standard library HTTP & REST)
│   ├── __init__.py
│   ├── server.py               # Threaded HTTP server & REST endpoint router
│   ├── storage.py              # Local JSON database (participants, submissions, leaderboard)
│   ├── problems_manager.py     # Problem loader, schema validator, and admin manager
│   └── auth.py                 # Admin password verification & auth helpers
│
├── judge/                      # Local code execution & judging subsystem
│   ├── __init__.py
│   ├── compiler.py             # Compilers for C (gcc), Java (javac), syntax checks for Python
│   ├── executor.py             # Subprocess execution, timeout enforcement, output truncation
│   └── judge.py                # Output normalization, sample runner & hidden tests judge
│
├── problems/                   # Problem catalog categorized by difficulty
│   ├── easy/
│   │   ├── two_sum/
│   │   │   ├── problem.json    # Problem metadata, Markdown spec, starter codes, visible samples
│   │   │   ├── problem.txt     # Offline printable problem description
│   │   │   └── hidden_tests/   # Secret test cases evaluated on server
│   │   │       ├── test1.txt
│   │   │       ├── test2.txt
│   │   │       ├── test3.txt
│   │   │       ├── test4.txt
│   │   │       └── test5.txt
│   │   ├── reverse_string/
│   │   ├── palindrome_number/
│   │   ├── find_maximum/
│   │   └── count_vowels/
│   ├── medium/
│   │   ├── valid_parentheses/
│   │   ├── maximum_subarray/
│   │   ├── merge_intervals/
│   │   ├── longest_substring/
│   │   └── rotate_array/
│   └── hard/
│       ├── binary_tree/
│       ├── shortest_path/
│       ├── n_queens/
│       ├── word_ladder/
│       └── dijkstra_algorithm/
│
├── data/                       # Local JSON database storage
│   ├── participants.json       # Registered participant records
│   ├── submissions.json        # Detailed submission history
│   └── leaderboard.json        # Live computed rankings
│
└── frontend/                   # 100% Offline Dark Developer Single Page Application
    ├── index.html              # HTML5 application shell & view templates
    ├── css/
    │   └── style.css           # Custom dark cyber/developer stylesheet
    └── js/
        ├── app.js              # SPA router, state manager, timer & API integration
        ├── editor.js           # Line-numbered interactive code editor
        └── admin.js            # Admin dashboard logic (CRUD, reset, data export)
```

---

## How Hidden Test Cases Work

1. **Server-Side Isolation**: Hidden test cases reside exclusively inside `problems/<tier>/<problem_id>/hidden_tests/` on the server filesystem.
2. **Zero Leakage**: When the frontend requests problem details via `GET /api/problems/:id`, the server returns only the visible description and sample examples.
3. **Execution on Submit**: When a participant clicks **Submit Code**, the backend compiles the code and executes each hidden test case file sequentially.
4. **Result Sanitization**: The judge returns only high-level summary metrics (`passed_count`, `total_count`, `status`, `score`, `runtime`). Secret inputs and expected outputs are never returned over HTTP.

---

## How to Add New Problems

You can add problems either through the **Admin Panel** in the UI or directly in the filesystem:

### Filesystem Method:
1. Create a directory inside `problems/easy/`, `problems/medium/`, or `problems/hard/`, e.g., `problems/easy/my_new_problem/`.
2. Create `problem.json`:
```json
{
  "id": "my_new_problem",
  "title": "My New Challenge",
  "difficulty": "Easy",
  "points": 100,
  "time_limit": 2.0,
  "category": "Math",
  "description": "Problem description in Markdown format...",
  "input_format": "Input format specification...",
  "output_format": "Output format specification...",
  "constraints": "1 <= N <= 10^5",
  "sample_tests": [
    {
      "input": "5",
      "output": "25",
      "explanation": "5 squared is 25."
    }
  ],
  "starter_code": {
    "python": "import sys\n\ndef solve():\n    n = int(sys.stdin.read().strip())\n    print(n * n)\n\nif __name__ == '__main__':\n    solve()\n",
    "java": "import java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        System.out.println(n * n);\n    }\n}\n",
    "c": "#include <stdio.h>\n\nint main() {\n    int n;\n    if (scanf(\"%d\", &n) == 1) printf(\"%d\\n\", n * n);\n    return 0;\n}\n"
  }
}
```
3. Create `hidden_tests/` subdirectory with `test1.txt`, `test2.txt`, etc.:
```text
INPUT:
10
EXPECTED:
100
```
4. Restart the server or click reload in Admin Panel.

---

## Configuration Options (`config.json`)

```json
{
  "competition_name": "CODE COMBAT",
  "tagline": "Compete. Code. Conquer.",
  "competition_duration_minutes": 90,
  "admin_password": "admin123",
  "server_port": 8000,
  "server_host": "127.0.0.1",
  "execution_timeout_seconds": 3.0,
  "max_output_length": 50000
}
```

---

## Running the Automated Test Suite

To run the complete automated test suite verifying compilers, judge execution, timeout kills, and leaderboard calculations:

```bash
python test_suite.py
```

Expected output:
```
======================================================================
 TEST SUITE SUMMARY: 23 / 23 PASSED (100% Success Rate)
======================================================================
```

---

## Security & Sandboxing Notice

> [!IMPORTANT]
> - **Prototype Scope**: This platform executes participant code locally using subprocess execution with strict timeouts (2.0–3.0s), temporary execution directories, and output size caps.
> - **Production Deployment**: Production deployment in untrusted public environments requires container/VM sandboxing such as **Docker**, **nsjail**, or **isolate** for kernel-level resource and syscall isolation. This prototype is designed for controlled college lab and offline contest environments.
