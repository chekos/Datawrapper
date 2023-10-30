"""Test the user methods."""
from datawrapper import Datawrapper


def test_get_user():
    """Test the get user method."""
    # Connect
    dw = Datawrapper()

    # Get the user list
    get = dw.get_users()

    # Verify format of data
    assert isinstance(get, dict)
    assert isinstance(get["list"], list)

    # Get the first user
    my_id = dw.get_my_account()["id"]
    user = dw.get_user(my_id)
    assert isinstance(user, dict)
    assert user["id"] == my_id
