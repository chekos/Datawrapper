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

    # Get recently edited and published charts
    charts = dw.get_recently_edited_charts(user["id"])
    assert isinstance(charts, dict)

    charts = dw.get_recently_published_charts(user["id"])
    assert isinstance(charts, dict)


def test_edit_user():
    """Test the user editing methods."""
    # Connect
    dw = Datawrapper()

    # Get my account
    my_account = dw.get_my_account()
    my_id = my_account["id"]

    # Edit my account
    dw.update_user(my_id, name="Test User")

    # Get my account again
    user = dw.get_user(my_id)
    assert user["name"] == "Test User"

    # Reset my account
    dw.update_user(my_id, name=my_account["name"])

    # Get my account again
    user = dw.get_user(my_id)
    assert user["name"] == my_account["name"]
