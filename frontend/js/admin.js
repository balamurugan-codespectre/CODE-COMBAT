/**
 * CODE COMBAT Pro - Admin Operations & Authentication Module
 */

const Admin = {
  token: '',
  adminId: 'admincse',

  getToken() {
    return this.token || '';
  },

  getAdminId() {
    return this.adminId || 'admincse';
  },

  isAuthenticated() {
    return Boolean(this.token);
  },

  lock() {
    this.token = '';
    this.adminId = 'admincse';
    sessionStorage.removeItem('cc_admin_token');
    sessionStorage.removeItem('cc_admin_id');
    localStorage.removeItem('cc_admin_token');
    localStorage.removeItem('cc_admin_id');

    const idInput = document.getElementById('admin-login-id');
    const passInput = document.getElementById('admin-login-pass');
    const authErrorEl = document.getElementById('admin-auth-error');
    if (idInput) idInput.value = '';
    if (passInput) passInput.value = '';
    if (authErrorEl) {
      authErrorEl.textContent = '';
      authErrorEl.style.display = 'none';
    }

    const gateEl = document.getElementById('admin-auth-gate');
    const portalEl = document.getElementById('admin-portal-content');
    if (gateEl) gateEl.style.display = 'block';
    if (portalEl) portalEl.style.display = 'none';
  },

  getAuthHeaders() {
    const token = this.getToken();
    const headers = { 'Content-Type': 'application/json' };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  },

  checkAuthUI() {
    const gateEl = document.getElementById('admin-auth-gate');
    const portalEl = document.getElementById('admin-portal-content');
    const displayIdEl = document.getElementById('admin-display-id');
    const authErrorEl = document.getElementById('admin-auth-error');

    if (authErrorEl) authErrorEl.style.display = 'none';

    if (this.isAuthenticated()) {
      if (gateEl) gateEl.style.display = 'none';
      if (portalEl) portalEl.style.display = 'flex';
      if (displayIdEl) displayIdEl.textContent = this.getAdminId();
      this.loadSets();
      this.checkHealth();
    } else {
      if (gateEl) gateEl.style.display = 'block';
      if (portalEl) portalEl.style.display = 'none';
      const idInput = document.getElementById('admin-login-id');
      if (idInput && App.currentView === 'admin') {
        setTimeout(() => idInput.focus(), 50);
      }
    }
  },

  async handleLogin(e) {
    if (e) e.preventDefault();
    const idInput = document.getElementById('admin-login-id');
    const passInput = document.getElementById('admin-login-pass');
    const errorEl = document.getElementById('admin-auth-error');

    const adminId = idInput ? idInput.value.trim() : '';
    const password = passInput ? passInput.value.trim() : '';

    if (!adminId || !password) {
      if (errorEl) {
        errorEl.textContent = 'Please enter both Administrator ID and Password.';
        errorEl.style.display = 'block';
      }
      return;
    }

    try {
      const res = await fetch('/api/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          admin_id: adminId,
          password: password
        })
      });

      const data = await res.json();
      if (data.authenticated && data.token) {
        this.token = data.token;
        this.adminId = data.admin_id || adminId;

        if (idInput) idInput.value = '';
        if (passInput) passInput.value = '';
        if (errorEl) errorEl.style.display = 'none';

        this.checkAuthUI();
        App.showToast(`Admin Portal Unlocked. Welcome, ${data.admin_id || adminId}!`, 'success');
      } else {
        const errMsg = data.error || 'Invalid Administrator ID or Password.';
        if (errorEl) {
          errorEl.textContent = errMsg;
          errorEl.style.display = 'block';
        }
        App.showToast(errMsg, 'error');
      }
    } catch (err) {
      const msg = 'Login request failed: ' + err.message;
      if (errorEl) {
        errorEl.textContent = msg;
        errorEl.style.display = 'block';
      }
      App.showToast(msg, 'error');
    }
  },

  logout() {
    this.lock();
    this.checkAuthUI();
    App.showToast('Admin Portal locked successfully.', 'info');
  },

  async exportAllJSON() {
    try {
      const res = await fetch('/api/admin/export', {
        headers: this.getAuthHeaders()
      });
      const data = await res.json();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `code_combat_backup_${new Date().toISOString().slice(0,10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
      App.showToast('JSON database export downloaded.', 'success');
    } catch (e) {
      App.showToast('Export failed: ' + e.message, 'error');
    }
  },

  async loadSets() {
    try {
      const res = await fetch('/api/admin/sets', {
        headers: this.getAuthHeaders()
      });
      if (!res.ok) return;
      const data = await res.json();
      const sel = document.getElementById('admin-set-select');
      if (sel && data.sets) {
        sel.innerHTML = data.sets.map(s => `
          <option value="${s.id}" ${s.id === data.active_set ? 'selected' : ''}>${s.name}</option>
        `).join('');
      }
    } catch (e) {
      console.warn('Error loading problem sets:', e);
    }
  },

  async switchProblemSet() {
    const sel = document.getElementById('admin-set-select');
    const resetCheck = document.getElementById('admin-set-reset-check');
    if (!sel) return;

    const setId = sel.value;
    const resetData = resetCheck ? resetCheck.checked : true;

    try {
      const res = await fetch('/api/admin/switch-set', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          token: this.getToken(),
          set_id: setId,
          reset_data: resetData
        })
      });

      const data = await res.json();
      if (data.success) {
        App.showToast(data.message || `Switched to ${setId.toUpperCase()}!`, 'success');

        if (resetData) {
          App.participant = null;
          localStorage.removeItem('cc_participant');
          const badge = document.getElementById('user-badge');
          if (badge) badge.style.display = 'none';
        }

        App.loadProblems();
        App.loadLeaderboard();
        this.checkHealth();
      } else {
        if (res.status === 401) {
          this.logout();
          App.showToast('Admin session expired. Please log in again.', 'warning');
        } else {
          App.showToast('Switch set failed: ' + (data.error || 'Unknown error'), 'error');
        }
      }
    } catch (e) {
      App.showToast('Network error switching set: ' + e.message, 'error');
    }
  },

  async handleChangeCredentials(e) {
    if (e) e.preventDefault();
    const currPass = document.getElementById('admin-curr-pass')?.value || '';
    const newId = document.getElementById('admin-new-id')?.value.trim() || '';
    const newPass = document.getElementById('admin-new-pass')?.value || '';
    const confirmPass = document.getElementById('admin-confirm-pass')?.value || '';

    if (!currPass) {
      App.showToast('Please enter your current admin password.', 'warning');
      return;
    }
    if (newPass && newPass.length < 4) {
      App.showToast('New password must be at least 4 characters long.', 'warning');
      return;
    }
    if (newPass && newPass !== confirmPass) {
      App.showToast('New passwords do not match. Please re-enter.', 'error');
      return;
    }

    try {
      const res = await fetch('/api/admin/change-password', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          token: this.getToken(),
          old_password: currPass,
          new_admin_id: newId || undefined,
          new_password: newPass || undefined
        })
      });

      const data = await res.json();
      if (data.success) {
        if (newId) {
          this.adminId = newId;
          const displayIdEl = document.getElementById('admin-display-id');
          if (displayIdEl) displayIdEl.textContent = newId;
        }
        App.showToast('Admin credentials updated successfully!', 'success');
        if (document.getElementById('admin-curr-pass')) document.getElementById('admin-curr-pass').value = '';
        if (document.getElementById('admin-new-id')) document.getElementById('admin-new-id').value = '';
        if (document.getElementById('admin-new-pass')) document.getElementById('admin-new-pass').value = '';
        if (document.getElementById('admin-confirm-pass')) document.getElementById('admin-confirm-pass').value = '';
      } else {
        App.showToast('Update failed: ' + (data.error || 'Incorrect current credentials'), 'error');
      }
    } catch (err) {
      App.showToast('Network error: ' + err.message, 'error');
    }
  },

  async resetCompetition() {
    if (!confirm('⚠️ WARNING: This will permanently wipe ALL participants, scores, submissions, and leaderboard rankings across the competition!\n\nAre you sure you want to proceed?')) {
      return;
    }

    try {
      const res = await fetch('/api/admin/reset', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ token: this.getToken() })
      });
      const data = await res.json();
      if (data.success) {
        App.showToast('Competition completely reset. All points & submissions wiped to 0.', 'success');
        
        // Clear client participant session and scores
        App.participant = null;
        localStorage.removeItem('cc_participant');
        const badge = document.getElementById('user-badge');
        if (badge) badge.style.display = 'none';

        // Refresh views
        App.loadLeaderboard();
        App.loadProblems();
        this.checkHealth();
      } else {
        if (res.status === 401) {
          this.logout();
          App.showToast('Admin session expired. Please log in again.', 'warning');
        } else {
          App.showToast('Reset failed: ' + (data.error || 'Unauthorized'), 'error');
        }
      }
    } catch (e) {
      App.showToast('Reset request error: ' + e.message, 'error');
    }
  },

  async checkHealth() {
    const el = document.getElementById('admin-health-status');
    if (!el) return;
    try {
      const res = await fetch('/api/health');
      const health = await res.json();
      el.innerHTML = `
        <div>Status: <strong>${health.status.toUpperCase()}</strong></div>
        <div>Uptime: ${health.uptime_seconds}s</div>
        <div>Active Problem Set: <strong>${health.active_problem_set ? health.active_problem_set.toUpperCase() : 'SET 1'}</strong></div>
        <div>Python: OK | C: ${health.compilers.c ? health.compilers.c_compiler : 'Not Found'} | Java: ${health.compilers.java ? health.compilers.java_compiler : 'Not Found'}</div>
        <div>Loaded Problems in Active Set: <strong>${health.total_problems}</strong></div>
      `;
    } catch (e) {
      el.innerHTML = `<span style="color:var(--accent-red)">Health check failed: ${e.message}</span>`;
    }
  }
};

window.Admin = Admin;


