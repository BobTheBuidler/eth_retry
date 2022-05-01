# type: ignore

from brownie import web3
from eth_retry.eth_retry import auto_retry

@auto_retry
def do_work(w3):
    work = [w3.eth.chain_id for i in range(5000)]
    return work

def test_auto_retry_sync():
    do_work(web3)