from __future__ import annotations

from js_bundler.models import (
    ComparisonEntry,
    ComparisonResult,
    ExportDeclaration,
    JavaScriptFile,
    Statement,
)


class Comparator:
    """
    Compares parsed JavaScript files.
    """

    def compare(self, files: list[JavaScriptFile]) -> ComparisonResult:
        result = ComparisonResult()

        import_index: dict[str, list[str]] = {}
        variable_index: dict[str, object] = {}
        function_index: dict[str, object] = {}
        arrow_function_index: dict[str, object] = {}
        object_index: dict[str, object] = {}
        array_index: dict[str, object] = {}
        class_index: dict[str, object] = {}
        statement_codes: set[str] = set()

        for file in files:
            for import_decl in file.imports:
                key = import_decl.module
                existing_imports = import_index.get(key)
                if existing_imports is None:
                    import_index[key] = list(import_decl.imported)
                    result.imports.append(
                        ComparisonEntry(
                            declaration_type="import",
                            status="unique",
                            first=import_decl,
                            winner=import_decl,
                        )
                    )
                else:
                    imported = [name for name in import_decl.imported if name not in existing_imports]
                    if imported:
                        existing_imports.extend(imported)
                        result.imports.append(
                            ComparisonEntry(
                                declaration_type="import",
                                status="conflict",
                                first=list(existing_imports),
                                second=import_decl,
                                winner=import_decl,
                            )
                        )
                    else:
                        result.imports.append(
                            ComparisonEntry(
                                declaration_type="import",
                                status="duplicate",
                                first=import_decl,
                                second=None,
                                winner=import_decl,
                            )
                        )

            for variable in file.variables:
                existing = variable_index.get(variable.name)
                if existing is None:
                    variable_index[variable.name] = variable
                    result.variables.append(
                        ComparisonEntry(
                            declaration_type="variable",
                            status="unique",
                            first=variable,
                            winner=variable,
                        )
                    )
                else:
                    if existing.value != variable.value or existing.kind != variable.kind:
                        result.variables.append(
                            ComparisonEntry(
                                declaration_type="variable",
                                status="conflict",
                                first=existing,
                                second=variable,
                                winner=variable,
                            )
                        )
                    else:
                        result.variables.append(
                            ComparisonEntry(
                                declaration_type="variable",
                                status="duplicate",
                                first=existing,
                                second=variable,
                                winner=existing,
                            )
                        )

            for function in file.functions:
                existing = function_index.get(function.name)
                if existing is None:
                    function_index[function.name] = function
                    result.functions.append(
                        ComparisonEntry(
                            declaration_type="function",
                            status="unique",
                            first=function,
                            winner=function,
                        )
                    )
                else:
                    status = "conflict" if existing.body != function.body else "duplicate"
                    result.functions.append(
                        ComparisonEntry(
                            declaration_type="function",
                            status=status,
                            first=existing,
                            second=function,
                            winner=existing,
                        )
                    )

            for arrow_function in file.arrow_functions:
                existing = arrow_function_index.get(arrow_function.name)
                if existing is None:
                    arrow_function_index[arrow_function.name] = arrow_function
                    result.arrow_functions.append(
                        ComparisonEntry(
                            declaration_type="arrow_function",
                            status="unique",
                            first=arrow_function,
                            winner=arrow_function,
                        )
                    )
                else:
                    status = "conflict" if existing.body != arrow_function.body else "duplicate"
                    result.arrow_functions.append(
                        ComparisonEntry(
                            declaration_type="arrow_function",
                            status=status,
                            first=existing,
                            second=arrow_function,
                            winner=existing,
                        )
                    )

            for obj in file.objects:
                existing = object_index.get(obj.name)
                if existing is None:
                    object_index[obj.name] = obj
                    result.objects.append(
                        ComparisonEntry(
                            declaration_type="object",
                            status="unique",
                            first=obj,
                            winner=obj,
                        )
                    )
                else:
                    status = "conflict" if existing.properties != obj.properties else "duplicate"
                    result.objects.append(
                        ComparisonEntry(
                            declaration_type="object",
                            status=status,
                            first=existing,
                            second=obj,
                            winner=existing,
                        )
                    )

            for array in file.arrays:
                existing = array_index.get(array.name)
                if existing is None:
                    array_index[array.name] = array
                    result.arrays.append(
                        ComparisonEntry(
                            declaration_type="array",
                            status="unique",
                            first=array,
                            winner=array,
                        )
                    )
                else:
                    status = "conflict" if existing.elements != array.elements else "duplicate"
                    result.arrays.append(
                        ComparisonEntry(
                            declaration_type="array",
                            status=status,
                            first=existing,
                            second=array,
                            winner=existing,
                        )
                    )

            for cls in file.classes:
                existing = class_index.get(cls.name)
                if existing is None:
                    class_index[cls.name] = cls
                    result.classes.append(
                        ComparisonEntry(
                            declaration_type="class",
                            status="unique",
                            first=cls,
                            winner=cls,
                        )
                    )
                else:
                    status = "conflict" if existing.methods != cls.methods else "duplicate"
                    result.classes.append(
                        ComparisonEntry(
                            declaration_type="class",
                            status=status,
                            first=existing,
                            second=cls,
                            winner=existing,
                        )
                    )

            for statement in file.statements:
                if statement.code not in statement_codes:
                    statement_codes.add(statement.code)
                    result.statements.append(statement)

            for export in file.exports:
                if isinstance(export, ExportDeclaration):
                    result.exports.append(export)

        return result