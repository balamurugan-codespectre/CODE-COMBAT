/**
 * CODE COMBAT Pro - Admin Operations Module
 */

const Admin = {
  async exportAllJSON() {
    try {
      const res = await fetch('/api/admin/export');
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
      const res = await fetch('/api/admin/sets');
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
    const passInput = document.getElementById('admin-set-pass');
    const resetCheck = document.getElementById('admin-set-reset-check');
    if (!sel) return;

    const setId = sel.value;
    let password = passInput ? passInput.value.trim() : '';

    if (!password) {
      password = prompt('Enter Admin Password to switch problem set:');
      if (!password) return;
    }

    const resetData = resetCheck ? resetCheck.checked : true;

    try {
      const res = await fetch('/api/admin/switch-set', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          password: password,
          set_id: setId,
          reset_data: resetData
        })
      });
      const data = await res.json();
      if (data.success) {
        App.showToast(data.message || `Switched to ${setId.toUpperCase()}!`, 'success');
        if (passInput) passInput.value = '';

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
        App.showToast('Switch set failed: ' + (data.error || 'Invalid password'), 'error');
      }
    } catch (e) {
      App.showToast('Network error switching set: ' + e.message, 'error');
    }
  },

  async handleChangePassword(e) {
    if (e) e.preventDefault();
    const currPass = document.getElementById('admin-curr-pass')?.value || '';
    const newPass = document.getElementById('admin-new-pass')?.value || '';
    const confirmPass = document.getElementById('admin-confirm-pass')?.value || '';

    if (!currPass) {
      App.showToast('Please enter your current admin password.', 'warning');
      return;
    }
    if (!newPass || newPass.length < 4) {
      App.showToast('New password must be at least 4 characters long.', 'warning');
      return;
    }
    if (newPass !== confirmPass) {
      App.showToast('New passwords do not match. Please re-enter.', 'error');
      return;
    }

    try {
      const res = await fetch('/api/admin/change-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          old_password: currPass,
          new_password: newPass
        })
      });
      const data = await res.json();
      if (data.success) {
        App.showToast('Admin password updated successfully!', 'success');
        document.getElementById('admin-curr-pass').value = '';
        document.getElementById('admin-new-pass').value = '';
        document.getElementById('admin-confirm-pass').value = '';
      } else {
        App.showToast('Password change failed: ' + (data.error || 'Incorrect current password'), 'error');
      }
    } catch (err) {
      App.showToast('Network error: ' + err.message, 'error');
    }
  },

  async resetCompetition() {
    const pass = prompt('Enter Admin Password to wipe all scores, points, and submissions:');
    if (!pass) return;

    try {
      const res = await fetch('/api/admin/reset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: pass })
      });
      const data = await res.json();
      if (data.success) {
        App.showToast('Competition completely reset. All points and submissions wiped to 0.', 'success');
        // Clear client participant session and scores
        App.participant = null;
        localStorage.removeItem('cc_participant');
        const badge = document.getElementById('user-badge');
        if (badge) badge.style.display = 'none';

        // Refresh views
        App.loadLeaderboard();
        App.loadProblems();
        if (typeof Admin.checkHealth === 'function') Admin.checkHealth();
      } else {
        App.showToast('Reset failed: ' + (data.error || 'Invalid password'), 'error');
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

