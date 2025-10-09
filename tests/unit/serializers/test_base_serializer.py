"""Unit tests for BaseChart serialization."""

import datawrapper


class TestBaseChartSerialization:
    """Test BaseChart model serialization."""

    def test_base_chart_serialize_minimal(self):
        """Test BaseChart serialization with minimal data."""
        chart = datawrapper.BaseChart(title="Test Chart", chart_type="d3-bars")

        # Test the serialize_model method directly
        serialized = chart.serialize_model()

        assert isinstance(serialized, dict)
        assert "title" in serialized
        assert "type" in serialized
        assert serialized["title"] == "Test Chart"
        assert serialized["type"] == "d3-bars"

    def test_base_chart_serialize_with_metadata(self):
        """Test BaseChart serialization with metadata sections."""
        chart = datawrapper.BaseChart(
            title="Test Chart",
            chart_type="d3-bars",
            source_name="Test Source",  # Use individual fields, not Describe object
            byline="Test Author",
            notes="Test notes",
        )

        serialized = chart.serialize_model()

        # Check main structure
        assert isinstance(serialized, dict)
        assert "title" in serialized
        assert "type" in serialized
        assert "metadata" in serialized

        # Check metadata structure
        metadata = serialized["metadata"]
        assert "describe" in metadata
        assert "annotate" in metadata

        # Check describe section
        describe = metadata["describe"]
        assert "source-name" in describe
        assert "byline" in describe
        assert describe["source-name"] == "Test Source"
        assert describe["byline"] == "Test Author"

        # Check annotate section
        annotate = metadata["annotate"]
        assert "notes" in annotate
        assert annotate["notes"] == "Test notes"

    def test_base_chart_serialize_with_data(self):
        """Test BaseChart serialization with data."""
        chart = datawrapper.BaseChart(
            title="Test Chart",
            chart_type="d3-bars",
            data=[
                {"Category": "A", "Value": 10},
                {"Category": "B", "Value": 20},
                {"Category": "C", "Value": 15},
            ],
        )

        serialized = chart.serialize_model()

        assert "title" in serialized
        assert "type" in serialized
        # Note: data might not be in serialized output depending on implementation
        # This tests the serialization doesn't break with data present

    def test_base_chart_model_dump_vs_serialize(self):
        """Test difference between model_dump and serialize_model."""
        chart = datawrapper.BaseChart(
            title="Test Chart", chart_type="d3-bars", byline="Test Author"
        )

        # Test model_dump (Pydantic's built-in)
        model_dump = chart.model_dump(by_alias=True)

        # Test serialize_model (custom serializer)
        serialize_model = chart.serialize_model()

        # Both should be dicts but may have different structures
        assert isinstance(model_dump, dict)
        assert isinstance(serialize_model, dict)

        # serialize_model should have the API structure
        assert "title" in serialize_model
        assert "type" in serialize_model

    def test_base_chart_serialize_empty_metadata(self):
        """Test BaseChart serialization with empty metadata objects."""
        chart = datawrapper.BaseChart(
            title="Test Chart",
            chart_type="d3-bars",
            # No additional metadata - will use defaults
        )

        serialized = chart.serialize_model()

        assert isinstance(serialized, dict)
        assert "metadata" in serialized

        metadata = serialized["metadata"]
        assert "describe" in metadata
        assert "annotate" in metadata

    def test_base_chart_serialize_json_compatibility(self):
        """Test that serialized output is JSON-compatible."""
        import json

        chart = datawrapper.BaseChart(
            title="Test Chart",
            chart_type="d3-bars",
            source_name="Test Source",
            byline="Test Author",
        )

        serialized = chart.serialize_model()

        # Should be able to convert to JSON without errors
        json_str = json.dumps(serialized)
        assert isinstance(json_str, str)

        # Should be able to parse back
        parsed = json.loads(json_str)
        assert parsed["title"] == "Test Chart"
        assert parsed["type"] == "d3-bars"

    def test_base_chart_serialize_special_characters(self):
        """Test BaseChart serialization with special characters."""
        chart = datawrapper.BaseChart(
            title="Chart with émojis 🎉 and ñ",
            chart_type="d3-bars",
            source_name="Source with 中文",
            byline="Author with quotes 'single' \"double\"",
        )

        serialized = chart.serialize_model()

        assert "émojis 🎉 and ñ" in serialized["title"]

        metadata = serialized["metadata"]
        describe = metadata["describe"]
        assert "中文" in describe["source-name"]
        assert "quotes 'single' \"double\"" in describe["byline"]

    def test_base_chart_serialize_none_values(self):
        """Test BaseChart serialization with None values."""
        chart = datawrapper.BaseChart(
            title="Test Chart",
            chart_type="d3-bars",
            # Use default empty values for metadata
        )

        # Should not raise an error
        serialized = chart.serialize_model()
        assert isinstance(serialized, dict)
        assert "title" in serialized
        assert "type" in serialized
