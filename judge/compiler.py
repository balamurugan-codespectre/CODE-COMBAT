"""
CODE COMBAT - Code Compiler Module
Handles syntax validation and compilation for Python, Java, and C.
"""

import os
import sys
import shutil
import subprocess
import ast
import re
from typing import Dict, Any, Optional, Tuple


class Compiler:
    """Manages compilation and pre-execution checks for supported languages."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.timeout = self.config.get("compile_timeout_seconds", 10.0)

    @staticmethod
    def detect_c_compiler() -> Optional[str]:
        """Detects and validates an available working C compiler on the host system."""
        import tempfile
        for compiler in ["clang", "gcc", "cl", "clang.exe", "gcc.exe"]:
            resolved = shutil.which(compiler)
            if resolved:
                td = tempfile.mkdtemp(prefix="test_c_")
                try:
                    src = os.path.join(td, "test.c")
                    with open(src, "w", encoding="utf-8") as f:
                        f.write("int main(){return 0;}\n")
                    res = subprocess.run(
                        [resolved, "test.c", "-o", "test.exe"],
                        cwd=td,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        timeout=3.0
                    )
                    if res.returncode == 0 and os.path.exists(os.path.join(td, "test.exe")):
                        return resolved
                except Exception:
                    pass
                finally:
                    shutil.rmtree(td, ignore_errors=True)
        return None

    @staticmethod
    def detect_java_compiler() -> Optional[str]:
        """Detects available Java compiler on the host system."""
        if shutil.which("javac"):
            return "javac"
        return None

    def compile(self, language: str, source_code: str, work_dir: str) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Prepares and compiles source code inside work_dir.

        Returns:
            (success: bool, error_message: Optional[str], metadata: Optional[Dict[str, Any]])
        """
        lang = language.lower().strip()

        if lang == "python" or lang == "python3" or lang == "py":
            return self._prepare_python(source_code, work_dir)
        elif lang == "java":
            return self._compile_java(source_code, work_dir)
        elif lang == "c":
            return self._compile_c(source_code, work_dir)
        else:
            return False, f"Unsupported language: '{language}'. Supported: Python, Java, C.", None

    def _prepare_python(self, source_code: str, work_dir: str) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """Validates Python syntax and writes solution.py."""
        # 1. Syntax check via AST
        try:
            ast.parse(source_code, filename="solution.py")
        except SyntaxError as se:
            err = f"SyntaxError on line {se.lineno}: {se.msg}\n  {se.text or ''}"
            return False, err, None
        except Exception as e:
            return False, f"Syntax Error: {str(e)}", None

        # 2. Write file
        file_path = os.path.join(work_dir, "solution.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(source_code)

        metadata = {
            "entry_file": file_path,
            "cmd": [sys.executable, file_path],
            "language": "python"
        }
        return True, None, metadata

    def _compile_java(self, source_code: str, work_dir: str) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """Compiles Java source code using javac."""
        javac = self.detect_java_compiler()
        if not javac:
            return False, "Java compiler (javac) is not found on this system PATH.", None

        # Extract public class name if specified, default to Solution
        class_match = re.search(r'public\s+class\s+([A-Za-z0-9_]+)', source_code)
        if class_match:
            class_name = class_match.group(1)
        else:
            # Check for non-public Solution class
            if re.search(r'class\s+Solution', source_code):
                class_name = "Solution"
            else:
                # Find the first class definition
                first_class = re.search(r'class\s+([A-Za-z0-9_]+)', source_code)
                class_name = first_class.group(1) if first_class else "Solution"

        file_path = os.path.join(work_dir, f"{class_name}.java")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(source_code)

        try:
            res = subprocess.run(
                [javac, f"{class_name}.java"],
                cwd=work_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=self.timeout
            )
            if res.returncode != 0:
                err_msg = res.stderr or res.stdout or "Compilation failed."
                return False, err_msg.strip(), None
        except subprocess.TimeoutExpired:
            return False, f"Java compilation timed out after {self.timeout} seconds.", None
        except Exception as e:
            return False, f"Java compilation error: {str(e)}", None

        # Find java runtime
        java_cmd = shutil.which("java") or "java"
        metadata = {
            "entry_file": file_path,
            "cmd": [java_cmd, "-cp", work_dir, class_name],
            "language": "java",
            "class_name": class_name
        }
        return True, None, metadata

    def _compile_c(self, source_code: str, work_dir: str) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """Compiles C source code using gcc or clang."""
        c_compiler = self.detect_c_compiler()
        if not c_compiler:
            return (
                False,
                "C compiler (gcc/clang) was not found on this system PATH.\n"
                "Please install MinGW-w64 / GCC or run solutions in Python or Java.",
                None
            )

        src_path = os.path.join(work_dir, "solution.c")
        exe_name = "solution.exe" if sys.platform.startswith("win") else "solution"
        exe_path = os.path.join(work_dir, exe_name)

        with open(src_path, "w", encoding="utf-8") as f:
            f.write(source_code)

        compile_cmd = [c_compiler, "-O2", "solution.c", "-o", exe_name, "-lm"]
        try:
            res = subprocess.run(
                compile_cmd,
                cwd=work_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=self.timeout
            )
            if res.returncode != 0:
                err_msg = res.stderr or res.stdout or "C compilation failed."
                return False, err_msg.strip(), None
        except subprocess.TimeoutExpired:
            return False, f"C compilation timed out after {self.timeout} seconds.", None
        except Exception as e:
            return False, f"C compilation error: {str(e)}", None

        metadata = {
            "entry_file": src_path,
            "cmd": [exe_path],
            "language": "c"
        }
        return True, None, metadata
