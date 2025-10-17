"""Test folder related API enpoints."""

from unittest.mock import MagicMock

from datawrapper import Datawrapper


def test_get_folders(monkeypatch):
    """Test the get_folders method with mocked API response."""
    # Mock response data
    mock_folders = {
        "list": [
            {"id": 1, "name": "Test Folder 1"},
            {"id": 2, "name": "Test Folder 2"},
        ],
        "total": 2,
    }

    # Create mock get method
    mock_get = MagicMock(return_value=mock_folders)

    # Patch the get method
    monkeypatch.setattr("datawrapper.Datawrapper.get", mock_get)

    # Test
    dw = Datawrapper()
    folder_list = dw.get_folders()
    assert len(folder_list["list"]) > 0


def test_folder_crud(monkeypatch):
    """Run folder related tests for creation, updating and deleting with mocked API."""
    # Mock response data
    mock_folder_1 = {
        "id": 12345,
        "name": "My new folder abc123",
        "parentId": None,
        "userId": 1,
        "teamId": None,
    }

    mock_folder_2 = {
        "id": 12346,
        "name": "My second folder abc123",
        "parentId": None,
        "userId": 1,
        "teamId": None,
    }

    mock_folder_2_with_parent = {
        "id": 12346,
        "name": "My second folder abc123",
        "parentId": 12345,
        "userId": 1,
        "teamId": None,
    }

    mock_folder_2_renamed = {
        "id": 12346,
        "name": "My second folder (renamed)",
        "parentId": 12345,
        "userId": 1,
        "teamId": None,
    }

    # Track which call we're on for get_folder
    get_folder_call_count = [0]

    def mock_get_folder(self, url, **kwargs):
        """Mock get_folder to return different responses based on call count."""
        get_folder_call_count[0] += 1
        if get_folder_call_count[0] == 1:
            return mock_folder_1
        elif get_folder_call_count[0] == 2:
            return mock_folder_2_with_parent
        else:
            return mock_folder_2_renamed

    # Track which call we're on for create_folder
    create_folder_call_count = [0]

    def mock_post(self, url, **kwargs):
        """Mock post to return different folder data based on call count."""
        create_folder_call_count[0] += 1
        if create_folder_call_count[0] == 1:
            return mock_folder_1
        else:
            return mock_folder_2

    def mock_patch(self, url, **kwargs):
        """Mock patch to return updated folder data."""
        if "parentId" in kwargs.get("data", {}):
            return mock_folder_2_with_parent
        else:
            return mock_folder_2_renamed

    def mock_delete(self, url, **kwargs):
        """Mock delete to return True."""
        return True

    # Patch all the methods
    monkeypatch.setattr("datawrapper.Datawrapper.get", mock_get_folder)
    monkeypatch.setattr("datawrapper.Datawrapper.post", mock_post)
    monkeypatch.setattr("datawrapper.Datawrapper.patch", mock_patch)
    monkeypatch.setattr("datawrapper.Datawrapper.delete", mock_delete)

    # Connect
    dw = Datawrapper()

    # Create a new folder
    folder_info = dw.create_folder(name="My new folder abc123")
    assert folder_info["id"] == 12345

    # Get the folder's data with a fresh get_folder call
    folder_info = dw.get_folder(folder_info["id"])
    assert folder_info["id"] == 12345

    # Make a second folder
    second_folder_info = dw.create_folder(name="My second folder abc123")
    assert second_folder_info["id"] == 12346

    # Move the second folder into the first folder
    dw.update_folder(folder_id=second_folder_info["id"], parent_id=folder_info["id"])

    # Get the folder's data with a fresh get_folder call
    second_folder_info = dw.get_folder(second_folder_info["id"])

    # Verify it has the parent
    assert second_folder_info["parentId"] == folder_info["id"]

    # Change the name of the second folder
    dw.update_folder(
        folder_id=second_folder_info["id"], name="My second folder (renamed)"
    )

    # Get it fresh and verify the change
    second_folder_info = dw.get_folder(second_folder_info["id"])
    assert second_folder_info["name"] == "My second folder (renamed)"

    # Delete both folders
    result = dw.delete_folder(folder_info["id"])
    assert result is True
