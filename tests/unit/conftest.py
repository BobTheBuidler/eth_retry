import importlib

import eth_retry.ENVIRONMENT_VARIABLES as envs
import eth_retry.eth_retry as er
import pytest


def _reload_eth_retry():
    importlib.reload(envs)
    importlib.reload(er)
    return er


@pytest.fixture(autouse=True)
def _reload_defaults():
    _reload_eth_retry()
    yield


@pytest.fixture
def reload_eth_retry(monkeypatch):
    def _reload(**env):
        for key, value in env.items():
            if value is None:
                monkeypatch.delenv(key, raising=False)
            else:
                monkeypatch.setenv(key, value)
        return _reload_eth_retry()

    return _reload
