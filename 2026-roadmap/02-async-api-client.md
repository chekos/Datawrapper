# Async API Client

**Category:** Architecture
**Quarter:** Q1-Q2
**T-shirt Size:** L

## Why This Matters

Modern Python applications—especially those built with FastAPI, Starlette, or async web frameworks—expect async-native libraries. The current synchronous-only implementation forces users to either block their event loops or wrap calls in `asyncio.to_thread()`, creating friction and performance overhead. An async client unlocks efficient concurrent operations: creating 50 charts simultaneously, bulk-updating dashboards, or integrating with real-time data pipelines without blocking.

This is foundational infrastructure that enables future initiatives like batch operations and real-time charts while positioning the library for the async-first Python ecosystem.

## Current State

The library is entirely synchronous, using the `requests` library for HTTP operations:

```python
# datawrapper/__main__.py
import requests as r

def get(self, url: str, params: dict | None = None, timeout: int = 15) -> Any:
    response = r.get(url=url, headers=headers, params=params, timeout=timeout)
    # ...
```

Key limitations:
- Each HTTP call blocks the thread
- No way to parallelize multiple API operations
- Incompatible with async web frameworks without workarounds
- `pytest-asyncio` is installed but unused

## Proposed Future State

The library provides both sync and async clients with identical APIs:

```python
import datawrapper as dw

# Synchronous (existing behavior)
chart = dw.BarChart(title="Sales", data=df)
chart.create()

# Async client for concurrent operations
async with dw.AsyncDatawrapper() as client:
    # Create 10 charts concurrently
    charts = await asyncio.gather(*[
        dw.BarChart(title=f"Region {i}", data=dfs[i]).acreate(client)
        for i in range(10)
    ])

# Async chart methods
chart = dw.BarChart(title="Sales", data=df)
await chart.acreate()  # Uses default async client
await chart.apublish()
```

The async client uses `httpx` or `aiohttp` under the hood, with proper connection pooling, retry logic, and rate limit handling.

## Key Deliverables

- [ ] **AsyncDatawrapper class** - Async version of the main Datawrapper client
- [ ] **Async HTTP layer** - Replace/supplement `requests` with `httpx` (supports both sync and async)
- [ ] **Async chart methods** - Add `acreate()`, `apublish()`, `aupdate()`, `adelete()` to BaseChart
- [ ] **Connection pooling** - Reuse connections across requests
- [ ] **Async context manager** - Proper resource cleanup with `async with`
- [ ] **Concurrent helpers** - Utilities like `gather_charts()` for bulk operations
- [ ] **Documentation** - Guide for async usage patterns
- [ ] **Test suite** - Async tests using pytest-asyncio

## Prerequisites

None - can begin immediately. The async implementation can coexist with sync code.

## Risks & Open Questions

- **Dependency choice**: `httpx` vs `aiohttp`? httpx is recommended as it supports both sync and async with the same API, potentially replacing `requests` entirely
- **API surface**: Should async methods be separate (`acreate`) or use a flag (`create(async_=True)`)? Separate methods are more Pythonic
- **Default client**: Should there be a global async client, or require explicit instantiation?
- **Backwards compatibility**: Sync API must remain the default; async is opt-in
- **Testing complexity**: Mocking async HTTP requires different patterns than sync

## Notes

Current HTTP methods in `datawrapper/__main__.py` (lines 84-346):
- `delete()` - lines 84-133
- `get()` - lines 135-178
- `patch()` - lines 180-232
- `post()` - lines 234-288
- `put()` - lines 290-346

Each would need an async counterpart. Consider using httpx which provides:
```python
# httpx can do both
import httpx

# Sync
response = httpx.get(url)

# Async
async with httpx.AsyncClient() as client:
    response = await client.get(url)
```

This would also enable Initiative 03 (HTTP Performance Layer) since httpx has built-in connection pooling and retry support.
