import asyncio

import pytest

import eth_retry.eth_retry as er


def test_auto_retry_retries_then_succeeds_async(monkeypatch):
    attempts = {"count": 0}
    sleeps = []

    async def flaky():
        attempts["count"] += 1
        if attempts["count"] <= 2:
            raise asyncio.TimeoutError("timeout")
        return "ok"

    async def fake_sleep(seconds):
        sleeps.append(seconds)

    monkeypatch.setattr(er, "randrange", lambda *_: 1)
    monkeypatch.setattr(er, "aiosleep", fake_sleep)

    wrapped = er.auto_retry(max_retries=5, min_sleep_time=1, max_sleep_time=2)(flaky)
    result = asyncio.run(wrapped())
    assert result == "ok"
    assert attempts["count"] == 3
    assert sleeps == []


def test_auto_retry_respects_max_retries_async(monkeypatch):
    attempts = {"count": 0}
    sleeps = []

    async def fail():
        attempts["count"] += 1
        raise asyncio.TimeoutError("timeout")

    async def fake_sleep(seconds):
        sleeps.append(seconds)

    monkeypatch.setattr(er, "randrange", lambda *_: 1)
    monkeypatch.setattr(er, "aiosleep", fake_sleep)

    wrapped = er.auto_retry(max_retries=1, min_sleep_time=1, max_sleep_time=2)(fail)
    with pytest.raises(asyncio.TimeoutError):
        asyncio.run(wrapped())
    assert attempts["count"] == 3
    assert sleeps == []
