from json import JSONDecodeError

import pytest

import eth_retry.eth_retry as er


@pytest.mark.parametrize(
    "message",
    [
        "execution aborted (timeout = 5s)",
        "execution aborted (timeout = 10s)",
        "max retries exceeded with url",
        "temporary failure in name resolution",
        "parse error",
        "max rate limit reached",
        "max calls per sec rate limit reached",
        "please use api key for higher rate limit",
        "too many invalid api key attempts, please try again later",
        "after last accepted block",
        "too many requests",
        "cannot assign requested address",
        "your app has exceeded its compute units per second capacity. if you have retries enabled, you can safely ignore this message. if not, check out https://docs.alchemy.com/reference/throughput",
        "request limit reached - reduce calls per second or upgrade your account at quicknode.com",
    ],
)
def test_should_retry_string_matches(message):
    assert er.should_retry(Exception(message), failures=0, max_retries=3) is True


@pytest.mark.parametrize(
    "exc",
    [
        ConnectionError("connection"),
        er.requests.exceptions.ConnectionError("connection"),
        er.HTTPError("http error"),
        er.ReadTimeout("timeout"),
        er.MaxRetryError(None, "http://example.com", "retry"),
        JSONDecodeError("bad json", "doc", 0),
        er.ClientError("client"),
        er.AsyncioTimeoutError("timeout"),
    ],
)
def test_should_retry_general_exceptions(exc):
    assert er.should_retry(exc, failures=0, max_retries=3) is True


def test_should_retry_skips_too_large_and_404():
    assert er.should_retry(ConnectionError("Too Large"), failures=0, max_retries=3) is False
    assert er.should_retry(ConnectionError("404"), failures=0, max_retries=3) is False


def test_should_retry_operational_error_locked():
    assert (
        er.should_retry(er.OperationalError("database is locked"), failures=0, max_retries=3)
        is True
    )


def test_should_not_retry_other_operational_errors():
    assert er.should_retry(er.OperationalError("disk i/o error"), failures=0, max_retries=3) is False


def test_should_retry_respects_max_retries():
    assert er.should_retry(ConnectionError("connection"), failures=2, max_retries=1) is False


def test_should_retry_disabled(reload_eth_retry):
    module = reload_eth_retry(ETH_RETRY_DISABLED="1")
    assert module.should_retry(ConnectionError("connection"), failures=0, max_retries=3) is False


def test_should_not_retry_unmatched_exception():
    assert er.should_retry(ValueError("nope"), failures=0, max_retries=3) is False
