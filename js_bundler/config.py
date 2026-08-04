from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from js_bundler import constants


@dataclass(slots=True)
class AppConfig:

    input_directory: Path = Path(constants.INPUT_DIRECTORY)

    output_directory: Path = Path(constants.OUTPUT_DIRECTORY)

    encoding: str = constants.DEFAULT_ENCODING

    def validate(self) -> None:

        if not self.input_directory.exists():
            raise FileNotFoundError(
                f"Input directory not found: "
                f"{self.input_directory}"
            )

        if not self.input_directory.is_dir():
            raise NotADirectoryError(
                self.input_directory
            )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )