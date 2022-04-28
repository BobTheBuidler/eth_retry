# type: ignore

class DummyException(Exception):
    pass

try:
    from sqlite3 import OperationalError
except ModuleNotFoundError:
    OperationalError = DummyException

try:
    from requests.exceptions import HTTPError, ReadTimeout
except ModuleNotFoundError:
    HTTPError, ReadTimeout = DummyException, DummyException
