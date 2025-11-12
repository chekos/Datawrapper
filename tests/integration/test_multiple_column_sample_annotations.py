"""
Integration tests for MultipleColumnChart annotation deserialization from sample files.

These tests ensure that text and range annotations in the sample files are properly
deserialized with all their fields, including position coordinates and plot-specific fields.
"""

import json
from pathlib import Path

import pytest

from datawrapper.charts import MultipleColumnChart


class TestMultipleColumnPopulationSampleAnnotations:
    """Test annotation deserialization from the population.json sample file."""

    @pytest.fixture
    def population_sample(self):
        """Load the population.json sample file."""
        sample_path = (
            Path(__file__).parent.parent
            / "samples"
            / "multiple_column"
            / "population.json"
        )
        with open(sample_path) as f:
            data = json.load(f)
            return data["chart"]["crdt"]["data"]

    def test_deserializes_text_annotations_with_coordinates(self, population_sample):
        """Text annotations should have x, y coordinates extracted from position object."""
        chart = MultipleColumnChart(
            **MultipleColumnChart.deserialize_model(population_sample)
        )

        # Should have 5 text annotations
        assert len(chart.text_annotations) == 5

        # Check first annotation has coordinates
        first_anno = chart.text_annotations[0]
        assert first_anno.id == "qlTwCClb1c"
        assert first_anno.text == "Projection"
        assert first_anno.x == "2018/04/30 15:23"
        assert first_anno.y == "36224085.8571"
        assert first_anno.plot == "Mumbai (Bombay)"
        assert first_anno.show_in_all_plots is False

    def test_deserializes_range_annotations_with_coordinates(self, population_sample):
        """Range annotations should have x0, x1, y0, y1 coordinates extracted from position object."""
        chart = MultipleColumnChart(
            **MultipleColumnChart.deserialize_model(population_sample)
        )

        # Should have 2 range annotations
        assert len(chart.range_annotations) == 2

        # Check first range annotation (y-axis line)
        first_range = chart.range_annotations[0]
        assert first_range.id == "gYi6VGb7lA"
        assert first_range.type == "y"
        assert first_range.x0 == "2009/01/23 14:50"
        assert first_range.x1 == "2009/01/23 14:50"
        assert first_range.y0 == "11765087.7143"
        assert first_range.y1 == "13622733.1429"
        assert first_range.plot == "Paris"
        assert first_range.show_in_all_plots is True

        # Check second range annotation (x-axis range)
        second_range = chart.range_annotations[1]
        assert second_range.id == "abr7XsuQVb"
        assert second_range.type == "x"
        assert second_range.x0 == "2018/01/01 13:22"
        assert second_range.x1 == "2037/07/02 01:00"
        assert second_range.y0 == "26626251.1429"
        assert second_range.y1 == "27245466.2857"
        assert second_range.plot == "Mumbai (Bombay)"
        assert second_range.show_in_all_plots is True

    def test_text_annotation_roundtrip_preserves_coordinates(self, population_sample):
        """Text annotations should maintain coordinates through serialize/deserialize cycle.

        Note: IDs are not preserved because they are server-generated and only exist
        when fetching from the API. Local serialization produces list format without IDs.
        """
        chart = MultipleColumnChart(
            **MultipleColumnChart.deserialize_model(population_sample)
        )

        # Serialize and deserialize
        serialized = chart.serialize_model()
        chart2 = MultipleColumnChart(
            **MultipleColumnChart.deserialize_model(serialized)
        )

        # Compare first text annotation (excluding ID which is not preserved)
        assert len(chart2.text_annotations) == len(chart.text_annotations)
        original = chart.text_annotations[0]
        roundtrip = chart2.text_annotations[0]

        # IDs are not preserved through local serialization (server-generated)
        assert roundtrip.x == original.x
        assert roundtrip.y == original.y
        assert roundtrip.plot == original.plot
        assert roundtrip.show_in_all_plots == original.show_in_all_plots
        assert roundtrip.text == original.text

    def test_range_annotation_roundtrip_preserves_coordinates(self, population_sample):
        """Range annotations should maintain coordinates through serialize/deserialize cycle.

        Note: IDs are not preserved because they are server-generated and only exist
        when fetching from the API. Local serialization produces list format without IDs.
        """
        chart = MultipleColumnChart(
            **MultipleColumnChart.deserialize_model(population_sample)
        )

        # Serialize and deserialize
        serialized = chart.serialize_model()
        chart2 = MultipleColumnChart(
            **MultipleColumnChart.deserialize_model(serialized)
        )

        # Compare first range annotation (excluding ID which is not preserved)
        assert len(chart2.range_annotations) == len(chart.range_annotations)
        original = chart.range_annotations[0]
        roundtrip = chart2.range_annotations[0]

        # IDs are not preserved through local serialization (server-generated)
        assert roundtrip.x0 == original.x0
        assert roundtrip.x1 == original.x1
        assert roundtrip.y0 == original.y0
        assert roundtrip.y1 == original.y1
        assert roundtrip.plot == original.plot
        assert roundtrip.show_in_all_plots == original.show_in_all_plots
        assert roundtrip.type == original.type

    def test_all_text_annotations_have_required_fields(self, population_sample):
        """All text annotations should have text, x, y fields after deserialization."""
        chart = MultipleColumnChart(
            **MultipleColumnChart.deserialize_model(population_sample)
        )

        for anno in chart.text_annotations:
            assert anno.text is not None, f"Annotation {anno.id} missing text"
            assert anno.x is not None, f"Annotation {anno.id} missing x coordinate"
            assert anno.y is not None, f"Annotation {anno.id} missing y coordinate"

    def test_all_range_annotations_have_required_fields(self, population_sample):
        """All range annotations should have x0, x1, y0, y1 fields after deserialization."""
        chart = MultipleColumnChart(
            **MultipleColumnChart.deserialize_model(population_sample)
        )

        for anno in chart.range_annotations:
            assert anno.x0 is not None, (
                f"Range annotation {anno.id} missing x0 coordinate"
            )
            assert anno.x1 is not None, (
                f"Range annotation {anno.id} missing x1 coordinate"
            )
            assert anno.y0 is not None, (
                f"Range annotation {anno.id} missing y0 coordinate"
            )
            assert anno.y1 is not None, (
                f"Range annotation {anno.id} missing y1 coordinate"
            )


class TestMultipleColumnUKSpendingSampleAnnotations:
    """Test annotation deserialization from the uk-spending.json sample file."""

    @pytest.fixture
    def uk_spending_sample(self):
        """Load the uk-spending.json sample file."""
        sample_path = (
            Path(__file__).parent.parent
            / "samples"
            / "multiple_column"
            / "uk-spending.json"
        )
        with open(sample_path) as f:
            data = json.load(f)
            return data["chart"]["crdt"]["data"]

    def test_deserializes_text_annotations_with_plot_field(self, uk_spending_sample):
        """Text annotations should have plot field and coordinates."""
        chart = MultipleColumnChart(
            **MultipleColumnChart.deserialize_model(uk_spending_sample)
        )

        # Should have 3 text annotations
        assert len(chart.text_annotations) == 3

        # Check all have plot field and coordinates
        for anno in chart.text_annotations:
            assert anno.plot is not None, f"Annotation {anno.id} missing plot field"
            assert anno.x is not None, f"Annotation {anno.id} missing x coordinate"
            assert anno.y is not None, f"Annotation {anno.id} missing y coordinate"
            assert (
                anno.show_in_all_plots is False
            )  # Default for plot-specific annotations

    def test_text_annotations_have_correct_plot_assignments(self, uk_spending_sample):
        """Text annotations should be assigned to correct plots."""
        chart = MultipleColumnChart(
            **MultipleColumnChart.deserialize_model(uk_spending_sample)
        )

        # Map annotations by ID to expected plot
        expected_plots = {
            "OuxekId1tS": "Health",
            "mQ3_Dnpncq": "Defence",
            "Xq4FVQBE-J": "Education",
        }

        for anno in chart.text_annotations:
            assert anno.plot == expected_plots[anno.id], (
                f"Annotation {anno.id} has wrong plot: {anno.plot} != {expected_plots[anno.id]}"
            )


class TestMultipleColumnEmptyAnnotationSamples:
    """Test that samples with empty annotations deserialize correctly."""

    @pytest.fixture
    def jobs_sample(self):
        """Load the jobs.json sample file."""
        sample_path = (
            Path(__file__).parent.parent / "samples" / "multiple_column" / "jobs.json"
        )
        with open(sample_path) as f:
            data = json.load(f)
            return data["chart"]["crdt"]["data"]

    @pytest.fixture
    def social_media_sample(self):
        """Load the social-media.json sample file."""
        sample_path = (
            Path(__file__).parent.parent
            / "samples"
            / "multiple_column"
            / "social-media.json"
        )
        with open(sample_path) as f:
            data = json.load(f)
            return data["chart"]["crdt"]["data"]

    def test_jobs_sample_has_empty_annotations(self, jobs_sample):
        """Jobs sample should deserialize with empty annotation lists."""
        chart = MultipleColumnChart(
            **MultipleColumnChart.deserialize_model(jobs_sample)
        )
        assert chart.text_annotations == []
        assert chart.range_annotations == []

    def test_social_media_sample_has_empty_annotations(self, social_media_sample):
        """Social media sample should deserialize with empty annotation lists."""
        chart = MultipleColumnChart(
            **MultipleColumnChart.deserialize_model(social_media_sample)
        )
        assert chart.text_annotations == []
        assert chart.range_annotations == []
