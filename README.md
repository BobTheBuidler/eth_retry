
# eth_retry
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
