# Table

This example, drawn from [Datawrapper's official documentation](https://www.datawrapper.de/academy/examples-of-datawrapper-tables), demonstrates how to create a table showing how life expectancy has increased in different countries. The table uses flags alongside country names, a mini line chart and a bar chart. It sticks one column to the bottom of the table, and colours the background of cells in the Continent column depending on the Continent value.

<iframe title="Life expectancy in all countries increased since 1960, but with a different pace" aria-label="Table" id="datawrapper-chart-Azxvm" src="https://datawrapper.dwcdn.net/Azxvm/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="519" data-external="1"></iframe><script type="text/javascript">window.addEventListener("message",function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r,i=0;r=e[i];i++)if(r.contentWindow===a.source){var d=a.data["datawrapper-height"][t]+"px";r.style.height=d}}});</script>

```python
import pandas as pd
import datawrapper as dw

# Load media trust data from GitHub
df = pd.read_csv(
    "https://raw.githubusercontent.com/chekos/Datawrapper/main/tests/samples/table/life_expectancy.csv"
)

excluded_columns = ["Country", "Increase between 1960 and 2016", "Continent"]
line_column_names = [col for col in df.columns if col not in excluded_columns]

chart = dw.Table(
    # Chart title
    title="Life expectancy in all countries increased since 1960, but with a different pace",
    # Introductory text explaining the context
    intro="Life expectancy at birth in years, 1960-2016",
    # Data source attribution
    source_name="Worldbank",
    source_url="https://data.worldbank.org/indicator/sp.dyn.le00.in"
    # Data from pandas DataFrame
    data=df,
    # Show a search bar on the table
    searchable=True,
    # Sort the table in ascending direction by the specified column
    sort_table=True, sort_by="Increase between 1960 and 2016", sort_direction="asc",
    # Show six rows of the table per page
    rows_per_page=6,
    # Show a card design on devices smaller than 450px
    mobile_fallback=True,
    # Change the style of the header row to have a thin grey bottom border, and grey text
    header_style=dw.TableRow(border_bottom=dw.BorderWidth.THIN, border_bottom_color="#aaaaaa", style=dw.TableTextStyle(color="#494949", font_size=0.9)),
    # Set styles for specific columns
    column_styles=[
        # Set the country column width and replace country codes with flags
        dw.TableColumn(name="Country", flag_style=dw.ReplaceFlagsType.CIRCLE, fixed_width=True, width=0.21),
        # Set the 1960 column width
        dw.TableColumn(name="1960", fixed_width=True, width=0.4),
        # Set the continent column width and colour cells based on provided colour map
        dw.TableColumn(name="Continent", fixed_width=True, width=0.04, custom_color=True,
        custom_color_background={
            "Africa": "#FFCF90",
            "Asia": "#EF9278",
            "Europe": "#8dbbc1",
            "North America": "#86BA90",
            "Oceania": "#b989b0",
            "South America": "#92cdb2"
            }
        ),
        # Set increase column width, show as bar chart and exclude from mobile view
        dw.TableColumn(name="Increase between 1960 and 2016", fixed_width=True, width=0.35, show_as_bar=True, bar_color="#15607a", show_on_mobile=False)
    ],
    # Stick the world column to the bottom of every page and colour its background
    row_styles=[dw.TableBodyRow(row_index=187, sticky=True, style=dw.TableTextStyle(background="#f0f0f0", bold=True))],
    # Combine year columns into mini line chart
    mini_charts=[dw.MiniLine(columns=line_column_names, color="#c71e1d", height=40)],
    # Append " years" to values in increase column
    column_format=[dw.ColumnFormat(column="Increase between 1960 and 2016", number_append=" years")])

# Create the chart in Datawrapper
chart.create()
```

## Table with heatmap
This example, drawn from [Datawrapper's official documentation](https://www.datawrapper.de/academy/examples-of-datawrapper-tables), demonstrates how to create a heatmap table showing unemployment rates in different countries.

<iframe title="Unemployment rate in selected countries" aria-label="Table" id="datawrapper-chart-uFSM1" src="https://datawrapper.dwcdn.net/uFSM1/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="584" data-external="1"></iframe><script type="text/javascript">window.addEventListener("message",function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r,i=0;r=e[i];i++)if(r.contentWindow===a.source){var d=a.data["datawrapper-height"][t]+"px";r.style.height=d}}});</script>

```python
import pandas as pd
import datawrapper as dw

# Load media trust data from GitHub
df = pd.read_csv(
    "https://raw.githubusercontent.com/chekos/Datawrapper/main/tests/samples/table/unemployment.csv"
)

df = pd.read_csv("tests/samples/table/unemployment.csv")
column_names = [col for col in df.columns if col.lower() != 'country']
column_styles = []
# create column styles to format the contents of the numerical columns
for col in column_names:
    column_styles.append(dw.TableColumn(name=col, format=dw.NumberFormat.PERCENT_ONE_DECIMAL))

chart = dw.Table(
    # Chart title
    title="Unemployment rate in selected countries",
    # Introductory text explaining the context
    intro="January-August 2020, sorted by the unemployment rate in January",
    # Data source attribution
    source_name="OECD",
    source_url="data.oecd.org/unemp/unemployment-rate.htm",
    # Data from pandas DataFrame
    data=df,
    # Sort table by ascending values in "Jan" column
    sort_table=True, sort_by="Jan", sort_direction="asc",
    # Make the header row have a medium bottom border and not be bold
    header_style=dw.TableRow(
        border_bottom=dw.BorderWidth.MEDIUM,
        style=dw.TableTextStyle(font_size=0.9, bold=False)
        ),
    # Bold the rows with index 4 and 9
    row_styles=[
        dw.TableBodyRow(row_index=4, style=dw.TableTextStyle(bold=True)),
        dw.TableBodyRow(row_index=9, style=dw.TableTextStyle(bold=True))
    ],
    # Make the table a heatmap with custom colors and do not show a heatmap legend
    heatmap=dw.HeatMapContinuous(
        legend=False,
        colors=[
            "#feebe2",
            "#fcc5c0",
            "#fa9fb5",
            "#f768a1",
            "#c51b8a",
            "#7a0177"]),
    # Add the column styles created earlier
    column_styles=column_styles
)

chart.create()
```

## Reference

```{eval-rst}
.. parameter-table:: datawrapper.charts.Table
