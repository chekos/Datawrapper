# Working with chart objects

This guide tours the key operations available on all of our object-oriented chart types.

## Creating a new chart

```python
import datawrapper as dw

# Sample data
data = {
    "Language": ["Python", "JavaScript", "Java", "C#", "C++"],
    "Popularity": [29.9, 19.5, 17.3, 6.7, 6.5]
}

# Create a chart
chart = dw.BarChart(
    title="Most Popular Programming Languages 2024",
    data=data,
    value_label_format=dw.NumberFormat.ONE_DECIMAL,
)

# Create it in Datawrapper
chart_id = chart.create()
print(f"Created chart: {chart_id}")
```

## Getting an existing chart

You can retrieve an existing chart by its ID using the `get()` classmethod:

```python
# Retrieve an existing chart
existing_chart = dw.BarChart.get(chart_id="abc123")

# The chart object now has all the configuration from Datawrapper
print(existing_chart.title)
print(existing_chart.chart_id)
```

## Updating an existing chart

After creating or retrieving a chart, you can modify its properties and update it:

```python
# Modify the chart properties
chart.title = "Programming Language Popularity - Updated"
chart.intro = "Based on 2024 developer survey data"

# Update the data
new_data = {
    "Language": ["Python", "JavaScript", "Java", "C#", "C++", "TypeScript"],
    "Popularity": [30.5, 20.1, 16.8, 7.2, 6.5, 5.9]
}
chart.data = new_data

# Push the changes to Datawrapper
chart.update()
```

## Publishing a chart

Once your chart is ready, publish it to make it publicly accessible:

```python
chart.publish()
```

You can also make it display in a Jupyter notebook by passing `display=True`:

```python
chart.publish(display=True)
```

## Exporting a chart

Export your chart as an SVG, PNG, or PDF file:

```python
# Export as PNG (default)
chart.export(filepath="chart.png")

# Export as SVG with custom dimensions
chart.export(
    filepath="chart.svg",
    unit="px",
    width=800,
    height=600
)

# Export as PDF
chart.export(filepath="chart.pdf")
```

The export method supports various other options for customizing the output format and dimensions.

## Duplicating a chart

Create an editable copy of your chart:

```python
# Create a duplicate
duplicate_chart = chart.duplicate()

# The duplicate is a new chart with a different ID
print(f"Original: {chart.chart_id}")
print(f"Duplicate: {duplicate_chart.chart_id}")

# You can now modify the duplicate independently
duplicate_chart.title = "Copy of Programming Languages"
duplicate_chart.update()
```

## Forking a Chart

Create a fork that maintains a reference to the original:

```python
# Create a fork
forked_chart = chart.fork()

# The fork is a new chart that references the original
print(f"Original: {chart.chart_id}")
print(f"Fork: {forked_chart.chart_id}")

# Modify the fork
forked_chart.title = "Fork: Programming Languages 2025"
forked_chart.update()
```

Forking is similar to duplicating, but maintains a connection to the source chart in Datawrapper.

## Deleting a chart

Remove a chart from Datawrapper:

```python
# Delete the chart
success = chart.delete()

if success:
    print("Chart deleted successfully")
    # The chart_id is now None
    print(f"Chart ID: {chart.chart_id}")
```

## Getting display URLs

Retrieve the published URLs for your chart:

```python
# Get all display URLs for the chart
urls = chart.get_display_urls()

# The response includes various URL formats
for url_info in urls:
    print(f"{url_info['type']}: {url_info['url']}")
```

This returns a list of URL dictionaries with different formats (e.g., responsive iframe, plain URL) that you can use to embed or share your chart.

## Getting iframe code

Get the HTML iframe embed code for your chart:

```python
# Get standard iframe code
iframe_code = chart.get_iframe_code()
print(iframe_code)

# Get responsive iframe code
responsive_iframe = chart.get_iframe_code(responsive=True)
print(responsive_iframe)
```

The iframe code can be directly embedded in HTML pages. The `responsive=True` option generates code that automatically adjusts to container width.

## Getting editor URL

Get the Datawrapper URL to continue editing your chart:

```python
# Get the editor URL
editor_url = chart.get_editor_url()
print(f"Edit chart at: {editor_url}")
```

## Getting png URL

Get the fallback image URL for use in noscript tags:

```python
# Get the PNG URL
png_url = chart.get_png_url()
print(f"PNG fallback: {png_url}")

# Use in HTML noscript tags
html = f'<noscript><img src="{png_url}" alt="Chart" /></noscript>'
```

This provides a static image fallback for environments where JavaScript is disabled. It's also a handy way to get a direct link to the chart image for other uses.
