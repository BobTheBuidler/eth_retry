"""Benchmark tests for synchronous eth_retry decorator."""
import pytest
from eth_retry.eth_retry import auto_retry


@pytest.mark.benchmark
def test_auto_retry_sync_no_error():
    """Benchmark auto_retry decorator with successful function execution."""
    counter = 0

    @auto_retry
    def successful_function():
        nonlocal counter
        counter += 1
        return counter

    result = successful_function()
    assert result > 0


@pytest.mark.benchmark
def test_auto_retry_sync_with_single_retry():
    """Benchmark auto_retry decorator with one retry before success."""
    attempts = 0

    @auto_retry(min_sleep_time=0, max_sleep_time=0)
    def function_with_one_failure():
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise ConnectionError("Temporary connection error")
        return "success"

    result = function_with_one_failure()
    assert result == "success"
    assert attempts == 2


@pytest.mark.benchmark
def test_decorator_application_overhead():
    """Benchmark the overhead of applying the auto_retry decorator."""

    def simple_function():
        return 42

    decorated = auto_retry(simple_function)
    result = decorated()
    assert result == 42


@pytest.mark.benchmark
def test_should_retry_logic():
    """Benchmark the should_retry decision logic."""
    from eth_retry.eth_retry import should_retry

    # Test various exception types
    exceptions = [
        ConnectionError("test"),
        ValueError("max rate limit reached"),
        ValueError("execution aborted (timeout = 5s)"),
        RuntimeError("unrelated error"),
    ]

    for exc in exceptions:
        _ = should_retry(exc, failures=0, max_retries=10)
