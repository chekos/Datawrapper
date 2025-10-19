# Scatter Plots

## Example

This example recreates a scatter plot showing student cities in Germany, with dynamic sizing based on the number of students and color-coded by the share of students in the population.

```python
import pandas as pd
import datawrapper as dw

# Load data from GitHub
df = pd.read_csv(
    "https://raw.githubusercontent.com/palewire/Datawrapper/main/tests/samples/scatter/german-students.csv"
)

# Create scatter plot
chart = dw.ScatterPlot(
    # Chart title
    title="What are the student cities in Germany?",
    # Intro text with HTML formatting
    intro="There were 2.807.000 students in Germany in 2016. Where were they based, and which cities had the highest share of students? <b>The size of the circle represents the number of students in these cities. The darker the circle, the higher the share of students.</b>",
    # Data source attribution
    source_name="Eurostat 2016",
    source_url="https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Statistics_on_European_cities/de#Bildung_und_Besch.C3.A4ftigung",
    # Byline
    byline="Lisa Charlotte Muth, Datawrapper",
    # Data
    data=df,
    # X-axis: Number of students
    x_column="students",
    # Y-axis: Share of students in %
    y_column="percent",
    # Size: Dynamic sizing based on number of students
    size_column="students",
    # Color: Color by student percentage category
    color_column="color",
    # Labels: City names
    label_column="city",
    # X-axis range
    x_axis_min=0,
    x_axis_max=200000,
    # Y-axis range
    y_axis_min=0,
    y_axis_max=52,
    # X-axis format (abbreviated numbers)
    x_grid_format=dw.NumberFormat.ABBREVIATED,
    # Y-axis format (integer)
    y_grid_format=dw.NumberFormat.INTEGER,
    # X-axis grid lines
    x_grid_lines=dw.ScatterGridLines.ON,
    # Y-axis grid lines
    y_grid_lines=dw.ScatterGridLines.ON,
    # Color category mapping for student percentage ranges
    color_category={
        "less than 5%": "#A8DA9B",
        "5-10%": "#96C797",
        "10%-20%": "#78AA91",
        "more than 20%": "#406274",
    },
    # Category order for legend
    category_order=["less than 5%", "5-10%", "10%-20%", "more than 20%"],
    # Show color legend
    show_color_key=True,
    # Dynamic point sizing
    size_mode="dynamic",
    # Maximum point size
    max_size=33.85,
    # Custom tooltip with HTML table
    tooltip_title="<big>{{ city }}</big>",
    tooltip_body='<table>\n  <tr>\n    <td>Population: &emsp; </td>\n    <td>Students:</td>\n  </tr>\n  <tr>\n    <td><b>{{ pop }}</b></td>\n  </b>\n    <td><b>{{ students }}</b></td>\n</tr>\n</table>\n<hr>\n<big><b>{{ percent }}% of the population are students.</big></b>',
    # Enable tooltips
    tooltip_enabled=True,
    # Plot height (fixed)
    plot_height=357,
    # Text annotations for axis labels
    text_annotations=[
        dw.TextAnnotation(
            # Label for Y-axis
            text="↑\nhigher share \nof students",
            x=146367.9122,
            y=41.1759,
            align="br",
            bold=True,
            size=14,
        ),
        dw.TextAnnotation(
            # Label for X-axis
            text="more \nstudents\nlive in these \ncities\n→",
            x=153803.5969,
            y=38.7234,
            align="tl",
            bold=True,
            size=14,
        ),
    ],
)

# Create the chart
chart.create()
```

<iframe title="What are the student cities in Germany?" aria-label="Scatter Plot" id="datawrapper-chart-GQDw3" src="https://datawrapper.dwcdn.net/GQDw3/10/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="534" data-external="1"></iframe><script type="text/javascript">!function(){"use strict";window.addEventListener("message",(function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r=0;r<e.length;r++)if(e[r].contentWindow===a.source){var i=a.data["datawrapper-height"][t]+"px";e[r].style.height=i}}}))}();
</script>

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.ScatterPlot
