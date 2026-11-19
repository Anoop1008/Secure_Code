# PPT SLIDE CONTENT — SECURECODE AI
### Capstone Project Presentation | Chandigarh University

---

## SLIDE 1 — TITLE SLIDE

**SECURE CODE REVIEW AND SOFTWARE QUALITY ANALYSIS PLATFORM**

*SecureCode AI*

---

Submitted by:

| Name | UID |
|---|---|
| Anoop Shukla | 23BCS10912 |
| Driti Khurana | 23BCS11997 |
| Sahil Mondal | 23BCS14298 |
| Kavya | 23BCS14821 |

Department of Computer Science & Engineering  
Chandigarh University, Mohali — May 2026

---

## SLIDE 2 — THE PROBLEM

**Why Security Cannot Wait Until the End**

- Over **80% of enterprise data breaches** originate from vulnerabilities introduced during development
- A bug found during **coding costs almost nothing** to fix
- The **same bug found after launch costs 30x to 100x more** — in data leaks, server shutdowns, and legal penalties
- Existing tools are either **too slow** (taking minutes to scan) or **too complex** to understand without a security expert
- Developers need **instant, in-context feedback** — not post-deployment panic

> *The earlier you find a problem, the cheaper it is to fix it.*

---

## SLIDE 3 — OUR SOLUTION

**SecureCode AI — Think of It as "Grammarly for Code Security"**

Just like Grammarly highlights writing mistakes as you type, SecureCode AI:

- ✅ **Instantly scans** submitted code and highlights every security flaw with line numbers
- ✅ **Grades the code** from F (dangerous) to A+ (fully secure) in under a second
- ✅ **Auto-fixes** all detected flaws with a single click — no manual rewriting needed
- ✅ **Tracks complexity and technical debt** so managers know the repair cost in hours
- ✅ **Generates downloadable audit reports** for clients and compliance teams

**Who uses it?** Developers, Team Leads, Security Auditors, Engineering Managers

---

## SLIDE 4 — HOW IT WORKS

**Three-Layer Architecture**

**Layer 1 — The User Interface (Browser)**
- Clean, visual dashboard accessible from any browser
- Code editor with real-time highlighted annotations on the right

**Layer 2 — The Detection Engine (Backend)**
- Reads and parses the code without ever executing it (100% safe)
- Uses a hybrid approach: reads the code's grammatical structure AND matches known danger patterns
- Covers Python and Node.js / JavaScript

**Layer 3 — Scoring & Repair Pipeline**
- Calculates Security Score, Quality Score, Complexity Grade, and Technical Debt hours
- Applies proven industry patterns to rewrite insecure code into safe code
- Re-grades the code after each fix

---

## SLIDE 5 — PLATFORM FEATURES (LIVE DEMO)

**5 Core Tabs of the Application**

| Tab | What It Does |
|---|---|
| 🖥️ Executive Dashboard | Shows health grade (A+ to F), security/quality scores, vulnerability count, and estimated debt hours |
| 🔍 Code Scanner & Annotator | Dual-pane editor — code on left, security badges on right; one-click Auto-Fix |
| 🔀 Git Diff Analyzer | Scans only the newly added lines in a Pull Request before it is merged into the main project |
| ⚠️ Vulnerabilities & OWASP | Detailed audit table with line number, severity, official standard name, and fix recommendation |
| 📄 Audit Report Exporter | Downloads a client-ready HTML report or raw JSON data for automated pipelines |

---

## SLIDE 6 — WHAT WE DETECT & FIX

**Security Vulnerabilities Covered**

| Issue | Real-World Risk | Severity |
|---|---|---|
| SQL Injection | Hacker reads or deletes the entire customer database | 🔴 Critical |
| Command Injection | Hacker takes full control of the company server | 🔴 Critical |
| Dangerous Code Execution | Any text from the internet is blindly run as a command | 🔴 Critical |
| Hardcoded Passwords / API Keys | Credentials are visible to anyone with code access | 🟠 High |
| Path Traversal | User can access private system files outside their folder | 🟠 High |
| Weak Password Hashing | Outdated scrambling algorithms cracked in seconds | 🟡 Medium |

**Standards Followed:** OWASP Top 10 (2021) · CWE / SANS Top 25 · ISO/IEC 25010 · NIST SP 800-53

---

## SLIDE 7 — RESULTS & IMPACT

**Before and After Auto-Fix — Measured on the Live Platform**

| Metric | Before (Vulnerable Code) | After (Auto-Fixed Code) |
|---|---|---|
| Security Health Grade | **F** | **A+** |
| Security Score | **0 / 100** | **100 / 100** |
| Vulnerabilities Found | **7 Issues** | **0 Issues** |
| Quality Score | 79.3 / 100 | 75.7 / 100 |
| Cyclomatic Complexity | 5 (A) | 7 (B) |
| Estimated Technical Debt | **10.5 hours** | **1.6 hours** |

**Key Achievement:** Our platform reduced detected technical debt by **84.7%** in a single automated pass — with no manual developer effort required.

---

## SLIDE 8 — CONCLUSION & FUTURE WORK

**What We Built & What Comes Next**

**What We Delivered:**
- A fully functional, real-time DevSecOps platform running at sub-second speed
- 7-category vulnerability detection mapped to international security standards
- Automated one-click code remediation with live re-grading
- Professional audit report generation for compliance and management use

**Future Roadmap:**
- 🔌 Package as a **VS Code Plugin** so developers never need to leave their editor
- 🤖 Integrate a **local AI model** for plain-language explanation of complex design flaws
- 🔗 Build a **GitHub Actions integration** to block Pull Requests that fail the security scan
- 🌐 Expand language support to **Java, Go, and C++**

---

*Thank you — We are happy to take your questions.*
