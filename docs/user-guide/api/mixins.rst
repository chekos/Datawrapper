Mixins
======

The mixins module provides reusable functionality that can be shared across multiple chart types. These mixins handle common chart configuration patterns like grid display, formatting, and axis customization.

.. currentmodule:: datawrapper.charts.mixins

Grid Configuration
------------------

GridDisplayMixin
~~~~~~~~~~~~~~~

Controls the visibility of grid lines on chart axes.

.. autoclass:: GridDisplayMixin
   :members:
   :show-inheritance:

**Example:**

.. code-block:: python

   import datawrapper as dw

   chart = dw.LineChart(
       title="Temperature Trends",
       x_grid=dw.GridDisplay.OFF,
       y_grid=dw.GridDisplay.ON
   )

GridFormatMixin
~~~~~~~~~~~~~~~

Controls the formatting of grid labels on chart axes.

.. autoclass:: GridFormatMixin
   :members:
   :show-inheritance:

**Example:**

.. code-block:: python

   import datawrapper as dw

   chart = dw.LineChart(
       title="Sales Over Time",
       x_grid_format=dw.DateFormat.MONTH_ABBREVIATED_WITH_YEAR,
       y_grid_format=dw.NumberFormat.THOUSANDS_SEPARATOR
   )

Axis Customization
------------------

CustomRangeMixin
~~~~~~~~~~~~~~~~

Sets custom minimum and maximum values for chart axes.

.. autoclass:: CustomRangeMixin
   :members:
   :show-inheritance:

**Example:**

.. code-block:: python

   import datawrapper as dw

   chart = dw.ColumnChart(
       title="Revenue by Quarter",
       custom_range_y=[0, 1000000]  # Set Y-axis from 0 to 1M
   )

CustomTicksMixin
~~~~~~~~~~~~~~~~

Sets custom tick mark positions on chart axes.

.. autoclass:: CustomTicksMixin
   :members:
   :show-inheritance:

**Example:**

.. code-block:: python

   import datawrapper as dw

   chart = dw.LineChart(
       title="Monthly Data",
       custom_ticks_x=["Jan", "Apr", "Jul", "Oct"],
       custom_ticks_y=[0, 25, 50, 75, 100]
   )
