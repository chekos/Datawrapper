# Multiple Column Charts

## Basic Example

```python
import pandas as pd
from datawrapper.charts import MultipleColumnChart, NumberFormat

data = pd.DataFrame(
    {
        "Quarter": ["Q1", "Q2", "Q3", "Q4"] * 3,
        "Region": ["North"] * 4 + ["South"] * 4 + ["East"] * 4,
        "Sales": [450, 520, 580, 650, 320, 380, 290, 410, 280, 310, 330, 360],
    }
)

chart = MultipleColumnChart(
    title="Quarterly Sales by Region",
    intro="Sales performance across regions (in thousands)",
    source_name="Sales Database",
    data=data,
    grid_column=3,
    grid_row_height=140,
    y_grid_format=NumberFormat.ABBREVIATED,
    base_color="#3498db",
    show_value_labels="off",
    show_tooltips=True,
)

chart.create()
```

## API Reference

```{eval-rst}
.. autoclass:: datawrapper.charts.MultipleColumnChart
   :members:
   :inherited-members:
   :exclude-members: model_config, model_fields, model_computed_fields
```
