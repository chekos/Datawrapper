# MultipleColumnChart

This example, drawn from [Datawrapper's official documentation](https://www.datawrapper.de/charts/multiple-columns), demonstrates how to create small multiple column charts showing population growth in major cities from 1950 to 2035. The chart features custom panel titles with country information, highlighted data for 2025, a range annotation to mark the projection period and a 4-column grid layout.

<iframe title="Population of the world's largest cities, 1950 to 2035" aria-label="Multiple Columns" id="datawrapper-chart-8kNfG" src="https://datawrapper.dwcdn.net/8kNfG/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="460" data-external="1"></iframe><script type="text/javascript">window.addEventListener("message",function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r,i=0;r=e[i];i++)if(r.contentWindow===a.source){var d=a.data["datawrapper-height"][t]+"px";r.style.height=d}}});</script>

```python
import pandas as pd
import datawrapper as dw

# Load population data from GitHub
df = pd.read_csv(
    "https://raw.githubusercontent.com/chekos/Datawrapper/main/tests/samples/multiple_column/population.csv",
    sep="\t"
)

chart = dw.MultipleColumnChart(
    # Chart title
    title="Population of the world's largest cities, 1950 to 2035",
    # Data source attribution
    source_name="Our World in Data",
    source_url="https://ourworldindata.org/urbanization",
    # Data from pandas DataFrame
    data=df,
    # Layout configuration - 4 columns on desktop, 2 on mobile
    grid_layout="fixedCount",
    grid_column=4,
    grid_column_mobile=2,
    grid_row_height=140,
    # Sort panels by end value (2035 population) in descending order
    sort=True,
    sort_by="end",
    sort_reverse=False,
    # Set custom column color with highlighted year for 2025
    base_color="#c9a291",
    color_category={
        "2025": "#c71e1d"
    },
    # Format y-axis with abbreviated numbers
    y_grid_format=dw.NumberFormat.ABBREVIATED_ONE_DECIMAL,
    y_grid_labels="inside",
    y_grid_label_align="left",
    # Custom panel titles with city and country information
    panels=[
        {"column": "Delhi", "title": "Delhi, <span style=\"color:gray; font-weight: normal;\">India</span>"},
        {"column": "Dhaka", "title": "Dhaka, <span style=\"color:gray; font-weight: normal;\"> Bangladesh </span>"},
        {"column": "Lagos", "title": "Lagos, <span style=\"color:gray; font-weight: normal;\">Nigeria</span>"},
        {"column": "Paris", "title": "Paris, <span style=\"color:gray; font-weight: normal;\">France</span>"},
        {"column": "Tokyo", "title": "Tokyo, <span style=\"color:gray; font-weight: normal;\">Japan</span>"},
        {"column": "Beijing", "title": "Beijing, <span style=\"color:gray; font-weight: normal;\">China</span>"},
        {"column": "Mumbai (Bombay)", "title": "Mumbai, <span style=\"color:gray; font-weight: normal;\">India</span>"},
        {"column": "New York-Newark", "title": "New York/Newark, <span style=\"color:gray; font-weight: normal;\">U.S.</span>"},
    ],
    # Add text annotation to label the projection period
    text_annotations=[
        {
            "text": "2025",
            "x": "2023/01/01",
            "y": 30000000,
            "align": "tc",
            "color": "#b73229",
            "size": 14,
            "bold": True,
        },
    ],
    # Add range annotation to highlight projection period
    range_annotations=[
        {
            "x0": "2018/01/01",
            "x1": "2037/07/02",
            "y0": 0,
            "y1": 50000000,
            "display": "range",
            "color": "#888",
            "opacity": 18,
        },
    ],
)

# Create the chart in Datawrapper
chart.create()
```

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.MultipleColumnChart
