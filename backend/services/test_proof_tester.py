from backend.services.patch_generator import MinimalPatchGenerator
from backend.services.proof_tester import ProofTester


generator = MinimalPatchGenerator()

patch = generator.generate_keyerror_patch(
    "demo_repo/app.py"
)

tester = ProofTester(
    "demo_repo"
)

result = tester.test_patch(
    patch.old_code,
    patch.new_code
)

print("\n=== REPAIRX BEHAVIORAL PROOF TEST ===")

print(f"Status: {result['status']}")
print(f"Reason: {result['reason']}")

if "valid_request" in result:
    print(f"Valid Request: {result['valid_request']}")

if "missing_user_request" in result:
    print(
        f"Missing User Request: "
        f"{result['missing_user_request']}"
    )