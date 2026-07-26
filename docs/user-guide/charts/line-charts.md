# LineChart

This example, drawn from <a href="https://www.datawrapper.de/charts/lines">the Datawrapper documentation</a>, demonstrates how to create a line chart with a shaded confidence interval around the line.

<iframe title="Global land temperature in July, 1753-2015" aria-label="Line chart" id="datawrapper-chart-9Qlvu" src="https://datawrapper.dwcdn.net/9Qlvu/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="400" data-external="1"></iframe><script type="text/javascript">window.addEventListener("message",function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r,i=0;r=e[i];i++)if(r.contentWindow===a.source){var d=a.data["datawrapper-height"][t]+"px";r.style.height=d}}});</script>

```python
import pandas as pd
import datawrapper as dw

# Load temperature data from GitHub
url = "https://raw.githubusercontent.com/chekos/datawrapper/main/tests/samples/line/land-temps.csv"
df = pd.read_csv(url)

chart = dw.LineChart(
    # Chart title
    title="Global land temperature in July, 1753-2015",
    # Data source attribution
    source_name="Berkeley Earth",
    source_url="http://berkeleyearth.org/data/",
    # Data from pandas DataFrame
    data=df,
    # Set the suffix on our values
    transformations=dw.Transform(
        column_format=[
            dw.ColumnFormat(
                column="LandAverageTemperature",
                number_append=" °C",
            )
        ]
    ),
    # Set the range
    custom_range_y=[8, 21],
    # Format Y-axis grid labels with no decimal places
    y_grid_format="0",
    # And now the tooltip with a bit more...
    tooltip_number_format="00.00",
    tooltip_x_format="YYYY",
    lines=[
        # Style the main line. The color argument is a line-centric
        # convenience for the chart's color_category map.
        dw.Line(
            column="LandAverageTemperature",
            color="#1d81a2",
            width=dw.LineWidth.THIN,
            interpolation=dw.LineInterpolation.CURVED,
        ),
        # Hide the other two
        dw.Line(
            column="lower",
            width=dw.LineWidth.INVISIBLE,
        ),
        dw.Line(
            column="upper",
            width=dw.LineWidth.INVISIBLE,
        ),
    ],
    # Add shaded confidence interval area
    area_fills=[
        dw.AreaFill(
            from_column="lower",
            to_column="upper",
            color="#cccccc",
            opacity=0.45,
        )
    ],
)

chart.create()
```

You can also keep colors in the legacy chart-level mapping when that better fits
existing code or shared category settings:

```python
chart = dw.LineChart(
    data=df,
    color_category={"LandAverageTemperature": "#1d81a2"},
    lines=[dw.Line(column="LandAverageTemperature", width=dw.LineWidth.THIN)],
)
```

`Line(color=...)` and `LineChart(color_category=...)` serialize to the same
Datawrapper `color-category` metadata. If both are provided for the same line,
the colors must match; conflicting values raise an error instead of silently
choosing one.

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.LineChart
