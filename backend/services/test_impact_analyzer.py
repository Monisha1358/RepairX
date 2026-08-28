from backend.services.impact_analyzer import ImpactAnalyzer


analyzer = ImpactAnalyzer(
    "demo_repo"
)

result = analyzer.analyze(
    "demo_repo/app.py",
    13
)

print("\n=== REPAIRX IMPACT ANALYSIS ===")

print(f"File:             {result.affected_file}")
print(f"Function:         {result.affected_function}")
print(f"Endpoint:         {result.affected_endpoint}")
print(f"Blast Radius:     {result.blast_radius}")
print(f"Risk Score:       {result.risk_score}/100")

print("\nDependencies:")

for dependency in result.dependencies:
    print(f"- {dependency}")