"""Test oembed functions."""

import pytest

from datawrapper import Datawrapper


@pytest.mark.api
def test_get_chart_display_urls():
    """Test get_oembed function."""
    dw = Datawrapper()

    # Get display urls for a chart
    data = dw.get_chart_display_urls("WpAbK")

    # Verify it contains a list of dictionarys
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
