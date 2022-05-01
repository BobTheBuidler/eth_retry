# type: ignore

import os

from brownie import network

network.connect(os.environ["PYTEST_NETWORK"])
