# Real-Time Charts

**Category:** New Feature
**Quarter:** Q4
**T-shirt Size:** XL

## Why This Matters

Static charts capture moments; real-time charts tell evolving stories. Live election results, stock tickers, server metrics, social media trends—these demand visualizations that update as data changes. Currently, updating a chart requires a full API call cycle (fetch, modify, publish), which is too slow for real-time use cases and wastes API quota. Native real-time support would unlock an entirely new category of use cases: live dashboards, streaming analytics, and dynamic data stories.

This transforms Datawrapper from a publishing tool into a real-time visualization platform.

## Current State

Updating a chart requires multiple API calls:

```python
# Polling-based "real-time" (not actually real-time)
while True:
    new_data = fetch_live_data()
    chart.data = new_data
    chart.update()  # API call
    chart.publish()  # Another API call
    time.sleep(30)  # Rate limits force slow updates
```

Problems:
- Minimum ~30 second update interval due to rate limits
- Each update requires 2+ API calls
- No push-based updates; only polling
- Published charts are static snapshots

The `external-data` URL feature theoretically supports dynamic data, but:
- Datawrapper controls refresh interval
- No event-driven updates
- Limited to simple URL fetching

## Proposed Future State

First-class support for real-time data visualization:

```python
import datawrapper as dw

# WebSocket-based live updates
chart = dw.LiveLineChart(
    title="Server CPU Usage",
    initial_data=get_initial_data()
)
chart.create()
chart.publish()

# Push updates via WebSocket
async with chart.live_connection() as conn:
    async for data_point in metric_stream():
        await conn.push(data_point)  # Instant update

# Or streaming with auto-aggregation
chart = dw.StreamingChart(
    title="Tweets per Minute",
    window="5m",
    aggregation="count"
)

async for tweet in twitter_stream:
    chart.ingest(tweet)  # Handles windowing and updates

# Declarative real-time dashboard
dashboard = dw.LiveDashboard(
    title="System Monitoring",
    charts=[
        dw.LiveLineChart(title="CPU", data_source=cpu_stream),
        dw.LiveLineChart(title="Memory", data_source=mem_stream),
        dw.LiveBarChart(title="Requests/s", data_source=request_stream)
    ],
    refresh_rate="1s"
)
```

Architecture:
- WebSocket connection for push-based updates
- Client-side rendering for sub-second updates
- Server-sent events (SSE) as fallback
- Intelligent batching for high-frequency data

## Key Deliverables

- [ ] **`LiveChart` base class** - Charts that support real-time updates
- [ ] **WebSocket transport** - Push updates via WebSocket connection
- [ ] **SSE fallback** - Server-sent events for simpler deployments
- [ ] **Data windowing** - Rolling windows for time-series data
- [ ] **Aggregation engine** - Real-time aggregations (sum, avg, count, percentiles)
- [ ] **Rate limiting client-side** - Batch updates to avoid overwhelming clients
- [ ] **Offline buffering** - Queue updates during disconnection
- [ ] **Live dashboard** - Coordinated real-time multi-chart views
- [ ] **Historical playback** - Replay recorded data streams
- [ ] **Alerting hooks** - Trigger alerts when data crosses thresholds
- [ ] **Embeddable widget** - JavaScript widget for embedding live charts

## Prerequisites

- Initiative 02 (Async API Client) - Required for WebSocket and streaming support
- Initiative 09 (Gallery Builder) - For live dashboards
- Investigation of Datawrapper's real-time capabilities

## Risks & Open Questions

- **Datawrapper API support**: Does the Datawrapper API support WebSocket or SSE? If not, this may require client-side rendering
- **Infrastructure**: Real-time features may require a proxy server for WebSocket termination
- **Scale**: How many concurrent live charts can be supported?
- **Cost**: Real-time features may have different pricing implications
- **Browser compatibility**: WebSocket support in embedded contexts
- **Data retention**: How long to keep historical data for live charts?
- **Security**: Authentication for WebSocket connections

## Notes

If Datawrapper doesn't natively support real-time updates, this could be implemented as a client-side overlay:

```
┌─────────────────────────────────────────────────────┐
│                  Architecture                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Python App ──WebSocket──▶ Live Proxy Server        │
│                                │                    │
│                                ▼                    │
│                    ┌───────────────────┐            │
│                    │ Client Browser    │            │
│                    │ ┌───────────────┐ │            │
│                    │ │ Datawrapper   │ │            │
│                    │ │ Chart (base)  │ │            │
│                    │ └───────────────┘ │            │
│                    │ ┌───────────────┐ │            │
│                    │ │ Live Overlay  │◀┼─WebSocket  │
│                    │ │ (JS Widget)   │ │            │
│                    │ └───────────────┘ │            │
│                    └───────────────────┘            │
└─────────────────────────────────────────────────────┘
```

The external data URL feature could be leveraged for slower updates:

```python
# Set up a data endpoint that this library manages
chart = dw.BarChart(
    title="Sales",
    external_data="https://yourserver.com/api/chart-data/abc123"
)

# Library provides the data endpoint
@app.get("/api/chart-data/{chart_id}")
def get_chart_data(chart_id: str):
    return get_current_data(chart_id)
```

For true real-time, consider integrating with streaming platforms:
- Apache Kafka
- Redis Pub/Sub
- AWS Kinesis
- Google Pub/Sub

The `rich` library's `Live` display could provide terminal-based live chart previews during development:

```python
from rich.live import Live
from rich.table import Table

with Live(chart.to_rich_table(), refresh_per_second=4) as live:
    for data in stream:
        chart.update(data)
        live.update(chart.to_rich_table())
```
