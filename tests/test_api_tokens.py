"""Test the API token functions."""
from datawrapper import Datawrapper


def test_api_tokens():
    """Test login token methods."""
    # Create a client
    dw = Datawrapper()

    # Create a new login token
    comment = "Test comment"
    scopes = ["chart:read"]
    create = dw.create_api_token(comment, scopes)

    # Get all login tokens
    get = dw.get_api_tokens()

    # Verify that the created token is in the list of all tokens
    assert create["id"] in [token["id"] for token in get["list"]]

    # Upload the comment and scopes
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
