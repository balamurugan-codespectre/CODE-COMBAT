/**
 * CODE COMBAT Pro - Main Single Page Application Controller
 */

const App = {
  currentView: 'home',
  participant: null,
  problems: [],
  activeProblem: null,
  currentLanguage: 'python',
  editor: null,

  init() {
    // 1. Initialize custom editor
    this.editor = new CodeEditor('editor-code', 'editor-lines');

    // 2. Restore participant session
    const saved = localStorage.getItem('cc_participant');
    if (saved) {
      try {
        this.participant = JSON.parse(saved);
        this.updateUserBadge();
      } catch (e) {}
    }

    // 3. Fetch initial configuration & problems
    this.loadProblems();
    this.loadLeaderboard();
  },

  navigate(viewId) {
    document.querySelectorAll('.view-section').forEach(sec => sec.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(link => link.classList.remove('active'));

    const targetSec = document.getElementById(`view-${viewId}`);
    const targetLink = document.getElementById(`nav-${viewId}`);

    if (targetSec) targetSec.classList.add('active');
    if (targetLink) targetLink.classList.add('active');

    this.currentView = viewId;

    if (viewId === 'problems') this.loadProblems();
    if (viewId === 'leaderboard') this.loadLeaderboard();
    if (viewId === 'admin') Admin.checkHealth();
  },

  showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span>${type === 'success' ? '✓' : (type === 'error' ? '✖' : 'ℹ')}</span> <span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  },

  async handleRegister(e) {
    e.preventDefault();
    const name = document.getElementById('reg-name').value.trim();
    const college = document.getElementById('reg-college').value.trim();
    const reg_no = document.getElementById('reg-no').value.trim();

    try {
      const res = await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, college, reg_no })
      });
      const data = await res.json();
      if (data.success) {
        this.participant = data.participant;
        localStorage.setItem('cc_participant', JSON.stringify(data.participant));
        this.updateUserBadge();
        this.showToast(`Welcome, ${name}!`, 'success');
        this.navigate('problems');
      } else {
        this.showToast(data.error || 'Registration failed', 'error');
      }
    } catch (err) {
      this.showToast('Network error: ' + err.message, 'error');
    }
  },

  updateUserBadge() {
    if (!this.participant) return;
    document.getElementById('user-badge').style.display = 'flex';
    document.getElementById('user-name-display').textContent = this.participant.name;
    document.getElementById('user-score-display').textContent = `${this.participant.score || 0} pts`;
  },

  async loadProblems() {
    try {
      const pid = this.participant ? `?participant_id=${this.participant.id}` : '';
      const res = await fetch(`/api/problems${pid}`);
      const data = await res.json();
      this.problems = data.problems || [];
      this.renderProblemsTable(this.problems);
    } catch (e) {
      this.showToast('Failed to load problems: ' + e.message, 'error');
    }
  },

  renderProblemsTable(probs) {
    const tbody = document.getElementById('problems-table-body');
    if (!tbody) return;

    tbody.innerHTML = probs.map(p => `
      <tr onclick="App.openProblem('${p.id}')">
        <td>${p.solved ? '<span class="badge badge-solved">✓ Solved</span>' : '<span style="color:var(--text-muted)">-</span>'}</td>
        <td style="font-weight:600; color:#fff;">${p.title}</td>
        <td><span class="badge badge-${p.difficulty.toLowerCase()}">${p.difficulty}</span></td>
        <td style="font-family:var(--font-mono); font-weight:700; color:var(--accent-cyan);">${p.points} pts</td>
        <td style="color:var(--text-secondary);">${p.time_limit}s</td>
        <td><button class="btn btn-secondary" style="padding:0.3rem 0.75rem; font-size:0.8rem;">Solve ➔</button></td>
      </tr>
    `).join('');
  },

  filterProblems(difficulty, btn) {
    document.querySelectorAll('.filter-chips .chip').forEach(c => c.classList.remove('active'));
    if (btn) btn.classList.add('active');

    if (difficulty === 'all') {
      this.renderProblemsTable(this.problems);
    } else {
      this.renderProblemsTable(this.problems.filter(p => p.difficulty.toLowerCase() === difficulty.toLowerCase()));
    }
  },

  async openProblem(problemId) {
    try {
      const res = await fetch(`/api/problems/${problemId}`);
      const prob = await res.json();
      this.activeProblem = prob;

      document.getElementById('ide-prob-title').textContent = prob.title;
      const badge = document.getElementById('ide-prob-badge');
      badge.textContent = prob.difficulty;
      badge.className = `badge badge-${prob.difficulty.toLowerCase()}`;

      let samplesHtml = (prob.sample_tests || []).map((st, i) => `
        <div style="background:var(--bg-primary); padding:0.75rem; border-radius:6px; margin-top:0.75rem;">
          <div style="font-weight:700; color:var(--accent-cyan); font-size:0.85rem;">Example ${i + 1}</div>
          <div style="margin-top:0.25rem;"><strong>Input:</strong><pre style="font-family:var(--font-mono); font-size:0.85rem; color:#fff;">${st.input}</pre></div>
          <div style="margin-top:0.25rem;"><strong>Output:</strong><pre style="font-family:var(--font-mono); font-size:0.85rem; color:var(--accent-green);">${st.output}</pre></div>
        </div>
      `).join('');

      document.getElementById('ide-prob-description').innerHTML = `
        <div style="color:var(--text-primary); font-size:0.95rem; margin-bottom:1rem;">${prob.description}</div>
        <h4 style="color:var(--accent-cyan); font-size:0.9rem; margin-top:1rem;">Constraints</h4>
        <pre style="font-family:var(--font-mono); font-size:0.85rem; color:var(--text-secondary);">${prob.constraints || 'Standard constraints'}</pre>
        <h4 style="color:var(--accent-cyan); font-size:0.9rem; margin-top:1rem;">Sample Cases</h4>
        ${samplesHtml}
      `;

      this.handleLanguageChange();
      this.navigate('ide');
    } catch (e) {
      this.showToast('Error opening problem: ' + e.message, 'error');
    }
  },

  handleLanguageChange() {
    if (!this.activeProblem) return;
    this.currentLanguage = document.getElementById('ide-lang-select').value;
    const starter = (this.activeProblem.starter_code && this.activeProblem.starter_code[this.currentLanguage]) || '';
    this.editor.setValue(starter);
  },

  resetCode() {
    if (confirm('Reset code to starter template?')) {
      this.handleLanguageChange();
    }
  },

  switchOutputTab(tabId, btn) {
    document.querySelectorAll('.tabs-header .tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.panel-body .tab-pane').forEach(p => p.classList.remove('active'));

    btn.classList.add('active');
    document.getElementById(`tab-${tabId}`).classList.add('active');
  },

  async runCode() {
    if (!this.activeProblem) return;
    const code = this.editor.getValue();
    const btn = document.getElementById('btn-run');
    btn.disabled = true;
    btn.textContent = 'Running...';

    try {
      const res = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          problem_id: this.activeProblem.id,
          language: this.currentLanguage,
          code: code
        })
      });
      const data = await res.json();
      const r = data.result;

      let html = '';
      if (r.status === 'COMPILATION_ERROR') {
        html = `<div style="color:var(--accent-red); font-weight:700;">Compilation Error:</div><pre style="color:#ef4444; font-family:var(--font-mono); font-size:0.85rem; margin-top:0.5rem;">${r.error_message}</pre>`;
      } else {
        html = (r.results || []).map(t => `
          <div style="background:var(--bg-primary); padding:0.6rem; border-radius:6px; margin-bottom:0.5rem; border-left:4px solid ${t.passed ? 'var(--accent-green)' : 'var(--accent-red)'};">
            <div style="display:flex; justify-content:space-between; font-weight:700;">
              <span>Sample Test #${t.test_num}</span>
              <span style="color:${t.passed ? 'var(--accent-green)' : 'var(--accent-red)'};">${t.status} (${t.runtime}s)</span>
            </div>
            ${!t.passed ? `
              <div class="diff-view">
                <div class="diff-box expected"><strong>Expected:</strong><pre>${t.expected}</pre></div>
                <div class="diff-box actual"><strong>Actual:</strong><pre>${t.actual || t.error || ''}</pre></div>
              </div>
            ` : ''}
          </div>
        `).join('');
      }

      document.getElementById('sample-tests-container').innerHTML = html;
      this.switchOutputTab('sample-tests', document.querySelector('.tabs-header .tab-btn'));
      this.showToast(r.all_passed ? 'All sample tests passed!' : 'Some sample tests failed.', r.all_passed ? 'success' : 'warning');
    } catch (e) {
      this.showToast('Run error: ' + e.message, 'error');
    } finally {
      btn.disabled = false;
      btn.textContent = '▶ Run Tests';
    }
  },

  async submitCode() {
    if (!this.participant) {
      this.showToast('Please register first before submitting!', 'warning');
      this.navigate('register');
      return;
    }
    if (!this.activeProblem) return;

    const code = this.editor.getValue();
    const btn = document.getElementById('btn-submit');
    btn.disabled = true;
    btn.textContent = 'Grading...';

    try {
      const res = await fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          participant_id: this.participant.id,
          participant_name: this.participant.name,
          problem_id: this.activeProblem.id,
          language: this.currentLanguage,
          code: code
        })
      });
      const data = await res.json();

      const verdictEl = document.getElementById('submission-verdict-container');
      const isAccepted = data.status === 'ACCEPTED';

      verdictEl.innerHTML = `
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border-left:6px solid ${isAccepted ? 'var(--accent-green)' : 'var(--accent-red)'};">
          <div style="font-size:1.25rem; font-weight:800; color:${isAccepted ? 'var(--accent-green)' : 'var(--accent-red)'};">${data.status}</div>
          <div style="margin-top:0.5rem; color:var(--text-primary);">Test Cases Passed: <strong>${data.passed_count} / ${data.total_count}</strong></div>
          <div style="color:var(--accent-cyan); font-weight:700;">Score Earned: +${data.score_earned} pts</div>
          <div style="font-size:0.85rem; color:var(--text-muted); margin-top:0.25rem;">Total Runtime: ${data.runtime}s</div>
          ${data.error_message ? `<div style="color:var(--accent-red); margin-top:0.5rem; font-size:0.85rem;">${data.error_message}</div>` : ''}
        </div>
      `;

      // Switch to submission tab
      const subTabBtn = document.querySelectorAll('.tabs-header .tab-btn')[2];
      this.switchOutputTab('submission-res', subTabBtn);

      if (isAccepted) {
        this.showToast(`Accepted! Earned ${data.score_earned} points.`, 'success');
        this.participant.score = (this.participant.score || 0) + data.score_earned;
        this.updateUserBadge();
      } else {
        this.showToast(`Submission Verdict: ${data.status}`, 'error');
      }

      this.loadLeaderboard();
    } catch (e) {
      this.showToast('Submission error: ' + e.message, 'error');
    } finally {
      btn.disabled = false;
      btn.textContent = '🚀 Submit';
    }
  },

  async loadLeaderboard() {
    try {
      const res = await fetch('/api/leaderboard');
      const data = await res.json();
      this.leaderboardData = data.leaderboard || [];
      this.renderLeaderboard(this.leaderboardData);
    } catch (e) {
      console.error('Leaderboard load error:', e);
    }
  },

  renderLeaderboard(rows) {
    const tbody = document.getElementById('leaderboard-table-body');
    if (!tbody) return;

    tbody.innerHTML = rows.map(r => `
      <tr>
        <td style="font-weight:800; color:${r.rank === 1 ? 'gold' : (r.rank === 2 ? 'silver' : (r.rank === 3 ? '#cd7f32' : 'var(--text-muted)'))};">#${r.rank}</td>
        <td style="font-weight:600; color:#fff;">${r.name}</td>
        <td style="color:var(--text-secondary);">${r.college}</td>
        <td style="font-family:var(--font-mono); color:var(--text-muted);">${r.reg_no}</td>
        <td style="font-family:var(--font-mono); font-weight:800; color:var(--accent-green); font-size:1.05rem;">${r.score}</td>
        <td style="font-weight:700;">${r.solved_count} / 15</td>
        <td><span style="color:#10b981;">${r.easy_solved}E</span> · <span style="color:#f59e0b;">${r.medium_solved}M</span> · <span style="color:#ef4444;">${r.hard_solved}H</span></td>
        <td style="font-family:var(--font-mono); color:var(--text-secondary); font-size:0.85rem;">${r.total_runtime}s</td>
      </tr>
    `).join('');
  },

  filterLeaderboard() {
    const q = document.getElementById('leaderboard-search').value.toLowerCase();
    const filtered = (this.leaderboardData || []).filter(r => 
      r.name.toLowerCase().includes(q) || r.college.toLowerCase().includes(q) || r.reg_no.toLowerCase().includes(q)
    );
    this.renderLeaderboard(filtered);
  },

  exportLeaderboardCSV() {
    window.open('/api/admin/export/csv', '_blank');
  }
};

document.addEventListener('DOMContentLoaded', () => App.init());
window.App = App;
