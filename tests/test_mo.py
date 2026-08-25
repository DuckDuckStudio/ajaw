"""
检查附带的翻译文件（*.mo）。
"""

import base64
import importlib.resources

import requests


def test_bundled_mo_matches_upstream_main() -> None:
    """确保所有附带的 .mo 文件与上游 main 分支一致。"""

    locale_dir = importlib.resources.files("ajaw") / "locale"
    for language_dir in locale_dir.iterdir():
        assert language_dir.is_dir()

        local_mo = (language_dir / "LC_MESSAGES" / "argparse.mo").read_bytes()
        upstream_url = (
            "https://api.github.com/repos/DuckDuckStudio/python-argparse-translations/contents/"
            f"translations/1.1/locale/{language_dir.name}/LC_MESSAGES/argparse.mo"
        )
        response = requests.get(upstream_url, params={"ref": "main"}, timeout=10)
        response.raise_for_status()
        upstream_mo = base64.b64decode(response.json()["content"])

        assert local_mo == upstream_mo, (
            f"ajaw/locale/{language_dir.name}/LC_MESSAGES/argparse.mo 和上游的翻译不匹配"
        )
