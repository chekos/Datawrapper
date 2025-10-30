# ScatterPlot

This example, drawn from [Datawrapper's official documentation](https://www.datawrapper.de/charts/scatter-plot), demonstrates how to create a scatter plot.

<iframe title="Every country has a higher life expectancy now than in 1800" aria-label="Scatter Plot" id="datawrapper-chart-O4zib" src="https://datawrapper.dwcdn.net/O4zib/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="731" data-external="1"></iframe><script type="text/javascript">window.addEventListener("message",function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r,i=0;r=e[i];i++)if(r.contentWindow===a.source){var d=a.data["datawrapper-height"][t]+"px";r.style.height=d}}});</script>

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
    x_column="gdp",
    y_column="health",
    size_column="population",
    color_column="countries",
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
    max_size=71.09,
    # Set opacity for better visibility of overlapping bubbles
    opacity=0.97,
    # Set base color for all points
    base_color="#afafaf",
    # Configure color categories for specific countries
    color_category={
        "China": "#ae000b",
        "India": "#15607a",
        "Somalia": "#c86300",
        "United States": "#976f3a",
    },
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
    <td><b>{{ gdp }} Dollar</b></td>
  </b>
</tr>
</table>""",
    # Add custom lines connecting 1800 and 2015 data points for each country
    custom_lines="""220,1.5,220,45,1000000,45,1000000,1.5 @color:grey @opacity:0.1
220,46,220,92,1000000,92,1000000,46 @color:grey @opacity:0.1
1925,53.8,603,28.21@color:grey @opacity:0.1
10620,78,667,35.4@color:grey @opacity:0.1
13434,76.4,716,28.82@color:grey @opacity:0.1
7615,59.6,618,26.98@color:grey @opacity:0.1
21049,76.4,757,33.54@color:grey @opacity:0.1
17344,76.5,1507,33.2@color:grey @opacity:0.1
7763,74.7,514,34@color:grey @opacity:0.1
37138,75.72,833,34.42@color:grey @opacity:0.1
44056,82.3,815,34.05@color:grey @opacity:0.1
44401,81.3,1848,34.4@color:grey @opacity:0.1
16986,72.9,775,29.17@color:grey @opacity:0.1
22818,73.7,1445,35.18@color:grey @opacity:0.1
44138,79.1,1235,30.3@color:grey @opacity:0.1
3161,70.4,876,25.5@color:grey @opacity:0.1
12984,75.7,913,32.12@color:grey @opacity:0.1
17415,71,608,36.2@color:grey @opacity:0.1
41240,80.5,2412,40@color:grey @opacity:0.1
8501,71.7,579,26.5@color:grey @opacity:0.1
1830,62.3,597,31@color:grey @opacity:0.1
7983,72.7,629,28.8@color:grey @opacity:0.1
6295,73.2,854,33@color:grey @opacity:0.1
9833,78.9,669,35.1@color:grey @opacity:0.1
17196,58.7,397,33.6@color:grey @opacity:0.1
15441,74.4,1109,32@color:grey @opacity:0.1
73003,77.1,1512,29.2@color:grey @opacity:0.1
16371,74.8,1089,35.8@color:grey @opacity:0.1
1654,60.9,480,29.2@color:grey @opacity:0.1
777,61.4,418,31.5@color:grey @opacity:0.1
3267,69.4,903,35@color:grey @opacity:0.1
2897,59.4,626,28.75@color:grey @opacity:0.1
43294,81.7,1314,39@color:grey @opacity:0.1
6514,72.9,529,33.8@color:grey @opacity:0.1
599,49.6,424,30@color:grey @opacity:0.1
2191,57.4,418,30.9@color:grey @opacity:0.1
22465,79.4,1026,32@color:grey @opacity:0.1
13334,76.2,985,32@color:#B10615 @width:2
12761,78,963,32@color:grey @opacity:0.1
1472,68.1,696,32.1@color:grey @opacity:0.1
809,60.8,485,31.6@color:grey @opacity:0.1
6220,61.5,575,32.7@color:grey @opacity:0.1
14132,80.3,775,30.21@color:grey @opacity:0.1
3491,59.1,812,31.16@color:grey @opacity:0.1
21291,78.2,864,32.2@color:grey @opacity:0.1
29797,81.8,853,38.5@color:grey @opacity:0.1
29437,78.8,1915,34.95@color:grey @opacity:0.1
43495,80.4,2013,37.41@color:grey @opacity:0.1
3139,63.8,752,29.9@color:grey @opacity:0.1
12837,75.3,667,29.9@color:grey @opacity:0.1
10996,75.9,529,32.9@color:grey @opacity:0.1
11031,71.5,791,33@color:grey @opacity:0.1
7776,74.9,974,28.7@color:grey @opacity:0.1
31087,61,356,29.8@color:grey @opacity:0.1
1129,60.7,532,30.2@color:grey @opacity:0.1
26812,77.8,938,36.14@color:grey @opacity:0.1
1520,65.2,523,29.7@color:grey @opacity:0.1
7925,65.8,785,26.1@color:grey @opacity:0.1
38923,80.9,1244,36.57@color:grey @opacity:0.1
37599,81.8,1803,33.97@color:grey @opacity:0.1
18627,65.9,390,30.6@color:grey @opacity:0.1
1644,68.1,813,28.8@color:grey @opacity:0.1
7474,72.9,543,31.87@color:grey @opacity:0.1
44053,80.8,1639,38.37@color:grey @opacity:0.1
4099,65.3,696,28@color:grey @opacity:0.1
25430,81,1371,36.6@color:grey @opacity:0.1
27763,72.1,393,33.87@color:grey @opacity:0.1
11593,71.5,959,31.4@color:grey @opacity:0.1
7279,72.6,857,25.8@color:grey @opacity:0.1
1225,59.1,450,29.5@color:grey @opacity:0.1
1386,55.6,777,32@color:grey @opacity:0.1
6816,66.8,1214,31.12@color:grey @opacity:0.1
1710,64.3,633,29@color:grey @opacity:0.1
4270,73,675,33.9@color:grey @opacity:0.1
53874,83.73,1007,34.9@color:grey @opacity:0.1
24200,76.7,1249,36@color:grey @opacity:0.1
42182,83.3,926,42.85@color:grey @opacity:0.1
5903,67.2,1052,25.44@color:#1A637B @width:2
10504,71.1,994,30@color:grey @opacity:0.1
15573,74.6,977,25.6@color:grey @opacity:0.1
14646,67.4,970,31.2@color:grey @opacity:0.1
47758,81.7,1447,38.3@color:grey @opacity:0.1
31590,82.1,879,32@color:grey @opacity:0.1
33297,82.2,2225,29.69@color:grey @opacity:0.1
8606,75,1170,34.2@color:grey @opacity:0.1
36162,83.2,1050,36.4@color:grey @opacity:0.1
11752,78.5,976,31.7@color:grey @opacity:0.1
23468,70.2,1140,26.2@color:grey @opacity:0.1
2898,65.1,854,25.5@color:grey @opacity:0.1
1824,63,551,24.9@color:grey @opacity:0.1
82633,80.3,1097,26@color:grey @opacity:0.1
3245,69.8,508,23.94@color:grey @opacity:0.1
5212,67.1,864,31.9@color:grey @opacity:0.1
23282,75.4,751,33@color:grey @opacity:0.1
17050,78.9,1081,29.7@color:grey @opacity:0.1
2598,47.1,393,32.8@color:grey @opacity:0.1
958,63.2,797,31.1@color:grey @opacity:0.1
17261,74.1,1050,33.1@color:grey @opacity:0.1
26665,75.2,1270,28.9@color:grey @opacity:0.1
88314,82.2,1453,36.9@color:grey @opacity:0.1
148374,80.82,992,34.7@color:grey @opacity:0.1
12547,76.5,690,36.1@color:grey @opacity:0.1
1400,63.5,573,30.5@color:grey @opacity:0.1
799,60.5,350,30.3@color:grey @opacity:0.1
24320,75.3,997,30.6@color:grey @opacity:0.1
14408,80,842,32.65@color:grey @opacity:0.1
1684,60.2,603,26.41@color:grey @opacity:0.1
30265,82.1,781,28.7@color:grey @opacity:0.1
3877,69.7,527,32@color:grey @opacity:0.1
18350,74.5,940,28.7@color:grey @opacity:0.1
16850,75.9,1379,26.9@color:grey @opacity:0.1
3510,68.9,518,26.7@color:grey @opacity:0.1
4896,73.9,621,33.15@color:grey @opacity:0.1
11819,67.1,592,31.8@color:grey @opacity:0.1
14833,77.2,1057,35.4@color:grey @opacity:0.1
7319,74.6,715,33.1@color:grey @opacity:0.1
1176,57.1,390,30.28@color:grey @opacity:0.1
4012,68,840,30.8@color:grey @opacity:0.1
10040,64.2,540,32.4@color:grey @opacity:0.1
2352,69.7,654,32.8@color:grey @opacity:0.1
45784,81.3,4235,39.86@color:grey @opacity:0.1
34186,81.4,658,34.05@color:grey @opacity:0.1
4712,78,973,25.4@color:grey @opacity:0.1
943,61,446,30.8@color:grey @opacity:0.1
5727,64.6,851,30.4@color:grey @opacity:0.1
1390,72.1,579,26@color:grey @opacity:0.1
64304,82,1278,37.92@color:grey @opacity:0.1
48226,77.2,915,32.3@color:grey @opacity:0.1
4743,65.9,1021,25.8@color:grey @opacity:0.1
20485,78.2,847,32.9@color:grey @opacity:0.1
2529,60.9,546,31.5@color:grey @opacity:0.1
8219,74.4,835,35.5@color:grey @opacity:0.1
11903,79.5,1204,35.7@color:grey @opacity:0.1
6876,71,962,30.9@color:grey @opacity:0.1
24787,77.6,1213,35.9@color:grey @opacity:0.1
26437,80.8,1685,35.6@color:grey @opacity:0.1
33604,78.5,1375,30.43@color:grey @opacity:0.1
132877,79.7,1097,30.8@color:grey @opacity:0.1
19203,75.2,815,35.7@color:grey @opacity:0.1
23038,71,1430,29.57@color:grey @opacity:0.1
1549,65.9,431,31.8@color:grey @opacity:0.1
5558,73.2,1400,25.4@color:grey @opacity:0.1
3003,68,850,31@color:grey @opacity:0.1
52469,79.5,846,32.1@color:grey @opacity:0.1
2251,65.3,497,25.2@color:grey @opacity:0.1
12908,76.2,1358,35.5@color:grey @opacity:0.1
25684,74.1,792,37@color:grey @opacity:0.1
2085,57.1,734,25.1@color:grey @opacity:0.1
80794,82,1021,29.1@color:grey @opacity:0.1
27204,77.6,1427,36.4@color:grey @opacity:0.1
28550,80.9,1409,36.6@color:grey @opacity:0.1
2047,64,363,25.1@color:grey @opacity:0.1
624,54.2,694,29.4@color:#CA670D @width:2
12509,61.3,1480,33.5@color:grey @opacity:0.1
34644,81,576,25.8@color:grey @opacity:0.1
3047,56.1,507,26.67@color:grey @opacity:0.1
32979,82.6,1518,29.5@color:grey @opacity:0.1
10624,77.6,898,32.6@color:grey @opacity:0.1
9997,74.8,874,28.01@color:grey @opacity:0.1
10435,71.2,838,25.99@color:grey @opacity:0.1
3975,67.5,518,31.4@color:grey @opacity:0.1
17125,72,1636,32.9@color:grey @opacity:0.1
6095,51.8,490,32.3@color:grey @opacity:0.1
44892,82.1,1414,32.16@color:grey @opacity:0.1
56118,83,2701,38@color:grey @opacity:0.1
4637,68.2,1081,31.1@color:grey @opacity:0.1
42948,79.5,996,28.3@color:grey @opacity:0.1
2582,72.4,556,24.24@color:grey @opacity:0.1
2571,64.1,562,32.2@color:grey @opacity:0.1
14512,74.7,931,30.4@color:grey @opacity:0.1
2086,72.4,521,28.95@color:grey @opacity:0.1
1433,61.5,682,31.3@color:grey @opacity:0.1
5069,71.5,663,28.2@color:grey @opacity:0.1
30113,72.4,1230,32.9@color:grey @opacity:0.1
11126,77.6,716,28.8@color:grey @opacity:0.1
19360,79.2,1221,35@color:grey @opacity:0.1
15865,70,943,24@color:grey @opacity:0.1
1680,61.3,464,25.3@color:grey @opacity:0.1
8449,71.5,763,36.6@color:grey @opacity:0.1
60749,75.4,998,30.7@color:grey @opacity:0.1
38225,81,3431,38.65@color:grey @opacity:0.1
53354,79.1,2128,39.41@color:#9A7340 @width:2
20438,76.8,1758,32.9@color:grey @opacity:0.1
5598,71.8,502,26.93@color:grey @opacity:0.1
2912,64.9,585,24.3@color:grey @opacity:0.1
15753,74.8,682,32.2@color:grey @opacity:0.1
5623,75.4,861,32@color:grey @opacity:0.1
4319,74.6,1220,32.1@color:grey @opacity:0.1
3887,66,877,23.39@color:grey @opacity:0.1
4034,56.7,663,32.6@color:grey @opacity:0.1
1801,59.3,869,33.7@color:grey @opacity:0.1""",
    # Add text annotations to label years and key countries
    text_annotations=[
        dw.TextAnnotation(
            text="1800",
            x=156700,
            y=45,
            align="tr",
            dx=-14,
            dy=13,
            bold=True,
            size=22,
            color="#000000",
            outline=False,
        ),
        dw.TextAnnotation(
            text="2015",
            x=156700,
            y=92,
            align="tr",
            dx=-14,
            dy=13,
            bold=True,
            size=22,
            color="#000000",
            outline=False,
        ),
        dw.TextAnnotation(
            text="China",
            x="13398.7010",
            y="76.1317",
            align="mc",
            color="#efefef",
            size=13,
            outline=False,
        ),
        dw.TextAnnotation(
            text="India",
            x="5997.2352",
            y="67.2308",
            align="mc",
            color="#efefef",
            size=13,
            outline=False,
        ),
        dw.TextAnnotation(
            text="Somalia",
            x=620,
            y=55.5,
            align="tl",
            dx=10,
            dy=-1,
            color="#983c00",
            size=13,
            outline=False,
        ),
        dw.TextAnnotation(
            text="US",
            x="53787.2503",
            y="79.0931",
            align="mc",
            color="#efefef",
            size=13,
            outline=False,
        ),
    ],
)

# Create the chart in Datawrapper
chart.create()
```

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.ScatterPlot
```
