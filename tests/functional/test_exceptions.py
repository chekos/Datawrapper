import pytest

from datawrapper import Datawrapper
from datawrapper.exceptions import FailedRequestError


def test_get_failed_request():
    """Test that FailedRequestError is imported correctly."""
    dw = Datawrapper(access_token="test")
    with pytest.raises(FailedRequestError):
        dw.get_my_account()
