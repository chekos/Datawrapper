# HTTP Performance Layer

**Category:** Performance
**Quarter:** Q1
**T-shirt Size:** M

## Why This Matters

Every API call currently creates a new TCP connection with full SSL handshake—an expensive operation that adds 100-300ms of overhead per request. For users creating multiple charts or performing bulk operations, this compounds into significant latency. Additionally, rate limit errors (HTTP 429) cause immediate failures with no automatic retry, forcing users to implement their own backoff logic.

A proper HTTP performance layer with connection pooling, retry logic, and rate limit handling transforms the library from "works for simple cases" to "production-ready for automation at scale."

## Current State

HTTP operations in `datawrapper/__main__.py` have several performance issues:

**No Connection Pooling:**
```python
# Each call creates a new connection
response = r.get(url=url, headers=headers, params=params, timeout=timeout)
response = r.post(url, headers=headers, data=json.dumps(data), timeout=timeout)
```

**Rate Limiting - Detection Only:**
```python
if response.status_code == 429:
    raise RateLimitError(response)  # No retry, just fail
```

**No Retry Logic:**
- Transient network errors cause immediate failure
- No exponential backoff
- No configurable retry policies

**Fixed Timeouts:**
- GET: 15 seconds
- POST: 30 seconds
- No adaptive timeout based on operation type

## Proposed Future State

The library includes a robust HTTP client with enterprise-grade reliability:

```python
import datawrapper as dw

# Connection pooling is automatic
client = dw.Datawrapper()  # Reuses connections internally

# Rate limits are handled automatically with exponential backoff
for i in range(100):
    chart = dw.BarChart(title=f"Chart {i}", data=df)
    chart.create()  # Automatically retries on 429, backs off appropriately

# Configurable retry behavior
client = dw.Datawrapper(
    max_retries=5,
    backoff_factor=2.0,
    retry_on=[429, 500, 502, 503, 504],
    timeout=dw.Timeout(connect=5, read=30, write=60)
)
```

Performance improvements:
- 3-10x faster for bulk operations due to connection reuse
- Zero manual retry logic needed
- Graceful degradation under rate limits

## Key Deliverables

- [ ] **Session-based HTTP client** - Use `requests.Session()` for connection pooling
- [ ] **Exponential backoff for rate limits** - Auto-retry 429 errors with configurable delays
- [ ] **Retry-After header parsing** - Respect API's requested wait time
- [ ] **Configurable retry policy** - Max retries, backoff factor, retryable status codes
- [ ] **Adaptive timeouts** - Different timeouts for different operation types
- [ ] **Connection pool configuration** - Max connections, keep-alive settings
- [ ] **Request/response logging** - Debug-level logging for troubleshooting
- [ ] **Metrics collection** - Optional hooks for monitoring request latency/success rates

## Prerequisites

None - this is foundational infrastructure that should be implemented early.

## Risks & Open Questions

- **Breaking changes**: Should retry be opt-in or opt-out? Recommend opt-out (enabled by default) for better UX
- **Rate limit strategy**: Some APIs return Retry-After headers; need to detect and honor them
- **Idempotency**: Retrying POST requests could create duplicate charts. Need idempotency keys or only retry on safe methods?
- **Logging verbosity**: Debug logging should not expose tokens or sensitive data
- **Memory**: Connection pooling uses memory; need sensible defaults for max connections

## Notes

Current HTTP methods location: `datawrapper/__main__.py` lines 84-346

The `requests.Session()` object is imported but never used (line 14: `import requests as r`). Simple change to use session:

```python
class Datawrapper:
    def __init__(self, access_token=_ACCESS_TOKEN):
        self._access_token = access_token
        self._session = requests.Session()
        self._session.headers.update(self._get_auth_header())

    def get(self, url, ...):
        response = self._session.get(url, ...)  # Reuses connection
```

For retry logic, consider `urllib3.util.Retry` or `tenacity` library:

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
```

The `RateLimitError` class at `datawrapper/exceptions.py` (lines 21-52) already captures response details that could be used for smarter retry logic.
