# Stacked Bar Charts

## Example

```python
import pandas as pd
from datawrapper import StackedBarChart, NumberFormat

chart = StackedBarChart(
    title="Survey Responses by Age Group",
    intro="How do you feel about remote work?",
    data=pd.DataFrame(
        {
            "Age Group": ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
            "Strongly Favor": [45, 52, 38, 28, 18, 12],
            "Somewhat Favor": [35, 30, 35, 32, 28, 20],
            "Neutral": [12, 10, 15, 20, 25, 28],
            "Somewhat Oppose": [5, 5, 8, 12, 18, 22],
            "Strongly Oppose": [3, 3, 4, 8, 11, 18],
        }
    ),
    value_labels_format=NumberFormat.INTEGER,
    show_value_labels=True,
    color_category={
        "Strongly Favor": "#2ecc71",
        "Somewhat Favor": "#95a5a6",
        "Neutral": "#f39c12",
        "Somewhat Oppose": "#e67e22",
        "Strongly Oppose": "#e74c3c",
    },
    sort_bars=False,
)

chart.create()
```

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.StackedBarChart
```
