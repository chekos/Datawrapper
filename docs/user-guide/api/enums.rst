.. _enums:

Enums
=====

Enum classes provide type-safe configuration options for chart formatting and styling.

.. currentmodule:: datawrapper.charts.enums

ArrowHead
---------

.. code-block:: python

   import datawrapper as dw
   connector = dw.ConnectorLine(arrow_head=dw.ArrowHead.TRIANGLE)

.. enum-table:: datawrapper.charts.enums.ArrowHead

ConnectorLineType
-----------------

.. code-block:: python

   import datawrapper as dw
   connector = dw.ConnectorLine(type=dw.ConnectorLineType.CURVE_RIGHT)

.. enum-table:: datawrapper.charts.enums.ConnectorLineType

DateFormat
----------

.. code-block:: python

   import datawrapper as dw
   chart = dw.LineChart(x_grid_format=dw.DateFormat.MONTH_ABBREVIATED_WITH_YEAR)

.. enum-table:: datawrapper.charts.enums.DateFormat

GridDisplay
-----------

.. code-block:: python

   import datawrapper as dw
   chart = dw.LineChart(x_grid_display=dw.GridDisplay.ON)

.. enum-table:: datawrapper.charts.enums.GridDisplay

GridLabelAlign
--------------

.. code-block:: python

   import datawrapper as dw
   chart = dw.BarChart(axis_label_align=dw.GridLabelAlign.CENTER)

.. enum-table:: datawrapper.charts.enums.GridLabelAlign

GridLabelPosition
-----------------

.. code-block:: python

   import datawrapper as dw
   chart = dw.ColumnChart(y_grid_label_position=dw.GridLabelPosition.INSIDE)

.. enum-table:: datawrapper.charts.enums.GridLabelPosition

LineDash
--------

.. code-block:: python

   import datawrapper as dw
   line = dw.Line(column="temperature", dash=dw.LineDash.DASHED)

.. enum-table:: datawrapper.charts.enums.LineDash

LineInterpolation
-----------------

.. code-block:: python

   import datawrapper as dw
   line = dw.Line(column="temperature", interpolation=dw.LineInterpolation.CURVED)

.. enum-table:: datawrapper.charts.enums.LineInterpolation

LineWidth
---------

.. code-block:: python

   import datawrapper as dw
   line = dw.Line(column="temperature", width=dw.LineWidth.THICK)

.. enum-table:: datawrapper.charts.enums.LineWidth

NumberDivisor
-------------

.. code-block:: python

   import datawrapper as dw
   col_format = dw.ColumnFormat(column="revenue", number_divisor=dw.NumberDivisor.DIVIDE_BY_MILLION)

.. enum-table:: datawrapper.charts.enums.NumberDivisor

NumberFormat
------------

.. code-block:: python

   import datawrapper as dw
   chart = dw.BarChart(axis_label_format=dw.NumberFormat.THOUSANDS_SEPARATOR)

.. enum-table:: datawrapper.charts.enums.NumberFormat

RegressionMethod
----------------

.. code-block:: python

   import datawrapper as dw
   chart = dw.ScatterPlot(regression_method=dw.RegressionMethod.LINEAR)

.. enum-table:: datawrapper.charts.enums.RegressionMethod

ReplaceFlagsType
----------------

.. code-block:: python

   import datawrapper as dw
   chart = dw.BarChart(replace_flags=dw.ReplaceFlagsType.FOUR_BY_THREE)

.. enum-table:: datawrapper.charts.enums.ReplaceFlagsType

ScatterAxisPosition
-------------------

.. code-block:: python

   import datawrapper as dw
   chart = dw.ScatterPlot(x_axis_position=dw.ScatterAxisPosition.BOTTOM)

.. enum-table:: datawrapper.charts.enums.ScatterAxisPosition

ScatterGridLines
----------------

.. code-block:: python

   import datawrapper as dw
   chart = dw.ScatterPlot(x_grid_lines=dw.ScatterGridLines.ON)

.. enum-table:: datawrapper.charts.enums.ScatterGridLines

ScatterShape
------------

.. code-block:: python

   import datawrapper as dw
   chart = dw.ScatterPlot(shape=dw.ScatterShape.CIRCLE)

.. enum-table:: datawrapper.charts.enums.ScatterShape

ScatterSize
-----------

.. code-block:: python

   import datawrapper as dw
   chart = dw.ScatterPlot(size=dw.ScatterSize.MEDIUM)

.. enum-table:: datawrapper.charts.enums.ScatterSize

StrokeWidth
-----------

.. code-block:: python

   import datawrapper as dw
   connector = dw.ConnectorLine(stroke=dw.StrokeWidth.MEDIUM)

.. enum-table:: datawrapper.charts.enums.StrokeWidth

SymbolDisplay
-------------

.. code-block:: python

   import datawrapper as dw
   symbol = dw.LineSymbol(display=dw.SymbolDisplay.FIRST_LAST)

.. enum-table:: datawrapper.charts.enums.SymbolDisplay

SymbolShape
-----------

.. code-block:: python

   import datawrapper as dw
   symbol = dw.LineSymbol(shape=dw.SymbolShape.CIRCLE)

.. enum-table:: datawrapper.charts.enums.SymbolShape

SymbolStyle
-----------

.. code-block:: python

   import datawrapper as dw
   symbol = dw.LineSymbol(style=dw.SymbolStyle.OUTLINED)

.. enum-table:: datawrapper.charts.enums.SymbolStyle

ValueLabelAlignment
-------------------

.. code-block:: python

   import datawrapper as dw
   chart = dw.BarChart(value_label_alignment=dw.ValueLabelAlignment.CENTER)

.. enum-table:: datawrapper.charts.enums.ValueLabelAlignment

ValueLabelDisplay
-----------------

.. code-block:: python

   import datawrapper as dw
   chart = dw.ColumnChart(show_value_labels=dw.ValueLabelDisplay.ALWAYS)

.. enum-table:: datawrapper.charts.enums.ValueLabelDisplay

ValueLabelMode
--------------

.. code-block:: python

   import datawrapper as dw
   value_label = dw.LineValueLabel(mode=dw.ValueLabelMode.ALWAYS)

.. enum-table:: datawrapper.charts.enums.ValueLabelMode

ValueLabelPlacement
-------------------

.. code-block:: python

   import datawrapper as dw
   chart = dw.ColumnChart(value_labels_placement=dw.ValueLabelPlacement.OUTSIDE)

.. enum-table:: datawrapper.charts.enums.ValueLabelPlacement
