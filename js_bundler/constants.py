from __future__ import annotations

from pathlib import Path

# =============================================================================
# Directories
# =============================================================================

DEFAULT_INPUT_DIR = "input"
DEFAULT_OUTPUT_DIR = "output"

# =============================================================================
# Output Files
# =============================================================================

DEFAULT_BUNDLE_FILENAME = "bundle.js"
DEFAULT_REPORT_FILENAME = "report.txt"

# =============================================================================
# Supported File Extension
# =============================================================================

SUPPORTED_EXTENSION = ".js"

# =============================================================================
# Tree-sitter Node Types
# =============================================================================

IMPORT_STATEMENT = "import_statement"

EXPORT_STATEMENT = "export_statement"

LEXICAL_DECLARATION = "lexical_declaration"

VARIABLE_DECLARATOR = "variable_declarator"

FUNCTION_DECLARATION = "function_declaration"

CLASS_DECLARATION = "class_declaration"

ARROW_FUNCTION = "arrow_function"

OBJECT = "object"

ARRAY = "array"

CALL_EXPRESSION = "call_expression"

IF_STATEMENT = "if_statement"

FOR_STATEMENT = "for_statement"

WHILE_STATEMENT = "while_statement"

TRY_STATEMENT = "try_statement"

SWITCH_STATEMENT = "switch_statement"

EXPRESSION_STATEMENT = "expression_statement"

# =============================================================================
# Merge Strategies
# =============================================================================

PREFER_FIRST = "prefer_first"

PREFER_LAST = "prefer_last"

PREFER_LONGEST = "prefer_longest"

VALID_STRATEGIES = {
    PREFER_FIRST,
    PREFER_LAST,
    PREFER_LONGEST,
}

DEFAULT_STRATEGY = PREFER_LAST

# =============================================================================
# Logging
# =============================================================================

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"

LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

DEFAULT_LOG_LEVEL = "INFO"