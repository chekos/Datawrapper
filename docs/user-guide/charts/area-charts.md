# AreaChart

This example, drawn from [Datawrapper's official documentation](https://www.datawrapper.de/charts/area), demonstrates how to create a stacked area chart. The chart includes text and range annotations to highlight significant events. It also customizes the color scheme for different regions and formats the axes and value labels for better readability.

<iframe title="Migration to the US by world region, 1820-2009" aria-label="Area Chart" id="datawrapper-chart-sBGlG" src="https://datawrapper.dwcdn.net/sBGlG/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none; margin-bottom: 20px" height="400" data-external="1"></iframe><script type="text/javascript">window.addEventListener("message",function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r,i=0;r=e[i];i++)if(r.contentWindow===a.source){var d=a.data["datawrapper-height"][t]+"px";r.style.height=d}}});</script>

```python
import pandas as pd
import datawrapper as dw

# Load migration data from GitHub
df = pd.read_csv(
    "https://raw.githubusercontent.com/chekos/Datawrapper/main/tests/samples/area/migration.csv"
)

chart = dw.AreaChart(
    # The headline of the chart
    title="Migration to the US by world region, 1820-2009",
    # Introductory text explaining the data
    intro="The numbers are recorded by decade. For example, the numbers recorded for 1905 tell us the number of immigrants between 1900 and 1910.",
    # Data source attribution below the chart
    source_name="Department of Homeland Security",
    # URL to the original data source, linked in the chart's source attribution
    source_url="http://metrocosm.com/wp-content/uploads/2016/05/usa-immigration-data.xlsx",
    # Attribute of the author below the chart
    byline="Mirko Lorenz",
    # The DataFrame containing the source data
    data=df,
    # Transpose the data with a transformation
    transformations=dict(transpose=True),
    # Format x-axis labels as full years (e.g., "2020").
    # Alternatively, you could provide "YYYY" if you'd rather not use the DateFormat enum.
    x_grid_format=dw.DateFormat.YEAR_FULL,
    # Format y-axis labels with abbreviated numbers (e.g., "1.2m")
    # Alternatively, you could provide "0.[00]a" if you'd rather not use the NumberFormat enum.
    y_grid_format=dw.NumberFormat.ABBREVIATED_TWO_DECIMALS,
    # Align the y-axis labels to the right
    y_grid_label_align="right",
    # We always want the decimals for the tooltip number, but otherwise the same
    tooltip_number_format="0.00a",
    # Whether to stack the areas on top of each other
    stack_areas=True,
    # Use smooth curves between data points
    interpolation=dw.LineInterpolation.CURVED,
    # Set fixed plot height in pixels
    plot_height_fixed=388,
    # Map each region/country to a specific color
    color_category={
        "Austria-Hungary": "#1d81a2",
        "Germany": "#004765",
        "Ireland": "#3a96b8",
        "Italy": "#48adc0",
        "Norway and Sweden": "#2b8589",
        "Russia": "#329a9b",
        "United Kingdom": "#257085",
        "Rest of Europe": "#005d71",
        "Europe": "#00658d",
        "China": "#b4241c",
        "India": "#cd3d2e",
        "Philippines": "#dc464b",
        "Rest of Asia": "#E65340",
        "Asia": "#e65341",
        "Canada and Newfoundland": "#ffa126",
        "Mexico": "#ffca76",
        "Caribbean": "#ffe59c",
        "Central America": "#ffdc6b",
        "South America": "#ffbb7f",
        "Rest of America": "#fffbb1",
        "Africa": "#009a69",
        "Oceania": "#003f65",
        "Not Specified": "#181818",
    },
    # Text annotations to label regions and events
    text_annotations=[
        dw.TextAnnotation(
            text="E U R O P E",
            x="1896/07/27 16:00",
            y=1329923.3141,
            align="mc",
            color="#fefefe",
            bold=True,
            size=20,
            outline=False,
        ),
        dw.TextAnnotation(
            text="A S I A ",
            x="2000M5",
            y=2500000,
            align="mr",
            color="#121212",
            bold=True,
            size=14,
            outline=False,
        ),
        dw.TextAnnotation(
            text="A M E -\nR I C A",
            x="1994/08/01 20:41",
            y=6134172.0713,
            align="mc",
            color="#222222",
            bold=True,
            size=10,
            outline=False,
        ),
        dw.TextAnnotation(
            text="Germany",
            x="1851/01/04 01:21",
            y=439746.2628,
            align="ml",
            color="#d2d2d2",
            italic=True,
            size=11,
            outline=False,
        ),
        dw.TextAnnotation(
            text="World <br/>War I",
            x="1914M07",
            y=8000000.000000002,
            align="tl",
            dx=3,
            color="#575757",
            italic=True,
            size=11,
            outline=False,
        ),
        dw.TextAnnotation(
            text="World <br/>War II",
            x="1939M09",
            y=3000000.000000002,
            align="tl",
            dx=3,
            color="#575757",
            italic=True,
            size=11,
            outline=False,
        ),
    ],
    range_annotations=[
        # World War I period (1914-1918)
        dw.RangeAnnotation(
            x0="1914M07",
            x1="1918M11",
            color="#333333",
            opacity=14,
        ),
        # World War II period (1939-1945)
        dw.RangeAnnotation(
            x0="1939M09",
            x1="1945M09",
            color="#333333",
            opacity=10,
        ),
    ],
)

# Create the chart in Datawrapper
chart.create()
```

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.AreaChart
