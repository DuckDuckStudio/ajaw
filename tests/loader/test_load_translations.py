"""
测试 ajaw 的 argparse 翻译加载功能。
"""

import argparse
from unittest.mock import MagicMock, Mock

import pytest

from ajaw import loader


def test_load_translations_normalizes_language_and_patches_argparse(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """验证显式语言会被规范化并应用到 argparse。"""

    translation = Mock()
    translation.gettext = Mock(return_value="翻译文本")
    translation.ngettext = Mock(return_value="翻译复数文本")
    translation_path = MagicMock()
    locale_path = Mock()
    translation_path.__truediv__.return_value = locale_path
    resource_files = Mock(return_value=translation_path)
    translation_loader = Mock(return_value=translation)
    normalize = Mock(return_value="zh_CN.UTF-8")

    monkeypatch.setattr(loader.importlib.resources, "files", resource_files)
    monkeypatch.setattr(loader.gettext, "translation", translation_loader)
    monkeypatch.setattr(loader.locale, "normalize", normalize)

    loader.load_translations("zh_CN")

    normalize.assert_called_once_with("zh_CN")
    resource_files.assert_called_once_with("ajaw")
    translation_loader.assert_called_once_with("argparse", str(locale_path), ["zh_CN"])
    assert vars(argparse)["_"] is translation.gettext
    assert vars(argparse)["ngettext"] is translation.ngettext


def test_load_translations_detects_language_when_not_provided(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """验证未提供语言时会使用自动检测结果。"""

    translation = Mock()
    translation_loader = Mock(return_value=translation)

    detect_language = Mock(return_value="zh_CN")
    monkeypatch.setattr(loader, "_detect_language", detect_language)
    resource_path = MagicMock()
    resource_path.__truediv__.return_value = "package/locale"
    monkeypatch.setattr(
        loader.importlib.resources, "files", Mock(return_value=resource_path)
    )
    monkeypatch.setattr(loader.gettext, "translation", translation_loader)

    loader.load_translations()

    detect_language.assert_called_once_with()
    translation_loader.assert_called_once_with("argparse", "package/locale", ["zh_CN"])
