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

    // 3. Ensure Admin is locked on startup
    if (window.Admin && typeof window.Admin.lock === 'function') {
      window.Admin.lock();
    }

    // 4. Fetch initial configuration & problems
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

    // Always lock Admin Panel whenever entering Admin or leaving Admin view
    if (viewId === 'admin' || this.currentView === 'admin') {
      if (window.Admin && typeof window.Admin.lock === 'function') {
        window.Admin.lock();
      }
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
    if (viewId === 'admin') {
      Admin.checkAuthUI();
    }
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

  tierLocks: { easy: false, medium: false, hard: false },
  currentFilter: 'all',
  folderCollapsed: { easy: false, medium: false, hard: false },

  async loadProblems() {
    try {
      const pid = this.participant ? `?participant_id=${this.participant.id}` : '';
      const res = await fetch(`/api/problems${pid}`);
      const data = await res.json();
      this.problems = data.problems || [];
      this.tierLocks = data.tier_locks || { easy: false, medium: false, hard: false };

      const easyLocked = Boolean(this.tierLocks.easy);
      const medLocked = Boolean(this.tierLocks.medium);
      const hardLocked = Boolean(this.tierLocks.hard);
      
      const lockEasyEl = document.getElementById('chip-lock-easy');
      const lockMedEl = document.getElementById('chip-lock-medium');
      const lockHardEl = document.getElementById('chip-lock-hard');
      if (lockEasyEl) lockEasyEl.textContent = easyLocked ? '🔒' : '🔓';
      if (lockMedEl) lockMedEl.textContent = medLocked ? '🔒' : '🔓';
      if (lockHardEl) lockHardEl.textContent = hardLocked ? '🔒' : '🔓';

      this.renderProblemsFolders(this.problems);
    } catch (e) {
      this.showToast('Failed to load problems: ' + e.message, 'error');
    }
  },

  toggleFolder(tier) {
    this.folderCollapsed[tier] = !this.folderCollapsed[tier];
    const bodyEl = document.getElementById(`folder-body-${tier}`);
    const iconEl = document.getElementById(`folder-arrow-${tier}`);
    if (bodyEl) {
      bodyEl.style.display = this.folderCollapsed[tier] ? 'none' : 'block';
    }
    if (iconEl) {
      iconEl.textContent = this.folderCollapsed[tier] ? '▶' : '▼';
    }
  },

  renderProblemsFolders(probs) {
    const container = document.getElementById('category-folders-container');
    if (!container) return;

    const categories = [
      {
        id: 'easy',
        num: 1,
        name: 'Easy Challenges',
        diff: 'Easy',
        points: 100,
        color: 'var(--accent-green)',
        colorRgb: '16, 185, 129',
        badgeBg: 'rgba(16, 185, 129, 0.15)',
        badgeBorder: 'var(--accent-green)'
      },
      {
        id: 'medium',
        num: 2,
        name: 'Medium Challenges',
        diff: 'Medium',
        points: 200,
        color: 'var(--accent-amber)',
        colorRgb: '245, 158, 11',
        badgeBg: 'rgba(245, 158, 11, 0.15)',
        badgeBorder: 'var(--accent-amber)'
      },
      {
        id: 'hard',
        num: 3,
        name: 'Hard Challenges',
        diff: 'Hard',
        points: 300,
        color: 'var(--accent-red)',
        colorRgb: '239, 68, 68',
        badgeBg: 'rgba(239, 68, 68, 0.15)',
        badgeBorder: 'var(--accent-red)'
      }
    ];

    const filter = this.currentFilter || 'all';
    const visibleCategories = categories.filter(c => filter === 'all' || c.diff.toLowerCase() === filter.toLowerCase());

    container.innerHTML = visibleCategories.map(cat => {
      const catProbs = probs.filter(p => p.difficulty.toLowerCase() === cat.diff.toLowerCase());
      const isLocked = Boolean(this.tierLocks[cat.id]);
      const solvedCount = catProbs.filter(p => p.solved || p.status === 'Solved').length;
      const totalCount = catProbs.length || 5;
      const pct = Math.round((solvedCount / totalCount) * 100);
      const isCollapsed = Boolean(this.folderCollapsed[cat.id]);

      let folderStatusBadge = '';
      if (isLocked) {
        folderStatusBadge = `<span class="badge" style="background:rgba(239,68,68,0.18); color:var(--accent-red); border:1px solid var(--accent-red); font-weight:700;">🔒 LOCKED (Admin Password Required)</span>`;
      } else if (solvedCount === totalCount && totalCount > 0) {
        folderStatusBadge = `<span class="badge badge-solved" style="background:rgba(16,185,129,0.2); color:var(--accent-green); border:1px solid var(--accent-green); font-weight:700;">✓ ALL ${totalCount} SOLVED</span>`;
      } else {
        folderStatusBadge = `<span class="badge" style="background:${cat.badgeBg}; color:${cat.color}; border:1px solid ${cat.badgeBorder}; font-weight:700;">🔓 UNLOCKED &bull; ROUND ${cat.num}</span>`;
      }

      let bodyContent = '';
      if (isLocked) {
        bodyContent = `
          <div class="folder-locked-banner">
            <div class="folder-locked-info">
              <div style="font-size:2rem;">🔒</div>
              <div>
                <h4 style="color:#fff; margin:0 0 0.25rem 0; font-size:1.05rem;">Folder Locked: Category ${cat.num} (${cat.diff})</h4>
                <p style="color:var(--text-secondary); margin:0; font-size:0.85rem;">
                  This category folder is locked for sequential round progression. Unlock it once with Administrator credentials to grant access for all participants without asking again.
                </p>
              </div>
            </div>
            <button class="btn btn-primary" style="background:linear-gradient(135deg, var(--accent-amber), #d97706); border-color:var(--accent-amber); color:#000; font-weight:700; padding:0.6rem 1.25rem; font-size:0.9rem; white-space:nowrap;" onclick="event.stopPropagation(); App.openRoundLockModal('', ${cat.num}, '${cat.diff}')">
              🔓 Unlock Category ${cat.num} (Admin Password)
            </button>
          </div>
        `;
      } else {
        bodyContent = `
          <div class="folder-body" id="folder-body-${cat.id}" style="display:${isCollapsed ? 'none' : 'block'};">
            <table class="folder-table">
              <thead>
                <tr>
                  <th style="width:100px;">Status</th>
                  <th>Problem Title</th>
                  <th style="width:140px;">Difficulty</th>
                  <th style="width:110px;">Points</th>
                  <th style="width:130px; text-align:center;">Action</th>
                </tr>
              </thead>
              <tbody>
                ${catProbs.map(p => {
                  const isProbSolved = Boolean(p.solved || p.status === 'Solved');
                  const probNum = p.number ? `${p.number}. ` : '';
                  return `
                    <tr onclick="App.openProblem('${p.id}')" style="cursor:pointer;">
                      <td>
                        ${isProbSolved 
                          ? '<span class="badge badge-solved" style="background:rgba(16,185,129,0.2); color:var(--accent-green); border:1px solid var(--accent-green); font-weight:700;">✓ Solved</span>' 
                          : '<span class="badge" style="background:rgba(148,163,184,0.1); color:var(--text-muted); border:1px solid var(--border-color);">Todo</span>'}
                      </td>
                      <td style="font-weight:600; color:#fff;">
                        ${probNum}${p.title}
                        ${isProbSolved ? '<span style="color:var(--accent-green); font-size:0.85rem; margin-left:0.5rem;" title="Solved">✓</span>' : ''}
                      </td>
                      <td>
                        <span class="badge badge-${p.difficulty.toLowerCase()}" style="font-size:0.75rem;">
                          ${p.difficulty}
                        </span>
                      </td>
                      <td style="font-family:var(--font-mono); font-weight:700; color:var(--accent-cyan);">${p.points} pts</td>
                      <td style="text-align:center;">
                        ${isProbSolved
                          ? `<button class="btn btn-solved" style="padding:0.35rem 0.85rem; font-size:0.8rem; cursor:pointer;" onclick="event.stopPropagation(); App.openProblem('${p.id}')">Solved ✓</button>`
                          : `<button class="btn btn-primary" style="padding:0.35rem 0.85rem; font-size:0.8rem; font-weight:600; cursor:pointer;" onclick="event.stopPropagation(); App.openProblem('${p.id}')">Solve ➔</button>`
                        }
                      </td>
                    </tr>
                  `;
                }).join('')}
              </tbody>
            </table>
          </div>
        `;
      }

      return `
        <div class="category-folder-card folder-${cat.id} ${isLocked ? 'is-locked' : ''}" id="category-card-${cat.id}">
          <div class="category-folder-header" onclick="${isLocked ? `App.openRoundLockModal('', ${cat.num}, '${cat.diff}')` : `App.toggleFolder('${cat.id}')`}">
            <div class="folder-title-group">
              <div class="folder-icon" style="color:${isLocked ? 'var(--accent-red)' : cat.color};">
                ${isLocked ? '🔒' : (solvedCount === totalCount && totalCount > 0 ? '🏆' : '📁')}
              </div>
              <div>
                <div class="folder-name">
                  <span>Category ${cat.num}: ${cat.name}</span>
                  ${folderStatusBadge}
                </div>
                <div class="folder-meta">
                  <span>${totalCount} Challenges</span>
                  <span>&bull;</span>
                  <span>${cat.points} Points Each</span>
                  <span>&bull;</span>
                  <span>
                    Solved: <strong style="color:${solvedCount > 0 ? 'var(--accent-green)' : '#fff'};">${solvedCount}/${totalCount}</strong>
                    <span class="folder-progress-bar-bg">
                      <span class="folder-progress-bar-fill" style="width:${pct}%; background:${cat.color};"></span>
                    </span>
                  </span>
                </div>
              </div>
            </div>

            <div class="folder-actions">
              ${isLocked 
                ? `<button class="btn btn-secondary" style="font-size:0.8rem; padding:0.35rem 0.75rem; border-color:var(--accent-amber); color:var(--accent-amber);" onclick="event.stopPropagation(); App.openRoundLockModal('', ${cat.num}, '${cat.diff}')">🔑 Enter Password</button>`
                : `<span id="folder-arrow-${cat.id}" style="color:var(--text-muted); font-size:0.9rem; font-weight:bold;">${isCollapsed ? '▶' : '▼'}</span>`
              }
            </div>
          </div>

          ${bodyContent}
        </div>
      `;
    }).join('');
  },

  filterProblems(difficulty, btn) {
    document.querySelectorAll('.filter-chips .chip').forEach(c => c.classList.remove('active'));
    if (btn) btn.classList.add('active');
    this.currentFilter = difficulty;
    this.renderProblemsFolders(this.problems);
  },

  toggleProblemSection(sectionId) {
    const el = document.getElementById(`lc-sec-${sectionId}`);
    const btn = document.getElementById(`lc-btn-${sectionId}`);
    if (!el) return;
    const isHidden = (el.style.display === 'none' || !el.style.display);
    el.style.display = isHidden ? 'block' : 'none';
    if (btn) {
      if (isHidden) btn.classList.add('active');
      else btn.classList.remove('active');
    }
  },

  copySampleInput(encodedText) {
    try {
      const text = decodeURIComponent(encodedText);
      navigator.clipboard.writeText(text).then(() => {
        this.showToast('📋 Sample input copied to clipboard!', 'success');
      }).catch(() => {
        // Fallback for older browsers / iframe contexts
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        this.showToast('📋 Sample input copied to clipboard!', 'success');
      });
    } catch (e) {
      this.showToast('Failed to copy sample input', 'warning');
    }
  },

  escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  },

  copyErrorMessage(encodedText) {
    try {
      const text = decodeURIComponent(encodedText);
      navigator.clipboard.writeText(text).then(() => {
        this.showToast('📋 Error message copied to clipboard!', 'info');
      }).catch(() => {
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        this.showToast('📋 Error message copied to clipboard!', 'info');
      });
    } catch (e) {
      this.showToast('Failed to copy error message', 'warning');
    }
  },

  renderErrorBox({ type, title, message, tips, meta, warningStyle } = {}) {
    const rawMsg = (message || 'An error occurred during execution.').trim();
    const encodedMsg = encodeURIComponent(rawMsg);
    const boxClass = warningStyle ? 'error-box-card warning-style' : 'error-box-card';
    
    let defaultTitle = 'Execution Error';
    let icon = '⚠️';
    if (type === 'COMPILATION') {
      defaultTitle = 'Compilation / Syntax Error';
      icon = '❌';
    } else if (type === 'RUNTIME') {
      defaultTitle = 'Runtime Error / Exception';
      icon = '💥';
    } else if (type === 'TLE') {
      defaultTitle = 'Time Limit Exceeded';
      icon = '⏱️';
    } else if (type === 'WA') {
      defaultTitle = 'Wrong Answer (Output Mismatch)';
      icon = '❌';
    }

    const displayTitle = title || defaultTitle;

    // Generate beginner-friendly smart debugging tips
    let autoTip = tips;
    if (!autoTip) {
      const lower = rawMsg.toLowerCase();
      if (lower.includes('syntaxerror') || lower.includes('expected') || lower.includes(';') || lower.includes('error: expected')) {
        autoTip = 'Check for missing semicolons <code>;</code>, unmatched parentheses <code>()</code>, brackets <code>[]</code>, curly braces <code>{}</code>, or missing colons <code>:</code>.';
      } else if (lower.includes('nameerror') || lower.includes('cannot find symbol') || lower.includes('undeclared identifier')) {
        autoTip = 'A variable, function, or method name is misspelled, not defined, or declared in a different scope.';
      } else if (lower.includes('indexerror') || lower.includes('arrayindexoutofboundsexception') || lower.includes('segmentation fault') || lower.includes('out of bounds')) {
        autoTip = 'Array or list index out of range. Ensure your loop bounds stay within valid indexes (e.g. <code>i &lt; len(arr)</code> or <code>i &lt; n</code>).';
      } else if (lower.includes('zerodivisionerror') || lower.includes('/ by zero') || lower.includes('arithmeticexception')) {
        autoTip = 'Division or modulo by zero occurred. Add a check to confirm the denominator is not zero before dividing.';
      } else if (lower.includes('nullpointerexception') || lower.includes('nonetype') || lower.includes('none type') || lower.includes('null')) {
        autoTip = 'Null or NoneType reference accessed. Ensure objects, arrays, or return values are properly initialized before accessing their properties.';
      } else if (lower.includes('timed out') || lower.includes('time limit') || type === 'TLE') {
        autoTip = 'Execution exceeded runtime limit (> 2.0s). Check for infinite loops (<code>while</code> conditions that never terminate) or optimize nested loops from $O(N^2)$ to $O(N)$.';
      } else if (lower.includes('wrong answer') || type === 'WA') {
        autoTip = 'Your output does not match expected output. Verify your logic against edge cases (zeroes, negative numbers, single elements) and check spacing/newlines.';
      }
    }

    return `
      <div class="${boxClass}">
        <div class="error-box-header">
          <div class="error-box-title-group">
            <span class="error-badge-icon">${icon}</span>
            <span class="error-box-title">${displayTitle}</span>
          </div>
          <div style="display:flex; align-items:center; gap:0.5rem;">
            ${meta ? `<span class="error-box-meta">${meta}</span>` : ''}
            <button class="copy-error-btn" onclick="App.copyErrorMessage('${encodedMsg}')">📋 Copy Error</button>
          </div>
        </div>
        <pre class="error-terminal"><code>${this.escapeHtml(rawMsg)}</code></pre>
        ${autoTip ? `
          <div class="error-tips-box">
            <span>💡</span>
            <div><strong>Debugging Tip:</strong> ${autoTip}</div>
          </div>
        ` : ''}
      </div>
    `;
  },

  async openProblem(problemId) {
    if (!this.participant) {
      this.showToast('Please register first to access coding challenges!', 'warning');
      this.navigate('register');
      return;
    }

    const probMeta = this.problems.find(p => p.id === problemId);
    if (probMeta && probMeta.locked) {
      const roundNum = probMeta.round_num || (probMeta.difficulty === 'Easy' ? 1 : (probMeta.difficulty === 'Medium' ? 2 : 3));
      this.openRoundLockModal(problemId, roundNum, probMeta.difficulty || 'Easy');
      return;
    }

    try {
      const pidParam = this.participant ? `?participant_id=${this.participant.id}` : '';
      const res = await fetch(`/api/problems/${problemId}${pidParam}`);
      if (!res.ok) {
        if (res.status === 403) {
          const errData = await res.json();
          this.showToast(errData.error || 'This round is currently locked by the administrator.', 'warning');
          const roundNum = probMeta ? probMeta.round_num : 1;
          const diff = probMeta ? probMeta.difficulty : 'Easy';
          this.openRoundLockModal(problemId, roundNum, diff);
          return;
        }
      }
      const prob = await res.json();
      if (prob.locked) {
        this.openRoundLockModal(problemId, prob.round_num || 1, prob.difficulty || 'Easy');
        return;
      }
      this.activeProblem = prob;

      const isSolved = Boolean(probMeta && (probMeta.solved || probMeta.status === 'Solved'));
      const probNum = prob.number ? `${prob.number}. ` : '';

      document.getElementById('ide-prob-title').textContent = `${probNum}${prob.title}`;
      const badge = document.getElementById('ide-prob-badge');
      badge.innerHTML = `Round ${prob.round_num || 1}: ${prob.difficulty}${isSolved ? ' &bull; &check; Solved' : ''}`;
      badge.className = `badge badge-${prob.difficulty.toLowerCase()}`;

      // 1. Interactive Chips (Topics, Companies, Hints)
      const topicsList = prob.topics || [prob.category || 'Algorithms'];
      const companiesList = prob.companies || ['Amazon', 'Google', 'Microsoft', 'Meta'];
      const hintsList = prob.hints || [];

      const topicsPills = topicsList.map(t => `<span class="lc-tag-pill">🏷️ ${t}</span>`).join('');
      const companiesPills = companiesList.map(c => `<span class="lc-tag-pill" style="border-color:rgba(0,242,254,0.3); color:var(--accent-cyan);">🏢 ${c}</span>`).join('');
      const hintsContentHtml = this.renderHintsHtml(hintsList, prob.total_hint_penalty || 0, prob.max_score || prob.points, prob.points);

      // 2. Beginner-friendly Sample Test Cases & Format
      const inputFormatHtml = prob.input_format ? `
        <div class="io-format-card">
          <div class="io-format-title">📥 Input Format</div>
          <div class="io-format-text">${prob.input_format}</div>
        </div>
      ` : '';

      const outputFormatHtml = prob.output_format ? `
        <div class="io-format-card output-card">
          <div class="io-format-title">📤 Output Format</div>
          <div class="io-format-text">${prob.output_format}</div>
        </div>
      ` : '';

      const ioGridHtml = (inputFormatHtml || outputFormatHtml) ? `
        <div class="io-format-grid">
          ${inputFormatHtml}
          ${outputFormatHtml}
        </div>
      ` : '';

      const samples = (prob.sample_tests && prob.sample_tests.length > 0) ? prob.sample_tests : (prob.leetcode_examples || []);
      const sampleCasesHtml = samples.slice(0, 4).map((st, i) => {
        const rawIn = st.input || '';
        const rawOut = st.output || '';
        const encodedIn = encodeURIComponent(rawIn);
        return `
          <div class="sample-case-card">
            <div class="sample-case-header">
              <span class="sample-case-title">Sample Test Case ${i + 1}</span>
              <button class="copy-input-btn" onclick="App.copySampleInput('${encodedIn}')">📋 Copy Input</button>
            </div>
            <div class="sample-case-grid">
              <div>
                <div class="sample-label">Sample Input:</div>
                <pre class="sample-pre"><code>${rawIn}</code></pre>
              </div>
              <div>
                <div class="sample-label">Expected Output:</div>
                <pre class="sample-pre output-pre"><code>${rawOut}</code></pre>
              </div>
            </div>
            ${st.explanation ? `<div class="sample-explanation"><strong>💡 Explanation:</strong> ${st.explanation}</div>` : ''}
          </div>
        `;
      }).join('');

      // 3. Constraints items
      const rawConstraints = prob.constraints || 'Standard constraints apply.';
      const constraintLines = rawConstraints.split('\n').filter(c => c.trim().length > 0);
      const constraintsHtml = constraintLines.map(line => `<li class="lc-constraint-item">${line.replace(/`/g, '')}</li>`).join('');

      // 4. Render Problem Pane
      const maxScoreDisplay = prob.max_score || prob.points;
      const penaltyDisplay = prob.total_hint_penalty || 0;

      document.getElementById('ide-prob-description').innerHTML = `
        <!-- Header Metadata & Action Chips -->
        <div class="lc-header-tags">
          ${isSolved ? '<span class="badge badge-solved" style="background:rgba(16,185,129,0.15); color:var(--accent-green); border:1px solid var(--accent-green); font-size:0.75rem;">✓ Solved</span>' : '<span class="badge" style="background:rgba(148,163,184,0.1); color:var(--text-muted); border:1px solid var(--border-color); font-size:0.75rem;">Todo</span>'}
          <span class="badge badge-${prob.difficulty.toLowerCase()}" style="font-size:0.75rem;">${prob.difficulty}</span>
          <span id="ide-prob-points-badge" style="font-family:var(--font-mono); font-size:0.78rem; font-weight:700; color:${penaltyDisplay > 0 ? 'var(--accent-amber)' : 'var(--accent-cyan)'}; background:rgba(0,242,254,0.08); padding:0.2rem 0.5rem; border-radius:4px; border:1px solid rgba(0,242,254,0.2);" title="Current Max Earnable Score">Max: ${maxScoreDisplay} / ${prob.points} pts</span>
          
          <button class="lc-chip-btn" id="lc-btn-topics" onclick="App.toggleProblemSection('topics')">🏷️ Topics</button>
          <button class="lc-chip-btn" id="lc-btn-companies" onclick="App.toggleProblemSection('companies')">🏢 Companies</button>
          <button class="lc-chip-btn" id="lc-btn-hints" onclick="App.toggleProblemSection('hints')">💡 Hints (3)</button>
        </div>

        <!-- Hidden Sections: Topics, Companies, Hints -->
        <div id="lc-sec-topics" class="lc-section-box" style="display:none;">
          <div style="font-size:0.8rem; font-weight:700; color:var(--text-secondary); margin-bottom:0.4rem;">Related Topics:</div>
          <div>${topicsPills}</div>
        </div>

        <div id="lc-sec-companies" class="lc-section-box" style="display:none;">
          <div style="font-size:0.8rem; font-weight:700; color:var(--text-secondary); margin-bottom:0.4rem;">Asked By Companies:</div>
          <div>${companiesPills}</div>
        </div>

        <div id="lc-sec-hints" class="lc-section-box" style="display:none;">
          ${hintsContentHtml}
        </div>

        <!-- Beginner Tip Banner -->
        <div class="beginner-tip-banner">
          <span>💡 <strong>Beginner Friendly:</strong> Starter code with input reading is pre-loaded in the editor. Write your logic where indicated, or write your own custom function. Both are evaluated automatically!</span>
        </div>

        <!-- Problem Description Statement -->
        <div style="color:var(--text-primary); font-size:0.95rem; line-height:1.7; margin-bottom:1.25rem;">
          ${prob.description.replace(/\n\n/g, '<br><br>')}
        </div>

        <!-- Input / Output Specifications -->
        ${ioGridHtml}

        <!-- Sample Test Cases Section -->
        <div style="margin-top:1.5rem;">
          <h4 style="color:#fff; font-size:0.92rem; margin-bottom:0.75rem; display:flex; align-items:center; gap:0.4rem;">🧪 Sample Test Cases:</h4>
          ${sampleCasesHtml}
        </div>

        <!-- Constraints Section -->
        <div style="margin-top:1.5rem;">
          <h4 style="color:#fff; font-size:0.92rem; margin-bottom:0.5rem;">Constraints:</h4>
          <ul class="lc-constraints-list">
            ${constraintsHtml}
          </ul>
        </div>
      `;

      this.handleLanguageChange();
      this.navigate('ide');
    } catch (e) {
      this.showToast('Error opening problem: ' + e.message, 'error');
    }
  },

  renderHintsHtml(hints, totalPenalty, maxScore, basePoints) {
    if (!hints || !hints.length) {
      return '<div style="color:var(--text-muted); font-size:0.85rem;">No hints available for this problem.</div>';
    }
    return `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
        <span style="font-size:0.85rem; font-weight:700; color:var(--accent-amber);">💡 3-Tier Progressive Hints:</span>
        <span style="font-size:0.75rem; color:var(--text-muted); font-family:var(--font-mono);">
          Max Score: <strong style="color:var(--accent-cyan);">${maxScore}</strong> / ${basePoints} pts
          ${totalPenalty > 0 ? `<span style="color:#ef4444; margin-left:0.35rem;">(-${totalPenalty} penalty)</span>` : ''}
        </span>
      </div>
      <div class="lc-hints-container">
        ${hints.map(h => {
          if (h.unlocked) {
            return `
              <div class="lc-hint-card unlocked">
                <div class="lc-hint-header">
                  <span class="lc-hint-title">💡 Hint ${h.index}</span>
                  <span class="lc-hint-badge penalty-badge">✓ Unlocked (-${h.penalty} pts)</span>
                </div>
                <div class="lc-hint-text">${h.text || 'Hint unlocked.'}</div>
              </div>
            `;
          } else {
            return `
              <div class="lc-hint-card locked" id="hint-card-${h.index}">
                <div class="lc-hint-header">
                  <span class="lc-hint-title">🔒 Hint ${h.index}</span>
                  <span class="lc-hint-cost">Penalty: -${h.penalty} pts</span>
                </div>
                <div class="lc-hint-lock-desc">
                  Viewing this progressive clue will deduct <strong>${h.penalty} points</strong> from your maximum score for this problem.
                </div>
                <div>
                  <button class="btn btn-unlock-hint" onclick="App.unlockHint(${h.index}, ${h.penalty})">
                    🔓 Unlock Hint ${h.index} (-${h.penalty} pts)
                  </button>
                </div>
              </div>
            `;
          }
        }).join('')}
      </div>
    `;
  },

  async unlockHint(hintIndex, penalty) {
    if (!this.participant || !this.participant.id) {
      this.showToast('Please register first to unlock hints.', 'warning');
      return;
    }
    if (!this.activeProblem) return;

    const confirmed = confirm(
      `Unlock Hint ${hintIndex}?\n\nViewing this hint will permanently deduct ${penalty} points from your maximum score for "${this.activeProblem.title}".\n\nDo you want to unlock it?`
    );
    if (!confirmed) return;

    try {
      const res = await fetch('/api/problems/unlock-hint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          participant_id: this.participant.id,
          problem_id: this.activeProblem.id,
          hint_index: hintIndex
        })
      });
      const data = await res.json();
      if (data.success) {
        if (this.activeProblem.hints) {
          const targetHint = this.activeProblem.hints.find(h => h.index === hintIndex);
          if (targetHint) {
            targetHint.unlocked = true;
            targetHint.text = data.hint_text;
          }
        }
        this.activeProblem.max_score = data.max_score;
        this.activeProblem.total_hint_penalty = data.total_hint_penalty;

        const ptsBadge = document.getElementById('ide-prob-points-badge');
        if (ptsBadge) {
          ptsBadge.textContent = `Max: ${data.max_score} / ${this.activeProblem.points} pts`;
          if (data.total_hint_penalty > 0) {
            ptsBadge.style.color = 'var(--accent-amber)';
            ptsBadge.title = `Total Hint Penalty: -${data.total_hint_penalty} pts`;
          }
        }

        const hintsSec = document.getElementById('lc-sec-hints');
        if (hintsSec) {
          hintsSec.innerHTML = this.renderHintsHtml(
            this.activeProblem.hints,
            data.total_hint_penalty,
            data.max_score,
            this.activeProblem.points
          );
        }

        if (typeof data.participant_score === 'number' && this.participant) {
          this.participant.score = data.participant_score;
          localStorage.setItem('cc_participant', JSON.stringify(this.participant));
          this.updateUserBadge();
        }
        this.loadLeaderboard();

        this.showToast(`Hint ${hintIndex} unlocked! (-${penalty} pts). Total Score: ${this.participant ? this.participant.score : 0} pts`, 'info');
      } else {
        this.showToast(data.error || 'Failed to unlock hint', 'error');
      }
    } catch (e) {
      this.showToast('Error unlocking hint: ' + e.message, 'error');
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

  openRoundLockModal(problemId, roundNum, difficulty) {
    const modal = document.getElementById('modal-round-lock');
    const titleEl = document.getElementById('round-lock-modal-title');
    const descEl = document.getElementById('round-lock-modal-desc');
    const tierInput = document.getElementById('round-lock-tier');
    const targetInput = document.getElementById('round-lock-target-prob');
    const idInput = document.getElementById('round-lock-id');
    const passInput = document.getElementById('round-lock-pass');
    const errorEl = document.getElementById('round-lock-error');

    const diff = (difficulty || 'Easy').trim();
    const diffLower = diff.toLowerCase();
    const round = roundNum || (diffLower === 'easy' ? 1 : (diffLower === 'medium' ? 2 : 3));

    if (titleEl) titleEl.innerHTML = `🔒 Category ${round}: ${diff} Tier Locked`;
    if (descEl) descEl.innerHTML = `<strong>Round ${round} (${diff} Challenges)</strong> is currently locked by the event administrator for sequential round competition. Enter administrator credentials to unlock this entire round for all participants:`;
    if (tierInput) tierInput.value = diffLower;
    if (targetInput) targetInput.value = problemId || '';
    if (errorEl) {
      errorEl.textContent = '';
      errorEl.style.display = 'none';
    }

    if (idInput) {
      const savedAdminId = (typeof Admin !== 'undefined' && Admin.getAdminId && Admin.getAdminId()) || localStorage.getItem('cc_admin_id') || '';
      idInput.value = savedAdminId;
    }
    if (passInput) passInput.value = '';

    if (modal) {
      modal.style.display = 'flex';
      setTimeout(() => {
        if (idInput && !idInput.value.trim()) {
          idInput.focus();
        } else if (passInput) {
          passInput.focus();
        }
      }, 50);
    }
  },

  closeRoundLockModal() {
    const modal = document.getElementById('modal-round-lock');
    if (modal) modal.style.display = 'none';
  },

  toggleRoundPassVisibility() {
    const passInput = document.getElementById('round-lock-pass');
    if (!passInput) return;
    passInput.type = passInput.type === 'password' ? 'text' : 'password';
  },

  async submitRoundUnlock(e) {
    if (e) e.preventDefault();
    const tierInput = document.getElementById('round-lock-tier');
    const targetInput = document.getElementById('round-lock-target-prob');
    const idInput = document.getElementById('round-lock-id');
    const passInput = document.getElementById('round-lock-pass');
    const errorEl = document.getElementById('round-lock-error');
    const submitBtn = document.getElementById('btn-round-lock-submit');

    const tier = (tierInput ? tierInput.value : 'easy').toLowerCase();
    const targetProb = targetInput ? targetInput.value : '';
    const adminId = idInput ? idInput.value.trim() : '';
    const password = passInput ? passInput.value.trim() : '';

    if (!adminId || !password) {
      if (errorEl) {
        errorEl.textContent = 'Please enter both Administrator ID and Password.';
        errorEl.style.display = 'block';
      }
      return;
    }

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Unlocking Round...';
    }

    try {
      const res = await fetch('/api/admin/toggle-tier-lock', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tier: tier,
          locked: false,
          admin_id: adminId,
          password: password
        })
      });

      const data = await res.json();
      if (data.success) {
        localStorage.setItem('cc_admin_id', adminId);
        this.closeRoundLockModal();
        this.showToast(data.message || `🔓 Category ${tier.toUpperCase()} unlocked for all participants!`, 'success');
        
        // Refresh catalog
        await this.loadProblems();

        // If user was trying to open a specific problem in this round, open it!
        if (targetProb) {
          this.openProblem(targetProb);
        }
      } else {
        const errMsg = data.error || 'Invalid Admin credentials. Unlock failed.';
        if (errorEl) {
          errorEl.textContent = errMsg;
          errorEl.style.display = 'block';
        }
        this.showToast(errMsg, 'error');
      }
    } catch (err) {
      const msg = 'Unlock request failed: ' + err.message;
      if (errorEl) {
        errorEl.textContent = msg;
        errorEl.style.display = 'block';
      }
      this.showToast(msg, 'error');
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = '🔓 Unlock Category / Round';
      }
    }
  },

  openSolutionModal() {
    if (!this.activeProblem) {
      this.showToast('Please select a problem first.', 'warning');
      return;
    }

    const modal = document.getElementById('modal-solution-lock');
    const idInput = document.getElementById('sol-lock-id');
    const passInput = document.getElementById('sol-lock-pass');
    const errorEl = document.getElementById('sol-lock-error');

    if (errorEl) errorEl.style.display = 'none';

    // Pre-populate admin ID if available from session/local storage
    const savedAdminId = (typeof Admin !== 'undefined' && Admin.getAdminId && Admin.getAdminId()) || localStorage.getItem('cc_admin_id') || '';
    if (idInput) {
      idInput.value = savedAdminId;
    }
    if (passInput) {
      passInput.value = '';
      passInput.type = 'password';
    }

    if (modal) {
      modal.style.display = 'flex';
      setTimeout(() => {
        if (idInput && !idInput.value.trim()) {
          idInput.focus();
        } else if (passInput) {
          passInput.focus();
        }
      }, 50);
    }
  },

  closeSolutionModal() {
    const modal = document.getElementById('modal-solution-lock');
    if (modal) modal.style.display = 'none';
  },

  toggleSolutionPassVisibility() {
    const passInput = document.getElementById('sol-lock-pass');
    if (!passInput) return;
    passInput.type = passInput.type === 'password' ? 'text' : 'password';
  },

  async submitSolutionUnlock(e) {
    if (e) e.preventDefault();
    if (!this.activeProblem) return;

    const idInput = document.getElementById('sol-lock-id');
    const passInput = document.getElementById('sol-lock-pass');
    const errorEl = document.getElementById('sol-lock-error');
    const submitBtn = document.getElementById('btn-sol-lock-submit');

    const adminId = idInput ? idInput.value.trim() : '';
    const password = passInput ? passInput.value.trim() : '';

    if (!adminId || !password) {
      if (errorEl) {
        errorEl.textContent = 'Please enter both Admin ID and Password.';
        errorEl.style.display = 'block';
      }
      return;
    }

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Verifying...';
    }

    try {
      const res = await fetch('/api/admin/get-solution', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          problem_id: this.activeProblem.id,
          language: this.currentLanguage,
          admin_id: adminId,
          password: password
        })
      });

      const data = await res.json();
      if (data.success && data.solution) {
        localStorage.setItem('cc_admin_id', adminId);
        if (data.token) {
          sessionStorage.setItem('cc_admin_token', data.token);
          sessionStorage.setItem('cc_admin_id', data.admin_id || adminId);
        }
        this.closeSolutionModal();
        this.editor.setValue(data.solution);
        const langDisplay = this.getLanguageDisplayName(this.currentLanguage);
        this.showToast(`✨ ${langDisplay} solution unlocked & inserted! (Admin: ${data.admin_id || adminId})`, 'success');
      } else {
        const errMsg = data.error || 'Invalid Admin ID or Password. Access denied.';
        if (errorEl) {
          errorEl.textContent = errMsg;
          errorEl.style.display = 'block';
        }
        this.showToast(errMsg, 'error');
      }
    } catch (err) {
      const msg = 'Verification request failed: ' + err.message;
      if (errorEl) {
        errorEl.textContent = msg;
        errorEl.style.display = 'block';
      }
      this.showToast(msg, 'error');
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = '🔓 Unlock & Insert';
      }
    }
  },

  getLanguageDisplayName(lang) {
    if (lang === 'python') return 'Python 3 (Normal)';
    if (lang === 'python_class') return 'Python 3 (Class)';
    if (lang === 'java') return 'Java';
    if (lang === 'c') return 'C';
    return (lang || 'Code').toUpperCase();
  },

  async fetchAndInsertSolution(token) {
    if (!this.activeProblem) return;
    try {
      const res = await fetch('/api/admin/get-solution', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          problem_id: this.activeProblem.id,
          language: this.currentLanguage,
          token: token
        })
      });

      const data = await res.json();
      if (data.success && data.solution) {
        this.editor.setValue(data.solution);
        const langDisplay = this.getLanguageDisplayName(this.currentLanguage);
        this.showToast(`🔓 ${langDisplay} solution inserted into editor!`, 'success');
      } else {
        sessionStorage.removeItem('cc_admin_token');
        this.openSolutionModal();
      }
    } catch (err) {
      this.openSolutionModal();
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
        document.getElementById('sample-tests-container').innerHTML = this.renderErrorBox({
          type: 'COMPILATION',
          title: 'Execution / Server Error',
          message: errorMsg,
          meta: this.currentLanguage.toUpperCase()
        });
        this.switchOutputTab('sample-tests', document.querySelector('.tabs-header .tab-btn'));
        this.showToast(errorMsg, 'error');
        return;
      }

      if (data.is_custom) {
        const r = data.result || {};
        const outBox = document.getElementById('custom-stdout');
        if (outBox) {
          const isErr = (r.status !== 'ACCEPTED' && r.status !== 'OK' && r.status !== 'DONE') || Boolean(r.stderr || r.error);
          const hasStdout = Boolean(r.stdout && r.stdout.trim().length > 0);
          
          let html = `
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.65rem;">
              <span style="font-weight:700; color:${isErr ? 'var(--accent-red)' : 'var(--accent-green)'};">
                ${isErr ? '❌ Verdict: ' + (r.status || 'ERROR') : '✓ Verdict: ACCEPTED'}
              </span>
              <span style="font-family:var(--font-mono); font-size:0.8rem; color:var(--text-muted);">${r.runtime ? r.runtime.toFixed(3) : '0.000'}s</span>
            </div>
          `;

          if (hasStdout) {
            html += `
              <div style="margin-bottom:0.65rem;">
                <div style="font-size:0.75rem; font-weight:700; color:var(--text-muted); text-transform:uppercase; margin-bottom:0.25rem;">Standard Output (stdout):</div>
                <pre class="sample-pre" style="color:#fff;">${this.escapeHtml(r.stdout)}</pre>
              </div>
            `;
          }

          if (r.stderr || r.error || r.status === 'COMPILATION_ERROR' || r.status === 'RUNTIME_ERROR' || r.status === 'TIME_LIMIT_EXCEEDED') {
            html += this.renderErrorBox({
              type: r.status === 'COMPILATION_ERROR' ? 'COMPILATION' : (r.status === 'TIME_LIMIT_EXCEEDED' ? 'TLE' : 'RUNTIME'),
              title: r.status === 'COMPILATION_ERROR' ? 'Compilation Error' : (r.status === 'TIME_LIMIT_EXCEEDED' ? 'Time Limit Exceeded' : 'Runtime Error / Stderr'),
              message: r.stderr || r.error || 'Execution failed.',
              meta: this.currentLanguage.toUpperCase(),
              warningStyle: r.status === 'TIME_LIMIT_EXCEEDED'
            });
          } else if (!hasStdout) {
            html += `<div style="color:var(--text-muted); font-size:0.85rem; font-style:italic;">(Program completed with no stdout output)</div>`;
          }

          outBox.innerHTML = html;
        }
        this.switchOutputTab('custom-input', document.querySelectorAll('.tabs-header .tab-btn')[1]);
        this.showToast(`Custom run completed (${r.status || 'DONE'})`, isErr ? 'warning' : 'info');
        return;
      }

      const r = data.result || {};
      let html = '';
      if (r.status === 'COMPILATION_ERROR') {
        html = this.renderErrorBox({
          type: 'COMPILATION',
          title: 'Compilation / Syntax Error',
          message: r.error_message || 'Compilation failed. Please verify syntax, imports, and method signatures.',
          meta: this.currentLanguage.toUpperCase()
        });
      } else {
        html = (r.results || []).map(t => {
          if (t.passed) {
            return `
              <div style="background:var(--bg-primary); padding:0.75rem 1rem; border-radius:6px; margin-bottom:0.65rem; border-left:4px solid var(--accent-green);">
                <div style="display:flex; justify-content:space-between; align-items:center; font-weight:700;">
                  <span style="color:var(--accent-green); display:flex; align-items:center; gap:0.4rem;">
                    <span>✓</span> Sample Test #${t.test_num}: ACCEPTED
                  </span>
                  <span style="font-family:var(--font-mono); font-size:0.8rem; color:var(--text-muted);">${typeof t.runtime === 'number' ? t.runtime.toFixed(3) : t.runtime}s</span>
                </div>
              </div>
            `;
          }

          // Test failed (Wrong Answer, Runtime Error, or TLE)
          const isTLE = t.status === 'TIME_LIMIT_EXCEEDED';
          const isRuntime = t.status === 'RUNTIME_ERROR' || Boolean(t.error || t.stderr);

          return `
            <div style="background:var(--bg-primary); padding:0.85rem 1rem; border-radius:6px; margin-bottom:0.85rem; border-left:4px solid ${isTLE ? 'var(--accent-amber)' : 'var(--accent-red)'};">
              <div style="display:flex; justify-content:space-between; align-items:center; font-weight:700; margin-bottom:0.5rem;">
                <span style="color:${isTLE ? 'var(--accent-amber)' : 'var(--accent-red)'}; display:flex; align-items:center; gap:0.4rem;">
                  <span>${isTLE ? '⏱️' : '❌'}</span> Sample Test #${t.test_num}: ${t.status}
                </span>
                <span style="font-family:var(--font-mono); font-size:0.8rem; color:var(--text-muted);">${typeof t.runtime === 'number' ? t.runtime.toFixed(3) : t.runtime}s</span>
              </div>

              ${isRuntime ? this.renderErrorBox({
                type: 'RUNTIME',
                title: `Test #${t.test_num} Runtime Exception`,
                message: t.stderr || t.error || t.actual || 'Runtime error occurred.',
                meta: this.currentLanguage.toUpperCase()
              }) : ''}

              ${isTLE ? this.renderErrorBox({
                type: 'TLE',
                title: `Test #${t.test_num} Time Limit Exceeded`,
                message: `Execution timed out (> 2.0s). Your program did not finish within the allowed runtime limit.`,
                warningStyle: true
              }) : ''}

              <div class="diff-view">
                <div class="diff-box expected">
                  <div style="font-size:0.75rem; font-weight:700; color:var(--accent-green); text-transform:uppercase; margin-bottom:0.25rem;">Expected Output:</div>
                  <pre style="margin:0; font-family:var(--font-mono); font-size:0.85rem; color:#fff; white-space:pre-wrap;">${this.escapeHtml(t.expected)}</pre>
                </div>
                <div class="diff-box actual">
                  <div style="font-size:0.75rem; font-weight:700; color:var(--accent-red); text-transform:uppercase; margin-bottom:0.25rem;">Your Output:</div>
                  <pre style="margin:0; font-family:var(--font-mono); font-size:0.85rem; color:#fca5a5; white-space:pre-wrap;">${this.escapeHtml(t.actual || '(No stdout produced)')}</pre>
                </div>
              </div>
            </div>
          `;
        }).join('');
      }

      document.getElementById('sample-tests-container').innerHTML = html;
      this.switchOutputTab('sample-tests', document.querySelector('.tabs-header .tab-btn'));
      this.showToast(r.all_passed ? 'All sample tests passed!' : 'Some sample tests failed.', r.all_passed ? 'success' : 'warning');
    } catch (e) {
      document.getElementById('sample-tests-container').innerHTML = this.renderErrorBox({
        type: 'RUNTIME',
        title: 'Run Error',
        message: e.message
      });
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
        verdictEl.innerHTML = this.renderErrorBox({
          type: 'COMPILATION',
          title: 'Submission Error',
          message: `${errorMsg}\n${data.error_message || ''}`,
          meta: this.currentLanguage.toUpperCase()
        });
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

      let errorBoxHtml = '';
      if (!isAccepted && (data.error_message || status === 'COMPILATION_ERROR' || status === 'RUNTIME_ERROR' || status === 'TIME_LIMIT_EXCEEDED' || status === 'WRONG_ANSWER')) {
        const errType = status === 'COMPILATION_ERROR' ? 'COMPILATION' : (status === 'TIME_LIMIT_EXCEEDED' ? 'TLE' : (status === 'RUNTIME_ERROR' ? 'RUNTIME' : 'WA'));
        const errTitle = status === 'COMPILATION_ERROR' ? 'Compilation / Syntax Error' : (status === 'TIME_LIMIT_EXCEEDED' ? 'Time Limit Exceeded' : (status === 'RUNTIME_ERROR' ? 'Runtime Error' : 'Test Failure Breakdown'));
        errorBoxHtml = this.renderErrorBox({
          type: errType,
          title: errTitle,
          message: data.error_message || `Solution failed on hidden test cases (${passedCount}/${totalCount} passed).`,
          meta: this.currentLanguage.toUpperCase(),
          warningStyle: status === 'TIME_LIMIT_EXCEEDED'
        });
      }

      verdictEl.innerHTML = `
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border-left:6px solid ${statusColor}; margin-bottom:0.75rem;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div style="font-size:1.25rem; font-weight:800; color:${statusColor};">${status}</div>
            <div style="font-family:var(--font-mono); font-size:0.85rem; color:var(--text-muted);">Runtime: ${runtime}s</div>
          </div>
          <div style="margin-top:0.5rem; color:var(--text-primary); font-size:0.9rem;">
            Hidden Test Cases Passed: <strong style="color:${isAccepted ? 'var(--accent-green)' : (passedCount > 0 ? 'var(--accent-amber)' : 'var(--accent-red)')};">${passedCount} / ${totalCount}</strong>
          </div>
          <div style="color:var(--accent-cyan); font-weight:700; margin-top:0.2rem;">Score Earned: +${scoreEarned} pts</div>
          ${data.already_solved ? `<div style="color:var(--accent-green); font-size:0.85rem; margin-top:0.35rem;">✓ Problem already solved previously. Points are recorded.</div>` : ''}
        </div>
        ${errorBoxHtml}
      `;

      this.switchOutputTab('submission-res', subTabBtn);

      if (isAccepted) {
        if (typeof data.participant_score === 'number' && this.participant) {
          this.participant.score = data.participant_score;
        } else if (scoreEarned > 0 && this.participant) {
          this.participant.score = (this.participant.score || 0) + scoreEarned;
        }
        if (this.participant) {
          localStorage.setItem('cc_participant', JSON.stringify(this.participant));
          this.updateUserBadge();
        }
        this.showToast(`Accepted! +${scoreEarned} pts added. Total Score: ${this.participant ? this.participant.score : scoreEarned} pts!`, 'success');
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
