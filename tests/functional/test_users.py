"""Test the user methods."""

from unittest.mock import Mock, patch

from datawrapper import Datawrapper


def test_get_user(monkeypatch):
    """Test the get user method with mocked API responses."""
    # Mock response data
    mock_user_id = "test-user-123"

    mock_users_list = {
        "list": [
            {"id": mock_user_id, "name": "Test User", "email": "test@example.com"},
            {"id": "user-456", "name": "Another User", "email": "another@example.com"},
        ],
        "total": 2,
    }

    mock_account = {
        "id": mock_user_id,
        "name": "Test User",
        "email": "test@example.com",
        "role": "editor",
    }

    mock_user = {
        "id": mock_user_id,
        "name": "Test User",
        "email": "test@example.com",
        "role": "editor",
    }

    mock_edited_charts = {
        "list": [
            {"id": "chart1", "title": "Edited Chart 1"},
            {"id": "chart2", "title": "Edited Chart 2"},
        ],
        "total": 2,
    }

    mock_published_charts = {
        "list": [
            {"id": "chart3", "title": "Published Chart 1"},
            {"id": "chart4", "title": "Published Chart 2"},
        ],
        "total": 2,
    }

    # Track which call we're on
    call_count = [0]

    def mock_get(self, url, **kwargs):
        """Mock get to return different responses based on URL."""
        call_count[0] += 1
        if call_count[0] == 1:
            # First call: get_users()
            return mock_users_list
        elif call_count[0] == 2:
            # Second call: get_my_account()
            return mock_account
        elif call_count[0] == 3:
            # Third call: get_user(my_id)
            return mock_user
        elif call_count[0] == 4:
            # Fourth call: get_recently_edited_charts(user_id)
            return mock_edited_charts
        else:
            # Fifth call: get_recently_published_charts(user_id)
            return mock_published_charts

    # Patch the get method
    monkeypatch.setattr("datawrapper.Datawrapper.get", mock_get)

    # Test
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
