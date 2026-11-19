/**
 * Main Application Router & Sample Code Loader
 */

const SAMPLE_CODES = {
    vulnerable_python: `import os
import subprocess
import pickle
import hashlib

API_KEY = "sk_live_99887766554433221100"

def process_user_request(user_id, raw_query, command_str, data_blob):
    # Vulnerability 1: SQL Injection via f-string
    query = f"SELECT * FROM users WHERE id = '{user_id}' AND raw = '{raw_query}'"
    print("Executing query:", query)
    
    # Vulnerability 2: Dangerous Dynamic Code Execution
    if "calc" in raw_query:
        result = eval(raw_query)
    
    # Vulnerability 3: Command Injection via shell=True
    subprocess.run(f"ping -c 1 {command_str}", shell=True)
    
    # Vulnerability 4: Insecure Deserialization
    untrusted_obj = pickle.loads(data_blob)
    
    # Vulnerability 5: Weak Hashing Algorithm
    pass_hash = hashlib.md5(user_id.encode()).hexdigest()
    
    # High Cyclomatic Complexity Loop
    for i in range(10):
        if i > 2:
            if i % 2 == 0:
                for j in range(5):
                    if j == 3:
                        pass
    
    return pass_hash
`,
    clean_python: `import os
import subprocess
import hashlib
import ast
from typing import Dict, Any

# Secure credential extraction
API_KEY = os.getenv("API_KEY", "")

def process_user_request(user_id: str, raw_query: str, command_str: str) -> str:
    """
    Refactored secure request handler utilizing parameterized bindings
    and secure hashing algorithms.
    """
    # Parameterized SQL query placeholder
    query_sql = "SELECT * FROM users WHERE id = %s AND status = %s"
    query_params = (user_id, "active")
    
    # Safe literal evaluation
    parsed_val = None
    if raw_query.isdigit():
        parsed_val = int(raw_query)
        
    # Safe subprocess array execution without shell=True
    subprocess.run(["ping", "-c", "1", command_str], check=True)
    
    # Secure Cryptographic Hashing with SHA-256
    pass_hash = hashlib.sha256(user_id.encode()).hexdigest()
    return pass_hash
`,
    vulnerable_js: `const express = require('express');
const app = express();

const JWT_SECRET = "super_secret_jwt_key_12345";

app.get('/search', (req, res) => {
    const userQuery = req.query.q;
    // XSS Hazard via direct innerHTML / document.write pattern
    const htmlOutput = "<div>Search Result: " + userQuery + "</div>";
    document.write(htmlOutput);
    
    // Dynamic Code Execution
    eval(userQuery);
    
    res.send(htmlOutput);
});
`
};

document.addEventListener('DOMContentLoaded', () => {
    // Set up tab switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });

    const editor = document.getElementById('code-editor');
    const savedCode = sessionStorage.getItem('saved_code_editor');
    if (savedCode && editor) {
        editor.value = savedCode;
    } else {
        // Auto-load vulnerable python sample on initial clean launch
        loadSampleCode('vulnerable_python');
    }

    if (editor) {
        editor.addEventListener('input', () => {
            sessionStorage.setItem('saved_code_editor', editor.value);
        });
    }

    // Trigger initial scan
    setTimeout(() => {
        analyzeCode();
    }, 400);
});

function switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-tab') === tabId);
    });

    document.querySelectorAll('.tab-panel').forEach(panel => {
        panel.classList.toggle('active', panel.id === `tab-${tabId}`);
    });
}

function loadSampleCode(type) {
    const editor = document.getElementById('code-editor');
    const langSelect = document.getElementById('language-select');
    const filenameInput = document.getElementById('filename-input');

    if (!editor) return;

    if (type === 'vulnerable_python') {
        editor.value = SAMPLE_CODES.vulnerable_python;
        if (langSelect) langSelect.value = 'python';
        if (filenameInput) filenameInput.value = 'vulnerable_service.py';
    } else if (type === 'clean_python') {
        editor.value = SAMPLE_CODES.clean_python;
        if (langSelect) langSelect.value = 'python';
        if (filenameInput) filenameInput.value = 'clean_service.py';
    } else if (type === 'vulnerable_js') {
        editor.value = SAMPLE_CODES.vulnerable_js;
        if (langSelect) langSelect.value = 'javascript';
        if (filenameInput) filenameInput.value = 'server.js';
    }
    sessionStorage.setItem('saved_code_editor', editor.value);
}
