import subprocess
from pathlib import Path


class GitDetective:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def _run_git(self, *args):
        result = subprocess.run(
            ["git", *args],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout.strip()

    def get_history(self, limit: int = 10):
        output = self._run_git(
            "log",
            f"-{limit}",
            "--pretty=format:%H|%s"
        )

        commits = []

        for line in output.splitlines():
            commit_hash, message = line.split("|", 1)

            commits.append({
                "hash": commit_hash,
                "message": message
            })

        return commits

    def get_diff(self, old_commit: str, new_commit: str):
        return self._run_git(
            "diff",
            "--unified=5",
            old_commit,
            new_commit
        )

    def get_changed_files(self, old_commit: str, new_commit: str):
        output = self._run_git(
            "diff",
            "--name-only",
            old_commit,
            new_commit
        )

        return output.splitlines()