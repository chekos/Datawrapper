import datawrapper
from tests.utils import _test_class


def test_range_annotation():
    _test_class(datawrapper.RangeAnnotation)


def test_text_annotation():
    _test_class(datawrapper.TextAnnotation)
