"""Mock-based API tests that verify the chart creation workflow without hitting real API."""

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd

from datawrapper import BarChart


def test_create_sample_bar_chart_mock():
    """Test that creates the European turnout sample chart using mocked API calls.

    This test verifies the complete workflow without requiring real API access:
    1. Loads the European turnout sample configuration
    2. Creates sample data matching the chart structure
    3. Creates a BarChart instance with the sample configuration
    4. Mocks the Datawrapper API calls
    5. Verifies the chart creation and data upload workflow
    """
    # Load the European turnout sample JSON
    sample_path = (
        Path(__file__).parent.parent / "samples" / "bar" / "european-turnout.json"
    )
    with open(sample_path) as f:
        sample_data = json.load(f)

    # Extract chart configuration from sample
    chart_config = sample_data["chart"]["crdt"]["data"]

    # Create sample data that matches the chart structure
    sample_countries_data = pd.DataFrame(
        {
            "Country": [
                "Romania (2020)",
                "Bulgaria (2024)",
                "Albania (2021)",
                "United Kingdom (2024)",
                "Germany (2021)",
                "Sweden (2022)",
                "Spain (2023)",
                "France (2024)",
                "Luxembourg (2018)",
                "Belgium (2024)",
                "Turkey (2023)",
                "Malta (2022)",
            ],
            "Turnout": [
                33.2,
                33.4,
                46.3,
                60.0,
                76.4,
                83.8,
                66.0,
                66.7,
                91.0,
                88.5,
                87.0,
                85.6,
            ],
        }
    )

    print(
        f"\n📊 Creating European Turnout Chart with {len(sample_countries_data)} countries..."
    )

    # Create BarChart instance with configuration from sample
    chart = BarChart(
        title=chart_config["title"],
        data=sample_countries_data,
    )

    print("✅ BarChart instance created successfully")

    # Mock the Datawrapper client and API responses
    with patch("datawrapper.charts.base.Datawrapper") as mock_datawrapper_class:
        # Create mock client instance
        mock_client = Mock()
        mock_datawrapper_class.return_value = mock_client

        # Mock the create_chart response for chart creation
        mock_create_response = {"id": "test-chart-123", "title": chart.title}
        mock_client.create_chart.return_value = mock_create_response

        # Mock the _CHARTS_URL attribute
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        print("🚀 Creating chart via mocked Datawrapper API...")

        # Create the chart (this should use our mocked client)
        chart.create(access_token="test-token")
        chart_id = chart.chart_id

        print(f"✅ Chart created successfully with ID: {chart_id}")

        # Verify the chart creation API call
        mock_client.create_chart.assert_called_once()
        create_call_args = mock_client.create_chart.call_args

        # Check the call arguments
        call_kwargs = create_call_args[1]
        assert call_kwargs["title"] == chart.title
        assert call_kwargs["chart_type"] == chart.chart_type
        assert "metadata" in call_kwargs

        # Check that CSV data was provided
        csv_data = call_kwargs["data"]
        assert csv_data is not None
        assert "Country,Turnout" in csv_data  # CSV header
        assert "Romania (2020),33.2" in csv_data  # Sample data row

        # Verify chart_id was set correctly
        assert chart.chart_id == chart_id
        assert chart_id == "test-chart-123"

        print("✅ All API calls verified successfully!")
        print("📋 Chart metadata structure validated")
        print("📊 Data upload (CSV format) validated")
        print("🎯 Chart ID assignment validated")


def test_create_simple_bar_chart_mock():
    """Test creating a simple bar chart with mocked API calls."""
    # Create simple test data
    test_data = pd.DataFrame(
        {"Category": ["A", "B", "C", "D", "E"], "Value": [23, 45, 56, 78, 32]}
    )

    print("\n📊 Creating simple test chart...")

    # Create a simple BarChart
    chart = BarChart(
        title="API Test Chart - Simple Bar Chart",
        data=test_data,
    )

    print("✅ Simple BarChart instance created")

    # Mock the Datawrapper client and API responses
    with patch("datawrapper.charts.base.Datawrapper") as mock_datawrapper_class:
        # Create mock client instance
        mock_client = Mock()
        mock_datawrapper_class.return_value = mock_client

        # Mock the create_chart response for chart creation
        mock_create_response = {"id": "simple-chart-456", "title": chart.title}
        mock_client.create_chart.return_value = mock_create_response

        # Mock the _CHARTS_URL attribute
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        print("🚀 Creating chart via mocked API...")

        # Create via API
        chart.create(access_token="test-token")
        chart_id = chart.chart_id

        print(f"✅ Chart created with ID: {chart_id}")

        # Verify the API calls were made correctly
        assert mock_client.create_chart.called

        # Verify chart_id was set
        assert chart.chart_id == "simple-chart-456"
        assert chart_id == "simple-chart-456"

        # Verify the serialized data structure
        serialized = chart.serialize_model()
        assert serialized["type"] == "d3-bars"
        assert serialized["title"] == "API Test Chart - Simple Bar Chart"
        assert "metadata" in serialized
        assert "data" in serialized["metadata"]
        assert "describe" in serialized["metadata"]
        assert "visualize" in serialized["metadata"]
        assert "publish" in serialized["metadata"]
        assert "annotate" in serialized["metadata"]

        print("🎉 Simple mock test completed successfully!")


def test_update_chart_mock():
    """Test updating an existing chart with mocked API calls."""
    # Create test data
    test_data = pd.DataFrame({"Month": ["Jan", "Feb", "Mar"], "Sales": [100, 150, 200]})

    # Create chart
    chart = BarChart(
        title="Sales Chart - Update Test",
        data=test_data,
    )

    # Set a chart_id as if it was already created
    chart.chart_id = "existing-chart-789"

    print("\n📊 Testing chart update functionality...")

    # Mock the Datawrapper client and API responses
    with patch("datawrapper.charts.base.Datawrapper") as mock_datawrapper_class:
        # Create mock client instance
        mock_client = Mock()
        mock_datawrapper_class.return_value = mock_client

        # Mock the update_chart response for chart update (returns None)
        mock_client.update_chart.return_value = None

        # Mock the _CHARTS_URL attribute
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        print("🔄 Updating chart via mocked API...")

        # Update the chart
        chart.update(access_token="test-token")
        updated_chart_id = chart.chart_id

        print(f"✅ Chart updated successfully with ID: {updated_chart_id}")

        # Verify the update API call
        mock_client.update_chart.assert_called_once()
        update_call_args = mock_client.update_chart.call_args

        # Check the call arguments
        call_kwargs = update_call_args[1]
        assert call_kwargs["chart_id"] == "existing-chart-789"
        assert call_kwargs["title"] == chart.title
        assert call_kwargs["chart_type"] == chart.chart_type
        assert "metadata" in call_kwargs

        # Verify the returned chart_id matches
        assert updated_chart_id == "existing-chart-789"
        assert chart.chart_id == "existing-chart-789"

        print("✅ Chart update workflow verified successfully!")


if __name__ == "__main__":
    # Run the tests directly
    test_create_sample_bar_chart_mock()
    test_create_simple_bar_chart_mock()
    test_update_chart_mock()
    print("\n🎉 All mock-based API tests completed successfully!")
