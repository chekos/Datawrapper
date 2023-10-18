import pytest

from datawrapper import Datawrapper
from datawrapper.exceptions import FailedRequest


def test_get_failed_request():
    """Test that FailedRequest is imported correctly."""
    dw = Datawrapper(access_token="test")
    with pytest.raises(FailedRequest):
        dw.get_my_account()
