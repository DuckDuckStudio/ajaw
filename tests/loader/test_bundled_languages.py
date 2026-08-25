"""
测试 ajaw.loader 的 BUNDLED_LANGUAGES 常量是否正确。
"""

import importlib.resources

from ajaw import BUNDLED_LANGUAGES


def test_bundled_languages_contains_all() -> None:
    """确保 BUNDLED_LANGUAGES 包含所有内置语言。"""

    locale_dir = importlib.resources.files("ajaw") / "locale"
    available_languages = tuple(
        entry.name for entry in locale_dir.iterdir() if entry.is_dir()
    )
    assert not any((l not in BUNDLED_LANGUAGES) for l in available_languages)
