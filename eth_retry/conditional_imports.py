
class DummyException(Exception):
    pass

try:
    from sqlite3 import OperationalError
except ModuleNotFoundError:
    OperationalError = DummyException # type: ignore

try:
    from requests.exceptions import HTTPError, ReadTimeout # type: ignore
except ModuleNotFoundError:
    HTTPError, ReadTimeout = DummyException, DummyException # type: ignore
