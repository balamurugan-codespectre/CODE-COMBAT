"""
CODE COMBAT - Code Executor Module
Executes compiled programs in controlled isolated subprocesses with timeout and memory limits.
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
        self.default_timeout = self.config.get("execution_timeout_seconds", 3.0)
        self.max_output_length = self.config.get("max_output_length", 50000)

    def execute(
        self,
        cmd: list,
        work_dir: str,
        stdin_data: str = "",
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Runs the specified command inside work_dir.

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
        run_timeout = timeout if timeout is not None else self.default_timeout
        start_time = time.perf_counter()
        
        # Prepare environment (prevent buffer lag in python, strip sensitive env if needed)
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        env["PYTHONDONTWRITEBYTECODE"] = "1"

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

            try:
                stdout_data, stderr_data = process.communicate(
                    input=stdin_data,
                    timeout=run_timeout
                )
                runtime = time.perf_counter() - start_time
                exit_code = process.returncode

                # Truncate if output is too massive
                if len(stdout_data) > self.max_output_length:
                    stdout_data = stdout_data[:self.max_output_length] + "\n...[Output truncated due to size limit]"
                if len(stderr_data) > self.max_output_length:
                    stderr_data = stderr_data[:self.max_output_length] + "\n...[Error output truncated]"

                if exit_code != 0:
                    return {
                        "status": "ERROR",
                        "stdout": stdout_data,
                        "stderr": stderr_data.strip(),
                        "runtime": round(runtime, 4),
                        "exit_code": exit_code,
                        "error": stderr_data.strip() or f"Process exited with non-zero code {exit_code}"
                    }

                return {
                    "status": "OK",
                    "stdout": stdout_data,
                    "stderr": stderr_data.strip(),
                    "runtime": round(runtime, 4),
                    "exit_code": exit_code,
                    "error": None
                }

            except subprocess.TimeoutExpired:
                # Forcefully terminate process and all child processes
                self._terminate_process(process)
                runtime = time.perf_counter() - start_time
                return {
                    "status": "TIMEOUT",
                    "stdout": "",
                    "stderr": f"Time Limit Exceeded ({run_timeout}s)",
                    "runtime": round(runtime, 4),
                    "exit_code": None,
                    "error": f"Time Limit Exceeded: Execution took longer than {run_timeout} seconds."
                }

        except Exception as e:
            runtime = time.perf_counter() - start_time
            return {
                "status": "ERROR",
                "stdout": "",
                "stderr": str(e),
                "runtime": round(runtime, 4),
                "exit_code": -1,
                "error": f"Execution failed to launch: {str(e)}"
            }

    def _terminate_process(self, process: subprocess.Popen):
        """Cleanly terminates a process tree."""
        try:
            if sys.platform.startswith("win"):
                # Windows taskkill kills process tree
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(process.pid)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=2.0
                )
            else:
                process.kill()
        except Exception:
            try:
                process.kill()
            except Exception:
                pass
