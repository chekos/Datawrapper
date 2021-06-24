"""Access Datawrapper's API to create, update, delete charts.

Datawrapper API lets you programatically interface with your charts.
It lets you create and edit charts, update your account information and many more things to come.

    This package is a light-weight wrapper around Datawrapper's API.

        Typical usage example:

        dw = Datawrapper(access_token = <YOUR_ACCESS_TOKEN_HERE>)

        dw.account_info()
"""
from typing import Any, Dict, Iterable, List, Union

import json
import os
from pathlib import Path

import IPython
import pandas as pd
import requests as r
from IPython.display import HTML, Image


class Datawrapper:
    """Handles connecting with Datawrapper's API.

    Handles access to your Datawrapper's account, create, delete and move charts, tables or maps.
    Will attempt to read environment variable DATAWRAPPER_ACCESS_TOKEN by default.

    Args:
        access_token: A personal access token to use the API. See app.datawrapper.de/account/api-tokens.
    """

    _BASE_URL = "https://api.datawrapper.de"
    _CHARTS_URL = _BASE_URL + "/v3/charts"
    _PUBLISH_URL = _BASE_URL + "/charts"
    _FOLDERS_URL = _BASE_URL + "/folders"

    _ACCESS_TOKEN = os.getenv("DATAWRAPPER_ACCESS_TOKEN")

    def __init__(self, access_token=_ACCESS_TOKEN):
        """To create a token head to app.datawrapper.de/account/api-tokens.
        By default this will look for DATAWRAPPER_ACCESS_TOKEN environment variable.

        Parameters
        ----------
        access_token : [type], optional
            [description], by default _ACCESS_TOKEN
        """

        self._access_token = access_token
        self._auth_header = {"Authorization": f"Bearer {access_token}"}

    def account_info(self) -> Union[Dict[Any, Any], None, Any]:
        """Access your account information.

        Returns
        -------
        dict
            A dictionary containing your account information.
        """
        account_info_response = r.get(
            url=self._BASE_URL + "/v3/me", headers=self._auth_header
        )
        if account_info_response.status_code == 200:
            return account_info_response.json()
        else:
            print(
                "Couldn't find account. Make sure your credentials (access_code) are correct."
            )
            return None

    def add_data(self, chart_id: str, data: pd.DataFrame) -> r.Response:
        """Add data to a specified chart.

        Parameters
        ----------
        chart_id : str
            ID of chart, table or map to add data to.
        data : pd.DataFrame
            A pandas dataframe containing the data to be added.

        Returns
        -------
        requests.Response
            A requests.Response
        """

        _header = self._auth_header
        _header["content-type"] = "text/csv"

        _data = data.to_csv(index=False, encoding="utf-8")

        return r.put(
            url=f"{self._CHARTS_URL}/{chart_id}/data",
            headers=_header,
            data=_data.encode("utf-8"),
        )

    def refresh_data(self, chart_id: str) -> r.Response:
        """Fetch configured external data and add it to the chart.

        Parameters
        ----------
        chart_id : str
            ID of chart, table or map to add data to.

        Returns
        -------
        requests.Response
            A requests.Response
        """
        _header = self._auth_header
        _header["accept"] = "*/*"

        return r.post(
            url=f"{self._CHARTS_URL}/{chart_id}/data/refresh",
            headers=_header,
        )

    def create_chart(
        self,
        title: str = "New Chart",
        chart_type: str = "d3-bars-stacked",
        data: Union[pd.DataFrame, None] = None,
        folder_id: str = "",
    ) -> Union[Dict[Any, Any], None, Any]:
        """Creates a new Datawrapper chart, table or map.
        You can pass a pandas DataFrame as a `data` argument to upload data.
        Returns the created chart's information.

        Parameters
        ----------
        title : str, optional
            Title for new chart, table or map, by default "New Chart"
        chart_type : str, optional
            Chart type to be created. See https://developer.datawrapper.de/docs/chart-types, by default "d3-bars-stacked"
        data : [type], optional
            A pandas DataFrame containing the data to be added, by default None
        folder_id : str, optional
            ID of folder in Datawrapper.de for the chart, table or map to be created in, by default ""

        Returns
        -------
        dict
            A dictionary containing the created chart's information.
        """

        _header = self._auth_header
        _header["content-type"] = "application/json"

        _data = {"title": title, "type": chart_type}

        if folder_id:
            _data["folderId"] = folder_id

        new_chart_response = r.post(
            url=self._CHARTS_URL, headers=_header, data=json.dumps(_data)
        )

        if (
            chart_type == "d3-maps-choropleth"
            or chart_type == "d3-maps-symbols"
            or chart_type == "locator-map"
        ):
            print(
                "\nNOTE: Maps need a valid basemap, set in properties -> visualize"
            )
            print(
                "Full list of valid maps can be retrieved with\n\ncurl --request GET --url https://api.datawrapper.de/plugin/basemap\n"
            )

        if new_chart_response.status_code <= 201:
            chart_info = new_chart_response.json()
            print(f"New chart {chart_info['type']} created!")
        else:
            print(
                f"Chart could not be created, check your authorization credentials (access token){', and that the folder_id is valid (i.e exists, and your account has access to it)' if folder_id else ''}"
            )

        if data is not None:
            self.add_data(chart_id=chart_info["id"], data=data)

        return chart_info

    def update_description(
        self,
        chart_id: str,
        source_name: str = "",
        source_url: str = "",
        intro: str = "",
        byline: str = "",
    ) -> Union[Any, None]:
        """Update a chart's description.

        Parameters
        ----------
        chart_id : str
            ID of chart, table or map.
        source_name : str, optional
            Source of data, by default ""
        source_url : str, optional
            URL of source of data, by default ""
        intro : str, optional
            Introduction of your chart, table or map, by default ""
        byline : str, optional
            Who made this?, by default ""
        """

        _header = self._auth_header
        _header["content-type"] = "application/json"
        _data = {
            "metadata": {
                "describe": {
                    "source-name": source_name,
                    "source-url": source_url,
                    "intro": intro,
                    "byline": byline,
                }
            }
        }
        update_description_response = r.patch(
            url=self._CHARTS_URL + f"/{chart_id}",
            headers=_header,
            data=json.dumps(_data),
        )
        if update_description_response.status_code == 200:
            print("Chart updated!")
        else:
            print(
                "Error. Status code: ", update_description_response.status_code
            )
            print("Couldn't update chart.")
        return None

    def publish_chart(
        self, chart_id: str, display: bool = True
    ) -> Union[Any, None]:
        """Publishes a chart, table or map.

        Parameters
        ----------
        chart_id : str
            ID of chart, table or map.
        display : bool, optional
            Display the published chart as output in notebook cell, by default True
        """

        publish_chart_response = r.post(
            url=f"{self._PUBLISH_URL}/{chart_id}/publish",
            headers=self._auth_header,
        )
        if publish_chart_response.status_code <= 201:
            # print(f"Chart published at {publish_chart_info[]}")
            if display:
                publish_chart_info = publish_chart_response.json()
                iframe_code = publish_chart_info["data"]["metadata"]["publish"][
                    "embed-codes"
                ]["embed-method-iframe"]
                # iframe_width = publish_chart_info['data']['metadata']['publish']['embed-width']
                # iframe_height = publish_chart_info['data']['metadata']['publish']['embed-height']
                return HTML(iframe_code)
            else:
                return None
        else:
            print("Chart couldn't be published at this time.")
            return None

    def chart_properties(
        self, chart_id: str
    ) -> Union[Dict[Any, Any], None, Any, Iterable[Any]]:
        """Retrieve information of a specific chart, table or map.

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.

        Returns
        -------
        dict
            A dictionary containing the information of the chart, table, or map.
        """
        chart_properties_response = r.get(
            url=self._CHARTS_URL + f"/{chart_id}",
            headers=self._auth_header,
        )
        if chart_properties_response.status_code == 200:
            return chart_properties_response.json()
        else:
            print(
                "Make sure you have the right id and authorization credentials (access_token)."
            )
            return None

    def update_metadata(
        self, chart_id: str, properties: Dict[Any, Any]
    ) -> Union[Any, None]:
        """Update a chart, table, or map's metadata.
        Example: https://developer.datawrapper.de/docs/creating-a-chart-new#edit-colors

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.
        properties : dict
            A python dictionary of properties to update.
        """
        _header = self._auth_header
        _header["content-type"] = "application/json"
        _data = {"metadata": properties}

        update_properties_response = r.patch(
            url=self._CHARTS_URL + f"/{chart_id}",
            headers=_header,
            data=json.dumps(_data),
        )
        if update_properties_response.status_code == 200:
            print("Chart's metadata updated!")
            # return update_properties_response.json()
        else:
            print(
                "Error. Status code: ", update_properties_response.status_code
            )
            x = update_properties_response.text
            y = json.loads(x)
            print("Message: ", y["message"])
            print("Chart could not be updated.")
        return None

    def update_chart(
        self,
        chart_id: str,
        title: str = "",
        theme: str = "",
        chart_type: str = "",
        language: str = "",
        folder_id: str = "",
        organization_id: str = "",
    ) -> Union[Any, None]:
        """Updates a chart's title, theme, type, language, or location (folder/organization).

        Parameters
        ----------
        chart_id : str
            ID Of chart, table, or map.
        title : str, optional
            New title, by default ""
        theme : str, optional
            New theme, by default ""
        chart_type : str, optional
            New chart type. See https://developer.datawrapper.de/docs/chart-types, by default ""
        language : str, optional
            New language, by default ""
        folder_id : str, optional
            New folder's ID, by default ""
        organization_id : str, optional
            New organization's ID, by default ""
        """
        _header = self._auth_header
        _header["accept"] = "*/*"
        _header["content-type"] = "application/json"
        _query = {}
        if title:
            _query["title"] = title
        if theme:
            _query["theme"] = theme
        if chart_type:
            _query["type"] = chart_type
        if language:
            _query["language"] = language
        if folder_id:
            _query["folderId"] = folder_id
        if organization_id:
            _query["organizationId"] = organization_id

        update_chart_response = r.patch(
            url=self._CHARTS_URL + f"/{chart_id}",
            headers=_header,
            data=json.dumps(_query),
        )
        if update_chart_response.status_code == 200:
            print(f"Chart with id {chart_id} updated!")
            return self.publish_chart(chart_id)
        else:
            print("Chart could not be updated at the time.")
            return None

    def display_chart(self, chart_id: str) -> IPython.display.HTML:
        """Displays a datawrapper chart.

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.

        Returns
        -------
        IPython.display.HTML
            HTML displaying the chart.
        """
        _chart_properties = self.chart_properties(chart_id)
        _iframe_code = _chart_properties["metadata"]["publish"]["embed-codes"][  # type: ignore
            "embed-method-iframe"
        ]

        return HTML(_iframe_code)

    def get_iframe_code(
        self, chart_id: str, responsive: bool = False
    ) -> Union[str, Any]:
        """Returns a chart, table, or map's iframe embed code.

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.
        responsive : bool, optional
            Whether to return a responsive iframe embed code., by default False

        Returns
        -------
        str
            iframe embed code.
        """
        _chart_properties = self.chart_properties(chart_id)

        if responsive:
            iframe_code = _chart_properties["metadata"]["publish"][  # type: ignore
                "embed-codes"
            ][
                "embed-method-responsive"
            ]
        else:
            iframe_code = _chart_properties["metadata"]["publish"][  # type: ignore
                "embed-codes"
            ][
                "embed-method-iframe"
            ]
        return iframe_code

    def export_chart(
        self,
        chart_id: str,
        unit: str = "px",
        mode: str = "rgb",
        width: int = 100,
        plain: bool = False,
        zoom: int = 2,
        scale: int = 1,
        border_width: int = 20,
        output: str = "png",
        filepath: str = "./image.png",
        display: bool = False,
    ) -> Union[Any, None]:
        """Exports a chart, table, or map.

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.
        unit : str, optional
            One of px, mm, inch. Defines the unit in which the borderwidth, height, and width will be measured in, by default "px"
        mode : str, optional
            One of rgb or cmyk. Which color mode the output should be in, by default "rgb"
        width : int, optional
            Width of visualization. If not specified, it takes the chart width, by default None
        plain : bool, optional
            Defines if only the visualization should be exported (True), or if it should include header and footer as well (False), by default False
        zoom : int, optional
            Defines the multiplier for the png size, by default 2
        scale : int, optional
            Defines the multiplier for the pdf size, by default 1
        border_width : int, optional
            Margin arouund the visualization, by default 20
        output : str, optional
            One of png, pdf, or svg, by default "png"
        filepath : str, optional
            Name/filepath to save output in, by default "./image.png"
        display : bool, optional
            Whether to display the exported image as output in the notebook cell, by default False

        Returns
        -------
        IPython.display.Image
            If display is True, it returns an Image.
        """
        _export_url = f"{self._CHARTS_URL}/{chart_id}/export/{output}"
        _filepath = Path(filepath)
        _filepath = _filepath.with_suffix(f".{output}")

        _plain = "true" if plain else "false"
        querystring = {
            "unit": unit,
            "mode": mode,
            "width": width,
            "plain": _plain,
            "zoom": zoom,
            "scale": scale,
            "borderWidth": border_width,
        }

        _header = self._auth_header
        _header["accept"] = "*/*"

        export_chart_response = r.get(
            url=_export_url, headers=_header, params=querystring  # type: ignore
        )

        if export_chart_response.status_code == 200:
            with open(_filepath, "wb") as response:
                response.write(export_chart_response.content)
            if display:
                return Image(_filepath)
            else:
                print(f"File exported at {_filepath}")
        elif export_chart_response.status_code == 403:
            print("You don't have access to the requested code.")
        elif export_chart_response.status_code == 401:
            print("You couldn't be authenticated.")
        else:
            print("Couldn't export at this time.")
        return None

    def get_folders(self) -> Union[Dict[Any, Any], None, Any]:
        """Get a list of folders in your Datawrapper account.

        Returns
        -------
        dict
            A dictionary containing the folders in your Datawrapper account and their information.
        """
        get_folders_response = r.get(
            url=self._FOLDERS_URL,
            headers=self._auth_header,
        )

        if get_folders_response.status_code == 200:
            return get_folders_response.json()
        else:
            print(
                "Couldn't retrieve folders in account. Make sure you have the rigth authorization credentials (access token)."
            )
            return None

    def move_chart(self, chart_id: str, folder_id: str) -> Union[Any, None]:
        """Moves a chart, table, or map to a specified folder.

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.
        folder_id : str
            ID of folder to move visualization to.
        """

        _header = self._auth_header
        _header["content-type"] = "application/json"

        _data = {"folderId": folder_id}

        move_chart_response = r.patch(
            url=self._CHARTS_URL + f"/{chart_id}",
            headers=_header,
            data=json.dumps(_data),
        )

        if move_chart_response.status_code == 200:
            print(f"Chart moved to folder {folder_id}")
        else:
            print("Chart could not be moved at the moment.")
        return None

    def delete_chart(self, chart_id: str) -> r.Response.content:  # type: ignore
        """Deletes a specified chart, table or map.


        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.

        Returns
        -------
        r.Response.content
            The content of the requests.delete
        """

        delete_chart_response = r.delete(
            url=self._CHARTS_URL + f"/{chart_id}", headers=self._auth_header
        )
        if delete_chart_response.content:
            return delete_chart_response.content
        else:
            print(f"Successfully deleted chart with id {chart_id}")
            return None

    def get_charts(
        self,
        user_id: str = "",
        published: str = "true",
        search: str = "",
        order: str = "DESC",
        order_by: str = "createdAt",
        limit: int = 25,
    ) -> Union[None, List[Any]]:
        """Retrieves a list of charts by User

        Parameters
        ----------
        user_id : str, optional
            ID of the user to fetch charts for, by default ""
        published : str, optional
            Flag to filter resutls by publish status, by default "true"
        search : str, optional
            Search for charts with a specific title, by default ""
        order : str, optional
            Result order (ascending or descending), by default "DESC"
        order_by : str, optional
            Attribute to order by. One of createdAt, email, id, or name, by default "createdAt"
        limit : int, optional
            Maximum items to fetch, by default 25

        Returns
        -------
        list
            List of charts.
        """

        _url = self._CHARTS_URL
        _header = self._auth_header
        _header["accept"] = "*/*"
        _query = {}
        if user_id:
            _query["userId"] = user_id
        if published:
            _query["published"] = published
        if search:
            _query["search"] = search
        if order:
            _query["order"] = order
        if order_by:
            _query["orderBy"] = order_by
        if limit:
            _query["limit"] = str(limit)

        get_charts_response = r.get(url=_url, headers=_header, params=_query)

        if get_charts_response.status_code == 200:
            return get_charts_response.json()["list"]  # type: ignore
        else:
            print("Could not retrieve charts at this moment.")
            return None
