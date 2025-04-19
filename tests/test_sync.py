# type: ignore

from brownie import web3
from eth_retry.eth_retry import auto_retry
from joblib import Parallel, delayed


@auto_retry
def do_work(w3):
    Parallel(100, "threading")(delayed(getattr)(w3.eth, "chain_id") for _ in range(5000))


def test_auto_retry_sync():
    do_work(web3)
