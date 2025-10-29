"""Unit tests for TextAlign enum."""

import pytest
from pydantic import ValidationError

from datawrapper import TextAlign
from datawrapper.charts import TextAnnotation


def test_text_align_enum_values():
    """Test that TextAlign enum has all expected values."""
    assert TextAlign.TOP_LEFT == "tl"
    assert TextAlign.TOP_CENTER == "tc"
    assert TextAlign.TOP_RIGHT == "tr"
    assert TextAlign.MIDDLE_LEFT == "ml"
    assert TextAlign.MIDDLE_CENTER == "mc"
    assert TextAlign.MIDDLE_RIGHT == "mr"
    assert TextAlign.BOTTOM_LEFT == "bl"
    assert TextAlign.BOTTOM_CENTER == "bc"
    assert TextAlign.BOTTOM_RIGHT == "br"


def test_text_align_enum_count():
    """Test that TextAlign enum has exactly 9 values."""
    assert len(TextAlign) == 9


def test_text_annotation_with_enum():
    """Test TextAnnotation accepts TextAlign enum values."""
    anno = TextAnnotation(text="Test annotation", x=10, y=20, align=TextAlign.TOP_LEFT)
    assert anno.align == TextAlign.TOP_LEFT


def test_text_annotation_with_string():
    """Test TextAnnotation accepts valid string values for backwards compatibility."""
    anno = TextAnnotation(text="Test annotation", x=10, y=20, align="tc")
    assert anno.align == "tc"


def test_text_annotation_invalid_string():
    """Test TextAnnotation rejects invalid string values."""
    with pytest.raises(ValidationError) as exc_info:
        TextAnnotation(text="Test annotation", x=10, y=20, align="invalid")
    assert "Invalid text alignment" in str(exc_info.value)


def test_text_annotation_all_enum_values():
    """Test TextAnnotation accepts all TextAlign enum values."""
    for align_value in TextAlign:
        anno = TextAnnotation(text="Test", x=0, y=0, align=align_value)
        assert anno.align == align_value


def test_text_annotation_all_string_values():
    """Test TextAnnotation accepts all valid string values."""
    valid_strings = ["tl", "tc", "tr", "ml", "mc", "mr", "bl", "bc", "br"]
    for align_str in valid_strings:
        anno = TextAnnotation(text="Test", x=0, y=0, align=align_str)
        assert anno.align == align_str


def test_text_align_import_from_top_level():
    """Test that TextAlign can be imported from top-level datawrapper package."""
    from datawrapper import TextAlign as TopLevelTextAlign

    assert TopLevelTextAlign.TOP_LEFT == "tl"


def test_text_align_import_from_charts():
    """Test that TextAlign can be imported from datawrapper.charts."""
    from datawrapper.charts import TextAlign as ChartsTextAlign

    assert ChartsTextAlign.TOP_LEFT == "tl"


def test_text_align_import_from_enums():
    """Test that TextAlign can be imported from datawrapper.charts.enums."""
    from datawrapper.charts.enums import TextAlign as EnumsTextAlign

    assert EnumsTextAlign.TOP_LEFT == "tl"
