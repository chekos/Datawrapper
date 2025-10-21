# Quick start guide

This guide will help you create your first Datawrapper chart using the object-oriented Python API. You'll learn the basics of chart creation, configuration, and publishing.

## Prerequisites

- Python 3.10 or higher
- An account at [datawrapper.de](https://www.datawrapper.de/)
- A Datawrapper API token with appropriate permissions

## Installation

Install the datawrapper package using `uv` or `pip` or another Python package manager:

```bash
# Using uv (recommended)
uv add datawrapper

# Or using pip
pip install datawrapper
```

## Getting Your API Token

1. Log in to your Datawrapper account
2. Go to Settings → API Tokens
3. Click "Create new token"
4. Give it a descriptive name (e.g., "Python Scripts")
5. Copy the token and store it securely
6. Set it as an environment variable named `DATAWRAPPER_ACCESS_TOKEN`

## Creating your first chart

Let's create a simple bar chart showing programming language popularity:

```python
import pandas as pd
import datawrapper as dw

# Set up your data
data = pd.DataFrame(
    {
        "Language": ["Python", "JavaScript", "TypeScript", "Java", "C#"],
        "Percentage": [49.3, 62.3, 38.5, 30.5, 27.1],
    }
)

# Create a bar chart
chart = dw.BarChart(
    title="Most Popular Programming Languages 2024",
    intro="Based on Stack Overflow Developer Survey",
    data=data,
    value_label_format=dw.NumberFormat.ONE_DECIMAL,
    source_name="Stack Overflow",
    source_url="https://insights.stackoverflow.com/survey/2024",
    byline="Datawrapper Quickstart Guide",
)

# Create the chart on Datawrapper (uses DATAWRAPPER_ACCESS_TOKEN environment variable)
chart.create()

# You could also provide the token at runtime
# chart_id = chart.create(access_token="your_token_here")

# Publish the chart
chart.publish()
```

## Updating an existing chart

```python
# Get the chart from the API
chart = dw.get_chart(chart_id)

# Make a change
chart.title = "Most Popular Programming Languages in 2024!!!"
chart.update()
```

## Creating multiple charts

```python
for category in ["Sales", "Revenue", "Profit"]:
    chart = dw.BarChart(
        title=f"{category} by Region", data=get_data_for_category(category)
    )
    chart.create()
```

Happy charting! 📊
