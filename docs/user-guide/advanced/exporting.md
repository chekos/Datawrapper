# Exporting Charts

Export Datawrapper charts in various formats including PNG, PDF, and SVG. In many cases, exporting can be done directly through the chart object methods and these methods should be considered deprecated. However, for advanced use cases or when working directly with the Datawrapper API, the following examples demonstrate how to export charts using the client. Where possible, prefer using the chart object's export methods.

## Export as PNG

Export a chart as a PNG image:

```python
client.export_chart(
    chart_id="abc123",
    output="png",
    filepath="chart.png",
    display=True  # Opens the image after saving
)
```

## Export as PDF

Export a chart as a PDF:

```python
client.export_chart(
    chart_id="abc123",
    output="pdf",
    filepath="chart.pdf"
)
```

## Export as SVG

Export a chart as an SVG:

```python
client.export_chart(
    chart_id="abc123",
    output="svg",
    filepath="chart.svg"
)
```

## Export with Custom Dimensions

Specify custom dimensions for the export:

```python
client.export_chart(
    chart_id="abc123",
    output="png",
    filepath="chart.png",
    width=1200,
    height=800
)
```
