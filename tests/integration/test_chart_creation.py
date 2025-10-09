"""Integration tests for chart creation workflows."""

import pandas as pd
import pytest

from datawrapper import BarChart, RangeAnnotation, TextAnnotation


class TestChartCreationWorkflow:
    """Test complete chart creation workflows."""

    @pytest.mark.integration
    def test_bar_chart_creation_workflow(self, sample_dataframe):
        """Test complete bar chart creation workflow."""
        # Create chart
        chart = BarChart(
            title="Integration Test Chart",
            data=sample_dataframe,
            label_column="labels",
            bar_column="values",
        )

        # Verify chart properties
        assert chart.title == "Integration Test Chart"
        assert chart.chart_type == "d3-bars"
        assert chart.data is not None
        assert len(chart.data) == len(sample_dataframe)

        # Test serialization
        serialized = chart.serialize_model()
        assert isinstance(serialized, dict)
        assert "metadata" in serialized
        assert "title" in serialized
        assert serialized["title"] == "Integration Test Chart"

    @pytest.mark.integration
    def test_chart_with_annotations_workflow(self, sample_dataframe):
        """Test chart creation with annotations."""
        # Create annotations
        text_annotation = TextAnnotation(
            text="Peak value", x=2, y=80, bold=True, color="#FF0000"
        )

        range_annotation = RangeAnnotation(
            type="y", x0=0, x1=4, y0=50, y1=100, color="#00FF00", opacity=30
        )

        # Create chart with annotations
        chart = BarChart(
            title="Chart with Annotations",
            data=sample_dataframe,
            label_column="labels",
            bar_column="values",
            text_annotations=[text_annotation],
            range_annotations=[range_annotation],
        )

        # Verify annotations are included
        assert len(chart.text_annotations) == 1
        assert len(chart.range_annotations) == 1
        assert chart.text_annotations[0].text == "Peak value"
        assert chart.range_annotations[0].color == "#00FF00"

        # Test serialization includes annotations
        serialized = chart.serialize_model()
        metadata = serialized["metadata"]
        assert "visualize" in metadata
        assert "text-annotations" in metadata["visualize"]
        assert "range-annotations" in metadata["visualize"]
        assert len(metadata["visualize"]["text-annotations"]) == 1
        assert len(metadata["visualize"]["range-annotations"]) == 1

    @pytest.mark.integration
    def test_data_validation_workflow(self):
        """Test data validation in chart creation workflow."""
        # Test with valid data
        valid_data = pd.DataFrame(
            {"categories": ["A", "B", "C"], "values": [10, 20, 30]}
        )

        chart = BarChart(
            title="Valid Data Chart",
            data=valid_data,
            label_column="categories",
            bar_column="values",
        )

        assert chart.data is not None
        assert len(chart.data) == 3

        # Test serialization works
        serialized = chart.serialize_model()
        assert "metadata" in serialized

    @pytest.mark.integration
    def test_chart_update_workflow(self, simple_bar_chart):
        """Test chart update workflow."""
        original_title = simple_bar_chart.title

        # Update chart properties
        simple_bar_chart.title = "Updated Title"

        # Add annotation
        new_annotation = TextAnnotation(text="New annotation", x=1, y=50)
        simple_bar_chart.text_annotations.append(new_annotation)

        # Verify updates
        assert simple_bar_chart.title == "Updated Title"
        assert simple_bar_chart.title != original_title
        assert len(simple_bar_chart.text_annotations) == 1

        # Test serialization reflects updates
        serialized = simple_bar_chart.serialize_model()
        assert serialized["title"] == "Updated Title"
        assert len(serialized["metadata"]["visualize"]["text-annotations"]) == 1

    @pytest.mark.integration
    def test_multiple_chart_types_workflow(self, sample_dataframe):
        """Test workflow with multiple chart configurations."""
        charts = []

        # Create different chart configurations
        configs = [
            {"title": "Basic Chart", "text_annotations": []},
            {
                "title": "Chart with Text",
                "text_annotations": [TextAnnotation(text="Note", x=0, y=0)],
            },
            {
                "title": "Chart with Range",
                "range_annotations": [RangeAnnotation(x0=0, x1=2, y0=0, y1=50)],
            },
        ]

        for config in configs:
            chart = BarChart(
                data=sample_dataframe,
                label_column="labels",
                bar_column="values",
                **config,
            )
            charts.append(chart)

        # Verify all charts were created successfully
        assert len(charts) == 3
        for chart in charts:
            assert chart.chart_type == "d3-bars"
            serialized = chart.serialize_model()
            assert "metadata" in serialized
            assert "title" in serialized

    @pytest.mark.integration
    @pytest.mark.slow
    def test_large_dataset_workflow(self, large_dataframe):
        """Test workflow with large dataset."""
        chart = BarChart(
            title="Large Dataset Chart",
            data=large_dataframe,
            label_column="category",
            bar_column="value",
        )

        # Verify chart handles large data
        assert chart.data is not None
        assert len(chart.data) == len(large_dataframe)

        # Test serialization performance
        serialized = chart.serialize_model()
        assert isinstance(serialized, dict)
        assert "metadata" in serialized

    @pytest.mark.integration
    def test_chart_serialization_roundtrip(self, simple_bar_chart):
        """Test complete serialization roundtrip."""
        # Serialize chart
        serialized = simple_bar_chart.serialize_model()

        # Verify serialized structure
        assert isinstance(serialized, dict)
        assert "title" in serialized
        assert "type" in serialized
        assert "metadata" in serialized

        # Verify metadata structure
        metadata = serialized["metadata"]
        assert "describe" in metadata
        assert "visualize" in metadata

        # Verify visualize section
        visualize = metadata["visualize"]
        assert "text-annotations" in visualize
        assert "range-annotations" in visualize
        assert isinstance(visualize["text-annotations"], list)
        assert isinstance(visualize["range-annotations"], list)


class TestChartValidationWorkflow:
    """Test chart validation workflows."""

    @pytest.mark.integration
    def test_invalid_data_handling(self, invalid_data_samples):
        """Test handling of invalid data in workflow."""
        for data_type, invalid_data in invalid_data_samples.items():
            if data_type == "empty_dataframe":
                # Empty dataframe should be handled gracefully
                chart = BarChart(
                    title="Empty Data Test",
                    data=invalid_data,
                    label_column="labels",
                    bar_column="values",
                )
                assert chart.data is not None
                assert len(chart.data) == 0

    @pytest.mark.integration
    def test_annotation_validation_workflow(self):
        """Test annotation validation in complete workflow."""
        # Create chart
        chart = BarChart(
            title="Annotation Validation Test",
            data=pd.DataFrame({"labels": ["A", "B"], "values": [1, 2]}),
            label_column="labels",
            bar_column="values",
        )

        # Add valid annotations
        valid_text = TextAnnotation(text="Valid", x=0, y=0)
        valid_range = RangeAnnotation(x0=0, x1=1, y0=0, y1=2)

        chart.text_annotations.append(valid_text)
        chart.range_annotations.append(valid_range)

        # Test serialization works with valid annotations
        serialized = chart.serialize_model()
        assert len(serialized["metadata"]["visualize"]["text-annotations"]) == 1
        assert len(serialized["metadata"]["visualize"]["range-annotations"]) == 1

    @pytest.mark.integration
    def test_chart_metadata_workflow(self, chart_metadata_samples):
        """Test chart metadata handling workflow."""
        for _metadata_type, metadata in chart_metadata_samples.items():
            # Create chart with different metadata configurations
            chart = BarChart(
                title=metadata["title"],
                data=pd.DataFrame({"labels": ["A"], "values": [1]}),
                label_column="labels",
                bar_column="values",
            )

            # Test serialization
            serialized = chart.serialize_model()
            assert serialized["title"] == metadata["title"]
            assert serialized["type"] == "d3-bars"


@pytest.mark.integration
class TestChartFactoryIntegration:
    """Test chart factory integration."""

    def test_factory_chart_creation(self, simple_bar_chart):
        """Test chart created by factory works in full workflow."""
        # Chart should be fully functional
        assert simple_bar_chart.title is not None
        assert simple_bar_chart.data is not None
        assert simple_bar_chart.chart_type == "d3-bars"

        # Should serialize correctly
        serialized = simple_bar_chart.serialize_model()
        assert isinstance(serialized, dict)
        assert "metadata" in serialized

    def test_factory_chart_with_annotations(self, bar_chart_with_annotations):
        """Test annotated chart from factory."""
        # Should have annotations
        assert len(bar_chart_with_annotations.text_annotations) > 0
        assert len(bar_chart_with_annotations.range_annotations) > 0

        # Should serialize with annotations
        serialized = bar_chart_with_annotations.serialize_model()
        visualize = serialized["metadata"]["visualize"]
        assert len(visualize["text-annotations"]) > 0
        assert len(visualize["range-annotations"]) > 0
