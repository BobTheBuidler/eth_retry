import json
import os
from typing import Any

import aiohttp
import requests
from brownie import network


def _build_rpc_response(request_body: Any) -> dict[str, Any]:
    payload = request_body if isinstance(request_body, dict) else request_body[0]
    method = payload.get("method")
    request_id = payload.get("id", 1)
    if method == "web3_clientVersion":
        result = "MockClient/0.0.0"
    else:
        result = "0x1"
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


class _MockResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.status_code = 200
        self._payload = payload
        self.content = json.dumps(payload).encode()

    def raise_for_status(self) -> None:
        return None


class _AsyncMockResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    async def read(self) -> bytes:
        return json.dumps(self._payload).encode()


def _mock_requests_post(self: requests.Session, url: str, *args: Any, **kwargs: Any) -> _MockResponse:
    data = kwargs.get("data") or (args[0] if args else None)
    request_body = json.loads(data) if isinstance(data, (bytes, str)) else data
    return _MockResponse(_build_rpc_response(request_body))


async def _mock_aiohttp_post(
    self: aiohttp.ClientSession, url: str, *args: Any, **kwargs: Any
) -> _AsyncMockResponse:
    data = kwargs.get("data") or (args[0] if args else None)
    request_body = json.loads(data) if isinstance(data, (bytes, str)) else data
    return _AsyncMockResponse(_build_rpc_response(request_body))


setattr(requests.Session, "post", _mock_requests_post)
setattr(aiohttp.ClientSession, "post", _mock_aiohttp_post)

os.environ.setdefault("PYTEST_NETWORK", "mainnet")
os.environ.setdefault("WEB3_INFURA_PROJECT_ID", "test")

network.connect(os.environ["PYTEST_NETWORK"])
