import unittest
import sys
import os

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.engine.static_analyzer import StaticAnalyzer
from app.engine.metrics import CodeMetricsCalculator
from app.engine.git_scanner import GitScanner

class TestStaticAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = StaticAnalyzer()
        self.metrics_calc = CodeMetricsCalculator()
        self.git_scanner = GitScanner()

    def test_static_analyzer_detects_sqli(self):
        vulnerable_code = """
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
"""
        vulns = self.analyzer.analyze(vulnerable_code, "test.py", "python")
        self.assertTrue(len(vulns) > 0)
        sqli_found = any(v.cwe == "CWE-89" for v in vulns)
        self.assertTrue(sqli_found, "SQL Injection vulnerability (CWE-89) should be detected.")

    def test_static_analyzer_detects_eval(self):
        vulnerable_code = """
def run_dynamic(user_input):
    return eval(user_input)
"""
        vulns = self.analyzer.analyze(vulnerable_code, "test.py", "python")
        self.assertTrue(len(vulns) > 0)
        eval_found = any(v.cwe == "CWE-95" for v in vulns)
        self.assertTrue(eval_found, "Dynamic code execution (CWE-95) should be detected.")

    def test_metrics_calculator(self):
        code = """
# Test function
def calculate_sum(a, b):
    if a > 0:
        if b > 0:
            return a + b
    return 0
"""
        metrics = self.metrics_calc.calculate(code, "python", 0)
        self.assertGreater(metrics.total_loc, 0)
        self.assertGreaterEqual(metrics.cyclomatic_complexity, 3)
        self.assertGreater(metrics.maintainability_index, 0)
        self.assertIn(metrics.maintainability_grade, ["A", "B", "C", "D", "F"])

    def test_git_diff_parser(self):
        diff = """diff --git a/app.py b/app.py
--- a/app.py
+++ b/app.py
@@ -1,3 +1,3 @@
-API_KEY = "123"
+API_KEY = "SECRET_123456789"
"""
        parsed = self.git_scanner.parse_git_diff(diff)
        self.assertTrue(len(parsed) > 0)
        self.assertIn("SECRET_123456789", parsed[0]["code"])

if __name__ == "__main__":
    unittest.main()
