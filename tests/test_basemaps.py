"""Test basemaps related API enpoints."""
from datawrapper import Datawrapper


def test_get_basemaps():
    """Test the get_basemaps method."""
    dw = Datawrapper()
    basemaps_list = dw.get_basemaps()
    assert len(basemaps_list) > 0