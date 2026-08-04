from __future__ import annotations

from dataclasses import dataclass, field

from typing import Literal

@dataclass(slots=True)
class Variable:
    """
    Represents a JavaScript variable declaration.

    Example:

        const API_URL = "/api";
    """

    kind: str
    name: str
    value: str


@dataclass(slots=True)
class Function:
    """
    Represents a JavaScript function declaration.

    Example:

        function showToast(message) {
            console.log(message);
        }
    """

    name: str
    parameters: list[str] = field(default_factory=list)
    body: str = ""


@dataclass(slots=True)
class JavaScriptFile:
    """
    Represents one parsed JavaScript file.
    """

    filename: str

    variables: list[Variable] = field(default_factory=list)

    functions: list[Function] = field(default_factory=list)



@dataclass(slots=True)
class VariableConflict:
    """
    Same variable name, different value.
    """

    name: str
    first: Variable
    second: Variable


@dataclass(slots=True)
class FunctionDuplicate:
    """
    Same function name.
    """

    name: str
    first: Function
    second: Function


@dataclass(slots=True)
class ComparisonResult:
    """
    Result produced by Comparator.
    """

    unique_variables: list[Variable] = field(default_factory=list)

    variable_conflicts: list[VariableConflict] = field(default_factory=list)

    unique_functions: list[Function] = field(default_factory=list)

    duplicate_functions: list[FunctionDuplicate] = field(default_factory=list)


from enum import Enum


class MergeStrategy(str, Enum):
    PREFER_FIRST = "prefer_first"
    PREFER_LAST = "prefer_last"


@dataclass(slots=True)
class MergeResult:
    bundle: JavaScriptFile

    resolved_conflicts: list[VariableConflict] = field(
        default_factory=list
    )

    removed_duplicates: list[str] = field(
        default_factory=list
    )