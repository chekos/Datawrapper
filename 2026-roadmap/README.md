# Datawrapper Python Library: 2026 Strategic Roadmap

## Executive Summary

This roadmap outlines a transformative vision for the Datawrapper Python library over the next four quarters. Starting from a solid foundation—a well-typed, well-tested Python wrapper for the Datawrapper API—these initiatives will evolve the library into the **definitive data visualization toolkit for Python developers**.

The roadmap addresses three strategic imperatives:

1. **Completeness**: Full parity with the Datawrapper API (all chart types, all features)
2. **Performance**: Enterprise-grade reliability with async support, connection pooling, and intelligent batching
3. **Extensibility**: A platform that grows with the ecosystem through plugins, integrations, and real-time capabilities

By Q4 2026, developers will be able to go from raw data to published, real-time dashboards in minutes—programmatically, reliably, and at scale.

---

## High-Level Themes

### Q1: Foundation & Performance
- Complete the chart type catalog
- Modernize HTTP layer with pooling and retries
- Begin async client development

### Q2: Clean Architecture & Efficiency
- Remove legacy API debt
- Launch batch operations framework
- Ship command-line interface

### Q3: Extensibility & Integration
- Release plugin architecture
- Build data pipeline connectors
- Begin gallery/dashboard work

### Q4: Advanced Capabilities
- Complete interactive galleries
- Launch real-time visualization features
- Pursue moonshot initiative

---

## Initiative Overview

| # | Initiative | Category | Quarter | Size | Description |
|---|------------|----------|---------|------|-------------|
| 00 | [AI-Powered Visualization Assistant](./00-moonshot.md) | Moonshot | Q4+ | XXL | Natural language to charts; intelligent recommendations |
| 01 | [Complete Chart Type Coverage](./01-complete-chart-type-coverage.md) | New Feature | Q1 | XL | Maps, tables, pie charts, and all missing types |
| 02 | [Async API Client](./02-async-api-client.md) | Architecture | Q1-Q2 | L | Async/await support for concurrent operations |
| 03 | [HTTP Performance Layer](./03-http-performance-layer.md) | Performance | Q1 | M | Connection pooling, retry logic, rate limit handling |
| 04 | [Legacy API Sunset](./04-legacy-api-sunset.md) | Technical Debt | Q2 | M | Remove deprecated methods, refactor codebase |
| 05 | [Batch Operations Framework](./05-batch-operations-framework.md) | New Feature | Q2 | L | Bulk create/update/delete with smart concurrency |
| 06 | [Command-Line Interface](./06-command-line-interface.md) | DX Improvement | Q2-Q3 | M | Full-featured CLI for terminal workflows |
| 07 | [Plugin Architecture](./07-plugin-architecture.md) | Architecture | Q3 | L | Extensible chart type system with discovery |
| 08 | [Data Pipeline Integration](./08-data-pipeline-integration.md) | Integration | Q3 | L | Database, cloud storage, and workflow connectors |
| 09 | [Interactive Gallery Builder](./09-interactive-gallery-builder.md) | New Feature | Q3-Q4 | XL | Multi-chart dashboards and templated reports |
| 10 | [Real-Time Charts](./10-real-time-charts.md) | New Feature | Q4 | XL | Live-updating visualizations with streaming data |

---

## Dependency Graph

```
                                    ┌────────────────────────┐
                                    │   00. AI-Powered       │
                                    │   Visualization        │
                                    │   (Moonshot)           │
                                    └───────────┬────────────┘
                                                │
                    ┌───────────────────────────┼────────────────────────────┐
                    │                           │                            │
                    ▼                           ▼                            ▼
        ┌───────────────────┐     ┌───────────────────────┐    ┌────────────────────┐
        │  10. Real-Time    │     │  09. Gallery Builder  │    │  08. Data Pipeline │
        │      Charts       │     │                       │    │     Integration    │
        └─────────┬─────────┘     └──────────┬────────────┘    └─────────┬──────────┘
                  │                          │                           │
                  │                          │                           │
                  ▼                          ▼                           │
        ┌───────────────────┐     ┌───────────────────────┐              │
        │  02. Async API    │     │  05. Batch Operations │◀─────────────┘
        │     Client        │     │                       │
        └─────────┬─────────┘     └──────────┬────────────┘
                  │                          │
                  │                          ├────────────────────────────┐
                  ▼                          ▼                            ▼
        ┌───────────────────┐     ┌───────────────────────┐    ┌────────────────────┐
        │  03. HTTP Perf    │     │  06. CLI              │    │  07. Plugin        │
        │     Layer         │     │                       │    │     Architecture   │
        └───────────────────┘     └───────────────────────┘    └─────────┬──────────┘
                                                                         │
                  ┌──────────────────────────────────────────────────────┘
                  │
                  ▼
        ┌───────────────────────────────────────────────────────────────────┐
        │                   01. Complete Chart Type Coverage                │
        │                                                                   │
        │  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐  │
        │  │  LocatorMap     │   │  DataTable      │   │  PieChart       │  │
        │  │  ChoroplethMap  │   │  DonutChart     │   │  Treemap        │  │
        │  │  SymbolMap      │   │  RangePlot      │   │  ...            │  │
        │  └─────────────────┘   └─────────────────┘   └─────────────────┘  │
        └───────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
                              ┌───────────────────────┐
                              │  04. Legacy API       │
                              │      Sunset           │
                              └───────────────────────┘
```

### Critical Path

1. **Q1**: Start with 01 (Chart Types), 03 (HTTP), and begin 02 (Async) in parallel
2. **Q2**: Complete 02 (Async), then 04 (Legacy Sunset) and 05 (Batch) can proceed
3. **Q2-Q3**: 06 (CLI) depends on 05 (Batch); 07 (Plugin) depends on 01 (Chart Types)
4. **Q3**: 08 (Data Pipeline) can run parallel to 07 (Plugin) and 09 (Gallery)
5. **Q3-Q4**: 09 (Gallery) needs 01, 05, and ideally 08
6. **Q4**: 10 (Real-Time) requires 02 (Async) and benefits from 09 (Gallery)
7. **Q4+**: Moonshot builds on everything, especially 01, 08, 09, 10

---

## Success Metrics

### Library Adoption
- PyPI downloads: 2x growth by Q4
- GitHub stars: Reach 1,000
- Active contributors: 10+ regular contributors

### Technical Health
- Test coverage: Maintain >90%
- Type coverage: 100% of public API
- Documentation coverage: All public methods documented

### Feature Completeness
- Chart types: 100% parity with Datawrapper API
- API coverage: All v3 API endpoints wrapped
- Platform support: Python 3.10-3.14

### Performance
- HTTP performance: 5x faster bulk operations via connection pooling
- Async adoption: 50% of new users using async patterns
- Rate limit handling: Zero user-visible rate limit errors

---

## Risk Factors

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Datawrapper API changes | Medium | High | Monitor API changelog; version-pin API compatibility |
| Scope creep | High | Medium | Strict prioritization; say no to out-of-scope features |
| Community adoption | Medium | Medium | Invest in documentation and examples |
| Maintainer bandwidth | Medium | High | Build contributor community; clear contribution guidelines |
| Breaking changes | Low | High | Semantic versioning; migration guides; deprecation periods |

---

## How to Use This Roadmap

Each initiative file contains:
- **Why This Matters**: Strategic justification
- **Current State**: What exists today
- **Proposed Future State**: The vision with code examples
- **Key Deliverables**: Specific, actionable items
- **Prerequisites**: Dependencies on other initiatives
- **Risks & Open Questions**: Known unknowns
- **Notes**: Implementation hints and references to existing code

Start with the initiatives that have no prerequisites (01, 03) or tackle the moonshot as a north-star vision that guides all other work.

---

## Contributing

This roadmap is a living document. To propose changes:

1. Open an issue describing the change
2. Reference specific initiative files
3. Explain how it affects the dependency graph
4. Consider timeline and resource implications

The roadmap will be reviewed quarterly and adjusted based on community feedback, API changes, and strategic priorities.
