import pytest

import eth_retry.eth_retry as er


def test_auto_retry_retries_then_succeeds_sync(monkeypatch):
    attempts = {"count": 0}
    sleeps = []

    def flaky():
        attempts["count"] += 1
        if attempts["count"] <= 2:
            raise ConnectionError("temporary failure in name resolution")
        return "ok"

    monkeypatch.setattr(er, "randrange", lambda *_: 1)
    monkeypatch.setattr(er, "timesleep", lambda seconds: sleeps.append(seconds))

    wrapped = er.auto_retry(max_retries=5, min_sleep_time=1, max_sleep_time=2)(flaky)
    assert wrapped() == "ok"
    assert attempts["count"] == 3
    assert sleeps == [1, 2]


def test_auto_retry_non_retryable_exception_bubbles_sync(monkeypatch):
    sleeps = []

    def fail():
        raise ValueError("no retry")

    monkeypatch.setattr(er, "timesleep", lambda seconds: sleeps.append(seconds))

    wrapped = er.auto_retry(max_retries=2)(fail)
    with pytest.raises(ValueError):
        wrapped()
    assert sleeps == []


def test_auto_retry_respects_max_retries_sync(monkeypatch):
    attempts = {"count": 0}
    sleeps = []

    def fail():
        attempts["count"] += 1
        raise ConnectionError("temporary failure in name resolution")

    monkeypatch.setattr(er, "randrange", lambda *_: 1)
    monkeypatch.setattr(er, "timesleep", lambda seconds: sleeps.append(seconds))

    wrapped = er.auto_retry(max_retries=1, min_sleep_time=1, max_sleep_time=2)(fail)
    with pytest.raises(ConnectionError):
        wrapped()
    assert attempts["count"] == 3
    assert sleeps == [1, 2]


def test_auto_retry_rejects_async_generator():
    async def gen():
        yield 1

    with pytest.raises(ValueError, match="async gen function not supported"):
        er.auto_retry(gen)
