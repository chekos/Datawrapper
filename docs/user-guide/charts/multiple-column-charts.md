# MultipleColumnChart

This example, drawn from [Datawrapper's official documentation](https://academy.datawrapper.de/article/405-examples-of-datawrapper-multiple-column-charts), demonstrates how to create small multiple column charts showing population growth in major cities from 1950 to 2035.

<iframe title="Population of the world's largest cities, 1950 to 2035" aria-label="Multiple Columns" id="datawrapper-chart-qjyDH" src="https://datawrapper.dwcdn.net/qjyDH/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="460" data-external="1"></iframe><script type="text/javascript">window.addEventListener("message",function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r,i=0;r=e[i];i++)if(r.contentWindow===a.source){var d=a.data["datawrapper-height"][t]+"px";r.style.height=d}}});</script>

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
    # Turn off the y grid lines
    y_grid=False,
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
    # Add text annotations to label specific panels
    text_annotations=[
        # "Projection" label on Mumbai panel
        dw.MultipleColumnTextAnnotation(
            text="Projection",
            x="2018/04/30 15:23",
            y=36224085,
            dx=-21,
            dy=-8,
            plot="Mumbai (Bombay)",
            size=13,
            color="#858585",
            align=dw.TextAlign.TOP_RIGHT,
            width=37,
            connector_line=dw.ConnectorLine(
                enabled=True,
                type=dw.ConnectorLineType.STRAIGHT,
                stroke=dw.StrokeWidth.THIN,
                inherit_color=True,
                arrow_head=False,
            ),
            show_mobile=True,
            show_desktop=True,
        ),
        # "Paris 2035" label on Delhi panel
        dw.MultipleColumnTextAnnotation(
            text="Paris 2035",
            x="1947/07/03 01:00",
            y=16409201,
            dx=0,
            dy=0,
            plot="Delhi",
            size=13,
            color="#858585",
            align=dw.TextAlign.TOP_LEFT,
            width=37,
            show_mobile=True,
            show_desktop=True,
        ),
        # "2025 population: 34.7M" label on Delhi panel with HTML formatting
        dw.MultipleColumnTextAnnotation(
            text='<b style="color:#b73229">2025 population:</b>\n34.7M',
            x="2023/07/14 22:34",
            y=33128010,
            dx=-21,
            dy=-29,
            plot="Delhi",
            size=13,
            color="#494949",
            align=dw.TextAlign.TOP_RIGHT,
            outline=True,
            width=66,
            connector_line=dw.ConnectorLine(
                enabled=True,
                type=dw.ConnectorLineType.STRAIGHT,
                stroke=dw.StrokeWidth.THIN,
                inherit_color=False,
                arrow_head=False,
            ),
            show_mobile=True,
            show_desktop=True,
        ),
        # "Paris grew the most..." label on Paris panel
        dw.MultipleColumnTextAnnotation(
            text="Paris grew the most between 1851 to 1856 (by over 20%).",
            x="1947/10/03 18:05",
            y=43097373,
            dx=0,
            dy=0,
            plot="Paris",
            size=13,
            color="#494949",
            align=dw.TextAlign.TOP_LEFT,
            outline=True,
            width=66,
            show_mobile=True,
            show_desktop=True,
        ),
        # "Lagos is expected to double..." label on Lagos panel (hidden)
        dw.MultipleColumnTextAnnotation(
            text="Lagos is expected to double in size by 2035 compared to 2015.",
            x="1947/07/03 01:00",
            y=43096075,
            dx=0,
            dy=0,
            plot="Lagos",
            size=13,
            color="#494949",
            align=dw.TextAlign.TOP_LEFT,
            outline=True,
            width=72,
            show_mobile=False,
            show_desktop=False,
        ),
    ],
    # Add range annotation to highlight projection period
    range_annotations=[
        dw.MultipleColumnXRangeAnnotation(**{
            "x0": "2018/01/01",
            "x1": "2037/07/02",
            "y0": 0,
            "y1": 50000000,
            "color": "#888",
            "opacity": 18,
        }),
        dw.MultipleColumnYLineAnnotation(**{
            "y0": 11765087.7143,
            "color": "#888",
            "opacity": 76,
            "stroke_width": dw.StrokeWidth.MEDIUM,
            "stroke_type": dw.StrokeType.DOTTED,
        })
    ],
)

# Create the chart in Datawrapper
chart.create()
```

## Reference

### MultipleColumnChart

```{eval-rst}
.. parameter-table:: datawrapper.charts.MultipleColumnChart
```

### MultipleColumnTextAnnotation

```{eval-rst}
.. parameter-table:: datawrapper.charts.MultipleColumnTextAnnotation
```

### MultipleColumnRangeAnnotation

```{eval-rst}
.. parameter-table:: datawrapper.charts.MultipleColumnRangeAnnotation
```

### MultipleColumnXRangeAnnotation

```{eval-rst}
.. parameter-table:: datawrapper.charts.MultipleColumnXRangeAnnotation
```

### MultipleColumnYRangeAnnotation

```{eval-rst}
.. parameter-table:: datawrapper.charts.MultipleColumnYRangeAnnotation
```

### MultipleColumnXLineAnnotation

```{eval-rst}
.. parameter-table:: datawrapper.charts.MultipleColumnXLineAnnotation
```

### MultipleColumnYLineAnnotation

```{eval-rst}
.. parameter-table:: datawrapper.charts.MultipleColumnYLineAnnotation
```
