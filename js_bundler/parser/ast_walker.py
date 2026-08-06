from __future__ import annotations

from tree_sitter import Node

from js_bundler.models import JavaScriptFile
from js_bundler.parser.visitors import (
    ArrayVisitor,
    ArrowFunctionVisitor,
    ClassVisitor,
    ExportVisitor,
    FunctionVisitor,
    ImportVisitor,
    ObjectVisitor,
    StatementVisitor,
    VariableVisitor,
)


class ASTWalker:
    """
    Traverse the Tree-sitter AST recursively and build a JavaScriptFile model.
    """

    def __init__(self) -> None:
        self._source = ""
        self._filename = ""
        self._order = 0

    def walk(self, tree, source: str, filename: str) -> JavaScriptFile:
        self._source = source
        self._filename = filename
        self._order = 0

        file_model = JavaScriptFile(filename=filename)
        self._walk_node(tree.root_node, file_model)

        return file_model

    def _walk_node(self, node: Node, file_model: JavaScriptFile) -> None:
        if node.type == "import_statement":
            self._add_import(file_model, node)

        elif node.type == "export_statement":
            self._add_export(file_model, node)

        elif node.type in {"lexical_declaration", "variable_declaration"}:
            self._handle_variable_block(file_model, node)

        elif node.type == "function_declaration":
            self._add_function(file_model, node)

        elif node.type == "arrow_function":
            self._add_arrow_function(file_model, node)

        elif node.type == "class_declaration":
            self._add_class(file_model, node)

        elif node.type == "object":
            self._add_object(file_model, node)

        elif node.type == "array":
            self._add_array(file_model, node)

        elif node.type in {
            "expression_statement",
            "if_statement",
            "for_statement",
            "while_statement",
            "try_statement",
            "switch_statement",
            "call_expression",
        }:
            self._add_statement(file_model, node)

        for child in node.children:
            self._walk_node(child, file_model)

    def _handle_variable_block(
        self,
        file_model: JavaScriptFile,
        node: Node,
    ) -> None:
        for child in node.children:
            if child.type != "variable_declarator":
                continue

            visitor = VariableVisitor(
                child,
                self._source,
                self._filename,
                self._next_order(),
            )
            declaration = visitor.visit()

            if declaration is not None:
                file_model.variables.append(declaration)

    def _add_import(self, file_model: JavaScriptFile, node: Node) -> None:
        visitor = ImportVisitor(
            node,
            self._source,
            self._filename,
            self._next_order(),
        )
        declaration = visitor.visit()

        if declaration is not None:
            file_model.imports.append(declaration)

    def _add_export(self, file_model: JavaScriptFile, node: Node) -> None:
        visitor = ExportVisitor(
            node,
            self._source,
            self._filename,
            self._next_order(),
        )
        declaration = visitor.visit()

        if declaration is not None:
            file_model.exports.append(declaration)

    def _add_function(self, file_model: JavaScriptFile, node: Node) -> None:
        visitor = FunctionVisitor(
            node,
            self._source,
            self._filename,
            self._next_order(),
        )
        declaration = visitor.visit()

        if declaration is not None:
            file_model.functions.append(declaration)

    def _add_arrow_function(
        self,
        file_model: JavaScriptFile,
        node: Node,
    ) -> None:
        visitor = ArrowFunctionVisitor(
            node,
            self._source,
            self._filename,
            self._next_order(),
        )
        declaration = visitor.visit()

        if declaration is not None:
            file_model.arrow_functions.append(declaration)

    def _add_class(self, file_model: JavaScriptFile, node: Node) -> None:
        visitor = ClassVisitor(
            node,
            self._source,
            self._filename,
            self._next_order(),
        )
        declaration = visitor.visit()

        if declaration is not None:
            file_model.classes.append(declaration)

    def _add_object(self, file_model: JavaScriptFile, node: Node) -> None:
        visitor = ObjectVisitor(
            node,
            self._source,
            self._filename,
            self._next_order(),
        )
        declaration = visitor.visit()

        if declaration is not None:
            file_model.objects.append(declaration)

    def _add_array(self, file_model: JavaScriptFile, node: Node) -> None:
        visitor = ArrayVisitor(
            node,
            self._source,
            self._filename,
            self._next_order(),
        )
        declaration = visitor.visit()

        if declaration is not None:
            file_model.arrays.append(declaration)

    def _add_statement(
        self,
        file_model: JavaScriptFile,
        node: Node,
    ) -> None:
        if node.type == "expression_statement":
            child = next(
                (
                    child
                    for child in node.children
                    if child.type == "call_expression"
                ),
                None,
            )
            if child is not None:
                node = child

        visitor = StatementVisitor(
            node,
            self._source,
            self._filename,
            self._next_order(),
        )
        declaration = visitor.visit()

        if declaration is not None:
            file_model.statements.append(declaration)

    def _next_order(self) -> int:
        self._order += 1
        return self._order