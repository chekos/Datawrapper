"""Test River functions with mocked API calls."""

from unittest.mock import patch

from datawrapper import Datawrapper


def test_get_river():
    """Test the get_river function with mocked API."""
    with patch.object(Datawrapper, "get") as mock_get:
        # Mock the get_river response
        mock_river_response = {
            "list": [
                {
                    "id": "river1",
                    "title": "Test River Chart 1",
                    "type": "d3-bars",
                    "description": "Test description",
                    "byline": "Test byline",
                },
                {
                    "id": "river2",
                    "title": "Test River Chart 2",
                    "type": "d3-lines",
                    "description": "Another test",
                    "byline": "Another byline",
                },
            ]
        }

        # Mock get_river_chart response
        mock_river_chart = {
            "id": "river1",
            "title": "Test River Chart 1",
            "type": "d3-bars",
            "description": "Test description",
            "byline": "Test byline",
        }

        # Set up side_effect to return different values for each call
        mock_get.side_effect = [mock_river_response, mock_river_chart]

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

        # Test the get_river_chart function too
        chart = dw.get_river_chart(river[0]["id"])
        assert isinstance(chart, dict)
        assert "id" in chart

        # Verify the calls were made
        assert mock_get.call_count == 2


def test_get_river_with_parameters():
    """Test get_river with different parameters."""
    with patch.object(Datawrapper, "get") as mock_get:
        # Mock responses for different parameter combinations
        mock_river_response = {
            "list": [
                {
                    "id": "river1",
                    "title": "Approved Chart",
                    "type": "d3-bars",
                }
            ]
        }

        # Set up side_effect to return the same response for all calls
        mock_get.side_effect = [
            mock_river_response,
            mock_river_response,
        ]

        dw = Datawrapper()

        # Test some different parameters
        dw.get_river(approved=True)
        dw.get_river(approved=True, search="test")

        # Verify the calls were made
        assert mock_get.call_count == 2


def test_update_river_chart():
    """Test updating a river chart."""
    with (
        patch.object(Datawrapper, "get") as mock_get,
        patch.object(Datawrapper, "put") as mock_put,
    ):
        # Mock get_charts response
        mock_charts_response = {
            "list": [
                {
                    "id": "chart123",
                    "title": "My Chart",
                    "type": "d3-bars",
                }
            ]
        }

        # Mock update_river_chart response (returns True)
        mock_put.return_value = True

        # Mock get_river_chart response after update
        mock_updated_chart = {
            "id": "chart123",
            "title": "My Chart",
            "type": "d3-bars",
            "description": "Test description",
            "byline": "Test byline",
            "tags": ["test"],
            "forkable": True,
        }

        # Set up side_effect for get calls
        mock_get.side_effect = [mock_charts_response, mock_updated_chart]

        dw = Datawrapper()

        # Get a chart we own
        chart = dw.get_charts()["list"][0]

        # Update a river chart
        chart_id = chart["id"]
        update = dw.update_river_chart(
            chart_id,
            description="Test description",
            byline="Test byline",
            tags=["test"],
            forkable=True,
        )
        assert update is True

        # Verify that the river chart was updated
        chart = dw.get_river_chart(chart_id)
        assert chart["description"] == "Test description"

        # Verify the calls were made
        assert mock_get.call_count == 2
        assert mock_put.call_count == 1


if __name__ == "__main__":
    # Run the tests directly
    test_get_river()
    print("✅ test_get_river passed")

    test_get_river_with_parameters()
    print("✅ test_get_river_with_parameters passed")

    test_update_river_chart()
    print("✅ test_update_river_chart passed")

    print("\n🎉 All mocked River tests completed successfully!")
