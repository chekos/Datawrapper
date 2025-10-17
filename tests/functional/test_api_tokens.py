"""Test the API token functions with mocked API calls."""

from unittest.mock import patch

from datawrapper import Datawrapper


def test_api_tokens():
    """Test API token methods with mocked API."""
    with (
        patch.object(Datawrapper, "post") as mock_post,
        patch.object(Datawrapper, "get") as mock_get,
        patch.object(Datawrapper, "put") as mock_put,
        patch.object(Datawrapper, "delete") as mock_delete,
    ):
        # Mock the create_api_token response
        mock_token_id = "test_api_token_123"
        mock_post.return_value = {
            "id": mock_token_id,
            "comment": "Test comment",
            "scopes": ["chart:read"],
            "created_at": "2024-01-15T10:00:00Z",
        }

        # Mock the get_api_tokens responses
        # First call: includes the created token with original comment/scopes
        mock_get_with_token_original = {
            "list": [
                {
                    "id": mock_token_id,
                    "comment": "Test comment",
                    "scopes": ["chart:read"],
                    "created_at": "2024-01-15T10:00:00Z",
                    "last_used": None,
                },
                {
                    "id": "other_token_456",
                    "comment": "Other token",
                    "scopes": ["chart:read", "chart:write"],
                    "created_at": "2024-01-10T08:00:00Z",
                    "last_used": "2024-01-14T12:00:00Z",
                },
            ]
        }

        # Second call: includes the token with updated comment/scopes
        mock_get_with_token_updated = {
            "list": [
                {
                    "id": mock_token_id,
                    "comment": "Test comment",
                    "scopes": ["chart:read", "chart:write"],
                    "created_at": "2024-01-15T10:00:00Z",
                    "last_used": None,
                },
                {
                    "id": "other_token_456",
                    "comment": "Other token",
                    "scopes": ["chart:read", "chart:write"],
                    "created_at": "2024-01-10T08:00:00Z",
                    "last_used": "2024-01-14T12:00:00Z",
                },
            ]
        }

        # Third call: token has been deleted
        mock_get_without_token = {
            "list": [
                {
                    "id": "other_token_456",
                    "comment": "Other token",
                    "scopes": ["chart:read", "chart:write"],
                    "created_at": "2024-01-10T08:00:00Z",
                    "last_used": "2024-01-14T12:00:00Z",
                }
            ]
        }

        # Set up side_effect for multiple get calls
        mock_get.side_effect = [
            mock_get_with_token_original,
            mock_get_with_token_updated,
            mock_get_without_token,
        ]

        # Mock the update response (typically returns True or success status)
        mock_put.return_value = True

        # Mock the delete response (typically returns True or success status)
        mock_delete.return_value = True

        # Create a client
        dw = Datawrapper()

        # Create a new API token
        comment = "Test comment"
        scopes = ["chart:read"]
        create = dw.create_api_token(comment, scopes)

        # Get all API tokens
        get = dw.get_api_tokens()

        # Verify that the created token is in the list of all tokens
        assert create["id"] in [token["id"] for token in get["list"]]

        # Update the comment and scopes
        comment = "Test comment"
        scopes = ["chart:read", "chart:write"]
        update = dw.update_api_token(create["id"], comment, scopes)
        assert update is True

        # Verify that the comment and scopes were updated
        get = dw.get_api_tokens()
        get_item = [token for token in get["list"] if token["id"] == create["id"]][0]
        assert get_item["comment"] == comment
        assert get_item["scopes"] == scopes

        # Delete the token
        delete = dw.delete_api_token(create["id"])

        # Verify that the token was deleted
        assert delete is True

        # Verify that the token is no longer in the list of all tokens
        get = dw.get_api_tokens()
        assert create["id"] not in [token["id"] for token in get["list"]]

        # Verify all expected calls were made
        mock_post.assert_called_once()
        assert mock_get.call_count == 3  # get_api_tokens called 3 times
        mock_put.assert_called_once()
        mock_delete.assert_called_once()
