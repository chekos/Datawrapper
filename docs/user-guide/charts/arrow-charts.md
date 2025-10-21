# ArrowChart

This example, drawn from <a href="https://www.datawrapper.de/charts/arrow-plot">the Datawrapper documentation</a>, demonstrates how to create an arrow chart with customized sorting and highlighted elements.

<iframe title="Many European countries bring income inequality down with taxes. The US and Mexico: Not so much." aria-label="Arrow Plot" id="datawrapper-chart-W0zuU" src="https://datawrapper.dwcdn.net/W0zuU/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none; margin-bottom: 20px;" height="416" data-external="1"></iframe><script type="text/javascript">window.addEventListener("message",function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r,i=0;r=e[i];i++)if(r.contentWindow===a.source){var d=a.data["datawrapper-height"][t]+"px";r.style.height=d}}});</script>

```python
import pandas as pd
import datawrapper as dw

# Load data from GitHub
url = "https://raw.githubusercontent.com/chekos/datawrapper/main/tests/samples/arrow/inequality.csv"
df = pd.read_csv(url, sep="\t")

# Create arrow chart
chart = dw.ArrowChart(
    # Chart title
    title="Many European countries bring income inequality down with taxes. The US and Mexico: Not so much.",
    # The description line with a bit of HTML
    intro="Income inequality (gini index) in selected OECD countries in 2014, before and after taxes. A gini index of 0 means that every household earns exactly the same income, while an index of 1 means that one household in the country makes all the income. <b>The lower the Gini index, the more equal the income is distributed in a country.</b>",
    # Data source attribution
    source_name="OECD",
    # The byline
    byline="Lisa Charlotte Rost, Datawrapper",
    # Pass the DataFrame
    data=df,
    # Start column (Gini before taxes)
    start_column="Gini before taxes",
    # End column (Gini after taxes)
    end_column="Gini after taxes",
    # Custom X-axis range
    range_extent="custom",
    custom_range=[0.15, 0.6],
    # Value label format (three decimal places)
    value_label_format=dw.NumberFormat.THREE_DECIMALS,
    # Sort by the start column
    sort_by="end",
    # Enable sorting
    sort_ranges=True,
    # Show arrow key/legend
    arrow_key=True,
    # Set the default arrow color
    base_color="rgb(196, 148, 67)",
    # Highlight specific countries in red
    color_column="Country",
    label_column="Country",
    color_by_column=True,
    color_category={
        "<b>Mexico</b>": "#c71e1d",
        "<b>United States</b>": "#c71e1d"
    }
)

# Create the chart in Datawrapper
chart.create()
```

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.ArrowChart
