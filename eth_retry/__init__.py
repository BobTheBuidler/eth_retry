import functools
import logging
import os
from random import randrange
from time import sleep
from typing import Any, Callable

from eth_retry.conditional_imports import (HTTPError,  # type: ignore
                                           OperationalError, ReadTimeout)

logger = logging.getLogger('eth_retry')

MIN_SLEEP_TIME = int(os.environ.get("MIN_SLEEP_TIME", 10))
MAX_SLEEP_TIME = int(os.environ.get("MAX_SLEEP_TIME", 20))
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", 10))


def auto_retry(func: Callable[...,Any]) -> Callable[...,Any]:
    '''
    Decorator that will retry the function on:
    - ConnectionError
    - HTTPError
    - TimeoutError
    - ReadTimeout
    
    It will also retry on specific ValueError exceptions:
    - Max rate limit reached
    - please use API Key for higher rate limit
    - execution aborted (timeout = 5s)
    
    On repeat errors, will retry in increasing intervals.
    '''

    @functools.wraps(func)
    def auto_retry_wrap(*args: Any, **kwargs: Any) -> Any:
        failures = 0
        sleep_time = randrange(MIN_SLEEP_TIME,MAX_SLEEP_TIME)
        while True:

            # Attempt to execute `func` and return response
            try:
                return func(*args, **kwargs)

            # Generic exceptions
            except (ConnectionError, HTTPError, TimeoutError, ReadTimeout) as e:
                # This happens when we pass too large of a request to the node. Do not retry.
                if failures > MAX_RETRIES or 'Too Large' in str(e) or '404' in str(e):
                    raise
                logger.warning(f'{str(e)} [{failures}]')
            
            # Specific exceptions
            except OperationalError as e:
                # This happens when brownie's deployments.db gets locked. Just retry.
                if failures > MAX_RETRIES or 'database is locked' not in str(e):
                    raise
                logger.warning(f'{str(e)} [{failures}]')
            except ValueError as e:
                retry_on_errs = (
                    # Occurs on any chain when making computationally intensive calls. Just retry.
                    # Sometimes works, sometimes doesn't. Worth a shot.
                    'execution aborted (timeout = 5s)',

                    # From block explorer while interacting with api. Just retry.
                    'Max rate limit reached',
                    'please use API Key for higher rate limit',

                    # Occurs occasionally on AVAX when node is slow to sync. Just retry.
                    'after last accepted block',
                )
                if failures > MAX_RETRIES or not any(err in str(e) for err in retry_on_errs):
                    raise
                logger.warning(f'{str(e)} [{failures}]')
            
            # Attempt failed, sleep time
            failures += 1
            sleep(failures * sleep_time)

    return auto_retry_wrap
