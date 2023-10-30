"""Test the login token functions."""
from datawrapper import Datawrapper


def test_login_tokens():
    """Test login token methods."""
    # Create a client
    dw = Datawrapper()

    # Create a login token
    create = dw.create_login_token()

    # Get the list of login tokens
    get = dw.get_login_tokens()

    # Verify that the created id is in the get list
    assert create["id"] in [token["id"] for token in get["list"]]

    # Login with the token
    dw.login(create["token"])

    # Delete the login token
    dw.delete_login_token(create["id"])

    # Verify that the created id is not in the get list
    get2 = dw.get_login_tokens()
    assert create["id"] not in [token["id"] for token in get2["list"]]
