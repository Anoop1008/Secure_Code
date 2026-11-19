# SECURECODE AI: TEAM EVALUATION & VIVA PREPARATION GUIDE
**Department of Computer Science and Engineering | Chandigarh University**  
**Project:** Secure Code Review and Software Quality Analysis Platform  
**Target Audience:** Anoop Shukla, Driti Khurana, Sahil Mondal, Kavya  
**Date of Evaluation:** Final Capstone Viva  

---

## TABLE OF CONTENTS
1. [30-Second Elevator Pitch & Project Vision](#1-30-second-elevator-pitch--project-vision)
2. [The Core Problem & Why Existing Tools Fail](#2-the-core-problem--why-existing-tools-fail)
3. [System Architecture & How It Works Under the Hood](#3-system-architecture--how-it-works-under-the-hood)
4. [Platform Feature Walkthrough (Tab-by-Tab Live Demo Guide)](#4-platform-feature-walkthrough-tab-by-tab-live-demo-guide)
5. [The Vulnerabilities We Detect (CWE & OWASP Mappings)](#5-the-vulnerabilities-we-detect-cwe--owasp-mappings)
6. [Mathematical Formularies & Scoring Models (Examiner Favorites)](#6-mathematical-formularies--scoring-models-examiner-favorites)
7. [Step-by-Step Live Demo Execution Script](#7-step-by-step-live-demo-execution-script)
8. [Top 20 Viva Questions & Bulletproof Model Answers](#8-top-20-viva-questions--bulletproof-model-answers)
9. [Team Speaking Role Allocations](#9-team-speaking-role-allocations)

---

## 1. 30-SECOND ELEVATOR PITCH & PROJECT VISION

> **If an examiner says: "Introduce your project in two sentences":**  
> *"Our project, **SecureCode AI**, is an automated DevSecOps platform that unifies static application security testing (SAST), code quality metrics, and intelligent remediation into a single real-time developer workflow. Instead of waiting for slow CI/CD scans or post-deployment penetration tests, developers get sub-second security annotations, Git pull-request diff auditing, and one-click auto-fixes directly as they write code."*

### Key Keywords to Emphasize:
- **Shift-Left Security:** Catching security vulnerabilities early during authoring, not late in production.
- **Hybrid Detection Engine:** Combining fast Abstract Syntax Tree (AST) semantic parsing with high-precision Regular Expression signature matching.
- **Actionable Remediation:** Not just identifying problems, but generating automated, context-aware patches and audit reports.

---

## 2. THE CORE PROBLEM & WHY EXISTING TOOLS FAIL

### The Industry Problem
- Over **80% of enterprise security breaches** stem from application-layer vulnerabilities (SQL injection, hardcoded secrets, unsafe shell commands) introduced accidentally during rapid development cycles.
- Fixing a vulnerability discovered in **production costs up to 30x to 100x more** (NIST study) than fixing it during coding.

### Why Existing Solutions Fall Short (The Gap We Fill)
1. **SonarQube / Veracode:**
   - *Limitation:* Heavyweight, resource-intensive, often decoupled from the developer's immediate editing interface. Takes minutes to scan large codebases.
2. **Snyk / GitHub Dependabot:**
   - *Limitation:* Excellent for third-party open-source dependencies (SCA), but weaker on custom proprietary first-party source code logic and dynamic string interpolations.
3. **Bandit / Flake8:**
   - *Limitation:* Standalone command-line tools that generate raw terminal dumps without executive health grades, technical debt estimation, or inline interactive auto-fixing drawers.

### Our Solution
- **Zero-Setup Lightweight Architecture:** Sub-second response times (<180 ms for typical code modules).
- **Dual-Pane Interactive Editor:** Code on the left, line-by-line security badges on the right.
- **Git Unified Diff Scanning:** Analyze Git patches and Pull Request diffs directly before merging.
- **Quantitative Metrics:** Cyclomatic Complexity ($CC$), SEI Maintainability Index ($MI$), and Technical Debt remediation hours.

---

## 3. SYSTEM ARCHITECTURE & HOW IT WORKS UNDER THE HOOD

```
+-------------------------------------------------------------------------------+
|                           FRONTEND CLIENT (SPA)                               |
|  Tailwind CSS UI | PrismJS Syntax Highlighting | Circular SVG Metric Gauges    |
|  Dual-Pane Code Annotator | Git Diff Scanner | Audit Exporter                 |
+-------------------------------------------------------------------------------+
                                      |
                     REST API (HTTP JSON Payloads)
                                      v
+-------------------------------------------------------------------------------+
|                      BACKEND ENGINE (FastAPI / Uvicorn)                       |
|                                                                               |
|  [Route 1: /api/analyze]       [Route 2: /api/fix-all]   [Route 3: /api/diff] |
+-------------------------------------------------------------------------------+
           |                                   |                    |
           v                                   v                    v
+-----------------------+           +------------------+   +-------------------+
|  HYBRID AST & REGEX   |           |  REMEDIATION     |   | GIT UNIFIED DIFF  |
|  ANALYZER CORE        |           |  ORCHESTRATOR    |   | PARSER            |
| - Python `ast` Module |           | - Context-Aware  |   | - Unified Diff    |
| - Precompiled RegEx   |           |   Transformations|     Chunk Regex       |
| - AST Node Visitors   |           | - AST Node Sub   |   | - Line Mapping    |
+-----------------------+           +------------------+   +-------------------+
           |                                   |                    |
           +-----------------+-----------------+--------------------+
                             |
                             v
+-------------------------------------------------------------------------------+
|                     METRIC COMPUTATION & SCORING PIPELINE                     |
|  * McCabe Cyclomatic Complexity ($CC = E - V + 2P$)                           |
|  * SEI Maintainability Index ($MI = 171 - 5.2\ln(V) - 0.23CC - 16.2\ln(L)...$) |
|  * Vulnerability Penalty Scoring ($100 - \sum w_i \times N_i$)                |
|  * Technical Debt Estimation ($TD = \sum Hours$)                              |
+-------------------------------------------------------------------------------+
```

### Core Technologies Used:
1. **FastAPI & Uvicorn (Backend):** Asynchronous Python web framework delivering high-throughput, low-latency API responses.
2. **Python `ast` (Abstract Syntax Tree) Module:** Parses source code into syntax trees to inspect function calls, assignments, and arguments semantically without executing untrusted code.
3. **Regular Expressions (`re`):** Pre-compiled pattern matchers for detecting hardcoded API credentials, JWT keys, and dangerous subprocess shell invocations.
4. **Tailwind CSS & Vanilla JS (Frontend):** Modern, reactive user interface with zero heavy bundle overhead.

---

## 4. PLATFORM FEATURE WALKTHROUGH (TAB-BY-TAB LIVE DEMO GUIDE)

Our application has **5 core operational tabs**. Every teammate should know what each tab does:

### Tab 1: Executive Dashboard
- **What it shows:** High-level summary of code health designed for both developers and engineering leaders.
- **Key Metrics Displayed:**
  - **Security Health Grade:** Letter grade from **F** (critical vulnerabilities detected) to **A+** (clean, secure code).
  - **Security Score (0–100):** Deductive penalty model based on vulnerability severity.
  - **Quality Score (0–100):** Maintainability and structural clarity score.
  - **Vulnerabilities Detected:** Total count of active security issues.
  - **Maintainability Index:** SEI standard (e.g., 76.67 'B' or 75.13 'B').
  - **Cyclomatic Complexity:** Number of independent execution pathways (e.g., 5 'A').
  - **Estimated Technical Debt:** Remediation effort measured in engineering hours (e.g., 10.5 hrs $\to$ 1.6 hrs).
  - **Visual Gauges:** Two circular SVG gauges (Red/Green for Security, Blue for Quality).

### Tab 2: Code Scanner & Annotator
- **What it shows:** The developer's direct workspace.
- **Left Pane:** Multi-line code editor with quick presets (`Vulnerable Python`, `Clean Python`, `Node.js Express`).
- **Right Pane:** Real-time annotated code drawer highlighting exact vulnerable lines with color-coded severity badges (`CRITICAL`, `HIGH`, `MEDIUM`).
- **One-Click Auto-Fix Button:** Automatically runs remediation rules and replaces insecure code with secure equivalents in real time.

### Tab 3: Git Diff Analyzer
- **What it shows:** Pull Request and commit auditor.
- **How it works:** Developers or CI bots paste standard Git unified diff patches (`git diff`).
- **Value:** Analyzes *only incoming changes*, flagging if a developer is introducing a security regression before merging into `main`.

### Tab 4: Vulnerabilities & OWASP
- **What it shows:** An itemized, sortable audit table of all detected weaknesses.
- **Columns:**
  - `Line Number`
  - `Severity Badge` (Critical, High, Medium, Low)
  - `Title & Security Standards` (CWE identifier + OWASP Top 10 category)
  - `Vulnerable Snippet` (The exact line of flawed code)
  - `Remediation Recommendation` (Concrete security engineering advice)
  - `Action Button` (Individual inline fix button)

### Tab 5: Audit Report Exporter
- **What it shows:** Compliance and reporting center.
- **Deliverables:**
  - **Download HTML Audit Report:** Fully styled, standalone, client-ready executive security report.
  - **Export Raw JSON Audit Data:** Machine-readable payload for CI/CD integration and automated quality gates.

---

## 5. THE VULNERABILITIES WE DETECT (CWE & OWASP MAPPINGS)

When asked *"What specific vulnerabilities does your platform catch?"*, cite this table:

| Vulnerability Title | CWE ID | OWASP Top 10 (2021) | Severity | Why It Is Dangerous | How We Remediate It |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SQL Injection** | **CWE-89** | A03:2021 - Injection | **CRITICAL** | Attacker extracts, modifies, or deletes the entire database via dynamic string interpolation. | Replace string concatenation (`f"SELECT... {user}"`) with parameterized query placeholders (`cursor.execute(sql, (user,))`). |
| **Command Injection** | **CWE-78** | A03:2021 - Injection | **CRITICAL** | Spawning a system shell allows attackers to execute arbitrary OS commands via chained inputs (`id; rm -rf /`). | Remove `shell=True` and pass command arguments as a validated structured list (`subprocess.run(['cmd', arg])`). |
| **Dangerous Dynamic Execution** | **CWE-95** | A03:2021 - Injection | **CRITICAL** | Using `eval()` or `exec()` executes arbitrary attacker-supplied Python code. | Replace `eval()` with `ast.literal_eval()` or structured JSON parsers. |
| **Insecure Deserialization** | **CWE-502** | A08:2021 - Software & Data Integrity | **CRITICAL** | Unpickling untrusted byte streams leads to direct Remote Code Execution (RCE). | Replace `pickle.loads()` with safe serialization formats like `json.loads()`. |
| **Hardcoded Secret / API Key** | **CWE-798** | A07:2021 - Identification & Auth Failures | **HIGH** | Plaintext API keys committed to version control can be scraped and exploited. | Extract secrets into environment variables (`os.getenv('API_KEY')`) or vault secrets. |
| **Path Traversal** | **CWE-22** | A01:2021 - Broken Access Control | **HIGH** | Dot-dot-slash (`../`) manipulation allows attackers to read arbitrary files from the filesystem (`/etc/passwd`). | Validate paths with `os.path.abspath()` and verify they resolve within an authorized root directory. |
| **Insecure Cryptographic Hash** | **CWE-327** | A02:2021 - Cryptographic Failures | **MEDIUM** | MD5 and SHA-1 suffer from collision vulnerabilities and are cryptographically broken. | Upgrade hashing algorithms to `hashlib.sha256()` or `sha512()`. |

---

## 6. MATHEMATICAL FORMULARIES & SCORING MODELS (EXAMINER FAVORITES)

Examiners love asking: *"How do you calculate your scores? Show me the mathematics."* Here are the exact formulas:

### 1. McCabe's Cyclomatic Complexity ($CC$)
$$CC = E - V + 2P$$
- $E$ = Number of edges in the program's Control Flow Graph (CFG).
- $V$ = Number of vertices (atomic basic blocks).
- $P$ = Number of connected components ($P=1$ for a single function).
- **Simplified rule:** $CC = 1 + \sum(\text{Decision Points})$ (count of `if`, `elif`, `for`, `while`, `except`, `and`, `or`).
- **Interpretation:**
  - $1 - 10$: Simple, low risk (Grade A).
  - $11 - 20$: Moderate complexity, medium risk (Grade B).
  - $21 - 50$: Complex, high risk (Grade C).
  - $> 50$: Untestable, critical risk.

### 2. SEI Maintainability Index ($MI$)
Our platform implements the standard Software Engineering Institute (SEI) composite polynomial:
$$MI_{\text{raw}} = 171 - 5.2\ln(V_{\text{hal}}) - 0.23(CC) - 16.2\ln(SLOC) + 50\sin(\sqrt{2.4 \cdot CR})$$
Where:
- $V_{\text{hal}} = (N_1 + N_2) \cdot \log_2(\eta_1 + \eta_2)$ is the **Halstead Program Volume**.
- $SLOC$ = Executable Source Lines of Code.
- $CR$ = Comment Ratio ($CLOC / Total\_LOC$).
- Normalized to $0 - 100$:
$$MI = \max(0.0, \min(100.0, (MI_{\text{raw}} \cdot 100.0) / 171.0))$$

### 3. Security Score Penalty Deduction Model ($S_{\text{sec}}$)
$$S_{\text{sec}} = \max\left(0, 100 - (25 \cdot N_{\text{crit}} + 15 \cdot N_{\text{high}} + 10 \cdot N_{\text{med}} + 5 \cdot N_{\text{low}})\right)$$
- If a codebase has 2 Critical vulnerabilities and 1 High:  
  $\text{Score} = 100 - (2 \times 25 + 1 \times 15) = 100 - 65 = 35/100$ (Grade **F**).
- When all vulnerabilities are fixed:  
  $\text{Score} = 100 - 0 = \mathbf{100/100}$ (Grade **A+**).

### 4. Technical Debt Estimation ($TD$)
$$TD = \sum_{v \in V} \text{RemediationHours}(v) + \max(0, CC - 10) \cdot 0.5 + \max(0, 65 - MI) \cdot 0.1$$
- **Standard remediation effort constants:**
  - Critical severity (SQLi, Command Injection): **2.5 hours** each.
  - High severity (Hardcoded Secret, Path Traversal): **1.5 hours** each.
  - Medium severity (MD5 Weak Hash): **1.0 hour** each.
  - Low severity: **0.5 hours** each.

---

## 7. STEP-BY-STEP LIVE DEMO EXECUTION SCRIPT

Follow this exact walkthrough during your viva demonstration:

### Step 1: Open the Application
- Open Google Chrome and navigate to: `http://localhost:8000` (or `127.0.0.1:8000`).
- Point out the clean executive header and active status indicator.

### Step 2: Demonstrate the Vulnerable Code Scan
1. Click on the **`Code Scanner & Annotator`** tab.
2. Click the preset button: **`⚠ Vulnerable Python`**.
3. Point to the code editor:
   - *"Here we have a realistic payment checkout service containing hardcoded Stripe API keys, dynamic SQL string interpolation, an `eval()` discount engine, and unsanitized `subprocess.run(..., shell=True)`."*
4. Click **`🚀 Scan & Review Code`**.
5. Observe the sub-second execution:
   - Point to the right-hand annotated drawer: *"Notice how line 7, line 11, line 16, line 19, and line 22 are instantly highlighted with color-coded severity badges."*

### Step 3: Demonstrate the Executive Dashboard
1. Switch to the **`Executive Dashboard`** tab.
2. Explain the metrics:
   - Security Health Grade: **F**
   - Security Score: **0 / 100**
   - Vulnerabilities Detected: **7**
   - Estimated Technical Debt: **10.5 hrs**
   - Point to the red circular gauge and AI Code Health Summary.

### Step 4: Demonstrate the Vulnerabilities & OWASP Tab
1. Click on **`Vulnerabilities & OWASP`**.
2. Show the detailed table:
   - *"Each finding maps directly to official CWE standards and the OWASP Top 10 2021 taxonomy."*
   - Highlight the concrete recommendations provided for each issue.

### Step 5: Demonstrate the Remediation (Auto-Fix)
1. Switch back to **`Code Scanner & Annotator`**.
2. Click the green **`✨ Auto-Fix All`** button.
3. Show the updated code in the editor:
   - String concatenation in SQL query is replaced with parameterized placeholders.
   - `shell=True` is eliminated.
   - Secret key is replaced with `os.getenv()`.
4. Switch back to **`Executive Dashboard`**:
   - Point out the updated scores:
     - Security Health Grade: **A+**
     - Security Score: **100 / 100**
     - Vulnerabilities Detected: **0**
     - Estimated Technical Debt: reduced from **10.5 hrs down to 1.6 hrs**.
   - Show the green circular gauge.
5. Switch to **`Vulnerabilities & OWASP`**:
   - Point to the banner: *"Zero Security Vulnerabilities Detected!"*

### Step 6: Demonstrate the Git Diff Analyzer
1. Click on the **`Git Diff Analyzer`** tab.
2. Paste or load a sample unified diff commit.
3. Click **`🔍 Analyze Git Diff`**.
4. Explain:
   - *"This simulates a developer opening a Pull Request on GitHub or GitLab. The engine analyzes only the modified lines (`+` lines) and flags any newly introduced vulnerabilities before the code can be merged into production."*

### Step 7: Demonstrate Compliance Reporting
1. Click on **`Audit Report Exporter`**.
2. Click **`📥 Download HTML Audit Report`**:
   - Show the generated self-contained HTML audit file complete with badges and remediation tables.
3. Click **`💾 Export Raw JSON Audit Data`**:
   - Explain: *"This JSON output allows CI/CD systems like Jenkins or GitHub Actions to enforce automated quality gates."*

---

## 8. TOP 20 VIVA QUESTIONS & BULLETPROOF MODEL ANSWERS

### Q1: What is the main objective of your project?
> **Model Answer:**  
> *"The primary objective is to build a lightweight, sub-second static code review platform that combines security vulnerability detection (OWASP Top 10 and CWE) with structural software quality metrics (Cyclomatic Complexity and Maintainability Index), providing real-time line annotations and automated remediation before code reaches production."*

### Q2: What is the difference between SAST and DAST? Where does your platform fit?
> **Model Answer:**  
> *"SAST (Static Application Security Testing) analyzes source code from the inside without executing it (white-box testing). DAST (Dynamic Application Security Testing) tests running applications from the outside by sending malicious payloads (black-box testing). Our platform is a **SAST** tool, positioned early in the development phase to shift security left."*

### Q3: How do you detect vulnerabilities without executing malicious code?
> **Model Answer:**  
> *"We use Python's built-in `ast` (Abstract Syntax Tree) module. When a developer submits code, the engine parses it into a hierarchical syntax tree. We implement specialized `NodeVisitor` classes that inspect specific node types—such as `ast.Call`, `ast.Assign`, and `ast.BinOp`. For example, when inspecting an SQL query, we check if the string argument to `cursor.execute` is built via `ast.FormattedValue` (f-string) or `ast.BinOp` (string concatenation) rather than a tuple of parameters."*

### Q4: Why not just use Regular Expressions for everything? Why use AST?
> **Model Answer:**  
> *"Regular expressions are fast but syntax-blind. They struggle with nested parentheses, multi-line logic, comments, and variable scope. For example, regex cannot reliably distinguish whether `eval()` is called inside a comment or inside actual execution logic. AST gives us true semantic understanding. However, for patterns like hardcoded API tokens (`sk_live_...`), regex is exceptionally effective. That is why our engine is a **hybrid** combining both."*

### Q5: What is Cyclomatic Complexity and why does it matter?
> **Model Answer:**  
> *"Cyclomatic Complexity, formulated by Thomas McCabe, measures the number of linearly independent paths through a program's source code. Mathematically it is $CC = E - V + 2P$. High cyclomatic complexity indicates deeply nested conditional logic, which is hard to understand, test, and maintain, and significantly correlates with a higher likelihood of security defects."*

### Q6: How is the Maintainability Index calculated?
> **Model Answer:**  
> *"We use the standard SEI polynomial formula which combines Halstead Program Volume ($V$), Cyclomatic Complexity ($CC$), Source Lines of Code ($SLOC$), and Comment Ratio ($CR$). We normalize the raw score to a $0 - 100$ scale. A score above 75 represents high maintainability (Grade A or B), while a score below 65 indicates high technical debt."*

### Q7: What is Technical Debt and how does your tool estimate it in hours?
> **Model Answer:**  
> *"Technical debt represents the future rework cost incurred by choosing an easy or flawed solution today. Our platform models technical debt in engineering remediation hours: each Critical issue is weighted at 2.5 hours, High issues at 1.5 hours, Medium issues at 1.0 hour, plus penalty hours for excessive cyclomatic complexity ($CC > 10$) and low maintainability ($MI < 65$)."*

### Q8: What happens when the user clicks 'Auto-Fix All'?
> **Model Answer:**  
> *"The backend's remediation engine takes the AST analysis and applies deterministic, context-aware code transformations. For SQL injection, it rewrites the query into a parameterized string and passes the parameters as a tuple. For dynamic execution, it removes `eval()`. For subprocess calls, it strips `shell=True` and transforms the command string into a safe argument array. The clean code is returned and re-analyzed instantly, updating all scores to 100%."*

### Q9: How does the Git Diff Analyzer work?
> **Model Answer:**  
> *"It parses unified diff patches formatted like `diff --git`. It scans the hunk headers (e.g., `@@ -14,5 +14,12 @@`) and evaluates only lines starting with `+` (added code), ignoring context lines or deleted lines (`-`). This ensures that developers are only evaluated on the code they actually modified in that specific pull request."*

### Q10: How does your tool compare to SonarQube?
> **Model Answer:**  
> *"SonarQube is a fantastic enterprise platform, but it requires dedicated Java server infrastructure, a relational database, and lengthy build-stage scans taking several minutes. Our platform is ultra-lightweight, runs in sub-second timeframes (<180 ms), integrates an immediate interactive code editor with line annotations, and supports instant one-click auto-fixing directly in the browser."*

### Q11: How do you prevent false positives?
> **Model Answer:**  
> *"By leveraging AST semantic inspection rather than naive keyword matching. For example, instead of flagging every occurrence of the word 'SELECT', we verify that the call is made on a database cursor object and specifically check whether string concatenation or interpolation is used in constructing the query parameter."*

### Q12: Can your system analyze other programming languages besides Python?
> **Model Answer:**  
> *"Yes. While our primary deep AST parser is specialized for Python, our regex and structural analyzer includes preset signature patterns for JavaScript / Node.js Express (detecting `child_process.exec`, insecure CORS, hardcoded JWT secrets) and can be extended to languages like Java and Go by plugging in tree-sitter or ANTLR grammar parsers."*

### Q13: What security standards does your project align with?
> **Model Answer:**  
> *"Our project strictly maps all detections to **OWASP Top 10 (2021)**, **CWE/SANS Top 25 Most Dangerous Software Weaknesses**, and adheres to **ISO/IEC 25010** software product quality standards and **NIST SP 800-53** security controls."*

### Q14: Is the code executed on your server during analysis?
> **Model Answer:**  
> *"No! This is a core architectural safety feature. The code is only parsed into an Abstract Syntax Tree via Python's standard `ast.parse()` library. The code itself is never executed or imported, eliminating any risk of server-side code execution."*

### Q15: What backend framework did you use and why?
> **Model Answer:**  
> *"We used **FastAPI** running on **Uvicorn** ASGI server. FastAPI was chosen because of its asynchronous capabilities, automatic Pydantic request validation, high execution speed comparable to NodeJS and Go, and clean RESTful design."*

### Q16: How does the platform export reports?
> **Model Answer:**  
> *"The Audit Report Exporter generates two formats: a self-contained, responsive HTML file embedded with CSS styling, badges, and remediation advice for management and stakeholders, and a structured raw JSON payload for automated CI/CD pipeline integration."*

### Q17: What are the hardware and software minimum requirements?
> **Model Answer:**  
> *"The platform is extremely lightweight. It runs on any modern dual-core CPU with 2 GB RAM, requires Python 3.10+ and a modern web browser. Analysis runs in memory with zero database overhead."*

### Q18: What were the major technical challenges you encountered during development?
> **Model Answer:**  
> *"The most challenging aspects were: 1) Accurately mapping AST node line offsets to front-end editor positions, 2) Constructing deterministic code rewrite rules that remediate security flaws without altering the program's intended business logic, and 3) Parsing complex Git unified diff hunks correctly."*

### Q19: What are the future enhancements planned for this project?
> **Model Answer:**  
> *"Our planned roadmap includes: 1) Integrating local Small Language Models (SLMs) for complex semantic reasoning on edge cases, 2) Packaging the engine as a native VS Code and JetBrains IDE extension, and 3) Developing a GitHub Action for direct PR commenting and blocking."*

### Q20: Why should an organization adopt SecureCode AI?
> **Model Answer:**  
> *"Because it drastically reduces the cost and cycle time of security reviews. By empowering developers to identify and auto-fix security vulnerabilities at the moment of code creation, organizations eliminate security backlogs, pass compliance audits, and prevent catastrophic production data breaches."*

---

## 9. TEAM SPEAKING ROLE ALLOCATIONS

To demonstrate high teamwork and collaboration during tomorrow's evaluation, divide the speaking roles as follows:

### 1. Anoop Shukla (Lead & Architecture Specialist)
- **What to introduce:** Project Title, Problem Statement, DevSecOps Shift-Left concept.
- **Technical focus:** Overall architecture diagram, FastAPI backend design, REST API endpoints.
- **Viva topics to handle:** System architecture, tool comparisons (SonarQube vs. SecureCode AI), future roadmap.

### 2. Driti Khurana (Security & Detection Engine Specialist)
- **What to introduce:** Security vulnerabilities detected (SQLi, Command Injection, CWE-89, CWE-78, etc.).
- **Technical focus:** Hybrid AST Parser and Regex Engine, `NodeVisitor` implementation, OWASP Top 10 mapping.
- **Viva topics to handle:** How AST parsing works, false positive prevention, vulnerability classification.

### 3. Sahil Mondal (Metrics, Algorithms & Git Diff Specialist)
- **What to introduce:** Mathematical formulations and scoring models.
- **Technical focus:** McCabe Cyclomatic Complexity formula, SEI Maintainability Index polynomial, Technical Debt calculation, Git Unified Diff analyzer.
- **Viva topics to handle:** How complexity is calculated, how Git patches are audited, scoring penalty models.

### 4. Kavya (UI/UX, Demo Lead & Reporting Specialist)
- **What to introduce:** Front-end interactive features and compliance reporting.
- **Technical focus:** Live platform demonstration (switching tabs, running scans, triggering Auto-Fix, downloading audit reports).
- **Viva topics to handle:** User workflow, Executive Dashboard metrics, HTML and JSON report export, industry compliance (ISO 25010, NIST).

---

## FINAL TIPS FOR TOMORROW'S EVALUATION
1. **Be Confident:** You built a functional, sub-second DevSecOps platform with live AST parsing, automated patching, and quantitative scoring.
2. **Stick to the Terms:** Use proper terminology (*"Shift-Left"*, *"AST NodeVisitor"*, *"McCabe Cyclomatic Complexity"*, *"CWE-89"*, *"Parameterization"*).
3. **Show, Don't Just Tell:** Keep the browser running with the platform ready at `http://localhost:8000`. Run the scan live in front of the examiners.
4. **Support Each Other:** If one teammate is asked a question and pauses, another teammate can politely add: *"Adding to what my teammate mentioned, our platform also..."*

**Good luck! You are thoroughly prepared to ace this evaluation.**
