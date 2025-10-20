# ColumnChart

This example, drawn from <a href="https://www.datawrapper.de/charts/column">the Datawrapper documentation</a>, demonstrates how to customize a column chart with annotations and custom colors.

<iframe title="U.S. unemployment rate" aria-label="Column Chart" id="datawrapper-chart-smskc" src="https://datawrapper.dwcdn.net/smskc/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="400" data-external="1"></iframe><script type="text/javascript">window.addEventListener("message",function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r,i=0;r=e[i];i++)if(r.contentWindow===a.source){var d=a.data["datawrapper-height"][t]+"px";r.style.height=d}}});</script>

```python
import pandas as pd
import datawrapper as dw

# Load unemployment data from GitHub
url = "https://raw.githubusercontent.com/chekos/datawrapper/main/tests/samples/column/unemployment.csv"
df = pd.read_csv(url)

chart = dw.ColumnChart(
    # Chart headline
    title="U.S. unemployment rate",
    # Introductory text
    intro="January 2016-September 2020",
    # Data source attribution
    source_name="U.S. Bureau of Labor Statistics",
    source_url="https://www.bls.gov/",
    # Data from pandas DataFrame
    data=df,
    # Format labels with one decimal place and a percentage sign
    y_grid_format=dw.NumberFormat.PERCENT_UP_TO_ONE_DECIMAL,
    value_labels_format=dw.NumberFormat.PERCENT_UP_TO_ONE_DECIMAL,
    # Highlight specific columns with custom colors
    base_color="#CCCCCC",
    color_category={
        "2020/04": "rgb(21, 96, 122)",
        "2020/05": "rgb(21, 96, 122)",
        "2020/06": "rgb(21, 96, 122)",
        "2020/07": "rgb(21, 96, 122)",
        "2020/08": "rgb(21, 96, 122)",
        "2020/09": "rgb(21, 96, 122)",
    },
    # Annotations to highlight the COVID-19 period
    range_annotations=[
        dw.RangeAnnotation(
            x0="2020/01/01",
            x1="2020/09/30",
            color="#777777",
            opacity=10,
            type="x",
        )
    ],
    text_annotations=[
        dw.TextAnnotation(
            x="2020/04/01",
            y=14,
            dx=-50,
            dy=50,
            text="In <b>April 2020</b>, the unemployment rate rose to almost <b>15%</b>.",
            align="tr",
            size=14,
            color="rgb(21, 96, 122)",
            connector_line=dw.ConnectorLine(
                color="rgb(21, 96, 122)",
                type=dw.ConnectorLineType.CURVE_RIGHT,
            ),
        )
    ],
)

chart.create()
```

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.ColumnChart
