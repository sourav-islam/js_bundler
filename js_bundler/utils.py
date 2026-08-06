from __future__ import annotations

import logging
from pathlib import Path

from js_bundler import constants


def setup_logger(level: str) -> None:
    """
    Configure application logging.
    """

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=constants.LOG_FORMAT,
        datefmt=constants.LOG_DATE_FORMAT,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a named logger.
    """

    return logging.getLogger(name)


def read_file(path: Path) -> str:
    """
    Read a UTF-8 text file.
    """

    return path.read_text(
        encoding="utf-8"
    )


def write_file(
    path: Path,
    content: str,
) -> None:
    """
    Write UTF-8 text to disk.
    """

    path.write_text(
        content,
        encoding="utf-8",
    )


def ensure_directory(path: Path) -> None:
    """
    Create directory if it does not exist.
    """

    path.mkdir(
        parents=True,
        exist_ok=True,
    )