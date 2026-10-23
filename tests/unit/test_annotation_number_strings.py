"""Annotation numbers that Datawrapper stores as strings or floats."""

import pytest
from pydantic import ValidationError

from datawrapper import RangeAnnotation, TextAnnotation


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("3", 3), ("-12", -12), ("-29.5", -29.5), (-29.5, -29.5), (7, 7)],
)
def test_text_annotation_offsets_accept_api_values(raw, expected):
    annotation = TextAnnotation.model_validate(
        {"x": 0, "y": 0, "text": "Label", "dx": raw, "dy": raw}
    )

    assert annotation.dx == expected
    assert annotation.dy == expected
    assert annotation.serialize_model()["dy"] == expected


def test_text_annotation_offsets_keep_integers_as_integers():
    annotation = TextAnnotation.model_validate(
        {"x": 0, "y": 0, "text": "Label", "dx": "3"}
    )

    assert isinstance(annotation.dx, int)


def test_text_annotation_offsets_reject_non_numbers():
    with pytest.raises(ValidationError):
        TextAnnotation.model_validate({"x": 0, "y": 0, "text": "Label", "dx": "left"})


@pytest.mark.parametrize(("raw", "expected"), [("10", 10), ("64", 64), (50, 50)])
def test_range_annotation_opacity_accepts_numeric_strings(raw, expected):
    annotation = RangeAnnotation.model_validate(
        {"type": "x", "x0": 0, "x1": 1, "opacity": raw}
    )

    assert annotation.opacity == expected
    assert annotation.serialize_model()["opacity"] == expected


@pytest.mark.parametrize("raw", ["150", "-1", "opaque"])
def test_range_annotation_opacity_still_validates(raw):
    with pytest.raises(ValidationError):
        RangeAnnotation.model_validate({"type": "x", "x0": 0, "x1": 1, "opacity": raw})
