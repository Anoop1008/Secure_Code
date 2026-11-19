/**
 * Analyzer API Handler & State Management
 */

let currentAnalysisResult = null;

async function analyzeCode() {
    const editor = document.getElementById('code-editor');
    const langSelect = document.getElementById('language-select');
    const filenameInput = document.getElementById('filename-input');
    const scanBtn = document.getElementById('scan-btn');

    if (!editor || !editor.value.trim()) {
        alert('Please enter or paste source code to scan.');
        return;
    }

    const code = editor.value;
    const language = langSelect ? langSelect.value : 'python';
    const filename = filenameInput && filenameInput.value.trim() ? filenameInput.value.trim() : 'main.py';

    if (scanBtn) {
        scanBtn.disabled = true;
        scanBtn.innerHTML = '⚡ Scanning Code AST...';
    }

    try {
        const response = await fetch('/api/analyze/snippet', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, language, filename })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Analysis request failed.');
        }

        const data = await response.json();
        currentAnalysisResult = data;
        window.currentAnalysisResult = data;
        updateUIWithResults(data);

    } catch (error) {
        console.error('Scan Error:', error);
        alert('Analysis Error: ' + error.message);
    } finally {
        if (scanBtn) {
            scanBtn.disabled = false;
            scanBtn.innerHTML = '🚀 Scan & Review Code';
        }
    }
}

async function analyzeDiffPatch() {
    const diffEditor = document.getElementById('diff-editor');
    const scanDiffBtn = document.getElementById('scan-diff-btn');

    if (!diffEditor || !diffEditor.value.trim()) {
        alert('Please paste a Git unified diff patch.');
        return;
    }

    if (scanDiffBtn) {
        scanDiffBtn.disabled = true;
        scanDiffBtn.innerHTML = '⚡ Parsing Diff...';
    }

    try {
        const response = await fetch('/api/analyze/diff', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ diff_content: diffEditor.value, filename: 'patch.diff' })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Diff analysis failed.');
        }

        const data = await response.json();
        currentAnalysisResult = data;
        window.currentAnalysisResult = data;
        updateUIWithResults(data);

        // Switch to overview tab
        switchTab('overview');

    } catch (error) {
        alert('Diff Scan Error: ' + error.message);
    } finally {
        if (scanDiffBtn) {
            scanDiffBtn.disabled = false;
            scanDiffBtn.innerHTML = '🔍 Analyze Git Diff';
        }
    }
}

function updateUIWithResults(data) {
    // 1. Update Executive Stats Cards
    const gradeEl = document.getElementById('stat-grade');
    if (gradeEl) {
        gradeEl.innerText = data.overall_grade;
        const isA = data.overall_grade.startsWith('A');
        const isB = data.overall_grade === 'B';
        const isC = data.overall_grade === 'C';
        const gradeColor = isA ? '#10b981' : (isB ? '#38bdf8' : (isC ? '#f59e0b' : '#ef4444'));
        gradeEl.style.color = gradeColor;

        const gradeCard = gradeEl.closest('.stat-card');
        if (gradeCard) {
            gradeCard.className = 'stat-card ' + (isA ? 'stat-emerald' : (isB ? 'stat-purple' : (isC ? 'stat-amber' : 'stat-rose')));
        }
    }

    const secScoreEl = document.getElementById('stat-sec-score');
    if (secScoreEl) {
        secScoreEl.innerText = `${data.security_score}/100`;
        secScoreEl.style.color = data.security_score >= 80 ? '#10b981' : (data.security_score >= 60 ? '#f59e0b' : '#ef4444');
    }

    document.getElementById('stat-qual-score').innerText = `${data.quality_score}/100`;
    document.getElementById('stat-vuln-count').innerText = data.vulnerabilities.length;
    document.getElementById('stat-maintainability').innerText = `${data.metrics.maintainability_index} (${data.metrics.maintainability_grade})`;
    document.getElementById('stat-complexity').innerText = `${data.metrics.cyclomatic_complexity} (${data.metrics.complexity_grade})`;
    document.getElementById('stat-tech-debt').innerText = `${data.metrics.technical_debt_hours} hrs`;

    // 2. Update AI Summary Box
    const aiSummaryEl = document.getElementById('ai-summary-text');
    if (aiSummaryEl) {
        aiSummaryEl.innerText = data.ai_summary;
    }

    const aiRecList = document.getElementById('ai-recommendations-list');
    if (aiRecList) {
        aiRecList.innerHTML = data.ai_recommendations.map(r => `<li style="margin-bottom: 6px;">${r}</li>`).join('');
    }

    // 3. Render Gauges & Charts
    renderScoreGauge('sec-gauge-container', data.security_score, data.security_score >= 80 ? '#10b981' : (data.security_score >= 60 ? '#f59e0b' : '#ef4444'));
    renderScoreGauge('qual-gauge-container', data.quality_score, data.quality_score >= 80 ? '#10b981' : '#3b82f6');
    renderSeverityBreakdown(data.vulnerability_counts);
    renderOwaspBreakdown(data.owasp_breakdown);

    // 4. Render Line-by-Line Code Viewer
    const editor = document.getElementById('code-editor');
    if (editor) {
        renderAnnotatedCode(editor.value, data.vulnerabilities);
    }

    // 5. Render Vulnerabilities Table
    renderVulnerabilitiesTable(data.vulnerabilities);
}

function escapeTableHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function renderVulnerabilitiesTable(vulnerabilities) {
    const tbody = document.getElementById('vuln-table-body');
    if (!tbody) return;

    if (vulnerabilities.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center; padding: 24px; color: var(--accent-emerald); font-weight: 600;">
                    🎉 Zero Security Vulnerabilities Detected!
                </td>
            </tr>
        `;
        return;
    }

    let html = '';
    vulnerabilities.forEach(v => {
        const badgeClass = `badge-${v.severity.toLowerCase()}`;
        html += `
            <tr>
                <td><strong>Line ${v.line}</strong></td>
                <td><span class="badge ${badgeClass}">${v.severity}</span></td>
                <td>
                    <strong>${escapeTableHtml(v.title)}</strong><br/>
                    <span style="font-size: 11px; color: var(--text-muted);">${v.cwe} • ${v.owasp}</span>
                </td>
                <td style="font-family: var(--font-code); font-size: 12px; color: var(--accent-cyan);">
                    <code>${escapeTableHtml(v.code_snippet)}</code>
                </td>
                <td style="font-size: 12.5px; color: var(--text-secondary);">${escapeTableHtml(v.recommendation)}</td>
                <td>
                    <button class="btn btn-secondary" style="padding: 4px 10px; font-size: 11px;" 
                            onclick="applyFixById('${v.id}')">
                        ✨ Fix
                    </button>
                </td>
            </tr>
        `;
    });

    tbody.innerHTML = html;
}

async function exportAuditReport(format) {
    if (!currentAnalysisResult) {
        alert('Please run a code scan before exporting an audit report.');
        return;
    }

    try {
        const response = await fetch('/api/report/export', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ analysis_result: currentAnalysisResult, format })
        });

        if (format === 'html') {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Security_Audit_Report_${currentAnalysisResult.scan_id}.html`;
            document.body.appendChild(a);
            a.click();
            a.remove();
        } else {
            const json = await response.json();
            const blob = new Blob([JSON.stringify(json, null, 2)], { type: 'application/json' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Security_Audit_${currentAnalysisResult.scan_id}.json`;
            document.body.appendChild(a);
            a.click();
            a.remove();
        }
    } catch (err) {
        alert('Report Export Failed: ' + err.message);
    }
}
