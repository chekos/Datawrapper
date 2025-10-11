"""Test River functions."""

import pytest

from datawrapper import Datawrapper


@pytest.mark.api
def test_get_river():
    """Test the get_river function."""
    # Create a client
    dw = Datawrapper()

    # Get the river
    river = dw.get_river()["list"]

    # Verify that the river is a list
    assert isinstance(river, list)
    assert len(river) > 0
    assert isinstance(river[0], dict)
    assert "id" in river[0]
    assert "title" in river[0]

    # Test the get_river_chart function too
    chart = dw.get_river_chart(river[0]["id"])
    assert isinstance(chart, dict)
    assert "id" in chart

    # Test some different parameters
    dw.get_river(approved=True)
    dw.get_river(approved=True, search="test")

    # Get a chart we own
    chart = dw.get_charts()["list"][0]

    # Update a river chart
    chart_id = chart["id"]
    update = dw.update_river_chart(
        chart_id,
        description="Test description",
        byline="Test byline",
        tags=["test"],
        forkable=True,
    )
    assert update is True

    # Verify that the river chart was updated
    chart = dw.get_river_chart(chart_id)
    assert chart["description"] == "Test description"
