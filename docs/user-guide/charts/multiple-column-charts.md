# Multiple Column Charts

## Example

This example demonstrates how to create a multiple column chart showing the population of the world's largest cities from 1950 to 2035. The chart uses 8 panels (one for each city) with custom HTML-styled titles, highlights the year 2025 in red, and includes text and range annotations.

```python
import pandas as pd
import datawrapper as dw

# Load data from GitHub
url = "https://raw.githubusercontent.com/palewire/datawrapper-api-classes/main/tests/samples/multiple_column/population.csv"
df = pd.read_csv(url)

chart = dw.MultipleColumnChart(
    # Chart metadata
    title="Population of the world's largest cities, 1950 to 2035",
    # Data source attribution
    source_name="Our World in Data",
    source_url="https://ourworldindata.org/urbanization",
    # Data
    data=df,
    # Grid layout - 4 columns
    grid_column=4,
    # Fixed row height
    grid_row_height=140,
    # Y-axis format - abbreviated numbers (e.g., "10M")
    y_grid_format=dw.NumberFormat.ABBREVIATED_ONE_DECIMAL,
    # Y-axis labels inside the plot area
    y_grid_labels="inside",
    # X-axis and Y-axis grid lines off
    x_grid_display="off",
    y_grid_display="off",
    # Base color for columns
    base_color="#c9a291",
    # Highlight 2025 in red
    column_color={"2025": "#c71e1d"},
    # Category labels for legend
    category_labels={"2025": "...for 2025"},
    # Exclude all other years from the legend
    exclude_from_color_key=[
        "1950", "1955", "1960", "1965", "1970", "1975", "1980", "1985",
        "1990", "1995", "2000", "2005", "2010", "2015", "2020", "2030", "2035"
    ],
    # Hide the color key
    show_color_key=False,
    # Panel titles with HTML styling
    panel_titles={
        "Beijing": "Beijing, <span style=\"color:gray; font-weight: normal;\">China</span>",
        "Delhi": "Delhi, <span style=\"color:gray; font-weight: normal;\">India</span>",
        "Dhaka": "Dhaka, <span style=\"color:gray; font-weight: normal;\"> Bangladesh </span>",
        "Lagos": "Lagos, <span style=\"color:gray; font-weight: normal;\">Nigeria</span>",
        "Mumbai (Bombay)": "Mumbai, <span style=\"color:gray; font-weight: normal;\">India</span>",
        "New York-Newark": "New York/Newark, <span style=\"color:gray; font-weight: normal;\">U.S.</span>",
        "Paris": "Paris, <span style=\"color:gray; font-weight: normal;\">France</span>",
        "Tokyo": "Tokyo, <span style=\"color:gray; font-weight: normal;\">Japan</span>",
    },
    # Text annotations
    text_annotations=[
        # Projection label for Mumbai
        dw.TextAnnotation(
            text="Projection",
            x="2018/04/30 15:23",
            y=36224085.8571,
            plot="Mumbai (Bombay)",
            dx=-21,
            dy=-8,
            align="tr",
            size=13,
            color="#858585",
            connector_line=dw.ConnectorLine(
                type=dw.ConnectorLineType.STRAIGHT,
                stroke=dw.StrokeWidth.THIN
            )
        ),
        # Paris 2035 label
        dw.TextAnnotation(
            text="Paris 2035",
            x="1947/07/03 01:00",
            y=16409201.2857,
            plot="Delhi",
            align="tl",
            size=13,
            color="#858585"
        ),
        # Delhi 2025 population callout
        dw.TextAnnotation(
            text="<b style=\"color:#b73229\">2025 population:</b>\n34.7M",
            x="2023/07/14 22:34",
            y=33128010.1429,
            plot="Delhi",
            dx=-21,
            dy=-29,
            align="tr",
            size=13,
            color="#494949",
            bg=True,
            connector_line=dw.ConnectorLine(
                type=dw.ConnectorLineType.STRAIGHT,
                stroke=dw.StrokeWidth.THIN,
                inherit_color=False
            )
        ),
        # Paris growth note
        dw.TextAnnotation(
            text="Paris grew the most between 1851 to 1856 (by over 20%).",
            x="1947/10/03 18:05",
            y=43097373.9429,
            plot="Paris",
            align="tl",
            size=13,
            color="#494949",
            bg=True
        ),
        # Lagos projection note (hidden on mobile/desktop, shown as fallback)
        dw.TextAnnotation(
            text="Lagos is expected to double in size by 2035 compared to 2015.",
            x="1947/07/03 01:00",
            y=43096075.7522,
            plot="Lagos",
            align="tl",
            size=13,
            color="#494949",
            bg=True,
            show_mobile=False,
            show_desktop=False
        ),
    ],
    # Range annotations
    range_annotations=[
        # Horizontal line in Paris panel
        dw.RangeAnnotation(
            x0="2009/01/23 14:50",
            x1="2009/01/23 14:50",
            y0=11765087.7143,
            y1=13622733.1429,
            plot="Paris",
            range_type="y",
            display="line",
            color="#888",
            opacity=76,
            stroke_type="dotted",
            stroke_width=2,
            show_in_all_plots=True
        ),
        # Shaded projection period in Mumbai panel
        dw.RangeAnnotation(
            x0="2018/01/01 13:22",
            x1="2037/07/02 01:00",
            y0=26626251.1429,
            y1=27245466.2857,
            plot="Mumbai (Bombay)",
            range_type="x",
            display="range",
            color="#888",
            opacity=18,
            show_in_all_plots=True
        ),
    ],
)

chart.create()
```

<iframe title="Population of the world's largest cities, 1950 to 2035" aria-label="Multiple Columns" id="datawrapper-chart-ZEBmw" src="https://datawrapper.dwcdn.net/ZEBmw/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="460" data-external="1"></iframe><script type="text/javascript">!function(){"use strict";window.addEventListener("message",(function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r=0;r<e.length;r++)if(e[r].contentWindow===a.source){var i=a.data["datawrapper-height"][t]+"px";e[r].style.height=i}}}))}();
</script>

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.MultipleColumnChart
