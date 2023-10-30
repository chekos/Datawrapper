"""Test oembed functions."""
from datawrapper import Datawrapper


def test_get_oembed():
    """Test get_oembed function."""
    dw = Datawrapper()

    # Get oembed data for a chart
    url = "https://datawrapper.dwcdn.net/WpAbK/2/"
    data = dw.get_oembed(url)

    # Verify that the oembed data is correct
    assert data["type"] == "rich"
    assert data["version"] == "1.0"
    assert data["title"] == "<strong>More than Earth can handle</strong>"
    assert data["width"] == "600"
    assert data["height"] == "500"

    # Request it with a different height and width
    data = dw.get_oembed(url, max_width=300, max_height=300)

    # Verify that the oembed data is correct
    assert data["width"] == 300
    assert data["height"] == 250

    # Request it as an iframe format
    dw.get_oembed(url, iframe=True)
