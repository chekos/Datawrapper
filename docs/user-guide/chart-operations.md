# Chart Operations

After creating your first chart with the quickstart guide, you'll want to know what operations you can perform on chart objects. This guide tours the key operations available on all chart types.

We'll use the same simple example from the quickstart - a bar chart showing programming language popularity.

## Creating a new chart

First, let's create a chart to work with:

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

## Getting an Existing Chart

You can retrieve an existing chart by its ID using the `get()` classmethod:

```python
# Retrieve an existing chart
existing_chart = dw.BarChart.get(chart_id="abc123")

# The chart object now has all the configuration from Datawrapper
print(existing_chart.title)
print(existing_chart.chart_id)
```

This is useful when you want to work with charts you've already created, or when collaborating with others.

## Updating a Chart

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

The `update()` method sends all current chart properties to Datawrapper, so any changes you've made will be reflected.

## Publishing a Chart

Once your chart is ready, publish it to make it publicly accessible:

```python
# Publish the chart
chart.publish()

# The chart now has a public URL
print(f"Chart URL: https://datawrapper.dwcdn.net/{chart.chart_id}/")
```

You can also control the display mode:

```python
# Publish with specific display settings
chart.publish(display=True)  # Make it visible
```

## Exporting a Chart

Export your chart as an image file (PNG, SVG, or PDF):

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

The export method supports various options for customizing the output format and dimensions.

## Duplicating a Chart

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

Duplicating is useful when you want to create variations of a chart without affecting the original.

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

## Deleting a Chart

Remove a chart from Datawrapper:

```python
# Delete the chart
success = chart.delete()

if success:
    print("Chart deleted successfully")
    # The chart_id is now None
    print(f"Chart ID: {chart.chart_id}")
```

**Warning:** Deletion is permanent and cannot be undone. Make sure you really want to delete the chart before calling this method.
