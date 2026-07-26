# Data transformations

Datawrapper stores Check & Describe transformation settings under `metadata.data`.
The object-oriented chart API exposes those settings in two compatible ways:

1. Pass the nested `transformations=` argument for full API-shaped control.
2. Pass supported transformation settings directly to a chart as top-level keyword
   arguments when you only need the common cases.

The flat fields are a small ergonomic layer over the existing `Transform` model.
They do not replace `Transform`, and they serialize to the same
`metadata.data` payload that Datawrapper expects.

## Flat transformation fields

Use top-level fields when you want to set one or two data transformations without
constructing a nested `dw.Transform(...)` object:

```python
chart = dw.AreaChart(
    title="Migration to the US by world region, 1820-2009",
    data=df,
    transpose=True,
)
```

The supported flat fields match the current `Transform` model:

- `transpose`
- `vertical_header` / `vertical-header`
- `horizontal_header` / `horizontal-header`
- `column_order` / `column-order`
- `column_format` / `column-format`
- `changes`
- `external_data` / `external-data`
- `use_datawrapper_cdn` / `use-datawrapper-cdn`
- `upload_method` / `upload-method`

`column_format` accepts the same inputs as `Transform.column_format`: a list of
`dw.ColumnFormat` objects or dictionaries, or an API-shaped dictionary keyed by
column name. For example:

```python
chart = dw.LineChart(
    title="Global land temperature in July, 1753-2015",
    data=df,
    column_format=[
        dw.ColumnFormat(
            column="LandAverageTemperature",
            number_append=" °C",
        )
    ],
)
```

Real Datawrapper API responses and Datawrapper Academy examples often represent
`metadata.data.column-format` as a dictionary keyed by column name. That shape can
also be used at the top level:

```python
chart = dw.LineChart(
    title="Global land temperature in July, 1753-2015",
    data=df,
    column_format={
        "LandAverageTemperature": {
            "type": "auto",
            "ignore": False,
            "number-append": " °C",
            "number-format": "-",
            "number-divisor": 0,
            "number-prepend": "",
        }
    },
)
```

## When to use `Transform`

Keep using the nested `transformations=` argument when you are round-tripping API
metadata, preserving advanced Datawrapper response shapes, or grouping multiple
data settings explicitly:

```python
chart = dw.BarChart(
    title="Corrected values",
    data=df,
    transformations=dw.Transform(
        changes=[
            dw.DataChange(
                row=9,
                column=3,
                value="1.7",
                time=1573134075869,
                previous="0.7",
            )
        ]
    ),
)
```

## Combining flat and nested forms

Flat fields compose with `transformations=` by filling settings that are not set
inside the nested `Transform` object:

```python
chart = dw.LineChart(
    title="Formatted and reordered",
    data=df,
    transformations=dw.Transform(column_order=[0, 2, 1]),
    column_format=[dw.ColumnFormat(column="sales", type="number")],
)
```

If both forms provide the same setting, matching values are accepted. Conflicting
values raise a validation error so the chart does not silently choose one source
over the other:

```python
# Raises a validation error: transpose is True in one place and False in another.
chart = dw.LineChart(
    title="Conflicting settings",
    data=df,
    transformations=dw.Transform(transpose=True),
    transpose=False,
)
```

For API-loaded charts, Datawrapper metadata continues to deserialize into the
nested `transformations` model. The flat fields are intended as construction-time
conveniences and are omitted from `model_dump()`; serialization always writes the
merged result to `metadata.data`.
