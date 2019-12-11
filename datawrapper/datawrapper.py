"""Main module."""
import requests as r
import os
import json
from IPython.display import HTML, Image
from pathlib import Path

class Datawrapper():
    """
    Access Datawrapper's API to create, update, delete charts.
    """
    _BASE_URL = "https://api.datawrapper.de"
    _CHARTS_URL = _BASE_URL + "/v3/charts"
    _PUBLISH_URL = _BASE_URL + "/charts"

    _ACCESS_TOKEN = os.getenv("DATAWRAPPER_ACCESS_TOKEN")

    def __init__(self, access_token = _ACCESS_TOKEN):
        """
        Arguments:
            access_token (str): To create a token head to app.datawrapper.de/account/api-tokens
        """
        self._access_token = access_token
        self._auth_header = {"Authorization": f"Bearer {access_token}"}


    def account_info(self):
        """
        Access your account information.
        """
        account_info_response = r.get(
            url = self._BASE_URL + "/v3/me",
            headers = self._auth_header
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
        _header = self._auth_header
        _header['content-type'] = 'text/csv'

        _data = data.to_csv(index = False, encoding = 'utf-8')

        add_data_response = r.put(
            url = f"{self._CHARTS_URL}/{chart_id}/data",
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
        _header = self._auth_header
        _header['content-type'] = 'application/json'

        _data = {"title": title, "type": chart_type}

        new_chart_response = r.post(
            url = self._CHARTS_URL,
            headers = _header,
            data = json.dumps(_data)
        )

        if new_chart_response.status_code <= 201:
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
        _header = self._auth_header
        _header['content-type'] = 'application/json'
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
        update_description_response = r.patch(
            url = self._CHARTS_URL + f"/{chart_id}",
            headers = _header,
            data = json.dumps(_data),
        )
        if update_description_response.status_code == 200:
            print("Chart updated!")
        else:
            print("Couldn't update chart.")
        

    
    def publish_chart(self, chart_id, display = True):
        """
        Publishes a chart, table or map. 
        """
        publish_chart_response = r.post(
            url = f"{self._PUBLISH_URL}/{chart_id}/publish",
            headers = self._auth_header,
        )
        if publish_chart_response.status_code <= 201:
            publish_chart_info = publish_chart_response.json()
            #print(f"Chart published at {publish_chart_info[]}")
            if display:
                iframe_code = publish_chart_info['data']['metadata']['publish']['embed-codes']['embed-method-iframe']
                # iframe_width = publish_chart_info['data']['metadata']['publish']['embed-width']
                # iframe_height = publish_chart_info['data']['metadata']['publish']['embed-height']
                return HTML(iframe_code)
        else:
            print("Chart couldn't be published at this time.")
    
    def chart_properties(self, chart_id):
        """
        Retrieve information of a specific chart, table or map.
        """
        chart_properties_response = r.get(
            url = self._CHARTS_URL + f"/{chart_id}",
            headers = self._auth_header,
        )
        if chart_properties_response.status_code == 200:
            return chart_properties_response.json()
        else:
            print("Make sure you have the right id and authorization credentials (access_token).")
    
    def update_metadata(self, chart_id, properties):
        """
        Updates a chart's, table's or map's metadata.
        """
        _header = self._auth_header
        _header['content-type'] = 'application/json'
        _data = { 'metadata': properties}

        update_properties_response = r.patch(
            url = self._CHARTS_URL + f"/{chart_id}",
            headers = _header,
            data = json.dumps(_data),
        )
        if update_properties_response.status_code == 200:
            print("Chart's metadata updated!")
            #return update_properties_response.json()
        else:
            print("Chart could not be updated.")

    def display_chart(self, chart_id):
        """
        Displays a datawrapper chart.
        """
        _chart_properties = self.chart_properties(chart_id)
        _iframe_code = _chart_properties['metadata']['publish']['embed-codes']['embed-method-iframe']
        
        return HTML(_iframe_code)

    def export_chart(self, chart_id, unit = "px", mode = "rgb", width = 600, plain = False, scale = 1, output = 'png', filepath = "./image.png", display = False):
        """
        Exports a datawrapper chart, table, or map.
        """
        _export_url = f"{self._CHARTS_URL}/{chart_id}/export/{output}"
        _filepath = Path(filepath)
        _filepath = _filepath.with_suffix(f".{output}")

        if plain:
            plain = 'true'
        else:
            plain = 'false'
        
        querystring = {"unit": unit, "mode": mode, "width": width, "plain": plain, "scale": scale}

        _header = self._auth_header
        _header['accept'] = '*/*'

        export_chart_response = r.get(
            url = _export_url, 
            headers = _header, 
            params = querystring
            )

        if export_chart_response.status_code == 200:
            with open(_filepath, 'wb') as response:
                response.write(export_chart_response.content)
        elif export_chart_response.status_code == 403:
            print("You don't have access to the requested code.")
        else:
            print("Couldn't export at this time.")

        if display:
            return Image(_filepath)
        else:
            print(f"File exported at {_filepath}")




        