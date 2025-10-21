# Chart Operations

Chart operations that have been largely deprecated by our object-oriented models. Maintained for backwards compatibility and advanced use cases. Where possible, you should use the chart classes and methods instead.

## Chart Management

### Get Chart Information

Retrieve information about a specific chart:

```python
chart_info = client.get_chart(chart_id="abc123")
print(f"Title: {chart_info['title']}")
print(f"Type: {chart_info['type']}")
print(f"Status: {chart_info['publicVersion']}")
```

### Copy a Chart

Create a copy of an existing chart:

```python
new_chart = client.copy_chart(chart_id="abc123")
print(f"New chart ID: {new_chart['id']}")
```

### Delete a Chart

Delete a chart permanently:

```python
client.delete_chart(chart_id="abc123")
```

### Fork a Chart

Fork a chart (create a copy with a reference to the original):

```python
forked_chart = client.fork_chart(chart_id="abc123")
print(f"Forked chart ID: {forked_chart['id']}")
```

## Data Updates

### Update Chart Data

Update the data for an existing chart:

```python
import pandas as pd

# Load new data
new_data = pd.read_csv("updated_data.csv")

# Update the chart
client.add_data(chart_id="abc123", data=new_data)

# Republish to see changes
client.publish_chart(chart_id="abc123")
```

### Update Data from URL

Update chart data from a URL:
```python
client.add_data(
    chart_id="abc123",
    data="https://example.com/data.csv"
)
client.publish_chart(chart_id="abc123")
```

## Metadata Customization

```python
client.add_data(
    chart_id="abc123",
    data="https://example.com/data.csv"
)
client.publish_chart(chart_id="abc123")
```

## Chart Customization

### Update Chart Metadata

```python
client.update_metadata(
    chart_id="abc123",
    metadata={
        "title": "Updated Chart Title",
        "description": "New description text"
    }
)
client.publish_chart(chart_id="abc123")
```

Customize chart appearance and behavior through metadata:

```python
metadata = {
    "visualize": {
        "thick": True,
        "custom-colors": {
            "Category A": "#FF6B6B",
            "Category B": "#4ECDC4",
            "Category C": "#45B7D1"
        }
    }
}

client.update_metadata(chart_id="abc123", metadata=metadata)
client.publish_chart(chart_id="abc123")
```

### Update Chart Description

Add source information and byline:

```python
client.update_description(
    chart_id="abc123",
    source_name="U.S. Census Bureau",
    source_url="https://www.census.gov",
    byline="Data Analysis Team",
    intro="This chart shows population trends over the past decade.",
    notes="Data updated quarterly."
)
client.publish_chart(chart_id="abc123")
```

### Update Chart Title

Change the chart title:

```python
client.update_chart(
    chart_id="abc123",
    title="Updated Chart Title",
    intro="New introduction text"
)
client.publish_chart(chart_id="abc123")
```
