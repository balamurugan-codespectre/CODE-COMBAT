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

  async init() {
    // 1. Initialize custom editor
    this.editor = new CodeEditor('editor-code', 'editor-lines');

    // 2. Restore participant session
    const saved = localStorage.getItem('cc_participant');
    if (saved) {
      try {
        this.participant = JSON.parse(saved);
        this.updateUserBadge();
        // Verify participant still exists on server (in case of Admin reset)
        this.syncParticipant();
      } catch (e) {
        this.participant = null;
        localStorage.removeItem('cc_participant');
      }
    }

    // 3. Fetch initial configuration & problems
    this.loadProblems();
    this.loadLeaderboard();
  },

  async syncParticipant() {
    if (!this.participant || !this.participant.id) return;
    try {
      const res = await fetch(`/api/participant/${this.participant.id}`);
      if (res.ok) {
        const data = await res.json();
        if (data.participant) {
          this.participant = data.participant;
          localStorage.setItem('cc_participant', JSON.stringify(data.participant));
          this.updateUserBadge();
        }
      } else if (res.status === 404) {
        // Admin wiped DB or participant deleted
        this.participant = null;
        localStorage.removeItem('cc_participant');
        const badge = document.getElementById('user-badge');
        if (badge) badge.style.display = 'none';
        this.loadProblems();
      }
    } catch (e) {
      // Offline fallback: keep cached session
    }
  },

  navigate(viewId) {
    const protectedViews = ['intro', 'problems', 'ide'];
    if (protectedViews.includes(viewId) && !this.participant) {
      this.showToast('Please register first to enter the arena and view rules/challenges!', 'warning');
      viewId = 'register';
    }

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

  logout() {
    if (confirm('Sign out of current participant session?')) {
      this.participant = null;
      localStorage.removeItem('cc_participant');
      document.getElementById('user-badge').style.display = 'none';
      this.showToast('Signed out successfully.', 'info');
      this.navigate('home');
    }
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
        this.showToast(`Welcome, ${name}! Please review competition rules.`, 'success');
        this.navigate('intro');
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

    tbody.innerHTML = probs.map(p => {
      const isSolved = Boolean(p.solved || p.status === 'Solved');
      return `
        <tr onclick="App.openProblem('${p.id}')">
          <td>
            ${isSolved 
              ? '<span class="badge badge-solved" style="background:rgba(16,185,129,0.2); color:var(--accent-green); border:1px solid var(--accent-green); font-weight:700;">✓ Solved</span>' 
              : '<span class="badge" style="background:rgba(148,163,184,0.1); color:var(--text-muted); border:1px solid var(--border-color);">Todo</span>'}
          </td>
          <td style="font-weight:600; color:#fff;">
            ${p.title}
            ${isSolved ? '<span style="color:var(--accent-green); font-size:0.85rem; margin-left:0.5rem;" title="Solved">✓</span>' : ''}
          </td>
          <td><span class="badge badge-${p.difficulty.toLowerCase()}">${p.difficulty}</span></td>
          <td style="font-family:var(--font-mono); font-weight:700; color:var(--accent-cyan);">${p.points} pts</td>
          <td style="color:var(--text-secondary);">${p.time_limit}s</td>
          <td>
            ${isSolved
              ? `<button class="btn btn-solved" style="padding:0.35rem 0.85rem; font-size:0.8rem; cursor:pointer;" onclick="event.stopPropagation(); App.openProblem('${p.id}')">Solved ✓</button>`
              : `<button class="btn btn-primary" style="padding:0.35rem 0.85rem; font-size:0.8rem; font-weight:600; cursor:pointer;" onclick="event.stopPropagation(); App.openProblem('${p.id}')">Solve ➔</button>`
            }
          </td>
        </tr>
      `;
    }).join('');
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
    if (!this.participant) {
      this.showToast('Please register first to access coding challenges!', 'warning');
      this.navigate('register');
      return;
    }
    try {
      const res = await fetch(`/api/problems/${problemId}`);
      const prob = await res.json();
      this.activeProblem = prob;

      const probMeta = this.problems.find(p => p.id === problemId);
      const isSolved = Boolean(probMeta && (probMeta.solved || probMeta.status === 'Solved'));

      document.getElementById('ide-prob-title').textContent = prob.title;
      const badge = document.getElementById('ide-prob-badge');
      badge.innerHTML = `${prob.difficulty}${isSolved ? ' &bull; &check; Solved' : ''}`;
      badge.className = `badge badge-${prob.difficulty.toLowerCase()}`;

      const visibleSamples = (prob.sample_tests || []).slice(0, 2);
      let samplesHtml = visibleSamples.map((st, i) => `
        <div style="background:var(--bg-primary); padding:0.75rem; border-radius:6px; margin-top:0.75rem; border:1px solid var(--border-color);">
          <div style="font-weight:700; color:var(--accent-cyan); font-size:0.85rem;">Example ${i + 1}</div>
          <div style="margin-top:0.25rem;"><strong>Input:</strong><pre style="font-family:var(--font-mono); font-size:0.85rem; color:#fff; background:rgba(0,0,0,0.3); padding:0.4rem; border-radius:4px;">${st.input}</pre></div>
          <div style="margin-top:0.25rem;"><strong>Output:</strong><pre style="font-family:var(--font-mono); font-size:0.85rem; color:var(--accent-green); background:rgba(0,0,0,0.3); padding:0.4rem; border-radius:4px;">${st.output}</pre></div>
          ${st.explanation ? `<div style="margin-top:0.35rem; font-size:0.85rem; color:var(--text-secondary);"><strong>Explanation:</strong> ${st.explanation}</div>` : ''}
        </div>
      `).join('');

      document.getElementById('ide-prob-description').innerHTML = `
        <div style="color:var(--text-primary); font-size:0.95rem; margin-bottom:1rem;">${prob.description}</div>
        <h4 style="color:var(--accent-cyan); font-size:0.9rem; margin-top:1rem;">Constraints</h4>
        <pre style="font-family:var(--font-mono); font-size:0.85rem; color:var(--text-secondary); background:rgba(0,0,0,0.2); padding:0.5rem; border-radius:4px;">${prob.constraints || 'Standard constraints'}</pre>
        <h4 style="color:var(--accent-cyan); font-size:0.9rem; margin-top:1rem;">Examples (2 of ${(prob.sample_tests || []).length} Sample Cases Shown)</h4>
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

    const customStdin = document.getElementById('custom-stdin')?.value || '';
    const activeTab = document.querySelector('.tabs-header .tab-btn.active')?.textContent || '';
    const isCustom = activeTab.includes('Custom');

    try {
      const res = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          problem_id: this.activeProblem.id,
          language: this.currentLanguage,
          code: code,
          custom_input: isCustom ? customStdin : undefined,
          is_custom: isCustom
        })
      });
      const data = await res.json().catch(() => ({ error: 'Invalid server response' }));

      if (!res.ok || data.error) {
        const errorMsg = data.error || `Run failed (HTTP ${res.status})`;
        document.getElementById('sample-tests-container').innerHTML = `
          <div style="color:var(--accent-red); font-weight:700;">Run Error:</div>
          <pre style="color:#ef4444; font-family:var(--font-mono); font-size:0.85rem; margin-top:0.5rem;">${errorMsg}</pre>
        `;
        this.switchOutputTab('sample-tests', document.querySelector('.tabs-header .tab-btn'));
        this.showToast(errorMsg, 'error');
        return;
      }

      if (data.is_custom) {
        const r = data.result || {};
        const outBox = document.getElementById('custom-stdout');
        if (outBox) {
          outBox.innerHTML = `
            <div style="color:var(--accent-cyan); font-weight:700; margin-bottom:0.25rem;">Verdict: ${r.status || 'DONE'} (${r.runtime ? r.runtime.toFixed(3) : 0}s)</div>
            ${r.stdout ? `<div style="color:#fff;"><strong>Stdout:</strong><pre style="margin-top:0.25rem; white-space:pre-wrap;">${r.stdout}</pre></div>` : ''}
            ${r.stderr || r.error ? `<div style="color:var(--accent-red); margin-top:0.5rem;"><strong>Stderr:</strong><pre style="margin-top:0.25rem; white-space:pre-wrap;">${r.stderr || r.error}</pre></div>` : ''}
          `;
        }
        this.switchOutputTab('custom-input', document.querySelectorAll('.tabs-header .tab-btn')[1]);
        this.showToast(`Custom run completed (${r.status})`, 'info');
        return;
      }

      const r = data.result || {};
      let html = '';
      if (r.status === 'COMPILATION_ERROR') {
        html = `<div style="color:var(--accent-red); font-weight:700;">Compilation Error:</div><pre style="color:#ef4444; font-family:var(--font-mono); font-size:0.85rem; margin-top:0.5rem; white-space:pre-wrap;">${r.error_message || 'Compilation failed.'}</pre>`;
      } else {
        html = (r.results || []).map(t => `
          <div style="background:var(--bg-primary); padding:0.6rem; border-radius:6px; margin-bottom:0.5rem; border-left:4px solid ${t.passed ? 'var(--accent-green)' : 'var(--accent-red)'};">
            <div style="display:flex; justify-content:space-between; font-weight:700;">
              <span>Sample Test #${t.test_num}</span>
              <span style="color:${t.passed ? 'var(--accent-green)' : 'var(--accent-red)'};">${t.status} (${typeof t.runtime === 'number' ? t.runtime.toFixed(3) : t.runtime}s)</span>
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
    if (!this.participant || !this.participant.id) {
      this.showToast('Please register first before submitting!', 'warning');
      this.navigate('register');
      return;
    }
    if (!this.activeProblem) {
      this.showToast('No active problem selected.', 'warning');
      return;
    }

    const code = this.editor.getValue();
    if (!code || !code.trim()) {
      this.showToast('Please write some code before submitting!', 'warning');
      return;
    }

    const btn = document.getElementById('btn-submit');
    btn.disabled = true;
    btn.textContent = 'Grading...';

    const verdictEl = document.getElementById('submission-verdict-container');
    const subTabBtn = document.querySelectorAll('.tabs-header .tab-btn')[2];

    try {
      const res = await fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          participant_id: this.participant.id,
          participant_name: this.participant.name || 'Anonymous',
          problem_id: this.activeProblem.id,
          language: this.currentLanguage,
          code: code
        })
      });

      const data = await res.json().catch(() => ({ error: 'Failed to parse server response' }));

      if (!res.ok || data.error || !data.status) {
        const errorMsg = data.error || `Evaluation failed (HTTP ${res.status})`;
        verdictEl.innerHTML = `
          <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border-left:6px solid var(--accent-red);">
            <div style="font-size:1.25rem; font-weight:800; color:var(--accent-red);">Submission Error</div>
            <div style="margin-top:0.5rem; color:#ef4444; font-size:0.9rem;">${errorMsg}</div>
            ${data.error_message ? `<pre style="color:#ef4444; font-family:var(--font-mono); font-size:0.85rem; margin-top:0.5rem; white-space:pre-wrap;">${data.error_message}</pre>` : ''}
          </div>
        `;
        this.switchOutputTab('submission-res', subTabBtn);
        this.showToast(errorMsg, 'error');
        return;
      }

      const status = data.status || 'ERROR';
      const isAccepted = status === 'ACCEPTED';
      const passedCount = Number(data.passed_count ?? 0);
      const totalCount = Number(data.total_count ?? (this.activeProblem.hidden_tests ? this.activeProblem.hidden_tests.length : 5));
      const scoreEarned = Number(data.score_earned ?? 0);
      const runtime = typeof data.runtime === 'number' ? data.runtime.toFixed(3) : (data.runtime || '0.000');
      
      let statusColor = 'var(--accent-cyan)';
      if (isAccepted) statusColor = 'var(--accent-green)';
      else if (status === 'TIME_LIMIT_EXCEEDED') statusColor = 'var(--accent-amber)';
      else if (['WRONG_ANSWER', 'COMPILATION_ERROR', 'RUNTIME_ERROR'].includes(status)) statusColor = 'var(--accent-red)';

      verdictEl.innerHTML = `
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border-left:6px solid ${statusColor};">
          <div style="font-size:1.25rem; font-weight:800; color:${statusColor};">${status}</div>
          <div style="margin-top:0.5rem; color:var(--text-primary);">Test Cases Passed: <strong>${passedCount} / ${totalCount}</strong></div>
          <div style="color:var(--accent-cyan); font-weight:700;">Score Earned: +${scoreEarned} pts</div>
          <div style="font-size:0.85rem; color:var(--text-muted); margin-top:0.25rem;">Total Runtime: ${runtime}s</div>
          ${data.already_solved ? `<div style="color:var(--accent-green); font-size:0.85rem; margin-top:0.35rem;">✓ Problem already solved previously. Points are recorded.</div>` : ''}
          ${data.error_message ? `<div style="color:var(--accent-red); margin-top:0.5rem; font-size:0.85rem; white-space:pre-wrap; font-family:var(--font-mono);">${data.error_message}</div>` : ''}
        </div>
      `;

      this.switchOutputTab('submission-res', subTabBtn);

      if (isAccepted) {
        this.showToast(`Accepted! Earned ${scoreEarned} points.`, 'success');
        if (scoreEarned > 0) {
          this.participant.score = (this.participant.score || 0) + scoreEarned;
          localStorage.setItem('cc_participant', JSON.stringify(this.participant));
          this.updateUserBadge();
        }
        this.loadProblems();
      } else {
        this.showToast(`Submission Verdict: ${status}`, 'error');
      }

      this.loadLeaderboard();
    } catch (e) {
      verdictEl.innerHTML = `
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border-left:6px solid var(--accent-red);">
          <div style="font-size:1.25rem; font-weight:800; color:var(--accent-red);">Network Error</div>
          <div style="margin-top:0.5rem; color:#ef4444; font-size:0.9rem;">${e.message}</div>
        </div>
      `;
      this.switchOutputTab('submission-res', subTabBtn);
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
