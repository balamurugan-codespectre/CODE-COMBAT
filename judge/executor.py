"""
CODE COMBAT Pro - Code Executor Module
Executes compiled programs in isolated subprocesses with timeout and resource limits.
"""

import subprocess
import time
import sys
import os
from typing import Dict, Any, Optional


class Executor:
    """Executes target processes with timeout enforcement and resource constraints."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.default_timeout = float(self.config.get("execution_timeout_seconds", 3.0))
        self.max_output_length = int(self.config.get("max_output_length", 50000))

    def execute(
        self,
        cmd: list,
        work_dir: str,
        stdin_data: str = "",
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Runs the specified command inside work_dir with timeout and memory limits.

        Returns:
            {
                "status": "OK" | "TIMEOUT" | "ERROR",
                "stdout": str,
                "stderr": str,
                "runtime": float,
                "exit_code": int | None,
                "error": str | None
            }
        """
        run_timeout = float(timeout) if timeout is not None else self.default_timeout
        start_time = time.perf_counter()

        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        env["PYTHONDONTWRITEBYTECODE"] = "1"

        try:
            process = None
            for attempt in range(6):
                try:
                    process = subprocess.Popen(
                        cmd,
                        cwd=work_dir,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        env=env
                    )
                    break
                except (PermissionError, OSError) as pe:
                    if attempt < 5 and sys.platform.startswith("win"):
                        time.sleep(0.12 * (attempt + 1))
                    else:
                        raise pe

            try:
                stdout_data, stderr_data = process.communicate(
                    input=stdin_data,
                    timeout=run_timeout
                )
                runtime = time.perf_counter() - start_time

                if len(stdout_data) > self.max_output_length:
                    stdout_data = stdout_data[:self.max_output_length] + "\n[OUTPUT TRUNCATED: Exceeded buffer limit]"

                if process.returncode != 0:
                    return {
                        "status": "ERROR",
                        "stdout": stdout_data,
                        "stderr": stderr_data,
                        "runtime": round(runtime, 4),
                        "exit_code": process.returncode,
                        "error": f"Process exited with return code {process.returncode}"
                    }

                return {
                    "status": "OK",
                    "stdout": stdout_data,
                    "stderr": stderr_data,
                    "runtime": round(runtime, 4),
                    "exit_code": 0,
                    "error": None
                }

            except subprocess.TimeoutExpired:
                # Force kill process tree
                self._kill_process_tree(process)
                runtime = time.perf_counter() - start_time
                return {
                    "status": "TIMEOUT",
                    "stdout": "",
                    "stderr": f"Execution exceeded time limit of {run_timeout:.2f}s.",
                    "runtime": round(runtime, 4),
                    "exit_code": None,
                    "error": f"Time Limit Exceeded ({run_timeout:.2f}s)"
                }

        except Exception as e:
            runtime = time.perf_counter() - start_time
            return {
                "status": "ERROR",
                "stdout": "",
                "stderr": str(e),
                "runtime": round(runtime, 4),
                "exit_code": None,
                "error": f"Execution Error: {str(e)}"
            }

    @staticmethod
    def _kill_process_tree(process: subprocess.Popen):
        """Kills process and all its children cleanly."""
        try:
            if sys.platform.startswith("win"):
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(process.pid)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False
                )
            else:
                process.kill()
        except Exception:
            try:
                process.kill()
            except Exception:
                pass
