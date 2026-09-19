/**
 * CODE COMBAT - Admin Dashboard Logic
 * Controls problem management (CRUD), submissions logs, participant lists, data export, and competition reset.
 */

const Admin = {
  authenticated: false,

  init() {
    this.bindEvents();
  },

  bindEvents() {
    const loginForm = document.getElementById("admin-login-form");
    if (loginForm) {
      loginForm.addEventListener("submit", (e) => {
        e.preventDefault();
        this.login();
      });
    }

    const resetBtn = document.getElementById("admin-reset-btn");
    if (resetBtn) {
      resetBtn.addEventListener("click", () => this.resetCompetition());
    }

    const exportBtn = document.getElementById("admin-export-btn");
    if (exportBtn) {
      exportBtn.addEventListener("click", () => this.exportData());
    }
  },

  async login() {
    const passInput = document.getElementById("admin-password-input");
    const password = passInput ? passInput.value : "";
    if (!password) {
      App.showToast("Please enter the admin password.", "error");
      return;
    }

    try {
      const res = await App.apiPost("/api/admin/login", { password });
      if (res.authenticated) {
        this.authenticated = true;
        App.closeModal("admin-login-modal");
        App.showToast("Admin access granted.", "success");
        this.loadAdminData();
      } else {
        App.showToast("Incorrect admin password.", "error");
      }
    } catch (e) {
      App.showToast("Authentication failed: " + e.message, "error");
    }
  },

  async loadAdminData() {
    if (!this.authenticated) {
      App.openModal("admin-login-modal");
      return;
    }

    this.loadSubmissions();
    this.loadParticipants();
    this.loadProblemsList();
  },

  async loadSubmissions() {
    const tableBody = document.getElementById("admin-submissions-body");
    if (!tableBody) return;

    try {
      const res = await App.apiGet("/api/submissions?limit=200");
      const subs = res.submissions || [];

      if (subs.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="8" style="text-align:center; color: var(--text-dim); padding: 24px;">No submissions logged yet.</td></tr>`;
        return;
      }

      tableBody.innerHTML = subs.map(sub => {
        const statusClass = sub.status === "ACCEPTED" ? "badge-easy" : "badge-hard";
        const timeStr = new Date(sub.timestamp).toLocaleTimeString();
        return `
          <tr>
            <td><code>${sub.id}</code></td>
            <td><strong>${App.escapeHtml(sub.participant_name)}</strong></td>
            <td>${App.escapeHtml(sub.problem_title)}</td>
            <td><span class="badge badge-${sub.difficulty.toLowerCase()}">${sub.difficulty}</span></td>
            <td><span class="badge ${statusClass}">${sub.status}</span></td>
            <td>${sub.passed_count}/${sub.total_count}</td>
            <td>${sub.score} pts</td>
            <td>${timeStr}</td>
          </tr>
        `;
      }).join("");
    } catch (e) {
      console.error("Failed to load admin submissions", e);
    }
  },

  async loadParticipants() {
    const tableBody = document.getElementById("admin-participants-body");
    if (!tableBody) return;

    try {
      const res = await App.apiGet("/api/admin/participants");
      const parts = res.participants || [];

      if (parts.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="6" style="text-align:center; color: var(--text-dim); padding: 24px;">No participants registered.</td></tr>`;
        return;
      }

      tableBody.innerHTML = parts.map(p => `
        <tr>
          <td><code>${p.id}</code></td>
          <td><strong>${App.escapeHtml(p.name)}</strong></td>
          <td>${App.escapeHtml(p.college || "-")}</td>
          <td><code>${App.escapeHtml(p.reg_no || "-")}</code></td>
          <td>${p.solved_problems?.length || 0}</td>
          <td><strong>${p.score || 0} pts</strong></td>
        </tr>
      `).join("");
    } catch (e) {
      console.error("Failed to load participants", e);
    }
  },

  async loadProblemsList() {
    const container = document.getElementById("admin-problems-list");
    if (!container) return;

    try {
      const res = await App.apiGet("/api/problems");
      const problems = res.problems || [];

      container.innerHTML = problems.map(p => `
        <div style="background: var(--bg-input); border: 1px solid var(--border-color); padding: 14px 18px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
          <div>
            <div style="font-weight: 700; color: #fff; font-size: 15px;">${App.escapeHtml(p.title)} <span class="badge badge-${p.difficulty.toLowerCase()}">${p.difficulty}</span></div>
            <div style="font-size: 12px; color: var(--text-dim); margin-top: 4px;">ID: <code>${p.id}</code> | Category: ${p.category} | Points: ${p.points}</div>
          </div>
          <button class="btn btn-danger" style="padding: 6px 12px; font-size: 12px;" onclick="Admin.deleteProblem('${p.id}')">Delete</button>
        </div>
      `).join("");
    } catch (e) {
      console.error("Failed to load admin problems", e);
    }
  },

  async deleteProblem(problemId) {
    if (!confirm(`Are you sure you want to permanently delete problem '${problemId}'?`)) {
      return;
    }

    try {
      const res = await fetch(`/api/admin/problem/${problemId}`, { method: "DELETE" });
      const data = await res.json();
      if (data.success) {
        App.showToast(data.message, "success");
        this.loadProblemsList();
        App.loadProblems();
      } else {
        App.showToast(data.error || "Failed to delete problem", "error");
      }
    } catch (e) {
      App.showToast("Error deleting problem: " + e.message, "error");
    }
  },

  async resetCompetition() {
    const pass = prompt("WARNING: This will erase all registered participants, submissions, and leaderboard rankings.\nType the Admin Password to confirm:");
    if (!pass) return;

    try {
      const res = await App.apiPost("/api/admin/reset", { password: pass });
      if (res.success) {
        App.showToast("Competition data has been completely reset.", "success");
        this.loadAdminData();
        App.loadLeaderboard();
        App.loadProblems();
      } else {
        App.showToast(res.error || "Reset failed", "error");
      }
    } catch (e) {
      App.showToast("Reset error: " + e.message, "error");
    }
  },

  async exportData() {
    try {
      const data = await App.apiGet("/api/admin/export");
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `code_combat_export_${new Date().toISOString().slice(0, 10)}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      App.showToast("Competition data exported successfully.", "success");
    } catch (e) {
      App.showToast("Failed to export data: " + e.message, "error");
    }
  }
};
