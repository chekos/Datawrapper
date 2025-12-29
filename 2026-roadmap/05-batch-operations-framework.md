# Batch Operations Framework

**Category:** New Feature
**Quarter:** Q2
**T-shirt Size:** L

## Why This Matters

Data teams often need to create, update, or manage dozens or hundreds of charts at once—think weekly reports with regional breakdowns, or updating all charts when a data source changes. Currently, each operation is a separate API call, leading to rate limiting, slow performance, and complex retry logic. A batch operations framework transforms these workflows from "painful scripts with sleep() calls" to "one-liner bulk updates with automatic optimization."

This is a force multiplier for power users and automation pipelines.

## Current State

All operations are single-chart:

```python
# Painful: Creating 50 regional charts
charts = []
for region in regions:
    chart = dw.BarChart(title=f"{region} Sales", data=get_data(region))
    chart.create()  # API call
    chart.publish()  # API call
    charts.append(chart)
    time.sleep(0.5)  # Manual rate limit handling
```

There's no batching, no automatic parallelization, and no intelligent rate limit handling. The test cleanup code in `tests/conftest.py` (lines 475-481) shows the problem:

```python
for workspace in workspaces["list"]:
    if workspace["name"].startswith("Test Workspace"):
        try:
            dw.delete_workspace(workspace["slug"])  # Sequential!
        except RateLimitError:
            break  # Just gives up on rate limit
```

## Proposed Future State

The library provides intelligent batch operations with automatic optimization:

```python
import datawrapper as dw

# Bulk create with automatic rate limit handling
charts = [
    dw.BarChart(title=f"{region} Sales", data=get_data(region))
    for region in regions
]
results = dw.batch.create(charts, max_concurrent=10)

# Bulk update
dw.batch.update(charts, metadata={"theme": "dark-mode"})

# Bulk publish
dw.batch.publish(charts)

# Bulk delete with dry-run
dw.batch.delete(chart_ids, dry_run=True)  # Preview what would be deleted

# Query and update pattern
charts = dw.query.charts(folder_id="marketing", created_after="2024-01-01")
dw.batch.update(charts, metadata={"archived": True})
```

Under the hood:
- Automatic parallelization respecting rate limits
- Progress callbacks for long operations
- Transaction-like rollback on partial failures
- Dry-run mode for safety

## Key Deliverables

- [ ] **`dw.batch` module** - Container for batch operations
- [ ] **`batch.create(charts)`** - Bulk chart creation
- [ ] **`batch.update(charts, metadata)`** - Bulk metadata updates
- [ ] **`batch.publish(charts)`** - Bulk publishing
- [ ] **`batch.delete(charts)`** - Bulk deletion with safeguards
- [ ] **`batch.export(charts, format)`** - Bulk export to files
- [ ] **Rate limit aware executor** - Smart concurrency with backoff
- [ ] **Progress reporting** - Callbacks and progress bars (rich integration)
- [ ] **Dry-run mode** - Preview operations without executing
- [ ] **Error aggregation** - Collect all errors, don't fail on first
- [ ] **Retry failed items** - Automatic retry of failed individual items

## Prerequisites

- Initiative 03 (HTTP Performance Layer) - Required for intelligent rate limit handling
- Initiative 02 (Async API Client) - Beneficial for parallel operations but not strictly required

## Risks & Open Questions

- **Rate limit fairness**: How aggressive should parallelization be? Need to respect API quotas
- **Partial failures**: What happens when 45 of 50 charts succeed? Options:
  - Return partial results with error list
  - Rollback successful operations
  - Retry failed operations
- **Memory**: Large batch operations could use significant memory for tracking
- **Idempotency**: If a batch is interrupted and rerun, how to avoid duplicates?
- **Progress persistence**: For very long operations, should progress be persisted to allow resume?

## Notes

The `rich` library is already a dependency and provides excellent progress bars:

```python
from rich.progress import track

for chart in track(charts, description="Creating charts..."):
    chart.create()
```

Consider making batch operations return a `BatchResult` object:

```python
@dataclass
class BatchResult:
    successful: list[Chart]
    failed: list[tuple[Chart, Exception]]
    skipped: list[Chart]

    @property
    def success_rate(self) -> float:
        total = len(self.successful) + len(self.failed) + len(self.skipped)
        return len(self.successful) / total if total > 0 else 0.0
```

For async operations, `asyncio.gather()` with `return_exceptions=True` allows collecting all results without failing fast:

```python
results = await asyncio.gather(*tasks, return_exceptions=True)
successful = [r for r in results if not isinstance(r, Exception)]
failed = [r for r in results if isinstance(r, Exception)]
```
