from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class VulnerabilityItem(BaseModel):
    id: str
    title: str
    description: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    cwe: str       # e.g., CWE-89
    owasp: str     # e.g., A03:2021 - Injection
    line: int
    end_line: Optional[int] = None
    code_snippet: str
    recommendation: str
    suggested_fix: str

class MetricsSummary(BaseModel):
    total_loc: int
    source_loc: int
    comment_loc: int
    cyclomatic_complexity: float
    complexity_grade: str
    maintainability_index: float
    maintainability_grade: str
    technical_debt_hours: float
    comment_density: float

class AnalysisRequest(BaseModel):
    code: str
    filename: Optional[str] = "main.py"
    language: Optional[str] = "python"
    api_key: Optional[str] = None

class GitAnalysisRequest(BaseModel):
    repo_url: str
    branch: Optional[str] = "main"

class DiffAnalysisRequest(BaseModel):
    diff_content: str
    filename: Optional[str] = "patch.diff"

class AnalysisResult(BaseModel):
    scan_id: str
    timestamp: str
    filename: str
    language: str
    security_score: float
    quality_score: float
    overall_grade: str
    vulnerabilities: List[VulnerabilityItem]
    metrics: MetricsSummary
    vulnerability_counts: Dict[str, int]
    owasp_breakdown: Dict[str, int]
    ai_summary: str
    ai_recommendations: List[str]

class ExportReportRequest(BaseModel):
    analysis_result: AnalysisResult
    format: str = "html"
