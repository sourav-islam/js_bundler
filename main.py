from __future__ import annotations
from js_bundler.merger import Merger
from js_bundler.config import AppConfig
from js_bundler.parser.parser import JavaScriptParser
from js_bundler.writer import BundleWriter


def print_result(files) -> None:

    print()

    print("=" * 60)
    print("Parsed JavaScript Files")
    print("=" * 60)

    for file in files:

        print()

        print(f"File: {file.filename}")

        print()

        print("Variables")

        if not file.variables:
            print("  None")

        for variable in file.variables:

            print(
                f"  "
                f"{variable.kind} "
                f"{variable.name} = "
                f"{variable.value}"
            )

        print()

        print("Functions")

        if not file.functions:
            print("  None")

        for function in file.functions:

            print(
                f"  "
                f"{function.name}"
                f"("
                f"{', '.join(function.parameters)}"
                f")"
            )


def main() -> None:

    config = AppConfig()

    config.validate()

    parser = JavaScriptParser()

    javascript_files = parser.parse_directory(
        config.input_directory
    )

    from js_bundler.comparator import Comparator

    comparison = Comparator().compare(javascript_files)
    merger = Merger()

    result = merger.merge(javascript_files)
    writer = BundleWriter()
    output_paths = writer.write_bundle(
        javascript_files,
        result,
        config.output_directory,
    )

    print()

    print("=" * 60)
    print("MERGED BUNDLE")
    print("=" * 60)

    print()

    print("Variables")

    for variable in result.bundle.variables:

        print(
            variable.kind,
            variable.name,
            "=",
            variable.value,
        )

    print()

    print("Functions")

    for function in result.bundle.functions:

        print(function.name)

    print()
    print("Bundle written to:", output_paths["bundle"])
    print("Report written to:", output_paths["report"])


if __name__ == "__main__":
    main()