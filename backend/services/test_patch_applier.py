from backend.services.patch_generator import MinimalPatchGenerator
from backend.services.patch_applier import PatchApplier


generator = MinimalPatchGenerator()
applier = PatchApplier()

file_path = "demo_repo/app.py"

patch = generator.generate_keyerror_patch(
    file_path
)

result = applier.apply(
    patch.file_path,
    patch.old_code,
    patch.new_code
)

print("\n=== REPAIRX PATCH APPLIER ===")
print(f"Status: {result.status}")
print(f"File: {result.file_path}")
print(f"Message: {result.message}")
print(f"Backup: {result.backup_path}")