# BarChart

This example, drawn from <a href="https://academy.datawrapper.de/article/412-examples-of-datawrapper-bar-charts">the Datawrapper documentation</a>, recreates a bar chart showing custom colors and a confidence interval using a bar overlay.

<iframe title="Score of Happiness" aria-label="Bar Chart" id="datawrapper-chart-Fk2y7" src="https://datawrapper.dwcdn.net/Fk2y7/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none; margin-bottom: 20px;" height="400" data-external="1"></iframe><script type="text/javascript">window.addEventListener("message",function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r,i=0;r=e[i];i++)if(r.contentWindow===a.source){var d=a.data["datawrapper-height"][t]+"px";r.style.height=d}}});</script>

```python
import pandas as pd
import datawrapper as dw

# Load data from GitHub
url = "https://raw.githubusercontent.com/chekos/datawrapper/main/tests/samples/bar/happiness-scores.csv"
df = pd.read_csv(url)

# Create the bar chart
chart = dw.BarChart(
    # Chart title with HTML formatting
    title="Score of Happiness<br>",
    # Source information
    source_name="World Happiness Report 2019",
    source_url="https://worldhappiness.report/ed/2019/changing-world-happiness/",
    # Intro text explaining the ranking methodology
    intro="The ranking is based on life evaluations (the average answer to the question how people evaluate the quality of their current lives on a scale of 0 to 10) for each country, averaged over the years 2016-2018.",
    # Byline
    byline="Daniela Haake",
    # Data
    data=df,
    # Value label format using enum
    value_label_format=dw.NumberFormat.THOUSANDS_WITH_OPTIONAL_DECIMALS,
    # Show value labels
    show_value_labels=True,
    # Value label alignment
    value_label_alignment="left",
    # Don't sort bars (keep original order)
    sort_bars=False,
    # Color by continent with custom mapping
    show_color_key=True,
    color_column="Continent",
    color_category={
        "Asia": "#ec6951",
        "Africa": "#8c1946",
        "Europe": "#ff9f51",
        "Oceania": "#e7d5c2",
        "3. Norway": "#f7d503",
        "7. Sweden": "#f7d503",
        "9. Canada": "#ef7f35",
        "93. China": "#c2c101",
        "1. Finland": "#f7d503",
        "140. India": "#c2c101",
        "147. Haiti": "#ef7f35",
        "149. Syria": "#c2c101",
        "151. Yemen": "#c2c101",
        "2. Denmark": "#f7d503",
        "4. Iceland": "#f7d503",
        "68. Russia": "#c2c101",
        "95. Bhutan": "#c2c101",
        "10. Austria": "#f7d503",
        "150. Malawi": "#2c7f67",
        "152. Rwanda": "#2c7f67",
        "17. Germany": "#f7d503",
        "148. Botswana": "#2c7f67",
        "153. Tanzania": "#2c7f67",
        "North America": "#e7d5c2",
        "5. Netherlands": "#f7d503",
        "6. Switzerland": "#f7d503",
        "8. New Zealand": "#ae5b3e",
        "154. Afghanistan": "#c2c101",
        "156. South Sudan": "#2c7f67",
        "19. United States": "#ef7f35",
        "15. United Kingdom": "#f7d503",
        "155. Central African Republic": "#2c7f67"
    },
    # Category labels for the legend
    label_column="Country",
    category_labels={
        "1. Finland": "Europe",
        "2. Denmark": "Europe",
        "3. Norway": "Europe",
        "4. Iceland": "Europe",
        "5. Netherlands": "Europe",
        "6. Switzerland": "Europe",
        "7. Sweden": "Europe",
        "8. New Zealand": "Oceania",
        "9. Canada": "North America",
        "10. Austria": "Europe",
        "15. United Kingdom": "Europe",
        "17. Germany": "Europe",
        "19. United States": "North America",
        "68. Russia": "Asia",
        "93. China": "Asia",
        "95. Bhutan": "Asia",
        "140. India": "Asia",
        "147. Haiti": "North America",
        "148. Botswana": "Africa",
        "149. Syria": "Asia",
        "150. Malawi": "Africa",
        "151. Yemen": "Asia",
        "152. Rwanda": "Africa",
        "153. Tanzania": "Africa",
        "154. Afghanistan": "Asia",
        "155. Central African Republic": "Africa",
        "156. South Sudan": "Africa"
    },
    # Bar overlay for confidence interval
    overlays=[
        dw.BarOverlay(
            from_column="Whisker-low",
            to_column="Whisker-high",
            color="#999999",
            opacity=0.7,
            pattern="diagonal-up",
            title="Confidence Interval (95%)",
            type="range",
            show_in_color_key=True,
            label_directly=False
        )
    ]
)

# Create the chart
chart.create()
```

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.BarChart
```
