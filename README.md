# SecureCode AI: Secure Code Review and Software Quality Analysis Platform

**SecureCode AI** is an automated DevSecOps platform that unifies static application security testing (SAST), code quality metrics, and intelligent remediation into a single real-time developer workflow.

Developed as a Capstone Engineering Project at **Chandigarh University**, Department of Computer Science & Engineering.

---

## 🚀 Key Features

- **Sub-Second Static Code Analysis:** AST-based semantic analysis and regex pattern matching for fast, accurate vulnerability detection.
- **Vulnerability Coverage:** Detects SQL Injection (CWE-89), Command Injection (CWE-78), Dangerous Dynamic Code Execution (CWE-95), Hardcoded Secrets (CWE-798), Path Traversal (CWE-22), Insecure Deserialization (CWE-502), and Weak Cryptography (CWE-327) mapped to OWASP Top 10 standards.
- **Automated Remediation (Auto-Fix):** One-click contextual patching that safely refactors insecure code into compliant patterns.
- **Git Unified Diff / Pull Request Scanner:** Audits incoming git diff patches before code merges to block security regressions.
- **Objective Health Metrics:** Calculates McCabe Cyclomatic Complexity ($CC$), SEI Maintainability Index ($MI$), and Technical Debt remediation hours.
- **Executive Reporting:** Generates self-contained HTML audit reports and RFC-compliant JSON outputs for CI/CD pipelines.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.13, FastAPI, Uvicorn, Python `ast` module, Python `re` module, Pytest
- **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript, PrismJS, SVG circular gauges
- **Architecture:** Zero-cloud dependency, lightweight, privacy-focused local execution

---

## 🏁 Getting Started

### 1. Prerequisites
- Python 3.10+
- Git

### 2. Setup Virtual Environment & Install Dependencies
```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install fastapi uvicorn pytest
```

### 3. Run the Platform
```bash
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```
Open your browser and navigate to:
```
http://127.0.0.1:8000
```

### 4. Running Backend Tests
```bash
pytest backend/tests
```

---

## 👥 Project Contributors

- **Anoop Shukla** (23BCS10912)
- **Driti Khurana** (23BCS11997)
- **Sahil Mondal** (23BCS14298)
- **Kavya** (23BCS14821)

*Department of Computer Science & Engineering, Chandigarh University*
