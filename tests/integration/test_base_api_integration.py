"""Tests for BaseChart API integration functionality."""

import os
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from datawrapper import BaseChart


class TestBaseChartAPIIntegration:
    """Test the API integration methods in BaseChart."""

    def test_get_client_with_token_parameter(self):
        """Test _get_client with access_token parameter."""
        chart = BaseChart(**{"chart-type": "d3-bars", "title": "Test Chart"})

        with patch("datawrapper.charts.base.Datawrapper") as mock_dw:
            mock_instance = Mock()
            mock_dw.return_value = mock_instance

            client = chart._get_client(access_token="test-token")

            mock_dw.assert_called_once_with(access_token="test-token")
            assert client == mock_instance
            assert chart._client == mock_instance

    def test_get_client_with_environment_variable(self):
        """Test _get_client with DATAWRAPPER_ACCESS_TOKEN environment variable."""
        chart = BaseChart(**{"chart-type": "d3-bars", "title": "Test Chart"})

        with patch.dict(os.environ, {"DATAWRAPPER_ACCESS_TOKEN": "env-token"}):
            with patch("datawrapper.charts.base.Datawrapper") as mock_dw:
                mock_instance = Mock()
                mock_dw.return_value = mock_instance

                client = chart._get_client()

                mock_dw.assert_called_once_with(access_token="env-token")
                assert client == mock_instance

    def test_get_client_no_token_raises_error(self):
        """Test _get_client raises ValueError when no token is available."""
        chart = BaseChart(**{"chart-type": "d3-bars", "title": "Test Chart"})

        # Ensure no environment variable is set
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(
                ValueError, match="No Datawrapper access token provided"
            ):
                chart._get_client()

    def test_get_client_reuses_existing_client(self):
        """Test _get_client reuses existing client instance."""
        chart = BaseChart(**{"chart-type": "d3-bars", "title": "Test Chart"})
        mock_client = Mock()
        chart._client = mock_client

        client = chart._get_client(access_token="test-token")

        assert client == mock_client

    def test_create_chart_success(self):
        """Test successful chart creation."""
        chart = BaseChart(
            **{
                "chart-type": "d3-bars",
                "title": "Test Chart",
                "data": pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]}),
            }
        )

        mock_client = Mock()
        mock_client.create_chart.return_value = {"id": "test-chart-id"}
        mock_client.update_chart.return_value = {"id": "test-chart-id"}
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        with patch.object(chart, "_get_client", return_value=mock_client):
            chart = chart.create(access_token="test-token")

            assert chart.chart_id == "test-chart-id"

            # Verify create_chart was called with correct parameters
            mock_client.create_chart.assert_called_once()
            call_args = mock_client.create_chart.call_args
            assert call_args[1]["title"] == "Test Chart"
            assert call_args[1]["chart_type"] == "d3-bars"
            assert call_args[1]["data"] is not None
            assert call_args[1]["metadata"] is not None

    def test_create_chart_invalid_response(self):
        """Test chart creation with invalid API response."""
        chart = BaseChart(**{"chart-type": "d3-bars", "title": "Test Chart"})

        mock_client = Mock()
        mock_client.create_chart.return_value = {"id": None}  # Invalid ID

        with patch.object(chart, "_get_client", return_value=mock_client):
            with pytest.raises(ValueError, match="Invalid chart ID received from API"):
                chart.create(access_token="test-token")

    def test_create_chart_missing_id(self):
        """Test chart creation with missing ID in response."""
        chart = BaseChart(**{"chart-type": "d3-bars", "title": "Test Chart"})

        mock_client = Mock()
        mock_client.create_chart.return_value = {}  # No ID field

        with patch.object(chart, "_get_client", return_value=mock_client):
            with pytest.raises(ValueError, match="Invalid chart ID received from API"):
                chart.create(access_token="test-token")

    def test_update_chart_success(self):
        """Test successful chart update."""
        chart = BaseChart(
            **{
                "chart-type": "d3-bars",
                "title": "Updated Chart",
                "data": pd.DataFrame({"x": [1, 2, 3], "y": [7, 8, 9]}),
            }
        )
        chart.chart_id = "existing-chart-id"

        mock_client = Mock()
        mock_client.update_chart.return_value = {"id": "existing-chart-id"}
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        with patch.object(chart, "_get_client", return_value=mock_client):
            chart = chart.update(access_token="test-token")

            assert chart.chart_id == "existing-chart-id"

            # Verify update_chart was called with correct parameters
            mock_client.update_chart.assert_called_once()
            call_args = mock_client.update_chart.call_args
            assert call_args[1]["chart_id"] == "existing-chart-id"
            assert call_args[1]["title"] == "Updated Chart"
            assert call_args[1]["chart_type"] == "d3-bars"
            assert call_args[1]["data"] is not None
            assert call_args[1]["metadata"] is not None

    def test_update_chart_no_chart_id(self):
        """Test update raises error when no chart_id is set."""
        chart = BaseChart(**{"chart-type": "d3-bars", "title": "Test Chart"})

        with pytest.raises(ValueError, match="No chart_id set"):
            chart.update(access_token="test-token")

    def test_update_chart_empty_data(self):
        """Test update with empty data passes None for data parameter."""
        chart = BaseChart(**{"chart-type": "d3-bars", "title": "Test Chart"})
        chart.chart_id = "existing-chart-id"
        # Leave data empty (default)

        mock_client = Mock()
        mock_client.update_chart.return_value = {"id": "existing-chart-id"}

        with patch.object(chart, "_get_client", return_value=mock_client):
            chart.update(access_token="test-token")

            # Verify update_chart was called
            mock_client.update_chart.assert_called_once()
            call_args = mock_client.update_chart.call_args

            # Verify data parameter is None for empty data
            assert call_args[1]["data"] is None

    def test_create_with_list_data(self):
        """Test chart creation with list data instead of DataFrame."""
        chart = BaseChart(
            **{
                "chart-type": "d3-bars",
                "title": "Test Chart",
                "data": [{"x": 1, "y": 4}, {"x": 2, "y": 5}, {"x": 3, "y": 6}],
            }
        )

        mock_client = Mock()
        mock_client.create_chart.return_value = {"id": "test-chart-id"}
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        with patch.object(chart, "_get_client", return_value=mock_client):
            chart = chart.create(access_token="test-token")

            assert chart.chart_id == "test-chart-id"

            # Verify create_chart was called for chart creation
            mock_client.create_chart.assert_called_once()

    def test_api_integration_excludes_private_fields(self):
        """Test that chart_id and _client are excluded from serialization."""
        chart = BaseChart(**{"chart-type": "d3-bars", "title": "Test Chart"})
        chart.chart_id = "test-id"
        chart._client = Mock()

        serialized = chart.model_dump()

        assert "chart_id" not in serialized
        assert "_client" not in serialized

    def test_full_workflow_create_then_update(self):
        """Test full workflow: create chart then update it."""
        chart = BaseChart(
            **{
                "chart-type": "d3-bars",
                "title": "Initial Title",
                "data": pd.DataFrame({"x": [1, 2], "y": [3, 4]}),
            }
        )

        mock_client = Mock()
        mock_client.create_chart.return_value = {"id": "workflow-chart-id"}
        mock_client.update_chart.return_value = {"id": "workflow-chart-id"}
        mock_client.patch.return_value = None
        mock_client.put.return_value = None
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        with patch.object(chart, "_get_client", return_value=mock_client):
            # Create the chart
            chart = chart.create(access_token="test-token")
            assert chart.chart_id == "workflow-chart-id"

            # Update the chart
            chart.title = "Updated Title"
            chart.data = pd.DataFrame({"x": [5, 6], "y": [7, 8]})

            updated = chart.update(access_token="test-token")
            assert updated.chart_id == "workflow-chart-id"

            # Verify both create and update were called
            assert mock_client.create_chart.call_count == 1  # Chart creation
            assert mock_client.update_chart.call_count == 1  # Chart update via update()
            assert mock_client.patch.call_count == 0  # No longer used
            assert mock_client.put.call_count == 0  # No longer used
