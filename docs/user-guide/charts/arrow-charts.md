# Arrow Charts

## Basic Example

```python
import pandas as pd
from datawrapper.charts import ArrowChart, NumberFormat

# Prepare data with start and end columns
data = pd.DataFrame(
    {
        "Country": [
            ":us: United States",
            ":cn: China",
            ":jp: Japan",
            ":de: Germany",
            ":in: India",
        ],
        "2020": [20.9, 14.7, 5.0, 3.8, 2.7],
        "2024": [23.5, 18.2, 4.8, 4.1, 3.9],
    }
)

chart = ArrowChart(
    title="GDP Growth: 2020 to 2024",
    intro="Gross Domestic Product in trillions of USD",
    source_name="World Bank",
    data=data,
    axis_start="2020",
    axis_end="2024",
    value_label_format=NumberFormat.ONE_DECIMAL,
    sort_ranges=True,
    sort_by="end",
    reverse_order=True,
    thick_arrows=True,
    replace_flags="4x3",
)

chart.create()
```

## API Reference

```{eval-rst}
.. autoclass:: datawrapper.charts.ArrowChart
   :members:
   :inherited-members:
   :exclude-members: model_config, model_fields, model_computed_fields
