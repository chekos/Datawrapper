"""Test the API token functions."""
from datawrapper import Datawrapper


def test_api_tokens():
    """Test login token methods."""
    # Create a client
    dw = Datawrapper()

    # Get all login tokens
    dw.get_api_tokens()
