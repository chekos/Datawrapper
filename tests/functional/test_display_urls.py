"""Test display URLs functions."""

from unittest.mock import patch

from datawrapper import Datawrapper


def test_get_chart_display_urls():
    """Test get_chart_display_urls function."""
    with patch.object(Datawrapper, "get") as mock_get:
        # Setup mock response
        mock_get.return_value = [
            {
                "id": "abc123",
                "url": "https://datawrapper.dwcdn.net/WpAbK/1/",
                "type": "responsive",
            },
            {
                "id": "def456",
                "url": "https://datawrapper.dwcdn.net/WpAbK/plain.png",
                "type": "static-image",
            },
        ]

        # Create client and call method
        dw = Datawrapper()
        data = dw.get_chart_display_urls("WpAbK")

        # Verify it contains a list of dictionaries
        assert isinstance(data, list)
        assert isinstance(data[0], dict)
        assert "url" in data[0]
        assert "type" in data[0]

        # Verify the mock was called once
        mock_get.assert_called_once()
