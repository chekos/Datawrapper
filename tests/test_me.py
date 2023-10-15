"""Test methods that use the /me endpoint."""
from datawrapper import Datawrapper


def test_get_my_account():
    """Test the get_my_account method."""
    dw = Datawrapper()
    assert isinstance(dw.get_my_account(), dict)