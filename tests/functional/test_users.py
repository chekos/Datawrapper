"""Test the user methods."""

from unittest.mock import Mock, patch

import pytest

from datawrapper import Datawrapper


@pytest.mark.api
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
    """Test the user editing methods using mocked API calls."""
    # Mock account data
    mock_account = {
        "id": "test-user-123",
        "name": "Original Name",
        "email": "test@example.com",
    }

    with patch("tests.functional.test_users.Datawrapper") as mock_dw_class:
        # Create mock client instance
        mock_client = Mock()
        mock_dw_class.return_value = mock_client

        # Mock get_my_account to return our test account
        mock_client.get_my_account.return_value = mock_account.copy()

        # Track update calls to return appropriate user state
        update_call_count = 0

        def mock_get_user(user_id):
            nonlocal update_call_count
            # Return state based on how many updates have been called
            if update_call_count == 1:
                # After first update
                return {**mock_account, "name": "Test User"}
            elif update_call_count >= 2:
                # After reset
                return mock_account.copy()
            else:
                # Initial state
                return mock_account.copy()

        def mock_update_user(user_id, **kwargs):
            nonlocal update_call_count
            update_call_count += 1
            return None

        mock_client.get_user.side_effect = mock_get_user
        mock_client.update_user.side_effect = mock_update_user

        # Now run the actual test logic
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

        # Verify the API calls were made correctly
        assert mock_client.get_my_account.call_count == 1
        assert mock_client.update_user.call_count == 2
        assert mock_client.get_user.call_count == 2
