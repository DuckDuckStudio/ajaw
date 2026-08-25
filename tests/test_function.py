"""
测试实际使用效果。
"""

import argparse
import re

import pytest

from ajaw import BUNDLED_LANGUAGES, load_translations


def test_argparse_output_is_translated(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    确认加载翻译后，帮助文本已翻译。
    """

    for lang in BUNDLED_LANGUAGES:
        load_translations(lang)

        parser = argparse.ArgumentParser(prog="demo")
        parser.add_argument("--version", action="version", version="demo 1.0")

        try:
            parser.parse_args(["--help"])
        except SystemExit:
            pass

        output = capsys.readouterr().out
        help_output = re.search(r"^\s+-h,\s--help\s+(.*)$", output, re.MULTILINE)
        assert help_output is not None
        assert help_output.group(1) != "show this help message and exit"
