from __future__ import annotations

from js_bundler.config import AppConfig
from js_bundler.parser.parser import JavaScriptParser


def test_parse_directory():

    parser = JavaScriptParser()

    config = AppConfig()

    files = parser.parse_directory(
        config.input_directory
    )

    assert len(files) == 2


def test_global_file():

    parser = JavaScriptParser()

    config = AppConfig()

    files = parser.parse_directory(
        config.input_directory
    )

    global_file = next(
        file
        for file in files
        if file.filename == "global.js"
    )

    assert len(global_file.variables) == 1

    assert len(global_file.functions) == 2

    assert global_file.variables[0].name == "API_URL"

    assert global_file.functions[0].name == "showToast"

    assert global_file.functions[1].name == "formatPrice"


def test_home_file():

    parser = JavaScriptParser()

    config = AppConfig()

    files = parser.parse_directory(
        config.input_directory
    )

    home_file = next(
        file
        for file in files
        if file.filename == "home.js"
    )

    assert len(home_file.variables) == 1

    assert len(home_file.functions) == 2

    assert home_file.variables[0].value == '"/v2/api"'

    assert home_file.functions[0].name == "showToast"

    assert home_file.functions[1].name == "loadHero"