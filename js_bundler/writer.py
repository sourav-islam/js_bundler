from __future__ import annotations

from pathlib import Path
from typing import Any

from js_bundler.merger import MergeResult
from js_bundler.models import (
    ArrayDeclaration,
    ArrowFunction,
    ClassDeclaration,
    ComparisonResult,
    ExportDeclaration,
    Function,
    ImportDeclaration,
    JavaScriptFile,
    ObjectDeclaration,
    Statement,
    Variable,
)
from js_bundler.utils import ensure_directory, write_file


def _count_status(entries: list[object], status: str) -> int:
    return sum(1 for entry in entries if getattr(entry, "status", None) == status)


class BundleWriter:
    """
    Writes the bundled JavaScript file and report to disk.
    """

    def write_bundle(
        self,
        files: list[JavaScriptFile],
        comparison: ComparisonResult,
        result: MergeResult,
        output_dir: Path,
    ) -> dict[str, str]:
        ensure_directory(output_dir)

        bundle_path = output_dir / "bundle.js"
        report_path = output_dir / "report.txt"

        bundle_content = self._build_bundle(result.bundle)
        report_content = self._build_report(
            files, comparison, result, bundle_path, report_path
        )

        write_file(bundle_path, bundle_content)
        write_file(report_path, report_content)

        return {
            "bundle": str(bundle_path),
            "report": str(report_path),
        }

    def _build_bundle(self, bundle: JavaScriptFile) -> str:
        sections: list[str] = []

        if bundle.imports:
            sections.append(self._build_imports(bundle.imports))

        if bundle.variables:
            sections.append(self._build_variables(bundle.variables))

        if bundle.objects:
            sections.append(self._build_objects(bundle.objects))

        if bundle.arrays:
            sections.append(self._build_arrays(bundle.arrays))

        if bundle.functions:
            sections.append(self._build_functions(bundle.functions))

        if bundle.arrow_functions:
            sections.append(self._build_arrow_functions(bundle.arrow_functions))

        if bundle.classes:
            sections.append(self._build_classes(bundle.classes))

        if bundle.statements:
            sections.append(self._build_statements(bundle.statements))

        if bundle.exports:
            sections.append(self._build_exports(bundle.exports))

        return "\n\n".join(sections).rstrip() + "\n"

    def _build_imports(self, imports: list[ImportDeclaration]) -> str:
        lines: list[str] = []

        for import_decl in imports:
            imported = ", ".join(import_decl.imported)
            lines.append(f"import {{ {imported} }} from \"{import_decl.module}\";")

        return "\n".join(lines)

    def _build_variables(self, variables: list[Variable]) -> str:
        lines: list[str] = []
        for variable in variables:
            lines.append(f"{variable.kind} {variable.name} = {variable.value};")
        return "\n".join(lines)

    def _build_objects(self, objects: list[ObjectDeclaration]) -> str:
        lines: list[str] = []
        for obj in objects:
            properties = ",\n    ".join(
                f"{key}: {value}" for key, value in obj.properties.items()
            )
            lines.append(
                f"const {obj.name} = {{\n    {properties}\n}};"
            )
        return "\n\n".join(lines)

    def _build_arrays(self, arrays: list[ArrayDeclaration]) -> str:
        lines: list[str] = []
        for array in arrays:
            elements = ", ".join(array.elements)
            lines.append(f"const {array.name} = [{elements}];")
        return "\n".join(lines)

    def _build_functions(self, functions: list[Function]) -> str:
        lines: list[str] = []
        for function in functions:
            lines.append(
                f"function {function.name}({', '.join(function.parameters)}) {function.body}"
            )
        return "\n\n".join(lines)

    def _build_arrow_functions(self, arrow_functions: list[ArrowFunction]) -> str:
        lines: list[str] = []
        for arrow_function in arrow_functions:
            lines.append(
                f"const {arrow_function.name} = ({', '.join(arrow_function.parameters)}) => {arrow_function.body};"
            )
        return "\n".join(lines)

    def _build_classes(self, classes: list[ClassDeclaration]) -> str:
        lines: list[str] = []
        for cls in classes:
            methods = []
            for method in cls.methods:
                methods.append(
                    f"    {method.name}({', '.join(method.parameters)}) {method.body}"
                )
            lines.append(
                f"class {cls.name} {{\n{chr(10).join(methods)}\n}}"
            )
        return "\n\n".join(lines)

    def _build_statements(self, statements: list[Statement]) -> str:
        return "\n".join(statement.code for statement in statements)

    def _build_exports(self, exports: list[ExportDeclaration]) -> str:
        lines: list[str] = []
        for export in exports:
            if export.is_default and export.exported:
                lines.append(f"export default {export.exported[0]};")
            elif export.exported:
                lines.append(f"export {{ {', '.join(export.exported)} }};")
        return "\n".join(lines)

    def _build_report(
        self,
        files: list[JavaScriptFile],
        comparison: ComparisonResult,
        result: MergeResult,
        bundle_path: Path,
        report_path: Path,
    ) -> str:
        lines: list[str] = [
            "Bundle Report",
            "=" * 60,
            f"Input files: {len(files)}",
            f"Bundle file: {result.bundle.filename}",
            "",
            "Comparison Summary",
            "-" * 60,
            f"Imports compared: {len(comparison.imports)}",
            f"Variables compared: {len(comparison.variables)}",
            f"Functions compared: {len(comparison.functions)}",
            f"Arrow functions compared: {len(comparison.arrow_functions)}",
            f"Objects compared: {len(comparison.objects)}",
            f"Arrays compared: {len(comparison.arrays)}",
            f"Classes compared: {len(comparison.classes)}",
            f"Statements compared: {len(comparison.statements)}",
            f"Exports compared: {len(comparison.exports)}",
            f"Conflicts found: {self._count_conflicts(comparison)}",
            f"Duplicate entries detected: {self._count_duplicates(comparison)}",
            "",
            "Bundle Summary",
            "-" * 60,
            f"Bundle file: {bundle_path}",
            f"Report file: {report_path}",
            f"Variables in bundle: {len(result.bundle.variables)}",
            f"Functions in bundle: {len(result.bundle.functions)}",
            f"Arrow functions in bundle: {len(result.bundle.arrow_functions)}",
            f"Classes in bundle: {len(result.bundle.classes)}",
            "",
        ]

        if result.resolved_conflicts:
            lines.append("Resolved conflicts:")
            for conflict in result.resolved_conflicts:
                lines.append(f"  - {conflict}")
            lines.append("")

        if result.removed_duplicates:
            lines.append("Removed duplicates:")
            for duplicate in result.removed_duplicates:
                lines.append(f"  - {duplicate}")
            lines.append("")

        lines.append("Files included:")
        for file in files:
            lines.append(f"  - {file.filename}")

        return "\n".join(lines) + "\n"

    def _count_conflicts(self, comparison: ComparisonResult) -> int:
        return sum(
            _count_status(entries, "conflict")
            for entries in (
                comparison.variables,
                comparison.functions,
                comparison.arrow_functions,
                comparison.objects,
                comparison.arrays,
                comparison.classes,
            )
        )

    def _count_duplicates(self, comparison: ComparisonResult) -> int:
        return sum(
            _count_status(entries, "duplicate")
            for entries in (
                comparison.variables,
                comparison.functions,
                comparison.arrow_functions,
                comparison.objects,
                comparison.arrays,
                comparison.classes,
            )
        )
