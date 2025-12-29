# Data Pipeline Integration

**Category:** Integration
**Quarter:** Q3
**T-shirt Size:** L

## Why This Matters

Charts are only as good as their data. While the library handles pandas DataFrames elegantly, real-world data lives in databases, cloud storage, APIs, and data warehouses. Users currently must write boilerplate to extract data from these sources before creating charts. Native integrations with popular data tools would make datawrapper a natural extension of existing data pipelines—from dbt to Airflow to Jupyter.

This positions the library as the visualization layer for the modern data stack.

## Current State

Data input is limited to:
- Pandas DataFrames (primary method)
- CSV files (via `add_data()` deprecated method)
- GeoJSON for maps
- Manual data dictionaries

```python
# Users must handle data extraction themselves
import pandas as pd
import datawrapper as dw

# From database
df = pd.read_sql("SELECT * FROM sales", connection)

# From cloud storage
df = pd.read_parquet("s3://bucket/sales.parquet")

# Then create chart
chart = dw.BarChart(title="Sales", data=df)
```

No native support for:
- Database connections
- Cloud storage (S3, GCS, Azure Blob)
- Data warehouse queries (Snowflake, BigQuery, Redshift)
- REST/GraphQL APIs
- Streaming data

## Proposed Future State

Seamless integration with data sources:

```python
import datawrapper as dw

# Direct from database
chart = dw.BarChart(
    title="Sales by Region",
    data=dw.data.from_sql(
        "SELECT region, SUM(amount) FROM sales GROUP BY region",
        connection_string="postgresql://..."
    )
)

# From cloud storage
chart = dw.LineChart(
    title="Daily Metrics",
    data=dw.data.from_s3("s3://analytics/metrics.parquet")
)

# From data warehouse with caching
chart = dw.BarChart(
    title="Revenue",
    data=dw.data.from_bigquery(
        "SELECT date, revenue FROM analytics.daily_revenue",
        cache_ttl=3600  # Cache for 1 hour
    )
)

# Scheduled refresh
chart = dw.BarChart(
    title="Live Sales",
    data=dw.data.from_api(
        "https://api.company.com/sales",
        refresh_schedule="0 * * * *"  # Hourly
    )
)

# Pipeline integration
@dw.pipeline.step
def create_regional_charts(data: pd.DataFrame) -> list[dw.Chart]:
    return [
        dw.BarChart(title=f"{region} Sales", data=region_data)
        for region, region_data in data.groupby("region")
    ]
```

## Key Deliverables

- [ ] **`dw.data` module** - Data source abstraction layer
- [ ] **SQL connectors** - PostgreSQL, MySQL, SQLite support
- [ ] **Cloud storage connectors** - S3, GCS, Azure Blob (Parquet, CSV, JSON)
- [ ] **Data warehouse connectors** - BigQuery, Snowflake, Redshift
- [ ] **REST API connector** - Generic HTTP/JSON data source
- [ ] **Caching layer** - Optional caching for expensive queries
- [ ] **Data transformations** - Common transforms (pivot, aggregate, filter)
- [ ] **Airflow operators** - `DatawrapperCreateChartOperator`, `DatawrapperPublishOperator`
- [ ] **dbt integration** - Post-hook for chart creation from dbt models
- [ ] **Jupyter magics** - `%%datawrapper` cell magic for inline chart creation
- [ ] **Credential management** - Secure handling of database passwords, API keys

## Prerequisites

- Initiative 05 (Batch Operations) - For efficient multi-chart pipelines

## Risks & Open Questions

- **Dependency bloat**: Database drivers are heavy; should they be optional extras?
- **Credential security**: How to safely handle database passwords and API keys?
- **Connection management**: Who owns connection lifecycle? Library or user?
- **Query injection**: SQL connectors must prevent injection attacks
- **Cloud auth**: How to handle AWS IAM, GCP service accounts, Azure AD?
- **Rate limits**: External APIs may have their own rate limits to respect
- **Data freshness**: How to handle stale cache vs real-time requirements?

## Notes

Optional dependencies pattern in `pyproject.toml`:

```toml
[project.optional-dependencies]
sql = ["sqlalchemy", "psycopg2-binary", "pymysql"]
aws = ["boto3", "s3fs"]
gcp = ["google-cloud-bigquery", "gcsfs"]
azure = ["azure-storage-blob"]
all-data = ["datawrapper[sql,aws,gcp,azure]"]
```

The `external-data` field in chart metadata (`datawrapper/charts/models/api_sections.py` line 37) already supports URLs for external data. This could be leveraged:

```python
# Chart with external data URL (data refreshed by Datawrapper)
chart = dw.BarChart(
    title="Sales",
    external_data="https://api.company.com/sales/summary.csv"
)
```

For Airflow integration:

```python
from airflow.decorators import task
from datawrapper.integrations.airflow import DatawrapperOperator

@task
def create_daily_chart():
    chart = dw.BarChart(title="Daily Sales", data=df)
    chart.create()
    chart.publish()
    return chart.chart_id

# Or using operators
create_chart = DatawrapperCreateChartOperator(
    task_id="create_chart",
    chart_type="bar",
    title="{{ ds }} Sales Report",
    data_task_id="extract_data"
)
```

Jupyter magic example:

```python
%%datawrapper bar --title "Sales"
SELECT region, sum(amount) FROM sales GROUP BY region
```
