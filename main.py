from __future__ import annotations

from pathlib import Path

from js_bundler.comparator import Comparator
from js_bundler.config import AppConfig
from js_bundler.merger import Merger
from js_bundler.parser.parser import JavaScriptParser
from js_bundler.writer import BundleWriter


def main() -> None:
    config = AppConfig.from_args()
    config.validate()

    parser = JavaScriptParser()
    javascript_files = parser.parse_directory(config.input_dir)

    comparison = Comparator().compare(javascript_files)
    merger = Merger()
    result = merger.merge(javascript_files, strategy=config.strategy)

    writer = BundleWriter()
    output_paths = writer.write_bundle(
        javascript_files,
        comparison,
        result,
        config.output_dir,
    )

    # report.txt already contains the comparison + bundle summary, so we
    # just print it instead of keeping a second, separate implementation
    # of the same summary logic in sync.
    print()
    print(Path(output_paths["report"]).read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    main()