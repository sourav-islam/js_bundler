from __future__ import annotations

from pathlib import Path

import tree_sitter_javascript
from tree_sitter import Language, Parser

from js_bundler.models import JavaScriptFile
from js_bundler.parser.ast_walker import ASTWalker


class JavaScriptParser:
    """
    Parses JavaScript source code using Tree-sitter and converts it
    into a JavaScriptFile model.
    """

    def __init__(self) -> None:
        # Create the tree-sitter Language and construct a Parser.
        # Different tree-sitter bindings expose different Parser APIs
        # (some provide `Parser.set_language()`, others accept the
        # language in the constructor). Try both in a safe way.
        self._language = Language(tree_sitter_javascript.language())

        # Preferred: create Parser and call set_language if available.
        parser = Parser()
        set_lang = getattr(parser, "set_language", None)
        if callable(set_lang):
            set_lang(self._language)
            self._parser = parser
        else:
            # Fallback: try to construct Parser with the language argument.
            try:
                self._parser = Parser(self._language)
            except TypeError:
                # If neither approach works, re-raise a helpful error.
                raise RuntimeError(
                    "Unsupported tree-sitter Parser API: cannot set language."
                )

        self._walker = ASTWalker()

    def parse_file(self, path: Path) -> JavaScriptFile:
        """
        Parse a JavaScript file.
        """
        source = path.read_text(encoding="utf-8")
        return self.parse_source(source=source, filename=path.name)

    def parse_source(self, source: str, filename: str) -> JavaScriptFile:
        """
        Parse JavaScript source code.
        """
        tree = self._parser.parse(source.encode("utf-8"))
        return self._walker.walk(tree=tree, source=source, filename=filename)

    def parse_directory(self, directory: Path) -> list[JavaScriptFile]:
        """
        Parse every JavaScript file inside a directory.
        """
        javascript_files: list[JavaScriptFile] = []

        for path in sorted(directory.glob("*.js")):
            javascript_files.append(self.parse_file(path))

        return javascript_files