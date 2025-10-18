.. _enums:

Enums
=====

Enum classes provide type-safe configuration options for chart formatting and styling.

.. currentmodule:: datawrapper.charts.enums

ArrowHead
---------

.. code-block:: python

   from datawrapper.charts import ArrowHead
   connector = ConnectorLine(arrow_head=ArrowHead.TRIANGLE)

.. enum-table:: datawrapper.charts.enums.ArrowHead

ConnectorLineType
-----------------

.. code-block:: python

   from datawrapper import ConnectorLineType
   connector = ConnectorLine(type=ConnectorLineType.CURVE_RIGHT)

.. enum-table:: datawrapper.charts.enums.ConnectorLineType

DateFormat
----------

.. code-block:: python

   from datawrapper.charts import DateFormat
   chart = LineChart(x_grid_format=DateFormat.MONTH_ABBREVIATED_WITH_YEAR)

.. enum-table:: datawrapper.charts.enums.DateFormat

GridDisplay
-----------

.. code-block:: python

   from datawrapper.charts import GridDisplay
   chart = LineChart(x_grid_display=GridDisplay.ON)

.. enum-table:: datawrapper.charts.enums.GridDisplay

GridLabelAlign
--------------

.. code-block:: python

   from datawrapper.charts import GridLabelAlign
   chart = BarChart(axis_label_align=GridLabelAlign.CENTER)

.. enum-table:: datawrapper.charts.enums.GridLabelAlign

GridLabelPosition
-----------------

.. code-block:: python

   from datawrapper.charts import GridLabelPosition
   chart = ColumnChart(y_grid_label_position=GridLabelPosition.INSIDE)

.. enum-table:: datawrapper.charts.enums.GridLabelPosition

LineDash
--------

.. code-block:: python

   from datawrapper.charts import LineDash
   line = Line(column="temperature", dash=LineDash.DASHED)

.. enum-table:: datawrapper.charts.enums.LineDash

LineInterpolation
-----------------

.. code-block:: python

   from datawrapper.charts import LineInterpolation
   line = Line(column="temperature", interpolation=LineInterpolation.MONOTONE)

.. enum-table:: datawrapper.charts.enums.LineInterpolation

LineWidth
---------

.. code-block:: python

   from datawrapper.charts import LineWidth
   line = Line(column="temperature", width=LineWidth.THICK)

.. enum-table:: datawrapper.charts.enums.LineWidth

NumberDivisor
-------------

.. code-block:: python

   from datawrapper.charts import NumberDivisor
   col_format = ColumnFormat(column="revenue", number_divisor=NumberDivisor.DIVIDE_BY_MILLION)

.. enum-table:: datawrapper.charts.enums.NumberDivisor

NumberFormat
------------

.. code-block:: python

   from datawrapper.charts import NumberFormat
   chart = BarChart(axis_label_format=NumberFormat.THOUSANDS_SEPARATOR)

.. enum-table:: datawrapper.charts.enums.NumberFormat

PlotHeightMode
--------------

.. code-block:: python

   from datawrapper.charts import PlotHeightMode
   chart = LineChart(plot_height=400)  # Uses PlotHeightMode.FIXED internally

.. enum-table:: datawrapper.charts.enums.PlotHeightMode

RegressionMethod
----------------

.. code-block:: python

   from datawrapper.charts import RegressionMethod
   chart = ScatterPlot(regression_method=RegressionMethod.LINEAR)

.. enum-table:: datawrapper.charts.enums.RegressionMethod

ReplaceFlagsType
----------------

.. code-block:: python

   from datawrapper.charts import ReplaceFlagsType
   chart = BarChart(replace_flags=ReplaceFlagsType.FOUR_BY_THREE)

.. enum-table:: datawrapper.charts.enums.ReplaceFlagsType

ScatterAxisPosition
-------------------

.. code-block:: python

   from datawrapper.charts import ScatterAxisPosition
   chart = ScatterPlot(x_axis_position=ScatterAxisPosition.BOTTOM)

.. enum-table:: datawrapper.charts.enums.ScatterAxisPosition

ScatterGridLines
----------------

.. code-block:: python

   from datawrapper.charts import ScatterGridLines
   chart = ScatterPlot(x_grid_lines=ScatterGridLines.ON)

.. enum-table:: datawrapper.charts.enums.ScatterGridLines

ScatterShape
------------

.. code-block:: python

   from datawrapper.charts import ScatterShape
   chart = ScatterPlot(shape=ScatterShape.CIRCLE)

.. enum-table:: datawrapper.charts.enums.ScatterShape

ScatterSize
-----------

.. code-block:: python

   from datawrapper.charts import ScatterSize
   chart = ScatterPlot(size=ScatterSize.MEDIUM)

.. enum-table:: datawrapper.charts.enums.ScatterSize

StrokeWidth
-----------

.. code-block:: python

   from datawrapper.charts import StrokeWidth
   connector = ConnectorLine(stroke=StrokeWidth.MEDIUM)

.. enum-table:: datawrapper.charts.enums.StrokeWidth

SymbolDisplay
-------------

.. code-block:: python

   from datawrapper.charts import SymbolDisplay
   symbol = LineSymbol(display=SymbolDisplay.FIRST_LAST)

.. enum-table:: datawrapper.charts.enums.SymbolDisplay

SymbolShape
-----------

.. code-block:: python

   from datawrapper.charts import SymbolShape
   symbol = LineSymbol(shape=SymbolShape.CIRCLE)

.. enum-table:: datawrapper.charts.enums.SymbolShape

SymbolStyle
-----------

.. code-block:: python

   from datawrapper.charts import SymbolStyle
   symbol = LineSymbol(style=SymbolStyle.OUTLINED)

.. enum-table:: datawrapper.charts.enums.SymbolStyle

ValueLabelAlignment
-------------------

.. code-block:: python

   from datawrapper.charts import ValueLabelAlignment
   chart = BarChart(value_label_alignment=ValueLabelAlignment.CENTER)

.. enum-table:: datawrapper.charts.enums.ValueLabelAlignment

ValueLabelDisplay
-----------------

.. code-block:: python

   from datawrapper.charts import ValueLabelDisplay
   chart = ColumnChart(show_value_labels=ValueLabelDisplay.ALWAYS)

.. enum-table:: datawrapper.charts.enums.ValueLabelDisplay

ValueLabelMode
--------------

.. code-block:: python

   from datawrapper.charts import ValueLabelMode
   value_label = LineValueLabel(mode=ValueLabelMode.ALWAYS)

.. enum-table:: datawrapper.charts.enums.ValueLabelMode

ValueLabelPlacement
-------------------

.. code-block:: python

   from datawrapper.charts import ValueLabelPlacement
   chart = ColumnChart(value_labels_placement=ValueLabelPlacement.OUTSIDE)

.. enum-table:: datawrapper.charts.enums.ValueLabelPlacement
