"""Unit tests for AreaFill opacity field validator."""

import pytest
from pydantic import ValidationError

from datawrapper.charts.line import AreaFill


def test_opacity_valid_default():
    """Test that the default opacity value (0.3) is valid."""
    fill = AreaFill(**{"from": "baseline", "to": "new"})
    assert fill.opacity == 0.3


def test_opacity_valid_zero():
    """Test that opacity=0.0 is valid (minimum boundary)."""
    fill = AreaFill(**{"from": "baseline", "to": "new", "opacity": 0.0})
    assert fill.opacity == 0.0


def test_opacity_valid_one():
    """Test that opacity=1.0 is valid (maximum boundary)."""
    fill = AreaFill(**{"from": "baseline", "to": "new", "opacity": 1.0})
    assert fill.opacity == 1.0


def test_opacity_valid_middle():
    """Test that a middle value like 0.5 is valid."""
    fill = AreaFill(**{"from": "baseline", "to": "new", "opacity": 0.5})
    assert fill.opacity == 0.5


def test_opacity_valid_decimal():
    """Test that decimal values are valid."""
    fill = AreaFill(**{"from": "baseline", "to": "new", "opacity": 0.75})
    assert fill.opacity == 0.75


def test_opacity_invalid_negative():
    """Test that negative opacity values raise ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        AreaFill(**{"from": "baseline", "to": "new", "opacity": -0.1})

    error = exc_info.value.errors()[0]
    assert "Invalid opacity: -0.1" in str(error.get("ctx", {}).get("error", ""))
    assert "Must be between 0.0 and 1.0" in str(error.get("ctx", {}).get("error", ""))


def test_opacity_invalid_over_one():
    """Test that opacity values over 1.0 raise ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        AreaFill(**{"from": "baseline", "to": "new", "opacity": 1.1})

    error = exc_info.value.errors()[0]
    assert "Invalid opacity: 1.1" in str(error.get("ctx", {}).get("error", ""))
    assert "Must be between 0.0 and 1.0" in str(error.get("ctx", {}).get("error", ""))


def test_opacity_invalid_large_value():
    """Test that very large opacity values raise ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        AreaFill(**{"from": "baseline", "to": "new", "opacity": 2.0})

    error = exc_info.value.errors()[0]
    assert "Invalid opacity: 2.0" in str(error.get("ctx", {}).get("error", ""))
    assert "Must be between 0.0 and 1.0" in str(error.get("ctx", {}).get("error", ""))


def test_opacity_invalid_very_negative():
    """Test that very negative opacity values raise ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        AreaFill(**{"from": "baseline", "to": "new", "opacity": -1.0})

    error = exc_info.value.errors()[0]
    assert "Invalid opacity: -1.0" in str(error.get("ctx", {}).get("error", ""))
    assert "Must be between 0.0 and 1.0" in str(error.get("ctx", {}).get("error", ""))


def test_opacity_boundary_just_below_zero():
    """Test that opacity just below 0.0 raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        AreaFill(**{"from": "baseline", "to": "new", "opacity": -0.01})

    error = exc_info.value.errors()[0]
    assert "Invalid opacity: -0.01" in str(error.get("ctx", {}).get("error", ""))


def test_opacity_boundary_just_above_one():
    """Test that opacity just above 1.0 raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        AreaFill(**{"from": "baseline", "to": "new", "opacity": 1.01})

    error = exc_info.value.errors()[0]
    assert "Invalid opacity: 1.01" in str(error.get("ctx", {}).get("error", ""))
