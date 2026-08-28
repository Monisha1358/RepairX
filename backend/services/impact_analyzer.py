import ast
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ImpactReport:
    affected_file: str
    affected_function: str
    affected_endpoint: str
    dependencies: list[str]
    blast_radius: str
    risk_score: int


class ImpactAnalyzer:

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def analyze(self, file_path: str, line_number: int):

        path = Path(file_path)

        # If the supplied path already contains the repository
        # directory, don't add it again.
        if not path.is_absolute():

            if path.parts and path.parts[0] == self.repo_path.name:
                path = Path(*path.parts)

            else:
                path = self.repo_path / path

        source = path.read_text(
            encoding="utf-8"
        )

        tree = ast.parse(source)

        affected_function = "Unknown"
        dependencies = []

        for node in ast.walk(tree):

            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
            ):

                start = node.lineno
                end = getattr(
                    node,
                    "end_lineno",
                    start
                )

                if start <= line_number <= end:

                    affected_function = node.name

                    for child in ast.walk(node):

                        if isinstance(
                            child,
                            ast.Name
                        ):
                            dependencies.append(
                                child.id
                            )

                    break

        dependencies = sorted(
            set(dependencies)
        )

        endpoint = self._find_endpoint(
            tree,
            affected_function
        )

        dependency_count = len(
            dependencies
        )

        if dependency_count <= 5:
            blast_radius = "LOW"
            risk_score = 20

        elif dependency_count <= 10:
            blast_radius = "MEDIUM"
            risk_score = 50

        else:
            blast_radius = "HIGH"
            risk_score = 80

        return ImpactReport(
            affected_file=str(path),
            affected_function=affected_function,
            affected_endpoint=endpoint,
            dependencies=dependencies,
            blast_radius=blast_radius,
            risk_score=risk_score
        )

    def _find_endpoint(
        self,
        tree,
        function_name: str
    ):

        for node in ast.walk(tree):

            if not isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
            ):
                continue

            if node.name != function_name:
                continue

            for decorator in node.decorator_list:

                if not isinstance(
                    decorator,
                    ast.Call
                ):
                    continue

                if not isinstance(
                    decorator.func,
                    ast.Attribute
                ):
                    continue

                if decorator.func.attr not in {
                    "get",
                    "post",
                    "put",
                    "delete",
                    "patch"
                }:
                    continue

                if not decorator.args:
                    continue

                value = decorator.args[0]

                if isinstance(
                    value,
                    ast.Constant
                ):
                    return str(value.value)

        return "Not detected"