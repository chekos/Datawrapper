# LineChart

## Example

This example demonstrates how to create a line chart showing global land temperature in July from 1753-2015, with confidence intervals displayed as a shaded area.

```python
import pandas as pd
import datawrapper as dw

# Load temperature data from GitHub
url = "https://raw.githubusercontent.com/palewire/datawrapper-api-classes/main/tests/samples/line/land-temps.csv"
df = pd.read_csv(url)

chart = dw.LineChart(
    # Chart title
    title="Global land temperature in July, 1753-2015",
    # Data source attribution
    source_name="Berkeley Earth",
    source_url="http://berkeleyearth.org/data/",
    # Introductory text
    intro="Average land temperature in July, in degrees Celsius",
    # Chart byline
    byline="John Burn-Murdoch",
    # Data from pandas DataFrame
    data=df,
    # Hide X-axis grid lines
    x_grid_display="off",
    # Show Y-axis grid lines
    y_grid_display="on",
    # Format Y-axis grid labels with one decimal place
    y_grid_format=dw.NumberFormat.ONE_DECIMAL,
    # Use monotone interpolation for smooth curves
    interpolation=dw.LineInterpolation.MONOTONE,
    # Configure the main temperature line
    lines=[
        dw.Line(
            # Column to plot
            column="LandAverageTemperature",
            # Line color
            color="#c71e1d",
            # Line width
            width=dw.LineWidth.MEDIUM,
            # Show symbol on last data point
            symbols=dw.LineSymbol(
                display=dw.SymbolDisplay.LAST,
                size=5
            ),
            # Show value label on last data point
            value_labels=dw.LineValueLabel(
                last=True
            )
        )
    ],
    # Add shaded confidence interval area
    area_fills=[
        {
            "from": "lower",
            "to": "upper",
            "color": "#cccccc",
            "opacity": 0.5
        }
    ],
)

chart.create()
```

<div style="min-height:433px" id="datawrapper-vis-BsBaq"><script type="text/javascript" defer src="https://datawrapper.dwcdn.net/BsBaq/embed.js" charset="utf-8" data-target="#datawrapper-vis-BsBaq"></script><noscript><img src="https://datawrapper.dwcdn.net/BsBaq/full.png" alt="" /></noscript></div>

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.LineChart
