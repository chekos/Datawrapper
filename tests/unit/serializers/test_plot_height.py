"""Tests for PlotHeight serializer utility."""

from datawrapper.charts.serializers import PlotHeight


class TestPlotHeightSerialize:
    """Test PlotHeight.serialize() method."""

    def test_serialize_fixed_mode(self):
        """Test serialization with fixed mode."""
        result = PlotHeight.serialize("fixed", 400, 0.5)
        assert result == {
            "plotHeightMode": "fixed",
            "plotHeightFixed": 400,
            "plotHeightRatio": 0.5,
        }

    def test_serialize_ratio_mode(self):
        """Test serialization with ratio mode."""
        result = PlotHeight.serialize("ratio", 300, 0.75)
        assert result == {
            "plotHeightMode": "ratio",
            "plotHeightFixed": 300,
            "plotHeightRatio": 0.75,
        }

    def test_serialize_with_float_fixed(self):
        """Test serialization with float fixed height."""
        result = PlotHeight.serialize("fixed", 350.5, 0.6)
        assert result == {
            "plotHeightMode": "fixed",
            "plotHeightFixed": 350.5,
            "plotHeightRatio": 0.6,
        }


class TestPlotHeightDeserialize:
    """Test PlotHeight.deserialize() method."""

    def test_deserialize_all_fields_present(self):
        """Test deserialization when all fields are present."""
        visualize = {
            "plotHeightMode": "fixed",
            "plotHeightFixed": 400,
            "plotHeightRatio": 0.5,
        }
        result = PlotHeight.deserialize(visualize)
        assert result == {
            "plot_height_mode": "fixed",
            "plot_height_fixed": 400,
            "plot_height_ratio": 0.5,
        }

    def test_deserialize_ratio_mode(self):
        """Test deserialization with ratio mode."""
        visualize = {
            "plotHeightMode": "ratio",
            "plotHeightFixed": 300,
            "plotHeightRatio": 0.75,
        }
        result = PlotHeight.deserialize(visualize)
        assert result == {
            "plot_height_mode": "ratio",
            "plot_height_fixed": 300,
            "plot_height_ratio": 0.75,
        }

    def test_deserialize_missing_fields(self):
        """Test deserialization when fields are missing (should return empty dict)."""
        visualize = {}
        result = PlotHeight.deserialize(visualize)
        assert result == {}

    def test_deserialize_partial_fields(self):
        """Test deserialization when only some fields are present."""
        visualize = {
            "plotHeightMode": "fixed",
            "plotHeightFixed": 350,
        }
        result = PlotHeight.deserialize(visualize)
        assert result == {
            "plot_height_mode": "fixed",
            "plot_height_fixed": 350,
        }

    def test_deserialize_with_float_values(self):
        """Test deserialization with float values."""
        visualize = {
            "plotHeightMode": "ratio",
            "plotHeightFixed": 325.5,
            "plotHeightRatio": 0.625,
        }
        result = PlotHeight.deserialize(visualize)
        assert result == {
            "plot_height_mode": "ratio",
            "plot_height_fixed": 325.5,
            "plot_height_ratio": 0.625,
        }

    def test_deserialize_with_other_fields(self):
        """Test that deserialization ignores unrelated fields."""
        visualize = {
            "plotHeightMode": "fixed",
            "plotHeightFixed": 400,
            "plotHeightRatio": 0.5,
            "some-other-field": "value",
            "another-field": 123,
        }
        result = PlotHeight.deserialize(visualize)
        assert result == {
            "plot_height_mode": "fixed",
            "plot_height_fixed": 400,
            "plot_height_ratio": 0.5,
        }
        # Verify other fields are not included
        assert "some-other-field" not in result
        assert "another-field" not in result


class TestPlotHeightRoundTrip:
    """Test round-trip serialization/deserialization."""

    def test_round_trip_fixed_mode(self):
        """Test that serialize -> deserialize preserves data for fixed mode."""
        # Serialize
        serialized = PlotHeight.serialize("fixed", 400, 0.5)
        # Deserialize
        deserialized = PlotHeight.deserialize(serialized)
        # Verify
        assert deserialized == {
            "plot_height_mode": "fixed",
            "plot_height_fixed": 400,
            "plot_height_ratio": 0.5,
        }

    def test_round_trip_ratio_mode(self):
        """Test that serialize -> deserialize preserves data for ratio mode."""
        # Serialize
        serialized = PlotHeight.serialize("ratio", 300, 0.75)
        # Deserialize
        deserialized = PlotHeight.deserialize(serialized)
        # Verify
        assert deserialized == {
            "plot_height_mode": "ratio",
            "plot_height_fixed": 300,
            "plot_height_ratio": 0.75,
        }
