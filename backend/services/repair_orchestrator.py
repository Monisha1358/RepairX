from pathlib import Path

from backend.services.root_cause_analyzer import RootCauseAnalyzer
from backend.services.patch_generator import MinimalPatchGenerator
from backend.services.risk_gate import RepairRiskGate
from backend.services.proof_tester import ProofTester
from backend.services.impact_analyzer import ImpactAnalyzer
from backend.services.patch_applier import PatchApplier


class RepairOrchestrator:

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

        self.root_cause_analyzer = RootCauseAnalyzer(
            str(self.repo_path)
        )

        self.patch_generator = MinimalPatchGenerator()

        self.risk_gate = RepairRiskGate()

        self.proof_tester = ProofTester(
            str(self.repo_path)
        )

        self.impact_analyzer = ImpactAnalyzer(
            str(self.repo_path)
        )

        self.patch_applier = PatchApplier()

    def repair(
        self,
        error_type: str,
        error_message: str,
        traceback: str
    ):

        # -------------------------------------------------
        # 1. ROOT CAUSE ANALYSIS
        # -------------------------------------------------

        root_cause = self.root_cause_analyzer.analyze(
            error_type,
            error_message,
            traceback
        )

        affected_file = root_cause["affected_file"]
        affected_line = root_cause["affected_line"]

        if not affected_file:
            return {
                "status": "FAILED",
                "stage": "ROOT_CAUSE_ANALYSIS",
                "reason": "Could not identify the affected file.",
                "root_cause": root_cause
            }

        if not affected_line:
            return {
                "status": "FAILED",
                "stage": "ROOT_CAUSE_ANALYSIS",
                "reason": "Could not identify the affected line.",
                "root_cause": root_cause
            }

        # -------------------------------------------------
        # 2. PATCH GENERATION
        # -------------------------------------------------

        if error_type != "KeyError":
            return {
                "status": "NO_PATCH",
                "stage": "PATCH_GENERATION",
                "reason": (
                    f"No automated patch strategy exists for "
                    f"{error_type}."
                ),
                "root_cause": root_cause
            }

        patch = self.patch_generator.generate_keyerror_patch(
            affected_file
        )

        # -------------------------------------------------
        # 3. LOAD SOURCE
        # -------------------------------------------------

        file_path = Path(affected_file)

        if not file_path.is_absolute():

            if (
                file_path.parts
                and file_path.parts[0] == self.repo_path.name
            ):
                source_path = file_path
            else:
                source_path = self.repo_path / file_path

        else:
            source_path = file_path

        try:
            surrounding_code = source_path.read_text(
                encoding="utf-8"
            )

        except Exception as error:
            return {
                "status": "FAILED",
                "stage": "SOURCE_LOADING",
                "reason": str(error),
                "root_cause": root_cause
            }

        # -------------------------------------------------
        # 4. REPAIR RISK GATE
        # -------------------------------------------------

        risk = self.risk_gate.assess(
            patch.old_code,
            patch.new_code,
            surrounding_code
        )

        if not risk.approved:
            return {
                "status": "BLOCKED",
                "stage": "RISK_GATE",
                "reason": (
                    "Repair was blocked because the risk gate "
                    "did not approve the proposed patch."
                ),
                "root_cause": root_cause,
                "patch": patch,
                "risk": risk
            }

        # -------------------------------------------------
        # 5. BEHAVIORAL PROOF
        # -------------------------------------------------

        proof = self.proof_tester.test_patch(
            patch.old_code,
            patch.new_code
        )

        if proof.get("status") != "PASS":
            return {
                "status": "REJECTED",
                "stage": "BEHAVIORAL_PROOF",
                "reason": (
                    "The proposed repair did not pass "
                    "behavioral validation."
                ),
                "root_cause": root_cause,
                "patch": patch,
                "risk": risk,
                "proof": proof
            }

        # -------------------------------------------------
        # 6. IMPACT / BLAST-RADIUS ANALYSIS
        # -------------------------------------------------

        impact = self.impact_analyzer.analyze(
            affected_file,
            affected_line
        )

        # -------------------------------------------------
        # 7. APPLY APPROVED PATCH
        # -------------------------------------------------

        apply_result = self.patch_applier.apply(
            patch.file_path,
            patch.old_code,
            patch.new_code
        )

        if apply_result.status != "PASS":
            return {
                "status": "APPLY_FAILED",
                "stage": "PATCH_APPLICATION",
                "reason": apply_result.message,
                "root_cause": root_cause,
                "patch": patch,
                "risk": risk,
                "proof": proof,
                "impact": impact,
                "apply_result": apply_result
            }

        # -------------------------------------------------
        # 8. FINAL REPAIR RESULT
        # -------------------------------------------------

        return {
            "status": "REPAIRED",
            "stage": "COMPLETED",

            "root_cause": root_cause,

            "patch": {
                "file_path": patch.file_path,
                "old_code": patch.old_code,
                "new_code": patch.new_code,
                "reason": patch.reason
            },

            "risk": {
                "score": risk.score,
                "level": risk.level,
                "approved": risk.approved,
                "reasons": risk.reasons
            },

            "proof": proof,

            "impact": {
                "affected_file": impact.affected_file,
                "affected_function": impact.affected_function,
                "affected_endpoint": impact.affected_endpoint,
                "dependencies": impact.dependencies,
                "blast_radius": impact.blast_radius,
                "risk_score": impact.risk_score
            },

            "apply_result": {
                "status": apply_result.status,
                "file_path": apply_result.file_path,
                "message": apply_result.message,
                "backup_path": apply_result.backup_path
            }
        }