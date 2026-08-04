from __future__ import annotations

from js_bundler.models import (
    ComparisonResult,
    FunctionDuplicate,
    JavaScriptFile,
    VariableConflict,
)


class Comparator:

    """
    Compares parsed JavaScript files.
    """

    def compare(
        self,
        files: list[JavaScriptFile],
    ) -> ComparisonResult:

        result = ComparisonResult()

        variable_index = {}

        function_index = {}

        for file in files:

            # -------------------------
            # Variables
            # -------------------------

            for variable in file.variables:

                if variable.name not in variable_index:

                    variable_index[variable.name] = variable

                    result.unique_variables.append(variable)

                else:

                    existing = variable_index[variable.name]

                    if existing.value != variable.value:

                        result.variable_conflicts.append(

                            VariableConflict(

                                name=variable.name,

                                first=existing,

                                second=variable,
                            )
                        )

            # -------------------------
            # Functions
            # -------------------------

            for function in file.functions:

                if function.name not in function_index:

                    function_index[function.name] = function

                    result.unique_functions.append(function)

                else:

                    result.duplicate_functions.append(

                        FunctionDuplicate(

                            name=function.name,

                            first=function_index[function.name],

                            second=function,
                        )
                    )

        return result