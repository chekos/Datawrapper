# Column Charts

## Example

This example demonstrates how to create a column chart showing U.S. unemployment rates from 2016-2020, highlighting the dramatic spike during the COVID-19 pandemic.

```python
import pandas as pd
import datawrapper as dw

# Load unemployment data from GitHub
url = "https://raw.githubusercontent.com/palewire/datawrapper-api-classes/main/tests/samples/column/unemployment.csv"
df = pd.read_csv(url)

chart = dw.ColumnChart(
    # Chart title with HTML line break
    title="U.S. unemployment rate",
    # Data source attribution
    source_name="U.S. Bureau of Labor Statistics",
    source_url="https://www.bls.gov/",
    # Introductory text
    intro="Seasonally adjusted unemployment rate, January 2016 - September 2020",
    # Chart byline
    byline="Sergio Hernandez",
    # Data from pandas DataFrame
    data=df,
    # Format Y-axis grid labels with one decimal place
    y_grid_format=dw.NumberFormat.ONE_DECIMAL,
    # Always show value labels
    show_value_labels="always",
    # Place value labels outside the columns
    value_labels_placement="outside",
    # Format value labels with one decimal place
    value_labels_format=dw.NumberFormat.ONE_DECIMAL,
    # Set fixed plot height in pixels
    plot_height=228,
    # Highlight specific column in red
    column_color={"2020/04": "#c71e1d"},
)

chart.create()
```

<div style="min-height:433px" id="datawrapper-vis-1rJm1"><script type="text/javascript" defer src="https://datawrapper.dwcdn.net/1rJm1/embed.js" charset="utf-8" data-target="#datawrapper-vis-1rJm1"></script><noscript><img src="https://datawrapper.dwcdn.net/1rJm1/full.png" alt="" /></noscript></div>

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.ColumnChart
