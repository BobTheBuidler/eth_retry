# type: ignore

import asyncio
from eth_retry.eth_retry import auto_retry_async

from brownie import web3
from web3 import AsyncHTTPProvider, Web3
from web3.eth import AsyncEth

async_w3 = Web3(AsyncHTTPProvider(web3.provider.endpoint_uri))
async_w3.eth = AsyncEth(async_w3)

@auto_retry_async
async def do_work(w3):
    work = [w3.eth.chain_id for i in range(5000)]
    return await asyncio.gather(*work)

def test_auto_retry_sync():
    loop = asyncio.get_event_loop()
    _ = loop.run_until_complete(
        asyncio.gather(*[
            do_work(async_w3)
        ])
    )