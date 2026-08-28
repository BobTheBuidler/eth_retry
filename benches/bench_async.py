"""Benchmark tests for asynchronous eth_retry decorator."""
import asyncio
import pytest
from eth_retry.eth_retry import auto_retry


@pytest.mark.benchmark
def test_auto_retry_async_no_error():
    """Benchmark auto_retry decorator with successful async function execution."""
    counter = 0

    @auto_retry
    async def successful_async_function():
        nonlocal counter
        counter += 1
        return counter

    result = asyncio.run(successful_async_function())
    assert result > 0


@pytest.mark.benchmark
def test_auto_retry_async_with_single_retry():
    """Benchmark auto_retry decorator with one retry before success (async)."""
    attempts = 0

    @auto_retry(min_sleep_time=0, max_sleep_time=0)
    async def async_function_with_one_failure():
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise ConnectionError("Temporary connection error")
        return "success"

    result = asyncio.run(async_function_with_one_failure())
    assert result == "success"
    assert attempts == 2


@pytest.mark.benchmark
def test_async_decorator_application_overhead():
    """Benchmark the overhead of applying the auto_retry decorator to async functions."""

    async def simple_async_function():
        return 42

    decorated = auto_retry(simple_async_function)
    result = asyncio.run(decorated())
    assert result == 42


@pytest.mark.benchmark
def test_async_timeout_handling():
    """Benchmark handling of asyncio.TimeoutError."""
    attempts = 0

    @auto_retry(min_sleep_time=0, max_sleep_time=0, max_retries=2)
    async def timeout_then_success():
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise asyncio.TimeoutError()
        return "success"

    result = asyncio.run(timeout_then_success())
    assert result == "success"
