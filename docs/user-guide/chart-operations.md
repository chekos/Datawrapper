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
