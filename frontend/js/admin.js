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

  async resetCompetition() {
    const pass = prompt('Enter Admin Password to wipe all scores and submissions:');
    if (!pass) return;

    try {
      const res = await fetch('/api/admin/reset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: pass })
      });
      const data = await res.json();
      if (data.success) {
        App.showToast('Competition reset successfully.', 'success');
        App.loadLeaderboard();
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
        <div>Python: OK | C: ${health.compilers.c ? health.compilers.c_compiler : 'Not Found'} | Java: ${health.compilers.java ? health.compilers.java_compiler : 'Not Found'}</div>
        <div>Loaded Problems: ${health.total_problems}</div>
      `;
    } catch (e) {
      el.innerHTML = `<span style="color:var(--accent-red)">Health check failed: ${e.message}</span>`;
    }
  }
};

window.Admin = Admin;
