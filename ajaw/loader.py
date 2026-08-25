"""
加载并应用随包内置的 argparse 翻译文件。

翻译文件（`.mo`）来源于 [DuckDuckStudio/python-argparse-translations](https://github.com/DuckDuckStudio/python-argparse-translations)。
"""

import argparse
import gettext
import importlib.resources
import locale
from typing import Final

BUNDLED_LANGUAGES: Final = ("zh_CN",)
"""
ajaw 中附带的翻译语言。
"""


def _detect_language() -> str:
    """
    检测系统的语言代码，失败返回默认的 `zh_CN`。

    Returns:
        str: 检测到的系统语言代码，失败返回默认的 `zh_CN`。
    """

    # fmt: off
    return locale.getdefaultlocale()[0] or "zh_CN"  # https://github.com/python/cpython/issues/130796 pylint: disable=deprecated-method / W4902
    # fmt: on


def load_translations(lang: str | None = None) -> None:
    """
    加载并应用随包内置的 argparse 翻译文件。
    """

    lang = locale.normalize(lang).split(".")[0] if lang else _detect_language()

    t = gettext.translation(
        "argparse", str(importlib.resources.files("ajaw") / "locale"), [lang]
    )
    # ty: ignore[unresolved-attribute]
    argparse._ = t.gettext  # pyright: ignore[reportAttributeAccessIssue]
    # ty: ignore[unresolved-attribute]
    argparse.ngettext = t.ngettext  # pyright: ignore[reportAttributeAccessIssue]
