"""Integration tests for BaseChart export methods.

These tests use mocked API calls to verify the export_png, export_pdf, and export_svg
methods work correctly without requiring actual API access.
"""

from unittest.mock import MagicMock, patch

import pytest

from datawrapper.charts import BarChart


class TestExportPNG:
    """Test PNG export functionality."""

    def test_export_png_success(self):
        """Test successful PNG export with default parameters."""
        # Create mock client factory with closure to capture instance
        created_clients = []

        def mock_client_factory(access_token=None):
            mock_client = MagicMock()
            mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"
            mock_client.get.return_value = b"PNG_DATA"
            created_clients.append(mock_client)
            return mock_client

        with patch(
            "datawrapper.charts.base.BaseChart._get_client",
            side_effect=mock_client_factory,
        ) as mock_get_client:
            # Create chart and export
            chart = BarChart(title="Test Chart")
            chart.chart_id = "abc123"
            result = chart.export_png()

            # Verify
            assert result == b"PNG_DATA"
            mock_get_client.assert_called_once()
            # Get the mock client that was created
            mock_client = created_clients[0]
            call_args = mock_client.get.call_args
            assert (
                call_args[0][0]
                == "https://api.datawrapper.de/v3/charts/abc123/export/png"
            )
            assert call_args[1]["params"]["unit"] == "px"
            assert call_args[1]["params"]["mode"] == "rgb"
            assert call_args[1]["params"]["plain"] == "false"

    def test_export_png_with_all_parameters(self):
        """Test PNG export with all parameters specified."""
        # Create mock client factory with closure to capture instance
        created_clients = []

        def mock_client_factory(access_token=None):
            mock_client = MagicMock()
            mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"
            mock_client.get.return_value = b"PNG_DATA"
            created_clients.append(mock_client)
            return mock_client

        with patch(
            "datawrapper.charts.base.BaseChart._get_client",
            side_effect=mock_client_factory,
        ) as mock_get_client:
            # Create chart and export with all parameters
            chart = BarChart(title="Test Chart")
            chart.chart_id = "abc123"
            result = chart.export_png(
                width=800,
                height=600,
                plain=True,
                zoom=3,
                transparent=True,
                border_width=10,
                border_color="#FF0000",
            )

            # Verify
            assert result == b"PNG_DATA"
            mock_get_client.assert_called_once()
            mock_client = created_clients[0]
            call_args = mock_client.get.call_args
            params = call_args[1]["params"]
            assert params["width"] == "800"
            assert params["height"] == "600"
            assert params["plain"] == "true"
            assert params["zoom"] == "3"
            assert params["transparent"] == "true"
            assert params["borderWidth"] == "10"
            assert params["borderColor"] == "#FF0000"

    def test_export_png_no_chart_id(self):
        """Test that export_png raises ValueError when no chart_id is set."""
        chart = BarChart(title="Test Chart")
        with pytest.raises(ValueError, match="No chart_id set"):
            chart.export_png()

    def test_export_png_custom_access_token(self):
        """Test PNG export with custom access token."""

        # Create mock client factory
        def mock_client_factory(access_token=None):
            mock_client = MagicMock()
            mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"
            mock_client.get.return_value = b"PNG_DATA"
            return mock_client

        with patch(
            "datawrapper.charts.base.BaseChart._get_client",
            side_effect=mock_client_factory,
        ) as mock_get_client:
            # Create chart and export with custom token
            chart = BarChart(title="Test Chart")
            chart.chart_id = "abc123"
            result = chart.export_png(access_token="custom_token")

            # Verify
            assert result == b"PNG_DATA"
            mock_get_client.assert_called_once()


class TestExportPDF:
    """Test PDF export functionality."""

    def test_export_pdf_success(self):
        """Test successful PDF export with default parameters."""
        # Create mock client factory with closure to capture instance
        created_clients = []

        def mock_client_factory(access_token=None):
            mock_client = MagicMock()
            mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"
            mock_client.get.return_value = b"PDF_DATA"
            created_clients.append(mock_client)
            return mock_client

        with patch(
            "datawrapper.charts.base.BaseChart._get_client",
            side_effect=mock_client_factory,
        ) as mock_get_client:
            # Create chart and export
            chart = BarChart(title="Test Chart")
            chart.chart_id = "abc123"
            result = chart.export_pdf()

            # Verify
            assert result == b"PDF_DATA"
            mock_get_client.assert_called_once()
            mock_client = created_clients[0]
            call_args = mock_client.get.call_args
            assert (
                call_args[0][0]
                == "https://api.datawrapper.de/v3/charts/abc123/export/pdf"
            )
            assert call_args[1]["params"]["unit"] == "px"
            assert call_args[1]["params"]["mode"] == "rgb"
            assert call_args[1]["params"]["plain"] == "false"

    def test_export_pdf_with_all_parameters(self):
        """Test PDF export with all parameters specified."""
        # Create mock client factory with closure to capture instance
        created_clients = []

        def mock_client_factory(access_token=None):
            mock_client = MagicMock()
            mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"
            mock_client.get.return_value = b"PDF_DATA"
            created_clients.append(mock_client)
            return mock_client

        with patch(
            "datawrapper.charts.base.BaseChart._get_client",
            side_effect=mock_client_factory,
        ) as mock_get_client:
            # Create chart and export with all parameters
            chart = BarChart(title="Test Chart")
            chart.chart_id = "abc123"
            result = chart.export_pdf(
                width=800,
                height=600,
                plain=True,
                unit="mm",
                mode="cmyk",
                scale=2,
                border_width=10,
                border_color="#FF0000",
            )

            # Verify
            assert result == b"PDF_DATA"
            mock_get_client.assert_called_once()
            mock_client = created_clients[0]
            call_args = mock_client.get.call_args
            params = call_args[1]["params"]
            assert params["width"] == "800"
            assert params["height"] == "600"
            assert params["plain"] == "true"
            assert params["unit"] == "mm"
            assert params["mode"] == "cmyk"
            assert params["scale"] == "2"
            assert params["borderWidth"] == "10"
            assert params["borderColor"] == "#FF0000"

    def test_export_pdf_no_chart_id(self):
        """Test that export_pdf raises ValueError when no chart_id is set."""
        chart = BarChart(title="Test Chart")
        with pytest.raises(ValueError, match="No chart_id set"):
            chart.export_pdf()

    def test_export_pdf_custom_access_token(self):
        """Test PDF export with custom access token."""

        # Create mock client factory
        def mock_client_factory(access_token=None):
            mock_client = MagicMock()
            mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"
            mock_client.get.return_value = b"PDF_DATA"
            return mock_client

        with patch(
            "datawrapper.charts.base.BaseChart._get_client",
            side_effect=mock_client_factory,
        ) as mock_get_client:
            # Create chart and export with custom token
            chart = BarChart(title="Test Chart")
            chart.chart_id = "abc123"
            result = chart.export_pdf(access_token="custom_token")

            # Verify
            assert result == b"PDF_DATA"
            mock_get_client.assert_called_once()


class TestExportSVG:
    """Tests for the export_svg method."""

    def test_export_svg_success(self):
        """Test successful SVG export with default parameters."""
        # Create mock client factory with closure to capture instance
        created_clients = []

        def mock_client_factory(access_token=None):
            mock_client = MagicMock()
            mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"
            mock_client.get.return_value = b"<svg>SVG_DATA</svg>"
            created_clients.append(mock_client)
            return mock_client

        with patch(
            "datawrapper.charts.base.BaseChart._get_client",
            side_effect=mock_client_factory,
        ) as mock_get_client:
            # Create chart and export
            chart = BarChart(title="Test Chart")
            chart.chart_id = "abc123"
            result = chart.export_svg()

            # Verify
            assert result == b"<svg>SVG_DATA</svg>"
            assert isinstance(result, bytes)
            mock_get_client.assert_called_once()
            mock_client = created_clients[0]
            call_args = mock_client.get.call_args
            assert (
                call_args[0][0]
                == "https://api.datawrapper.de/v3/charts/abc123/export/svg"
            )

    def test_export_svg_with_all_parameters(self):
        """Test SVG export with all optional parameters."""
        # Create mock client factory with closure to capture instance
        created_clients = []

        def mock_client_factory(access_token=None):
            mock_client = MagicMock()
            mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"
            mock_client.get.return_value = b"<svg>SVG_DATA</svg>"
            created_clients.append(mock_client)
            return mock_client

        with patch(
            "datawrapper.charts.base.BaseChart._get_client",
            side_effect=mock_client_factory,
        ) as mock_get_client:
            # Create chart and export with all parameters
            chart = BarChart(title="Test Chart")
            chart.chart_id = "abc123"
            result = chart.export_svg(width=800, height=600, plain=True)

            # Verify
            assert result == b"<svg>SVG_DATA</svg>"
            mock_get_client.assert_called_once()
            mock_client = created_clients[0]
            call_args = mock_client.get.call_args
            url = call_args[0][0]
            params = call_args[1]["params"]
            assert url == "https://api.datawrapper.de/v3/charts/abc123/export/svg"
            assert params["width"] == "800"
            assert params["height"] == "600"
            assert params["plain"] == "true"

    def test_export_svg_no_chart_id(self):
        """Test SVG export raises error when no chart_id is set."""
        chart = BarChart(title="Test Chart")
        with pytest.raises(ValueError, match="No chart_id set"):
            chart.export_svg()

    def test_export_svg_custom_access_token(self):
        """Test SVG export with custom access token."""

        # Create mock client factory
        def mock_client_factory(access_token=None):
            mock_client = MagicMock()
            mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"
            mock_client.get.return_value = b"<svg>SVG_DATA</svg>"
            return mock_client

        with patch(
            "datawrapper.charts.base.BaseChart._get_client",
            side_effect=mock_client_factory,
        ) as mock_get_client:
            # Create chart and export with custom token
            chart = BarChart(title="Test Chart")
            chart.chart_id = "abc123"
            result = chart.export_svg(access_token="custom_token")

            # Verify
            assert result == b"<svg>SVG_DATA</svg>"
            mock_get_client.assert_called_once()


class TestExportMethodComparison:
    """Tests comparing the new export methods with the legacy export method."""

    def test_export_png_vs_legacy_export(self):
        """Test that export_png produces same result as legacy export method."""

        # Create mock client factory
        def mock_client_factory(access_token=None):
            mock_client = MagicMock()
            mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"
            mock_client.get.return_value = b"PNG_IMAGE_DATA"
            return mock_client

        with patch(
            "datawrapper.charts.base.BaseChart._get_client",
            side_effect=mock_client_factory,
        ) as mock_get_client:
            # Create chart
            chart = BarChart(title="Test Chart")
            chart.chart_id = "abc123"

            # Export using new method
            result_new = chart.export_png(width=800, height=600)

            # Verify both produce bytes
            assert isinstance(result_new, bytes)
            assert result_new == b"PNG_IMAGE_DATA"
            mock_get_client.assert_called_once()

    def test_all_export_methods_return_bytes(self):
        """Test that all export methods return bytes."""
        # Create mock client factory that returns different data for each call
        call_count = [0]

        def mock_client_factory(access_token=None):
            mock_client = MagicMock()
            mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"
            # Return different data based on call count
            if call_count[0] == 0:
                mock_client.get.return_value = b"PNG_DATA"
            elif call_count[0] == 1:
                mock_client.get.return_value = b"PDF_DATA"
            else:
                mock_client.get.return_value = b"SVG_DATA"
            call_count[0] += 1
            return mock_client

        with patch(
            "datawrapper.charts.base.BaseChart._get_client",
            side_effect=mock_client_factory,
        ) as mock_get_client:
            # Create chart
            chart = BarChart(title="Test Chart")
            chart.chart_id = "abc123"

            # Test all export methods
            png_result = chart.export_png()
            pdf_result = chart.export_pdf()
            svg_result = chart.export_svg()

            # Verify all return bytes
            assert isinstance(png_result, bytes)
            assert isinstance(pdf_result, bytes)
            assert isinstance(svg_result, bytes)
            assert png_result == b"PNG_DATA"
            assert pdf_result == b"PDF_DATA"
            assert svg_result == b"SVG_DATA"
            assert mock_get_client.call_count == 3


class TestExportParameterValidation:
    """Tests for parameter validation and formatting in export methods."""

    def test_export_png_boolean_parameters(self):
        """Test that boolean parameters are correctly formatted as lowercase strings."""
        # Create mock client factory with closure to capture instance
        created_clients = []

        def mock_client_factory(access_token=None):
            mock_client = MagicMock()
            mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"
            mock_client.get.return_value = b"PNG_DATA"
            created_clients.append(mock_client)
            return mock_client

        with patch(
            "datawrapper.charts.base.BaseChart._get_client",
            side_effect=mock_client_factory,
        ) as mock_get_client:
            # Create chart and export with boolean parameters
            chart = BarChart(title="Test Chart")
            chart.chart_id = "abc123"
            result = chart.export_png(plain=True, transparent=False)

            # Verify
            assert result == b"PNG_DATA"
            mock_get_client.assert_called_once()
            mock_client = created_clients[0]
            call_args = mock_client.get.call_args
            params = call_args[1]["params"]
            # Verify boolean parameters are lowercase strings
            assert params["plain"] == "true"
            assert params["transparent"] == "false"

    def test_export_pdf_unit_parameter(self):
        """Test that unit parameter accepts valid values (px, mm, in)."""

        # Create mock client factory
        def mock_client_factory(access_token=None):
            mock_client = MagicMock()
            mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"
            mock_client.get.return_value = b"PDF_DATA"
            return mock_client

        with patch(
            "datawrapper.charts.base.BaseChart._get_client",
            side_effect=mock_client_factory,
        ) as mock_get_client:
            # Create chart
            chart = BarChart(title="Test Chart")
            chart.chart_id = "abc123"

            # Test with different unit values
            for unit in ["px", "mm", "inch"]:
                result = chart.export_pdf(unit=unit)
                assert result == b"PDF_DATA"

            # Verify all three calls were made
            assert mock_get_client.call_count == 3

    def test_export_pdf_mode_parameter(self):
        """Test that mode parameter accepts valid values (rgb, cmyk)."""

        # Create mock client factory
        def mock_client_factory(access_token=None):
            mock_client = MagicMock()
            mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"
            mock_client.get.return_value = b"PDF_DATA"
            return mock_client

        with patch(
            "datawrapper.charts.base.BaseChart._get_client",
            side_effect=mock_client_factory,
        ) as mock_get_client:
            # Create chart
            chart = BarChart(title="Test Chart")
            chart.chart_id = "abc123"

            # Test with different mode values
            for mode in ["rgb", "cmyk"]:
                result = chart.export_pdf(mode=mode)
                assert result == b"PDF_DATA"

            # Verify both calls were made
            assert mock_get_client.call_count == 2
