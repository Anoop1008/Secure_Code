import json
import html
from app.models.schemas import AnalysisResult

class AuditReportGenerator:
    """
    Audit Report Generator:
    Generates clean, professional, enterprise-grade HTML and JSON security audit reports
    with simple, corporate color grading suitable for formal documentation and print/PDF export.
    """

    def generate_html_report(self, result: AnalysisResult) -> str:
        # Subtle corporate badge styles
        severity_styles = {
            "CRITICAL": "background: #fef2f2; color: #991b1b; border: 1px solid #fecaca;",
            "HIGH":     "background: #fff7ed; color: #9a3412; border: 1px solid #fed7aa;",
            "MEDIUM":   "background: #fffbeb; color: #92400e; border: 1px solid #fde68a;",
            "LOW":      "background: #f0f9ff; color: #0369a1; border: 1px solid #bae6fd;",
            "INFO":     "background: #f8fafc; color: #475569; border: 1px solid #e2e8f0;"
        }

        grade_styles = {
            "A+": "background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0;",
            "A":  "background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0;",
            "B":  "background: #eff6ff; color: #1e40af; border: 1px solid #bfdbfe;",
            "C":  "background: #fffbeb; color: #854d0e; border: 1px solid #fde68a;",
            "D":  "background: #fff1f2; color: #9f1239; border: 1px solid #fecdd3;",
            "F":  "background: #fef2f2; color: #991b1b; border: 1px solid #fecaca;"
        }

        vuln_rows = ""
        if result.vulnerabilities:
            for v in result.vulnerabilities:
                style = severity_styles.get(v.severity, severity_styles["INFO"])
                escaped_snippet = html.escape(v.code_snippet)
                escaped_rec = html.escape(v.recommendation)
                escaped_title = html.escape(v.title)
                vuln_rows += f"""
                <tr>
                    <td style="padding: 12px 14px; font-weight: 600; color: #334155; white-space: nowrap;">Line {v.line}</td>
                    <td style="padding: 12px 14px; white-space: nowrap;">
                        <span style="{style} padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 11px; letter-spacing: 0.03em;">
                            {v.severity}
                        </span>
                    </td>
                    <td style="padding: 12px 14px;">
                        <div style="font-weight: 600; color: #0f172a; font-size: 13.5px;">{escaped_title}</div>
                        <div style="font-size: 11.5px; color: #64748b; margin-top: 3px;">{html.escape(v.cwe)} &bull; {html.escape(v.owasp)}</div>
                    </td>
                    <td style="padding: 12px 14px;">
                        <div style="font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 12px; color: #0f172a; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 6px 10px; max-width: 320px; overflow-x: auto;">
                            <code>{escaped_snippet}</code>
                        </div>
                    </td>
                    <td style="padding: 12px 14px; font-size: 13px; color: #334155; line-height: 1.5;">
                        {escaped_rec}
                    </td>
                </tr>
                """
        else:
            vuln_rows = """
            <tr>
                <td colspan="5" style="padding: 28px; text-align: center; color: #166534; background: #f0fdf4; font-weight: 600; font-size: 13.5px;">
                    Zero Security Vulnerabilities Detected. The scanned code meets baseline security standards.
                </td>
            </tr>
            """

        clean_recommendations = []
        for rec in result.ai_recommendations:
            # Strip any lingering emoji from recommendations
            clean_rec = rec.encode('ascii', 'ignore').decode('ascii').strip()
            if clean_rec.startswith(":"):
                clean_rec = clean_rec[1:].strip()
            clean_recommendations.append(f"<li style='margin-bottom: 10px; line-height: 1.55;'>{html.escape(clean_rec or rec)}</li>")

        recommendations_html = "".join(clean_recommendations)
        grade_style = grade_styles.get(result.overall_grade, grade_styles["B"])

        # Clean score text colors
        sec_color = "#166534" if result.security_score >= 80 else ("#854d0e" if result.security_score >= 60 else "#991b1b")
        vuln_color = "#991b1b" if len(result.vulnerabilities) > 0 else "#166534"

        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Audit & Software Quality Report - {html.escape(result.filename)}</title>
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
            margin: 0;
            padding: 32px 16px;
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
        }}
        .report-container {{
            max-width: 1080px;
            margin: 0 auto;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 40px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        }}
        .report-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 24px;
            margin-bottom: 32px;
        }}
        .report-title h1 {{
            margin: 0 0 6px 0;
            font-size: 22px;
            font-weight: 700;
            color: #0f172a;
            letter-spacing: -0.01em;
        }}
        .report-meta {{
            font-size: 13px;
            color: #64748b;
            line-height: 1.6;
        }}
        .report-meta span {{
            color: #0f172a;
            font-weight: 600;
        }}
        .grade-box {{
            {grade_style}
            padding: 10px 22px;
            border-radius: 6px;
            text-align: center;
            min-width: 100px;
        }}
        .grade-letter {{
            font-size: 32px;
            font-weight: 800;
            line-height: 1;
        }}
        .grade-sub {{
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 4px;
            opacity: 0.85;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 14px;
            margin-bottom: 32px;
        }}
        .metric-card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 14px 16px;
        }}
        .metric-label {{
            font-size: 11px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
        }}
        .metric-value {{
            font-size: 22px;
            font-weight: 700;
            color: #0f172a;
            margin-top: 4px;
        }}
        .metric-sub {{
            font-size: 11.5px;
            color: #94a3b8;
            margin-top: 2px;
        }}
        .section-header {{
            font-size: 15px;
            font-weight: 700;
            color: #0f172a;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 8px;
            margin: 32px 0 16px 0;
        }}
        .summary-panel {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 18px 20px;
            font-size: 14px;
            color: #334155;
            line-height: 1.6;
        }}
        table.audit-table {{
            width: 100%;
            border-collapse: collapse;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            margin-bottom: 24px;
        }}
        table.audit-table th {{
            background: #f8fafc;
            color: #475569;
            font-size: 11.5px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            text-align: left;
            padding: 10px 14px;
            border-bottom: 1px solid #e2e8f0;
        }}
        table.audit-table td {{
            border-bottom: 1px solid #f1f5f9;
            vertical-align: top;
        }}
        table.audit-table tr:last-child td {{
            border-bottom: none;
        }}
        ul.recs-list {{
            margin: 0;
            padding-left: 20px;
            color: #334155;
            font-size: 13.5px;
        }}
        .report-footer {{
            text-align: center;
            font-size: 12px;
            color: #94a3b8;
            border-top: 1px solid #e2e8f0;
            padding-top: 20px;
            margin-top: 36px;
        }}
        @media print {{
            body {{
                background: #ffffff;
                padding: 0;
            }}
            .report-container {{
                box-shadow: none;
                border: none;
                padding: 0;
                max-width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <div class="report-container">
        
        <!-- Header -->
        <div class="report-header">
            <div class="report-title">
                <h1>Software Security & Code Quality Audit Report</h1>
                <div class="report-meta">
                    Target File: <span>{html.escape(result.filename)}</span> &bull; 
                    Language: <span>{html.escape(result.language.upper())}</span> &bull; 
                    Scan ID: <span>{html.escape(result.scan_id)}</span><br/>
                    Generated: {html.escape(result.timestamp)}
                </div>
            </div>
            <div class="grade-box">
                <div class="grade-letter">{result.overall_grade}</div>
                <div class="grade-sub">Overall Rating</div>
            </div>
        </div>

        <!-- Metrics Row -->
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Security Score</div>
                <div class="metric-value" style="color: {sec_color};">{result.security_score} <span style="font-size: 13px; font-weight: 500; color: #64748b;">/ 100</span></div>
                <div class="metric-sub">OWASP / CWE Evaluation</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Quality Score</div>
                <div class="metric-value">{result.quality_score} <span style="font-size: 13px; font-weight: 500; color: #64748b;">/ 100</span></div>
                <div class="metric-sub">Maintainability Index</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Vulnerabilities</div>
                <div class="metric-value" style="color: {vuln_color};">{len(result.vulnerabilities)}</div>
                <div class="metric-sub">Total Findings</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Maintainability</div>
                <div class="metric-value">{result.metrics.maintainability_index}</div>
                <div class="metric-sub">Grade {result.metrics.maintainability_grade} (SEI Standard)</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Complexity</div>
                <div class="metric-value">{result.metrics.cyclomatic_complexity}</div>
                <div class="metric-sub">Control Flow (Grade {result.metrics.complexity_grade})</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Technical Debt</div>
                <div class="metric-value">{result.metrics.technical_debt_hours} <span style="font-size: 13px; font-weight: 500; color: #64748b;">hrs</span></div>
                <div class="metric-sub">Remediation Effort</div>
            </div>
        </div>

        <!-- Executive Summary -->
        <div class="section-header">Executive Summary</div>
        <div class="summary-panel">
            {html.escape(result.ai_summary)}
        </div>

        <!-- Findings Table -->
        <div class="section-header">Identified Security & Quality Findings</div>
        <table class="audit-table">
            <thead>
                <tr>
                    <th style="width: 80px;">Location</th>
                    <th style="width: 90px;">Severity</th>
                    <th style="width: 250px;">Title & Classification</th>
                    <th>Vulnerable Snippet</th>
                    <th>Recommendation</th>
                </tr>
            </thead>
            <tbody>
                {vuln_rows}
            </tbody>
        </table>

        <!-- Remediation Plan -->
        <div class="section-header">Remediation & Action Plan</div>
        <div class="summary-panel">
            <ul class="recs-list">
                {recommendations_html}
            </ul>
        </div>

        <!-- Footer -->
        <div class="report-footer">
            Generated by Secure Code Review & Software Quality Analysis Platform &bull; Professional Audit Document
        </div>

    </div>
</body>
</html>
        """
        return html_template
