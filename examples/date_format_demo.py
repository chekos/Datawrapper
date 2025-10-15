"""Demo script showing DateFormat enum usage in Datawrapper charts.

This example demonstrates how to use the DateFormat enum for formatting
date values in various chart types.
"""

from datawrapper import Datawrapper
from datawrapper.charts import AreaChart, ColumnChart, LineChart, ScatterPlot
from datawrapper.charts.models import DateFormat, NumberFormat

# Initialize Datawrapper (requires API token)
dw = Datawrapper()

# Example 1: LineChart with date formatting
print("Example 1: LineChart with DateFormat enum")
line_chart = LineChart(
    title="Temperature Over Time",
    x_grid_format=DateFormat.MONTH_ABBREVIATED_WITH_YEAR,  # "Jan '24"
    y_grid_format=NumberFormat.ONE_DECIMAL,  # "23.5"
)
print(f"  X-axis format: {line_chart.x_grid_format}")
print(f"  Y-axis format: {line_chart.y_grid_format}")
print()

# Example 2: AreaChart with multiline date format
print("Example 2: AreaChart with multiline date format")
area_chart = AreaChart(
    title="Sales by Quarter",
    x_grid_format=DateFormat.YEAR_QUARTER_MULTILINE,  # "2024" on line 2, "Q1" on line 1
    y_grid_format=NumberFormat.CURRENCY_ABBREVIATED,  # "$1.3m"
)
print(f"  X-axis format: {area_chart.x_grid_format}")
print(f"  Y-axis format: {area_chart.y_grid_format}")
print()

# Example 3: ColumnChart with locale-dependent date format
print("Example 3: ColumnChart with locale-dependent date format")
column_chart = ColumnChart(
    title="Monthly Revenue",
    x_grid_format=DateFormat.LOCALE_DATE_LONG,  # "January 30, 2024" (en-US)
    y_grid_format=NumberFormat.THOUSANDS_SEPARATOR,  # "10,000"
)
print(f"  X-axis format: {column_chart.x_grid_format}")
print(f"  Y-axis format: {column_chart.y_grid_format}")
print()

# Example 4: Backwards compatibility with raw strings
print("Example 4: Backwards compatibility with raw format strings")
line_chart_custom = LineChart(
    title="Custom Formats",
    x_grid_format="DD.MM.YYYY",  # Custom date format
    y_grid_format="0,0.00",  # Custom number format
)
print(f"  X-axis format: {line_chart_custom.x_grid_format}")
print(f"  Y-axis format: {line_chart_custom.y_grid_format}")
print()

# Example 5: Mixing enum and string formats
print("Example 5: Mixing enum and string formats")
area_chart_mixed = AreaChart(
    title="Mixed Format Example",
    x_grid_format=DateFormat.MONTH_ABBREVIATED,  # Using enum
    y_grid_format="$0.[00]a",  # Using custom string
)
print(f"  X-axis format: {area_chart_mixed.x_grid_format}")
print(f"  Y-axis format: {area_chart_mixed.y_grid_format}")
print()

# Example 6: Sport season formats
print("Example 6: Sport season formats")
column_chart_sport = ColumnChart(
    title="Team Performance by Season",
    x_grid_format=DateFormat.SPORT_SEASON_ABBREVIATED,  # "'15-'16"
    y_grid_format=NumberFormat.INTEGER,  # "42"
)
print(f"  X-axis format: {column_chart_sport.x_grid_format}")
print(f"  Y-axis format: {column_chart_sport.y_grid_format}")
print()

# Example 7: All available DateFormat options
print("Example 7: All available DateFormat enum values")
print("=" * 60)
for name, member in DateFormat.__members__.items():
    print(f"  DateFormat.{name:30s} = '{member.value}'")
print()

# Example 8: Common date format patterns
print("Example 8: Common date format use cases")
print("=" * 60)
print("  Year only:        ", DateFormat.YEAR_FULL.value)
print("  Month & Year:     ", DateFormat.MONTH_ABBREVIATED_WITH_YEAR.value)
print("  Full date:        ", DateFormat.MONTH_DAY_YEAR_FULL.value)
print("  Quarter:          ", DateFormat.YEAR_QUARTER.value)
print("  Multiline:        ", DateFormat.YEAR_MONTH_MULTILINE.value)
print("  Locale-dependent: ", DateFormat.LOCALE_DATE_LONG.value)
print()

print("✓ DateFormat enum provides type-safe, readable date formatting")
print("✓ Backwards compatible with raw format strings")
print("✓ Works seamlessly with NumberFormat enum")
