"""
CODE COMBAT Pro - Native Desktop Application Entrypoint
Runs the embedded backend server and presents a standalone native desktop window.
"""

import os
import sys
import time
import json
import socket
import threading
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.server import run_server


def find_free_port(preferred_port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("127.0.0.1", preferred_port)) != 0:
            return preferred_port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start_backend_thread(host="127.0.0.1", port=8000):
    server_thread = threading.Thread(
        target=run_server,
        kwargs={"host": host, "port": port},
        daemon=True,
        name="CodeCombatBackend"
    )
    server_thread.start()
    return server_thread


def wait_for_server(host, port, timeout=5.0):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            time.sleep(0.1)
    return False


def launch_native_window(app_url):
    try:
        import webview
        print(f"[*] Launching PyWebView Native Desktop Window for {app_url}...")
        window = webview.create_window(
            title="CODE COMBAT Pro — Competitive Programming Arena",
            url=app_url,
            width=1366,
            height=860,
            min_size=(1024, 680),
            resizable=True,
            confirm_close=True,
            background_color="#0a0e17"
        )
        webview.start(debug=False)
        return True
    except Exception as e:
        print(f"[!] PyWebView notice: {e}")
        print("[*] Launching native Edge / Chrome App Mode...")
        return launch_edge_app_mode(app_url)


def launch_edge_app_mode(app_url):
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    for exe in edge_paths:
        if os.path.exists(exe):
            cmd = [exe, f"--app={app_url}", "--window-size=1366,860"]
            proc = subprocess.Popen(cmd)
            proc.wait()
            return True

    import webbrowser
    webbrowser.open(app_url)
    print(f"[*] Application running at {app_url}. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    return True


def main():
    print("=" * 60)
    print("      ⚔️ CODE COMBAT PRO - NATIVE DESKTOP APPLICATION        ")
    print("=" * 60)

    config_path = os.path.join(BASE_DIR, "config.json")
    config = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            pass

    host = config.get("server_host", "127.0.0.1")
    preferred_port = int(config.get("server_port", 8000))
    port = find_free_port(preferred_port)

    if port != preferred_port:
        print(f"[*] Port {preferred_port} in use. Checking if server is responsive...")
        if wait_for_server(host, preferred_port, timeout=1.0):
            app_url = f"http://{host}:{preferred_port}"
            print(f"[✓] Existing CODE COMBAT server detected at {app_url}")
            launch_native_window(app_url)
            return
        else:
            print(f"[*] Starting server on free port {port}...")
            start_backend_thread(host, port)
    else:
        print(f"[*] Starting embedded Code Combat server on {host}:{port}...")
        start_backend_thread(host, port)

    app_url = f"http://{host}:{port}"
    if not wait_for_server(host, port, timeout=6.0):
        print(f"[!] Server waiting. Launching {app_url}...")

    print(f"[✓] CODE COMBAT Pro Server Ready at {app_url}")
    launch_native_window(app_url)
    print("[*] Desktop application closed. Exiting.")


if __name__ == "__main__":
    main()
