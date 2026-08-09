# type: ignore
import pytest
from brownie import web3
from joblib import Parallel, delayed

from eth_retry.eth_retry import auto_retry


@auto_retry
def do_work(w3):
    Parallel(100, "threading")(delayed(getattr)(w3.eth, "chain_id") for _ in range(5000))


def test_auto_retry_sync():
    do_work(web3)


def test_max_retries_type_error():
    with pytest.raises(TypeError):

        @auto_retry(max_retries="3")
        def fail(): ...


def test_min_sleep_time_type_error():
    with pytest.raises(TypeError):

        @auto_retry(min_sleep_time="3")
        def fail(): ...


def test_max_sleep_time_type_error():
    with pytest.raises(TypeError):

        @auto_retry(max_sleep_time="3")
        def fail(): ...


def test_suppress_logs_type_error():
    with pytest.raises(TypeError):

        @auto_retry(suppress_logs="3")
        def fail(): ...
