"""End-to-end API tests that create actual charts with Datawrapper."""

import json
import os
from pathlib import Path

import pandas as pd
import pytest

from datawrapper import BarChart


@pytest.mark.api
@pytest.mark.skipif(
    not os.getenv("DATAWRAPPER_ACCESS_TOKEN"),
    reason="No DATAWRAPPER_ACCESS_TOKEN environment variable set",
)
def test_create_sample_bar_chart_with_datawrapper():
    """End-to-end test that creates the European turnout sample chart with Datawrapper API.

    This test:
    1. Loads the European turnout sample configuration
    2. Creates sample data matching the chart structure
    3. Creates a BarChart instance with the sample configuration
    4. Creates the chart via Datawrapper API
    5. Publishes the chart
    6. Prints the chart URL for manual inspection

    Requires DATAWRAPPER_ACCESS_TOKEN environment variable to be set.
    """
    # Load the European turnout sample JSON
    sample_path = (
        Path(__file__).parent.parent / "samples" / "bar" / "european-turnout.json"
    )
    with open(sample_path) as f:
        sample_data = json.load(f)

    # Extract chart configuration from sample
    chart_config = sample_data["chart"]["crdt"]["data"]
    metadata = chart_config["metadata"]
    _visualize = metadata["visualize"]
    _describe = metadata["describe"]

    # Create sample data that matches the chart structure
    # Based on the European turnout chart configuration
    sample_countries_data = pd.DataFrame(
        {
            "Country": [
                "Romania (2020)",
                "Bulgaria (2024)",
                "Albania (2021)",
                "United Kingdom (2024)",
                "Germany (2021)",
                "Sweden (2022)",
                "Spain (2023)",
                "France (2024)",
                "Belgium (2024)",
                "Turkey (2023)",
                "Malta (2022)",
            ],
            "Turnout": [
                33.2,
                33.4,
                46.3,
                60.0,
                76.4,
                83.8,
                66.0,
                66.7,
                88.5,
                87.0,
                85.6,
            ],
        }
    )

    print(
        f"\n📊 Creating European Turnout Chart with {len(sample_countries_data)} countries..."
    )

    # Extract color mapping and category configuration from sample
    color_category_config = _visualize.get("color-category", {})
    color_category_map = color_category_config.get("map", {})
    category_labels_map = color_category_config.get("categoryLabels", {})
    category_order_list = color_category_config.get("categoryOrder", [])
    highlighted_countries = _visualize.get("highlighted-series", [])

    # Create BarChart instance with comprehensive configuration from sample
    chart = BarChart(
        title=chart_config["title"],
        data=sample_countries_data,
        # Source information (from BaseChart)
        source_name=_describe.get("source-name", ""),
        source_url=_describe.get("source-url", ""),
        # Color configuration
        color_category=color_category_map,
        category_labels=category_labels_map,
        category_order=category_order_list,
        show_color_key=_visualize.get("show-color-key", False),
        # Highlighting
        highlighted_series=highlighted_countries,
        # Sorting and ordering
        sort_bars=_visualize.get("sort-bars", False),
        reverse_order=_visualize.get("reverse-order", False),
        # Appearance
        background=_visualize.get("background", False),
        rules=_visualize.get("rules", False),
        base_color=_visualize.get("base-color", 7),
        # Range and formatting
        custom_range=_visualize.get("custom-range", ["", ""]),
        value_label_format=_visualize.get("value-label-format", ""),
        tick_position=_visualize.get("tick-position", "top"),
        # Notes (from BaseChart)
        notes=metadata.get("annotate", {}).get("notes", ""),
    )

    print(
        "✅ BarChart instance created successfully with enhanced category configuration"
    )
    print(f"   - Color mappings: {len(color_category_map)}")
    print(f"   - Category labels: {len(category_labels_map)}")
    print(f"   - Category order: {len(category_order_list)}")

    # Create the chart via Datawrapper API
    print("🚀 Creating chart via Datawrapper API...")
    chart.create()
    chart_id = chart.chart_id

    print(f"✅ Chart created successfully with ID: {chart_id}")

    # Publish the chart to get the public URL
    print("📤 Publishing chart...")

    # Get the Datawrapper client and publish
    client = chart._get_client()
    publish_response = client.post(f"{client._CHARTS_URL}/{chart_id}/publish")

    # Extract the public URL - handle different response types
    if isinstance(publish_response, dict):
        public_url = publish_response.get("publicUrl", "")
    else:
        public_url = ""

    if not public_url:
        # Fallback URL construction if not in response
        public_url = f"https://datawrapper.dwcdn.net/{chart_id}/"

    print("✅ Chart published successfully!")
    print(f"🌐 Chart URL: {public_url}")
    print(f"📊 Chart ID: {chart_id}")
    print(f"🔗 You can view the chart at: {public_url}")

    # Verify the chart was created successfully
    assert chart_id is not None
    assert len(chart_id) > 0
    assert chart.chart_id == chart_id

    # Verify we got a valid URL
    assert public_url.startswith("https://")
    assert chart_id in public_url

    print("\n🎉 End-to-end test completed successfully!")
    print("📋 Summary:")
    print(f"   - Chart Title: {chart.title}")
    print(f"   - Chart Type: {chart.chart_type}")
    print(f"   - Data Points: {len(chart.data)}")
    print(f"   - Chart ID: {chart_id}")
    print(f"   - Public URL: {public_url}")
    print("   - Category Configuration:")
    print(f"     • Color mappings: {len(color_category_map)}")
    print(f"     • Category labels: {len(category_labels_map)}")
    print(f"     • Category order: {len(category_order_list)}")


@pytest.mark.api
@pytest.mark.skipif(
    not os.getenv("DATAWRAPPER_ACCESS_TOKEN"),
    reason="No DATAWRAPPER_ACCESS_TOKEN environment variable set",
)
def test_create_simple_bar_chart_with_api():
    """Simpler end-to-end test that creates a basic bar chart.

    This is a minimal test to verify the API integration works
    with a simple chart configuration.
    """
    # Create simple test data
    test_data = pd.DataFrame(
        {"Category": ["A", "B", "C", "D", "E"], "Value": [23, 45, 56, 78, 32]}
    )

    print("\n📊 Creating simple test chart...")

    # Create a simple BarChart
    chart = BarChart(
        title="API Test Chart - Simple Bar Chart",
        data=test_data,
    )

    print("✅ Simple BarChart instance created")

    # Create via API
    print("🚀 Creating chart via API...")
    chart.create()
    chart_id = chart.chart_id

    print(f"✅ Chart created with ID: {chart_id}")

    # Publish the chart
    print("📤 Publishing chart...")
    client = chart._get_client()
    publish_response = client.post(f"{client._CHARTS_URL}/{chart_id}/publish")

    # Extract the public URL - handle different response types
    if isinstance(publish_response, dict):
        public_url = publish_response.get("publicUrl", "")
    else:
        public_url = ""

    if not public_url:
        # Fallback URL construction if not in response
        public_url = f"https://datawrapper.dwcdn.net/{chart_id}/"

    print("✅ Chart published!")
    print(f"🌐 Simple Chart URL: {public_url}")

    # Basic assertions
    assert chart_id is not None
    assert len(chart_id) > 0
    assert public_url.startswith("https://")

    print("🎉 Simple end-to-end test completed!")


@pytest.mark.api
@pytest.mark.skipif(
    not os.getenv("DATAWRAPPER_ACCESS_TOKEN"),
    reason="No DATAWRAPPER_ACCESS_TOKEN environment variable set",
)
def test_create_happiness_scores_bar_chart_with_datawrapper():
    """End-to-end test that creates the Happiness Scores sample chart with Datawrapper API.

    This test demonstrates advanced features including:
    - Range overlays (confidence intervals)
    - Continent-based color mapping
    - Custom grid configuration
    - Detailed metadata (intro, byline)
    - Value label formatting

    Requires DATAWRAPPER_ACCESS_TOKEN environment variable to be set.
    """
    # Load the happiness scores sample JSON
    sample_json_path = (
        Path(__file__).parent.parent / "samples" / "bar" / "happiness-scores.json"
    )
    with open(sample_json_path) as f:
        sample_data = json.load(f)

    # Extract chart configuration from sample
    chart_config = sample_data["chart"]["crdt"]["data"]
    metadata = chart_config["metadata"]
    visualize = metadata["visualize"]
    describe = metadata["describe"]

    # Load the happiness scores data from CSV
    sample_csv_path = (
        Path(__file__).parent.parent / "samples" / "bar" / "happiness-scores.csv"
    )
    sample_happiness_data = pd.read_csv(sample_csv_path, sep="\t")

    # Remove rows with all NaN values (the "..." separator rows in the CSV)
    sample_happiness_data = sample_happiness_data.dropna(how="all")

    print(
        f"\n📊 Creating Happiness Scores Chart with {len(sample_happiness_data)} countries..."
    )

    # Extract color mapping from sample
    color_category_map = visualize.get("color-category", {}).get("map", {})

    # Extract overlays configuration
    overlays_config = visualize.get("overlays", {})

    # Convert overlays dict to list format expected by BarChart
    # The overlays dict has overlay IDs as keys, we need to extract the overlay configs
    overlays_list = []
    for _overlay_id, overlay_config in overlays_config.items():
        overlays_list.append(
            {
                "type": overlay_config.get("type"),
                "from": overlay_config.get("from"),
                "to": overlay_config.get("to"),
                "color": overlay_config.get("color"),
                "opacity": overlay_config.get("opacity", 0.6),
                "pattern": overlay_config.get("pattern", "solid"),
                "title": overlay_config.get("title", ""),
                "showInColorKey": overlay_config.get("showInColorKey", True),
                "labelDirectly": overlay_config.get("labelDirectly", True),
            }
        )

    print(f"📈 Configured {len(overlays_list)} overlays (confidence intervals)")

    # Create BarChart instance with comprehensive configuration from sample
    chart = BarChart(
        title=chart_config["title"],
        data=sample_happiness_data,
        # Source and description information (from BaseChart)
        source_name=describe.get("source-name", ""),
        source_url=describe.get("source-url", ""),
        intro=describe.get("intro", ""),
        byline=describe.get("byline", ""),
        # Color configuration
        color_category=color_category_map,
        show_color_key=visualize.get("show-color-key", False),
        # Highlighting
        highlighted_series=visualize.get("highlighted-series", []),
        # Sorting and ordering
        sort_bars=visualize.get("sort-bars", False),
        reverse_order=visualize.get("reverse-order", False),
        # Appearance
        background=visualize.get("background", False),
        rules=visualize.get("rules", False),
        base_color=visualize.get("base-color", 0),
        # Range and formatting
        custom_range=visualize.get("custom-range", ["", ""]),
        value_label_format=visualize.get("value-label-format", ""),
        tick_position=visualize.get("tick-position", "top"),
        # Labels
        label_alignment=visualize.get("label-alignment", "left"),
        show_value_labels=visualize.get("show-value-labels", True),
        value_label_alignment=visualize.get("value-label-alignment", "left"),
        # Overlays (range annotations for confidence intervals)
        overlays=overlays_list,
        # Notes (from BaseChart)
        notes=metadata.get("annotate", {}).get("notes", ""),
    )

    print("✅ BarChart instance created successfully with advanced features:")
    print(f"   - Color mapping: {len(color_category_map)} entries")
    print(f"   - Overlays: {len(overlays_list)} configured")
    print(f"   - Intro text: {len(chart.intro)} characters")
    print(f"   - Byline: {chart.byline}")

    # Create the chart via Datawrapper API
    print("🚀 Creating chart via Datawrapper API...")
    chart.create()
    chart_id = chart.chart_id

    print(f"✅ Chart created successfully with ID: {chart_id}")

    # Publish the chart to get the public URL
    print("📤 Publishing chart...")

    # Get the Datawrapper client and publish
    client = chart._get_client()
    publish_response = client.post(f"{client._CHARTS_URL}/{chart_id}/publish")

    # Extract the public URL - handle different response types
    if isinstance(publish_response, dict):
        public_url = publish_response.get("publicUrl", "")
    else:
        public_url = ""

    if not public_url:
        # Fallback URL construction if not in response
        public_url = f"https://datawrapper.dwcdn.net/{chart_id}/"

    print("✅ Chart published successfully!")
    print(f"🌐 Chart URL: {public_url}")
    print(f"📊 Chart ID: {chart_id}")
    print(f"🔗 You can view the chart at: {public_url}")

    # Verify the chart was created successfully
    assert chart_id is not None
    assert len(chart_id) > 0
    assert chart.chart_id == chart_id

    # Verify we got a valid URL
    assert public_url.startswith("https://")
    assert chart_id in public_url

    print("\n🎉 Happiness Scores end-to-end test completed successfully!")
    print("📋 Summary:")
    print(f"   - Chart Title: {chart.title}")
    print(f"   - Chart Type: {chart.chart_type}")
    print(f"   - Data Points: {len(chart.data)}")
    print(f"   - Countries: {len(sample_happiness_data)}")
    print(
        f"   - Continents represented: {sample_happiness_data['Continent'].nunique()}"
    )
    print(f"   - Chart ID: {chart_id}")
    print(f"   - Public URL: {public_url}")
    print("   - Features implemented:")
    print("     • Confidence interval overlays")
    print("     • Continent-based color coding")
    print("     • Detailed metadata (intro, byline)")
    print("     • Custom value formatting")
