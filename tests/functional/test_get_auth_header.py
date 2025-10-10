"""Test the auth header getter function."""

from datawrapper import Datawrapper


def test_get_auth_header():
    """Test the auth header getter function."""
    dw = Datawrapper(access_token="test-token")
    auth_header = dw._get_auth_header()
    assert auth_header["Authorization"] == f"Bearer {dw._access_token}"

    auth_header["content-type"] = "text/csv"

    second_auth_header = dw._get_auth_header()
    # The auth header should not be modified
    assert second_auth_header.get("content-type") is None
