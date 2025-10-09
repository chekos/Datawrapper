"""Unit tests for BarChart category configuration features."""

import pandas as pd

from datawrapper import BarChart


def test_category_labels_configuration():
    """Test that category_labels are properly included in metadata."""
    data = pd.DataFrame(
        {
            "Country": ["A", "B", "C"],
            "Value": [1, 2, 3],
            "Group": ["Low", "Medium", "High"],
        }
    )

    category_labels = {
        "Low": "Countries with low turnout",
        "Medium": "Countries with medium turnout",
        "High": "Countries with high turnout",
    }

    chart = BarChart(title="Test Chart", data=data, category_labels=category_labels)

    metadata = chart.serialize_model()["metadata"]
    color_category = metadata["visualize"]["color-category"]

    assert "categoryLabels" in color_category
    assert color_category["categoryLabels"] == category_labels


def test_category_order_configuration():
    """Test that category_order is properly included in metadata."""
    data = pd.DataFrame({"Country": ["A", "B", "C"], "Value": [1, 2, 3]})

    category_order = ["C", "B", "A"]

    chart = BarChart(title="Test Chart", data=data, category_order=category_order)

    metadata = chart.serialize_model()["metadata"]
    color_category = metadata["visualize"]["color-category"]

    assert "categoryOrder" in color_category
    assert color_category["categoryOrder"] == category_order


def test_combined_category_configuration():
    """Test that color_category, category_labels, and category_order work together."""
    data = pd.DataFrame(
        {
            "Country": ["Romania", "Belgium", "Malta"],
            "Turnout": [33.2, 88.5, 85.6],
            "Category": ["Low", "High", "High"],
        }
    )

    color_map = {
        "Romania (2020)": "#c71e1d",
        "Belgium (2024)": "#267c87",
        "Malta (2022)": "#267c87",
    }

    category_labels = {
        "Romania (2020)": "European countries with the lowest turnout",
        "Belgium (2024)": "…..with the highest turnout",
        "Malta (2022)": "…..with the highest turnout",
    }

    category_order = ["Romania (2020)", "Belgium (2024)", "Malta (2022)"]

    chart = BarChart(
        title="European Voter Turnout",
        data=data,
        color_category=color_map,
        category_labels=category_labels,
        category_order=category_order,
    )

    metadata = chart.serialize_model()["metadata"]
    color_category = metadata["visualize"]["color-category"]

    # Verify all three components are present
    assert "map" in color_category
    assert color_category["map"] == color_map

    assert "categoryLabels" in color_category
    assert color_category["categoryLabels"] == category_labels

    assert "categoryOrder" in color_category
    assert color_category["categoryOrder"] == category_order


def test_category_labels_with_exclude_from_key():
    """Test that category_labels work alongside excludeFromKey."""
    data = pd.DataFrame({"Country": ["A", "B"], "Value": [1, 2]})

    color_category = {"A": "#ff0000", "B": "#00ff00"}

    category_labels = {"A": "Label A", "B": "Label B"}

    exclude_from_key = ["A"]

    chart = BarChart(
        title="Test",
        data=data,
        color_category=color_category,
        category_labels=category_labels,
        exclude_from_color_key=exclude_from_key,
    )

    metadata = chart.serialize_model()["metadata"]
    result = metadata["visualize"]["color-category"]

    # Verify all properties are present
    assert result["map"] == color_category
    assert result["categoryLabels"] == category_labels
    assert result["excludeFromKey"] == exclude_from_key


def test_empty_category_configuration():
    """Test that empty/default category configs don't break the chart."""
    data = pd.DataFrame({"Country": ["A", "B"], "Value": [1, 2]})

    chart = BarChart(
        title="Test",
        data=data,
        category_labels={},
        category_order=[],
    )

    metadata = chart.serialize_model()["metadata"]
    color_category = metadata["visualize"]["color-category"]

    # Empty dicts/lists should not be included
    assert "categoryLabels" not in color_category
    assert "categoryOrder" not in color_category

    # But the base structure should still exist
    assert "map" in color_category
    assert "excludeFromKey" in color_category


def test_category_configuration_with_none():
    """Test that None values for category configs work correctly."""
    data = pd.DataFrame({"Country": ["A", "B"], "Value": [1, 2]})

    # Default values should be empty dict/list
    chart = BarChart(title="Test", data=data)

    assert chart.category_labels == {}
    assert chart.category_order == []

    metadata = chart.serialize_model()["metadata"]
    color_category = metadata["visualize"]["color-category"]

    # Empty dicts/lists should not be included in serialization
    assert "categoryLabels" not in color_category
    assert "categoryOrder" not in color_category


def test_european_turnout_sample_structure():
    """Test that we can replicate the European turnout sample structure."""
    data = pd.DataFrame(
        {
            "Country": ["Romania (2020)", "Malta (2022)", "Belgium (2024)"],
            "Turnout": [33.2, 85.6, 88.5],
        }
    )

    # Simulate the structure from european-turnout.json
    color_map = {
        "Romania (2020)": "#c71e1d",
        "Bulgaria (2024)": "#c71e1d",
        "Malta (2022)": "#267c87",
        "Belgium (2024)": "#267c87",
    }

    category_labels = {
        "Romania (2020)": "European countries with the lowest turnout in their last national elections",
        "Bulgaria (2024)": "European countries with the lowest turnout in their last national elections",
        "Malta (2022)": "…..with the highest turnout",
        "Belgium (2024)": "…..with the highest turnout",
    }

    category_order = [
        "Romania (2020)",
        "Malta (2022)",
        "Belgium (2024)",
        "Bulgaria (2024)",
    ]

    chart = BarChart(
        title="European countries with lowest & highest voter turnout",
        data=data,
        color_category=color_map,
        category_labels=category_labels,
        category_order=category_order,
        show_color_key=True,
    )

    metadata = chart.serialize_model()["metadata"]
    color_category = metadata["visualize"]["color-category"]

    # Verify structure matches what Datawrapper expects
    assert isinstance(color_category, dict)
    assert "map" in color_category
    assert "categoryLabels" in color_category
    assert "categoryOrder" in color_category
    assert "excludeFromKey" in color_category

    # Verify correct values
    assert len(color_category["map"]) == 4
    assert len(color_category["categoryLabels"]) == 4
    assert len(color_category["categoryOrder"]) == 4
    assert metadata["visualize"]["show-color-key"] is True


def test_category_order_partial_list():
    """Test that category_order can contain a subset of categories."""
    data = pd.DataFrame({"Country": ["A", "B", "C", "D"], "Value": [1, 2, 3, 4]})

    color_map = {
        "A": "#ff0000",
        "B": "#00ff00",
        "C": "#0000ff",
        "D": "#ffff00",
    }

    # Only specify order for some categories
    category_order = ["D", "A"]  # B and C will use default order

    chart = BarChart(
        title="Test",
        data=data,
        color_category=color_map,
        category_order=category_order,
    )

    metadata = chart.serialize_model()["metadata"]
    color_category = metadata["visualize"]["color-category"]

    assert color_category["categoryOrder"] == ["D", "A"]
    assert len(color_category["map"]) == 4


def test_category_labels_do_not_require_all_categories():
    """Test that category_labels can be provided for only some categories."""
    data = pd.DataFrame({"Country": ["A", "B", "C"], "Value": [1, 2, 3]})

    color_map = {"A": "#ff0000", "B": "#00ff00", "C": "#0000ff"}

    # Only provide labels for some categories
    category_labels = {
        "A": "Category A Label",
        "C": "Category C Label",
        # B has no custom label
    }

    chart = BarChart(
        title="Test",
        data=data,
        color_category=color_map,
        category_labels=category_labels,
    )

    metadata = chart.serialize_model()["metadata"]
    color_category = metadata["visualize"]["color-category"]

    assert color_category["categoryLabels"] == category_labels
    assert "B" not in color_category["categoryLabels"]
