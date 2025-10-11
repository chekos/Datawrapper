"""Pytest configuration and global fixtures for datawrapper-api-classes tests."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import Mock

import pandas as pd
import pytest
from faker import Faker
from pydantic import BaseModel

# Import our modules
from datawrapper import (
    BarChart,
    BaseChart,
    RangeAnnotation,
    TextAnnotation,
)

# Init the faker
fake = Faker()

# ============================================================================
# Test Data Factories
# ============================================================================


class DataFrameFactory:
    """Factory for creating test DataFrames."""

    @classmethod
    def simple_bar_data(cls, rows: int = 5) -> pd.DataFrame:
        """Create simple bar chart data."""
        return pd.DataFrame(
            {
                "labels": [f"Category {i}" for i in range(1, rows + 1)],
                "values": [fake.random_int(min=10, max=100) for _ in range(rows)],
            }
        )

    @classmethod
    def time_series_data(cls, rows: int = 10) -> pd.DataFrame:
        """Create time series data."""
        dates = pd.date_range(start="2023-01-01", periods=rows, freq="D")
        return pd.DataFrame(
            {
                "date": dates,
                "value": [fake.random_int(min=50, max=200) for _ in range(rows)],
            }
        )

    @classmethod
    def multi_column_data(cls, rows: int = 5, columns: int = 3) -> pd.DataFrame:
        """Create multi-column data."""
        data: dict[str, Any] = {"labels": [f"Row {i}" for i in range(1, rows + 1)]}
        for col in range(1, columns + 1):
            data[f"col_{col}"] = [fake.random_int(min=1, max=100) for _ in range(rows)]
        return pd.DataFrame(data)

    @classmethod
    def large_dataset(cls, rows: int = 1000) -> pd.DataFrame:
        """Create large dataset for performance testing."""
        return pd.DataFrame(
            {
                "category": [f"Cat_{i % 20}" for i in range(rows)],
                "value": [fake.random_int(min=1, max=1000) for _ in range(rows)],
                "date": [
                    fake.date_between(start_date="-1y", end_date="today")
                    for _ in range(rows)
                ],
            }
        )


class ChartFactory:
    """Factory for creating test charts."""

    @classmethod
    def simple_bar_chart(cls, **kwargs) -> BarChart:
        """Create a simple bar chart."""
        defaults = {
            "title": fake.sentence(nb_words=4),
            "data": DataFrameFactory.simple_bar_data(),
            "label_column": "labels",
            "bar_column": "values",
        }
        defaults.update(kwargs)
        return BarChart(**defaults)

    @classmethod
    def bar_chart_with_annotations(cls, **kwargs) -> BarChart:
        """Create bar chart with annotations."""
        defaults = {
            "title": fake.sentence(nb_words=4),
            "data": DataFrameFactory.simple_bar_data(),
            "label_column": "labels",
            "bar_column": "values",
            "text_annotations": [
                TextAnnotation(text="Test annotation", x=10, y=20),
                TextAnnotation(text="Another annotation", x=30, y=40),
            ],
            "range_annotations": [
                RangeAnnotation(x0=0, x1=50, y0=0, y1=100),
                RangeAnnotation(x0=50, x1=100, y0=0, y1=100),
            ],
        }
        defaults.update(kwargs)
        return BarChart(**defaults)


class AnnotationFactory:
    """Factory for creating test annotations."""

    @classmethod
    def text_annotation(cls, **kwargs) -> TextAnnotation:
        """Create a text annotation."""
        defaults = {
            "text": fake.sentence(),
            "x": fake.random_int(min=0, max=100),
            "y": fake.random_int(min=0, max=100),
        }
        defaults.update(kwargs)
        return TextAnnotation(**defaults)

    @classmethod
    def range_annotation(cls, **kwargs) -> RangeAnnotation:
        """Create a range annotation."""
        x0 = fake.random_int(min=0, max=50)
        x1 = x0 + fake.random_int(min=10, max=50)
        defaults = {
            "x0": x0,
            "x1": x1,
            "y0": fake.random_int(min=0, max=50),
            "y1": fake.random_int(min=50, max=100),
            "type": "x",  # Use valid literal type
            "color": "#ff0000",  # Use valid color string
            "display": "line",  # Use valid literal type
            "strokeType": "solid",  # Use valid literal type
            "strokeWidth": 1,  # Use valid literal type
        }
        defaults.update(kwargs)
        return RangeAnnotation(**defaults)


# ============================================================================
# Mock API Responses
# ============================================================================


class MockAPIResponseFactory:
    """Factory for creating mock API responses."""

    @staticmethod
    def successful_chart_creation() -> dict[str, Any]:
        """Mock successful chart creation response."""
        return {
            "id": fake.uuid4(),
            "title": fake.sentence(),
            "type": "d3-bars",
            "createdAt": fake.iso8601(),
            "lastModifiedAt": fake.iso8601(),
            "publicUrl": f"https://datawrapper.dwcdn.net/{fake.uuid4()}/",
            "publicVersion": 1,
        }

    @staticmethod
    def chart_update_response() -> dict[str, Any]:
        """Mock chart update response."""
        return {
            "id": fake.uuid4(),
            "title": fake.sentence(),
            "lastModifiedAt": fake.iso8601(),
            "publicVersion": 2,
        }

    @staticmethod
    def api_error_response(status_code: int = 400) -> dict[str, Any]:
        """Mock API error response."""
        return {
            "error": {
                "code": status_code,
                "message": fake.sentence(),
                "details": fake.text(),
            }
        }


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """Provide a standard test DataFrame."""
    return DataFrameFactory.simple_bar_data()


@pytest.fixture
def large_dataframe() -> pd.DataFrame:
    """Provide a large DataFrame for performance testing."""
    return DataFrameFactory.large_dataset()


@pytest.fixture
def time_series_dataframe() -> pd.DataFrame:
    """Provide time series data."""
    return DataFrameFactory.time_series_data()


@pytest.fixture
def simple_bar_chart() -> BarChart:
    """Provide a simple bar chart for testing."""
    return ChartFactory.simple_bar_chart()


@pytest.fixture
def bar_chart_with_annotations() -> BarChart:
    """Provide a bar chart with annotations."""
    return ChartFactory.bar_chart_with_annotations()


@pytest.fixture
def text_annotation() -> TextAnnotation:
    """Provide a text annotation."""
    return AnnotationFactory.text_annotation()


@pytest.fixture
def range_annotation() -> RangeAnnotation:
    """Provide a range annotation."""
    return AnnotationFactory.range_annotation()


@pytest.fixture
def mock_datawrapper_client():
    """Provide a mocked Datawrapper client."""
    mock_client = Mock()

    # Mock successful responses
    mock_client.post.return_value = MockAPIResponseFactory.successful_chart_creation()
    mock_client.patch.return_value = MockAPIResponseFactory.chart_update_response()
    mock_client.put.return_value = None
    mock_client.get.return_value = {"data": "mock_data"}
    mock_client.delete.return_value = None

    return mock_client


@pytest.fixture
def mock_api_responses():
    """Provide mock API response factory."""
    return MockAPIResponseFactory


@pytest.fixture
def temp_config_file():
    """Provide a temporary configuration file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        config = {
            "access_token": "test-token-123",
            "api_base": "https://api.datawrapper.de/v3",
        }
        json.dump(config, f)
        temp_path = f.name

    yield temp_path

    # Cleanup
    os.unlink(temp_path)


@pytest.fixture
def env_with_token(monkeypatch):
    """Set up environment with Datawrapper token."""
    monkeypatch.setenv("DATAWRAPPER_ACCESS_TOKEN", "test-env-token")


@pytest.fixture
def clean_env(monkeypatch):
    """Clean environment of Datawrapper-related variables."""
    monkeypatch.delenv("DATAWRAPPER_ACCESS_TOKEN", raising=False)


@pytest.fixture
def invalid_data_samples():
    """Provide samples of invalid data for testing validation."""
    return {
        "empty_dataframe": pd.DataFrame(),
        "missing_columns": pd.DataFrame({"wrong_col": [1, 2, 3]}),
        "null_values": pd.DataFrame(
            {"labels": [None, "B", "C"], "values": [1, None, 3]}
        ),
        "wrong_types": pd.DataFrame({"labels": [1, 2, 3], "values": ["a", "b", "c"]}),
        "duplicate_labels": pd.DataFrame(
            {"labels": ["A", "A", "B"], "values": [1, 2, 3]}
        ),
    }


@pytest.fixture
def chart_metadata_samples():
    """Provide sample chart metadata for testing."""
    return {
        "minimal": {"title": "Test Chart", "type": "d3-bars"},
        "complete": {
            "title": "Complete Test Chart",
            "type": "d3-bars",
            "metadata": {
                "describe": {
                    "source-name": "Test Source",
                    "source-url": "https://example.com",
                    "byline": "Test Author",
                },
                "visualize": {"text-annotations": [], "range-annotations": []},
            },
        },
    }


# ============================================================================
# Test Utilities
# ============================================================================


@pytest.fixture
def assert_valid_chart():
    """Utility function to assert chart validity."""

    def _assert_valid_chart(chart: BaseChart):
        """Assert that a chart is valid."""
        assert chart.title is not None
        assert len(chart.title.strip()) > 0
        assert chart.chart_type is not None

        # Test serialization
        serialized = chart.serialize_model()
        assert isinstance(serialized, dict)
        assert "metadata" in serialized

        # Test model validation
        chart.model_validate(chart.model_dump())

    return _assert_valid_chart


@pytest.fixture
def assert_valid_serialization():
    """Utility function to assert serialization validity."""

    def _assert_valid_serialization(obj: BaseModel):
        """Assert that a Pydantic model serializes correctly."""
        # Test Python dict serialization
        python_dict = obj.model_dump(by_alias=True)
        assert isinstance(python_dict, dict)

        # Test JSON serialization
        json_str = obj.model_dump_json(by_alias=True)
        assert isinstance(json_str, str)

        # Test round-trip
        reconstructed = obj.__class__.model_validate_json(json_str)
        assert reconstructed == obj

    return _assert_valid_serialization


# ============================================================================
# Performance Testing Fixtures
# ============================================================================


@pytest.fixture
def benchmark_data():
    """Provide data for benchmark tests."""
    return {
        "small": DataFrameFactory.simple_bar_data(rows=10),
        "medium": DataFrameFactory.simple_bar_data(rows=100),
        "large": DataFrameFactory.simple_bar_data(rows=1000),
        "xlarge": DataFrameFactory.simple_bar_data(rows=10000),
    }


# ============================================================================
# Parametrized Fixtures
# ============================================================================


@pytest.fixture(params=["small", "medium", "large"])
def chart_sizes(request, benchmark_data):
    """Parametrized fixture for different chart sizes."""
    return benchmark_data[request.param]


@pytest.fixture(
    params=[
        {"chart_type": "d3-bars", "class": BarChart},
        # Add more chart types as they're implemented
    ]
)
def chart_types(request):
    """Parametrized fixture for different chart types."""
    return request.param


# ============================================================================
# Cleanup and Setup
# ============================================================================


@pytest.fixture(autouse=True)
def cleanup_temp_files():
    """Automatically cleanup temporary files after each test."""
    yield
    # Cleanup any temporary files created during tests
    temp_dir = Path(tempfile.gettempdir())
    for temp_file in temp_dir.glob("pytest_*"):
        try:
            temp_file.unlink()
        except (OSError, PermissionError):
            pass  # Ignore cleanup errors


def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Add custom markers
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "functional: marks tests as functional tests")
    config.addinivalue_line("markers", "api: marks tests as API tests")
    config.addinivalue_line("markers", "benchmark: marks tests as benchmark tests")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        # Add markers based on test file location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "functional" in str(item.fspath):
            item.add_marker(pytest.mark.functional)
        elif "api" in str(item.fspath):
            item.add_marker(pytest.mark.api)
            item.add_marker(pytest.mark.slow)

        # Mark benchmark tests
        if "benchmark" in item.name or "perf" in item.name:
            item.add_marker(pytest.mark.benchmark)
            item.add_marker(pytest.mark.slow)


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_workspaces_session():
    """Clean up test workspaces before and after test session."""

    def _cleanup():
        """Helper to cleanup test workspaces."""
        try:
            from datawrapper import Datawrapper
            from datawrapper.exceptions import RateLimitError

            # Only run if we have an API token
            if not os.getenv("DATAWRAPPER_ACCESS_TOKEN"):
                return

            dw = Datawrapper()
            workspaces = dw.get_workspaces()

            for workspace in workspaces["list"]:
                if workspace["name"].startswith("Test Workspace"):
                    try:
                        dw.delete_workspace(workspace["slug"])
                    except RateLimitError:
                        # Stop on rate limit to avoid further issues
                        break
                    except Exception:
                        # Ignore other errors during cleanup
                        pass
        except Exception:
            # Silently ignore all cleanup errors
            pass

    # Cleanup before tests
    _cleanup()

    yield

    # Cleanup after tests
    _cleanup()
