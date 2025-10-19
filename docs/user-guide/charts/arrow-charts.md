# ArrowChart

## Example

This example demonstrates how to create an arrow chart showing income inequality (Gini index) before and after taxes across different countries. The chart highlights how tax policies affect income distribution.

```python
import pandas as pd
import datawrapper as dw

# Load data from GitHub
url = "https://raw.githubusercontent.com/palewire/datawrapper-api-classes/main/tests/samples/arrow/inequality.csv"
df = pd.read_csv(url)

# Create arrow chart
chart = dw.ArrowChart(
    # Chart title
    title="Many European countries bring income inequality down with taxes. The US and Mexico: Not so much.",
    # Data source attribution
    source_name="OECD",
    # Pass the DataFrame
    data=df,
    # Start column (Gini before taxes)
    axis_start="Gini before taxes",
    # End column (Gini after taxes)
    axis_end="Gini after taxes",
    # Custom Y-axis range
    custom_range_y=[0.15, 0.6],
    # Y-axis grid format (thousands separator with optional decimals)
    y_grid_format=dw.NumberFormat.THOUSANDS_WITH_OPTIONAL_DECIMALS,
    # Value label format (one decimal place)
    value_label_format=dw.NumberFormat.ONE_DECIMAL,
    # Sort by the start column
    sort_by="Gini before taxes",
    # Enable sorting
    sort_ranges=True,
    # Label position (right side)
    labeling="right",
    # Show arrow key/legend
    show_arrow_key=True,
    # Highlight specific countries in red
    color_category={
        "Mexico": "#c71e1d",
        "United States": "#c71e1d"
    }
)

# Create the chart in Datawrapper
chart.create()
```

<iframe title="Many European countries bring income inequality down with taxes. The US and Mexico: Not so much." aria-label="Arrow Plot" id="datawrapper-chart-cjX4C" src="https://datawrapper.dwcdn.net/cjX4C/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="656" data-external="1"></iframe><script type="text/javascript">!function(){"use strict";window.addEventListener("message",(function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r=0;r<e.length;r++)if(e[r].contentWindow===a.source){var i=a.data["datawrapper-height"][t]+"px";e[r].style.height=i}}}))}();
</script>

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.ArrowChart
