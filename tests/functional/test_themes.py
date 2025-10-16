"""Test themes related API endpoints."""

from unittest.mock import patch

from datawrapper import Datawrapper


def test_get_themes():
    """Test the get_themes method."""
    with patch.object(Datawrapper, "get") as mock_get:
        # Setup mock responses for different calls
        def mock_get_side_effect(path, **kwargs):
            params = kwargs.get("params", {})
            if params.get("offset") == 2:
                return {
                    "list": [
                        {
                            "id": "theme3",
                            "title": "Theme 3",
                            "createdAt": "2024-01-03T00:00:00.000Z",
                        }
                    ],
                    "total": 10,
                    "next": None,
                }
            else:
                return {
                    "list": [
                        {
                            "id": "theme1",
                            "title": "Theme 1",
                            "createdAt": "2024-01-01T00:00:00.000Z",
                        },
                        {
                            "id": "theme2",
                            "title": "Theme 2",
                            "createdAt": "2024-01-02T00:00:00.000Z",
                        },
                    ],
                    "total": 10,
                    "next": "/v3/themes?offset=2&limit=2",
                }

        mock_get.side_effect = mock_get_side_effect

        # Create client
        dw = Datawrapper()

        # Test first call (default parameters)
        one = dw.get_themes()
        assert len(one["list"]) > 0

        # Test second call (with offset and limit)
        two = dw.get_themes(offset=2, limit=1)
        assert one["list"][0] != two["list"][0]

        # Verify the mock was called twice
        assert mock_get.call_count == 2
