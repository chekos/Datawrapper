# StackedBarChart

## Example

This example recreates a stacked bar chart showing trust in media reporting on various topics in Germany, with percentages stacked to show the distribution of trust levels.

```python
import pandas as pd
import datawrapper as dw

# Load data from GitHub
df = pd.read_csv(
    "https://raw.githubusercontent.com/palewire/Datawrapper/main/tests/samples/stacked_bar/media-trust.csv",
    sep=";"
)

# Create stacked bar chart
chart = dw.StackedBarChart(
    # Chart title
    title="How much do you trust the media reporting on the following topics?",
    # Intro text
    intro="Survey of 1,002 Germans, conducted in January 2016",
    # Data source attribution
    source_name="Infratest dimap for NDR",
    source_url="https://www.tagesschau.de/inland/deutschlandtrend/",
    # Byline
    byline="Lisa Charlotte Muth, Datawrapper",
    # Data
    data=df,
    # Stack as percentages
    stack_percentages=True,
    # Value label format (percentage)
    value_labels_format=dw.NumberFormat.PERCENT_INTEGER,
    # Color category mapping for trust levels
    color_category={
        "Very high trust": "#15607a",
        "High trust": "#5b9bae",
        "No answer": "#cccccc",
        "Low trust": "#d8b365",
        "Very low trust": "#8c510a",
    },
    # Category order for legend
    category_order=[
        "Very high trust",
        "High trust",
        "No answer",
        "Low trust",
        "Very low trust",
    ],
    # Don't sort bars (keep original order)
    sort_bars=False,
)

# Create the chart
chart.create()
```

<iframe title="How much do you trust the media reporting on the following topics?" aria-label="Stacked Bars" id="datawrapper-chart-yAViP" src="https://datawrapper.dwcdn.net/yAViP/3/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="296" data-external="1"></iframe><script type="text/javascript">!function(){"use strict";window.addEventListener("message",(function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r=0;r<e.length;r++)if(e[r].contentWindow===a.source){var i=a.data["datawrapper-height"][t]+"px";e[r].style.height=i}}}))}();
</script>

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.StackedBarChart
