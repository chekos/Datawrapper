# Working with chart objects

This guide tours the key operations available on all charts based on our object-oriented classes.

## Creating a new chart

```python
import pandas as pd
import datawrapper as dw

# Sample data
data = pd.DataFrame(
    {
        "Language": ["Python", "JavaScript", "TypeScript", "Java", "C#"],
        "Percentage": [49.3, 62.3, 38.5, 30.5, 27.1],
    }
)

# Configure the chart object
chart = dw.BarChart(
    title="Most Popular Programming Languages 2024",
    data=data,
    value_label_format=dw.NumberFormat.ONE_DECIMAL,
)

# Create it by sending to Datawrapper
chart.create()
```

## Getting an existing chart

You can retrieve an existing chart with the ID, which is found in its URL.

```python
# Retrieve an existing chart
existing_chart = dw.get_chart("abc123")

# The chart object now has all the configuration from Datawrapper
print(existing_chart.title)
print(existing_chart.chart_id)
```

## Updating an existing chart

```python
# Modify the chart properties
chart.title = "Programming Language Popularity - Updated"
chart.intro = "Based on 2024 developer survey data"

# Update the data
new_data = pd.DataFrame(
    {
        "Language": ["Python", "JavaScript", "TypeScript", "Java", "C#"],
        "Percentage": [30.5, 20.1, 16.8, 7.2, 6.5],
    }
)
chart.data = new_data

# This will send the updates to Datawrapper
chart.update()
```

## Publishing a chart

Once your chart is ready, publish it to make it publicly accessible:

```python
chart.publish()

# Chain with other operations
chart.create().publish()
```

## Exporting a chart

```python
# Export as PNG (default)
chart.export(filepath="chart.png")

# Export with custom dimensions
chart.export(
    filepath="chart.png",
    unit="px",
    width=800,
    height=600
)
```

## Duplicating a chart

```python
duplicate_chart = chart.duplicate()

# The duplicate is a new chart with a different ID
print(f"Original: {chart.chart_id}")
print(f"Duplicate: {duplicate_chart.chart_id}")

# You can now modify the duplicate independently
duplicate_chart.title = "Copy of Programming Languages"
duplicate_chart.update()
```

## Deleting a chart

```python
success = chart.delete()

if success:
    print("Chart deleted successfully")
```

## Getting editor URL

Get the Datawrapper URL to continue editing your chart:

```python
chart.get_editor_url()
```

## Getting iframe code

Get the HTML iframe embed code for your chart:

```python
# Get standard iframe code
iframe_code = chart.get_iframe_code()

# Get responsive iframe code
responsive_iframe = chart.get_iframe_code(responsive=True)
```

## Getting png URL

Get the fallback image URL for use in noscript tags:

```python
png_url = chart.get_png_url()

html = f'<noscript><img src="{png_url}" alt="Chart" /></noscript>'
```

## Exporting a chart in multiple formats

You can export charts in various formats such as PNG, PDF, and SVG using the chart object's export methods:

```python
# Get the data in bytes
png_data = chart.export_png(width=800, height=600)
pdf_data = chart.export_pdf(mode="cmyk")
svg_data = chart.export_svg(plain=True)

# Save to disk
Path("chart.png").write_bytes(png_data)
Path("chart.pdf").write_bytes(pdf_data)
Path("chart.svg").write_bytes(svg_data)
```

## Compatibility for maps, tables and newer Datawrapper types

The object-oriented API is the preferred path for chart types that have dedicated
classes, such as `BarChart`, `LineChart`, `ColumnChart` and `ScatterPlot`. The
older `Datawrapper.create_chart()`, `Datawrapper.update_chart()`,
`Datawrapper.add_data()` and `Datawrapper.publish_chart()` methods are deprecated
for those supported chart classes, but they are not scheduled for removal for
maps, tables or other Datawrapper visualization types until equivalent
object-oriented classes exist.

For unsupported types, use one of these compatible migration paths:

```python
import pandas as pd
import datawrapper as dw

# Forward-compatible object-oriented shim. This works for any non-empty
# Datawrapper visualization type, including maps that do not yet have a
# dedicated Python class.
chart = dw.BaseChart(
    chart_type="d3-maps-choropleth",
    title="Population by region",
    data=pd.DataFrame({"region": ["CA", "NY"], "value": [39.0, 19.6]}),
)
chart.create()
chart.publish()
```

You can also keep using the legacy client methods for unsupported types when you
need to pass raw Datawrapper metadata:

```python
client = dw.Datawrapper()
chart = client.create_chart(
    title="Population by region",
    chart_type="d3-maps-choropleth",
)
client.update_chart(
    chart["id"],
    metadata={"visualize": {"basemap": "usa-states"}},
)
client.publish_chart(chart["id"])
```

`dw.get_chart(chart_id)` returns a dedicated chart class when one is available.
When the Datawrapper API reports a type that is not yet modeled by this package,
it now returns `BaseChart` with a warning instead of failing as unsupported. This
keeps existing maps and newly released Datawrapper visualization types usable
while making it clear that chart-specific convenience fields are not available
until a dedicated class is added.

### Deprecation timeline

- Dedicated chart classes are the future-facing API for supported types.
- Legacy client methods remain available for unsupported maps, tables and new
  visualization types until a dedicated replacement exists.
- After a dedicated class lands for a type, the corresponding legacy-method use
  for that type should go through at least one minor release with clear warnings
  and migration examples before removal is considered in a future major release.
