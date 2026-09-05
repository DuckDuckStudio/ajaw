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


def _detect_language() -> str | None:
    """
    检测系统的语言代码，失败返回 `None`。

    Returns:
        str: 检测到的系统语言代码，失败返回 `None`。
    """

    # fmt: off
    return locale.getdefaultlocale()[0]  # https://github.com/python/cpython/issues/130796 pylint: disable=deprecated-method / W4902
    # fmt: on


def load_translations(lang: str | None = None) -> None:
    """
    加载并应用随包内置的 argparse 翻译文件。

    Args:
        lang:
            指定的语言；
            如果为 `None`，则尝试检测系统语言。

    Raises:
        ValueError: 指定了一个不支持的语言。
    """

    to_lang = locale.normalize(lang).split(".")[0] if lang else _detect_language()
    if to_lang:
        to_lang = to_lang.replace("-", "_")

    if (not to_lang) or (to_lang == "en_US"):
        # 不需要翻译
        return

    if to_lang not in BUNDLED_LANGUAGES:
        if lang:
            # 指定了一个不支持的语言
            raise ValueError(f"没有 {lang} ({to_lang}) 的翻译")

        return

    t = gettext.translation(
        "argparse", str(importlib.resources.files("ajaw") / "locale"), [to_lang]
    )
    # ty: ignore[unresolved-attribute]
    argparse._ = t.gettext  # pyright: ignore[reportAttributeAccessIssue]
    # ty: ignore[unresolved-attribute]
    argparse.ngettext = t.ngettext  # pyright: ignore[reportAttributeAccessIssue]
