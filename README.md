# JavaScript Bundler

A Python-based JavaScript bundler that parses multiple JavaScript files using **Tree-sitter**, analyzes their declarations, removes duplicate definitions, resolves conflicts, and generates a single optimized JavaScript bundle.

The project is designed for a website builder environment where JavaScript code can exist in multiple files (e.g., global scripts and page-specific scripts). The goal is to combine these files into one optimized bundle while preserving application behavior.

# Supported JavaScript Constructs

Current design supports analysis of:

- Import statements
- Export statements
- Variables (`const`, `let`, `var`)
- Functions
- Arrow functions
- Classes
- Objects
- Arrays
- Function calls
- If statements
- For loops
- While loops
- Try/Catch blocks
- Switch statements

---
## Setup

Install dependencies:
Clone the repository and install the required dependencies.

```bash

git clone https://github.com/sourav-islam/js_bundler.git
cd js_bundler
python3 venv -m .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
```

## Usage

Run the bundler from the project root:

```bash
python3 main.py
```

Optional arguments:

- `--input-dir`: directory containing `.js` source files (default: `input`)
- `--output-dir`: directory for generated files (default: `output`)
- `--strategy`: merge strategy, one of `prefer_first`, `prefer_last`, or `prefer_longest` (default: `prefer_last`)
- `--log-level`: logging level (default: `INFO`)

Example:

```bash
python3 main.py --input-dir input --output-dir output --strategy prefer_first
```

## Output

The bundler writes:

- `output/bundle.js` — merged JavaScript bundle
- `output/report.txt` — summary report of conflicts and duplicates

## Testing

Run tests with:

```bash
python3 -m pytest
```

# Architecture

```
JavaScript Files
        │
        ▼
Parser
(Tree-sitter)
        │
        ▼
AST Walker
        │
        ▼
JavaScript Models
        │
        ▼
Comparator
        │
        ▼
Merger
        │
        ▼
Writer
        │
        ▼
bundle.js
```

Each module has a single responsibility.

---

# Project Structure

```
js-bundler/
│
├── input/
│   ├── global.js
│   ├── home.js
│   └── product.js
│
├── output/
│   └── bundle.js
│
├── js_bundler/
│   ├── parser/
│   │   ├── parser.py
│   │   ├── ast_walker.py
│   │   └── visitors.py
│   │
│   ├── comparator.py
│   ├── merger.py
│   ├── writer.py
│   │
│   ├── models.py
│   ├── constants.py
│   ├── config.py
│   ├── utils.py
│   │
│   └── __init__.py
│
├── tests/
│
├── main.py
├── requirements.txt
└── README.md
```

