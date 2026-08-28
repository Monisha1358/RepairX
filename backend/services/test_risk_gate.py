from backend.services.risk_gate import RepairRiskGate
from backend.services.patch_generator import MinimalPatchGenerator


generator = MinimalPatchGenerator()
gate = RepairRiskGate()

patch = generator.generate_keyerror_patch(
    "demo_repo/app.py"
)

surrounding_code = """
users = {
    1: "Monisha",
    2: "RepairX"
}

username = users.get(user_id)

if username is None:
    return {"error": "User not found"}

return {
    "user": username.upper()
}
"""

result = gate.assess(
    patch.old_code,
    patch.new_code,
    surrounding_code
)

print("\n=== REPAIRX REPAIR RISK GATE ===")
print(f"Risk Score: {result.score}/100")
print(f"Risk Level: {result.level}")
print(f"Approved:   {result.approved}")

print("\nReasons:")
for reason in result.reasons:
    print(f"- {reason}")
    