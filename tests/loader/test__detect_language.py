"""
测试 ajaw.loader 的 _detect_language() 函数。
"""

import pytest

from ajaw import loader


def test_detect_language_returns_system_language(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """验证能够返回系统检测到的语言。"""

    monkeypatch.setattr(loader.locale, "getdefaultlocale", lambda: ("en_US", "UTF-8"))

    assert loader._detect_language() == "en_US"  # pyright: ignore[reportPrivateUsage] pylint: disable=protected-access / W0212


def test_detect_language_falls_back_to_zh_cn(monkeypatch: pytest.MonkeyPatch) -> None:
    """验证系统语言不可用时回退到简体中文。"""

    monkeypatch.setattr(loader.locale, "getdefaultlocale", lambda: (None, None))

    assert loader._detect_language() == "zh_CN"  # pyright: ignore[reportPrivateUsage] pylint: disable=protected-access / W0212
