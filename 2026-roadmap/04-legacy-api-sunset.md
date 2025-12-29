# Legacy API Sunset

**Category:** Technical Debt
**Quarter:** Q2
**T-shirt Size:** M

## Why This Matters

The codebase maintains 20+ deprecated methods in `datawrapper/__main__.py` that duplicate functionality now available through the modern object-oriented chart classes. This dual-API approach creates confusion for users, doubles the maintenance burden, and makes the codebase harder to understand and evolve. The deprecated methods also use different patterns (procedural vs OOP) which fragments the user experience and documentation.

Sunsetting the legacy API reduces cognitive load for maintainers, clarifies the "right way" to use the library, and frees up significant codebase real estate for new features.

## Current State

The main `Datawrapper` class in `__main__.py` (2,786 lines) contains two parallel APIs:

**Modern OOP API (recommended):**
```python
chart = dw.BarChart(title="Sales", data=df)
chart.create()
chart.publish()
```

**Legacy Procedural API (deprecated):**
```python
dw = Datawrapper()
chart_info = dw.create_chart(title="Sales", chart_type="d3-bars")
dw.add_data(chart_id, df)
dw.publish_chart(chart_id)
```

**Deprecated methods identified (with line numbers):**
- `get_chart()` - lines 650-673
- `create_chart()` - lines 686-740
- `update_chart()` - lines 792-836
- `delete_chart()` - lines 981-1001
- `copy_chart()` - lines 1027-1048
- `fork_chart()` - lines 1056-1082
- `publish_chart()` - lines 1100-1130
- `export_chart()` - lines 1159-1225
- `add_data()` - lines 1336-1361
- `chart_data()` - lines 1323-1330
- `get_my_account()` - lines 1564-1572
- And more...

All deprecated methods emit `DeprecationWarning` but remain fully functional.

## Proposed Future State

The library has a clean, single API pattern:

```python
import datawrapper as dw

# Only one way to create charts - the OOP way
chart = dw.BarChart(title="Sales", data=df)
chart.create()

# The Datawrapper class is purely for low-level operations
# like workspace/folder/user management
client = dw.Datawrapper()
workspaces = client.get_workspaces()
```

The deprecated chart methods are removed entirely. Users on older versions see clear migration documentation with automated migration tooling.

## Key Deliverables

- [ ] **Migration guide** - Comprehensive documentation mapping old methods to new patterns
- [ ] **Deprecation timeline** - Announce removal date (suggest 2 major versions ahead)
- [ ] **Migration script** - CLI tool to scan code and suggest replacements
- [ ] **Enhanced deprecation warnings** - Include specific migration instructions in warning messages
- [ ] **Remove deprecated methods** - Delete legacy chart methods from `__main__.py`
- [ ] **Refactor `__main__.py`** - Split remaining functionality into logical modules
- [ ] **Update documentation** - Remove all references to deprecated methods
- [ ] **Update examples** - Ensure all examples use modern API

## Prerequisites

- Initiative 01 (Complete Chart Type Coverage) should be substantially complete so users can migrate to OOP classes for all chart types

## Risks & Open Questions

- **Breaking changes**: Major version bump required; need clear communication
- **User migration burden**: Some users may have extensive code using deprecated API
- **Timing**: How long should deprecated methods coexist with warnings before removal?
- **Edge cases**: Are there use cases the modern API doesn't support that the legacy API does?
- **Large file refactoring**: Splitting `__main__.py` (2,786 lines) requires careful planning

## Notes

Deprecation warnings are currently silenced in tests (`pyproject.toml` lines 146-150):
```toml
filterwarnings = [
    "error",
    "ignore::UserWarning",
    "ignore::DeprecationWarning",  # This hides deprecation issues
]
```

This should be changed to surface deprecation warnings during development.

The legacy methods in `__main__.py` roughly break down as:
- **Chart operations** (~600 lines) - Can be removed; replaced by chart classes
- **Workspace/folder/user management** (~1200 lines) - Keep; not replaced by OOP API
- **HTTP methods** (~250 lines) - Keep; foundational infrastructure
- **Utility methods** (~700 lines) - Evaluate case-by-case

Consider creating separate modules:
- `datawrapper/client.py` - Core HTTP client
- `datawrapper/workspaces.py` - Workspace management
- `datawrapper/users.py` - User management
- `datawrapper/folders.py` - Folder management
