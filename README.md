
# eth_retry

[![CodSpeed](https://img.shields.io/badge/CodSpeed-Performance_Monitoring-blue?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTggMTVDMTEuODY2IDE1IDE1IDExLjg2NiAxNSA4QzE1IDQuMTM0IDExLjg2NiAxIDggMUM0LjEzNCAxIDEgNC4xMzQgMSA4QzEgMTEuODY2IDQuMTM0IDE1IDggMTVaIiBzdHJva2U9IiMxRjIzMjgiIHN0cm9rZS13aWR0aD0iMS41IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPHBhdGggZD0iTTggNVY4TDEwLjUgMTAuNSIgc3Ryb2tlPSIjMUYyMzI4IiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=)](https://codspeed.io/BobTheBuidler/eth_retry?utm_source=badge)

> Stop transient errors from wasting your time!

`eth_retry` is a Python library that provides one decorator, `eth_retry.auto_retry`.

`auto_retry` will automatically catch known transient exceptions that are common in the Ethereum/EVM ecosystem and will reattempt to evaluate your decorated function up to `os.environ['MAX_RETRIES']` (default: 10) times.

Supports both synchronous and asynchronous functions.

------------

Covers many common transient errors in the EVM ecosystem, including:
- RPC timeouts
- Block explorer API rate-limiting
- Generic exceptions:
  - ConnectionError
  - HTTPError
  - ReadTimeout
  - TimeoutError
- eth-brownie specific errors:
  - sqlite3.OperationalError: database is locked

## Installation:
`pip install eth_retry`
or
`pip install git+https://github.com/BobTheBuidler/eth_retry.git`

## Usage:
```
import eth_retry

@eth_retry.auto_retry
def some_function_that_errors_sometimes():
    i = 0
    am = 1
    doing = 2
    stuff = 3
    return stuff

error_free_result = some_function_that_errors_sometimes()
```

Between attempts, eth_retry will `time.sleep` for a random period between `os.environ['MIN_SLEEP_TIME']` (default: 10) and `os.environ['MAX_SLEEP_TIME']` (default: 20) seconds. The period is randomized to help prevent repetitive rate-limiting issues with parallelism by staggering the retries.

On the `n`th retry, the sleep period is multiplied by `n` so that the target endpoint can cool off in case of rate-limiting.

After `os.environ['MAX_RETRIES']` failures, eth_retry will raise the exception.

## Environment:
```
# Minimum sleep time in seconds. Integer. Defaults to 10.
MIN_SLEEP_TIME=10

# Maximum sleep time in seconds. Integer. Defaults to 20.
MAX_SLEEP_TIME=20

# Maximum number of times to retry. Integer. Defaults to 10.
MAX_RETRIES=10
```
