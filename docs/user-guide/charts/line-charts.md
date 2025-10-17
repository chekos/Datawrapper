# Line Charts

## Basic Example

```python
import pandas as pd
from datawrapper import LineChart, DateFormat, NumberFormat, LineWidth

chart = LineChart(
    title="Global Average Temperature Anomaly",
    intro="Temperature change relative to 1951-1980 average",
    data=pd.DataFrame(
        {
            "Year": [
                "1980",
                "1985",
                "1990",
                "1995",
                "2000",
                "2005",
                "2010",
                "2015",
                "2020",
                "2023",
            ],
            "Temperature": [0.26, 0.12, 0.45, 0.45, 0.42, 0.68, 0.72, 0.90, 1.02, 1.17],
        }
    ),
    x_grid_format=DateFormat.YEAR_FULL,
    y_grid_format=NumberFormat.ONE_DECIMAL,
    value_labels_format=NumberFormat.ONE_DECIMAL,
    base_color="#7f8c8d",
    lines=[
        dict(
            column="Temperature",
            width=LineWidth.THICK,
            symbols=dict(size=8, on="last"),
            value_labels=dict(last=True),
        )
    ],
)

chart.create()
```

## API Reference

```{eval-rst}
.. currentmodule:: datawrapper.charts

.. autoclass:: LineChart
    :members:
    :inherited-members:
```
