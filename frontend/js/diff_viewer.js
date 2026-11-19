/**
 * Interactive Line-by-Line Code Viewer & Inline AI Fix Drawer Component
 */

function renderAnnotatedCode(code, vulnerabilities) {
    const container = document.getElementById('annotated-code-view');
    if (!container) return;

    const lines = code.split('\n');

    // Index vulnerabilities by line number
    const vulnByLine = {};
    vulnerabilities.forEach(v => {
        if (!vulnByLine[v.line]) vulnByLine[v.line] = [];
        vulnByLine[v.line].push(v);
    });

    let html = '<div class="annotated-code-container">';

    lines.forEach((lineText, index) => {
        const lineNum = index + 1;
        const lineVulns = vulnByLine[lineNum] || [];

        let rowClass = 'code-line-row';
        if (lineVulns.length > 0) {
            const topSev = lineVulns[0].severity.toLowerCase();
            rowClass += ` has-vuln-${topSev}`;
        }

        const escapeHtml = str => {
            if (!str) return '';
            return String(str)
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        };

        html += `
            <div class="${rowClass}" id="line-row-${lineNum}">
                <div class="line-number">${lineNum}</div>
                <div class="line-content">${escapeHtml(lineText) || ' '}</div>
        `;

        if (lineVulns.length > 0) {
            lineVulns.forEach((v, vIdx) => {
                html += `
                    <span class="inline-vuln-badge" onclick="toggleFixDrawer(${lineNum}, ${vIdx})">
                        ⚠️ ${v.severity}: ${v.cwe} ▾
                    </span>
                `;
            });
        }

        html += `</div>`;

        // Render Inline AI Fix Drawer if present
        if (lineVulns.length > 0) {
            lineVulns.forEach((v, vIdx) => {
                html += `
                    <div class="inline-fix-drawer" id="fix-drawer-${lineNum}-${vIdx}" style="display: none;">
                        <div class="fix-header">
                            <span>🤖 AI Remediation: ${escapeHtml(v.title)}</span>
                            <span class="badge badge-${v.severity.toLowerCase()}">${v.severity}</span>
                        </div>
                        <p style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 8px;">
                            ${escapeHtml(v.description)}
                        </p>
                        <div style="font-size: 12px; color: var(--accent-cyan); margin-bottom: 6px;">
                            <strong>Recommendation:</strong> ${escapeHtml(v.recommendation)}
                        </div>
                        <div class="fix-snippet">${escapeHtml(v.suggested_fix)}</div>
                        <div style="margin-top: 10px; text-align: right;">
                            <button class="btn btn-secondary" style="padding: 4px 12px; font-size: 12px;" 
                                    onclick="applyFixById('${v.id}')">
                                ✨ Apply AI Fix to Editor
                            </button>
                        </div>
                    </div>
                `;
            });
        }
    });

    html += '</div>';
    container.innerHTML = html;
}

function toggleFixDrawer(lineNum, vIdx) {
    const drawer = document.getElementById(`fix-drawer-${lineNum}-${vIdx}`);
    if (drawer) {
        drawer.style.display = drawer.style.display === 'none' ? 'block' : 'none';
    }
}

function applyFixById(vulnId) {
    const res = window.currentAnalysisResult || currentAnalysisResult;
    if (!res || !res.vulnerabilities) {
        alert('Please run a code scan first.');
        return;
    }

    const vuln = res.vulnerabilities.find(v => v.id === vulnId);
    if (!vuln) {
        alert('Vulnerability fix metadata not found.');
        return;
    }

    applyFix(vuln);
}

function applyFix(vuln) {
    const editor = document.getElementById('code-editor');
    if (!editor) return;

    const originalSnippet = vuln.code_snippet ? vuln.code_snippet.trim() : '';
    const fixSnippet = vuln.suggested_fix || '';
    const targetLine = vuln.line;

    let lines = editor.value.split('\n');

    // 1. Check exact line number match first
    if (targetLine >= 1 && targetLine <= lines.length) {
        const lineContent = lines[targetLine - 1];
        if (!originalSnippet || lineContent.includes(originalSnippet) || originalSnippet.includes(lineContent.trim())) {
            const indentMatch = lineContent.match(/^(\s*)/);
            const indent = indentMatch ? indentMatch[1] : '';
            const indentedFix = fixSnippet.split('\n').map((l, i) => i === 0 ? indent + l.trimStart() : indent + l).join('\n');
            lines[targetLine - 1] = indentedFix;
            editor.value = lines.join('\n');
            alert(`✨ AI Fix applied successfully to Line ${targetLine}!\n\nRe-scanning code...`);
            if (typeof analyzeCode === 'function') analyzeCode();
            return;
        }
    }

    // 2. Try finding line containing originalSnippet
    if (originalSnippet) {
        const foundIdx = lines.findIndex(l => l.includes(originalSnippet) || (originalSnippet.length > 5 && l.trim().includes(originalSnippet)));
        if (foundIdx !== -1) {
            const lineContent = lines[foundIdx];
            const indentMatch = lineContent.match(/^(\s*)/);
            const indent = indentMatch ? indentMatch[1] : '';
            const indentedFix = fixSnippet.split('\n').map((l, i) => i === 0 ? indent + l.trimStart() : indent + l).join('\n');
            lines[foundIdx] = indentedFix;
            editor.value = lines.join('\n');
            alert(`✨ AI Fix applied successfully to Line ${foundIdx + 1}!\n\nRe-scanning code...`);
            if (typeof analyzeCode === 'function') analyzeCode();
            return;
        }
    }

    // 3. Fallback: direct string replace
    if (originalSnippet && editor.value.includes(originalSnippet)) {
        editor.value = editor.value.replace(originalSnippet, fixSnippet);
        alert('✨ AI Fix applied successfully!\n\nRe-scanning code...');
        if (typeof analyzeCode === 'function') analyzeCode();
        return;
    }

    alert('Could not auto-match the code snippet in editor. Please paste fix manually:\n\n' + fixSnippet);
}

function applyAllFixes() {
    const res = window.currentAnalysisResult || currentAnalysisResult;
    if (!res || !res.vulnerabilities || res.vulnerabilities.length === 0) {
        alert('🎉 No vulnerabilities to fix! Code is clean.');
        return;
    }

    const editor = document.getElementById('code-editor');
    if (!editor || !editor.value.trim()) return;

    let lines = editor.value.split('\n');

    // Sort descending by line number to avoid line-shift offsets during multi-line insertions
    const sortedVulns = [...res.vulnerabilities].sort((a, b) => b.line - a.line);
    const seenLines = new Set();
    const uniqueSorted = [];
    sortedVulns.forEach(v => {
        if (!seenLines.has(v.line)) {
            seenLines.add(v.line);
            uniqueSorted.push(v);
        }
    });

    let fixedCount = 0;
    uniqueSorted.forEach(v => {
        const targetLine = v.line;
        if (targetLine >= 1 && targetLine <= lines.length) {
            const lineContent = lines[targetLine - 1];
            const indentMatch = lineContent.match(/^(\s*)/);
            const indent = indentMatch ? indentMatch[1] : '';
            const indentedFix = (v.suggested_fix || '')
                .split('\n')
                .map((l, i) => i === 0 ? indent + l.trimStart() : indent + l)
                .join('\n');
            lines[targetLine - 1] = indentedFix;
            fixedCount++;
        }
    });

    editor.value = lines.join('\n');
    alert(`✨ Auto-patched ${fixedCount} vulnerabilities across the codebase!\n\nRe-analyzing now...`);
    if (typeof analyzeCode === 'function') analyzeCode();
}

function applyFixSnippet(originalSnippet, fixSnippet) {
    applyFix({ code_snippet: originalSnippet, suggested_fix: fixSnippet, line: 0 });
}
