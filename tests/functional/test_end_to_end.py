"""Functional end-to-end tests for datawrapper-api-classes."""

import json

import pandas as pd
import pytest

from datawrapper import BarChart, RangeAnnotation, TextAnnotation


@pytest.mark.api
class TestEndToEndWorkflows:
    """Test complete end-to-end workflows."""

    @pytest.mark.functional
    def test_complete_chart_creation_and_publication_workflow(self, sample_dataframe):
        """Test complete workflow from data to published chart."""
        # Step 1: Create chart with data
        chart = BarChart(
            title="End-to-End Test Chart",
            data=sample_dataframe,
            label_column="labels",
            bar_column="values",
            source_name="Test Source",
            source_url="https://example.com",
        )

        # Step 2: Add annotations
        text_annotation = TextAnnotation(
            text="Highest value", x=2, y=90, bold=True, color="#FF0000"
        )
        chart.text_annotations.append(text_annotation)

        range_annotation = RangeAnnotation(
            type="y", x0=0, x1=4, y0=75, y1=100, color="#00FF00", opacity=25
        )
        chart.range_annotations.append(range_annotation)

        # Step 3: Verify chart is properly configured
        assert chart.title == "End-to-End Test Chart"
        assert len(chart.text_annotations) == 1
        assert len(chart.range_annotations) == 1
        assert chart.source_name == "Test Source"

        # Step 4: Test serialization produces valid structure
        serialized = chart.serialize_model()
        assert isinstance(serialized, dict)
        assert "metadata" in serialized
        assert "title" in serialized
        assert serialized["title"] == "End-to-End Test Chart"

        # Verify annotations are serialized
        visualize = serialized["metadata"]["visualize"]
        assert len(visualize["text-annotations"]) == 1
        assert len(visualize["range-annotations"]) == 1

        # Verify axes configuration
        axes = serialized["metadata"]["axes"]
        assert axes["labels"] == "labels"
        assert axes["bars"] == "values"

    @pytest.mark.functional
    def test_data_processing_workflow(self):
        """Test data processing from raw data to chart-ready format."""
        # Step 1: Start with messy real-world data
        raw_data = pd.DataFrame(
            {
                "Country Name": ["United States", "Germany", "Japan", "Brazil"],
                "GDP (Billions)": [21427.7, 3846.4, 4937.4, 1869.2],
                "Population": [331002651, 83783942, 126476461, 212559417],
                "Year": [2019, 2019, 2019, 2019],
            }
        )

        # Step 2: Process data for visualization
        processed_data = raw_data[["Country Name", "GDP (Billions)"]].copy()
        processed_data = processed_data.sort_values("GDP (Billions)", ascending=False)

        # Step 3: Create chart with processed data
        chart = BarChart(
            title="GDP by Country (2019)",
            data=processed_data,
            label_column="Country Name",
            bar_column="GDP (Billions)",
            sort_bars=True,
            reverse_order=False,
        )

        # Step 4: Verify chart handles the data correctly
        assert chart.data is not None
        assert len(chart.data) == 4
        assert chart.sort_bars is True

        # Step 5: Test serialization
        serialized = chart.serialize_model()
        assert serialized["metadata"]["axes"]["labels"] == "Country Name"
        assert serialized["metadata"]["axes"]["bars"] == "GDP (Billions)"

    @pytest.mark.functional
    def test_annotation_workflow(self, sample_dataframe):
        """Test complete annotation workflow."""
        # Step 1: Create base chart
        chart = BarChart(
            title="Annotation Workflow Test",
            data=sample_dataframe,
            label_column="labels",
            bar_column="values",
        )

        # Step 2: Add multiple types of annotations
        annotations_to_add = [
            TextAnnotation(text="Peak", x=2, y=85, bold=True),
            TextAnnotation(text="Valley", x=1, y=25, italic=True),
            RangeAnnotation(type="y", x0=0, x1=4, y0=50, y1=80, color="#FFFF00"),
            RangeAnnotation(type="x", x0=1, x1=3, y0=0, y1=100, color="#FF00FF"),
        ]

        # Step 3: Add annotations one by one
        for annotation in annotations_to_add[:2]:  # Text annotations
            chart.text_annotations.append(annotation)

        for annotation in annotations_to_add[2:]:  # Range annotations
            chart.range_annotations.append(annotation)

        # Step 4: Verify annotations are properly stored
        assert len(chart.text_annotations) == 2
        assert len(chart.range_annotations) == 2

        # Step 5: Test serialization includes all annotations
        serialized = chart.serialize_model()
        visualize = serialized["metadata"]["visualize"]

        assert len(visualize["text-annotations"]) == 2
        assert len(visualize["range-annotations"]) == 2

        # Step 6: Verify annotation properties are preserved
        # Annotations are now stored as lists
        text_annos = visualize["text-annotations"]
        assert text_annos[0]["text"] == "Peak"
        assert text_annos[0]["bold"] is True
        assert text_annos[1]["text"] == "Valley"
        assert text_annos[1]["italic"] is True

        range_annos = visualize["range-annotations"]
        assert range_annos[0]["type"] == "y"
        assert range_annos[0]["color"] == "#FFFF00"
        assert range_annos[1]["type"] == "x"
        assert range_annos[1]["color"] == "#FF00FF"

    @pytest.mark.functional
    def test_chart_customization_workflow(self, sample_dataframe):
        """Test complete chart customization workflow."""
        # Step 1: Create chart with basic customizations
        chart = BarChart(
            title="Customization Test",
            data=sample_dataframe,
            label_column="labels",
            bar_column="values",
            base_color="#4682B4",
            background=True,
            thick=True,
        )

        # Step 2: Apply advanced customizations
        chart.sort_bars = True
        chart.reverse_order = True
        chart.show_value_labels = True
        chart.value_label_format = "0.1f"
        chart.tick_position = "bottom"
        chart.custom_range = (0, 100)

        # Step 3: Add color customizations
        chart.color_category = {
            "High": "#FF0000",
            "Medium": "#FFFF00",
            "Low": "#00FF00",
        }
        chart.show_color_key = True

        # Step 4: Verify customizations are applied
        assert chart.base_color == "#4682B4"
        assert chart.background is True
        assert chart.thick is True
        assert chart.sort_bars is True
        assert chart.reverse_order is True
        assert chart.custom_range == (0, 100)
        assert len(chart.color_category) == 3

        # Step 5: Test serialization includes customizations
        serialized = chart.serialize_model()
        visualize = serialized["metadata"]["visualize"]

        assert visualize["base-color"] == "#4682B4"
        assert visualize["background"] is True
        assert visualize["thick"] is True
        assert visualize["sort-bars"] is True
        assert visualize["reverse-order"] is True
        assert visualize["custom-range"] == [0, 100]
        assert visualize["show-color-key"] is True
        assert len(visualize["color-category"]["map"]) == 3

    @pytest.mark.functional
    def test_error_handling_workflow(self):
        """Test error handling in complete workflows."""
        # Test 1: Valid chart creation with minimal required fields
        valid_data = pd.DataFrame({"labels": ["A", "B"], "values": [1, 2]})

        # Should work with minimal required fields
        chart = BarChart(data=valid_data, label_column="labels", bar_column="values")
        assert chart.title == ""  # Default empty title

        # Test 2: Chart creation with empty data (should be allowed for later population)
        chart_with_empty_data = BarChart(
            title="Chart with empty data",
            data=pd.DataFrame(),
            label_column="labels",
            bar_column="values",
        )
        assert (
            chart_with_empty_data.data.empty
            if isinstance(chart_with_empty_data.data, pd.DataFrame)
            else len(chart_with_empty_data.data) == 0
        )
        assert chart_with_empty_data.title == "Chart with empty data"

        # Test 3: Verify chart can be created and serialized successfully
        chart = BarChart(
            title="Annotation Error Test",
            data=valid_data,
            label_column="labels",
            bar_column="values",
        )

        # Should be able to serialize without issues
        serialized = chart.serialize_model()
        assert serialized["title"] == "Annotation Error Test"
        assert "metadata" in serialized

    @pytest.mark.functional
    @pytest.mark.slow
    def test_performance_workflow(self, large_dataframe):
        """Test performance with large datasets."""
        # Step 1: Create chart with large dataset
        chart = BarChart(
            title="Performance Test Chart",
            data=large_dataframe,
            label_column="category",
            bar_column="value",
            sort_bars=True,
        )

        # Step 2: Add multiple annotations
        for i in range(10):
            chart.text_annotations.append(
                TextAnnotation(text=f"Note {i}", x=i * 10, y=50 + i * 5)
            )

        for i in range(5):
            chart.range_annotations.append(
                RangeAnnotation(x0=i * 20, x1=(i + 1) * 20, y0=0, y1=100)
            )

        # Step 3: Verify chart handles large data
        assert len(chart.data) == len(large_dataframe)
        assert len(chart.text_annotations) == 10
        assert len(chart.range_annotations) == 5

        # Step 4: Test serialization performance
        serialized = chart.serialize_model()
        assert isinstance(serialized, dict)
        assert len(serialized["metadata"]["visualize"]["text-annotations"]) == 10
        assert len(serialized["metadata"]["visualize"]["range-annotations"]) == 5

    @pytest.mark.functional
    def test_json_export_workflow(self, simple_bar_chart):
        """Test JSON export workflow."""
        # Step 1: Add some annotations
        simple_bar_chart.text_annotations.append(
            TextAnnotation(text="Export test", x=1, y=50)
        )

        # Step 2: Serialize to dict
        serialized = simple_bar_chart.serialize_model()

        # Step 3: Convert to JSON
        json_output = json.dumps(serialized, indent=2)

        # Step 4: Verify JSON is valid and contains expected structure
        parsed_json = json.loads(json_output)
        assert isinstance(parsed_json, dict)
        assert "title" in parsed_json
        assert "metadata" in parsed_json
        assert "visualize" in parsed_json["metadata"]

        # Step 5: Verify annotations are in JSON
        visualize = parsed_json["metadata"]["visualize"]
        assert len(visualize["text-annotations"]) == 1
        # Annotations are stored as lists
        text_anno = visualize["text-annotations"][0]
        assert text_anno["text"] == "Export test"

    @pytest.mark.functional
    def test_chart_comparison_workflow(self, sample_dataframe):
        """Test workflow for comparing different chart configurations."""
        # Step 1: Create multiple chart variants
        charts = {
            "basic": BarChart(
                title="Basic Chart",
                data=sample_dataframe,
                label_column="labels",
                bar_column="values",
            ),
            "sorted": BarChart(
                title="Sorted Chart",
                data=sample_dataframe,
                label_column="labels",
                bar_column="values",
                sort_bars=True,
            ),
            "styled": BarChart(
                title="Styled Chart",
                data=sample_dataframe,
                label_column="labels",
                bar_column="values",
                base_color="#FF6B6B",
                background=True,
                thick=True,
            ),
        }

        # Step 2: Verify each chart has different configurations
        assert charts["basic"].sort_bars is False
        assert charts["sorted"].sort_bars is True
        assert charts["styled"].base_color == "#FF6B6B"

        # Step 3: Compare serialized outputs
        serialized_charts = {
            name: chart.serialize_model() for name, chart in charts.items()
        }

        # Step 4: Verify differences in serialized data
        basic_viz = serialized_charts["basic"]["metadata"]["visualize"]
        sorted_viz = serialized_charts["sorted"]["metadata"]["visualize"]
        styled_viz = serialized_charts["styled"]["metadata"]["visualize"]

        assert basic_viz["sort-bars"] is False
        assert sorted_viz["sort-bars"] is True
        assert styled_viz["base-color"] == "#FF6B6B"
        assert styled_viz["background"] is True
        assert styled_viz["thick"] is True
