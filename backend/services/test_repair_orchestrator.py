from backend.services.repair_orchestrator import RepairOrchestrator


orchestrator = RepairOrchestrator(
    "demo_repo"
)


traceback = '''Traceback (most recent call last):
  File "demo_repo/app.py", line 17, in get_user
    username = users[user_id]
KeyError: 99
'''


result = orchestrator.repair(
    error_type="KeyError",
    error_message="99",
    traceback=traceback
)


print("\n=== REPAIRX REPAIR ORCHESTRATOR ===")

print(f"\nStatus: {result['status']}")
print(f"Stage: {result['stage']}")

if "root_cause" in result:

    root_cause = result["root_cause"]

    print("\n--- ROOT CAUSE ---")
    print(
        f"Affected File: "
        f"{root_cause.get('affected_file')}"
    )

    print(
        f"Affected Line: "
        f"{root_cause.get('affected_line')}"
    )

    print(
        f"Root Cause: "
        f"{root_cause.get('root_cause')}"
    )

    print(
        f"Confidence: "
        f"{root_cause.get('confidence')}"
    )


if "patch" in result:

    patch = result["patch"]

    print("\n--- PATCH ---")

    print(
        f"File: {getattr(patch, 'file_path', None)}"
    )

    print(
        f"Reason: {getattr(patch, 'reason', None)}"
    )


if "risk" in result:

    risk = result["risk"]

    print("\n--- RISK GATE ---")

    print(
        f"Risk Score: "
        f"{getattr(risk, 'score', None)}/100"
    )

    print(
        f"Risk Level: "
        f"{getattr(risk, 'level', None)}"
    )

    print(
        f"Approved: "
        f"{getattr(risk, 'approved', None)}"
    )


if "proof" in result:

    proof = result["proof"]

    print("\n--- BEHAVIORAL PROOF ---")
    print(
        f"Status: "
        f"{proof.get('status')}"
    )

    print(
        f"Reason: "
        f"{proof.get('reason')}"
    )


if "impact" in result:

    impact = result["impact"]

    print("\n--- IMPACT ANALYSIS ---")

    print(
        f"Function: "
        f"{impact.get('affected_function')}"
    )

    print(
        f"Endpoint: "
        f"{impact.get('affected_endpoint')}"
    )

    print(
        f"Blast Radius: "
        f"{impact.get('blast_radius')}"
    )

    print(
        f"Impact Risk: "
        f"{impact.get('risk_score')}/100"
    )

    print(
        f"Dependencies: "
        f"{impact.get('dependencies')}"
    )