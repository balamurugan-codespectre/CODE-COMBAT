# ⚔️ CODE COMBAT PRO - SYSTEM REQUIREMENTS & DEPLOYMENT GUIDE

This guide explains how to copy **Code Combat Pro** to any other computer (Windows, Linux, or macOS), configure prerequisites, and run the platform for offline single-machine usage or full college lab LAN network competitions.

---

## 1. System Requirements

### A. Core Requirements (Mandatory for Server & Judging)
| Component | Minimum Version | Recommended | Notes |
| :--- | :--- | :--- | :--- |
| **Operating System** | Windows 10/11, Ubuntu 20.04+, macOS 12+ | Windows 11 / Linux | Works 100% offline without internet. |
| **Python** | Python 3.8+ | Python 3.10, 3.11, 3.12, 3.14 | **Mandatory**: Check "Add Python to PATH" during installation. |
| **RAM** | 2 GB | 4 GB+ | Lightweight built-in HTTP server. |
| **Disk Space** | 250 MB | 500 MB | Includes all 30 problems, starter templates, and tests. |
| **Web Browser** | Any modern browser | Google Chrome, Edge, Brave, Firefox | Client interface (Monaco editor + live telemetry). |

### B. Language Compilers (Optional / as needed for student submissions)
| Language | Compiler / Runtime | Windows Setup | Linux Setup |
| :--- | :--- | :--- | :--- |
| **Python 3** | Built-in | Included with Python installation | `sudo apt install python3` |
| **C Language** | GCC / MinGW / Clang | [MinGW-w64](https://www.mingw-w64.org/) or [WinLibs](https://winlibs.com/) (`gcc.exe` in PATH) | `sudo apt install build-essential` |
| **Java** | OpenJDK / Oracle JDK 11+ | [Adoptium Eclipse Temurin](https://adoptium.net/) (`javac` & `java` in PATH) | `sudo apt install default-jdk` |

> [!NOTE]
> **No External Python Pip Packages Required!**
> The core server, SQLite ACID database, real-time live sync polling hub, and offline test judges use **100% Python Standard Library** with zero third-party dependencies.

---

## 2. How to Copy Code Combat Pro to Another Computer

### Method A: Via USB Pendrive or External Drive (Recommended for Offline Labs)
1. On your current machine, navigate to the project directory:
   ```
   C:\Users\rajku\.gemini\antigravity\scratch\code_combat
   ```
2. Copy the entire `code_combat` folder to your USB drive.
3. Plug the USB drive into the target computer and paste the `code_combat` folder to any location (e.g. `C:\CodeCombat` or Desktop).

### Method B: Via ZIP Archive
1. Right-click the `code_combat` folder -> **Send to** -> **Compressed (zipped) folder**.
2. Transfer `code_combat.zip` via USB, local network share, or email.
3. On the new computer, right-click `code_combat.zip` -> **Extract All...** to `C:\CodeCombat`.

---

## 3. How to Run on the New Computer

### 🚀 Option 1: Standalone Single Machine (One-Click)
Use this if the participant or administrator is using the application locally on one computer.

- **Windows**: Double-click `Start_Server.bat`.
- **Manual / Terminal**:
  ```bash
  python main.py
  ```
- The platform will automatically launch your default browser at `http://127.0.0.1:8000`.

---

### 🌐 Option 2: College Lab / Auditorium LAN Network (Multi-Client)
Use this if you are hosting a live competition across all lab PCs, laptops, or auditorium projector screens over college Wi-Fi or Ethernet LAN.

1. Connect the Host Server computer to the lab Wi-Fi or LAN switch.
2. Double-click `Start_LAN_Server.bat` (or run `python main.py --lan`).
3. The server terminal will display your LAN IP address:
   ```
   ======================================================================
    >> CODE COMBAT running at: http://192.168.1.50:8000
   ======================================================================
   ```
4. On all student lab computers and laptops, open Google Chrome/Edge and type:
   ```
   http://<HOST_IP>:8000
   (Example: http://192.168.1.50:8000)
   ```
5. All participants can register, code in Python/C/Java, submit against hidden test suites, and see real-time live standings simultaneously!

---

### 🖥️ Option 3: Desktop Window Mode (Standalone App)
If you prefer a native desktop window application without browser address bars:
1. Install optional GUI dependency:
   ```bash
   pip install pywebview
   ```
2. Double-click `Launch_Desktop_App.bat` (or run `python main_desktop.py`).

---

## 4. Administrator Credentials & Controls

### Master Administrator Credentials:
- **Admin ID**: `admincse`
- **Admin Password**: `infinixa26#cse@8148`

### Admin Panel Capabilities:
- **Round-Wise Category Locks**: Lock or unlock Round 1 (Easy), Round 2 (Medium), Round 3 (Hard) with 1 click.
- **Problem Set Switcher**: Instant toggle between **Set 1** (15 problems) and **Set 2** (15 problems) — 30 problems total.
- **Live Event Announcements**: Dispatch live broadcasts to all student screens in real time.
- **Freeze Leaderboard**: Freeze standings before the final reveal for suspense.
- **Official Solution Unlock**: Unlocks reference implementations inside the code editor for debugging.
- **Anti-Cheat Proctoring Logs**: Live telemetry tracking tab switches and window blur events.
- **One-Click Competition Reset**: Clears past student scores and submissions before the actual event begins.

---

## 5. Pre-Event Verification Checklist

Before starting your college competition, run the automated test suite on the host computer:

```bash
python test_suite.py
```
Expected output:
```
======================================================================
 🎯 TEST SUITE SUMMARY: 62 / 62 PASSED (100.0%)
======================================================================
 [✓] ALL PRODUCTION CRITERIA SATISFIED — CODE COMBAT PRO READY!
```

---
*Developed for Official College Competitive Programming & Tech-Fest Championships.*
