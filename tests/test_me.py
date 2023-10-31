"""Test methods that use the /me endpoint."""
from datawrapper import Datawrapper


def test_get_my_account():
    """Test the get_my_account method."""
    dw = Datawrapper()
    assert isinstance(dw.get_my_account(), dict)


def test_update_my_account():
    """Test update_my_account."""
    dw = Datawrapper()
    dw.update_my_account(name="Foobar")
    dw.update_my_account(name="Test user")


def test_get_my_recently_edited_charts():
    """Test my_recently_edited_charts."""
    dw = Datawrapper()

    one = dw.get_my_recently_edited_charts()
    assert isinstance(one, dict)
    assert isinstance(one["list"], list)

    two = dw.get_my_recently_edited_charts(limit=1)
    assert isinstance(two["list"], list)

    three = dw.get_my_recently_edited_charts(limit=1, offset=2)
    assert isinstance(three["list"], list)

    four = dw.get_my_recently_edited_charts(min_last_edit_step=3)
    assert isinstance(four["list"], list)


def test_get_my_recently_published_charts():
    """Test my_recently_published_charts."""
    dw = Datawrapper()

    one = dw.get_my_recently_published_charts()
    assert isinstance(one, dict)
    assert isinstance(one["list"], list)

    two = dw.get_my_recently_published_charts(limit=1)
    assert isinstance(two["list"], list)

    three = dw.get_my_recently_published_charts(limit=1, offset=2)
    assert isinstance(three["list"], list)
