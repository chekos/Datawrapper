=====
Usage
=====

Before using `datawrapper` in a project you'll need to get an access token from Datawrapper. See https://app.datawrapper.de/account/api-tokens

To use datawrapper in a project::

    from datawrapper import Datawrapper

    dw = Datawrapper(access_token = "INSERT_YOUR_ACCESS_TOKEN_HERE")

Now you have access to your Datawrapper account.

To view your account info run::
    dw.account_info()

Create a chart
    new_chart_info = dw.create_chart(title = 'New chart!', chart_type = 'd3-bars-stacked')

This returns a JSON with your new chart's info, including its ID which you will need to update, add data to, move, display or delete said chart.

You could also pass a pandas.DataFrame as data in the same call and you'll have created a chart and uploaded the data at once. 
::
    df = pd.read_csv("https://raw.githubusercontent.com/chekos/datasets/master/data/datawrapper_example.csv", sep=';')
    new_chart_info = dw.create_chart(title = 'New chart 2!', chart_type = 'd3-bars-stacked', data  = df)
    new_chart_info
    
    >>>> {'title': 'New chart 2!',
            'theme': 'default',
            'type': 'd3-bars-stacked',
            'language': 'en-US',
            'metadata': {'data': {}},
            'authorId': 163125,
            'id': 'OsgIU',
            'lastModifiedAt': '2019-12-11T23:17:35.826Z',
            'createdAt': '2019-12-11T23:17:35.826Z',
            'url': '/v3/charts/OsgIU'}

Your chart will have a different 'id'. That is super important because that's how you edit your chart!

Update the chart's description:
::
    dw.update_description(
        chart_id = new_chart_info['id'],
        source_name = 'UN Population Division',
        source_url = 'https://population.un.org/wup/',
        byline = 'Your name here!',
    )
    >>>> Chart updated!

For others to see your marvelous creation you need to publish your chart!
::
    dw.publish_chart(chart_id = new_chart_info['id'])

By default, `datawrapper` (the python package) will attempt to display your chart as the cell's output. This feature is still being tested so it might be changed to not do this by default in the future.
