"""Unit tests for ConnectorLine circle_style field validator."""

import pytest
from pydantic import ValidationError

from datawrapper.charts import ConnectorLine
from datawrapper.charts.enums.annos import StrokeType


def test_circle_style_valid_default():
    """Test that the default circle_style value ('solid') is valid."""
    connector = ConnectorLine()
    assert connector.circle_style == "solid"


def test_circle_style_valid_enum_solid():
    """Test that StrokeType.SOLID enum value is valid."""
    connector = ConnectorLine(circleStyle=StrokeType.SOLID)
    assert connector.circle_style == StrokeType.SOLID


def test_circle_style_valid_enum_dashed():
    """Test that StrokeType.DASHED enum value is valid."""
    connector = ConnectorLine(circleStyle=StrokeType.DASHED)
    assert connector.circle_style == StrokeType.DASHED


def test_circle_style_valid_string_solid():
    """Test that 'solid' string value is valid."""
    connector = ConnectorLine(circleStyle="solid")
    assert connector.circle_style == "solid"


def test_circle_style_valid_string_dashed():
    """Test that 'dashed' string value is valid."""
    connector = ConnectorLine(circleStyle="dashed")
    assert connector.circle_style == "dashed"


def test_circle_style_invalid_enum_dotted():
    """Test that StrokeType.DOTTED enum value raises ValidationError.

    Note: Pydantic converts enum values to strings before validation,
    so the error message will show 'dotted' not 'StrokeType.DOTTED'.
    """
    with pytest.raises(ValidationError) as exc_info:
        ConnectorLine(circleStyle=StrokeType.DOTTED)

    error = exc_info.value.errors()[0]
    # Pydantic converts the enum to its string value before validation
    assert "Invalid circle style: dotted" in str(error.get("ctx", {}).get("error", ""))
    assert "Must be either 'solid' or 'dashed'" in str(
        error.get("ctx", {}).get("error", "")
    )


def test_circle_style_invalid_string_dotted():
    """Test that 'dotted' string value raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        ConnectorLine(circleStyle="dotted")

    error = exc_info.value.errors()[0]
    assert "Invalid circle style: dotted" in str(error.get("ctx", {}).get("error", ""))
    assert "Must be either 'solid' or 'dashed'" in str(
        error.get("ctx", {}).get("error", "")
    )


def test_circle_style_invalid_string_random():
    """Test that invalid string values raise ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        ConnectorLine(circleStyle="invalid")

    error = exc_info.value.errors()[0]
    assert "Invalid circle style: invalid" in str(error.get("ctx", {}).get("error", ""))
    assert "Must be either 'solid' or 'dashed'" in str(
        error.get("ctx", {}).get("error", "")
    )


def test_circle_style_invalid_string_empty():
    """Test that empty string raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        ConnectorLine(circleStyle="")

    error = exc_info.value.errors()[0]
    assert "Invalid circle style:" in str(error.get("ctx", {}).get("error", ""))
    assert "Must be either 'solid' or 'dashed'" in str(
        error.get("ctx", {}).get("error", "")
    )


def test_circle_style_case_sensitive():
    """Test that circle_style validation is case-sensitive."""
    with pytest.raises(ValidationError) as exc_info:
        ConnectorLine(circleStyle="SOLID")

    error = exc_info.value.errors()[0]
    assert "Invalid circle style: SOLID" in str(error.get("ctx", {}).get("error", ""))


def test_circle_style_with_other_fields():
    """Test that circle_style validation works when other fields are set."""
    connector = ConnectorLine(type="straight", stroke=2, circleStyle=StrokeType.DASHED)
    assert connector.circle_style == StrokeType.DASHED
    assert connector.type == "straight"
    assert connector.stroke == 2


def test_circle_style_serialization_enum():
    """Test that enum values serialize correctly."""
    connector = ConnectorLine(circleStyle=StrokeType.SOLID)
    # Pydantic should serialize the enum to its string value
    assert connector.model_dump()["circle_style"] == "solid"


def test_circle_style_serialization_string():
    """Test that string values serialize correctly."""
    connector = ConnectorLine(circleStyle="dashed")
    assert connector.model_dump()["circle_style"] == "dashed"
