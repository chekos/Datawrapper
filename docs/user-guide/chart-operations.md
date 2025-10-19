# Working with chart objects

This guide tours the key operations available on all of our object-oriented chart types.

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

# Create a chart
chart = dw.BarChart(
    title="Most Popular Programming Languages 2024",
    data=data,
    value_label_format=dw.NumberFormat.ONE_DECIMAL,
)

# Create it in Datawrapper
chart_id = chart.create()
```

## Getting an existing chart

You can retrieve an existing chart by using `get_chart` with the chart ID:

```python
# Retrieve an existing chart
existing_chart = dw.get_chart("abc123")

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
new_data = pd.DataFrame(
    {
        "Language": ["Python", "JavaScript", "TypeScript", "Java", "C#"],
        "Percentage": [30.5, 20.1, 16.8, 7.2, 6.5],
    }
)
chart.data = new_data

# Push the changes to Datawrapper
chart.update()
```

## Publishing a chart

Once your chart is ready, publish it to make it publicly accessible:

```python
chart.publish()
```

## Exporting a chart

Export your chart as an SVG, PNG, or PDF file:

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
chart.get_editor_url()
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
