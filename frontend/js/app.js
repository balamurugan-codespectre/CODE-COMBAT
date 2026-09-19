/**
 * CODE COMBAT - Main Frontend Controller & SPA Router
 * Controls views, registration, problem studio, real-time judge integration, leaderboard, and countdown timer.
 */

const App = {
  config: {},
  participant: null,
  problems: [],
  currentProblem: null,
  currentDifficultyFilter: "ALL",
  searchQuery: "",
  editor: null,
  timerInterval: null,
  timeRemainingSeconds: 0,
  timerExpired: false,

  async init() {
    console.log("[CodeCombat] Initializing frontend application...");

    // 1. Fetch Configuration
    await this.loadConfig();

    // 2. Restore Participant Session
    this.restoreSession();

    // 3. Initialize Code Editor
    this.editor = new CodeEditor("code-editor-textarea", "editor-line-numbers", "editor-language-select");

    // 4. Initialize Admin Subsystem
    Admin.init();

    // 5. Bind Navigation and UI Events
    this.bindEvents();

    // 6. Initialize Timer
    this.initCompetitionTimer();

    // 7. Initial View Routing
    const hash = window.location.hash.replace("#", "") || "home";
    this.showView(hash);

    // 8. Load Initial Data
    this.loadProblems();
    this.loadLeaderboard();
  },

  // ------------------- API Helpers -------------------

  async apiGet(endpoint) {
    const res = await fetch(endpoint);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || `HTTP ${res.status}`);
    }
    return res.json();
  },

  async apiPost(endpoint, body) {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || `HTTP ${res.status}`);
    }
    return res.json();
  },

  // ------------------- Configuration & Session -------------------

  async loadConfig() {
    try {
      this.config = await this.apiGet("/api/config");
    } catch (e) {
      console.warn("Could not load backend config, using defaults", e);
      this.config = {
        competition_name: "CODE COMBAT",
        competition_duration_minutes: 90
      };
    }
  },

  restoreSession() {
    try {
      const saved = localStorage.getItem("codecombat_participant");
      if (saved) {
        this.participant = JSON.parse(saved);
        this.updateParticipantUI();
      }
    } catch (e) {}
  },

  updateParticipantUI() {
    const pill = document.getElementById("header-participant-pill");
    const nameSpan = document.getElementById("header-participant-name");
    const avatar = document.getElementById("header-participant-avatar");

    if (this.participant && this.participant.name) {
      pill.style.display = "flex";
      nameSpan.innerText = this.participant.name;
      avatar.innerText = this.participant.name.charAt(0).toUpperCase();
    } else {
      pill.style.display = "flex";
      nameSpan.innerText = "Guest (Register)";
      avatar.innerText = "?";
    }
  },

  // ------------------- Competition Timer -------------------

  initCompetitionTimer() {
    const durationMinutes = this.config.competition_duration_minutes || 90;
    const storageKey = "codecombat_end_timestamp";

    let endTime = localStorage.getItem(storageKey);
    if (!endTime) {
      endTime = Date.now() + durationMinutes * 60 * 1000;
      localStorage.setItem(storageKey, endTime);
    } else {
      endTime = parseInt(endTime, 10);
    }

    const timerDisplay = document.getElementById("competition-timer-display");

    const updateTimer = () => {
      const now = Date.now();
      const diff = Math.max(0, Math.floor((endTime - now) / 1000));
      this.timeRemainingSeconds = diff;

      const hrs = String(Math.floor(diff / 3600)).padStart(2, "0");
      const mins = String(Math.floor((diff % 3600) / 60)).padStart(2, "0");
      const secs = String(diff % 60).padStart(2, "0");

      if (timerDisplay) {
        timerDisplay.innerText = `${hrs}:${mins}:${secs}`;
      }

      // Visual warning classes
      const container = document.getElementById("competition-timer-container");
      if (container) {
        if (diff <= 180) { // < 3 mins
          container.className = "competition-timer timer-danger";
        } else if (diff <= 600) { // < 10 mins
          container.className = "competition-timer timer-warning";
        } else {
          container.className = "competition-timer";
        }
      }

      if (diff === 0 && !this.timerExpired) {
        this.timerExpired = true;
        this.showToast("Competition time has expired! Submissions are now closed.", "error");
        const submitBtn = document.getElementById("btn-submit-code");
        if (submitBtn) submitBtn.disabled = true;
      }
    };

    updateTimer();
    this.timerInterval = setInterval(updateTimer, 1000);
  },

  // ------------------- Navigation & View Routing -------------------

  showView(viewName) {
    this.currentView = viewName;
    window.location.hash = viewName;

    document.querySelectorAll(".view-section").forEach(sec => sec.classList.remove("active"));
    document.querySelectorAll(".nav-btn").forEach(btn => btn.classList.remove("active"));

    const targetSection = document.getElementById(`view-${viewName}`);
    if (targetSection) {
      targetSection.classList.add("active");
    }

    const targetNav = document.getElementById(`nav-${viewName}`);
    if (targetNav) {
      targetNav.classList.add("active");
    }

    if (viewName === "problems") {
      this.loadProblems();
    } else if (viewName === "leaderboard") {
      this.loadLeaderboard();
    } else if (viewName === "admin") {
      Admin.loadAdminData();
    }
  },

  bindEvents() {
    // Nav Buttons
    document.querySelectorAll("[data-nav]").forEach(el => {
      el.addEventListener("click", (e) => {
        const target = e.currentTarget.getAttribute("data-nav");
        this.showView(target);
      });
    });

    // Start Coding Button (Directs to Registration or Problems)
    const startCodingBtn = document.getElementById("btn-start-coding");
    if (startCodingBtn) {
      startCodingBtn.addEventListener("click", () => {
        if (!this.participant) {
          this.openModal("register-modal");
        } else {
          this.showView("problems");
        }
      });
    }

    // Participant Header Pill
    const participantPill = document.getElementById("header-participant-pill");
    if (participantPill) {
      participantPill.addEventListener("click", () => {
        this.openModal("register-modal");
      });
    }

    // Registration Form
    const regForm = document.getElementById("registration-form");
    if (regForm) {
      regForm.addEventListener("submit", (e) => {
        e.preventDefault();
        this.handleRegistration();
      });
    }

    // Difficulty Filter Buttons
    document.querySelectorAll(".filter-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
        e.currentTarget.classList.add("active");
        this.currentDifficultyFilter = e.currentTarget.getAttribute("data-diff");
        this.renderProblemsTable();
      });
    });

    // Problem Search Box
    const searchBox = document.getElementById("problem-search-input");
    if (searchBox) {
      searchBox.addEventListener("input", (e) => {
        this.searchQuery = e.target.value.toLowerCase().trim();
        this.renderProblemsTable();
      });
    }

    // Studio Action Buttons
    const runBtn = document.getElementById("btn-run-code");
    if (runBtn) runBtn.addEventListener("click", () => this.runCode());

    const submitBtn = document.getElementById("btn-submit-code");
    if (submitBtn) submitBtn.addEventListener("click", () => this.submitCode());

    const resetBtn = document.getElementById("btn-reset-code");
    if (resetBtn) {
      resetBtn.addEventListener("click", () => {
        if (confirm("Reset code editor to starter template? Your current changes will be discarded.")) {
          this.editor.resetCurrentCode();
          this.showToast("Code editor reset to starter template.", "info");
        }
      });
    }

    // Studio Test Tabs
    document.querySelectorAll(".test-tab-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        document.querySelectorAll(".test-tab-btn").forEach(b => b.classList.remove("active"));
        document.querySelectorAll(".test-tab-pane").forEach(p => p.style.display = "none");

        e.currentTarget.classList.add("active");
        const tabTarget = e.currentTarget.getAttribute("data-tab");
        const pane = document.getElementById(`tab-pane-${tabTarget}`);
        if (pane) pane.style.display = "block";
      });
    });

    // Custom Input Run Button
    const customRunBtn = document.getElementById("btn-run-custom-input");
    if (customRunBtn) {
      customRunBtn.addEventListener("click", () => this.runCustomInput());
    }

    // Modal Closers
    document.querySelectorAll(".modal-close-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        const modal = e.currentTarget.closest(".modal-overlay");
        if (modal) modal.classList.remove("active");
      });
    });
  },

  // ------------------- Participant Registration -------------------

  async handleRegistration() {
    const name = document.getElementById("reg-name-input").value.trim();
    const college = document.getElementById("reg-college-input").value.trim();
    const regNo = document.getElementById("reg-no-input").value.trim();

    if (!name) {
      this.showToast("Please enter your name.", "error");
      return;
    }

    try {
      const res = await this.apiPost("/api/register", {
        name,
        college,
        reg_no: regNo
      });

      if (res.success && res.participant) {
        this.participant = res.participant;
        localStorage.setItem("codecombat_participant", JSON.stringify(this.participant));
        this.updateParticipantUI();
        this.closeModal("register-modal");
        this.showToast(`Welcome, ${name}! Start coding!`, "success");
        this.showView("problems");
      }
    } catch (e) {
      this.showToast("Registration failed: " + e.message, "error");
    }
  },

  // ------------------- Problems Dashboard -------------------

  async loadProblems() {
    try {
      const pid = this.participant ? this.participant.id : "";
      const res = await this.apiGet(`/api/problems?participant_id=${pid}`);
      this.problems = res.problems || [];
      this.renderProblemsTable();
    } catch (e) {
      console.error("Failed to load problems", e);
    }
  },

  renderProblemsTable() {
    const tableBody = document.getElementById("problems-table-body");
    if (!tableBody) return;

    let filtered = this.problems.filter(p => {
      // Difficulty filter
      if (this.currentDifficultyFilter !== "ALL" && p.difficulty.toUpperCase() !== this.currentDifficultyFilter) {
        return false;
      }
      // Search filter
      if (this.searchQuery && !p.title.toLowerCase().includes(this.searchQuery) && !p.category.toLowerCase().includes(this.searchQuery)) {
        return false;
      }
      return true;
    });

    if (filtered.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 32px; color: var(--text-dim);">No problems found matching criteria.</td></tr>`;
      return;
    }

    tableBody.innerHTML = filtered.map((p, idx) => {
      const diffBadge = `badge-${p.difficulty.toLowerCase()}`;
      const statusBadge = p.status === "Solved" ? "badge-solved" : "badge-unsolved";
      return `
        <tr class="problem-row" onclick="App.openProblem('${p.id}')">
          <td style="color: var(--text-dim); font-family: var(--font-mono); font-size: 12px;">#${idx + 1}</td>
          <td class="problem-title-cell">
            <strong>${this.escapeHtml(p.title)}</strong>
          </td>
          <td style="color: var(--text-muted); font-size: 12px;">${p.category}</td>
          <td><span class="badge ${diffBadge}">${p.difficulty}</span></td>
          <td style="font-family: var(--font-mono); font-weight: 600; color: #fff;">${p.points} pts</td>
          <td><span class="badge ${statusBadge}">${p.status}</span></td>
        </tr>
      `;
    }).join("");
  },

  // ------------------- Coding Studio -------------------

  async openProblem(problemId) {
    try {
      const problem = await this.apiGet(`/api/problems/${problemId}`);
      if (!problem) return;

      this.currentProblem = problem;
      this.renderProblemStudio(problem);
      this.showView("studio");
    } catch (e) {
      this.showToast("Failed to open problem: " + e.message, "error");
    }
  },

  renderProblemStudio(problem) {
    // Problem Details Left Panel
    document.getElementById("studio-problem-title").innerText = problem.title;
    const diffBadge = document.getElementById("studio-difficulty-badge");
    diffBadge.className = `badge badge-${problem.difficulty.toLowerCase()}`;
    diffBadge.innerText = problem.difficulty;

    document.getElementById("studio-points-badge").innerText = `${problem.points} Points`;
    document.getElementById("studio-category-badge").innerText = problem.category || "General";
    document.getElementById("studio-time-limit").innerText = `Time Limit: ${problem.time_limit}s`;

    document.getElementById("studio-description").innerText = problem.description;
    document.getElementById("studio-input-format").innerText = problem.input_format;
    document.getElementById("studio-output-format").innerText = problem.output_format;
    document.getElementById("studio-constraints").innerText = problem.constraints;

    // Render Sample Tests inside Left Panel
    const samplesContainer = document.getElementById("studio-sample-examples");
    if (samplesContainer && problem.sample_tests) {
      samplesContainer.innerHTML = problem.sample_tests.map((st, idx) => `
        <div class="sample-test-card">
          <div class="sample-test-header">
            <span>Example ${idx + 1}</span>
          </div>
          <div class="sample-io-grid">
            <div class="sample-io-block">
              <h5>Input</h5>
              <pre>${this.escapeHtml(st.input)}</pre>
            </div>
            <div class="sample-io-block">
              <h5>Output</h5>
              <pre>${this.escapeHtml(st.output)}</pre>
            </div>
          </div>
          ${st.explanation ? `<div style="font-size: 12px; color: var(--text-dim); margin-top: 6px;"><em>Explanation:</em> ${this.escapeHtml(st.explanation)}</div>` : ""}
        </div>
      `).join("");
    }

    // Load into Code Editor
    this.editor.loadProblem(problem);

    // Switch right panel to sample tab
    this.switchTestTab("sample");
    document.getElementById("sample-results-container").innerHTML = `<div style="color: var(--text-dim); text-align: center; padding: 24px;">Click <strong>Run Code</strong> to test your solution against visible test cases.</div>`;
  },

  switchTestTab(tabName) {
    document.querySelectorAll(".test-tab-btn").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".test-tab-pane").forEach(p => p.style.display = "none");

    const tabBtn = document.querySelector(`[data-tab="${tabName}"]`);
    if (tabBtn) tabBtn.classList.add("active");

    const pane = document.getElementById(`tab-pane-${tabName}`);
    if (pane) pane.style.display = "block";
  },

  // ------------------- Code Execution & Testing -------------------

  async runCode() {
    if (!this.currentProblem) return;

    const code = this.editor.getCode();
    const lang = this.editor.getLanguage();
    const runBtn = document.getElementById("btn-run-code");
    const container = document.getElementById("sample-results-container");

    this.switchTestTab("sample");
    runBtn.disabled = true;
    runBtn.innerHTML = `<span>Running...</span>`;
    container.innerHTML = `<div style="text-align: center; padding: 32px; color: var(--accent-cyan); font-weight: 600;">Executing sample test cases...</div>`;

    try {
      const res = await this.apiPost("/api/run", {
        problem_id: this.currentProblem.id,
        language: lang,
        code: code,
        is_custom: false
      });

      const result = res.result;

      if (result.status === "COMPILATION_ERROR") {
        container.innerHTML = `
          <div class="result-banner result-banner-failed">
            <div class="result-banner-title">COMPILATION ERROR</div>
            <pre style="text-align: left; background: #06090e; padding: 12px; border-radius: 6px; font-size: 12px; overflow-x: auto; color: #fb7185; margin-top: 10px;">${this.escapeHtml(result.compilation_error)}</pre>
          </div>
        `;
        return;
      }

      const allPassed = result.all_passed;
      let html = `
        <div class="result-banner ${allPassed ? 'result-banner-accepted' : 'result-banner-failed'}">
          <div class="result-banner-title">${allPassed ? 'SAMPLE TESTS PASSED ✓' : 'SOME TESTS FAILED ✗'}</div>
          <div style="font-size: 13px;">${allPassed ? 'All sample test cases matched expected output.' : 'Check actual output against expected output below.'}</div>
        </div>
      `;

      html += (result.results || []).map(r => `
        <div class="case-result-card ${r.passed ? 'passed' : 'failed'}">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <strong>Test Case #${r.test_case}</strong>
            <span class="badge ${r.passed ? 'badge-easy' : 'badge-hard'}">${r.status} (${r.runtime}s)</span>
          </div>
          <div style="font-size: 11px; color: var(--text-dim); margin-bottom: 2px;">Input:</div>
          <pre style="background: #06090e; padding: 6px; border-radius: 4px; font-size: 11px; margin-bottom: 6px;">${this.escapeHtml(r.input)}</pre>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
            <div>
              <div style="font-size: 11px; color: var(--text-dim); margin-bottom: 2px;">Expected Output:</div>
              <pre style="background: #06090e; padding: 6px; border-radius: 4px; font-size: 11px; color: #34d399;">${this.escapeHtml(r.expected)}</pre>
            </div>
            <div>
              <div style="font-size: 11px; color: var(--text-dim); margin-bottom: 2px;">Actual Output:</div>
              <pre style="background: #06090e; padding: 6px; border-radius: 4px; font-size: 11px; color: ${r.passed ? '#34d399' : '#fb7185'};">${this.escapeHtml(r.actual || r.stderr || "(No output)")}</pre>
            </div>
          </div>
        </div>
      `).join("");

      container.innerHTML = html;
    } catch (e) {
      container.innerHTML = `<div class="result-banner result-banner-failed"><div class="result-banner-title">ERROR</div><div>${this.escapeHtml(e.message)}</div></div>`;
    } finally {
      runBtn.disabled = false;
      runBtn.innerHTML = `<span>Run Code</span>`;
    }
  },

  async runCustomInput() {
    const code = this.editor.getCode();
    const lang = this.editor.getLanguage();
    const customInput = document.getElementById("custom-input-textarea").value;
    const outputContainer = document.getElementById("custom-output-display");
    const runBtn = document.getElementById("btn-run-custom-input");

    runBtn.disabled = true;
    runBtn.innerText = "Executing...";
    outputContainer.innerText = "Executing in isolated sandbox...";

    try {
      const res = await this.apiPost("/api/run", {
        problem_id: this.currentProblem ? this.currentProblem.id : "scratch",
        language: lang,
        code: code,
        custom_input: customInput,
        is_custom: true
      });

      const r = res.result;
      let text = `[Status] : ${r.status}\n[Runtime]: ${r.runtime}s\n\n`;
      if (r.stdout) text += `--- STDOUT ---\n${r.stdout}\n`;
      if (r.stderr) text += `\n--- STDERR ---\n${r.stderr}\n`;
      if (!r.stdout && !r.stderr) text += `(Process completed with no output)`;

      outputContainer.innerText = text;
    } catch (e) {
      outputContainer.innerText = `Error: ${e.message}`;
    } finally {
      runBtn.disabled = false;
      runBtn.innerText = "Run Custom Input";
    }
  },

  async submitCode() {
    if (!this.participant) {
      this.openModal("register-modal");
      this.showToast("Please register first to submit solutions.", "info");
      return;
    }

    if (!this.currentProblem) return;

    const code = this.editor.getCode();
    const lang = this.editor.getLanguage();
    const submitBtn = document.getElementById("btn-submit-code");
    const resultsContainer = document.getElementById("submission-results-container");

    this.switchTestTab("results");
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<span>Judging...</span>`;
    resultsContainer.innerHTML = `
      <div style="text-align: center; padding: 40px;">
        <div style="font-size: 16px; font-weight: 700; color: var(--accent-cyan); margin-bottom: 8px;">Judging against Hidden Test Cases...</div>
        <div style="font-size: 13px; color: var(--text-dim);">Compiling and running against secret server test suites</div>
      </div>
    `;

    try {
      const res = await this.apiPost("/api/submit", {
        participant_id: this.participant.id,
        participant_name: this.participant.name,
        problem_id: this.currentProblem.id,
        language: lang,
        code: code
      });

      const isAccepted = (res.status === "ACCEPTED");
      const bannerClass = isAccepted ? "result-banner-accepted" : (res.status === "TIME_LIMIT_EXCEEDED" ? "result-banner-tle" : "result-banner-failed");

      resultsContainer.innerHTML = `
        <div class="result-banner ${bannerClass}">
          <div class="result-banner-title">${res.status} ${isAccepted ? '✓' : '✗'}</div>
          <div>${isAccepted ? 'All hidden test cases passed! Points awarded.' : (res.error_message || 'Hidden test case evaluation failed.')}</div>
        </div>

        <div class="result-stats-row">
          <div class="result-stat-box">
            <div class="result-stat-label">Test Cases</div>
            <div class="result-stat-val" style="color: ${isAccepted ? '#34d399' : '#fb7185'};">${res.passed_count} / ${res.total_count}</div>
          </div>
          <div class="result-stat-box">
            <div class="result-stat-label">Score Earned</div>
            <div class="result-stat-val" style="color: var(--accent-cyan);">+${res.score_earned} pts</div>
          </div>
          <div class="result-stat-box">
            <div class="result-stat-label">Peak Runtime</div>
            <div class="result-stat-val">${res.runtime}s</div>
          </div>
          <div class="result-stat-box">
            <div class="result-stat-label">Submission ID</div>
            <div class="result-stat-val" style="font-size: 13px;">${res.submission_id}</div>
          </div>
        </div>

        <div style="display: flex; gap: 10px; margin-top: 20px;">
          <button class="btn btn-primary" style="flex: 1;" onclick="App.showView('leaderboard')">View Leaderboard</button>
          <button class="btn btn-secondary" style="flex: 1;" onclick="App.showView('problems')">Back to Problems</button>
        </div>
      `;

      if (isAccepted) {
        this.showToast(`Accepted! +${res.score_earned} points awarded!`, "success");
      } else {
        this.showToast(`Submission Verdict: ${res.status}`, "error");
      }

      // Refresh problems & leaderboard in background
      this.loadProblems();
      this.loadLeaderboard();

    } catch (e) {
      resultsContainer.innerHTML = `<div class="result-banner result-banner-failed"><div class="result-banner-title">ERROR</div><div>${this.escapeHtml(e.message)}</div></div>`;
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = `<span>Submit Code</span>`;
    }
  },

  // ------------------- Leaderboard -------------------

  async loadLeaderboard() {
    const tableBody = document.getElementById("leaderboard-table-body");
    if (!tableBody) return;

    try {
      const res = await this.apiGet("/api/leaderboard");
      const board = res.leaderboard || [];

      if (board.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-dim); padding: 32px;">No participants on leaderboard yet. Be the first to conquer a challenge!</td></tr>`;
        return;
      }

      tableBody.innerHTML = board.map(item => {
        let rankClass = "rank-other";
        if (item.rank === 1) rankClass = "rank-1";
        else if (item.rank === 2) rankClass = "rank-2";
        else if (item.rank === 3) rankClass = "rank-3";

        const isMe = this.participant && this.participant.id === item.participant_id;

        return `
          <tr style="${isMe ? 'background: rgba(0, 242, 254, 0.05); font-weight: 600;' : ''}">
            <td><div class="rank-badge ${rankClass}">${item.rank}</div></td>
            <td><strong>${this.escapeHtml(item.name)}</strong> ${isMe ? '<span class="badge badge-solved" style="margin-left: 6px;">You</span>' : ''}</td>
            <td style="color: var(--text-muted);">${this.escapeHtml(item.college || "-")}</td>
            <td style="font-family: var(--font-mono);">${item.solved_count}</td>
            <td><span class="badge badge-easy">${item.easy_solved}</span></td>
            <td><span class="badge badge-medium">${item.medium_solved}</span></td>
            <td><span class="badge badge-hard">${item.hard_solved}</span></td>
            <td style="font-family: var(--font-mono); font-size: 15px; font-weight: 700; color: var(--accent-cyan);">${item.score}</td>
          </tr>
        `;
      }).join("");
    } catch (e) {
      console.error("Failed to load leaderboard", e);
    }
  },

  // ------------------- Modal & Toast System -------------------

  openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.add("active");
  },

  closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove("active");
  },

  showToast(message, type = "info") {
    let container = document.getElementById("toast-container");
    if (!container) {
      container = document.createElement("div");
      container.id = "toast-container";
      container.className = "toast-container";
      document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.innerText = message;

    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transition = "opacity 0.3s ease";
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  },

  escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
};

// Start application on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  App.init();
});
