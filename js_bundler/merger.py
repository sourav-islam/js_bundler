from __future__ import annotations

from js_bundler.models import (
    Function,
    JavaScriptFile,
    MergeResult,
    MergeStrategy,
    Variable,
)


class Merger:
    """
    Merges multiple parsed JavaScript files into one bundle.
    """

    def merge(
        self,
        files: list[JavaScriptFile],
        strategy: MergeStrategy = MergeStrategy.PREFER_LAST,
    ) -> MergeResult:

        variable_map: dict[str, Variable] = {}
        function_map: dict[str, Function] = {}

        resolved_conflicts = []
        removed_duplicates = []

        for file in files:

            #
            # Variables
            #

            for variable in file.variables:

                existing = variable_map.get(variable.name)

                if existing is None:

                    variable_map[variable.name] = variable
                    continue

                if existing.value != variable.value:

                    if strategy == MergeStrategy.PREFER_LAST:

                        variable_map[variable.name] = variable

                    resolved_conflicts.append(variable.name)

            #
            # Functions
            #

            for function in file.functions:

                if function.name in function_map:

                    removed_duplicates.append(function.name)
                    continue

                function_map[function.name] = function

        bundle = JavaScriptFile(
            filename="bundle.js",
            variables=list(variable_map.values()),
            functions=list(function_map.values()),
        )

        return MergeResult(
            bundle=bundle,
            resolved_conflicts=resolved_conflicts,
            removed_duplicates=removed_duplicates,
        )