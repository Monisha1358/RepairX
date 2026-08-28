import re
from pathlib import Path


class RootCauseAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def analyze(self, error_type: str, error_message: str, traceback: str):
        file_path = self._extract_file(traceback)
        line_number = self._extract_line(traceback)

        return {
            "error_type": error_type,
            "error_message": error_message,
            "affected_file": file_path,
            "affected_line": line_number,
            "root_cause": self._determine_root_cause(
                error_type,
                error_message,
                traceback
            ),
            "confidence": self._calculate_confidence(
                error_type,
                file_path,
                line_number
            )
        }

    def _extract_file(self, traceback: str):
        matches = re.findall(
            r'File "([^"]+)"',
            traceback
        )

        for path in reversed(matches):
            if "demo_repo" in path:
                return path

        return None

    def _extract_line(self, traceback: str):
        matches = re.findall(
            r'File "([^"]+)", line (\d+)',
            traceback
        )

        for path, line in reversed(matches):
            if "demo_repo" in path:
                return int(line)

        return None

    def _determine_root_cause(
        self,
        error_type: str,
        error_message: str,
        traceback: str
    ):
        if error_type == "KeyError":
            return (
                "The requested user_id does not exist in the users "
                "dictionary, causing a direct dictionary lookup to fail."
            )

        return (
            "The failure could not yet be classified automatically."
        )

    def _calculate_confidence(
        self,
        error_type: str,
        file_path: str,
        line_number: int
    ):
        score = 0.0

        if error_type:
            score += 0.4

        if file_path:
            score += 0.3

        if line_number:
            score += 0.3

        return round(score, 2)