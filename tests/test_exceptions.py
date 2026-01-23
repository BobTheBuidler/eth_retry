import asyncio
from json import JSONDecodeError

import aiohttp
import pytest
import requests
from sqlite3 import OperationalError
from urllib3.exceptions import MaxRetryError

from eth_retry import eth_retry
from eth_retry.eth_retry import auto_retry


def _no_sleep(*_args, **_kwargs) -> None:
    return None


async def _no_sleep_async(*_args, **_kwargs) -> None:
    return None


def _set_no_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(eth_retry, "randrange", lambda *_args, **_kwargs: 0)
    monkeypatch.setattr(eth_retry, "timesleep", _no_sleep)
    monkeypatch.setattr(eth_retry, "aiosleep", _no_sleep_async)


def test_retries_requests_exceptions(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_no_sleep(monkeypatch)

    exceptions = [
        requests.exceptions.ConnectionError("nope"),
        requests.exceptions.HTTPError("nope"),
        requests.exceptions.ReadTimeout("nope"),
        MaxRetryError(None, "http://example.com"),
        JSONDecodeError("bad", "{}", 0),
    ]

    for exception in exceptions:
        calls = {"count": 0}

        @auto_retry(max_retries=1, min_sleep_time=1, max_sleep_time=1)
        def flaky() -> str:
            calls["count"] += 1
            if calls["count"] == 1:
                raise exception
            return "ok"

        assert flaky() == "ok"
        assert calls["count"] == 2


def test_retries_brownie_operational_error(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_no_sleep(monkeypatch)
    calls = {"count": 0}

    @auto_retry(max_retries=1, min_sleep_time=1, max_sleep_time=1)
    def flaky() -> str:
        calls["count"] += 1
        if calls["count"] == 1:
            raise OperationalError("database is locked")
        return "ok"

    assert flaky() == "ok"
    assert calls["count"] == 2


def test_retries_aiohttp_client_error(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_no_sleep(monkeypatch)
    calls = {"count": 0}

    @auto_retry(max_retries=1, min_sleep_time=1, max_sleep_time=1)
    async def flaky() -> str:
        calls["count"] += 1
        if calls["count"] == 1:
            raise aiohttp.ClientError("nope")
        return "ok"

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(asyncio.gather(*[flaky()]))
    assert result == ["ok"]
    assert calls["count"] == 2
