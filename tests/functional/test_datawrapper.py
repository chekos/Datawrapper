"""Unit test package for datawrapper with mocked API calls."""

from unittest.mock import patch

import pandas as pd

from datawrapper import Datawrapper


def test_get_charts():
    """Test the get_charts method with mocked API."""
    # Mock the get method that get_charts calls internally
    with patch.object(Datawrapper, "get") as mock_get:
        # Mock the get_charts response
        mock_charts = [
            {"id": "chart1", "title": "Test Chart 1", "type": "d3-bars"},
            {"id": "chart2", "title": "Test Chart 2", "type": "d3-lines"},
        ]
        mock_get.return_value = mock_charts

        # Create client and call method
        dw = Datawrapper()
        result = dw.get_charts()

        # Verify the call was made
        mock_get.assert_called_once()

        # Verify the result
        assert result == mock_charts
        assert len(result) == 2


def test_get_folders():
    """Test the get_folders method with mocked API."""
    # Mock the get method that get_folders calls internally
    with patch.object(Datawrapper, "get") as mock_get:
        # Mock the get_folders response
        mock_folders = [
            {"id": "folder1", "name": "Test Folder 1"},
            {"id": "folder2", "name": "Test Folder 2"},
        ]
        mock_get.return_value = mock_folders

        # Create client and call method
        dw = Datawrapper()
        result = dw.get_folders()

        # Verify the call was made
        mock_get.assert_called_once()

        # Verify the result
        assert result == mock_folders
        assert len(result) == 2


def test_fork():
    """Test the fork_chart method with mocked API."""
    # Mock the post method that fork_chart calls internally
    with patch.object(Datawrapper, "post") as mock_post:
        # Source chart ID
        source_id = "dZntB"

        # Mock the fork_chart response - returns a new chart with different ID
        mock_fork_info = {
            "id": "forked123",
            "title": "Forked Chart",
            "type": "d3-bars",
            "forkable": True,
            "forkedFrom": source_id,
        }
        mock_post.return_value = mock_fork_info

        # Create client and call method
        dw = Datawrapper()
        fork_info = dw.fork_chart(source_id)

        # Verify the call was made
        mock_post.assert_called_once()

        # Verify the result
        assert isinstance(fork_info, dict)
        assert source_id != fork_info["id"]
        assert fork_info["id"] == "forked123"


def test_copy():
    """Test the copy_chart method with mocked API."""
    # Mock the post method that both create_chart and copy_chart call internally
    with patch.object(Datawrapper, "post") as mock_post:
        # Mock the create_chart response first, then copy_chart response
        mock_chart_info = {
            "id": "original123",
            "title": "Test copy_chart",
            "type": "d3-bars-stacked",
        }
        mock_copy_info = {
            "id": "copy456",
            "title": "Test copy_chart (Copy)",
            "type": "d3-bars-stacked",
        }
        # Set up side_effect to return different values for each call
        mock_post.side_effect = [mock_chart_info, mock_copy_info]

        # Create client and call methods
        dw = Datawrapper()
        chart_info = dw.create_chart(
            title="Test copy_chart",
            chart_type="d3-bars-stacked",
        )
        copy_info = dw.copy_chart(chart_info["id"])

        # Verify the calls were made
        assert mock_post.call_count == 2

        # Verify the results
        assert isinstance(copy_info, dict)
        assert chart_info["title"] in copy_info["title"]
        assert copy_info["id"] != chart_info["id"]


def test_usage():
    """Test creating and updating charts with mocked API calls."""
    # Mock pandas read_csv to avoid actual HTTP request
    mock_df = pd.DataFrame(
        {
            "Country": ["USA", "Canada", "Mexico"],
            "in rural areas": [20, 25, 30],
            "in other urban areas": [30, 35, 40],
            "Share of population that lives in the capital": [50, 40, 30],
        }
    )

    with (
        patch("pandas.read_csv") as mock_read_csv,
        patch.object(Datawrapper, "get") as mock_get,
        patch.object(Datawrapper, "post") as mock_post,
        patch.object(Datawrapper, "patch") as mock_patch,
        patch.object(Datawrapper, "put") as mock_put,
        patch.object(Datawrapper, "delete") as mock_delete,
        patch("pathlib.Path.open", create=True),
    ):
        # Setup pandas mock
        mock_read_csv.return_value = mock_df

        # Mock get_my_account
        mock_get.return_value = {
            "id": "user123",
            "email": "test@example.com",
            "name": "Test User",
            "metadata": {
                "publish": {
                    "embed-codes": {
                        "embed-method-iframe": '<iframe src="https://datawrapper.dwcdn.net/abc123/" width="600" height="400"></iframe>'
                    }
                }
            },
        }

        # Mock create_chart and publish_chart
        mock_chart_info = {
            "id": "test-chart-789",
            "title": "Where do people live?",
            "type": "d3-bars-stacked",
            "metadata": {
                "visualize": {"thick": True},
                "publish": {
                    "embed-width": 600,
                    "embed-height": 400,
                    "embed-codes": {
                        "embed-method-iframe": '<iframe src="https://datawrapper.dwcdn.net/abc123/" width="600" height="400"></iframe>'
                    },
                },
            },
            "publicUrl": "https://datawrapper.dwcdn.net/abc123/",
        }
        mock_publish_result = {
            "id": "test-chart-789",
            "publicId": "abc123",
            "publicUrl": "https://datawrapper.dwcdn.net/abc123/",
            "data": mock_chart_info,
        }
        mock_post.side_effect = [mock_chart_info, mock_publish_result]

        # Mock update_chart (patch returns dict)
        mock_patch.return_value = mock_chart_info

        # Mock add_data (put returns bool)
        mock_put.return_value = True

        # Mock delete_chart
        mock_delete.return_value = True

        # Now run the actual test workflow
        dw = Datawrapper()

        # Get account info
        account = dw.get_my_account()
        assert account["id"] == "user123"

        # Pull data
        df = pd.read_csv(
            "https://raw.githubusercontent.com/chekos/datasets/master/data/datawrapper_example.csv",
            sep=";",
        )
        assert len(df) == 3

        # Create a chart
        chart_info = dw.create_chart(
            title="Where do people live?", chart_type="d3-bars-stacked", data=df
        )
        assert chart_info["id"] == "test-chart-789"

        # Add a description
        dw.update_description(
            chart_info["id"],
            source_name="UN Population Division",
            source_url="https://population.un.org/wup/",
            byline="datawrapper at pypi",
        )

        # Pub it
        publish_result = dw.publish_chart(chart_id=chart_info["id"], display=False)
        assert "publicUrl" in publish_result

        # Change it
        properties = {
            "visualize": {
                "thick": True,
                "custom-colors": {
                    "in rural areas": "#dadada",
                    "in other urban areas": "#1d81a2",
                    "Share of population that lives in the capital": "#15607a",
                },
            }
        }
        dw.update_chart(chart_info["id"], metadata=properties)

        # Export it (mock get for export)
        mock_get.return_value = b"fake image data"
        dw.export_chart(
            chart_info["id"], output="png", filepath="chart.png", display=False
        )

        # Get iframe code
        mock_get.return_value = mock_chart_info
        iframe_code = dw.get_iframe_code(chart_info["id"])
        assert "iframe" in iframe_code

        # Pull metadata
        props = dw.get_chart(chart_info["id"])
        assert props["id"] == "test-chart-789"

        # Get data
        mock_get.return_value = mock_df.to_csv(index=False)
        data = dw.get_data(chart_info["id"])
        assert "Country" in data

        # Nuke it
        dw.delete_chart(chart_info["id"])

        # Verify key API calls were made
        assert mock_get.call_count >= 1
        assert mock_post.call_count == 2
        assert mock_patch.call_count >= 1
        assert mock_put.call_count >= 1
        assert mock_delete.call_count == 1


if __name__ == "__main__":
    # Run the tests directly
    test_get_charts()
    print("✅ test_get_charts passed")

    test_get_folders()
    print("✅ test_get_folders passed")

    test_fork()
    print("✅ test_fork passed")

    test_copy()
    print("✅ test_copy passed")

    test_usage()
    print("✅ test_usage passed")

    print("\n🎉 All mocked Datawrapper tests completed successfully!")
