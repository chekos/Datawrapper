# Column Charts

## Basic Example

```python
import pandas as pd
from datawrapper import ColumnChart, NumberFormat, DateFormat

chart = ColumnChart(
    title="Monthly Sales Performance",
    intro="Revenue by month in 2024",
    data=pd.DataFrame(
        {
            "Month": [
                "2025-01",
                "2025-02",
                "2025-03",
                "2025-04",
                "2025-05",
                "2025-06",
                "2025-07",
                "2025-08",
                "2025-09",
                "2025-10",
                "2025-11",
                "2025-12",
            ],
            "Revenue": [
                -15000,
                25000,
                48000,
                61000,
                58000,
                67000,
                72000,
                69000,
                74000,
                78000,
                82000,
                91000,
            ],
        }
    ),
    y_grid_format=NumberFormat.ABBREVIATED,
    value_labels_format=NumberFormat.ABBREVIATED,
    x_grid_format=DateFormat.MONTH_ABBREVIATED,
    show_value_labels="always",
    value_labels_placement="outside",
    column_color="#3498db",
    negative_color="#e74c3c",
)

chart.create()
```

## API Reference

```{eval-rst}
.. currentmodule:: datawrapper.charts

.. autoclass:: ColumnChart
    :members:
    :inherited-members:
```
