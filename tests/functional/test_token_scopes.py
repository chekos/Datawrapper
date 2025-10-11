"""Test the token scope functions."""

import pytest

from datawrapper import Datawrapper


@pytest.mark.api
def test_token_scopes():
    """Test token scopes."""
    # Create a client
    dw = Datawrapper()

    # Get scopes
    scopes = dw.get_token_scopes()

    # Assert it's a list
    assert isinstance(scopes, list)
