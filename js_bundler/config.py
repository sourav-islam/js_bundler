from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse

from js_bundler import constants


@dataclass(slots=True)
class AppConfig:

    input_dir: Path = Path(constants.DEFAULT_INPUT_DIR)

    output_dir: Path = Path(constants.DEFAULT_OUTPUT_DIR)

    strategy: str = constants.DEFAULT_STRATEGY

    log_level: str = constants.DEFAULT_LOG_LEVEL

    @property
    def bundle_path(self) -> Path:
        return self.output_dir / constants.DEFAULT_BUNDLE_FILENAME

    @property
    def report_path(self) -> Path:
        return self.output_dir / constants.DEFAULT_REPORT_FILENAME

    @property
    def input_files(self) -> list[Path]:

        return sorted(
            self.input_dir.glob(f"*{constants.SUPPORTED_EXTENSION}")
        )

    def validate(self) -> None:

        if self.strategy not in constants.VALID_STRATEGIES:
            raise ValueError(
                f"Invalid merge strategy: {self.strategy}"
            )

        if not self.input_dir.exists():
            raise FileNotFoundError(
                f"Input directory not found: {self.input_dir}"
            )

        if not self.input_files:
            raise FileNotFoundError(
                "No JavaScript files found."
            )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    @classmethod
    def from_args(cls, args=None) -> "AppConfig":

        parser = argparse.ArgumentParser(
            prog="js-bundler"
        )

        parser.add_argument(
            "--input-dir",
            default=constants.DEFAULT_INPUT_DIR,
        )

        parser.add_argument(
            "--output-dir",
            default=constants.DEFAULT_OUTPUT_DIR,
        )

        parser.add_argument(
            "--strategy",
            default=constants.DEFAULT_STRATEGY,
            choices=sorted(constants.VALID_STRATEGIES),
        )

        parser.add_argument(
            "--log-level",
            default=constants.DEFAULT_LOG_LEVEL,
        )

        parsed = parser.parse_args(args)

        return cls(
            input_dir=Path(parsed.input_dir),
            output_dir=Path(parsed.output_dir),
            strategy=parsed.strategy,
            log_level=parsed.log_level,
        )