# ScatterPlot

This example, drawn from [Datawrapper's official documentation](https://www.datawrapper.de/charts/scatter-plot), demonstrates how to create a scatter plot showing the relationship between GDP per capita and life expectancy over time. The chart uses bubble size to represent population and features text annotations to label specific countries and years.

<iframe title="Every country has a higher life expectancy now than in 1800" aria-label="Scatter Plot" id="datawrapper-chart-g9N3W" src="https://datawrapper.dwcdn.net/g9N3W/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="731" data-external="1"></iframe><script type="text/javascript">window.addEventListener("message",function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r,i=0;r=e[i];i++)if(r.contentWindow===a.source){var d=a.data["datawrapper-height"][t]+"px";r.style.height=d}}});</script>

```python
import pandas as pd
import datawrapper as dw

# Load life expectancy data from GitHub
df = pd.read_csv(
    "https://raw.githubusercontent.com/chekos/Datawrapper/main/tests/samples/scatter/life-expectancy.csv",
    sep="\t"
)

chart = dw.ScatterPlot(
    # Chart title
    title="Every country has a higher life expectancy now than in 1800",
    # Introductory text explaining the visualization
    intro="Gross domestic product per person adjusted for differences in purchasing power (in international 2011 dollars) vs life expectacy of newborns, for selected countries in 1800 and 2015. The size of the circle shows the population of the countries.",
    # Data source attribution
    source_name="Gapminder",
    source_url="https://www.gapminder.org/data/",
    # Author credit
    byline="Lisa Charlotte Muth, Datawrapper",
    # Data from pandas DataFrame
    data=df,
    # Define which columns to use for each dimension
    x_column="GPD",
    y_column="Health",
    size_column="population",
    label_column="country",
    # Use logarithmic scale for x-axis (GDP)
    x_log=True,
    # Set custom range for axes
    x_range=[200, ""],
    y_range=[0, 94],
    # Format axis labels
    x_format="0a",  # Abbreviated format (e.g., "10k")
    y_format="0a",
    # Configure bubble size
    size="dynamic",
    max_size=60,
    # Set opacity for better visibility of overlapping bubbles
    opacity=0.6,
    # Set base color for all points
    base_color="#15607a",
    # Set fixed plot height
    plot_height_fixed=581,
    # Disable automatic labeling (we'll add custom text annotations)
    auto_labels=False,
    # Custom tooltip format
    tooltip_title='<big>{{ country }}</big> in <big>{{ FORMAT(year, "YYYY") }}</big>',
    tooltip_body="""<table>
  <tr>
    <td>Life expectancy: &emsp; </td>
    <td>GDP per capita:</td>
  </tr>
  <tr>
    <td><b>{{ health }} years</b></td>
    <td><b>{{ FORMAT(gdp, "0,0") }} Int'l$</b></td>
  </tr>
</table>""",
    # Add text annotations to label years and key countries
    text_annotations=[
        {
            "text": "1800",
            "x": 156700,
            "y": 45,
            "align": "tr",
            "dx": -14,
            "dy": 13,
            "bold": True,
            "size": 18,
        },
        {
            "text": "2015",
            "x": 156700,
            "y": 92,
            "align": "tr",
            "dx": -14,
            "dy": 13,
            "bold": True,
            "size": 18,
        },
        {
            "text": "China",
            "x": "13398.7010",
            "y": "76.1317",
            "align": "mc",
            "color": "#000000",
            "size": 13,
        },
        {
            "text": "India",
            "x": "5997.2352",
            "y": "67.2308",
            "align": "mc",
            "color": "#000000",
            "size": 13,
        },
        {
            "text": "Somalia",
            "x": 620,
            "y": 55.5,
            "align": "tl",
            "dx": 10,
            "dy": -1,
            "color": "#000000",
            "size": 13,
        },
        {
            "text": "US",
            "x": "53787.2503",
            "y": "79.0931",
            "align": "mc",
            "color": "#000000",
            "size": 13,
        },
    ],
)

# Create the chart in Datawrapper
chart.create()
```

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.ScatterPlot
