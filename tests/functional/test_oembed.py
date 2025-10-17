"""Test oembed functions with mocked API calls."""

from unittest.mock import patch

from datawrapper import Datawrapper


def test_get_oembed():
    """Test get_oembed function with mocked API."""
    with patch.object(Datawrapper, "get") as mock_get:
        # Mock oembed response for default parameters
        mock_oembed_default = {
            "type": "rich",
            "version": "1.0",
            "title": "<strong>More than Earth can handle</strong>",
            "width": "600",
            "height": "500",
            "html": '<iframe src="https://datawrapper.dwcdn.net/WpAbK/2/" width="600" height="500"></iframe>',
        }

        # Mock oembed response for custom dimensions
        mock_oembed_custom = {
            "type": "rich",
            "version": "1.0",
            "title": "<strong>More than Earth can handle</strong>",
            "width": 300,
            "height": 250,
            "html": '<iframe src="https://datawrapper.dwcdn.net/WpAbK/2/" width="300" height="250"></iframe>',
        }

        # Mock oembed response for iframe format
        mock_oembed_iframe = {
            "type": "rich",
            "version": "1.0",
            "title": "<strong>More than Earth can handle</strong>",
            "width": "600",
            "height": "500",
            "html": '<iframe src="https://datawrapper.dwcdn.net/WpAbK/2/" width="600" height="500"></iframe>',
        }

        # Set up side_effect to return different values for each call
        mock_get.side_effect = [
            mock_oembed_default,
            mock_oembed_custom,
            mock_oembed_iframe,
        ]

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

        # Verify the calls were made
        assert mock_get.call_count == 3


if __name__ == "__main__":
    # Run the tests directly
    test_get_oembed()
    print("✅ test_get_oembed passed")

    print("\n🎉 All mocked oembed tests completed successfully!")
