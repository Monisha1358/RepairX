from backend.services.patch_generator import MinimalPatchGenerator


generator = MinimalPatchGenerator()

patch = generator.generate_keyerror_patch(
    "demo_repo/app.py"
)

print("\n=== REPAIRX MINIMAL PATCH ===")
print(f"File: {patch.file_path}")

print("\nOLD CODE:")
print(patch.old_code)

print("\nNEW CODE:")
print(patch.new_code)

print("\nREASON:")
print(patch.reason)