"""Test basemaps related API enpoints."""
from datawrapper import Datawrapper


def test_get_basemaps():
    """Test the get_basemaps method."""
    dw = Datawrapper()
    basemaps_list = dw.get_basemaps()
    assert len(basemaps_list) > 0


def test_get_basemap():
    """Test the get_basemap method."""
    dw = Datawrapper()

    # Test the standard query
    basemap_info = dw.get_basemap("iowa-counties")
    assert isinstance(basemap_info, dict)
    assert basemap_info["meta"]["slug"] == "usa-iowa-counties"
    assert basemap_info["meta"]["projection"] == {
        "rotate": [93.49589653689938, -42.075128883839746],
        "type": "geoAzimuthalEqualArea",
    }

    # Test the projection kwarg
    basemap_info = dw.get_basemap("iowa-counties", wgs84=True)
    assert basemap_info["meta"]["projection"] == {"type": "geoAzimuthalEqualArea"}


def test_get_basemap_key():
    """Test the get_basemap_key method."""
    dw = Datawrapper()

    # Test the standard query
    basemap_key = dw.get_basemap_key("iowa-counties", "GEOID")
    assert isinstance(basemap_key, dict)
    assert basemap_key["label"] == "FIPS"
    assert len(basemap_key["values"]) == 99
