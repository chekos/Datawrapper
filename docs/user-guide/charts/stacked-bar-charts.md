# StackedBarChart

This example, drawn from [Datawrapper's official documentation](https://www.datawrapper.de/charts/stacked-bars), demonstrates how to create a diverging stacked bar chart showing trust levels in media reporting across different topics. The chart displays percentages with a [custom color scheme](https://colorbrewer2.org/#type=diverging&scheme=PRGn&n=5) to differentiate between trust levels, sorted by low trust values. It also includes value formatting.

<iframe title="Trust in Media Reporting" aria-label="Stacked Bars" id="datawrapper-chart-VVR4V" src="https://datawrapper.dwcdn.net/VVR4V/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="339" data-external="1"></iframe><script type="text/javascript">window.addEventListener("message",function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r,i=0;r=e[i];i++)if(r.contentWindow===a.source){var d=a.data["datawrapper-height"][t]+"px";r.style.height=d}}});</script>

```python
import pandas as pd
import datawrapper as dw

# Load media trust data from GitHub
df = pd.read_csv(
    "https://raw.githubusercontent.com/chekos/Datawrapper/main/tests/samples/stacked_bar/media-trust.csv",
    sep=";"
)

chart = dw.StackedBarChart(
    # Chart title
    title="Trust in Media Reporting",
    # Introductory text explaining the context
    intro="Trust in Media Reporting regarding widely reported topics of 2015",
    # Data source attribution
    source_name="Infratest dimap",
    source_url="http://www.infratest-dimap.de/umfragen-analysen/bundesweit/umfragen/aktuell/wenig-vertrauen-in-medienberichterstattung/",
    # Data from pandas DataFrame
    data=df,
    # Enable percentage stacking
    stack_percentages=True,
    # Format value labels as percentages
    value_label_format="0%",
    # Use diverging mode for better visual separation
    value_label_mode="diverging",
    # Sort bars by the "Low trust" column in descending order
    sort_bars=True,
    sort_by="Low trust",
    reverse_order=True,
    # Enable the color legend
    show_color_key=True,
    # Use thick bars for better visibility
    thick_bars=True,
    # Use block labels for category names
    block_labels=True,
    # Custom color mapping for each trust level
    color_category={
        "Very high trust": "#15607a",
        "High trust": "#719aae",
        "No answer": "#e8e8e8",
        "Low trust": "#ff6954",
        "Very low trust": "#c71e1d",
    },
)

# Create the chart in Datawrapper
chart.create()
```

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.StackedBarChart
