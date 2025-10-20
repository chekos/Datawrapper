"""Functional tests for BaseChart delete, duplicate, and fork methods with mocked API calls."""

from unittest.mock import MagicMock, patch

import pytest

from datawrapper import Datawrapper
from datawrapper.charts import ColumnChart


def test_base_chart_delete_success():
    """Test the delete method with mocked API."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "test123",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock delete_chart response
    mock_client.delete_chart.return_value = True

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart
        chart = ColumnChart(title="Test Chart")
        chart.create()

        # Verify chart_id is set
        assert chart.chart_id == "test123"

        # Delete the chart
        result = chart.delete()

        # Verify the delete was called
        mock_client.delete_chart.assert_called_once_with(chart_id="test123")

        # Verify the result
        assert result is True

        # Verify chart_id is cleared after deletion
        assert chart.chart_id is None


def test_base_chart_delete_no_chart_id():
    """Test the delete method raises error when no chart_id is set."""
    chart = ColumnChart(title="Test Chart")

    # Attempt to delete without chart_id should raise ValueError
    with pytest.raises(ValueError, match="No chart_id set"):
        chart.delete()


def test_base_chart_delete_with_access_token():
    """Test the delete method with explicit access token."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "test456",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock delete_chart response
    mock_client.delete_chart.return_value = True

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart
        chart = ColumnChart(title="Test Chart")
        chart.create(access_token="custom_token")

        # Delete with custom token
        result = chart.delete(access_token="custom_token")

        # Verify the result
        assert result is True
        assert chart.chart_id is None


def test_base_chart_duplicate_success():
    """Test the duplicate method with mocked API."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "original123",
        "title": "Original Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock copy_chart response
    mock_copy_info = {
        "id": "copy456",
        "title": "Original Chart (Duplicate)",
        "type": "d3-bars",
    }
    mock_client.copy_chart.return_value = mock_copy_info

    with (
        patch.object(ColumnChart, "_get_client", return_value=mock_client),
        patch.object(ColumnChart, "get") as mock_get,
    ):
        # Configure mock_get to return a new chart instance
        mock_duplicated_chart = ColumnChart(title="Original Chart (Duplicate)")
        mock_duplicated_chart.chart_id = "copy456"
        mock_get.return_value = mock_duplicated_chart

        # Create original chart
        original_chart = ColumnChart(title="Original Chart")
        original_chart.create()

        # Verify original chart_id
        assert original_chart.chart_id == "original123"

        # Duplicate the chart
        copied_chart = original_chart.duplicate()

        # Verify copy_chart was called
        mock_client.copy_chart.assert_called_once_with(chart_id="original123")

        # Verify get was called to fetch full chart data
        mock_get.assert_called_once_with(chart_id="copy456", access_token=None)

        # Verify the duplicated chart is a new instance
        assert isinstance(copied_chart, ColumnChart)
        assert copied_chart.chart_id == "copy456"
        assert copied_chart.chart_id != original_chart.chart_id

        # Verify original chart_id is unchanged
        assert original_chart.chart_id == "original123"


def test_base_chart_duplicate_no_chart_id():
    """Test the duplicate method raises error when no chart_id is set."""
    chart = ColumnChart(title="Test Chart")

    # Attempt to duplicate without chart_id should raise ValueError
    with pytest.raises(ValueError, match="No chart_id set"):
        chart.duplicate()


def test_base_chart_duplicate_invalid_response():
    """Test the duplicate method handles invalid API response."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "test789",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock invalid copy_chart response (not a dict)
    mock_client.copy_chart.return_value = "invalid_response"

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create chart
        chart = ColumnChart(title="Test Chart")
        chart.create()

        # Attempt to duplicate should raise ValueError
        with pytest.raises(ValueError, match="Unexpected response type from API"):
            chart.duplicate()


def test_base_chart_duplicate_missing_id():
    """Test the duplicate method handles response with missing ID."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "test999",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock copy_chart response without ID
    mock_copy_info = {
        "title": "Test Chart (Duplicate)",
        "type": "d3-bars",
    }
    mock_client.copy_chart.return_value = mock_copy_info

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create chart
        chart = ColumnChart(title="Test Chart")
        chart.create()

        # Attempt to duplicate should raise ValueError
        with pytest.raises(ValueError, match="Invalid chart ID received from API"):
            chart.duplicate()


def test_base_chart_fork_success():
    """Test the fork method with mocked API."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "original789",
        "title": "Original Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock fork_chart response
    mock_fork_info = {
        "id": "fork123",
        "title": "Original Chart (Fork)",
        "type": "d3-bars",
        "forkedFrom": "original789",
    }
    mock_client.fork_chart.return_value = mock_fork_info

    with (
        patch.object(ColumnChart, "_get_client", return_value=mock_client),
        patch.object(ColumnChart, "get") as mock_get,
    ):
        # Configure mock_get to return a new chart instance
        mock_forked_chart = ColumnChart(title="Original Chart (Fork)")
        mock_forked_chart.chart_id = "fork123"
        mock_get.return_value = mock_forked_chart

        # Create original chart
        original_chart = ColumnChart(title="Original Chart")
        original_chart.create()

        # Verify original chart_id
        assert original_chart.chart_id == "original789"

        # Fork the chart
        forked_chart = original_chart.fork()

        # Verify fork_chart was called
        mock_client.fork_chart.assert_called_once_with(chart_id="original789")

        # Verify get was called to fetch full chart data
        mock_get.assert_called_once_with(chart_id="fork123", access_token=None)

        # Verify the forked chart is a new instance
        assert isinstance(forked_chart, ColumnChart)
        assert forked_chart.chart_id == "fork123"
        assert forked_chart.chart_id != original_chart.chart_id

        # Verify original chart_id is unchanged
        assert original_chart.chart_id == "original789"


def test_base_chart_fork_no_chart_id():
    """Test the fork method raises error when no chart_id is set."""
    chart = ColumnChart(title="Test Chart")

    # Attempt to fork without chart_id should raise ValueError
    with pytest.raises(ValueError, match="No chart_id set"):
        chart.fork()


def test_base_chart_fork_invalid_response():
    """Test the fork method handles invalid API response."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "test111",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock invalid fork_chart response (not a dict)
    mock_client.fork_chart.return_value = ["invalid", "response"]

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create chart
        chart = ColumnChart(title="Test Chart")
        chart.create()

        # Attempt to fork should raise ValueError
        with pytest.raises(ValueError, match="Unexpected response type from API"):
            chart.fork()


def test_base_chart_fork_missing_id():
    """Test the fork method handles response with missing ID."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "test222",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock fork_chart response without ID
    mock_fork_info = {
        "title": "Test Chart (Fork)",
        "type": "d3-bars",
    }
    mock_client.fork_chart.return_value = mock_fork_info

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create chart
        chart = ColumnChart(title="Test Chart")
        chart.create()

        # Attempt to fork should raise ValueError
        with pytest.raises(ValueError, match="Invalid chart ID received from API"):
            chart.fork()


def test_base_chart_fork_with_access_token():
    """Test the fork method with explicit access token."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "original333",
        "title": "Original Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock fork_chart response
    mock_fork_info = {
        "id": "fork444",
        "title": "Original Chart (Fork)",
        "type": "d3-bars",
    }
    mock_client.fork_chart.return_value = mock_fork_info

    with (
        patch.object(ColumnChart, "_get_client", return_value=mock_client),
        patch.object(ColumnChart, "get") as mock_get,
    ):
        # Configure mock_get to return a new chart instance
        mock_forked_chart = ColumnChart(title="Original Chart (Fork)")
        mock_forked_chart.chart_id = "fork444"
        mock_get.return_value = mock_forked_chart

        # Create chart with custom token
        chart = ColumnChart(title="Original Chart")
        chart.create(access_token="custom_token")

        # Fork with custom token
        forked_chart = chart.fork(access_token="custom_token")

        # Verify get was called with custom token
        mock_get.assert_called_once_with(
            chart_id="fork444", access_token="custom_token"
        )

        # Verify the forked chart
        assert isinstance(forked_chart, ColumnChart)
        assert forked_chart.chart_id == "fork444"


def test_base_chart_duplicate_with_access_token():
    """Test the duplicate method with explicit access token."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "original555",
        "title": "Original Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock copy_chart response
    mock_copy_info = {
        "id": "copy666",
        "title": "Original Chart (Duplicate)",
        "type": "d3-bars",
    }
    mock_client.copy_chart.return_value = mock_copy_info

    with (
        patch.object(ColumnChart, "_get_client", return_value=mock_client),
        patch.object(ColumnChart, "get") as mock_get,
    ):
        # Configure mock_get to return a new chart instance
        mock_duplicated_chart = ColumnChart(title="Original Chart (Duplicate)")
        mock_duplicated_chart.chart_id = "copy666"
        mock_get.return_value = mock_duplicated_chart

        # Create chart with custom token
        chart = ColumnChart(title="Original Chart")
        chart.create(access_token="custom_token")

        # Duplicate with custom token
        copied_chart = chart.duplicate(access_token="custom_token")

        # Verify get was called with custom token
        mock_get.assert_called_once_with(
            chart_id="copy666", access_token="custom_token"
        )

        # Verify the duplicated chart
        assert isinstance(copied_chart, ColumnChart)
        assert copied_chart.chart_id == "copy666"


def test_base_chart_get_display_urls_success():
    """Test the get_display_urls method with mocked API."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "test123",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock get_chart_display_urls response
    mock_display_urls = [
        {"url": "https://datawrapper.dwcdn.net/test123/1/", "type": "default"},
        {"url": "https://datawrapper.dwcdn.net/test123/plain.html", "type": "plain"},
    ]
    mock_client.get_chart_display_urls.return_value = mock_display_urls

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart
        chart = ColumnChart(title="Test Chart")
        chart.create()

        # Get display URLs
        result = chart.get_display_urls()

        # Verify the method was called
        mock_client.get_chart_display_urls.assert_called_once_with(chart_id="test123")

        # Verify the result
        assert result == mock_display_urls
        assert len(result) == 2
        assert result[0]["url"] == "https://datawrapper.dwcdn.net/test123/1/"


def test_base_chart_get_display_urls_no_chart_id():
    """Test the get_display_urls method raises error when no chart_id is set."""
    chart = ColumnChart(title="Test Chart")

    # Attempt to get display URLs without chart_id should raise ValueError
    with pytest.raises(ValueError, match="No chart_id set"):
        chart.get_display_urls()


def test_base_chart_get_display_urls_with_access_token():
    """Test the get_display_urls method with explicit access token."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "test456",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock get_chart_display_urls response
    mock_display_urls = [
        {"url": "https://datawrapper.dwcdn.net/test456/1/", "type": "default"}
    ]
    mock_client.get_chart_display_urls.return_value = mock_display_urls

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart
        chart = ColumnChart(title="Test Chart")
        chart.create(access_token="custom_token")

        # Get display URLs with custom token
        result = chart.get_display_urls(access_token="custom_token")

        # Verify the result
        assert result == mock_display_urls


def test_base_chart_get_iframe_code_success():
    """Test the get_iframe_code method with mocked API."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "test789",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock get_iframe_code response
    mock_iframe_code = '<iframe src="https://datawrapper.dwcdn.net/test789/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="400"></iframe>'
    mock_client.get_iframe_code.return_value = mock_iframe_code

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart
        chart = ColumnChart(title="Test Chart")
        chart.create()

        # Get iframe code
        result = chart.get_iframe_code()

        # Verify the method was called
        mock_client.get_iframe_code.assert_called_once_with(
            chart_id="test789", responsive=False
        )

        # Verify the result
        assert result == mock_iframe_code
        assert "test789" in result
        assert "<iframe" in result


def test_base_chart_get_iframe_code_responsive():
    """Test the get_iframe_code method with responsive=True."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "test999",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock get_iframe_code response for responsive
    mock_iframe_code = '<iframe src="https://datawrapper.dwcdn.net/test999/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="400"></iframe><script type="text/javascript">!function(){"use strict";window.addEventListener("message",(function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r=0;r<e.length;r++)if(e[r].contentWindow===a.source){var i=a.data["datawrapper-height"][t]+"px";e[r].style.height=i}}}))}();</script>'
    mock_client.get_iframe_code.return_value = mock_iframe_code

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart
        chart = ColumnChart(title="Test Chart")
        chart.create()

        # Get responsive iframe code
        result = chart.get_iframe_code(responsive=True)

        # Verify the method was called with responsive=True
        mock_client.get_iframe_code.assert_called_once_with(
            chart_id="test999", responsive=True
        )

        # Verify the result
        assert result == mock_iframe_code
        assert "test999" in result
        assert "<script" in result


def test_base_chart_get_iframe_code_no_chart_id():
    """Test the get_iframe_code method raises error when no chart_id is set."""
    chart = ColumnChart(title="Test Chart")

    # Attempt to get iframe code without chart_id should raise ValueError
    with pytest.raises(ValueError, match="No chart_id set"):
        chart.get_iframe_code()


def test_base_chart_get_iframe_code_with_access_token():
    """Test the get_iframe_code method with explicit access token."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "test111",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock get_iframe_code response
    mock_iframe_code = '<iframe src="https://datawrapper.dwcdn.net/test111/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="400"></iframe>'
    mock_client.get_iframe_code.return_value = mock_iframe_code

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart
        chart = ColumnChart(title="Test Chart")
        chart.create(access_token="custom_token")

        # Get iframe code with custom token
        result = chart.get_iframe_code(access_token="custom_token")

        # Verify the result
        assert result == mock_iframe_code


def test_base_chart_get_editor_url_success():
    """Test the get_editor_url method."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "aBcDe",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart
        chart = ColumnChart(title="Test Chart")
        chart.create()

        # Get editor URL
        result = chart.get_editor_url()

        # Verify the result
        expected_url = "https://app.datawrapper.de/edit/aBcDe/visualize#refine"
        assert result == expected_url
        assert "aBcDe" in result
        assert "visualize#refine" in result


def test_base_chart_get_editor_url_no_chart_id():
    """Test the get_editor_url method raises error when no chart_id is set."""
    chart = ColumnChart(title="Test Chart")

    # Attempt to get editor URL without chart_id should raise ValueError
    with pytest.raises(ValueError, match="No chart_id set"):
        chart.get_editor_url()


def test_base_chart_get_png_url_success():
    """Test the get_png_url method."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "XyZ123",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart
        chart = ColumnChart(title="Test Chart")
        chart.create()

        # Get PNG URL
        result = chart.get_png_url()

        # Verify the result
        expected_url = "https://datawrapper.dwcdn.net/XyZ123/full.png"
        assert result == expected_url
        assert "XyZ123" in result
        assert "full.png" in result


def test_base_chart_get_png_url_no_chart_id():
    """Test the get_png_url method raises error when no chart_id is set."""
    chart = ColumnChart(title="Test Chart")

    # Attempt to get PNG URL without chart_id should raise ValueError
    with pytest.raises(ValueError, match="No chart_id set"):
        chart.get_png_url()


def test_base_chart_get_public_url_success():
    """Test the get_public_url method."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "aO8Gv",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart
        chart = ColumnChart(title="Test Chart")
        chart.create()

        # Get public URL
        result = chart.get_public_url()

        # Verify the result
        expected_url = "https://datawrapper.dwcdn.net/aO8Gv/"
        assert result == expected_url
        assert "aO8Gv" in result
        assert result.startswith("https://datawrapper.dwcdn.net/")
        assert result.endswith("/")


def test_base_chart_get_public_url_no_chart_id():
    """Test the get_public_url method raises error when no chart_id is set."""
    chart = ColumnChart(title="Test Chart")

    # Attempt to get public URL without chart_id should raise ValueError
    with pytest.raises(ValueError, match="No chart_id set"):
        chart.get_public_url()


def test_base_chart_get_public_url_different_chart_ids():
    """Test the get_public_url method with different chart IDs."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Test with various chart ID formats
        test_ids = ["abc123", "XyZ789", "test-id", "12345"]

        for chart_id in test_ids:
            chart = ColumnChart(title="Test Chart")
            chart.chart_id = chart_id

            result = chart.get_public_url()
            expected_url = f"https://datawrapper.dwcdn.net/{chart_id}/"

            assert result == expected_url
            assert chart_id in result


def test_base_chart_publish_success():
    """Test the publish method with method chaining."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "test123",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock publish_chart response (returns dict with publicUrl)
    mock_publish_response = {
        "id": "test123",
        "publicUrl": "https://datawrapper.dwcdn.net/test123/",
        "publicId": "test123",
    }
    mock_client.publish_chart.return_value = mock_publish_response

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart
        chart = ColumnChart(title="Test Chart")
        chart.create()

        # Verify chart_id is set
        assert chart.chart_id == "test123"

        # Publish the chart
        result = chart.publish()

        # Verify the publish was called
        mock_client.publish_chart.assert_called_once_with(chart_id="test123")

        # Verify the result is the chart instance (for method chaining)
        assert isinstance(result, ColumnChart)
        assert result is chart


def test_base_chart_publish_no_chart_id():
    """Test the publish method raises error when no chart_id is set."""
    chart = ColumnChart(title="Test Chart")

    # Attempt to publish without chart_id should raise ValueError
    with pytest.raises(ValueError, match="No chart_id set"):
        chart.publish()


def test_base_chart_publish_with_access_token():
    """Test the publish method with explicit access token."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "test456",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock publish_chart response
    mock_publish_response = {
        "id": "test456",
        "publicUrl": "https://datawrapper.dwcdn.net/test456/",
        "publicId": "test456",
    }
    mock_client.publish_chart.return_value = mock_publish_response

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart
        chart = ColumnChart(title="Test Chart")
        chart.create(access_token="custom_token")

        # Publish with custom token
        result = chart.publish(access_token="custom_token")

        # Verify the result is the chart instance (for method chaining)
        assert isinstance(result, ColumnChart)
        assert result is chart


def test_base_chart_publish_failure():
    """Test the publish method raises exception when API returns empty/falsy response."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "test789",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock publish_chart response with empty dict (failure case)
    mock_client.publish_chart.return_value = {}

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart
        chart = ColumnChart(title="Test Chart")
        chart.create()

        # Publish the chart should raise exception
        with pytest.raises(Exception, match="Failed to publish chart test789"):
            chart.publish()

        # Verify the publish was called
        mock_client.publish_chart.assert_called_once_with(chart_id="test789")


def test_base_chart_publish_none_response():
    """Test the publish method raises exception when API returns None."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "test999",
        "title": "Test Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock publish_chart response with None (failure case)
    mock_client.publish_chart.return_value = None

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart
        chart = ColumnChart(title="Test Chart")
        chart.create()

        # Publish the chart should raise exception
        with pytest.raises(Exception, match="Failed to publish chart test999"):
            chart.publish()

        # Verify the publish was called
        mock_client.publish_chart.assert_called_once_with(chart_id="test999")


def test_base_chart_create_method_chaining():
    """Test that create() returns the chart instance for method chaining."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "chain123",
        "title": "Chained Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart and verify it returns self
        chart = ColumnChart(title="Chained Chart")
        result = chart.create()

        # Verify the result is the chart instance (for method chaining)
        assert isinstance(result, ColumnChart)
        assert result is chart
        assert result.chart_id == "chain123"

        # Verify create_chart was called
        mock_client.create_chart.assert_called_once()


def test_base_chart_update_method_chaining():
    """Test that update() returns the chart instance for method chaining."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "update123",
        "title": "Original Title",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock update_chart response
    mock_update_response = {
        "id": "update123",
        "title": "Updated Title",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.update_chart.return_value = mock_update_response

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart
        chart = ColumnChart(title="Original Title")
        chart.create()

        # Update the chart and verify it returns self
        chart.title = "Updated Title"
        result = chart.update()

        # Verify the result is the chart instance (for method chaining)
        assert isinstance(result, ColumnChart)
        assert result is chart
        assert result.chart_id == "update123"

        # Verify update_chart was called
        mock_client.update_chart.assert_called_once()


def test_base_chart_full_method_chaining():
    """Test full method chaining workflow: create().update().publish()."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "fullchain123",
        "title": "Initial Title",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock update_chart response
    mock_update_response = {
        "id": "fullchain123",
        "title": "Updated Title",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.update_chart.return_value = mock_update_response

    # Mock publish_chart response
    mock_publish_response = {
        "id": "fullchain123",
        "publicUrl": "https://datawrapper.dwcdn.net/fullchain123/",
        "publicId": "fullchain123",
    }
    mock_client.publish_chart.return_value = mock_publish_response

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart and chain methods
        chart = ColumnChart(title="Initial Title")

        # Test full method chaining
        result = chart.create().update().publish()

        # Verify the result is the chart instance
        assert isinstance(result, ColumnChart)
        assert result is chart
        assert result.chart_id == "fullchain123"

        # Verify all methods were called
        mock_client.create_chart.assert_called_once()
        mock_client.update_chart.assert_called_once()
        mock_client.publish_chart.assert_called_once()


def test_base_chart_create_with_access_token_chaining():
    """Test create() method chaining with explicit access token."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "token123",
        "title": "Token Chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create a chart with custom token
        chart = ColumnChart(title="Token Chart")
        result = chart.create(access_token="custom_token")

        # Verify the result is the chart instance
        assert isinstance(result, ColumnChart)
        assert result is chart
        assert result.chart_id == "token123"


def test_base_chart_update_with_access_token_chaining():
    """Test update() method chaining with explicit access token."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock create_chart response
    mock_chart_info = {
        "id": "token456",
        "title": "Original",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.create_chart.return_value = mock_chart_info

    # Mock update_chart response
    mock_update_response = {
        "id": "token456",
        "title": "Updated",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.update_chart.return_value = mock_update_response

    with patch.object(ColumnChart, "_get_client", return_value=mock_client):
        # Create and update with custom token
        chart = ColumnChart(title="Original")
        chart.create(access_token="custom_token")

        chart.title = "Updated"
        result = chart.update(access_token="custom_token")

        # Verify the result is the chart instance
        assert isinstance(result, ColumnChart)
        assert result is chart


if __name__ == "__main__":
    # Run the tests directly
    test_base_chart_delete_success()
    print("✅ test_base_chart_delete_success passed")

    test_base_chart_delete_no_chart_id()
    print("✅ test_base_chart_delete_no_chart_id passed")

    test_base_chart_delete_with_access_token()
    print("✅ test_base_chart_delete_with_access_token passed")

    test_base_chart_duplicate_success()
    print("✅ test_base_chart_duplicate_success passed")

    test_base_chart_duplicate_no_chart_id()
    print("✅ test_base_chart_duplicate_no_chart_id passed")

    test_base_chart_duplicate_invalid_response()
    print("✅ test_base_chart_duplicate_invalid_response passed")

    test_base_chart_duplicate_missing_id()
    print("✅ test_base_chart_duplicate_missing_id passed")

    test_base_chart_fork_success()
    print("✅ test_base_chart_fork_success passed")

    test_base_chart_fork_no_chart_id()
    print("✅ test_base_chart_fork_no_chart_id passed")

    test_base_chart_fork_invalid_response()
    print("✅ test_base_chart_fork_invalid_response passed")

    test_base_chart_fork_missing_id()
    print("✅ test_base_chart_fork_missing_id passed")

    test_base_chart_duplicate_with_access_token()
    print("✅ test_base_chart_duplicate_with_access_token passed")

    test_base_chart_get_display_urls_success()
    print("✅ test_base_chart_get_display_urls_success passed")

    test_base_chart_get_display_urls_no_chart_id()
    print("✅ test_base_chart_get_display_urls_no_chart_id passed")

    test_base_chart_get_display_urls_with_access_token()
    print("✅ test_base_chart_get_display_urls_with_access_token passed")

    test_base_chart_get_iframe_code_success()
    print("✅ test_base_chart_get_iframe_code_success passed")

    test_base_chart_get_iframe_code_responsive()
    print("✅ test_base_chart_get_iframe_code_responsive passed")

    test_base_chart_get_iframe_code_no_chart_id()
    print("✅ test_base_chart_get_iframe_code_no_chart_id passed")

    test_base_chart_get_iframe_code_with_access_token()
    print("✅ test_base_chart_get_iframe_code_with_access_token passed")

    test_base_chart_get_editor_url_success()
    print("✅ test_base_chart_get_editor_url_success passed")

    test_base_chart_get_editor_url_no_chart_id()
    print("✅ test_base_chart_get_editor_url_no_chart_id passed")

    test_base_chart_get_png_url_success()
    print("✅ test_base_chart_get_png_url_success passed")

    test_base_chart_get_png_url_no_chart_id()
    print("✅ test_base_chart_get_png_url_no_chart_id passed")

    test_base_chart_publish_success()
    print("✅ test_base_chart_publish_success passed")

    test_base_chart_publish_no_chart_id()
    print("✅ test_base_chart_publish_no_chart_id passed")

    test_base_chart_publish_with_access_token()
    print("✅ test_base_chart_publish_with_access_token passed")

    test_base_chart_publish_failure()
    print("✅ test_base_chart_publish_failure passed")

    test_base_chart_publish_none_response()
    print("✅ test_base_chart_publish_none_response passed")
