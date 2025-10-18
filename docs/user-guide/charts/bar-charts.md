# Bar Charts

## Example

```python
import pandas as pd
from datawrapper import BarChart, NumberFormat

chart = BarChart(
    title="Customer Satisfaction Survey",
    intro="How satisfied are you with our service?",
    data=pd.DataFrame(
        {
            "Response": [
                "Very Satisfied",
                "Satisfied",
                "Neutral",
                "Dissatisfied",
                "Very Dissatisfied",
            ],
            "Percentage": [45, 35, 12, 5, 3],
        }
    ),
    value_label_format=NumberFormat.PERCENT_INTEGER,
    show_value_labels=True,
    value_label_alignment="right",
    sort_bars=False,  # Keep original order
    color_category={
        "Very Satisfied": "#2ecc71",
        "Satisfied": "#95a5a6",
        "Neutral": "#f39c12",
        "Dissatisfied": "#e74c3c",
        "Very Dissatisfied": "#c0392b",
    },
)
chart.create()
```

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.BarChart
```
