"""Test the login token functions with mocked API calls."""

from unittest.mock import patch

from datawrapper import Datawrapper


def test_login_tokens():
    """Test login token methods with mocked API."""
    with (
        patch.object(Datawrapper, "post") as mock_post,
        patch.object(Datawrapper, "get") as mock_get,
        patch.object(Datawrapper, "delete") as mock_delete,
    ):
        # Mock the create_login_token response
        mock_token_id = "test_token_123"
        mock_token_value = "dw_test_token_abc123xyz"
        mock_post.return_value = {
            "id": mock_token_id,
            "token": mock_token_value,
            "created_at": "2024-01-15T10:00:00Z",
        }

        # Mock the get_login_tokens responses
        # First call: includes the created token
        mock_get_with_token = {
            "list": [
                {
                    "id": mock_token_id,
                    "created_at": "2024-01-15T10:00:00Z",
                    "last_used": None,
                },
                {
                    "id": "other_token_456",
                    "created_at": "2024-01-10T08:00:00Z",
                    "last_used": "2024-01-14T12:00:00Z",
                },
            ]
        }

        # Second call: login() method response (returns HTML)
        mock_login_response = "<html><body>Login successful</body></html>"

        # Third call: token has been deleted
        mock_get_without_token = {
            "list": [
                {
                    "id": "other_token_456",
                    "created_at": "2024-01-10T08:00:00Z",
                    "last_used": "2024-01-14T12:00:00Z",
                }
            ]
        }

        # Set up side_effect for multiple get calls
        mock_get.side_effect = [
            mock_get_with_token,
            mock_login_response,
            mock_get_without_token,
        ]

        # Mock the delete response (typically returns empty or success status)
        mock_delete.return_value = {}

        # Create a client
        dw = Datawrapper()

        # Create a login token
        create = dw.create_login_token()

        # Get the list of login tokens
        get = dw.get_login_tokens()

        # Verify that the created id is in the get list
        assert create["id"] in [token["id"] for token in get["list"]]

        # Login with the token (this would normally set the token in the client)
        dw.login(create["token"])

        # Delete the login token
        dw.delete_login_token(create["id"])

        # Verify that the created id is not in the get list
        get2 = dw.get_login_tokens()
        assert create["id"] not in [token["id"] for token in get2["list"]]

        # Verify all expected calls were made
        mock_post.assert_called_once()
        assert mock_get.call_count == 3  # get_login_tokens (2x) + login (1x)
        mock_delete.assert_called_once()
