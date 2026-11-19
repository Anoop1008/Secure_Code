import os
import re
from typing import List, Dict, Any

class GitScanner:
    """
    Git Repository & Diff Analyzer Engine:
    Parses unified git diffs, extracts modified line changes,
    and supports multi-file codebase scans.
    """

    def parse_git_diff(self, diff_content: str) -> List[Dict[str, Any]]:
        """
        Parses standard unified diff format into file-by-file added code snippets.
        """
        parsed_files = []
        current_file = None
        current_lines = []
        current_line_no = 0

        lines = diff_content.splitlines()
        for line in lines:
            if line.startswith("diff --git") or line.startswith("+++ b/"):
                if current_file and current_lines:
                    parsed_files.append({
                        "filename": current_file,
                        "code": "\n".join(current_lines)
                    })
                if line.startswith("+++ b/"):
                    current_file = line[6:].strip()
                elif line.startswith("diff --git"):
                    parts = line.split(" ")
                    if len(parts) >= 4:
                        current_file = parts[3].replace("b/", "")
                current_lines = []

            elif line.startswith("@@"):
                # Extract line numbers from hunk header: @@ -10,5 +12,8 @@
                match = re.search(r"\+(\d+)", line)
                if match:
                    current_line_no = int(match.group(1))

            elif line.startswith("+") and not line.startswith("+++"):
                current_lines.append(line[1:])
                current_line_no += 1
            elif not line.startswith("-"):
                current_lines.append(line)
                current_line_no += 1

        if current_file and current_lines:
            parsed_files.append({
                "filename": current_file,
                "code": "\n".join(current_lines)
            })

        return parsed_files if parsed_files else [{"filename": "patch.diff", "code": diff_content}]
