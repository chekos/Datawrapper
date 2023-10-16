"""Test themes related API enpoints."""
from datawrapper import Datawrapper


def test_get_themes():
    """Test the get_themes method."""
    dw = Datawrapper()

    one = dw.get_themes()
    assert len(one["list"]) > 0

    two = dw.get_themes(offset=2, limit=1)
    assert one["list"][0] != two["list"][0]
