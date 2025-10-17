"""Tests using real Datawrapper chart samples to validate our implementation."""

import json
from pathlib import Path
from typing import Any

import pytest

from datawrapper import BarChart


@pytest.fixture
def european_turnout_sample():
    """Load the european turnout sample JSON."""
    sample_path = (
        Path(__file__).parent.parent / "samples" / "bar" / "european-turnout.json"
    )
    with open(sample_path) as f:
        return json.load(f)


@pytest.fixture
def european_turnout_metadata(european_turnout_sample):
    """Extract metadata from the european turnout sample."""
    return european_turnout_sample["chart"]["crdt"]["data"]["metadata"]


@pytest.fixture
def european_turnout_visualize(european_turnout_metadata):
    """Extract visualize section from the european turnout sample."""
    return european_turnout_metadata["visualize"]


@pytest.fixture
def european_turnout_chart_data(european_turnout_sample):
    """Extract chart data from the european turnout sample."""
    return european_turnout_sample["chart"]["crdt"]["data"]


def extract_field_paths(obj: dict[str, Any], prefix: str = "") -> set[str]:
    """Extract all field paths from a nested dict."""
    paths = set()
    for key, value in obj.items():
        current_path = f"{prefix}.{key}" if prefix else key
        paths.add(current_path)
        if isinstance(value, dict):
            paths.update(extract_field_paths(value, current_path))
    return paths


def compare_dict_structure(
    actual: dict[str, Any], expected: dict[str, Any], path: str = ""
) -> list[str]:
    """Compare two dict structures and return list of differences."""
    differences = []

    # Check for missing keys in actual
    for key in expected:
        if key not in actual:
            differences.append(
                f"Missing key at {path}.{key}" if path else f"Missing key: {key}"
            )

    # Check for extra keys in actual (optional - might be too strict)
    # for key in actual:
    #     if key not in expected:
    #         differences.append(f"Extra key at {path}.{key}" if path else f"Extra key: {key}")

    return differences


class TestSampleLoading:
    """Test that we can load and parse sample JSON files correctly."""

    def test_load_european_turnout_sample(self, european_turnout_sample):
        """Test that we can load the european turnout sample JSON."""
        assert european_turnout_sample is not None
        assert isinstance(european_turnout_sample, dict)

    def test_sample_has_required_structure(self, european_turnout_sample):
        """Verify the sample has the expected top-level structure."""
        assert "chart" in european_turnout_sample
        assert "crdt" in european_turnout_sample["chart"]
        assert "data" in european_turnout_sample["chart"]["crdt"]

        data = european_turnout_sample["chart"]["crdt"]["data"]
        assert "metadata" in data
        assert "type" in data
        assert "title" in data
        assert data["type"] == "d3-bars"

    def test_metadata_structure(self, european_turnout_metadata):
        """Test that metadata has expected sections."""
        expected_sections = [
            "data",
            "describe",
            "visualize",
            "axes",
            "publish",
            "annotate",
            "custom",
        ]

        for section in expected_sections:
            assert section in european_turnout_metadata, (
                f"Missing metadata section: {section}"
            )

    def test_visualize_section_exists(self, european_turnout_visualize):
        """Test that visualize section has expected structure."""
        assert isinstance(european_turnout_visualize, dict)
        assert len(european_turnout_visualize) > 0


class TestFieldCoverage:
    """Test which fields from the sample we currently support."""

    def test_visualize_section_coverage(self, european_turnout_visualize):
        """Test that we support the fields in the sample's visualize section."""
        # Fields we currently support in BarChart
        supported_fields = {
            "sort-bars",
            "reverse-order",
            "custom-range",
            "background",
            "tick-position",
            "highlighted-series",
            "show-color-key",
            "base-color",
            "rules",
            "thick",
            "force-grid",
            "show-value-labels",
            "value-label-alignment",
            "value-label-format",
            "swap-labels",
            "replace-flags",
            "stack-color-legend",
            "custom-grid-lines",
            "axis-label-format",
            "color-category",
            "color-by-column",
            "group-by-column",
            "show-group-labels",
            "show-category-labels",
            "overlays",
            "text-annotations",
            "range-annotations",
            "label-alignment",
            "block-labels",
        }

        # Fields in the sample
        sample_fields = set(european_turnout_visualize.keys())

        # Fields we support that are in the sample
        supported_in_sample = sample_fields & supported_fields

        # Fields we don't support yet
        unsupported = sample_fields - supported_fields

        print(f"\nSupported fields in sample: {len(supported_in_sample)}")
        print(f"Unsupported fields in sample: {len(unsupported)}")
        print(f"Unsupported fields: {sorted(unsupported)}")

        # For now, just document what we're missing
        # Later we can make this a failing test to drive implementation
        assert len(supported_in_sample) > 0, "We should support at least some fields"

    def test_axes_section_coverage(self, european_turnout_metadata):
        """Test that we support the fields in the sample's axes section."""
        axes = european_turnout_metadata.get("axes", {})

        # Fields we currently support in BarChart axes
        supported_axes_fields = {"groups", "bars", "labels", "colors"}

        # Fields in the sample
        sample_axes_fields = set(axes.keys())

        print(f"\nAxes fields in sample: {sample_axes_fields}")
        print(f"Supported axes fields: {supported_axes_fields}")

        # We should support the basic axes structure
        if sample_axes_fields:
            supported_in_sample = sample_axes_fields & supported_axes_fields
            assert len(supported_in_sample) > 0, (
                "We should support at least some axes fields"
            )


class TestBarChartCreation:
    """Test creating BarChart instances from sample data."""

    def test_create_bar_chart_from_sample_basic(
        self, european_turnout_chart_data, european_turnout_visualize
    ):
        """Test creating a BarChart from sample metadata - basic fields."""
        # Extract basic fields that we know we support
        chart = BarChart(
            title=european_turnout_chart_data.get("title", ""),
            **{"chart-type": european_turnout_chart_data.get("type", "d3-bars")},
            **{"sort-bars": european_turnout_visualize.get("sort-bars", False)},
            **{"reverse-order": european_turnout_visualize.get("reverse-order", False)},
            background=european_turnout_visualize.get("background", False),
            **{"tick-position": european_turnout_visualize.get("tick-position", "top")},
        )

        # Verify the chart was created successfully
        assert chart.title == european_turnout_chart_data["title"]
        assert chart.chart_type == "d3-bars"
        assert chart.sort_bars == european_turnout_visualize["sort-bars"]
        assert chart.reverse_order == european_turnout_visualize["reverse-order"]
        assert chart.background == european_turnout_visualize["background"]
        assert chart.tick_position == european_turnout_visualize["tick-position"]

    def test_create_bar_chart_with_custom_range(self, european_turnout_visualize):
        """Test creating a BarChart with custom range from sample."""
        custom_range = european_turnout_visualize.get("custom-range", ["", ""])

        chart = BarChart(
            title="Test Chart",
            **{"custom-range": list(custom_range)},
        )

        assert chart.custom_range == list(custom_range)

    def test_create_bar_chart_with_highlighted_series(self, european_turnout_visualize):
        """Test creating a BarChart with highlighted series from sample."""
        highlighted_series = european_turnout_visualize.get("highlighted-series", [])

        chart = BarChart(
            title="Test Chart",
            **{"highlighted-series": highlighted_series},
        )

        assert chart.highlighted_series == highlighted_series

    def test_create_bar_chart_with_color_category(self, european_turnout_visualize):
        """Test creating a BarChart with color category mapping from sample."""
        color_category = european_turnout_visualize.get("color-category", {})
        color_map = color_category.get("map", {})

        if color_map:
            chart = BarChart(
                title="Test Chart",
                **{"color-category": color_map},
            )

            assert chart.color_category == color_map


class TestSerialization:
    """Test that our serialization produces output compatible with the sample format."""

    def test_basic_serialization_structure(self):
        """Test that our serialization has the expected top-level structure."""
        chart = BarChart(title="Test Chart")
        serialized = chart.serialize_model()

        # Check top-level structure
        assert "type" in serialized
        assert "title" in serialized
        assert "metadata" in serialized

        # Check metadata structure
        metadata = serialized["metadata"]
        assert "visualize" in metadata
        assert "axes" in metadata

    def test_serialization_matches_sample_format(self, european_turnout_visualize):
        """Test that our serialization format matches the sample for supported fields."""
        # Create a chart with configuration similar to the sample
        chart = BarChart(
            title="Test Chart",
            **{"sort-bars": european_turnout_visualize.get("sort-bars", False)},
            **{"reverse-order": european_turnout_visualize.get("reverse-order", False)},
            background=european_turnout_visualize.get("background", False),
            **{"tick-position": european_turnout_visualize.get("tick-position", "top")},
            **{
                "highlighted-series": european_turnout_visualize.get(
                    "highlighted-series", []
                )
            },
        )

        # Serialize
        serialized = chart.serialize_model()
        viz = serialized["metadata"]["visualize"]

        # Compare key fields that we support
        assert viz["sort-bars"] == european_turnout_visualize["sort-bars"]
        assert viz["reverse-order"] == european_turnout_visualize["reverse-order"]
        assert viz["background"] == european_turnout_visualize["background"]
        assert viz["tick-position"] == european_turnout_visualize["tick-position"]
        assert (
            viz["highlighted-series"]
            == european_turnout_visualize["highlighted-series"]
        )

    def test_color_category_serialization_format(self, european_turnout_visualize):
        """Test that color-category serialization matches sample format."""
        sample_color_category = european_turnout_visualize.get("color-category", {})
        sample_color_map = sample_color_category.get("map", {})

        if sample_color_map:
            # Create chart with color mapping
            chart = BarChart(
                title="Test Chart",
                **{"color-category": sample_color_map},
            )

            # Serialize
            serialized = chart.serialize_model()

            # Verify color-category structure matches sample format
            color_cat = serialized["metadata"]["visualize"]["color-category"]
            assert "map" in color_cat
            assert color_cat["map"] == sample_color_map

            # Check that we have the same structure as sample
            sample_keys = set(sample_color_category.keys())
            our_keys = set(color_cat.keys())

            # We should at least have the 'map' key
            assert "map" in our_keys

            # Document what we're missing
            missing_keys = sample_keys - our_keys
            if missing_keys:
                print(f"\nMissing color-category keys: {missing_keys}")

    def test_axes_serialization_format(self, european_turnout_metadata):
        """Test that axes serialization matches sample format."""
        sample_axes = european_turnout_metadata.get("axes", {})

        chart = BarChart(
            title="Test Chart",
            **{"custom-range": [0, 100]},
        )

        serialized = chart.serialize_model()
        our_axes = serialized["metadata"]["axes"]

        # Check that we have axes structure
        assert isinstance(our_axes, dict)

        # Document the structure differences
        sample_keys = set(sample_axes.keys())
        our_keys = set(our_axes.keys())

        print(f"\nSample axes keys: {sample_keys}")
        print(f"Our axes keys: {our_keys}")

        # We should have some axes configuration
        assert len(our_keys) > 0


class TestSpecificFeatures:
    """Test specific features found in the sample."""

    def test_custom_range_handling(self, european_turnout_visualize):
        """Test that we handle custom-range the same way as the sample."""
        sample_range = european_turnout_visualize.get("custom-range", ["", ""])

        chart = BarChart(
            title="Test Chart",
            **{"custom-range": list(sample_range)},
        )

        serialized = chart.serialize_model()
        our_range = serialized["metadata"]["visualize"]["custom-range"]

        # Should match the sample format
        assert our_range == sample_range

    def test_highlighted_series_handling(self, european_turnout_visualize):
        """Test that we handle highlighted-series the same way as the sample."""
        sample_highlighted = european_turnout_visualize.get("highlighted-series", [])

        chart = BarChart(
            title="Test Chart",
            **{"highlighted-series": sample_highlighted},
        )

        serialized = chart.serialize_model()
        our_highlighted = serialized["metadata"]["visualize"]["highlighted-series"]

        # Should match the sample format exactly
        assert our_highlighted == sample_highlighted

    def test_boolean_fields_handling(self, european_turnout_visualize):
        """Test that boolean fields are handled consistently with the sample."""
        boolean_fields = [
            ("sort-bars", "sort-bars"),
            ("reverse-order", "reverse-order"),
            ("background", "background"),
            ("show-color-key", "show-color-key"),
            ("rules", "rules"),
            ("thick", "thick"),
        ]

        for sample_key, chart_attr in boolean_fields:
            if sample_key in european_turnout_visualize:
                sample_value = european_turnout_visualize[sample_key]

                # Create chart with this value
                chart_kwargs = {"title": "Test Chart", chart_attr: sample_value}
                chart = BarChart(**chart_kwargs)

                # Serialize and check
                serialized = chart.serialize_model()
                our_value = serialized["metadata"]["visualize"][sample_key]

                assert our_value == sample_value, (
                    f"Mismatch for {sample_key}: expected {sample_value}, got {our_value}"
                )
