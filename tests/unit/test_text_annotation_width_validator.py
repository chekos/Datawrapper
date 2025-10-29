"""Unit tests for TextAnnotation width field validator."""

import pytest
from pydantic import ValidationError

from datawrapper.charts import TextAnnotation


def test_width_valid_default():
    """Test that the default width value (33.3) is valid."""
    anno = TextAnnotation(text="Test", x=0, y=0)
    assert anno.width == 33.3


def test_width_valid_zero():
    """Test that width=0.0 is valid (minimum boundary)."""
    anno = TextAnnotation(text="Test", x=0, y=0, width=0.0)
    assert anno.width == 0.0


def test_width_valid_hundred():
    """Test that width=100.0 is valid (maximum boundary)."""
    anno = TextAnnotation(text="Test", x=0, y=0, width=100.0)
    assert anno.width == 100.0


def test_width_valid_middle():
    """Test that a middle value like 50.0 is valid."""
    anno = TextAnnotation(text="Test", x=0, y=0, width=50.0)
    assert anno.width == 50.0


def test_width_valid_decimal():
    """Test that decimal values are valid."""
    anno = TextAnnotation(text="Test", x=0, y=0, width=25.5)
    assert anno.width == 25.5


def test_width_invalid_negative():
    """Test that negative width values raise ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        TextAnnotation(text="Test", x=0, y=0, width=-1.0)

    error = exc_info.value.errors()[0]
    assert "Invalid width: -1.0" in str(error["ctx"]["error"])
    assert "Must be between 0.0 and 100.0" in str(error["ctx"]["error"])


def test_width_invalid_over_hundred():
    """Test that width values over 100.0 raise ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        TextAnnotation(text="Test", x=0, y=0, width=100.1)

    error = exc_info.value.errors()[0]
    assert "Invalid width: 100.1" in str(error["ctx"]["error"])
    assert "Must be between 0.0 and 100.0" in str(error["ctx"]["error"])


def test_width_invalid_large_value():
    """Test that very large width values raise ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        TextAnnotation(text="Test", x=0, y=0, width=500.0)

    error = exc_info.value.errors()[0]
    assert "Invalid width: 500.0" in str(error["ctx"]["error"])
    assert "Must be between 0.0 and 100.0" in str(error["ctx"]["error"])


def test_width_invalid_very_negative():
    """Test that very negative width values raise ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        TextAnnotation(text="Test", x=0, y=0, width=-50.0)

    error = exc_info.value.errors()[0]
    assert "Invalid width: -50.0" in str(error["ctx"]["error"])
    assert "Must be between 0.0 and 100.0" in str(error["ctx"]["error"])


def test_width_boundary_just_below_zero():
    """Test that width just below 0.0 raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        TextAnnotation(text="Test", x=0, y=0, width=-0.1)

    error = exc_info.value.errors()[0]
    assert "Invalid width: -0.1" in str(error["ctx"]["error"])


def test_width_boundary_just_above_hundred():
    """Test that width just above 100.0 raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        TextAnnotation(text="Test", x=0, y=0, width=100.01)

    error = exc_info.value.errors()[0]
    assert "Invalid width: 100.01" in str(error["ctx"]["error"])
