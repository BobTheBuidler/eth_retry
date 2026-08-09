# type: ignore


class DummyException(Exception):
    pass


# eth-brownie
try:
    from sqlite3 import OperationalError
except ModuleNotFoundError:
    OperationalError = DummyException

# web3py
try:
    from requests.exceptions import HTTPError, ReadTimeout
except ModuleNotFoundError:
    HTTPError, ReadTimeout = DummyException, DummyException

# aiohttp
try:
    from aiohttp import ClientError
    from aiohttp import ClientResponseError
except ModuleNotFoundError:
    ClientError, ClientResponseError = DummyException, DummyException

# urllib
try:
    from urllib3.exceptions import MaxRetryError
except ModuleNotFoundError:
    MaxRetryError = DummyException
