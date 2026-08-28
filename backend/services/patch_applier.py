from dataclasses import dataclass
from pathlib import Path
import shutil


@dataclass
class PatchApplyResult:
    status: str
    file_path: str
    message: str
    backup_path: str | None = None


class PatchApplier:

    def apply(
        self,
        file_path: str,
        old_code: str,
        new_code: str
    ) -> PatchApplyResult:

        path = Path(file_path)

        if not path.exists():
            return PatchApplyResult(
                status="FAIL",
                file_path=str(path),
                message="Target file does not exist."
            )

        source = path.read_text(
            encoding="utf-8"
        )

        if old_code not in source:
            return PatchApplyResult(
                status="FAIL",
                file_path=str(path),
                message="Expected original code was not found."
            )

        backup_path = path.with_suffix(
            path.suffix + ".repairx.bak"
        )

        shutil.copy2(
            path,
            backup_path
        )

        repaired_source = source.replace(
            old_code,
            new_code,
            1
        )

        try:
            compile(
                repaired_source,
                str(path),
                "exec"
            )
        except SyntaxError as error:
            return PatchApplyResult(
                status="FAIL",
                file_path=str(path),
                message=(
                    "Patch would introduce a syntax error: "
                    + str(error)
                ),
                backup_path=str(backup_path)
            )

        path.write_text(
            repaired_source,
            encoding="utf-8"
        )

        return PatchApplyResult(
            status="PASS",
            file_path=str(path),
            message="Patch applied successfully.",
            backup_path=str(backup_path)
        )