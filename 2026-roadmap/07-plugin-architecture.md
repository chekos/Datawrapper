# Plugin Architecture

**Category:** Architecture
**Quarter:** Q3
**T-shirt Size:** L

## Why This Matters

The Datawrapper API evolves independently of this library. New chart types appear, new metadata fields are added, and regional variants emerge. Currently, supporting a new chart type requires changes to the core library, a release cycle, and user updates. A plugin architecture allows the community to extend the library without waiting for core maintainers, enables enterprise teams to add proprietary visualizations, and future-proofs the library against API changes.

This transforms the library from a static wrapper into an extensible platform.

## Current State

Chart types are hardcoded in `datawrapper/chart_factory.py`:

```python
chart_type_map = {
    "d3-lines": LineChart,
    "d3-bars": BarChart,
    "column-chart": ColumnChart,
    "d3-area": AreaChart,
    "d3-arrow-plot": ArrowChart,
    "d3-bars-split": MultipleColumnChart,
    "d3-scatter-plot": ScatterPlot,
    "d3-bars-stacked": StackedBarChart,
}
```

Adding a new chart type requires:
1. Creating a new class in `datawrapper/charts/`
2. Adding enums, models, serializers
3. Updating `chart_factory.py`
4. Adding tests and documentation
5. Releasing a new library version

There's no way for users to register custom chart types.

## Proposed Future State

A plugin system that allows runtime extension:

```python
import datawrapper as dw
from my_company.charts import CustomGaugeChart

# Register a custom chart type
dw.register_chart_type("custom-gauge", CustomGaugeChart)

# Use it like any built-in chart
chart = dw.CustomGaugeChart(title="Performance", data=df)
chart.create()

# Or discover it via factory
chart = dw.get_chart("abc123")  # Returns CustomGaugeChart if type matches
```

Plugin packages can be installed and auto-discovered:

```bash
pip install datawrapper-charts-financial  # Adds candlestick, waterfall, etc.
```

```python
# Auto-discovered from entry points
import datawrapper as dw
chart = dw.CandlestickChart(title="AAPL", data=ohlc_df)  # Just works
```

## Key Deliverables

- [ ] **Chart type registry** - Central registry for chart classes
- [ ] **`register_chart_type()` API** - Runtime registration of custom charts
- [ ] **Entry point discovery** - Auto-discover plugins from `datawrapper.charts` entry point
- [ ] **Base chart protocol** - Define interface requirements for chart plugins
- [ ] **Plugin validation** - Verify plugins implement required methods
- [ ] **Serializer plugins** - Allow custom serializers for new data types
- [ ] **Enum extension** - Allow plugins to add enum values
- [ ] **Plugin template** - Cookiecutter template for creating chart plugins
- [ ] **Plugin documentation** - Guide for creating and publishing plugins
- [ ] **Example plugin package** - Reference implementation for a custom chart

## Prerequisites

- Initiative 01 (Complete Chart Type Coverage) - Establishes patterns for chart classes
- Initiative 04 (Legacy API Sunset) - Clean API makes plugin interface clearer

## Risks & Open Questions

- **Interface stability**: Plugin API becomes a contract; breaking changes are costly
- **Validation complexity**: How to validate that a plugin handles all API variations?
- **Namespace conflicts**: What if two plugins register the same chart type?
- **Version compatibility**: Plugins may break with library updates
- **Testing plugins**: How to test plugins in isolation from the core library?
- **Discovery mechanism**: Entry points vs explicit imports vs configuration file?

## Notes

Python entry points provide a clean discovery mechanism. In a plugin's `pyproject.toml`:

```toml
[project.entry-points."datawrapper.charts"]
candlestick = "dw_financial:CandlestickChart"
waterfall = "dw_financial:WaterfallChart"
```

Then in the main library:

```python
from importlib.metadata import entry_points

def discover_chart_plugins():
    eps = entry_points(group="datawrapper.charts")
    for ep in eps:
        chart_class = ep.load()
        register_chart_type(ep.name, chart_class)
```

The current `BaseChart` class (`datawrapper/charts/base.py`) provides a solid foundation. Plugins would inherit from it:

```python
from datawrapper.charts import BaseChart
from pydantic import Field

class CandlestickChart(BaseChart):
    chart_type = "candlestick"  # Maps to Datawrapper API type

    # Custom fields
    up_color: str = Field(default="#00ff00")
    down_color: str = Field(default="#ff0000")

    def _get_visualize_metadata(self):
        return {
            "up-color": self.up_color,
            "down-color": self.down_color,
            **super()._get_visualize_metadata()
        }
```

The mixin pattern used in `datawrapper/charts/models/mixins.py` could be extended to provide reusable functionality for plugin authors.
