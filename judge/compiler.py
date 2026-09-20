"""
CODE COMBAT Pro - Polyglot Code Compiler Module
Handles syntax parsing, class extraction, and compilation for Python 3, Java, and C.
"""

import os
import sys
import shutil
import subprocess
import ast
import re
import tempfile
from typing import Dict, Any, Optional, Tuple, List


from .harness import Harness


class Compiler:
    """Manages compilation and pre-execution checks for supported languages."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.timeout = float(self.config.get("compile_timeout_seconds", 10.0))

    @staticmethod
    def _find_mingw_root() -> Optional[str]:
        """Finds MinGW header/library directory for Windows Clang sysroot."""
        candidates = [
            r"C:\Users\rajku\AppData\Local\Microsoft\WinGet\Packages\BrechtSanders.WinLibs.POSIX.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\mingw64",
            r"C:\mingw64",
            r"C:\msys64\mingw64",
            r"C:\msys64\ucrt64"
        ]
        user_profile = os.environ.get("USERPROFILE", "")
        if user_profile:
            winget_path = os.path.join(user_profile, "AppData", "Local", "Microsoft", "WinGet", "Packages")
            if os.path.isdir(winget_path):
                for folder in os.listdir(winget_path):
                    if "WinLibs" in folder:
                        cand = os.path.join(winget_path, folder, "mingw64")
                        if os.path.isdir(cand):
                            candidates.insert(0, cand)

        for c in candidates:
            if os.path.isdir(c) and os.path.isdir(os.path.join(c, "include")):
                return c
        return None

    @classmethod
    def get_c_compiler_config(cls) -> Optional[Dict[str, Any]]:
        """Detects, configures, and validates a working C compiler."""
        # 1. Look for clang executable
        clang_candidates = [
            r"C:\Program Files\LLVM\bin\clang.exe",
            shutil.which("clang.exe"),
            shutil.which("clang"),
            shutil.which("gcc.exe"),
            shutil.which("gcc")
        ]

        mingw_root = cls._find_mingw_root()

        for c in [x for x in clang_candidates if x and os.path.exists(x)]:
            # Build smoke-test command
            test_cmd = [c]
            if "clang" in c.lower() and sys.platform.startswith("win") and mingw_root:
                test_cmd.extend(["--target=x86_64-w64-windows-gnu", f"--sysroot={mingw_root}", "-O2", "-static"])
            else:
                test_cmd.extend(["-O2", "-static"])

            # Smoke test
            td = tempfile.mkdtemp(prefix="smoke_c_")
            try:
                src = os.path.join(td, "test.c")
                exe = os.path.join(td, "test.exe") if sys.platform.startswith("win") else os.path.join(td, "test")
                with open(src, "w", encoding="utf-8") as f:
                    f.write("#include <stdio.h>\nint main(){return 0;}\n")

                full_cmd = test_cmd + [src, "-o", exe]
                res = subprocess.run(full_cmd, cwd=td, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=4.0)
                if res.returncode == 0 and os.path.exists(exe):
                    return {
                        "executable": c,
                        "extra_flags": test_cmd[1:],
                        "display_name": os.path.basename(c)
                    }
            except Exception:
                pass
            finally:
                shutil.rmtree(td, ignore_errors=True)

        return None

    @classmethod
    def detect_c_compiler(cls) -> Optional[str]:
        """Detects and returns compiler path string for compatibility."""
        cfg = cls.get_c_compiler_config()
        return cfg["executable"] if cfg else None

    @staticmethod
    def detect_java_compiler() -> Optional[str]:
        """Detects available Java compiler on the host system."""
        resolved = shutil.which("javac")
        return resolved if resolved else None

    def compile(self, language: str, source_code: str, work_dir: str, problem_id: Optional[str] = None) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Prepares and compiles source code inside work_dir.
        If problem_id is supplied and the code does not contain a standalone main(),
        it is automatically wrapped with the LeetCode driver harness.

        Returns:
            (success: bool, error_message: Optional[str], metadata: Optional[Dict[str, Any]])
        """
        if problem_id:
            try:
                source_code = Harness.wrap_code(language, problem_id, source_code)
            except Exception as e:
                return False, f"Harness preparation error: {str(e)}", None

        lang = language.lower().strip()

        if lang in ["python", "python3", "py", "python_class", "python_leetcode", "python_normal", "python_script"]:
            return self._prepare_python(source_code, work_dir)
        elif lang == "java":
            return self._compile_java(source_code, work_dir)
        elif lang in ["c", "c99", "c11"]:
            return self._compile_c(source_code, work_dir)
        else:
            return False, f"Unsupported language: '{language}'. Supported: Python (Normal & Class), Java, C.", None

    def _prepare_python(self, source_code: str, work_dir: str) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """Validates Python syntax via AST and writes solution.py."""
        try:
            ast.parse(source_code, filename="solution.py")
        except SyntaxError as se:
            err = f"SyntaxError on line {se.lineno}, col {se.offset or 1}: {se.msg}\n  {se.text or ''}"
            return False, err, None
        except Exception as e:
            return False, f"Syntax Error: {str(e)}", None

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
            return False, "Java compiler (javac) is not found on this system PATH. Please install OpenJDK / JDK.", None

        # Extract public class name if specified, default to Solution
        class_match = re.search(r'public\s+class\s+([A-Za-z0-9_]+)', source_code)
        if class_match:
            class_name = class_match.group(1)
        else:
            if re.search(r'class\s+Solution', source_code):
                class_name = "Solution"
            else:
                first_class = re.search(r'class\s+([A-Za-z0-9_]+)', source_code)
                class_name = first_class.group(1) if first_class else "Solution"

        file_path = os.path.join(work_dir, f"{class_name}.java")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(source_code)

        try:
            res = subprocess.run(
                [javac, "-encoding", "UTF-8", f"{class_name}.java"],
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

        java_cmd = shutil.which("java") or "java"
        metadata = {
            "entry_file": file_path,
            "cmd": [java_cmd, "-cp", work_dir, "-Xmx256m", class_name],
            "language": "java",
            "class_name": class_name
        }
        return True, None, metadata

    def _compile_c(self, source_code: str, work_dir: str) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """Compiles C source code using auto-configured Clang or GCC."""
        c_cfg = self.get_c_compiler_config()
        if not c_cfg:
            return (
                False,
                "C compiler (Clang/GCC) was not found or configured on this system.\n"
                "Please run solutions in Python 3 or Java (OpenJDK).",
                None
            )

        src_path = os.path.join(work_dir, "solution.c")
        exe_name = "solution.exe" if sys.platform.startswith("win") else "solution"
        exe_path = os.path.join(work_dir, exe_name)

        with open(src_path, "w", encoding="utf-8") as f:
            f.write(source_code)

        compile_cmd = [c_cfg["executable"]] + c_cfg["extra_flags"] + ["solution.c", "-o", exe_name, "-lm"]
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
