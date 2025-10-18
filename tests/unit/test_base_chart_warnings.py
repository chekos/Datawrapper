"""Unit tests for BaseChart unrecognized field warnings."""

import warnings

import pandas as pd
import pytest

from datawrapper.charts.base import BaseChart


class TestBaseChartUnrecognizedFieldWarnings:
    """Test that BaseChart warns about unrecognized fields."""

    def test_valid_field_no_warning(self):
        """Valid field names should not trigger warnings."""
        with warnings.catch_warnings():
            warnings.simplefilter("error")  # Turn warnings into errors
            # Should not raise any warnings
            chart = BaseChart(
                chart_type="d3-lines",
                title="Test Chart",
                source_name="Test Source",
            )
            assert chart.title == "Test Chart"
            assert chart.source_name == "Test Source"

    def test_valid_alias_no_warning(self):
        """Valid field aliases should not trigger warnings."""
        with warnings.catch_warnings():
            warnings.simplefilter("error")  # Turn warnings into errors
            # Should not raise any warnings when using aliases
            chart = BaseChart(
                **{
                    "chart-type": "d3-lines",
                    "source-name": "Test Source",
                    "aria-description": "Test description",
                }
            )
            assert chart.source_name == "Test Source"
            assert chart.aria_description == "Test description"

    def test_invalid_field_triggers_warning(self):
        """Invalid field names should trigger a UserWarning."""
        with pytest.warns(UserWarning, match="unrecognized field"):
            chart = BaseChart(
                chart_type="d3-lines",
                title="Test Chart",
                invalid_field="This should warn",
            )
            # Chart should still be created
            assert chart.title == "Test Chart"

    def test_multiple_invalid_fields_warning(self):
        """Multiple invalid fields should all be mentioned in the warning."""
        with pytest.warns(UserWarning) as warning_list:
            chart = BaseChart(
                chart_type="d3-lines",
                title="Test Chart",
                invalid_field1="Value 1",
                invalid_field2="Value 2",
                another_typo="Value 3",
            )
            assert chart.title == "Test Chart"

        # Check that all invalid fields are mentioned in the warning
        warning_message = str(warning_list[0].message)
        assert "invalid_field1" in warning_message
        assert "invalid_field2" in warning_message
        assert "another_typo" in warning_message

    def test_typo_in_field_name_warning(self):
        """Common typos should trigger warnings."""
        with pytest.warns(UserWarning, match="titel"):
            chart = BaseChart(
                chart_type="d3-lines",
                titel="Test Chart",  # Typo: should be 'title'
            )
            # Chart should still be created with default title
            assert chart.title == ""

    def test_private_attributes_no_warning(self):
        """Private attributes (starting with _) should not trigger warnings."""
        with warnings.catch_warnings():
            warnings.simplefilter("error")  # Turn warnings into errors
            # Should not raise any warnings for private attributes
            chart = BaseChart(
                chart_type="d3-lines",
                title="Test Chart",
                _private_attr="This is private",
            )
            assert chart.title == "Test Chart"

    def test_warning_message_format(self):
        """Warning message should be clear and helpful."""
        with pytest.warns(UserWarning) as warning_list:
            BaseChart(
                chart_type="d3-lines",
                invalid_field="Value",
            )

        warning_message = str(warning_list[0].message)
        # Check that the warning message contains helpful information
        assert "BaseChart" in warning_message
        assert "unrecognized field" in warning_message
        assert "invalid_field" in warning_message
        assert "ignored" in warning_message
        assert "documentation" in warning_message or "typos" in warning_message

    def test_mixed_valid_and_invalid_fields(self):
        """Mix of valid and invalid fields should only warn about invalid ones."""
        with pytest.warns(UserWarning) as warning_list:
            chart = BaseChart(
                chart_type="d3-lines",
                title="Test Chart",  # Valid
                source_name="Test Source",  # Valid
                invalid_field="Value",  # Invalid
            )
            assert chart.title == "Test Chart"
            assert chart.source_name == "Test Source"

        warning_message = str(warning_list[0].message)
        assert "invalid_field" in warning_message
        # Valid fields should not be mentioned
        assert "title" not in warning_message
        assert "source_name" not in warning_message

    def test_data_field_no_warning(self):
        """The data field should not trigger warnings."""
        with warnings.catch_warnings():
            warnings.simplefilter("error")  # Turn warnings into errors
            df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
            chart = BaseChart(
                chart_type="d3-lines",
                title="Test Chart",
                data=df,
            )
            assert isinstance(chart.data, pd.DataFrame)
            assert not chart.data.empty

    def test_transformations_field_no_warning(self):
        """The transformations field should not trigger warnings."""
        with warnings.catch_warnings():
            warnings.simplefilter("error")  # Turn warnings into errors
            chart = BaseChart(
                chart_type="d3-lines",
                title="Test Chart",
                transformations={"transpose": False},
            )
            assert chart.title == "Test Chart"

    def test_warning_sorted_field_names(self):
        """Warning should list field names in sorted order for consistency."""
        with pytest.warns(UserWarning) as warning_list:
            BaseChart(
                chart_type="d3-lines",
                zebra_field="Z",
                apple_field="A",
                middle_field="M",
            )

        warning_message = str(warning_list[0].message)
        # Check that fields appear in sorted order
        apple_pos = warning_message.find("apple_field")
        middle_pos = warning_message.find("middle_field")
        zebra_pos = warning_message.find("zebra_field")
        assert apple_pos < middle_pos < zebra_pos

    def test_chart_id_excluded_field_no_warning(self):
        """The chart_id field (marked as exclude=True) should not trigger warnings."""
        with warnings.catch_warnings():
            warnings.simplefilter("error")  # Turn warnings into errors
            chart = BaseChart(
                chart_type="d3-lines",
                title="Test Chart",
                chart_id="test123",
            )
            assert chart.chart_id == "test123"
