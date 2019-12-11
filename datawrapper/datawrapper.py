"""Main module."""
import requests as r
import os
import json
from IPython.display import HTML

class Datawrapper(object):
    """
    Access Datawrapper's API to create, update, delete charts.
    """
    BASE_URL = "https://api.datawrapper.de"
    CHARTS_URL = BASE_URL + "/v3/charts"
    PUBLISH_URL = BASE_URL + "charts"

    ACCESS_TOKEN = os.getenv("DATAWRAPPER_ACCESS_TOKEN")

    def __init__(self, access_token = ACCESS_TOKEN):
        """
        Arguments:
            access_token (str): To create a token head to app.datawrapper.de/account/api-tokens
        """
        self.access_token = access_token
        self.auth_header = {"Authorization": f"Bearer {access_token}"}

    def account_info(self):
        """
        Access your account information.
        """
        account_info_response = r.get(
            url = self.BASE_URL + "/me",
            header = self.auth_header
        )
        if account_info_response.status_code == 200:
            return account_info_response.json()
        else:
            print("Couldn't find account. Make sure your credentials (access_code) are correct.")
    
    def add_data(self, chart_id, data):
        """
        Adds data to a chart, table, map.
        Arguments:
            id (str): Chart, table or map id.
            data (pandas DataFrame): a 
        """
        _header = self.auth_header
        _header['content-type'] = 'text/csv'

        _data = data.to_csv(index = False, encoding = 'utf-8')

        add_data_response = r.put(
            url = f"{self.CHARTS_URL}/{chart_id}/data",
            headers = _header,
            data = _data
        )
        return add_data_response



    def create_chart(self, title = 'New Chart', chart_type = "d3-bars-stacked", data = None):
        """
        Creates a new Datawrapper chart, table or map.
        You can pass a pandas DataFrame as data argument to upload data.
        Returns created chart information.
        """
        _header = self.auth_header
        _header['content-type'] = 'application/json'

        _data = {"title": title, "type": chart_type}

        new_chart_response = r.post(
            url = self.CHARTS_URL,
            headers = _header,
            data = _data
        )

        if new_chart_response.status_code == r.codes.ok:
            chart_info = new_chart_response.json()
            print(f"New chart {chart_info['type']} created!")
        else:
            print("Chart could not be created, check your authorization credentials (access token)")
        
        if data is not None:
            self.add_data(chart_id = chart_info['id'], data = data)

        return chart_info
    
    def update_description(self, chart_id, source_name = "", source_url = "", intro = "", byline = ""):
        """
        Update a chart's description.
        Arguments:
            id (str): Chart, table or map id.
            source_name (str): The data source.
            source_url (str): The data source's url.
            intro (str): Introduction of your chart/table/map.
            byline (str): Who made this?
        """

        _data = {
            'metadata': {
                'describe': {
                    'source-name': source_name,
                    'source-url': source_url,
                    'intro': intro,
                    'byline': byline,
                }
            }
        }
    
    def publish_chart(self, chart_id, display = True):
        """
        Publishes a chart, table or map. 
        """
        publish_chart_response = r.post(
            url = f"{self.PUBLISH_URL}/{chart_id}",
            headers = self.auth_header,
        )
        if publish_chart_response == r.codes.ok:
            publish_chart_info = publish_chart_response.json()
            print("Chart published!")
            if display:
                iframe_code = publish_chart_info['data']['metadata']['publish']['embed-codes']['embed-method-iframe']
                HTML(iframe_code)


        