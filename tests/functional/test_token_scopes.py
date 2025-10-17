"""Test the token scope functions."""

from unittest.mock import patch

from datawrapper import Datawrapper


def test_token_scopes():
    """Test token scopes."""
    with patch.object(Datawrapper, "get") as mock_get:
        # Setup mock response
        mock_get.return_value = [
            "chart:read",
            "chart:write",
            "visualization:read",
            "visualization:write",
            "theme:read",
            "folder:read",
        ]

        # Create a client
        dw = Datawrapper()

        # Get scopes
        scopes = dw.get_token_scopes()

        # Assert it's a list
        assert isinstance(scopes, list)
        assert len(scopes) > 0
        assert "chart:read" in scopes

        # Verify the mock was called correctly
        mock_get.assert_called_once_with(
            "https://api.datawrapper.de/v3/auth/token-scopes"
        )
