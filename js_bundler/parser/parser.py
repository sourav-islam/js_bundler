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
        self._language = Language(tree_sitter_javascript.language())
        self._parser = Parser()
        self._parser.set_language(self._language)
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