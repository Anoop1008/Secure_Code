import ast
import math
from typing import Dict, Any
from app.models.schemas import MetricsSummary

class CodeMetricsCalculator:
    """
    Computes Software Quality Metrics:
    - Lines of Code (Total, SLOC, CLOC, Comment Density)
    - Cyclomatic Complexity (CC)
    - Maintainability Index (MI)
    - Estimated Technical Debt (Hours)
    """

    def calculate(self, code: str, language: str = "python", vuln_count: int = 0) -> MetricsSummary:
        lines = code.splitlines()
        total_loc = len(lines)

        sloc = 0
        cloc = 0
        blank_loc = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                blank_loc += 1
            elif stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
                cloc += 1
            else:
                sloc += 1

        if sloc + cloc > 0:
            comment_density = round((cloc / (sloc + cloc)) * 100, 2)
        else:
            comment_density = 0.0

        # Calculate Cyclomatic Complexity
        complexity = self._calculate_cyclomatic_complexity(code, language)
        complexity_grade = self._grade_complexity(complexity)

        # Calculate Maintainability Index
        maintainability = self._calculate_maintainability_index(sloc, complexity, cloc, total_loc)
        maintainability_grade = self._grade_maintainability(maintainability)

        # Estimate Technical Debt in Hours
        tech_debt = self._estimate_technical_debt(sloc, complexity, maintainability, vuln_count)

        return MetricsSummary(
            total_loc=total_loc,
            source_loc=sloc,
            comment_loc=cloc,
            cyclomatic_complexity=round(complexity, 2),
            complexity_grade=complexity_grade,
            maintainability_index=round(maintainability, 2),
            maintainability_grade=maintainability_grade,
            technical_debt_hours=round(tech_debt, 1),
            comment_density=comment_density
        )

    def _calculate_cyclomatic_complexity(self, code: str, language: str) -> float:
        if language.lower() == "python":
            try:
                tree = ast.parse(code)
                decision_nodes = 0
                for node in ast.walk(tree):
                    if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.ExceptHandler, ast.Assert)):
                        decision_nodes += 1
                    elif isinstance(node, ast.BoolOp):
                        decision_nodes += len(node.values) - 1
                    elif isinstance(node, ast.IfExp):
                        decision_nodes += 1
                return float(1 + decision_nodes)
            except SyntaxError:
                pass

        # Fallback keyword heuristic for non-python or unparseable code
        decision_keywords = ["if", "else if", "elif", "for", "while", "catch", "except", "case", "&&", "||", "and", "or"]
        count = 1
        for kw in decision_keywords:
            count += len(re_findall(rf"\b{kw}\b", code))
        return float(count)

    def _calculate_maintainability_index(self, sloc: int, complexity: float, cloc: int, total_loc: int) -> float:
        if sloc <= 0:
            return 100.0

        # Halstead Volume approximation
        halstead_volume = max(1.0, sloc * math.log2(max(2.0, sloc)))

        # Standard SEI Formula
        raw_mi = 171.0 - (5.2 * math.log(halstead_volume)) - (0.23 * complexity) - (16.2 * math.log(sloc))

        # Add comment ratio bonus
        if total_loc > 0:
            comment_ratio = cloc / total_loc
            raw_mi += 50.0 * math.sin(math.sqrt(comment_ratio * 2.4))

        normalized_mi = max(0.0, min(100.0, (raw_mi * 100.0) / 171.0))
        return normalized_mi

    def _grade_complexity(self, cc: float) -> str:
        if cc <= 5:
            return "A"
        elif cc <= 10:
            return "B"
        elif cc <= 20:
            return "C"
        elif cc <= 30:
            return "D"
        else:
            return "F"

    def _grade_maintainability(self, mi: float) -> str:
        if mi >= 80:
            return "A"
        elif mi >= 65:
            return "B"
        elif mi >= 50:
            return "C"
        elif mi >= 35:
            return "D"
        else:
            return "F"

    def _estimate_technical_debt(self, sloc: int, cc: float, mi: float, vuln_count: int) -> float:
        # Base debt from vulnerability count (1.5 hours per vulnerability)
        vuln_debt = vuln_count * 1.5

        # Debt from high complexity (above CC=5)
        complexity_debt = max(0.0, (cc - 5) * 0.8)

        # Debt from low maintainability (below MI=70)
        maintainability_debt = max(0.0, (70 - mi) * 0.15)

        # Code volume multiplier
        size_factor = (sloc / 100) * 0.2

        total_debt = vuln_debt + complexity_debt + maintainability_debt + size_factor
        return max(0.5, total_debt)

def re_findall(pattern: str, text: str):
    import re
    return re.findall(pattern, text)
