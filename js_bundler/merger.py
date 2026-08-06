from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import PurePosixPath
from typing import Any

from js_bundler.models import (
    ArrowFunction,
    ArrayDeclaration,
    ClassDeclaration,
    Function,
    ImportDeclaration,
    JavaScriptFile,
    ObjectDeclaration,
    ExportDeclaration,
    Statement,
    Variable,
)


class MergeStrategy:
    PREFER_FIRST = "prefer_first"
    PREFER_LAST = "prefer_last"
    PREFER_LONGEST = "prefer_longest"


@dataclass(slots=True)
class MergeResult:
    bundle: JavaScriptFile
    resolved_conflicts: list[str] = field(default_factory=list)
    removed_duplicates: list[str] = field(default_factory=list)


class Merger:
    """
    Merges multiple parsed JavaScript files into one bundle.
    """

    def merge(
        self,
        files: list[JavaScriptFile],
        strategy: str = MergeStrategy.PREFER_FIRST,
    ) -> MergeResult:

        import_map: dict[str, set[str]] = {}
        import_order: list[str] = []
        variable_map: dict[str, Variable] = {}
        function_map: dict[str, Function] = {}
        arrow_function_map: dict[str, ArrowFunction] = {}
        object_map: dict[str, ObjectDeclaration] = {}
        array_map: dict[str, ArrayDeclaration] = {}
        class_map: dict[str, ClassDeclaration] = {}
        export_map: dict[str, ExportDeclaration] = {}
        statements: list[Statement] = []

        resolved_conflicts: list[str] = []
        removed_duplicates: list[str] = []

        # Filenames of every file being bundled together, e.g. {"global.js",
        # "home.js", "product.js"}. An import like `import { showToast } from
        # "./global.js"` is only safe to keep if "./global.js" points outside
        # the bundle; if it points at a sibling file that is itself being
        # merged in, that name is already declared locally in the bundle and
        # keeping the import would redeclare it (a SyntaxError).
        bundled_filenames = {file.filename for file in files}

        for file in files:
            for import_decl in file.imports:
                if PurePosixPath(import_decl.module).name in bundled_filenames:
                    continue

                if import_decl.module not in import_map:
                    import_map[import_decl.module] = set(import_decl.imported)
                    import_order.append(import_decl.module)
                else:
                    import_map[import_decl.module].update(import_decl.imported)

            for variable in file.variables:
                existing = variable_map.get(variable.name)
                if existing is None:
                    variable_map[variable.name] = variable
                    continue

                if existing.value != variable.value or existing.kind != variable.kind:
                    chosen = self._choose_variable(existing, variable, strategy)
                    if chosen is variable:
                        variable_map.pop(variable.name, None)
                        variable_map[variable.name] = variable
                    resolved_conflicts.append(variable.name)
                else:
                    removed_duplicates.append(variable.name)

            for function in file.functions:
                existing = function_map.get(function.name)
                if existing is None:
                    function_map[function.name] = function
                    continue

                chosen = self._choose_declaration(existing, function, strategy)
                if chosen is function:
                    function_map.pop(function.name, None)
                    function_map[function.name] = function
                if existing.body != function.body:
                    resolved_conflicts.append(function.name)
                else:
                    removed_duplicates.append(function.name)

            for arrow_function in file.arrow_functions:
                existing = arrow_function_map.get(arrow_function.name)
                if existing is None:
                    arrow_function_map[arrow_function.name] = arrow_function
                    continue

                chosen = self._choose_declaration(existing, arrow_function, strategy)
                if chosen is arrow_function:
                    arrow_function_map.pop(arrow_function.name, None)
                    arrow_function_map[arrow_function.name] = arrow_function
                if existing.body != arrow_function.body:
                    resolved_conflicts.append(arrow_function.name)
                else:
                    removed_duplicates.append(arrow_function.name)

            for obj in file.objects:
                existing = object_map.get(obj.name)
                if existing is None:
                    object_map[obj.name] = obj
                    continue

                chosen = self._choose_declaration(existing, obj, strategy)
                if chosen is obj:
                    object_map.pop(obj.name, None)
                    object_map[obj.name] = obj
                if existing.properties != obj.properties:
                    resolved_conflicts.append(obj.name)
                else:
                    removed_duplicates.append(obj.name)

            for array in file.arrays:
                existing = array_map.get(array.name)
                if existing is None:
                    array_map[array.name] = array
                    continue

                chosen = self._choose_declaration(existing, array, strategy)
                if chosen is array:
                    array_map.pop(array.name, None)
                    array_map[array.name] = array
                if existing.elements != array.elements:
                    resolved_conflicts.append(array.name)
                else:
                    removed_duplicates.append(array.name)

            for cls in file.classes:
                existing = class_map.get(cls.name)
                if existing is None:
                    class_map[cls.name] = cls
                    continue

                chosen = self._choose_declaration(existing, cls, strategy)
                if chosen is cls:
                    class_map.pop(cls.name, None)
                    class_map[cls.name] = cls
                if existing.methods != cls.methods:
                    resolved_conflicts.append(cls.name)
                else:
                    removed_duplicates.append(cls.name)

            for statement in file.statements:
                statements.append(statement)

            for export in file.exports:
                key = "default" if export.is_default else ",".join(export.exported)
                export_map[key] = export

        bundled_imports = [
            ImportDeclaration(
                module=module,
                imported=sorted(import_map[module]),
                source_file="bundle.js",
                order=index + 1,
            )
            for index, module in enumerate(import_order)
        ]

        bundle = JavaScriptFile(
            filename="bundle.js",
            imports=bundled_imports,
            variables=list(variable_map.values()),
            objects=list(object_map.values()),
            arrays=list(array_map.values()),
            functions=list(function_map.values()),
            arrow_functions=list(arrow_function_map.values()),
            classes=list(class_map.values()),
            statements=statements,
            exports=list(export_map.values()),
        )

        return MergeResult(
            bundle=bundle,
            resolved_conflicts=sorted(set(resolved_conflicts)),
            removed_duplicates=sorted(set(removed_duplicates)),
        )

    def _choose_variable(
        self,
        existing: Variable,
        candidate: Variable,
        strategy: str,
    ) -> Variable:
        if strategy == MergeStrategy.PREFER_LAST:
            return candidate
        if strategy == MergeStrategy.PREFER_FIRST:
            return existing
        if strategy == MergeStrategy.PREFER_LONGEST:
            return candidate if len(candidate.value) > len(existing.value) else existing
        return candidate

    def _choose_declaration(
        self,
        existing: Any,
        candidate: Any,
        strategy: str,
    ) -> Any:
        if strategy == MergeStrategy.PREFER_LAST:
            return candidate
        if strategy == MergeStrategy.PREFER_FIRST:
            return existing
        if strategy == MergeStrategy.PREFER_LONGEST:
            return candidate if self._declaration_size(candidate) > self._declaration_size(existing) else existing
        return candidate

    def _declaration_size(self, declaration: Any) -> int:
        if isinstance(declaration, Variable):
            return len(declaration.value)
        if isinstance(declaration, Function) or isinstance(declaration, ArrowFunction):
            return len(declaration.body)
        if isinstance(declaration, ObjectDeclaration):
            return sum(len(key) + len(value) for key, value in declaration.properties.items())
        if isinstance(declaration, ArrayDeclaration):
            return sum(len(element) for element in declaration.elements)
        if isinstance(declaration, ClassDeclaration):
            return sum(len(method.name) + len(method.body) for method in declaration.methods)
        return 0