# Usage

`datawrapper` is a light-weight wrapper around the [Datawrapper API](https://developer.datawrapper.de/docs/getting-started)
yeah I know... it's a lot to _wrap your head around._

<img src='https://i.kym-cdn.com/entries/icons/original/000/014/959/Screenshot_116.png' style='width:100px' />


To use `datawrapper` you're going to need a Datawrapper access token. If you have a Datawrapper.de account go to https://app.datawrapper.de/account/api-tokens.

If you don't have a Datawrapper.de account, sign up for one. They're free.


***
First we'll import the Datawrapper class from `datawrapper` and pandas so we can add some sample data.

```python
from datawrapper import Datawrapper
import pandas as pd
```

`datwrapper.Datawrapper` will load your access token if you have it as an environment variable `DATAWRAPPER_ACCESS_TOKEN`. If not, you'll have to pass it manually.

```python
ACCESS_TOKEN = "<YOUR_API_ACCESS_TOKEN_HERE>"
```

```python
dw = Datawrapper(access_token=ACCESS_TOKEN)

dw.account_info()
```

We'll use the same data the *Getting Started* tutorial from the API docs uses.

```python
df = pd.read_csv(
    "https://raw.githubusercontent.com/chekos/datasets/master/data/datawrapper_example.csv",
    sep=";",
)
df.head()
```

***
To create a chart and add data in one call just use `datawrapper.create_chart()` and pass the pandas DataFrame as the data argument. It will return a JSON with your new chart's information.

```python
chart_info = dw.create_chart(
    title="Where do people live?", chart_type="d3-bars-stacked", data=df
)
```

```python
chart_info
```

To add a source and a byline you can use `datawrapper.update_description()`

```python
dw.update_description(
    chart_info["id"],
    source_name="UN Population Division",
    source_url="https://population.un.org/wup/",
    byline="datawrapper at pypi",
)
```

Almost done! Your chart exists now but it's not published. In fact, you could go to `https://datawrapper.de/chart/<ID>/visualize` (add your new chart's id) to see how it looks like right now. 

To publish it you can use `datawrapper.publish_chart()`, just pass it your chart's id. 

```python
dw.publish_chart(chart_id=chart_info["id"])
```

![nooice](https://media1.tenor.com/images/d2c70f7f64587dc3b7c86ee06756fb4a/tenor.gif?itemid=4294979)


You can edit its metadata by passing them as a dictionary to `datawrapper.update_metadata()`. In this case, we want to make the bars thick and add custom colors to each of our labels.

```python
properties = {
    "visualize": {
        "thick": True,
        "custom-colors": {
            "in rural areas": "#dadada",
            "in other urban areas": "#1d81a2",
            "Share of population that lives in the capital": "#15607a",
        },
    }
}
dw.update_metadata(chart_info["id"], properties)
```

You'll have to republish your _new new_ chart.

```python
dw.publish_chart(chart_info["id"])
```

You can also **export** your chart as a `png` with `datwrapper.export_chart()`! (pdf and svg coming!)

```python
dw.export_chart("OsgIU", output="png", filepath="chart.png", display=True)
```
