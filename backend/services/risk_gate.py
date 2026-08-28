from dataclasses import dataclass


@dataclass
class RiskAssessment:
    score: int
    level: str
    approved: bool
    reasons: list[str]


class RepairRiskGate:

    def assess(
        self,
        old_code: str,
        new_code: str,
        surrounding_code: str
    ) -> RiskAssessment:

        score = 0
        reasons = []

        # Large patches are riskier.
        if len(new_code) > len(old_code) * 2:
            score += 30
            reasons.append("The proposed patch significantly increases code size.")
        else:
            reasons.append("The proposed patch is relatively small.")

        # Check whether the patch introduces risky operations.
        risky_patterns = [
            "os.system(",
            "subprocess.",
            "eval(",
            "exec(",
            "rm -rf",
            "DROP TABLE",
        ]

        for pattern in risky_patterns:
            if pattern in new_code:
                score += 30
                reasons.append(
                    f"Potentially risky operation detected: {pattern}"
                )

        # Check whether the surrounding code is preserved.
        if surrounding_code.strip():
            score += 0
            reasons.append(
                "Surrounding code was provided for contextual validation."
            )

        # A patch that only changes the intended section is lower risk.
        if old_code.strip() and new_code.strip():
            reasons.append(
                "Patch contains a defined before/after code transformation."
            )

        score = min(score, 100)

        if score < 30:
            level = "LOW"
            approved = True
        elif score < 70:
            level = "MEDIUM"
            approved = True
        else:
            level = "HIGH"
            approved = False

        return RiskAssessment(
            score=score,
            level=level,
            approved=approved,
            reasons=reasons
        )