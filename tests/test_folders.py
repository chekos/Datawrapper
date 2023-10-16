"""Test folder related API enpoints."""
import random
import string

from datawrapper import Datawrapper


def test_get_folders():
    """Test the get_folders method."""
    dw = Datawrapper()
    folder_list = dw.get_folders()
    assert len(folder_list) > 0


def test_folder_crud():
    """Run folder related tests for creation, updating and deleting."""
    # Connect
    dw = Datawrapper()

    # Get a randoms string suffix to use in our names
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))

    # Create a new folder
    folder_info = dw.create_folder(name="My new folder " + suffix)

    # Get the folder's data with a fresh get_folder call
    folder_info = dw.get_folder(folder_info["id"])

    # Make a second folder
    second_folder_info = dw.create_folder(name="My second folder " + suffix)

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
    dw.delete_folder(folder_info["id"])
