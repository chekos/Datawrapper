"""Test backwards compatibility and functionality of all enum types."""

from datawrapper.charts import (
    AreaChart,
    ArrowChart,
    BarChart,
    ColumnChart,
    LineChart,
    ScatterPlot,
    StackedBarChart,
)
from datawrapper.charts.annos import ConnectorLine, TextAnnotation
from datawrapper.charts.enums import (
    ArrowHead,
    ConnectorLineType,
    DateFormat,
    GridDisplay,
    GridLabelAlign,
    GridLabelPosition,
    LineInterpolation,
    NumberFormat,
    RegressionMethod,
    ReplaceFlagsType,
    ScatterAxisPosition,
    ScatterGridLines,
    ScatterShape,
    ScatterSize,
    StrokeWidth,
    SymbolDisplay,
    SymbolShape,
    SymbolStyle,
    ValueLabelAlignment,
    ValueLabelDisplay,
    ValueLabelMode,
    ValueLabelPlacement,
)
from datawrapper.charts.line import Line, LineSymbol


class TestGridDisplayEnum:
    """Test GridDisplay enum backwards compatibility."""

    def test_enum_values(self):
        """Test using enum values."""
        chart = AreaChart(
            title="Test",
            x_grid=GridDisplay.LINES,
            y_grid=GridDisplay.TICKS,
        )
        assert chart.x_grid == "lines"
        assert chart.y_grid == "ticks"

    def test_raw_strings(self):
        """Test using raw string values."""
        chart = AreaChart(
            title="Test",
            x_grid="on",
            y_grid="off",
        )
        assert chart.x_grid == "on"
        assert chart.y_grid == "off"


class TestGridLabelEnums:
    """Test GridLabelPosition and GridLabelAlign enums."""

    def test_position_enum(self):
        """Test GridLabelPosition enum."""
        chart = AreaChart(
            title="Test",
            y_grid_labels=GridLabelPosition.INSIDE,
        )
        assert chart.y_grid_labels == "inside"

    def test_align_enum(self):
        """Test GridLabelAlign enum."""
        chart = AreaChart(
            title="Test",
            y_grid_label_align=GridLabelAlign.LEFT,
        )
        assert chart.y_grid_label_align == "left"

    def test_raw_strings(self):
        """Test using raw string values."""
        chart = AreaChart(
            title="Test",
            y_grid_labels="outside",
            y_grid_label_align="center",
        )
        assert chart.y_grid_labels == "outside"
        assert chart.y_grid_label_align == "center"


class TestLineInterpolationEnum:
    """Test LineInterpolation enum backwards compatibility."""

    def test_enum_values(self):
        """Test using enum values."""
        chart = AreaChart(
            title="Test",
            interpolation=LineInterpolation.STEP,
        )
        assert chart.interpolation == "step"

    def test_raw_strings(self):
        """Test using raw string values."""
        chart = LineChart(
            title="Test",
            interpolation="cardinal",
        )
        assert chart.interpolation == "cardinal"

    def test_all_interpolation_types(self):
        """Test all interpolation types."""
        interpolations = [
            (LineInterpolation.LINEAR, "linear"),
            (LineInterpolation.STEP, "step"),
            (LineInterpolation.STEP_AFTER, "step-after"),
            (LineInterpolation.STEP_BEFORE, "step-before"),
            (LineInterpolation.CARDINAL, "cardinal"),
            (LineInterpolation.MONOTONE, "monotone-x"),
            (LineInterpolation.MONOTONE_X, "monotone-x"),
            (LineInterpolation.CURVED, "monotone-x"),
            (LineInterpolation.NATURAL, "natural"),
        ]
        for enum_val, expected in interpolations:
            chart = LineChart(title="Test", interpolation=enum_val)
            assert chart.interpolation == expected


class TestValueLabelEnums:
    """Test ValueLabel-related enums."""

    def test_display_enum_column_chart(self):
        """Test ValueLabelDisplay enum in ColumnChart."""
        chart = ColumnChart(
            title="Test",
            show_value_labels=ValueLabelDisplay.ALWAYS,
        )
        assert chart.show_value_labels == "always"

    def test_placement_enum(self):
        """Test ValueLabelPlacement enum."""
        chart = ColumnChart(
            title="Test",
            value_labels_placement=ValueLabelPlacement.OUTSIDE,
        )
        assert chart.value_labels_placement == "outside"

    def test_alignment_enum(self):
        """Test ValueLabelAlignment enum."""
        chart = BarChart(
            title="Test",
            value_label_alignment=ValueLabelAlignment.RIGHT,
        )
        assert chart.value_label_alignment == "right"

    def test_mode_enum(self):
        """Test ValueLabelMode enum."""
        chart = StackedBarChart(
            title="Test",
            value_label_mode=ValueLabelMode.DIVERGING,
        )
        assert chart.value_label_mode == "diverging"

    def test_raw_strings(self):
        """Test using raw string values."""
        chart = ColumnChart(
            title="Test",
            show_value_labels="hover",
            value_labels_placement="inside",
        )
        assert chart.show_value_labels == "hover"
        assert chart.value_labels_placement == "inside"

    def test_bar_chart_bool_show_value_labels(self):
        """Test that BarChart.show_value_labels is bool, not enum."""
        chart = BarChart(
            title="Test",
            show_value_labels=True,
        )
        assert chart.show_value_labels is True


class TestReplaceFlagsEnum:
    """Test ReplaceFlagsType enum backwards compatibility."""

    def test_enum_values(self):
        """Test using enum values."""
        chart = BarChart(
            title="Test",
            replace_flags=ReplaceFlagsType.FOUR_BY_THREE,
        )
        assert chart.replace_flags == "4x3"

    def test_raw_strings(self):
        """Test using raw string values."""
        chart = StackedBarChart(
            title="Test",
            replace_flags="circle",
        )
        assert chart.replace_flags == "circle"

    def test_all_flag_types(self):
        """Test all flag types."""
        flags = [
            (ReplaceFlagsType.OFF, "off"),
            (ReplaceFlagsType.FOUR_BY_THREE, "4x3"),
            (ReplaceFlagsType.ONE_BY_ONE, "1x1"),
            (ReplaceFlagsType.CIRCLE, "circle"),
        ]
        for enum_val, expected in flags:
            chart = ArrowChart(title="Test", replace_flags=enum_val)
            assert chart.replace_flags == expected


class TestConnectorLineEnums:
    """Test ConnectorLine-related enums."""

    def test_type_enum(self):
        """Test ConnectorLineType enum."""
        connector = ConnectorLine(
            type=ConnectorLineType.CURVE_RIGHT,
            stroke=2,
        )
        assert connector.type == "curveRight"

    def test_stroke_width_enum(self):
        """Test StrokeWidth enum."""
        connector = ConnectorLine(
            type="straight",
            stroke=StrokeWidth.MEDIUM,
        )
        assert connector.stroke == 2

    def test_arrow_head_enum(self):
        """Test ArrowHead enum."""
        connector = ConnectorLine(
            type="straight",
            stroke=1,
            arrow_head=ArrowHead.LINES,
        )
        assert connector.arrow_head == "lines"

    def test_raw_values(self):
        """Test using raw values."""
        connector = ConnectorLine(
            type="curveLeft",
            stroke=3,
            arrow_head="triangle",
        )
        assert connector.type == "curveLeft"
        assert connector.stroke == 3
        assert connector.arrow_head == "triangle"

    def test_in_text_annotation(self):
        """Test ConnectorLine in TextAnnotation."""
        anno = TextAnnotation(
            text="Test",
            x=10,
            y=20,
            connector_line=ConnectorLine(
                type=ConnectorLineType.STRAIGHT,
                stroke=StrokeWidth.THICK,
            ),
        )
        assert anno.connector_line.type == "straight"
        assert anno.connector_line.stroke == 3


class TestSymbolEnums:
    """Test Symbol-related enums."""

    def test_shape_enum(self):
        """Test SymbolShape enum."""
        symbol = LineSymbol(
            shape=SymbolShape.SQUARE,
            size=5,
        )
        assert symbol.shape == "square"

    def test_style_enum(self):
        """Test SymbolStyle enum."""
        symbol = LineSymbol(
            shape="circle",
            size=5,
            style=SymbolStyle.FILL,
        )
        assert symbol.style == "fill"

    def test_display_enum(self):
        """Test SymbolDisplay enum."""
        symbol = LineSymbol(
            shape="circle",
            size=5,
            on=SymbolDisplay.BOTH,
        )
        assert symbol.on == "both"

    def test_raw_values(self):
        """Test using raw values."""
        symbol = LineSymbol(
            shape="diamond",
            size=3,
            style="hollow",
        )
        assert symbol.shape == "diamond"
        assert symbol.style == "hollow"

    def test_in_line_model(self):
        """Test symbols in Line model."""
        line = Line(
            column="temperature",
            symbols=LineSymbol(
                shape=SymbolShape.CIRCLE,
                size=5,
                style=SymbolStyle.FILL,
                on=SymbolDisplay.BOTH,
            ),
        )
        assert line.symbols.shape == "circle"
        assert line.symbols.style == "fill"
        assert line.symbols.on == "both"


class TestScatterEnums:
    """Test Scatter-related enums."""

    def test_shape_enum(self):
        """Test ScatterShape enum."""
        chart = ScatterPlot(
            title="Test",
            fixed_shape=ScatterShape.SQUARE,
        )
        assert chart.fixed_shape == "symbolSquare"

    def test_size_enum(self):
        """Test ScatterSize enum."""
        chart = ScatterPlot(
            title="Test",
            size=ScatterSize.DYNAMIC,
        )
        assert chart.size == "dynamic"

    def test_axis_position_enum(self):
        """Test ScatterAxisPosition enum."""
        chart = ScatterPlot(
            title="Test",
            x_position=ScatterAxisPosition.LEFT,
            y_position=ScatterAxisPosition.BOTTOM,
        )
        assert chart.x_position == "left"
        assert chart.y_position == "bottom"

    def test_grid_lines_enum(self):
        """Test ScatterGridLines enum."""
        chart = ScatterPlot(
            title="Test",
            x_grid_lines=ScatterGridLines.NO_LABELS,
            y_grid_lines=ScatterGridLines.JUST_LABELS,
        )
        assert chart.x_grid_lines == "no-labels"
        assert chart.y_grid_lines == "just-labels"

    def test_regression_method_enum(self):
        """Test RegressionMethod enum."""
        chart = ScatterPlot(
            title="Test",
            regression_method=RegressionMethod.LINEAR,
        )
        assert chart.regression_method == "linear"

    def test_raw_values(self):
        """Test using raw values."""
        chart = ScatterPlot(
            title="Test",
            fixed_shape="symbolCircle",
            size="fixed",
            x_position="right",
            y_grid_lines="off",
            regression_method="linear",
        )
        assert chart.fixed_shape == "symbolCircle"
        assert chart.size == "fixed"
        assert chart.x_position == "right"
        assert chart.y_grid_lines == "off"
        assert chart.regression_method == "linear"


class TestNumberFormatEnum:
    """Test NumberFormat enum backwards compatibility."""

    def test_enum_values(self):
        """Test using enum values."""
        chart = BarChart(
            title="Test",
            axis_label_format=NumberFormat.THOUSANDS_SEPARATOR,
        )
        assert chart.axis_label_format == "0,0"

    def test_raw_strings(self):
        """Test using raw string values."""
        chart = ColumnChart(
            title="Test",
            y_grid_format="0.00",
        )
        assert chart.y_grid_format == "0.00"

    def test_various_formats(self):
        """Test various number formats."""
        formats = [
            (NumberFormat.INTEGER, "0"),
            (NumberFormat.ONE_DECIMAL, "0.0"),
            (NumberFormat.PERCENT_INTEGER, "0%"),
            (NumberFormat.ABBREVIATED, "0a"),
            (NumberFormat.CURRENCY_ABBREVIATED, "$0.[00]a"),
        ]
        for enum_val, expected in formats:
            chart = BarChart(title="Test", axis_label_format=enum_val)
            assert chart.axis_label_format == expected


class TestDateFormatEnum:
    """Test DateFormat enum backwards compatibility."""

    def test_enum_values(self):
        """Test using enum values."""
        chart = LineChart(
            title="Test",
            x_grid_format=DateFormat.MONTH_ABBREVIATED_WITH_YEAR,
        )
        assert chart.x_grid_format == "MMM 'YY"

    def test_raw_strings(self):
        """Test using raw string values."""
        chart = AreaChart(
            title="Test",
            x_grid_format="YYYY-MM-DD",
        )
        assert chart.x_grid_format == "YYYY-MM-DD"

    def test_various_formats(self):
        """Test various date formats."""
        formats = [
            (DateFormat.YEAR_FULL, "YYYY"),
            (DateFormat.MONTH_ABBREVIATED, "MMM"),
            (DateFormat.DAY_OF_WEEK_FULL, "dddd"),
            (DateFormat.HOUR_24_PADDED, "HH"),
        ]
        for enum_val, expected in formats:
            chart = LineChart(title="Test", x_grid_format=enum_val)
            assert chart.x_grid_format == expected


class TestEnumSerialization:
    """Test that enums serialize correctly."""

    def test_area_chart_serialization(self):
        """Test AreaChart serialization with enums."""
        chart = AreaChart(
            title="Test",
            x_grid=GridDisplay.LINES,
            interpolation=LineInterpolation.STEP,
        )
        serialized = chart.serialize_model()
        assert serialized["metadata"]["visualize"]["x-grid"] == "lines"
        assert serialized["metadata"]["visualize"]["interpolation"] == "step"

    def test_bar_chart_serialization(self):
        """Test BarChart serialization with enums."""
        chart = BarChart(
            title="Test",
            replace_flags=ReplaceFlagsType.CIRCLE,
            value_label_alignment=ValueLabelAlignment.LEFT,
        )
        serialized = chart.serialize_model()
        # replace_flags uses ReplaceFlags.serialize utility
        assert serialized["metadata"]["visualize"]["replace-flags"]["enabled"] is True
        assert serialized["metadata"]["visualize"]["replace-flags"]["style"] == "circle"
        assert serialized["metadata"]["visualize"]["value-label-alignment"] == "left"

    def test_column_chart_serialization(self):
        """Test ColumnChart serialization with enums."""
        chart = ColumnChart(
            title="Test",
            show_value_labels=ValueLabelDisplay.HOVER,
            value_labels_placement=ValueLabelPlacement.INSIDE,
        )
        serialized = chart.serialize_model()
        assert serialized["metadata"]["visualize"]["valueLabels"]["show"] == "hover"
        assert (
            serialized["metadata"]["visualize"]["valueLabels"]["placement"] == "inside"
        )

    def test_line_chart_serialization(self):
        """Test LineChart serialization with enums."""
        chart = LineChart(
            title="Test",
            interpolation=LineInterpolation.MONOTONE,
            x_grid=GridDisplay.TICKS,
        )
        serialized = chart.serialize_model()
        assert serialized["metadata"]["visualize"]["interpolation"] == "monotone-x"
        assert serialized["metadata"]["visualize"]["x-grid"] == "ticks"

    def test_scatter_plot_serialization(self):
        """Test ScatterPlot serialization with enums."""
        chart = ScatterPlot(
            title="Test",
            fixed_shape=ScatterShape.DIAMOND,
            x_position=ScatterAxisPosition.TOP,
        )
        serialized = chart.serialize_model()
        assert serialized["metadata"]["visualize"]["fixed-shape"] == "symbolDiamond"
        assert serialized["metadata"]["visualize"]["x-pos"] == "top"

    def test_connector_line_serialization(self):
        """Test ConnectorLine serialization with enums."""
        anno = TextAnnotation(
            text="Test",
            x=10,
            y=20,
            connector_line=ConnectorLine(
                type=ConnectorLineType.CURVE_LEFT,
                stroke=StrokeWidth.THICK,
                arrow_head=ArrowHead.TRIANGLE,
            ),
        )
        serialized = anno.serialize_model()
        assert serialized["connectorLine"]["type"] == "curveLeft"
        assert serialized["connectorLine"]["stroke"] == 3
        assert serialized["connectorLine"]["arrowHead"] == "triangle"


class TestEnumDeserialization:
    """Test that enums deserialize correctly from API responses."""

    def test_area_chart_deserialization(self):
        """Test AreaChart deserialization to enums."""
        api_response = {
            "id": "test123",
            "type": "d3-area",
            "title": "Test",
            "metadata": {
                "visualize": {
                    "x-grid": "lines",
                    "interpolation": "step",
                }
            },
        }
        init_data = AreaChart.deserialize_model(api_response)
        chart = AreaChart(**init_data)
        assert chart.x_grid == "lines"
        assert chart.interpolation == "step"

    def test_bar_chart_deserialization(self):
        """Test BarChart deserialization to enums."""
        api_response = {
            "id": "test123",
            "type": "d3-bars",
            "title": "Test",
            "metadata": {
                "visualize": {
                    "replace-flags": {"enabled": True, "style": "4x3"},
                    "value-label-alignment": "center",
                }
            },
        }
        init_data = BarChart.deserialize_model(api_response)
        chart = BarChart(**init_data)
        assert chart.replace_flags == "4x3"
        assert chart.value_label_alignment == "center"

    def test_column_chart_deserialization(self):
        """Test ColumnChart deserialization to enums."""
        api_response = {
            "id": "test123",
            "type": "column-chart",
            "title": "Test",
            "metadata": {
                "visualize": {
                    "valueLabels": {
                        "show": "always",
                        "placement": "outside",
                    }
                }
            },
        }
        init_data = ColumnChart.deserialize_model(api_response)
        chart = ColumnChart(**init_data)
        assert chart.show_value_labels == "always"
        assert chart.value_labels_placement == "outside"


class TestEnumEdgeCases:
    """Test edge cases and error handling."""

    def test_default_values(self):
        """Test that default values work correctly."""
        chart = AreaChart(title="Test")
        # Check that defaults are set correctly
        assert chart.x_grid == "off"
        assert chart.y_grid == "on"

    def test_mixed_enum_and_string_usage(self):
        """Test mixing enum and string values in same chart."""
        chart = AreaChart(
            title="Test",
            x_grid=GridDisplay.LINES,  # Using enum
            y_grid="ticks",  # Using string
            interpolation=LineInterpolation.STEP,  # Using enum
        )
        assert chart.x_grid == "lines"
        assert chart.y_grid == "ticks"
        assert chart.interpolation == "step"
