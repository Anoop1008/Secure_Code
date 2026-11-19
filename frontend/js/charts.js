/**
 * Charts & Visualization Module for Secure Code Review Platform
 */

function renderScoreGauge(elementId, score, color) {
    const wrapper = document.getElementById(elementId);
    if (!wrapper) return;

    const radius = 55;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (score / 100) * circumference;

    wrapper.innerHTML = `
        <div class="gauge-wrapper">
            <svg class="gauge-svg" width="140" height="140">
                <circle class="gauge-bg" cx="70" cy="70" r="${radius}"></circle>
                <circle class="gauge-fill" cx="70" cy="70" r="${radius}" 
                        style="stroke: ${color}; stroke-dasharray: ${circumference}; stroke-dashoffset: ${offset};">
                </circle>
            </svg>
            <div class="gauge-text" style="color: ${color};">${Math.round(score)}</div>
        </div>
    `;
}

function renderSeverityBreakdown(counts) {
    const container = document.getElementById('severity-bar-container');
    if (!container) return;

    const total = Object.values(counts).reduce((a, b) => a + b, 0);

    if (total === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 20px; color: #10b981; font-weight: 500;">
                🎉 No Vulnerabilities Detected!
            </div>
        `;
        return;
    }

    const severities = [
        { label: 'Critical', key: 'CRITICAL', color: '#ef4444' },
        { label: 'High', key: 'HIGH', color: '#f97316' },
        { label: 'Medium', key: 'MEDIUM', color: '#eab308' },
        { label: 'Low', key: 'LOW', color: '#3b82f6' }
    ];

    let html = '';
    severities.forEach(s => {
        const count = counts[s.key] || 0;
        const pct = total > 0 ? (count / total) * 100 : 0;
        html += `
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 4px;">
                    <span style="color: ${s.color}; font-weight: 600;">${s.label}</span>
                    <span style="color: var(--text-muted);">${count} issues (${Math.round(pct)}%)</span>
                </div>
                <div style="background: rgba(255,255,255,0.06); height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="background: ${s.color}; width: ${pct}%; height: 100%; border-radius: 4px; transition: width 0.6s ease;"></div>
                </div>
            </div>
        `;
    });

    container.innerHTML = html;
}

function renderOwaspBreakdown(owaspMap) {
    const container = document.getElementById('owasp-container');
    if (!container) return;

    const entries = Object.entries(owaspMap);
    if (entries.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 20px; color: var(--text-muted); font-size: 13px;">
                No OWASP Top 10 categories triggered in current scan.
            </div>
        `;
        return;
    }

    let html = '<div style="display: flex; flex-wrap: wrap; gap: 10px;">';
    entries.forEach(([category, count]) => {
        html += `
            <div style="background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.25); color: var(--accent-cyan); padding: 8px 14px; border-radius: 8px; font-size: 13px;">
                <strong>${category}</strong>: ${count}
            </div>
        `;
    });
    html += '</div>';

    container.innerHTML = html;
}
