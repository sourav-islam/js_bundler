from __future__ import annotations

from tree_sitter import Node

from js_bundler.models import Function, Variable


class ASTWalker:
    """
    Traverses the Tree-sitter AST and extracts
    supported JavaScript constructs.

    Milestone 1 supports:

    - Variable declarations
    - Function declarations
    """

    def __init__(self, source: bytes):
        self.source = source

    def walk(self, root: Node) -> tuple[list[Variable], list[Function]]:
        variables: list[Variable] = []
        functions: list[Function] = []

        self._walk_node(root, variables, functions)

        return variables, functions

    def _walk_node(
        self,
        node: Node,
        variables: list[Variable],
        functions: list[Function],
    ) -> None:

        if node.type == "lexical_declaration":
            variables.extend(self._extract_variables(node))

        elif node.type == "variable_declaration":
            variables.extend(self._extract_variables(node))

        elif node.type == "function_declaration":
            functions.append(self._extract_function(node))

        for child in node.children:
            self._walk_node(
                child,
                variables,
                functions,
            )

    def _extract_variables(
        self,
        declaration: Node,
    ) -> list[Variable]:

        variables: list[Variable] = []

        kind = declaration.child_by_field_name("kind")
        kind_text = (
            self._text(kind)
            if kind is not None
            else declaration.children[0].type
        )

        for child in declaration.children:

            if child.type != "variable_declarator":
                continue

            name_node = child.child_by_field_name("name")
            value_node = child.child_by_field_name("value")

            variables.append(
                Variable(
                    kind=kind_text,
                    name=self._text(name_node),
                    value=self._text(value_node),
                )
            )

        return variables

    def _extract_function(
        self,
        node: Node,
    ) -> Function:

        name_node = node.child_by_field_name("name")

        parameter_node = node.child_by_field_name("parameters")

        body_node = node.child_by_field_name("body")

        parameters: list[str] = []

        if parameter_node is not None:

            for child in parameter_node.children:

                if child.type == "identifier":
                    parameters.append(self._text(child))

        body = ""

        if body_node is not None:
            body = self._text(body_node)

        return Function(
            name=self._text(name_node),
            parameters=parameters,
            body=body,
        )

    def _text(self, node: Node | None) -> str:
        if node is None:
            return ""

        return self.source[
            node.start_byte : node.end_byte
        ].decode("utf-8")