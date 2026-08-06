from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# =============================================================================
# Base Declaration
# =============================================================================


@dataclass(slots=True)
class BaseDeclaration:
    """
    Base class for all named JavaScript declarations.
    """

    name: str
    source_file: str
    order: int


# =============================================================================
# Imports / Exports
# =============================================================================


@dataclass(slots=True)
class ImportDeclaration:
    """
    import { api } from "./api.js"
    """

    module: str
    imported: list[str]
    source_file: str
    order: int


@dataclass(slots=True)
class ExportDeclaration:
    """
    export { showToast }
    export default UserService
    """

    exported: list[str]
    is_default: bool
    source_file: str
    order: int


# =============================================================================
# Variables
# =============================================================================


@dataclass(slots=True)
class Variable(BaseDeclaration):
    """
    const API_URL = "/api"
    """

    kind: str
    value: str


# =============================================================================
# Objects
# =============================================================================


@dataclass(slots=True)
class ObjectDeclaration(BaseDeclaration):
    """
    const config = { ... }
    """

    properties: dict[str, str]


# =============================================================================
# Arrays
# =============================================================================


@dataclass(slots=True)
class ArrayDeclaration(BaseDeclaration):
    """
    const roles = [...]
    """

    elements: list[str]


# =============================================================================
# Functions
# =============================================================================


@dataclass(slots=True)
class Function(BaseDeclaration):
    """
    function showToast() {}
    """

    parameters: list[str] = field(default_factory=list)
    body: str = ""


@dataclass(slots=True)
class ArrowFunction(BaseDeclaration):
    """
    const formatPrice = () => {}
    """

    parameters: list[str] = field(default_factory=list)
    body: str = ""


# =============================================================================
# Classes
# =============================================================================


@dataclass(slots=True)
class Method:
    """
    Class method.
    """

    name: str
    parameters: list[str] = field(default_factory=list)
    body: str = ""


@dataclass(slots=True)
class ClassDeclaration(BaseDeclaration):
    """
    class UserService {}
    """

    methods: list[Method] = field(default_factory=list)


# =============================================================================
# Statements
# =============================================================================


@dataclass(slots=True)
class Statement:
    """
    Executable statements that must preserve order.
    """

    statement_type: str
    code: str
    source_file: str
    order: int


# =============================================================================
# JavaScript File
# =============================================================================


@dataclass(slots=True)
class JavaScriptFile:
    """
    Internal representation of one JavaScript source file.
    """

    filename: str

    imports: list[ImportDeclaration] = field(default_factory=list)

    variables: list[Variable] = field(default_factory=list)

    objects: list[ObjectDeclaration] = field(default_factory=list)

    arrays: list[ArrayDeclaration] = field(default_factory=list)

    functions: list[Function] = field(default_factory=list)

    arrow_functions: list[ArrowFunction] = field(default_factory=list)

    classes: list[ClassDeclaration] = field(default_factory=list)

    statements: list[Statement] = field(default_factory=list)

    exports: list[ExportDeclaration] = field(default_factory=list)


# =============================================================================
# Comparator Models
# =============================================================================


@dataclass(slots=True)
class ComparisonEntry:
    """
    Represents one comparison result.
    """

    declaration_type: str

    status: str

    first: Any | None = None

    second: Any | None = None

    winner: Any | None = None


@dataclass(slots=True)
class ComparisonResult:
    """
    Output of Comparator.
    """

    imports: list[ComparisonEntry] = field(default_factory=list)

    variables: list[ComparisonEntry] = field(default_factory=list)

    objects: list[ComparisonEntry] = field(default_factory=list)

    arrays: list[ComparisonEntry] = field(default_factory=list)

    functions: list[ComparisonEntry] = field(default_factory=list)

    arrow_functions: list[ComparisonEntry] = field(default_factory=list)

    classes: list[ComparisonEntry] = field(default_factory=list)

    statements: list[Statement] = field(default_factory=list)

    exports: list[ExportDeclaration] = field(default_factory=list)