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

    # Node types whose dedicated visitor already captures the entire
    # subtree verbatim as text (Function.body, ArrowFunction.body,
    # ClassDeclaration methods, ...). The walker must NOT keep recursing
    # into their children afterwards: doing so would re-discover the
    # statements *inside* that body (e.g. `console.log(message);` inside
    # `function showToast(message) {...}`) and hoist them out as bogus
    # top-level Statement entries, referencing parameters/locals that
    # don't exist at the top level of the bundle.
    _OPAQUE_BODY_TYPES = {"function_declaration", "arrow_function", "class_declaration"}

    def _walk_node(self, node: Node, file_model: JavaScriptFile) -> None:
        if node.type == "import_statement":
            self._add_import(file_model, node)

        elif node.type == "export_statement":
            self._add_export(file_model, node)

        elif node.type in {"lexical_declaration", "variable_declaration"}:
            self._handle_variable_block(file_model, node)

        elif node.type == "function_declaration":
            self._add_function(file_model, node)
            return

        elif node.type == "arrow_function":
            self._add_arrow_function(file_model, node)
            return

        elif node.type == "class_declaration":
            self._add_class(file_model, node)
            return

        elif node.type == "object":
            self._add_object(file_model, node)
            return

        elif node.type == "array":
            self._add_array(file_model, node)
            return

        elif node.type in {
            "expression_statement",
            "if_statement",
            "for_statement",
            "while_statement",
            "try_statement",
            "switch_statement",
        }:
            # Note: "call_expression" is deliberately not in this set.
            # A call used as a statement (e.g. `foo();`) is wrapped in an
            # "expression_statement", which _add_statement() already
            # unwraps to record as a single call_expression Statement.
            # Matching "call_expression" here too would both double-count
            # that same call and start picking up call expressions that
            # aren't statements at all (e.g. nested inside a return value).
            self._add_statement(file_model, node)

        for child in node.children:
            self._walk_node(child, file_model)

    # Declarator values with their own dedicated visitor/model. These are
    # picked up separately when the walker reaches that nested node
    # directly (e.g. the "object" inside `const config = {...}`), so
    # recording them again here as a plain Variable would declare the
    # same name twice in the bundled output.
    _DEDICATED_VALUE_TYPES = {"object", "array", "arrow_function", "class"}

    def _handle_variable_block(
        self,
        file_model: JavaScriptFile,
        node: Node,
    ) -> None:
        for child in node.children:
            if child.type != "variable_declarator":
                continue

            value_node = child.child_by_field_name("value")
            if value_node is not None and value_node.type in self._DEDICATED_VALUE_TYPES:
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