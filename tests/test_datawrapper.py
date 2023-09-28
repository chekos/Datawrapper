"""Unit test package for datawrapper."""
from datawrapper import Datawrapper
import pandas as pd


def test_get_charts():
    """Test the get_charts method."""
    dw = Datawrapper()
    dw.get_charts()


def test_get_folders():
    """Test the get_folders method."""
    dw = Datawrapper()
    dw.get_folders()


def test_usage():
    """Test creating and updating charts with the same code as our example notebook."""
    # Connect
    dw = Datawrapper()

    # Get account info
    dw.account_info()

    # Pull data
    df = pd.read_csv(
        "https://raw.githubusercontent.com/chekos/datasets/master/data/datawrapper_example.csv",
        sep=";",
    )

    # Create a chart
    chart_info = dw.create_chart(
        title="Where do people live?",
        chart_type="d3-bars-stacked",
        data=df
    )

    # Add a description
    dw.update_description(
        chart_info["id"],
        source_name="UN Population Division",
        source_url="https://population.un.org/wup/",
        byline="datawrapper at pypi",
    )

    # Pub it
    dw.publish_chart(chart_id=chart_info["id"], display=False)

    # Change it
    properties = {
        "visualize": {
            "thick": True,
            "custom-colors": {
                "in rural areas": "#dadada",
                "in other urban areas": "#1d81a2",
                "Share of population that lives in the capital": "#15607a",
            },
        }
    }
    dw.update_metadata(chart_info["id"], properties)

    # Export it
    dw.export_chart(
        chart_info["id"],
        output="png",
        filepath="chart.png",
        display=False
    )
    dw.get_iframe_code()

    # Pull metadata
    dw.chart_properties(chart_info["id"])
    dw.chart_data(chart_info["id"])

    # Nuke it
    dw.delete_chart(chart_info["id"])