# Interactive Gallery Builder

**Category:** New Feature
**Quarter:** Q3-Q4
**T-shirt Size:** XL

## Why This Matters

Individual charts tell stories, but chart collections tell complete narratives. Reports, dashboards, and data stories typically contain multiple coordinated visualizations. Currently, users must manage each chart individually and manually compose them into galleries or dashboards. A gallery builder enables programmatic creation of rich, multi-chart experiences—from automated weekly reports to interactive data stories.

This elevates the library from "chart creator" to "data storytelling platform."

## Current State

Charts are created and managed individually with no concept of grouping or layout:

```python
# Creating a "dashboard" is manual and tedious
charts = []
for metric in ["revenue", "users", "churn"]:
    chart = dw.LineChart(title=f"{metric.title()} Over Time", data=get_data(metric))
    chart.create()
    chart.publish()
    charts.append(chart)

# Then manually embed in HTML or compose in Datawrapper UI
```

The Datawrapper API supports "River" pages for multi-chart layouts, but there's no Python interface for creating them. References exist in `__main__.py`:
- `_RIVER_URL = _BASE_URL + "/v3/river"` (line 49)

## Proposed Future State

A fluent API for creating coordinated multi-chart experiences:

```python
import datawrapper as dw

# Create a gallery with layout
gallery = dw.Gallery(title="Q4 Performance Dashboard")

# Add charts with layout positions
gallery.add(
    dw.LineChart(title="Revenue Trend", data=revenue_df),
    position="top-left",
    width="50%"
)
gallery.add(
    dw.BarChart(title="Top Products", data=products_df),
    position="top-right",
    width="50%"
)
gallery.add(
    dw.DataTable(title="Detailed Breakdown", data=details_df),
    position="bottom",
    width="100%"
)

# Create and publish as a single unit
gallery.create()
gallery.publish()
print(gallery.url)  # https://datawrapper.dwcdn.net/river/abc123

# Template-based reports
template = dw.ReportTemplate.from_file("quarterly_report.yaml")
report = template.render(
    quarter="Q4 2024",
    data_sources={
        "revenue": revenue_df,
        "users": users_df,
        "products": products_df
    }
)
report.publish()

# Scheduled reports
dw.schedule(
    gallery,
    cron="0 9 * * 1",  # Every Monday at 9am
    recipients=["team@company.com"]
)
```

## Key Deliverables

- [ ] **`dw.Gallery` class** - Container for multiple charts with layout
- [ ] **Layout system** - Grid-based positioning and sizing
- [ ] **River API integration** - Create/manage Datawrapper River pages
- [ ] **Chart coordination** - Shared axes, color scales, filters across charts
- [ ] **Template system** - YAML/JSON templates for reusable report structures
- [ ] **Responsive layouts** - Mobile-friendly gallery configurations
- [ ] **Export options** - PDF, PNG, HTML export of entire galleries
- [ ] **Scheduling API** - Programmatic report scheduling
- [ ] **Email delivery** - Send published galleries via email
- [ ] **Embedding helpers** - Generate embed codes for galleries
- [ ] **Interactive filters** - Cross-chart filtering (if API supports)

## Prerequisites

- Initiative 01 (Complete Chart Type Coverage) - Tables and maps needed for rich dashboards
- Initiative 05 (Batch Operations) - Efficient creation of multiple charts
- Initiative 08 (Data Pipeline Integration) - Data sources for automated reports

## Risks & Open Questions

- **River API capabilities**: What layout and interactivity features does the River API actually support?
- **Chart limits**: Are there limits on charts per gallery?
- **Coordination complexity**: How to handle shared color scales, axes, and filters?
- **Template format**: YAML, JSON, or Python DSL for templates?
- **Preview**: How to preview galleries before publishing?
- **Versioning**: How to version and update existing galleries?
- **Permissions**: Can galleries have different permissions than individual charts?

## Notes

The `_RIVER_URL` endpoint in `__main__.py` (line 49) suggests River pages are API-accessible:

```python
_RIVER_URL = _BASE_URL + "/v3/river"
```

A Gallery could be modeled as:

```python
@dataclass
class GalleryItem:
    chart: BaseChart
    position: str  # "top-left", "top-right", "bottom", etc.
    width: str  # "50%", "100%", "300px"
    height: str | None = None

class Gallery:
    title: str
    description: str
    items: list[GalleryItem]
    theme: str | None

    def create(self) -> str:
        """Create gallery in Datawrapper, returns gallery ID."""
        # 1. Create all charts
        for item in self.items:
            item.chart.create()

        # 2. Create River page with layout
        river_data = {
            "title": self.title,
            "description": self.description,
            "blocks": [self._chart_to_block(item) for item in self.items]
        }
        response = self._client.post(self._RIVER_URL, data=river_data)
        return response["id"]
```

Template system example:

```yaml
# quarterly_report.yaml
title: "{{ quarter }} Performance Report"
layout: "2x2"
charts:
  - type: line
    title: "Revenue Trend"
    data_source: revenue
    position: [0, 0]

  - type: bar
    title: "Top Products"
    data_source: products
    position: [0, 1]

  - type: table
    title: "Regional Breakdown"
    data_source: regions
    position: [1, 0]
    span: 2  # Full width
```

The `rich` library could provide terminal previews of gallery layouts before publishing.
