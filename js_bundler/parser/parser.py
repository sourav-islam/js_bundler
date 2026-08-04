from __future__ import annotations

from pathlib import Path

import tree_sitter_javascript
from tree_sitter import Language, Parser

from js_bundler.constants import DEFAULT_ENCODING
from js_bundler.models import JavaScriptFile
from js_bundler.parser.ast_walker import ASTWalker


class JavaScriptParser:
    """
    Parses JavaScript files using Tree-sitter.
    """

    def __init__(self) -> None:

        language = Language(
            tree_sitter_javascript.language() #load the js grammar
        )

        self.parser = Parser()
        self.parser.language = language #Now the parser knows JavaScript.

    def parse_directory(
        self,
        directory: Path,
    ) -> list[JavaScriptFile]:

        javascript_files: list[JavaScriptFile] = []

        for path in sorted(directory.glob("*.js")):

            javascript_files.append(
                self.parse_file(path) #parse_file(home.js)
            )

        return javascript_files #[ JavaScriptFile(...),JavaScriptFile(...),JavaScriptFile(...)]

    def parse_file(
        self,
        path: Path,
    ) -> JavaScriptFile:

        source = path.read_bytes()

        tree = self.parser.parse(source)

        walker = ASTWalker(source)

        variables, functions = walker.walk(
            tree.root_node
        )

        return JavaScriptFile(
            filename=path.name,
            variables=variables,
            functions=functions,
        )