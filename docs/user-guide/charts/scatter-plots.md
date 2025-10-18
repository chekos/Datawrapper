# Scatter Plots

## Example

```python
import pandas as pd
from datawrapper import ScatterPlot, NumberFormat

chart = ScatterPlot(
    title="Height vs Weight Correlation",
    intro="Adult population sample (n=100)",
    data=pd.DataFrame(
        {
            "Height (cm)": [165, 170, 175, 180, 185, 160, 172, 178, 182, 168],
            "Weight (kg)": [65, 72, 78, 85, 92, 58, 70, 80, 88, 68],
            "Gender": ["F", "M", "M", "M", "M", "F", "F", "M", "M", "F"],
        }
    ),
    x_grid_format=NumberFormat.INTEGER,
    y_grid_format=NumberFormat.INTEGER,
    point_size=5,
    color_category={"F": "#e74c3c", "M": "#3498db"},
    show_legend=True,
    tooltip_enabled=False,
)

chart.create()
```

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.ScatterPlot
```
