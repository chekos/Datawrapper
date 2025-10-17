# Advanced API Usage

This guide covers advanced features of the Datawrapper API client for operations beyond chart creation with our object-oriented chart classes. It takes advantage of the Datawrapper class to manage accounts, folders, themes, teams, and more.

## Authentication

### Using Environment Variables

The recommended way to authenticate is by setting the DATAWRAPPER_ACCESS_TOKEN environment variable. Then initialize the client without passing the token.

```python
from datawrapper import Datawrapper

dw = Datawrapper()
```

### Passing Token Directly

You can also pass the token directly when initializing:

```python
from datawrapper import Datawrapper

dw = Datawrapper(access_token="your_token_here")
```

## Account Management

### Get Account Information

Retrieve information about your Datawrapper account:

```python
account_info = dw.get_my_account()
print(f"User: {account_info['name']}")
print(f"Email: {account_info['email']}")
print(f"Role: {account_info['role']}")
```

### Get Recently Edited Charts

Retrieve your recently edited charts:

```python
recent_charts = dw.get_my_recently_edited_charts(limit=10)
for chart in recent_charts:
    print(f"{chart['id']}: {chart['title']}")
```

### Get Published Charts

Retrieve your published charts:

```python
published_charts = dw.get_my_recently_published_charts(limit=10)
for chart in published_charts:
    print(f"{chart['id']}: {chart['title']} - {chart['publicUrl']}")
```

## Folders

### List Folders

Get all folders in your account:

```python
folders = dw.get_folders()
for folder in folders:
    print(f"{folder['id']}: {folder['name']}")
```

### Create a Folder

Create a new folder:

```python
folder = dw.create_folder(name="Q4 2024 Reports")
folder_id = folder['id']
```

### Move Chart to Folder

Move a chart to a specific folder:

```python
dw.move_chart(chart_id="abc123", folder_id=folder_id)
```

## Themes

### List Available Themes

Get all themes available to your account:

```python
themes = dw.get_themes()
for theme in themes:
    print(f"{theme['id']}: {theme['title']}")
```

### Apply Theme to Chart

Apply a theme when creating or updating a chart:

```python
from datawrapper.charts import BarChart

chart = BarChart(
    title="Themed Chart",
    data=df,
    theme="my-custom-theme"
)
chart_id = chart.create()
```

## Teams and Workspaces

### Get Team Information

If you're part of a team, retrieve team information:

```python
teams = dw.get_teams()
for team in teams:
    print(f"{team['id']}: {team['name']}")
```

### Get Team Settings

Get settings for a specific team:

```python
team_settings = dw.get_team_settings(team_id="team123")
```

## Chart Management

### Get Chart Information

Retrieve information about a specific chart:

```python
chart_info = dw.get_chart(chart_id="abc123")
print(f"Title: {chart_info['title']}")
print(f"Type: {chart_info['type']}")
print(f"Status: {chart_info['publicVersion']}")
```

### Copy a Chart

Create a copy of an existing chart:

```python
new_chart = dw.copy_chart(chart_id="abc123")
print(f"New chart ID: {new_chart['id']}")
```

### Delete a Chart

Delete a chart permanently:

```python
dw.delete_chart(chart_id="abc123")
```

### Fork a Chart

Fork a chart (create a copy with a reference to the original):

```python
forked_chart = dw.fork_chart(chart_id="abc123")
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
dw.add_data(chart_id="abc123", data=new_data)

# Republish to see changes
dw.publish_chart(chart_id="abc123")
```

### Update Data from URL

Update chart data from a URL:

```python
dw.add_data(
    chart_id="abc123",
    data="https://example.com/data.csv"
)
dw.publish_chart(chart_id="abc123")
```

## Metadata Customization

### Update Chart Metadata

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

dw.update_metadata(chart_id="abc123", metadata=metadata)
dw.publish_chart(chart_id="abc123")
```

### Update Chart Description

Add source information and byline:

```python
dw.update_description(
    chart_id="abc123",
    source_name="U.S. Census Bureau",
    source_url="https://www.census.gov",
    byline="Data Analysis Team",
    intro="This chart shows population trends over the past decade.",
    notes="Data updated quarterly."
)
dw.publish_chart(chart_id="abc123")
```

### Update Chart Title

Change the chart title:

```python
dw.update_chart(
    chart_id="abc123",
    title="Updated Chart Title",
    intro="New introduction text"
)
dw.publish_chart(chart_id="abc123")
```

## Exporting Charts

### Export as PNG

Export a chart as a PNG image:

```python
dw.export_chart(
    chart_id="abc123",
    output="png",
    filepath="chart.png",
    display=True  # Opens the image after saving
)
```

### Export as PDF

Export a chart as a PDF:

```python
dw.export_chart(
    chart_id="abc123",
    output="pdf",
    filepath="chart.pdf"
)
```

### Export as SVG

Export a chart as an SVG:

```python
dw.export_chart(
    chart_id="abc123",
    output="svg",
    filepath="chart.svg"
)
```

### Export with Custom Dimensions

Specify custom dimensions for the export:

```python
dw.export_chart(
    chart_id="abc123",
    output="png",
    filepath="chart.png",
    width=1200,
    height=800
)
```
