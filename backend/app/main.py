import datetime
import uuid
import os
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse

from app.models.schemas import (
    AnalysisRequest,
    GitAnalysisRequest,
    DiffAnalysisRequest,
    AnalysisResult,
    ExportReportRequest
)
from app.engine.static_analyzer import StaticAnalyzer
from app.engine.metrics import CodeMetricsCalculator
from app.engine.ai_engine import AIRemediationEngine
from app.engine.git_scanner import GitScanner
from app.engine.reporter import AuditReportGenerator

app = FastAPI(
    title="Secure Code Review and Software Quality Analysis Platform",
    description="Automated static analysis, security vulnerability scanning, software metrics, and AI remediation platform.",
    version="1.0.0"
)

# Enable CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = StaticAnalyzer()
metrics_calc = CodeMetricsCalculator()
ai_engine = AIRemediationEngine()
git_scanner = GitScanner()
reporter = AuditReportGenerator()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Secure Code Review Platform API",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

@app.post("/api/analyze/snippet", response_model=AnalysisResult)
def analyze_snippet(request: AnalysisRequest):
    if not request.code or not request.code.strip():
        raise HTTPException(status_code=400, detail="Code snippet cannot be empty.")

    filename = request.filename or "main.py"
    language = request.language or "python"

    # 1. Run Static Vulnerability Analysis
    vulnerabilities = analyzer.analyze(request.code, filename, language)

    # 2. Run Code Metrics Calculator
    metrics = metrics_calc.calculate(request.code, language, len(vulnerabilities))

    # 3. Calculate Security Score
    sec_deductions = 0
    vuln_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
    owasp_breakdown = {}

    for v in vulnerabilities:
        vuln_counts[v.severity] = vuln_counts.get(v.severity, 0) + 1
        owasp_breakdown[v.owasp] = owasp_breakdown.get(v.owasp, 0) + 1

        if v.severity == "CRITICAL":
            sec_deductions += 25
        elif v.severity == "HIGH":
            sec_deductions += 15
        elif v.severity == "MEDIUM":
            sec_deductions += 10
        elif v.severity == "LOW":
            sec_deductions += 5

    security_score = max(0.0, float(100 - sec_deductions))

    # 4. Calculate Quality Score
    quality_score = max(0.0, min(100.0, (metrics.maintainability_index * 0.6) + (max(0.0, 30.0 - metrics.cyclomatic_complexity) * 1.33)))

    # 5. Determine Overall Grade
    overall_score = (security_score * 0.6) + (quality_score * 0.4)
    if overall_score >= 90:
        overall_grade = "A+"
    elif overall_score >= 80:
        overall_grade = "A"
    elif overall_score >= 70:
        overall_grade = "B"
    elif overall_score >= 60:
        overall_grade = "C"
    elif overall_score >= 50:
        overall_grade = "D"
    else:
        overall_grade = "F"

    # 6. Generate AI Review & Remediation Suggestions
    ai_summary, ai_recommendations = ai_engine.generate_review_summary(
        vulnerabilities, metrics, language, request.api_key
    )

    scan_id = f"SCAN-{uuid.uuid4().hex[:8].upper()}"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return AnalysisResult(
        scan_id=scan_id,
        timestamp=timestamp,
        filename=filename,
        language=language,
        security_score=round(security_score, 1),
        quality_score=round(quality_score, 1),
        overall_grade=overall_grade,
        vulnerabilities=vulnerabilities,
        metrics=metrics,
        vulnerability_counts=vuln_counts,
        owasp_breakdown=owasp_breakdown,
        ai_summary=ai_summary,
        ai_recommendations=ai_recommendations
    )

@app.post("/api/analyze/diff", response_model=AnalysisResult)
def analyze_diff(request: DiffAnalysisRequest):
    if not request.diff_content or not request.diff_content.strip():
        raise HTTPException(status_code=400, detail="Diff content cannot be empty.")

    parsed_files = git_scanner.parse_git_diff(request.diff_content)
    combined_code = "\n".join([f["code"] for f in parsed_files])

    analysis_req = AnalysisRequest(
        code=combined_code,
        filename=request.filename or "git_patch.diff",
        language="python"
    )
    return analyze_snippet(analysis_req)

@app.post("/api/report/export")
def export_report(request: ExportReportRequest):
    if request.format == "json":
        return JSONResponse(content=request.analysis_result.dict())

    html_content = reporter.generate_html_report(request.analysis_result)
    return HTMLResponse(content=html_content, headers={
        "Content-Disposition": f"attachment; filename=Security_Audit_Report_{request.analysis_result.scan_id}.html"
    })

# Mount Frontend static files
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
