"""Test methods that use the /me endpoint."""

from datawrapper import Datawrapper


def test_get_my_account(monkeypatch):
    """Test the get_my_account method with mocked API response."""
    # Mock response data
    mock_account = {
        "id": 12345,
        "email": "test@example.com",
        "name": "Test User",
        "role": "editor",
        "language": "en-US",
    }

    def mock_get(self, url, **kwargs):
        """Mock get to return account data."""
        return mock_account

    # Patch the get method
    monkeypatch.setattr("datawrapper.Datawrapper.get", mock_get)

    # Test
    dw = Datawrapper()
    result = dw.get_my_account()
    assert isinstance(result, dict)
    assert result["id"] == 12345
    assert result["email"] == "test@example.com"


def test_update_my_account(monkeypatch):
    """Test update_my_account with mocked API response."""
    # Mock response data for different calls
    mock_account_foobar = {
        "id": 12345,
        "email": "test@example.com",
        "name": "Foobar",
        "role": "editor",
        "language": "en-US",
    }

    mock_account_test_user = {
        "id": 12345,
        "email": "test@example.com",
        "name": "Test user",
        "role": "editor",
        "language": "en-US",
    }

    # Track which call we're on
    call_count = [0]

    def mock_patch(self, url, **kwargs):
        """Mock patch to return updated account data."""
        call_count[0] += 1
        if call_count[0] == 1:
            return mock_account_foobar
        else:
            return mock_account_test_user

    # Patch the patch method
    monkeypatch.setattr("datawrapper.Datawrapper.patch", mock_patch)

    # Test
    dw = Datawrapper()
    result1 = dw.update_my_account(name="Foobar")
    assert result1["name"] == "Foobar"

    result2 = dw.update_my_account(name="Test user")
    assert result2["name"] == "Test user"


def test_get_my_recently_edited_charts(monkeypatch):
    """Test my_recently_edited_charts with mocked API response."""
    # Mock response data for different calls
    mock_response_default = {
        "list": [
            {"id": "abc123", "title": "Test Chart 1", "lastEditStep": 5},
            {"id": "def456", "title": "Test Chart 2", "lastEditStep": 4},
            {"id": "ghi789", "title": "Test Chart 3", "lastEditStep": 3},
        ],
        "total": 3,
    }

    mock_response_limit_1 = {
        "list": [
            {"id": "abc123", "title": "Test Chart 1", "lastEditStep": 5},
        ],
        "total": 3,
    }

    mock_response_limit_1_offset_2 = {
        "list": [
            {"id": "ghi789", "title": "Test Chart 3", "lastEditStep": 3},
        ],
        "total": 3,
    }

    mock_response_min_edit_step_3 = {
        "list": [
            {"id": "abc123", "title": "Test Chart 1", "lastEditStep": 5},
            {"id": "def456", "title": "Test Chart 2", "lastEditStep": 4},
            {"id": "ghi789", "title": "Test Chart 3", "lastEditStep": 3},
        ],
        "total": 3,
    }

    # Track which call we're on
    call_count = [0]

    def mock_get(self, url, **kwargs):
        """Mock get to return different responses based on call count."""
        call_count[0] += 1
        if call_count[0] == 1:
            return mock_response_default
        elif call_count[0] == 2:
            return mock_response_limit_1
        elif call_count[0] == 3:
            return mock_response_limit_1_offset_2
        else:
            return mock_response_min_edit_step_3

    # Patch the get method
    monkeypatch.setattr("datawrapper.Datawrapper.get", mock_get)

    # Test
    dw = Datawrapper()

    one = dw.get_my_recently_edited_charts()
    assert isinstance(one, dict)
    assert isinstance(one["list"], list)

    two = dw.get_my_recently_edited_charts(limit=1)
    assert isinstance(two["list"], list)

    three = dw.get_my_recently_edited_charts(limit=1, offset=2)
    assert isinstance(three["list"], list)

    four = dw.get_my_recently_edited_charts(min_last_edit_step=3)
    assert isinstance(four["list"], list)


def test_get_my_recently_published_charts(monkeypatch):
    """Test my_recently_published_charts with mocked API response."""
    # Mock response data for different calls
    mock_response_default = {
        "list": [
            {"id": "pub123", "title": "Published Chart 1", "publicVersion": 5},
            {"id": "pub456", "title": "Published Chart 2", "publicVersion": 3},
            {"id": "pub789", "title": "Published Chart 3", "publicVersion": 2},
        ],
        "total": 3,
    }

    mock_response_limit_1 = {
        "list": [
            {"id": "pub123", "title": "Published Chart 1", "publicVersion": 5},
        ],
        "total": 3,
    }

    mock_response_limit_1_offset_2 = {
        "list": [
            {"id": "pub789", "title": "Published Chart 3", "publicVersion": 2},
        ],
        "total": 3,
    }

    # Track which call we're on
    call_count = [0]

    def mock_get(self, url, **kwargs):
        """Mock get to return different responses based on call count."""
        call_count[0] += 1
        if call_count[0] == 1:
            return mock_response_default
        elif call_count[0] == 2:
            return mock_response_limit_1
        else:
            return mock_response_limit_1_offset_2

    # Patch the get method
    monkeypatch.setattr("datawrapper.Datawrapper.get", mock_get)

    # Test
    dw = Datawrapper()

    one = dw.get_my_recently_published_charts()
    assert isinstance(one, dict)
    assert isinstance(one["list"], list)

    two = dw.get_my_recently_published_charts(limit=1)
    assert isinstance(two["list"], list)

    three = dw.get_my_recently_published_charts(limit=1, offset=2)
    assert isinstance(three["list"], list)
