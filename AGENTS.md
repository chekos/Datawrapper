# AGENTS.md — Use Datawrapper to create charts (for coding agents)

**Audience:** Coding agents (Claude, Codex, GitHub Copilot, etc.) acting on behalf of a user.
**Goal:** Create a published, shareable chart URL from user-provided data and instructions.
**Success:** Return a chart URL (public if published, or private visualize link if draft) that reflects the user's spec; no leaking tokens; no unnecessary duplicate charts.

## Golden Path (copy/paste this)

```python
# Golden Path: verify token, create, publish, return URL
import os, sys, json
import pandas as pd
from datawrapper import ColumnChart  # choose any chart type you need

# 0) Version check + token verification
assert sys.version_info >= (3,10), "Use Python 3.10+ for datawrapper>=2.0"

# Optional: auto-load .env if present (do NOT print secrets)
try:
    from dotenv import load_dotenv; load_dotenv()
except Exception:
    pass

assert os.getenv("DATAWRAPPER_ACCESS_TOKEN"), "Set DATAWRAPPER_ACCESS_TOKEN first"  # do NOT print token

# 1) Prepare data
df = pd.DataFrame({
    "Quarter": ["Q1", "Q2", "Q3", "Q4"],
    "Revenue": [250, 300, 280, 350]
})

# 2) Create & safe publish (handles missing 'chart:publish' scope)
chart = ColumnChart(
    title="Quarterly Revenue",
    data=df,
    intro="Revenue in millions USD",
    source_name="Internal Finance"
).create()

try:
    chart.publish()
    result = {"public_url": chart.public_url, "chart_id": chart.id, "summary": "Quarterly revenue Q1-Q4"}
    # Include embed code for easy copy-paste
    embed = f'<iframe title="{chart.title}" aria-label="chart" src="https://datawrapper.dwcdn.net/{chart.id}/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="400"></iframe>'
    result["embed"] = embed
except Exception as e:
    # Still useful: return draft/visualize link so user can publish manually
    code = getattr(getattr(e, "response", None), "status_code", None)
    visualize_url = f"https://app.datawrapper.de/chart/{chart.id}/visualize"
    result = {"public_url": visualize_url, "chart_id": chart.id,
              "summary": "Draft chart - publish manually",
              "error": f"publish_failed{f'_{code}' if code else ''}"}

print(json.dumps(result))  # Return JSON for machine readability
```

## Standard Imports (use everywhere)

```python
from datawrapper import (
    BarChart, ColumnChart, LineChart, AreaChart,
    ScatterPlot, StackedBarChart, MultipleColumnChart, ArrowChart
)
from datawrapper.charts.enums import (
    NumberFormat, DateFormat, GridDisplay, LineWidth, LineDash,
    ValueLabelDisplay, NumberDivisor
)
from datawrapper.charts.models import TextAnnotation, RangeAnnotation
import pandas as pd
```

## Chart Lifecycle Policy

- **If user gives a chart ID** → `ChartClass.get(id)` → modify → `.update()` → (optional) `.publish()`
- **If user references an existing title and wants changes** → search (if available) or ask for the ID; prefer **update**
- **If user says "new chart" or "template copy"** → use `.duplicate()` from a known template → edit → `.update()` → `.publish()`
- **Never create multiple drafts** for the same instruction; one chart per request unless the user asks for variants

**Use chart classes by default.**
**Exception:** `locator-map` currently requires a JSON dataset → use the low-level client *only for this case*.

## Data Hygiene Rules

### Data formats supported
- **Default:** pandas DataFrame / CSV for bars, columns, lines, areas, scatter
- **Special:** JSON for complex charts (e.g., locator-map with markers, icons, tooltips)
- **Rule:** If data is tabular → use DataFrame/CSV. If locator-map with markers → use JSON payload
- **Wide vs long:**
  - Most categorical bars/columns: **wide** (one row per category, one or more value columns)
  - Many lines in one plot: prefer **wide** (one column per series) unless the API requires long
- **Coerce numerics:** `for c in value_cols: df[c] = pd.to_numeric(df[c], errors="coerce")`
- **Then handle NaNs:** `df = df.dropna()` (or `fillna(0)` if zero is appropriate)
- **Dates:** For time series, convert to timezone-aware UTC:
  ```python
  df["Date"] = pd.to_datetime(df["Date"], utc=True, errors="raise")
  ```
- **Percentages:** Convert to 0–100 *before* setting `NumberFormat.PERCENTAGE`
  ```python
  def ensure_percent_scale(df, cols):
      for c in cols:
          s = pd.to_numeric(df[c], errors="coerce")
          if s.max() is not None and s.max() <= 1:
              df[c] = s * 100
      return df
  ```
- **Sorting:** For ranked bars/columns, sort descending by the value column before create/publish
- **Idempotent title:** If creating new chart from data, append stable hash (includes chart type):
  ```python
  sig = (pd.util.hash_pandas_object(df, index=False).sum(), "ColumnChart")
  title = f"{base_title} — {abs(hash(sig)) % 10_000:04d}"
  ```

## Agent Output Format

### When you finish, always return:
1. **Chart:** `<public URL>` (or visualize link if publish failed)
2. **Chart ID:** `<chart_id>`
3. **Summary:** one sentence (e.g., "Quarterly revenue Q1–Q4, in M USD")
4. **How to reproduce:** minimal code block that users can copy/paste

### Preferred response format (JSON)
```json
{"public_url":"<url-or-draft>", "chart_id":"<id>", "summary":"<one sentence>"}
```

**If publish fails (403 scope):** Return
- `public_url`: `https://app.datawrapper.de/chart/<chart_id>/visualize`
- `note`: "Open this link and click **Publish**."

### Next steps (tell the user):
1. Click **Publish** (if not auto-published)
2. (Optional) Download/Export (PNG/HTML)
3. Use the embed code if needed

## Pick a chart quickly

- **Ranked categories** → BarChart (horizontal) or ColumnChart (vertical)
- **Time series (1–5 series)** → LineChart
- **Composition over time** → AreaChart
- **Relationship** → ScatterPlot
- **Geographic points** → locator-map (use JSON + low-level)

## Chart Type Examples

### Bar Chart (Horizontal)
```python
import pandas as pd
from datawrapper import BarChart

df = pd.DataFrame({
    "Country": ["USA", "China", "Japan", "Germany", "India"],
    "GDP": [21.43, 14.34, 5.08, 3.84, 2.87]
})
df = df.sort_values("GDP", ascending=False)  # Sort for ranking

chart = BarChart(
    title="Top 5 Economies by GDP",
    data=df,
    intro="2023 nominal GDP in trillion USD",
    source_name="World Bank"
).create().publish()

print(chart.public_url, chart.id)
```

### Line Chart (Time Series)
```python
import pandas as pd
from datawrapper import LineChart

df = pd.DataFrame({
    "Date": pd.date_range("2024-01-01", periods=12, freq="M"),
    "Sales": [100, 110, 125, 140, 135, 155, 170, 165, 180, 195, 210, 220],
    "Costs": [80, 85, 90, 95, 88, 92, 98, 94, 100, 105, 110, 115]
})
df["Date"] = pd.to_datetime(df["Date"], utc=True, errors="raise")  # Ensure datetime
df = df.sort_values("Date")  # Ensure monotonic

chart = LineChart(
    title="Monthly Sales vs Costs",
    data=df,
    intro="Company performance in 2024",
    source_name="ERP Export"
).create().publish()

print(chart.public_url, chart.id)
```

### Column Chart (Vertical)
```python
import pandas as pd
from datawrapper import ColumnChart
from datawrapper.charts.enums import NumberFormat

df = pd.DataFrame({
    "Quarter": ["Q1", "Q2", "Q3", "Q4"],
    "Revenue": [250, 300, 280, 350]
})

chart = ColumnChart(
    title="Quarterly Revenue",
    data=df,
    intro="Revenue in millions USD",
    axis_label_format=NumberFormat.CURRENCY_USD
).create().publish()

print(chart.public_url, chart.id)
```

### Scatter Plot
```python
import pandas as pd
from datawrapper import ScatterPlot

df = pd.DataFrame({
    "Height": [165, 170, 175, 180, 185, 160, 172, 178],
    "Weight": [60, 65, 70, 75, 80, 58, 68, 73],
    "Name": ["A", "B", "C", "D", "E", "F", "G", "H"]
})

chart = ScatterPlot(
    title="Height vs Weight Correlation",
    data=df
).create().publish()

print(chart.public_url, chart.id)
```

### Area Chart
```python
import pandas as pd
from datawrapper import AreaChart

df = pd.DataFrame({
    "Year": [2020, 2021, 2022, 2023, 2024],
    "Product A": [100, 120, 140, 160, 180],
    "Product B": [80, 90, 110, 130, 150],
    "Product C": [60, 70, 85, 95, 110]
})

chart = AreaChart(
    title="Product Sales Over Time",
    data=df,
    intro="Sales in thousands of units"
).create().publish()

print(chart.public_url, chart.id)
```

### Locator Map (JSON data)
```python
# Note: Locator maps require JSON dataset with markers, not DataFrames
from datawrapper import Datawrapper
import json

# JSON structure for locator map
map_data = {
    "markers": [
        {"lat": 40.7128, "lng": -74.0060, "name": "New York", "tooltip": "NYC Office"},
        {"lat": 51.5074, "lng": -0.1278, "name": "London", "tooltip": "EU HQ"},
        {"lat": 35.6762, "lng": 139.6503, "name": "Tokyo", "tooltip": "APAC Office"}
    ]
}

# For locator-map, use low-level API with JSON dataset
dw = Datawrapper()
chart_info = dw.create_chart(title="Global Offices", chart_type="locator-map")
dw.add_data(chart_id=chart_info["id"], data=json.dumps(map_data))
dw.publish_chart(chart_id=chart_info["id"])

print(f"https://app.datawrapper.de/chart/{chart_info['id']}/visualize", chart_info["id"])
```

## Common Configurations

### Number Formatting
```python
from datawrapper import ColumnChart, BarChart
from datawrapper.charts.enums import NumberFormat, NumberDivisor

# Currency
chart = ColumnChart(
    title="Revenue",
    data=df,
    axis_label_format=NumberFormat.CURRENCY_USD
).create().publish()

# Percentage (data should be 0-100)
if df["Rate"].max() <= 1:
    df["Rate"] = df["Rate"] * 100  # Convert 0.45 to 45
chart = BarChart(
    title="Market Share",
    data=df,
    axis_label_format=NumberFormat.PERCENTAGE
).create().publish()

# Thousands with separator
chart = BarChart(
    title="Population",
    data=df,
    number_divisor=NumberDivisor.THOUSANDS,
    axis_label_format=NumberFormat.THOUSANDS_SEPARATOR
).create().publish()
```

### Adding Annotations
```python
from datawrapper import LineChart
from datawrapper.charts.models import TextAnnotation

chart = LineChart(title="Stock Price", data=df)
chart.text_annotations = [
    TextAnnotation(
        x="2024-03-15",  # X position
        y=150,           # Y position
        text="Market crash"
    )
]
chart.create().publish()
print(chart.public_url, chart.id)
```

### Grid and Styling
```python
from datawrapper import BarChart
from datawrapper.charts.enums import GridDisplay

chart = BarChart(
    title="Sales Report",
    data=df,
    y_grid_display=GridDisplay.ON,
    base_color="#FF6B6B"  # hex string required (not "red")
).create().publish()
```

## Working with Existing Charts

### Update Existing
```python
from datawrapper import BarChart

# Get existing chart by ID
chart = BarChart.get("abc123")
chart.title = "Updated Title for 2024"
chart.intro = "New introduction text"
chart.update()  # Save changes
chart.publish()  # Re-publish if needed
print(chart.public_url, chart.id)
```

### Duplicate Template
```python
from datawrapper import ColumnChart

# Use existing as template
template = ColumnChart.get("xyz789")
new_chart = template.duplicate()
new_chart.title = "Q4 2024 Report"
new_chart.data = new_df
new_chart.update().publish()
print(new_chart.public_url, new_chart.id)
```

## Data Preparation Patterns

### From CSV (with locale handling)
```python
import pandas as pd
from datawrapper import LineChart

# Read as strings first to handle locale issues
df = pd.read_csv("data.csv", dtype=str)
df = df.apply(lambda c: c.str.strip() if c.dtype==object else c)  # Strip whitespace

# Clean and convert numeric columns
for c in ["Revenue", "Costs"]:  # your value columns
    df[c] = (df[c].str.replace("\u00A0", "")      # no-break spaces
                  .str.replace(",", "")             # drop thousands sep
                  .str.replace("%", "")             # drop percent sign
                  .astype(float))

df["Date"] = pd.to_datetime(df["Date"], utc=True, errors="raise")  # Parse dates
df = df.dropna()  # Remove missing values
df = df.sort_values("Date")  # Sort chronologically

chart = LineChart(
    title="Trend Analysis",
    data=df
).create().publish()
print(chart.public_url, chart.id)
```

### From Dictionary
```python
import pandas as pd
from datawrapper import BarChart

data = {
    "Product": ["Laptop", "Phone", "Tablet"],
    "Units": [45, 120, 78]
}
df = pd.DataFrame(data)
df = df.sort_values("Units", ascending=False)

chart = BarChart(
    title="Product Sales",
    data=df
).create().publish()
print(chart.public_url, chart.id)
```

### Pivot Wide to Long (if needed)
```python
# Most charts prefer wide format, but if you need long:
df_long = df.melt(id_vars=["Date"], var_name="Series", value_name="Value")
```

## Troubleshooting

- **401/403 Unauthorized:** Token missing/invalid → ask user to set `DATAWRAPPER_ACCESS_TOKEN`. Do NOT print the token
- **403 on publish:** Token may lack `chart:publish` scope → return visualize URL, tell user to publish manually:
  ```python
  visualize_url = f"https://app.datawrapper.de/chart/{chart.id}/visualize"
  ```
- **Python version:** Ensure Python ≥ 3.10 for datawrapper ≥ 2.0
- **400 Validation:** Check column names match fields; ensure numeric types; ensure dates parsed
  - Column names shouldn't start with a number and should contain only letters, numbers, spaces, underscore, hyphen
- **Rate limit / 429:** Exponential backoff (1s, 2s, 4s up to 5 tries), then report failure
- **Network issues:** Retry up to 3 times before surfacing error
- **Empty DataFrame:** Check data loading; ensure CSV path correct; verify column names
- **NaN values:** Use `.fillna(0)` or `.dropna()` before charting
- **JSON vs CSV:** Locator maps need JSON, not DataFrame. Use low-level API for complex map data
- **Large CSVs (>50k rows):** WARN USER before aggregating! Say: "Dataset has X rows. Should I aggregate/sample for better performance, or use all data?"

## Organization Conventions

- **Title:** `<Topic> — <Segment> — <Date>` (e.g., "Revenue — EMEA — 2024-Q3")
- **Intro:** One sentence explaining what the chart shows
- **Source:** Always credit data source
- **Source URL:** Add URL when available
- **Tags:** Add `team:<name>`, `source:<system>`, `status:published` if workspace supports
- **Folders:** Put charts in project/team folder if available

## Privacy & Security

- Never print or log the access token
- Don't echo back private data unless the user explicitly asks for it
- WARN about PII in chart labels - ask user before redacting
- If public sharing requested with sensitive data, ASK: "This data may contain sensitive information. Should I aggregate/anonymize it first?"
- Use environment variables, never hardcode credentials

## Dynamic Chart Selection

```python
import pandas as pd
from datawrapper import BarChart, ColumnChart, LineChart, AreaChart

def create_chart(chart_type: str, data: pd.DataFrame, title: str) -> dict:
    chart_classes = {
        "bar": BarChart,
        "column": ColumnChart,
        "line": LineChart,
        "area": AreaChart
    }
    ChartClass = chart_classes.get(chart_type.lower(), BarChart)
    try:
        chart = ChartClass(title=title, data=data).create().publish()
        return {"public_url": chart.public_url, "chart_id": chart.id}
    except Exception as e:
        return {"error": str(e)}
```

## Quick Reference

**Quick Steps**
1. DataFrame ready → choose chart class → `.create().publish()`
2. Return JSON: `{"public_url": url, "chart_id": id, "summary": text}`
3. If publish fails → return visualize link, ask user to click Publish
4. Update existing by ID when asked; avoid duplicate drafts
5. Dates parsed, percents scaled, NaNs handled, sorted if ranked
6. If error: apply playbook; never leak secrets

**Essential Pattern**
```python
import os, pandas as pd
from datawrapper import BarChart

assert os.getenv("DATAWRAPPER_ACCESS_TOKEN"), "Token required"
df = pd.DataFrame(your_data)
chart = BarChart(title="Your Title", data=df).create().publish()
print(chart.public_url, chart.id)  # Always return both
```

**Remember**
- Use chart classes from `datawrapper`, not low-level API (except locator-map)
- Data must be pandas DataFrame (except locator-map which needs JSON)
- Auth via `DATAWRAPPER_ACCESS_TOKEN` environment variable
- Charts aren't public until `.publish()`
- Always return the chart URL to the user