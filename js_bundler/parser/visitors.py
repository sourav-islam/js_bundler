from __future__ import annotations

from tree_sitter import Node

from js_bundler.models import (
    ArrayDeclaration,
    ArrowFunction,
    ClassDeclaration,
    ExportDeclaration,
    Function,
    ImportDeclaration,
    Method,
    ObjectDeclaration,
    Statement,
    Variable,
)


class ImportVisitor:
    def __init__(
        self,
        node: Node,
        source: str,
        filename: str,
        order: int,
    ) -> None:
        self._node = node
        self._source = source
        self._filename = filename
        self._order = order

    def visit(self) -> ImportDeclaration | None:
        module = ""
        imported: list[str] = []

        for child in self._node.children:
            if child.type == "string":
                module = self._text(child)
            elif child.type == "import_clause":
                imported.extend(self._collect_import_clause_names(child))

        return ImportDeclaration(
            module=module,
            imported=imported,
            source_file=self._filename,
            order=self._order,
        )

    def _collect_import_clause_names(self, node: Node) -> list[str]:
        names: list[str] = []

        for child in node.children:
            if child.type == "identifier":
                names.append(self._text(child))

            elif child.type == "named_imports":
                for spec in child.children:
                    if spec.type != "import_specifier":
                        continue

                    name_node = spec.child_by_field_name("name")
                    if name_node is not None:
                        names.append(self._text(name_node))

            elif child.type == "namespace_import":
                name_node = child.child_by_field_name("name")
                if name_node is not None:
                    names.append(self._text(name_node))

        return names

    def _text(self, node: Node | None) -> str:
        if node is None:
            return ""
        return self._source[node.start_byte:node.end_byte]


class ExportVisitor:
    def __init__(
        self,
        node: Node,
        source: str,
        filename: str,
        order: int,
    ) -> None:
        self._node = node
        self._source = source
        self._filename = filename
        self._order = order

    def visit(self) -> ExportDeclaration | None:
        exported: list[str] = []
        is_default = False

        for child in self._node.children:
            if child.type == "identifier":
                if self._text(child) == "default":
                    is_default = True
                else:
                    exported.append(self._text(child))

            elif child.type == "named_exports":
                for spec in child.children:
                    if spec.type != "export_specifier":
                        continue

                    name_node = spec.child_by_field_name("name")
                    if name_node is not None:
                        exported.append(self._text(name_node))

            elif child.type == "export_clause":
                for spec in child.children:
                    if spec.type != "export_specifier":
                        continue

                    name_node = spec.child_by_field_name("name")
                    if name_node is not None:
                        exported.append(self._text(name_node))

        return ExportDeclaration(
            exported=exported,
            is_default=is_default,
            source_file=self._filename,
            order=self._order,
        )

    def _text(self, node: Node | None) -> str:
        if node is None:
            return ""
        return self._source[node.start_byte:node.end_byte]


class VariableVisitor:
    def __init__(
        self,
        node: Node,
        source: str,
        filename: str,
        order: int,
    ) -> None:
        self._node = node
        self._source = source
        self._filename = filename
        self._order = order

    def visit(self) -> Variable | None:
        name_node = self._node.child_by_field_name("name")
        value_node = self._node.child_by_field_name("value")

        if name_node is None:
            return None

        kind = self._declaration_kind()

        return Variable(
            name=self._text(name_node),
            source_file=self._filename,
            order=self._order,
            kind=kind,
            value=self._text(value_node),
        )

    def _declaration_kind(self) -> str:
        parent = self._node.parent

        if parent is not None:
            kind_node = parent.child_by_field_name("kind")

            if kind_node is not None:
                return self._text(kind_node)

            if parent.type in {"lexical_declaration", "variable_declaration"}:
                for child in parent.children:
                    if child.type in {"const", "let", "var"}:
                        return self._text(child)

        return "var"

    def _text(self, node: Node | None) -> str:
        if node is None:
            return ""
        return self._source[node.start_byte:node.end_byte]


class FunctionVisitor:
    def __init__(
        self,
        node: Node,
        source: str,
        filename: str,
        order: int,
    ) -> None:
        self._node = node
        self._source = source
        self._filename = filename
        self._order = order

    def visit(self) -> Function | None:
        name_node = self._node.child_by_field_name("name")
        parameter_node = self._node.child_by_field_name("parameters")
        body_node = self._node.child_by_field_name("body")

        parameters: list[str] = []

        if parameter_node is not None:
            for child in parameter_node.children:
                if child.type == "identifier":
                    parameters.append(self._text(child))

        return Function(
            name=self._text(name_node),
            source_file=self._filename,
            order=self._order,
            parameters=parameters,
            body=self._text(body_node),
        )

    def _text(self, node: Node | None) -> str:
        if node is None:
            return ""
        return self._source[node.start_byte:node.end_byte]


class ArrowFunctionVisitor:
    def __init__(
        self,
        node: Node,
        source: str,
        filename: str,
        order: int,
    ) -> None:
        self._node = node
        self._source = source
        self._filename = filename
        self._order = order

    def visit(self) -> ArrowFunction | None:
        name = ""

        parent = self._node.parent
        if parent is not None and parent.type == "variable_declarator":
            name_node = parent.child_by_field_name("name")
            if name_node is not None:
                name = self._text(name_node)

        parameter_node = self._node.child_by_field_name("parameters")
        body_node = self._node.child_by_field_name("body")

        parameters: list[str] = []

        if parameter_node is not None:
            for child in parameter_node.children:
                if child.type == "identifier":
                    parameters.append(self._text(child))

        return ArrowFunction(
            name=name,
            source_file=self._filename,
            order=self._order,
            parameters=parameters,
            body=self._text(body_node),
        )

    def _text(self, node: Node | None) -> str:
        if node is None:
            return ""
        return self._source[node.start_byte:node.end_byte]


class ClassVisitor:
    def __init__(
        self,
        node: Node,
        source: str,
        filename: str,
        order: int,
    ) -> None:
        self._node = node
        self._source = source
        self._filename = filename
        self._order = order

    def visit(self) -> ClassDeclaration | None:
        name_node = self._node.child_by_field_name("name")
        body_node = self._node.child_by_field_name("body")

        methods: list[Method] = []

        if body_node is not None:
            for child in body_node.children:
                if child.type != "method_definition":
                    continue

                method_name_node = child.child_by_field_name("name")
                method_parameter_node = child.child_by_field_name("parameters")
                method_body_node = child.child_by_field_name("body")

                parameters: list[str] = []

                if method_parameter_node is not None:
                    for param in method_parameter_node.children:
                        if param.type == "identifier":
                            parameters.append(self._text(param))

                methods.append(
                    Method(
                        name=self._text(method_name_node),
                        parameters=parameters,
                        body=self._text(method_body_node),
                    )
                )

        return ClassDeclaration(
            name=self._text(name_node),
            source_file=self._filename,
            order=self._order,
            methods=methods,
        )

    def _text(self, node: Node | None) -> str:
        if node is None:
            return ""
        return self._source[node.start_byte:node.end_byte]


class ObjectVisitor:
    def __init__(
        self,
        node: Node,
        source: str,
        filename: str,
        order: int,
    ) -> None:
        self._node = node
        self._source = source
        self._filename = filename
        self._order = order

    def visit(self) -> ObjectDeclaration | None:
        name = ""

        parent = self._node.parent
        if parent is not None and parent.type == "variable_declarator":
            name_node = parent.child_by_field_name("name")
            if name_node is not None:
                name = self._text(name_node)

        properties: dict[str, str] = {}

        for child in self._node.children:
            if child.type != "pair":
                continue

            key_node = child.child_by_field_name("key")
            value_node = child.child_by_field_name("value")

            if key_node is not None:
                properties[self._text(key_node)] = self._text(value_node)

        return ObjectDeclaration(
            name=name,
            source_file=self._filename,
            order=self._order,
            properties=properties,
        )

    def _text(self, node: Node | None) -> str:
        if node is None:
            return ""
        return self._source[node.start_byte:node.end_byte]


class ArrayVisitor:
    def __init__(
        self,
        node: Node,
        source: str,
        filename: str,
        order: int,
    ) -> None:
        self._node = node
        self._source = source
        self._filename = filename
        self._order = order

    def visit(self) -> ArrayDeclaration | None:
        name = ""

        parent = self._node.parent
        if parent is not None and parent.type == "variable_declarator":
            name_node = parent.child_by_field_name("name")
            if name_node is not None:
                name = self._text(name_node)

        elements: list[str] = []

        for child in self._node.children:
            if child.type in {"", ","}:
                continue

            if child.type != "nested_identifier":
                elements.append(self._text(child))

        return ArrayDeclaration(
            name=name,
            source_file=self._filename,
            order=self._order,
            elements=elements,
        )

    def _text(self, node: Node | None) -> str:
        if node is None:
            return ""
        return self._source[node.start_byte:node.end_byte]


class StatementVisitor:
    def __init__(
        self,
        node: Node,
        source: str,
        filename: str,
        order: int,
    ) -> None:
        self._node = node
        self._source = source
        self._filename = filename
        self._order = order

    def visit(self) -> Statement | None:
        statement_type = self._node.type

        if self._node.type == "expression_statement":
            for child in self._node.children:
                if child.type == "call_expression":
                    statement_type = "call_expression"
                    break

        return Statement(
            statement_type=statement_type,
            code=self._text(self._node),
            source_file=self._filename,
            order=self._order,
        )

    def _text(self: Node | None) -> str:
        if node is None:
            return ""
        return self._source[node.start_byte:node.end_byte]