"""
CODE COMBAT - Test Case Judge Engine
Evaluates submissions against visible sample tests and server-side hidden test cases.
"""

import os
import glob
import tempfile
import shutil
from typing import Dict, Any, List, Optional, Tuple

from .compiler import Compiler
from .executor import Executor


class Judge:
    """Orchestrates compilation, execution, and evaluation against test cases."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.compiler = Compiler(self.config)
        self.executor = Executor(self.config)

    @staticmethod
    def normalize_output(text: str) -> str:
        """Standardizes line breaks, strips trailing whitespace per line and trailing empty lines."""
        if not text:
            return ""
        lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        # Strip right whitespace on each line
        stripped_lines = [line.rstrip() for line in lines]
        # Remove trailing empty lines
        while stripped_lines and stripped_lines[-1] == "":
            stripped_lines.pop()
        return "\n".join(stripped_lines)

    @staticmethod
    def parse_test_file(file_path: str) -> Tuple[str, str]:
        """
        Parses a test case file formatted with INPUT: and EXPECTED: headers.
        Falls back to standard text parsing if headers are not present.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "INPUT:" in content and "EXPECTED:" in content:
            parts = content.split("EXPECTED:")
            input_part = parts[0].replace("INPUT:", "").strip("\r\n")
            expected_part = parts[1].strip("\r\n")
            return input_part, expected_part
        elif "---INPUT---" in content and "---OUTPUT---" in content:
            parts = content.split("---OUTPUT---")
            input_part = parts[0].replace("---INPUT---", "").strip("\r\n")
            expected_part = parts[1].strip("\r\n")
            return input_part, expected_part
        else:
            # Fallback
            return content.strip(), ""

    def run_custom_input(
        self,
        language: str,
        code: str,
        custom_input: str = "",
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """Executes participant code against arbitrary custom input."""
        temp_dir = tempfile.mkdtemp(prefix="codecombat_custom_")
        try:
            # 1. Compile
            compile_ok, compile_err, meta = self.compiler.compile(language, code, temp_dir)
            if not compile_ok:
                return {
                    "status": "COMPILATION_ERROR",
                    "stdout": "",
                    "stderr": compile_err or "Compilation Error",
                    "runtime": 0.0,
                    "error": compile_err
                }

            # 2. Execute
            exec_res = self.executor.execute(
                cmd=meta["cmd"],
                work_dir=temp_dir,
                stdin_data=custom_input,
                timeout=timeout
            )

            status_map = {
                "OK": "SUCCESS",
                "TIMEOUT": "TIME_LIMIT_EXCEEDED",
                "ERROR": "RUNTIME_ERROR"
            }
            return {
                "status": status_map.get(exec_res["status"], "RUNTIME_ERROR"),
                "stdout": exec_res["stdout"],
                "stderr": exec_res["stderr"],
                "runtime": exec_res["runtime"],
                "error": exec_res.get("error")
            }
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def run_sample_tests(
        self,
        language: str,
        code: str,
        sample_tests: List[Dict[str, str]],
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Executes participant code against visible sample test cases.
        Returns full actual vs expected details for user feedback.
        """
        temp_dir = tempfile.mkdtemp(prefix="codecombat_sample_")
        try:
            # 1. Compile
            compile_ok, compile_err, meta = self.compiler.compile(language, code, temp_dir)
            if not compile_ok:
                return {
                    "status": "COMPILATION_ERROR",
                    "compilation_error": compile_err,
                    "results": [],
                    "all_passed": False
                }

            results = []
            all_passed = True

            for idx, test in enumerate(sample_tests, start=1):
                input_data = test.get("input", "")
                expected_output = test.get("output", "")
                explanation = test.get("explanation", "")

                exec_res = self.executor.execute(
                    cmd=meta["cmd"],
                    work_dir=temp_dir,
                    stdin_data=input_data,
                    timeout=timeout
                )

                if exec_res["status"] == "TIMEOUT":
                    results.append({
                        "test_case": idx,
                        "passed": False,
                        "status": "TIME_LIMIT_EXCEEDED",
                        "input": input_data,
                        "expected": expected_output,
                        "actual": "",
                        "stdout": "",
                        "stderr": exec_res["stderr"],
                        "runtime": exec_res["runtime"],
                        "explanation": explanation
                    })
                    all_passed = False
                elif exec_res["status"] == "ERROR":
                    results.append({
                        "test_case": idx,
                        "passed": False,
                        "status": "RUNTIME_ERROR",
                        "input": input_data,
                        "expected": expected_output,
                        "actual": exec_res["stdout"],
                        "stdout": exec_res["stdout"],
                        "stderr": exec_res["stderr"],
                        "runtime": exec_res["runtime"],
                        "explanation": explanation
                    })
                    all_passed = False
                else:
                    norm_actual = self.normalize_output(exec_res["stdout"])
                    norm_expected = self.normalize_output(expected_output)
                    passed = (norm_actual == norm_expected)

                    if not passed:
                        all_passed = False

                    results.append({
                        "test_case": idx,
                        "passed": passed,
                        "status": "PASSED" if passed else "WRONG_ANSWER",
                        "input": input_data,
                        "expected": expected_output,
                        "actual": norm_actual,
                        "stdout": exec_res["stdout"],
                        "stderr": exec_res["stderr"],
                        "runtime": exec_res["runtime"],
                        "explanation": explanation
                    })

            return {
                "status": "ACCEPTED" if all_passed else "FAILED",
                "compilation_error": None,
                "results": results,
                "all_passed": all_passed
            }
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def run_hidden_tests(
        self,
        language: str,
        code: str,
        hidden_tests_dir: str,
        problem_points: int = 100,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Judges a submission against server-side hidden test cases.
        IMPORTANT: Never exposes hidden test case inputs or expected outputs in the return value.
        """
        temp_dir = tempfile.mkdtemp(prefix="codecombat_submit_")
        try:
            # 1. Compile
            compile_ok, compile_err, meta = self.compiler.compile(language, code, temp_dir)
            if not compile_ok:
                return {
                    "status": "COMPILATION_ERROR",
                    "passed_count": 0,
                    "total_count": 0,
                    "score": 0,
                    "runtime": 0.0,
                    "error_message": compile_err or "Compilation Error"
                }

            # 2. Discover hidden test files
            if not os.path.isdir(hidden_tests_dir):
                return {
                    "status": "JUDGE_ERROR",
                    "passed_count": 0,
                    "total_count": 0,
                    "score": 0,
                    "runtime": 0.0,
                    "error_message": "Hidden tests directory not found on server."
                }

            test_files = sorted(
                glob.glob(os.path.join(hidden_tests_dir, "test*.txt")),
                key=lambda p: int(''.join(filter(str.isdigit, os.path.basename(p))) or '0')
            )

            if not test_files:
                return {
                    "status": "JUDGE_ERROR",
                    "passed_count": 0,
                    "total_count": 0,
                    "score": 0,
                    "runtime": 0.0,
                    "error_message": "No hidden test cases found for this problem."
                }

            total_count = len(test_files)
            passed_count = 0
            max_runtime = 0.0
            overall_verdict = "ACCEPTED"
            first_error_msg = None

            for file_path in test_files:
                input_data, expected_output = self.parse_test_file(file_path)

                exec_res = self.executor.execute(
                    cmd=meta["cmd"],
                    work_dir=temp_dir,
                    stdin_data=input_data,
                    timeout=timeout
                )

                max_runtime = max(max_runtime, exec_res["runtime"])

                if exec_res["status"] == "TIMEOUT":
                    if overall_verdict == "ACCEPTED":
                        overall_verdict = "TIME_LIMIT_EXCEEDED"
                        first_error_msg = f"Time Limit Exceeded on test case {passed_count + 1}"
                    # Don't break immediately or break to save time
                    break
                elif exec_res["status"] == "ERROR":
                    if overall_verdict == "ACCEPTED":
                        overall_verdict = "RUNTIME_ERROR"
                        first_error_msg = exec_res.get("stderr") or f"Runtime error on test case {passed_count + 1}"
                    break
                else:
                    norm_actual = self.normalize_output(exec_res["stdout"])
                    norm_expected = self.normalize_output(expected_output)

                    if norm_actual == norm_expected:
                        passed_count += 1
                    else:
                        if overall_verdict == "ACCEPTED":
                            overall_verdict = "WRONG_ANSWER"
                            first_error_msg = f"Wrong Answer on test case {passed_count + 1}"
                        # In competitive programming, we can stop at first wrong answer or evaluate all
                        # We stop at first failure for efficiency
                        break

            is_accepted = (passed_count == total_count and overall_verdict == "ACCEPTED")
            score_earned = problem_points if is_accepted else 0

            return {
                "status": "ACCEPTED" if is_accepted else overall_verdict,
                "passed_count": passed_count,
                "total_count": total_count,
                "score": score_earned,
                "runtime": round(max_runtime, 4),
                "error_message": None if is_accepted else first_error_msg
            }
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
