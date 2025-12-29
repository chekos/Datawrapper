# Complete Chart Type Coverage

**Category:** New Feature
**Quarter:** Q1
**T-shirt Size:** XL

## Why This Matters

The Datawrapper API supports a rich ecosystem of visualization types—including maps, tables, pie charts, donut charts, and more—but this Python wrapper currently only implements 8 chart types. This gap forces users to fall back to the deprecated low-level API for common use cases like geographic visualizations and tabular data. Completing chart type coverage is the single highest-impact initiative because it directly expands what users can accomplish with the library while establishing patterns that make future chart types trivial to add.

By achieving parity with the Datawrapper API's full visualization catalog, this library becomes the definitive Python interface for Datawrapper—not a partial implementation that forces workarounds.

## Current State

**Implemented (8 types):**
- `BarChart` (d3-bars)
- `ColumnChart` (column-chart)
- `LineChart` (d3-lines)
- `AreaChart` (d3-area)
- `ArrowChart` (d3-arrow-plot)
- `MultipleColumnChart` (d3-bars-split)
- `ScatterPlot` (d3-scatter-plot)
- `StackedBarChart` (d3-bars-stacked)

**Not Implemented but Referenced:**
- `locator-map` - Has working tests in `tests/functional/test_maps.py` but no class
- Tables - Mentioned in README and docstrings, no implementation
- `d3-maps` - Explicitly flagged as unsupported in `tests/functional/test_chart_factory.py`

**Completely Missing (based on Datawrapper API):**
- Choropleth maps
- Symbol maps
- Pie charts
- Donut charts
- Election result charts
- Range plots
- Bullet charts
- Waterfall charts
- Treemaps
- Sankey diagrams

## Proposed Future State

Every visualization type supported by the Datawrapper API has a corresponding type-safe Python class. Users can create any chart with the same elegant pattern:

```python
import datawrapper as dw

# Maps
map_chart = dw.LocatorMap(
    title="Coffee Shops in Portland",
    markers=markers_df,
    basemap="stamen-terrain"
)

# Tables
table = dw.DataTable(
    title="Q4 Sales Report",
    data=sales_df,
    searchable=True,
    sortable=True
)

# Pie charts
pie = dw.PieChart(
    title="Market Share 2024",
    data=market_df,
    show_labels=True
)
```

The `chart_factory.py` dynamically maps all API types to their classes, and users never need to touch the deprecated API.

## Key Deliverables

- [ ] **LocatorMap class** - Point, line, and area markers on geographic maps
- [ ] **ChoroplethMap class** - Region-based thematic maps with color scales
- [ ] **SymbolMap class** - Proportional symbol maps
- [ ] **DataTable class** - Interactive, searchable, sortable tables
- [ ] **PieChart class** - Basic pie chart with labels and legends
- [ ] **DonutChart class** - Pie variant with center hole
- [ ] **RangePlot class** - Min/max range visualizations
- [ ] **Treemap class** - Hierarchical area-based visualization
- [ ] **Update chart_factory.py** - Register all new types in the type map
- [ ] **Documentation** - User guides for each new chart type
- [ ] **Test coverage** - Unit, integration, and functional tests for each type

## Prerequisites

None - this can begin immediately. The existing `BaseChart` class and serialization infrastructure provide all necessary foundation.

## Risks & Open Questions

- **API schema discovery**: Some chart types may have undocumented metadata fields requiring reverse-engineering from the Datawrapper web UI
- **Map complexity**: Geographic visualizations require handling GeoJSON, basemap configurations, and projection systems that are significantly more complex than standard charts
- **Table interactivity**: DataTable may need special handling for client-side features like search and sort that work differently than chart visualizations
- **Prioritization**: Which chart types should be implemented first? Recommend prioritizing by user demand (maps > tables > pie > others)

## Notes

Existing test infrastructure in `tests/functional/test_maps.py` (lines 1-89) demonstrates that locator maps already work via the low-level API—the class wrapper is straightforward to build.

Reference `datawrapper/chart_factory.py` lines 54-63 for the current type mapping that needs extension.

The Datawrapper API documentation at https://developer.datawrapper.de/docs/chart-types provides the authoritative list of supported visualization types.
