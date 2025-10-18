# Exporting Charts

This guide covers exporting Datawrapper charts in various formats including PNG, PDF, and SVG.

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
