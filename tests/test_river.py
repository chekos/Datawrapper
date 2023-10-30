"""Test River functions."""
from datawrapper import Datawrapper


def test_get_river():
    """Test the get_river function."""
    # Create a client
    dw = Datawrapper()

    # Get the river
    river = dw.get_river()["list"]

    # Verify that the river is a list
    assert isinstance(river, list)
    assert len(river) > 0
    assert isinstance(river[0], dict)
    assert "id" in river[0]
    assert "title" in river[0]
