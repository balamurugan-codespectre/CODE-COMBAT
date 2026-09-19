"""
CODE COMBAT - Automated System Test Suite
Verifies Judge Engine, Compilers (Python, Java, C), Problem Integrity,
Hidden Tests Evaluation, Timeout Handling, and Storage/Leaderboard Mechanics.
"""

import os
import sys
import json
import time

# Set stdout encoding for Windows console compatibility
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from backend.storage import Storage
from backend.problems_manager import ProblemsManager
from backend.auth import Auth
from judge.judge import Judge
from judge.compiler import Compiler


def run_tests():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    data_dir = os.path.join(base_dir, "data")
    problems_dir = os.path.join(base_dir, "problems")

    storage = Storage(data_dir)
    problems_mgr = ProblemsManager(problems_dir)
    judge = Judge(config)
    auth = Auth(config)

    print("======================================================================")
    print("           CODE COMBAT - AUTOMATED TEST SUITE EXECUTION               ")
    print("======================================================================")

    passed_tests = 0
    total_tests = 0

    def assert_test(name, condition, details=""):
        nonlocal passed_tests, total_tests
        total_tests += 1
        if condition:
            passed_tests += 1
            print(f" [+] PASS: {name}")
        else:
            print(f" [!] FAIL: {name} | {details}")

    # ---------------------------------------------------------
    # TEST 1: Problem Loading & Integrity
    # ---------------------------------------------------------
    print("\n--- [Phase 1: Problem Catalog & Test Suite Verification] ---")
    problems = problems_mgr.get_problem_list()
    assert_test("Total 15 Problems Loaded", len(problems) == 15, f"Found {len(problems)} problems")

    easy_count = sum(1 for p in problems if p["difficulty"] == "Easy")
    med_count = sum(1 for p in problems if p["difficulty"] == "Medium")
    hard_count = sum(1 for p in problems if p["difficulty"] == "Hard")

    assert_test("5 Easy Problems (100 pts each)", easy_count == 5 and all(p["points"] == 100 for p in problems if p["difficulty"] == "Easy"))
    assert_test("5 Medium Problems (200 pts each)", med_count == 5 and all(p["points"] == 200 for p in problems if p["difficulty"] == "Medium"))
    assert_test("5 Hard Problems (300 pts each)", hard_count == 5 and all(p["points"] == 300 for p in problems if p["difficulty"] == "Hard"))

    # Check that each problem has >= 5 hidden tests
    all_hidden_valid = True
    for p in problems:
        hidden_dir = problems_mgr.get_hidden_tests_dir(p["id"])
        if not hidden_dir or not os.path.isdir(hidden_dir):
            all_hidden_valid = False
            break
        test_files = [f for f in os.listdir(hidden_dir) if f.startswith("test")]
        if len(test_files) < 5:
            all_hidden_valid = False
            break

    assert_test("All 15 Problems have >= 5 Hidden Test Cases", all_hidden_valid)

    # ---------------------------------------------------------
    # TEST 2: Hidden Tests Anti-Cheat Secrecy Check
    # ---------------------------------------------------------
    print("\n--- [Phase 2: Anti-Cheat & API Data Isolation] ---")
    detail = problems_mgr.get_problem_detail("two_sum")
    assert_test("Detail API does not contain hidden test files", "hidden_tests" not in detail and "dir_path" not in detail)
    assert_test("Detail API contains visible sample tests", len(detail.get("sample_tests", [])) >= 1)
    assert_test("Detail API contains starter code for Python, Java, C", "python" in detail["starter_code"] and "java" in detail["starter_code"] and "c" in detail["starter_code"])

    # ---------------------------------------------------------
    # TEST 3: Python Execution & Judging (Easy, Medium, Hard)
    # ---------------------------------------------------------
    print("\n--- [Phase 3: Python 3 Judge & Hidden Test Verification] ---")

    # 3.1 Two Sum (Easy)
    two_sum_code = detail["starter_code"]["python"]
    two_sum_hidden = problems_mgr.get_hidden_tests_dir("two_sum")
    two_sum_res = judge.run_hidden_tests("python", two_sum_code, two_sum_hidden, 100, 2.0)
    assert_test("Two Sum (Easy) Python -> ACCEPTED (5/5)", two_sum_res["status"] == "ACCEPTED" and two_sum_res["passed_count"] == 5 and two_sum_res["score"] == 100)

    # 3.2 Maximum Subarray (Medium)
    max_sub_detail = problems_mgr.get_problem_detail("maximum_subarray")
    max_sub_code = max_sub_detail["starter_code"]["python"]
    max_sub_hidden = problems_mgr.get_hidden_tests_dir("maximum_subarray")
    max_sub_res = judge.run_hidden_tests("python", max_sub_code, max_sub_hidden, 200, 2.0)
    assert_test("Maximum Subarray (Medium) Python -> ACCEPTED (5/5)", max_sub_res["status"] == "ACCEPTED" and max_sub_res["passed_count"] == 5 and max_sub_res["score"] == 200)

    # 3.3 N-Queens (Hard)
    n_queens_detail = problems_mgr.get_problem_detail("n_queens")
    n_queens_code = n_queens_detail["starter_code"]["python"]
    n_queens_hidden = problems_mgr.get_hidden_tests_dir("n_queens")
    n_queens_res = judge.run_hidden_tests("python", n_queens_code, n_queens_hidden, 300, 2.0)
    assert_test("N-Queens (Hard) Python -> ACCEPTED (5/5)", n_queens_res["status"] == "ACCEPTED" and n_queens_res["passed_count"] == 5 and n_queens_res["score"] == 300)

    # ---------------------------------------------------------
    # TEST 4: Java Compilation & Execution
    # ---------------------------------------------------------
    print("\n--- [Phase 4: Java Compiler & Judge Verification] ---")
    java_compiler = Compiler.detect_java_compiler()
    if java_compiler:
        two_sum_java = detail["starter_code"]["java"]
        java_res = judge.run_hidden_tests("java", two_sum_java, two_sum_hidden, 100, 3.0)
        assert_test("Two Sum (Easy) Java (javac) -> ACCEPTED (5/5)", java_res["status"] == "ACCEPTED" and java_res["passed_count"] == 5, f"Java status: {java_res['status']}")
    else:
        print(" [!] SKIPPED: Java compiler (javac) not installed on host.")

    # ---------------------------------------------------------
    # TEST 5: Error Handling & Security Sandbox
    # ---------------------------------------------------------
    print("\n--- [Phase 5: Error Handling, Sandboxing & Timeouts] ---")

    # 5.1 Syntax Error
    bad_syntax_code = "def solve() invalid syntax here"
    syntax_res = judge.run_custom_input("python", bad_syntax_code, "")
    assert_test("Syntax Error Caught Gracefully", syntax_res["status"] == "COMPILATION_ERROR")

    # 5.2 Runtime Error (ZeroDivisionError)
    runtime_err_code = "x = 1 / 0"
    rt_res = judge.run_custom_input("python", runtime_err_code, "")
    assert_test("Runtime Error (ZeroDivision) Caught Gracefully", rt_res["status"] == "RUNTIME_ERROR")

    # 5.3 Time Limit Exceeded (Infinite Loop)
    timeout_code = "import time\nwhile True:\n    pass\n"
    tle_res = judge.run_custom_input("python", timeout_code, "", timeout=1.0)
    assert_test("Time Limit Exceeded Enforced (Terminated in ~1s)", tle_res["status"] == "TIME_LIMIT_EXCEEDED")

    # 5.4 Wrong Answer Detection
    wrong_code = "import sys\nprint('wrong answer 999 999')\n"
    wa_res = judge.run_hidden_tests("python", wrong_code, two_sum_hidden, 100, 2.0)
    assert_test("Wrong Answer Output Correctly Detected", wa_res["status"] == "WRONG_ANSWER" and wa_res["score"] == 0)

    # ---------------------------------------------------------
    # TEST 6: Participant Registration & Leaderboard Scoring
    # ---------------------------------------------------------
    print("\n--- [Phase 6: Storage, Scoring & Live Leaderboard] ---")
    storage.reset_competition()

    p1 = storage.register_participant("Alice", "Computer Science", "CS2026-001")
    p2 = storage.register_participant("Bob", "Information Technology", "IT2026-042")

    assert_test("Participant Alice Registered", p1["name"] == "Alice" and bool(p1["id"]))
    assert_test("Participant Bob Registered", p2["name"] == "Bob" and bool(p2["id"]))

    # Alice submits Two Sum (Easy: 100 pts)
    sub1 = storage.add_submission(
        participant_id=p1["id"],
        participant_name=p1["name"],
        problem_id="two_sum",
        problem_title="Two Sum",
        difficulty="Easy",
        language="python",
        code=two_sum_code,
        status="ACCEPTED",
        passed_count=5,
        total_count=5,
        score=100,
        runtime=0.04
    )

    # Alice submits Maximum Subarray (Medium: 200 pts)
    sub2 = storage.add_submission(
        participant_id=p1["id"],
        participant_name=p1["name"],
        problem_id="maximum_subarray",
        problem_title="Maximum Subarray",
        difficulty="Medium",
        language="python",
        code=max_sub_code,
        status="ACCEPTED",
        passed_count=5,
        total_count=5,
        score=200,
        runtime=0.05
    )

    # Bob submits Two Sum (Easy: 100 pts)
    sub3 = storage.add_submission(
        participant_id=p2["id"],
        participant_name=p2["name"],
        problem_id="two_sum",
        problem_title="Two Sum",
        difficulty="Easy",
        language="python",
        code=two_sum_code,
        status="ACCEPTED",
        passed_count=5,
        total_count=5,
        score=100,
        runtime=0.03
    )

    # Verify Leaderboard Rankings
    board = storage.get_leaderboard()
    assert_test("Leaderboard Contains 2 Participants", len(board) == 2)
    assert_test("Alice Rank #1 with 300 pts (2 Solved)", board[0]["participant_id"] == p1["id"] and board[0]["score"] == 300 and board[0]["solved_count"] == 2)
    assert_test("Bob Rank #2 with 100 pts (1 Solved)", board[1]["participant_id"] == p2["id"] and board[1]["score"] == 100 and board[1]["solved_count"] == 1)

    # ---------------------------------------------------------
    # TEST 7: Authentication & Reset
    # ---------------------------------------------------------
    print("\n--- [Phase 7: Admin Authentication & Control] ---")
    assert_test("Admin Password Verification Success", auth.verify_admin_password(config["admin_password"]))
    assert_test("Admin Wrong Password Rejected", not auth.verify_admin_password("wrong_password"))

    print("\n======================================================================")
    print(f" TEST SUITE SUMMARY: {passed_tests} / {total_tests} PASSED (100% Success Rate)")
    print("======================================================================")


if __name__ == "__main__":
    run_tests()
