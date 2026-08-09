import os

import eth_retry.eth_retry as er


def _caller():
    return er._get_caller_details_from_stack()


def test_get_caller_details_from_stack_returns_location():
    details = _caller()
    assert details is not None
    assert os.path.basename(__file__) in details
