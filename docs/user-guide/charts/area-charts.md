# Area Charts

## Basic Example

```python
import pandas as pd
from datawrapper import AreaChart, DateFormat, NumberFormat

chart = AreaChart(
    title="U.S. Energy Production by Source",
    intro="Trillion BTUs, 1950-2020",
    data=pd.DataFrame(
        {
            "Year": ["1950", "1960", "1970", "1980", "1990", "2000", "2010", "2020"],
            "Coal": [12.3, 10.8, 14.6, 18.6, 22.5, 22.7, 22.0, 11.3],
            "Natural Gas": [6.2, 12.7, 21.7, 19.9, 18.3, 19.7, 21.6, 34.5],
            "Petroleum": [11.4, 14.9, 20.4, 18.2, 15.6, 12.4, 11.6, 11.3],
            "Nuclear": [0.0, 0.0, 0.2, 2.7, 6.1, 8.0, 8.4, 8.2],
            "Renewables": [1.5, 1.6, 1.4, 2.9, 3.0, 3.0, 4.3, 7.7],
        }
    ),
    x_grid_format=DateFormat.YEAR_FULL,
    y_grid_format=NumberFormat.ONE_DECIMAL,
    value_labels_format=NumberFormat.ONE_DECIMAL,
    stack_areas=True,
    interpolation="linear",
    color_category={
        "Coal": "#34495e",
        "Natural Gas": "#3498db",
        "Petroleum": "#e67e22",
        "Nuclear": "#9b59b6",
        "Renewables": "#2ecc71",
    },
)
chart.create()
```

## API Reference

```{eval-rst}
.. currentmodule:: datawrapper.charts

.. autoclass:: AreaChart
    :members:
    :inherited-members:
```
