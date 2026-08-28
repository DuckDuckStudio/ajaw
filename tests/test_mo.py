"""
检查附带的翻译文件（*.mo）。
"""

import base64
import importlib.resources
import time
from collections.abc import Callable
from typing import Any
from unittest.mock import Mock

import pytest
import requests

_MAX_RETRIES = 3


def _get_with_rate_limit_retries(
    url: str,
    sleep: Callable[[float], Any] = time.sleep,
) -> requests.Response:
    """请求 GitHub API，在触发未认证限流时等待并重试。"""

    for attempt in range(_MAX_RETRIES + 1):
        response = requests.get(url, params={"ref": "main"}, timeout=10)
        if (response.status_code not in (429, 403)) or (attempt == _MAX_RETRIES):
            response.raise_for_status()
            return response

        retry_after = response.headers.get("Retry-After")
        reset_at = response.headers.get("X-RateLimit-Reset")
        if retry_after is not None:
            delay = float(retry_after)
        elif reset_at is not None:
            delay = max(0.0, float(reset_at) - time.time())
        else:
            delay = 1.0
        sleep(delay)

    raise AssertionError("unreachable")


def test_get_with_rate_limit_retries_after_403(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """遇到 GitHub 限流时会等待后再次请求。"""

    responses = [
        requests.Response(),
        requests.Response(),
    ]
    responses[0].status_code = 403
    responses[0].headers["Retry-After"] = "2"
    responses[1].status_code = 200
    sleep = Mock()
    get = Mock(side_effect=responses)
    monkeypatch.setattr(requests, "get", get)

    response = _get_with_rate_limit_retries("https://example.test", sleep=sleep)

    assert response.status_code == 200
    assert get.call_count == 2
    sleep.assert_called_once_with(2.0)


def test_get_with_rate_limit_retries_after_reset_time(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """没有 Retry-After 时会根据限流重置时间等待。"""

    responses = [
        requests.Response(),
        requests.Response(),
    ]
    responses[0].status_code = 429
    responses[0].headers["X-RateLimit-Reset"] = "105"
    responses[1].status_code = 200
    sleep = Mock()
    get = Mock(side_effect=responses)
    monkeypatch.setattr(requests, "get", get)
    monkeypatch.setattr(time, "time", Mock(return_value=100))

    response = _get_with_rate_limit_retries("https://example.test", sleep=sleep)

    assert response.status_code == 200
    assert get.call_count == 2
    sleep.assert_called_once_with(5.0)


def test_get_with_rate_limit_retries_with_default_delay(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """没有限流响应头时会等待默认时长。"""

    responses = [
        requests.Response(),
        requests.Response(),
    ]
    responses[0].status_code = 403
    responses[1].status_code = 200
    sleep = Mock()
    get = Mock(side_effect=responses)
    monkeypatch.setattr(requests, "get", get)

    response = _get_with_rate_limit_retries("https://example.test", sleep=sleep)

    assert response.status_code == 200
    assert get.call_count == 2
    sleep.assert_called_once_with(1.0)


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
        response = _get_with_rate_limit_retries(upstream_url)
        upstream_mo = base64.b64decode(response.json()["content"])

        assert local_mo == upstream_mo, (
            f"ajaw/locale/{language_dir.name}/LC_MESSAGES/argparse.mo 和上游的翻译不匹配"
        )
