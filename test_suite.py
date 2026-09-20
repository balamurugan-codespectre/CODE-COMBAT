"""
CODE COMBAT Pro - Comprehensive System Test Suite
Verifies Judge Engine, Compilers (Python, Java, C), Problem Integrity,
Hidden Tests Evaluation, Timeouts & Process Sandboxing, SQLite WAL Storage,
HMAC Authentication, and Live Leaderboard Mechanics.
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
from backend.server import RateLimiter
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
    print("      ⚔️ CODE COMBAT PRO - COMPREHENSIVE AUTOMATED TEST SUITE        ")
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
    # TEST 1: Problem Loading & Catalog Integrity
    # ---------------------------------------------------------
    print("\n--- [Phase 1: Problem Catalog & Test Suite Integrity] ---")
    problems = problems_mgr.get_problem_list()
    assert_test("Total 15 Problems Loaded", len(problems) == 15, f"Found {len(problems)} problems")

    easy_count = sum(1 for p in problems if p["difficulty"] == "Easy")
    med_count = sum(1 for p in problems if p["difficulty"] == "Medium")
    hard_count = sum(1 for p in problems if p["difficulty"] == "Hard")

    assert_test("5 Easy Problems (100 pts each)", easy_count == 5 and all(p["points"] == 100 for p in problems if p["difficulty"] == "Easy"))
    assert_test("5 Medium Problems (200 pts each)", med_count == 5 and all(p["points"] == 200 for p in problems if p["difficulty"] == "Medium"))
    assert_test("5 Hard Problems (300 pts each)", hard_count == 5 and all(p["points"] == 300 for p in problems if p["difficulty"] == "Hard"))

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
    # TEST 2: Anti-Cheat & API Data Isolation
    # ---------------------------------------------------------
    print("\n--- [Phase 2: Anti-Cheat & API Data Isolation] ---")
    detail = problems_mgr.get_problem_detail("two_sum")
    assert_test("Detail API does not contain hidden test files", "hidden_tests" not in detail and "dir_path" not in detail)
    assert_test("Detail API contains visible sample tests", len(detail.get("sample_tests", [])) >= 1)
    assert_test("Detail API contains starter code for Python, Java, C", "python" in detail["starter_code"] and "java" in detail["starter_code"] and "c" in detail["starter_code"])

    # ---------------------------------------------------------
    # TEST 3: Multi-Language Compilers & Execution
    # ---------------------------------------------------------
    print("\n--- [Phase 3: Multi-Language Compilers & Execution] ---")

    # 3.1 Python 3 execution
    py_hidden_dir = problems_mgr.get_hidden_tests_dir("two_sum")
    res_py = judge.run_hidden_tests("python", detail["starter_code"]["python"], py_hidden_dir, 100, 3.0)
    assert_test("Python 3 Judge: Two Sum -> ACCEPTED (5/5)", res_py["status"] == "ACCEPTED" and res_py["passed_count"] == 5, f"status={res_py.get('status')}, error={res_py.get('error_message')}")

    # 3.2 Java (javac) execution
    res_java = judge.run_hidden_tests("java", detail["starter_code"]["java"], py_hidden_dir, 100, 3.0)
    assert_test("Java (javac) Judge: Two Sum -> ACCEPTED (5/5)", res_java["status"] == "ACCEPTED" and res_java["passed_count"] == 5, f"status={res_java.get('status')}, error={res_java.get('error_message')}")

    # 3.3 C compiler detection & execution
    c_compiler = Compiler.detect_c_compiler()
    if c_compiler:
        res_c = judge.run_hidden_tests("c", detail["starter_code"]["c"], py_hidden_dir, 100, 3.0)
        assert_test(f"C ({os.path.basename(c_compiler)}) Judge: Two Sum -> ACCEPTED (5/5)", res_c["status"] == "ACCEPTED" and res_c["passed_count"] == 5, f"status={res_c.get('status')}, error={res_c.get('error_message')}")
    else:
        assert_test("C compiler not available (optional on Windows host)", True)

    # ---------------------------------------------------------
    # TEST 4: Error Handling & Subprocess Sandboxing
    # ---------------------------------------------------------
    print("\n--- [Phase 4: Error Handling, Sandboxing & Timeouts] ---")

    # Syntax Error
    syntax_err_code = "def solve(\n  broken code here"
    res_syn = judge.run_custom_input("python", syntax_err_code, "")
    assert_test("Syntax Error Caught Gracefully", res_syn["status"] == "COMPILATION_ERROR" and "SyntaxError" in res_syn["stderr"])

    # Runtime Error
    runtime_err_code = "print(10 / 0)"
    res_rt = judge.run_custom_input("python", runtime_err_code, "")
    assert_test("Runtime Error (ZeroDivision) Caught Gracefully", res_rt["status"] == "RUNTIME_ERROR" and "ZeroDivisionError" in res_rt["stderr"])

    # Timeout
    infinite_loop_code = "import time\nwhile True:\n    time.sleep(0.1)"
    start_t = time.time()
    res_to = judge.run_custom_input("python", infinite_loop_code, "", timeout=1.0)
    elapsed = time.time() - start_t
    assert_test(f"Time Limit Exceeded Enforced ({elapsed:.2f}s)", res_to["status"] == "TIME_LIMIT_EXCEEDED" and elapsed < 2.5)

    # ---------------------------------------------------------
    # TEST 5: Dual Persistence (SQLite WAL & JSON Mirrors)
    # ---------------------------------------------------------
    print("\n--- [Phase 5: Dual ACID Storage & Leaderboard Engine] ---")
    storage.reset_competition()

    p_alice = storage.register_participant("Alice Smith", "Oxford University", "OX101")
    p_bob = storage.register_participant("Bob Johnson", "Cambridge", "CB202")

    assert_test("Participant Alice Registered", p_alice["id"] is not None and p_alice["reg_no"] == "OX101")
    assert_test("Participant Bob Registered", p_bob["id"] is not None and p_bob["reg_no"] == "CB202")

    # Alice solves two_sum (100) & maximum_subarray (200) -> 300 pts
    prob_med = problems_mgr.get_problem_detail("maximum_subarray")
    storage.add_submission(
        participant_id=p_alice["id"],
        participant_name=p_alice["name"],
        problem_id="two_sum",
        problem_title=detail["title"],
        difficulty="Easy",
        language="python",
        code="...",
        status="ACCEPTED",
        passed_count=5,
        total_count=5,
        score=100,
        runtime=0.035
    )
    storage.add_submission(
        participant_id=p_alice["id"],
        participant_name=p_alice["name"],
        problem_id="maximum_subarray",
        problem_title=prob_med["title"],
        difficulty="Medium",
        language="python",
        code="...",
        status="ACCEPTED",
        passed_count=5,
        total_count=5,
        score=200,
        runtime=0.045
    )

    # Bob solves two_sum (100) -> 100 pts
    storage.add_submission(
        participant_id=p_bob["id"],
        participant_name=p_bob["name"],
        problem_id="two_sum",
        problem_title=detail["title"],
        difficulty="Easy",
        language="python",
        code="...",
        status="ACCEPTED",
        passed_count=5,
        total_count=5,
        score=100,
        runtime=0.050
    )

    leaderboard = storage.get_leaderboard()
    assert_test("Leaderboard contains exactly 2 active participants", len(leaderboard) == 2)
    assert_test("Alice is Rank #1 with 300 pts (2 Solved)", leaderboard[0]["name"] == "Alice Smith" and leaderboard[0]["score"] == 300 and leaderboard[0]["solved_count"] == 2)
    assert_test("Bob is Rank #2 with 100 pts (1 Solved)", leaderboard[1]["name"] == "Bob Johnson" and leaderboard[1]["score"] == 100 and leaderboard[1]["solved_count"] == 1)

    # Verify JSON mirrors exist
    assert_test("JSON Mirrors Synced on Disk", os.path.exists(storage.participants_file) and os.path.exists(storage.leaderboard_file))

    # ---------------------------------------------------------
    # TEST 6: Cryptographic Auth & Rate Limiter
    # ---------------------------------------------------------
    print("\n--- [Phase 6: Cryptographic Security & Rate Limiting] ---")
    token = auth.create_session_token("usr_test123", "Tester Alice")
    verified = auth.verify_session_token(token)
    assert_test("HMAC Session Token Created & Verified", verified is not None and verified["pid"] == "usr_test123")

    tampered_token = token[:-5] + "XXXXX"
    tampered_ver = auth.verify_session_token(tampered_token)
    assert_test("Tampered HMAC Token Rejected", tampered_ver is None)

    assert_test("Admin Password Verification Success", auth.verify_admin_password(config.get("admin_password", "admin123")))
    assert_test("Admin ID & Password Verification Success", auth.verify_admin_credentials("admin", config.get("admin_password", "admin123")))
    assert_test("Admin Wrong Password Rejected", not auth.verify_admin_credentials("admin", "wrong_password"))
    assert_test("Admin Wrong ID Rejected", not auth.verify_admin_credentials("wrong_admin", config.get("admin_password", "admin123")))

    # Rate Limiter test
    limiter = RateLimiter(max_requests=5, window_seconds=60)
    for _ in range(5):
        limiter.is_allowed("127.0.0.1")
    assert_test("Rate Limiter Blocks Burst Requests Exceeding Limit", not limiter.is_allowed("127.0.0.1"))

    # ---------------------------------------------------------
    # TEST 7: Complete Admin Reset (Wipe Points, Submissions & Leaderboard)
    # ---------------------------------------------------------
    print("\n--- [Phase 7: Full Admin Reset & Zero State Validation] ---")
    storage.reset_competition()
    
    empty_lb = storage.get_leaderboard()
    empty_parts = storage.get_participants()
    empty_subs = storage.get_submissions()
    
    assert_test("Admin Reset: Leaderboard completely emptied (0 entries)", len(empty_lb) == 0)
    assert_test("Admin Reset: Participants table wiped (0 entries)", len(empty_parts) == 0)
    assert_test("Admin Reset: Submissions table wiped (0 entries)", len(empty_subs) == 0)
    
    # Read JSON mirror directly from disk
    with open(storage.leaderboard_file, "r", encoding="utf-8") as f:
        lb_json = json.load(f)
    assert_test("Admin Reset: JSON mirror for leaderboard is empty list []", lb_json == [])
    
    # Fresh registration starts at 0 points
    p_fresh = storage.register_participant("Charlie Test", "MIT", "MIT001")
    assert_test("Fresh Participant after Reset starts with Score = 0", p_fresh["score"] == 0 and len(p_fresh["solved_problems"]) == 0)

    # Clean up after test
    storage.reset_competition()

    # ---------------------------------------------------------
    # TEST 8: Problem Set Switching & Admin Credentials Management
    # ---------------------------------------------------------
    print("\n--- [Phase 8: Problem Set Switching & Password Management] ---")
    available_sets = problems_mgr.get_available_sets()
    assert_test("Multiple Problem Sets Available (Set 1 & Set 2)", len(available_sets) >= 2)

    # Switch to Set 2
    switched_to_set2 = problems_mgr.switch_set("set2")
    set2_problems = problems_mgr.get_problem_list()
    assert_test("Switched to Problem Set 2", switched_to_set2 and problems_mgr.active_set == "set2")
    assert_test("Set 2 contains 15 valid problems", len(set2_problems) == 15)

    # Switch back to Set 1
    switched_to_set1 = problems_mgr.switch_set("set1")
    set1_problems = problems_mgr.get_problem_list()
    assert_test("Switched back to Problem Set 1", switched_to_set1 and problems_mgr.active_set == "set1")
    assert_test("Set 1 contains 15 valid problems", len(set1_problems) == 15)

    # Credentials Update (ID + Password)
    original_id = config.get("admin_id", "admin")
    original_pass = config.get("admin_password", "admin123")
    auth.update_admin_credentials(new_id="superadmin", new_password="new_secure_pass_456")
    # Revert credentials
    auth.update_admin_credentials(new_id=original_id, new_password=original_pass)
    assert_test("Admin Credentials Reverted Successfully", auth.verify_admin_credentials(original_id, original_pass))

    # ---------------------------------------------------------
    # TEST 9: 3-Tier Progressive Hints & Score Deduction Mechanics
    # ---------------------------------------------------------
    print("\n--- [Phase 9: 3-Tier Progressive Hints & Score Deductions] ---")
    storage.reset_competition()
    p_player = storage.register_participant("David HintTester", "Stanford", "ST101")

    # 9.1 Verify all Set 1 problems have 3 hints and valid difficulty penalties
    set1_all_3_hints = True
    for prob in problems_mgr.get_problem_list():
        d = problems_mgr.get_problem_detail(prob["id"])
        hints = d.get("hints", [])
        if len(hints) != 3:
            set1_all_3_hints = False
            break
        # Locked hints must NOT leak text
        if any(h["text"] is not None for h in hints if not h["unlocked"]):
            set1_all_3_hints = False
            break
    assert_test("All 15 Set 1 Problems have 3 Progressive Hints (text secured when locked)", set1_all_3_hints)

    # 9.2 Test penalty values
    assert_test("Easy Problem Penalties: H1=10, H2=15, H3=25", 
                problems_mgr.get_hint_penalty("Easy", 1) == 10 and
                problems_mgr.get_hint_penalty("Easy", 2) == 15 and
                problems_mgr.get_hint_penalty("Easy", 3) == 25)
    assert_test("Medium Problem Penalties: H1=20, H2=30, H3=50", 
                problems_mgr.get_hint_penalty("Medium", 1) == 20 and
                problems_mgr.get_hint_penalty("Medium", 2) == 30 and
                problems_mgr.get_hint_penalty("Medium", 3) == 50)
    assert_test("Hard Problem Penalties: H1=30, H2=45, H3=75", 
                problems_mgr.get_hint_penalty("Hard", 1) == 30 and
                problems_mgr.get_hint_penalty("Hard", 2) == 45 and
                problems_mgr.get_hint_penalty("Hard", 3) == 75)

    # 9.3 Unlock Hint 1 on Easy problem (Two Sum: 100 pts -> 90 pts)
    storage.unlock_hint(p_player["id"], "two_sum", 1, 10)
    unlocked = storage.get_unlocked_hints(p_player["id"], "two_sum")
    pen1 = storage.get_total_hint_penalty(p_player["id"], "two_sum")
    assert_test("Hint 1 Unlocked & Recorded in SQLite Storage", unlocked == [1] and pen1 == 10)

    # Detail API reflects unlocked hint text and reduced max score
    p_detail = problems_mgr.get_problem_detail("two_sum", participant_id=p_player["id"], storage=storage)
    assert_test("Detail API: Max Score is 90 / 100 pts with Hint 1 text revealed",
                p_detail["max_score"] == 90 and
                p_detail["total_hint_penalty"] == 10 and
                p_detail["hints"][0]["unlocked"] is True and
                isinstance(p_detail["hints"][0]["text"], str) and
                p_detail["hints"][1]["unlocked"] is False)

    # 9.4 Submission awards 90 pts instead of 100 pts
    two_sum_dir = problems_mgr.get_hidden_tests_dir("two_sum")
    effective_pts = max(25, 100 - pen1)
    sub_res = judge.run_hidden_tests("python", p_detail["starter_code"]["python"], two_sum_dir, effective_pts, 3.0)
    sub_rec = storage.add_submission(
        participant_id=p_player["id"],
        participant_name=p_player["name"],
        problem_id="two_sum",
        problem_title=p_detail["title"],
        difficulty="Easy",
        language="python",
        code=p_detail["starter_code"]["python"],
        status=sub_res["status"],
        passed_count=sub_res["passed_count"],
        total_count=sub_res["total_count"],
        score=sub_res["score"],
        runtime=sub_res["runtime"]
    )
    lb_after_hint = storage.get_leaderboard()
    assert_test("Player Earned Exactly 90 pts on Two Sum with Hint 1 Deduction",
                sub_res["score"] == 90 and lb_after_hint[0]["score"] == 90)

    # 9.5 Unlock all 3 hints on Medium problem (Max Subarray: 200 pts - 100 pts penalty = 100 pts)
    storage.unlock_hint(p_player["id"], "maximum_subarray", 1, 20)
    storage.unlock_hint(p_player["id"], "maximum_subarray", 2, 30)
    storage.unlock_hint(p_player["id"], "maximum_subarray", 3, 50)
    total_med_pen = storage.get_total_hint_penalty(p_player["id"], "maximum_subarray")
    assert_test("Medium Problem All 3 Hints Unlocked: Penalty = 100 pts", total_med_pen == 100)

    med_detail = problems_mgr.get_problem_detail("maximum_subarray", participant_id=p_player["id"], storage=storage)
    assert_test("Medium Detail API: Max Score is 100 / 200 pts with all 3 hints revealed",
                med_detail["max_score"] == 100 and
                all(h["unlocked"] is True and h["text"] for h in med_detail["hints"]))

    # Cleanup test db
    storage.reset_competition()
    assert_test("Reset Competition wipes hint unlocks", len(storage.get_unlocked_hints(p_player["id"], "two_sum")) == 0)

    # ---------------------------------------------------------
    # FINAL SUMMARY
    # ---------------------------------------------------------
    print("\n======================================================================")
    print(f" 🎯 TEST SUITE SUMMARY: {passed_tests} / {total_tests} PASSED ({(passed_tests/total_tests)*100:.1f}%)")
    print("======================================================================")

    if passed_tests == total_tests:
        print(" [✓] ALL PRODUCTION CRITERIA SATISFIED — CODE COMBAT PRO READY!")
        return 0
    else:
        print(" [!] SOME TESTS FAILED.")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
