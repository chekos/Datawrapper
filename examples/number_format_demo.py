"""Demo of NumberFormat enum usage in Datawrapper charts.

This example demonstrates how to use the NumberFormat enum to format
numbers in various chart types with readable, semantic names.
"""

from datawrapper.charts import BarChart, ColumnChart, LineChart, NumberFormat

# Example 1: Using NumberFormat enum with BarChart
bar_chart = BarChart(
    title="Sales by Region",
    axis_label_format=NumberFormat.THOUSANDS_SEPARATOR,  # Format as "10,000"
    value_label_format=NumberFormat.ABBREVIATED_ONE_DECIMAL,  # Format as "123.4k"
)

# Example 2: Using NumberFormat enum with ColumnChart
column_chart = ColumnChart(
    title="Revenue Growth",
    y_grid_format=NumberFormat.THOUSANDS_WITH_OPTIONAL_DECIMALS,  # Format as "1,000[.00]"
    value_labels_format=NumberFormat.PERCENT_TWO_DECIMALS,  # Format as "0.00%"
)

# Example 3: Using NumberFormat enum with LineChart
line_chart = LineChart(
    title="Temperature Trends",
    y_grid_format=NumberFormat.ONE_DECIMAL,  # Format as "0.0"
    value_labels_format=NumberFormat.TWO_DECIMALS,  # Format as "0.00"
)

# Example 4: Backwards compatibility - raw format strings still work
legacy_chart = BarChart(
    title="Legacy Format",
    axis_label_format="0,0",  # Still works with raw format string
    value_label_format="$0.[00]a",  # Custom format string
)

# Example 5: Comparing enum vs raw string
print("Enum approach (recommended):")
print(f"  NumberFormat.THOUSANDS_SEPARATOR = {NumberFormat.THOUSANDS_SEPARATOR.value}")
print(f"  NumberFormat.PERCENT_TWO_DECIMALS = {NumberFormat.PERCENT_TWO_DECIMALS.value}")

print("\nRaw string approach (still supported):")
print(f"  '0,0' = 0,0")
print(f"  '0.00%' = 0.00%")

print("\nBoth approaches produce the same result!")

# Example 6: All available formats
print("\n=== Available NumberFormat Options ===")
print(f"AUTO: {NumberFormat.AUTO.value}")
print(f"THOUSANDS_WITH_OPTIONAL_DECIMALS: {NumberFormat.THOUSANDS_WITH_OPTIONAL_DECIMALS.value}")
print(f"INTEGER: {NumberFormat.INTEGER.value}")
print(f"ONE_DECIMAL: {NumberFormat.ONE_DECIMAL.value}")
print(f"TWO_DECIMALS: {NumberFormat.TWO_DECIMALS.value}")
print(f"THREE_DECIMALS: {NumberFormat.THREE_DECIMALS.value}")
print(f"UP_TO_ONE_DECIMAL: {NumberFormat.UP_TO_ONE_DECIMAL.value}")
print(f"UP_TO_TWO_DECIMALS: {NumberFormat.UP_TO_TWO_DECIMALS.value}")
print(f"PERCENT_INTEGER: {NumberFormat.PERCENT_INTEGER.value}")
print(f"PERCENT_ONE_DECIMAL: {NumberFormat.PERCENT_ONE_DECIMAL.value}")
print(f"PERCENT_TWO_DECIMALS: {NumberFormat.PERCENT_TWO_DECIMALS.value}")
print(f"PERCENT_UP_TO_ONE_DECIMAL: {NumberFormat.PERCENT_UP_TO_ONE_DECIMAL.value}")
print(f"PERCENT_UP_TO_TWO_DECIMALS: {NumberFormat.PERCENT_UP_TO_TWO_DECIMALS.value}")
print(f"THOUSANDS_SEPARATOR: {NumberFormat.THOUSANDS_SEPARATOR.value}")
print(f"ORDINAL: {NumberFormat.ORDINAL.value}")
print(f"ABBREVIATED: {NumberFormat.ABBREVIATED.value}")
print(f"ABBREVIATED_ONE_DECIMAL: {NumberFormat.ABBREVIATED_ONE_DECIMAL.value}")
print(f"ABBREVIATED_TWO_DECIMALS: {NumberFormat.ABBREVIATED_TWO_DECIMALS.value}")
print(f"ABBREVIATED_THREE_DECIMALS: {NumberFormat.ABBREVIATED_THREE_DECIMALS.value}")

print("\n=== Advanced Number Formats ===")
print(f"PLUS_SIGN: {NumberFormat.PLUS_SIGN.value}")
print(f"PLUS_SIGN_PERCENT: {NumberFormat.PLUS_SIGN_PERCENT.value}")
print(f"CURRENCY_ABBREVIATED_WITH_PLUS: {NumberFormat.CURRENCY_ABBREVIATED_WITH_PLUS.value}")
print(f"CURRENCY_ABBREVIATED: {NumberFormat.CURRENCY_ABBREVIATED.value}")
print(f"CURRENCY_OPTIONAL_DECIMALS: {NumberFormat.CURRENCY_OPTIONAL_DECIMALS.value}")
print(f"ZERO_PADDED: {NumberFormat.ZERO_PADDED.value}")
print(f"PARENTHESES_FOR_NEGATIVES: {NumberFormat.PARENTHESES_FOR_NEGATIVES.value}")
print(f"LEADING_DECIMAL: {NumberFormat.LEADING_DECIMAL.value}")
print(f"SCIENTIFIC_NOTATION: {NumberFormat.SCIENTIFIC_NOTATION.value}")
print(f"SCIENTIFIC_NOTATION_DECIMALS: {NumberFormat.SCIENTIFIC_NOTATION_DECIMALS.value}")
print(f"ABSOLUTE_VALUE: {NumberFormat.ABSOLUTE_VALUE.value}")

# Example 7: Advanced format use cases
print("\n=== Advanced Format Use Cases ===")

# Percent change with plus sign
change_chart = ColumnChart(
    title="Year-over-Year Change",
    value_labels_format=NumberFormat.PLUS_SIGN_PERCENT,  # Shows "+7%" or "-3%"
)
print(f"Percent change: {NumberFormat.PLUS_SIGN_PERCENT.value}")

# Currency with abbreviation
revenue_chart = BarChart(
    title="Revenue by Division",
    axis_label_format=NumberFormat.CURRENCY_ABBREVIATED,  # Shows "$1.3m"
)
print(f"Currency abbreviated: {NumberFormat.CURRENCY_ABBREVIATED.value}")

# Scientific notation for large numbers
science_chart = LineChart(
    title="Population Growth",
    y_grid_format=NumberFormat.SCIENTIFIC_NOTATION_DECIMALS,  # Shows "1.30e+6"
)
print(f"Scientific notation: {NumberFormat.SCIENTIFIC_NOTATION_DECIMALS.value}")
