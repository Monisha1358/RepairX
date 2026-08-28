import shutil
import subprocess
import tempfile
import time
import sys
import urllib.error
import urllib.request
from pathlib import Path


class ProofTester:

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def _wait_for_server(self, url: str, process, timeout: int = 10):
        start = time.time()

        while time.time() - start < timeout:

            if process.poll() is not None:
                return False

            try:
                urllib.request.urlopen(
                    url,
                    timeout=1
                )
                return True

            except urllib.error.HTTPError:
                # Server is running even if endpoint returns an error.
                return True

            except (
                urllib.error.URLError,
                ConnectionRefusedError
            ):
                time.sleep(0.5)

        return False

    def test_patch(self, old_code: str, new_code: str):

        temp_dir = Path(
            tempfile.mkdtemp(
                prefix="repairx_proof_"
            )
        )

        process = None

        try:
            # -------------------------------------------------
            # 1. Create isolated repository
            # -------------------------------------------------

            test_repo = temp_dir / "repo"

            shutil.copytree(
                self.repo_path,
                test_repo
            )

            # -------------------------------------------------
            # 2. Locate application file
            # -------------------------------------------------

            app_file = test_repo / "app.py"

            if not app_file.exists():
                return {
                    "status": "FAIL",
                    "reason": (
                        f"Application file was not found: "
                        f"{app_file}"
                    )
                }

            source = app_file.read_text(
                encoding="utf-8"
            )

            # -------------------------------------------------
            # 3. Verify original code
            # -------------------------------------------------

            if old_code not in source:

                return {
                    "status": "FAIL",
                    "reason": (
                        "Expected original code was not found "
                        "inside the isolated repository."
                    )
                }

            # -------------------------------------------------
            # 4. Apply proposed patch
            # -------------------------------------------------

            repaired_source = source.replace(
                old_code,
                new_code,
                1
            )

            app_file.write_text(
                repaired_source,
                encoding="utf-8"
            )

            # -------------------------------------------------
            # 5. Syntax validation
            # -------------------------------------------------

            compile(
                repaired_source,
                str(app_file),
                "exec"
            )

            # -------------------------------------------------
            # 6. Start isolated API
            # -------------------------------------------------

            process = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "uvicorn",
                    "app:app",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    "8010"
                ],
                cwd=str(test_repo),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            base_url = "http://127.0.0.1:8010"

            # -------------------------------------------------
            # 7. Wait until server is ready
            # -------------------------------------------------

            server_ready = self._wait_for_server(
                f"{base_url}/users/1",
                process
            )

            if not server_ready:

                stderr = ""

                if process.stderr:
                    stderr = process.stderr.read()

                return {
                    "status": "FAIL",
                    "reason": (
                        "Repaired API failed to start.\n"
                        + stderr
                    )
                }

            # -------------------------------------------------
            # 8. Test valid user
            # -------------------------------------------------

            try:

                response = urllib.request.urlopen(
                    f"{base_url}/users/1",
                    timeout=5
                )

                valid_status = response.status
                valid_body = response.read().decode()

            except Exception as error:

                return {
                    "status": "FAIL",
                    "reason": (
                        "Valid user request failed: "
                        + str(error)
                    )
                }

            # -------------------------------------------------
            # 9. Test previously failing user
            # -------------------------------------------------

            try:

                response = urllib.request.urlopen(
                    f"{base_url}/users/99",
                    timeout=5
                )

                missing_status = response.status
                missing_body = response.read().decode()

            except urllib.error.HTTPError as error:

                missing_status = error.code
                missing_body = error.read().decode()

            # -------------------------------------------------
            # 10. Validate results
            # -------------------------------------------------

            if valid_status != 200:

                return {
                    "status": "FAIL",
                    "reason": (
                        "Valid user request returned "
                        f"HTTP {valid_status}."
                    )
                }

            if missing_status >= 500:

                return {
                    "status": "FAIL",
                    "reason": (
                        "The repaired API still returns "
                        f"HTTP {missing_status} for user 99."
                    )
                }

            # -------------------------------------------------
            # 11. SUCCESS
            # -------------------------------------------------

            return {
                "status": "PASS",
                "reason": (
                    "Patch passed syntax validation, "
                    "preserved the valid user request, "
                    "and prevented the original missing-user failure."
                ),
                "valid_request": valid_body,
                "missing_user_request": missing_body
            }

        except Exception as error:

            return {
                "status": "FAIL",
                "reason": str(error)
            }

        finally:

            if process is not None:

                process.terminate()

                try:
                    process.wait(
                        timeout=3
                    )

                except subprocess.TimeoutExpired:

                    process.kill()

            shutil.rmtree(
                temp_dir,
                ignore_errors=True
            )