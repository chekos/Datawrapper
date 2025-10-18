"""Test that all enums are properly exported at multiple levels."""


class TestEnumImportsTopLevel:
    """Test that enums can be imported from the top-level datawrapper package."""

    def test_import_from_top_level(self):
        """Test importing all enums from datawrapper."""
        from datawrapper import (
            ConnectorLineType,
            GridDisplay,
            LineInterpolation,
            ScatterShape,
            ValueLabelDisplay,
        )

        # Verify they are the correct types
        assert hasattr(GridDisplay, "ON")
        assert hasattr(ValueLabelDisplay, "ALWAYS")
        assert hasattr(ScatterShape, "CIRCLE")
        assert hasattr(LineInterpolation, "LINEAR")
        assert hasattr(ConnectorLineType, "STRAIGHT")


class TestEnumImportsChartsLevel:
    """Test that enums can be imported from datawrapper.charts."""

    def test_import_from_charts_level(self):
        """Test importing all enums from datawrapper.charts."""
        from datawrapper.charts import (
            GridDisplay,
            RegressionMethod,
            ScatterSize,
            ValueLabelPlacement,
        )

        # Verify they are the correct types
        assert hasattr(GridDisplay, "OFF")
        assert hasattr(ValueLabelPlacement, "OUTSIDE")
        assert hasattr(ScatterSize, "FIXED")
        assert hasattr(RegressionMethod, "LINEAR")


class TestEnumImportsEnumsLevel:
    """Test that enums can be imported from datawrapper.charts.enums."""

    def test_import_from_enums_level(self):
        """Test importing all enums from datawrapper.charts.enums."""
        from datawrapper.charts.enums import (
            ArrowHead,
            GridLabelAlign,
            GridLabelPosition,
            SymbolStyle,
        )

        # Verify they are the correct types
        assert hasattr(GridLabelPosition, "AUTO")
        assert hasattr(GridLabelAlign, "LEFT")
        assert hasattr(SymbolStyle, "FILL")
        assert hasattr(ArrowHead, "LINES")


class TestEnumValues:
    """Test that enum values are correct."""

    def test_enum_values(self):
        """Test that enum values serialize correctly."""
        from datawrapper.charts.enums import (
            GridDisplay,
            LineInterpolation,
            NumberFormat,
            ScatterShape,
            ScatterSize,
            ValueLabelAlignment,
        )

        # Test string enum values
        assert GridDisplay.ON.value == "on"
        assert GridDisplay.OFF.value == "off"
        assert LineInterpolation.LINEAR.value == "linear"
        assert LineInterpolation.MONOTONE.value == "monotone-x"
        assert ScatterShape.CIRCLE.value == "symbolCircle"
        assert ScatterShape.SQUARE.value == "symbolSquare"
        assert ScatterSize.FIXED.value == "fixed"
        assert ScatterSize.DYNAMIC.value == "dynamic"
        assert ValueLabelAlignment.LEFT.value == "left"
        assert ValueLabelAlignment.RIGHT.value == "right"
        assert NumberFormat.THOUSANDS_SEPARATOR.value == "0,0"
        assert NumberFormat.ONE_DECIMAL.value == "0.0"
