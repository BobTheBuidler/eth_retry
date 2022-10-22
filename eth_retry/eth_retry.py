import asyncio
import functools
import inspect
import logging
import os
import sys
from json import JSONDecodeError
from random import randrange
from time import sleep
from typing import Any, Awaitable, Callable, TypeVar, Union, overload

import requests

from eth_retry.conditional_imports import ClientError  # type: ignore
from eth_retry.conditional_imports import HTTPError  # type: ignore
from eth_retry.conditional_imports import MaxRetryError  # type: ignore
from eth_retry.conditional_imports import OperationalError  # type: ignore
from eth_retry.conditional_imports import ReadTimeout  # type: ignore

logger = logging.getLogger('eth_retry')

# Environment
MIN_SLEEP_TIME = int(os.environ.get("MIN_SLEEP_TIME", 10))
MAX_SLEEP_TIME = int(os.environ.get("MAX_SLEEP_TIME", 20))
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", 10))

# Types
T = TypeVar("T")
if sys.version_info >= (3, 10):
    from typing import ParamSpec
    P = ParamSpec("P")
    Function = Callable[P ,T]
    CoroutineFunction = Function[Awaitable[T]]
    Decoratee = Union[Function[P, T], CoroutineFunction[P, T]]
else:
    Function = Callable[..., T]
    CoroutineFunction = Function[Awaitable[T]]
    Decoratee = Union[Function[T], CoroutineFunction[T]]

@overload
def auto_retry(func: CoroutineFunction[T]) -> CoroutineFunction[T]:...
    
@overload
def auto_retry(func: Function[T]) -> Function[T]:...

def auto_retry(func: Decoratee[T]):  # type: ignore
    '''
    Decorator that will retry the function on:
    - ConnectionError
    - requests.exceptions.ConnectionError
    - HTTPError
    - asyncio.exceptions.TimeoutError
    - ReadTimeout
    
    It will also retry on specific ValueError exceptions:
    - Max rate limit reached
    - please use API Key for higher rate limit
    - execution aborted (timeout = 5s)
    - parse error
    
    On repeat errors, will retry in increasing intervals.
    '''

    @functools.wraps(func)
    def auto_retry_wrap(*args: Any, **kwargs: Any) -> T:
        sleep_time = randrange(MIN_SLEEP_TIME,MAX_SLEEP_TIME)
        failures = 0
        while True:
            # Attempt to execute `func` and return response
            try:
                return func(*args, **kwargs)  # type: ignore
            except Exception as e:
                if not should_retry(e, failures):
                    raise
                logger.warning(f'{str(e)} [{failures}]')
            
            # Attempt failed, sleep time.
            failures += 1
            sleep(failures * sleep_time)

    @functools.wraps(func)
    async def auto_retry_wrap_async(*args: Any, **kwargs: Any) -> T:
        sleep_time = randrange(MIN_SLEEP_TIME,MAX_SLEEP_TIME)
        failures = 0
        while True:
            try:
                return await func(*args,**kwargs)  # type: ignore
            except asyncio.exceptions.TimeoutError:
                logger.warning(f'asyncio timeout [{failures}] {_get_caller_details_from_stack()}')
                continue
            except Exception as e:
                if not should_retry(e, failures):
                    raise
                logger.warning(f'{str(e)} [{failures}]')
            
            # Attempt failed, sleep time.
            failures += 1
            await asyncio.sleep(failures * sleep_time)

    if asyncio.iscoroutinefunction(func):
        return auto_retry_wrap_async
    return auto_retry_wrap

            
def should_retry(e: Exception, failures: int) -> bool:
    if failures > MAX_RETRIES:
        return False

    retry_on_errs = (
        # Occurs on any chain when making computationally intensive calls. Just retry.
        # Sometimes works, sometimes doesn't. Worth a shot.
        'execution aborted (timeout = 5s)',
        'max retries exceeded with url',
        'temporary failure in name resolution',
        'parse error',

        # From block explorer while interacting with api. Just retry.
        'max rate limit reached',
        'please use api key for higher rate limit',

        # Occurs occasionally on AVAX when node is slow to sync. Just retry.
        'after last accepted block',

        # The standard Moralis rate limiting message. Just retry.
        'too many requests'
      
        # You get this ssl error in docker sometimes
        'cannot assign requested address',
    )
    if any(err in str(e).lower() for err in retry_on_errs):
        return True
    
    general_exceptions = [
        ConnectionError,
        requests.exceptions.ConnectionError,
        HTTPError,
        ReadTimeout,
        MaxRetryError,
        JSONDecodeError,
        ClientError,
    ]
    if any(isinstance(e, E) for E in general_exceptions) and 'Too Large' not in str(e) and '404' not in str(e):
        return True
    # This happens when brownie's deployments.db gets locked. Just retry.
    elif isinstance(e, OperationalError) and 'database is locked' in str(e):
        return True

    return False


def _get_caller_details_from_stack() -> str:
    code_context = inspect.stack()[2].code_context
    if code_context is None:
        return f"{inspect.stack()[2].filename} line {inspect.stack()[2].lineno}"
    return f"{inspect.stack()[2].filename} line {inspect.stack()[2].lineno} {[code_context[0].strip()]}"
