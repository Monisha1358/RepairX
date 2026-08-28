from backend.services.root_cause_analyzer import RootCauseAnalyzer


traceback = """File "C:\\Users\\DELL ADMIN\\RepairX\\demo_repo\\app.py", line 13, in get_user
    username = users[user_id]
KeyError: 99"""


analyzer = RootCauseAnalyzer("demo_repo")

result = analyzer.analyze(
    error_type="KeyError",
    error_message="99",
    traceback=traceback
)

print("\n=== REPAIRX ROOT-CAUSE INVESTIGATION ===")
print(f"Error Type:      {result['error_type']}")
print(f"Error Message:   {result['error_message']}")
print(f"Affected File:   {result['affected_file']}")
print(f"Affected Line:   {result['affected_line']}")
print(f"Root Cause:      {result['root_cause']}")
print(f"Confidence:      {result['confidence']}")