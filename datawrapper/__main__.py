"""Access Datawrapper's API to create, update, delete charts.

Datawrapper API lets you programatically interface with your charts.
It lets you create and edit charts, update your account information and many more things
 to come.

    This package is a light-weight wrapper around Datawrapper's API.

        Typical usage example:

        dw = Datawrapper(access_token = <YOUR_ACCESS_TOKEN_HERE>)

        dw.account_info()
"""
from __future__ import annotations

import json
import logging
import os
from io import StringIO
from pathlib import Path
from typing import Any, Iterable

import IPython
import pandas as pd
import requests as r
from IPython.display import HTML, Image

logger = logging.getLogger(__name__)


class Datawrapper:
    """Handles connecting with Datawrapper's API.

    Handles access to your Datawrapper's account, create, delete and move charts, tables
      or maps.
    Will attempt to read environment variable DATAWRAPPER_ACCESS_TOKEN by default.

    Args:
        access_token: A personal access token to use the API.
        See app.datawrapper.de/account/api-tokens.
    """

    _BASE_URL = "https://api.datawrapper.de"
    _CHARTS_URL = _BASE_URL + "/v3/charts"
    _PUBLISH_URL = _BASE_URL + "/charts"
    _FOLDERS_URL = _BASE_URL + "/v3/folders"

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

    def account_info(self) -> dict[Any, Any] | None | Any:
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
            msg = (
                "Couldn't find account. Make sure your credentials ",
                "(access_code) are correct.",
            )
            logger.error(msg)
            raise Exception(msg)

    def add_data(self, chart_id: str, data: pd.DataFrame | str) -> r.Response:
        """Add data to a specified chart.

        Parameters
        ----------
        chart_id : str
            ID of chart, table or map to add data to.
        data : pd.DataFrame | str
            A pandas dataframe containing the data to be added or a string that contains
            the data.

        Returns
        -------
        requests.Response
            A requests.Response
        """
        # Set headers
        _header = self._auth_header
        _header["content-type"] = "text/csv"

        # If data is a pandas dataframe, convert to csv
        if isinstance(data, pd.DataFrame):
            _data = data.to_csv(index=False, encoding="utf-8")
        # If data is a string, use that
        else:
            _data = data

        # Add data to chart
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
        data: pd.DataFrame | str | None = None,
        folder_id: str = "",
        organization_id: str = "",
        metadata: dict[Any, Any] | None = None,
    ) -> dict[Any, Any] | None | Any:
        """Creates a new Datawrapper chart, table or map.

        You can pass a pandas DataFrame as a `data` argument to upload data.

        Returns the created chart's information.

        Parameters
        ----------
        title : str, optional
            Title for new chart, table or map, by default "New Chart"
        chart_type : str, optional
            Chart type to be created. See https://developer.datawrapper.de/docs/chart-types,
            by default "d3-bars-stacked"
        data : [type], optional
            A pandas DataFrame or string containing the data to be added,
            by default None
        folder_id : str, optional
            ID of folder in Datawrapper.de for the chart, table or map to be created in,
            by default ""
        organization_id : str, optional
            ID of the team where the chart should be created. The authenticated user
            must have access to this team.
        metadata: dict, optional
            A Python dictionary of properties to add.

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
        if organization_id:
            _data["organizationId"] = organization_id
        if metadata:
            _data["metadata"] = metadata  # type: ignore

        new_chart_response = r.post(
            url=self._CHARTS_URL, headers=_header, data=json.dumps(_data)
        )

        if (
            chart_type == "d3-maps-choropleth"
            or chart_type == "d3-maps-symbols"
            or chart_type == "locator-map"
        ):
            logger.debug(
                "\nNOTE: Maps need a valid basemap, set in properties -> visualize"
            )
            logger.debug(
                (
                    "Full list of valid maps can be retrieved with\n\n",
                    "curl --request GET --url https://api.datawrapper.de/plugin/basemap\n",
                )
            )

        if new_chart_response.status_code <= 201:
            chart_info = new_chart_response.json()
            logger.debug(f"New chart {chart_info['type']} created!")
        else:
            msg = f"Chart could not be created, check your authorization credentials (access token){', and that the folder_id is valid (i.e exists, and your account has access to it)' if folder_id else ''}"
            logger.error(msg)
            raise Exception(msg)

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
        aria_description: str = "",
        number_prepend: str = "",
        number_append: str = "",
        number_format: str = "-",
        number_divisor: int = 0,
    ) -> Any | None:
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
        aria_description : str, optional
            Alt text description
        number_prepend : str, optional
            Something to put before the number
        number_append : str, optional
            Something to after before the number
        number_format : str, optional
            The format number
        number_divisor : str, optional
            A multiplier or divisor for the numbers
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
                    "aria-description": aria_description,
                    "number-prepend": number_prepend,
                    "number-append": number_append,
                    "number-format": number_format,
                    "number-divisor": number_divisor,
                }
            }
        }
        update_description_response = r.patch(
            url=self._CHARTS_URL + f"/{chart_id}",
            headers=_header,
            data=json.dumps(_data),
        )
        if update_description_response.status_code == 200:
            logger.debug("Chart updated!")
            return None
        else:
            msg = f"Error. Status code: {update_description_response.status_code}"
            logger.error(msg)
            raise Exception(msg)

    def publish_chart(self, chart_id: str, display: bool = True) -> Any | None:
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
            publish_chart_info = publish_chart_response.json()
            logger.debug(f"Chart published at {publish_chart_info['url']}")
            if display:
                iframe_code = publish_chart_info["data"]["metadata"]["publish"][
                    "embed-codes"
                ]["embed-method-iframe"]
                return HTML(iframe_code)
            else:
                return None
        else:
            msg = "Chart couldn't be published at this time."
            logger.error(msg)
            raise Exception(msg)

    def chart_properties(
        self, chart_id: str
    ) -> dict[Any, Any] | None | Any | Iterable[Any]:
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
            msg = (
                "Make sure you have the right id and authorization ",
                "credentials (access_token).",
            )
            logger.error(msg)
            raise Exception(msg)

    def chart_data(self, chart_id: str):
        """Retrieve the data stored for a specific chart, table or map,
        which is typically CSV.


        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.

        Returns
        -------
        dict
            A dictionary containing the information of the chart, table, or map.
        """
        # Request the data endpoint
        response = r.get(
            url=self._CHARTS_URL + f"/{chart_id}/data",
            headers=self._auth_header,
        )

        # Check if the request was successful
        assert (
            response.ok
        ), "Ensure you have the right id and authorization credentials (access_token)."

        # Return the data as json if the mimetype is json
        if "json" in response.headers["content-type"]:
            return response.json()
        # If it's a csv, read the text into a dataframe
        elif "text/csv" in response.headers["content-type"]:
            return pd.read_csv(StringIO(response.text))
        # Otherwise just return the text
        else:
            return response.text

    def update_metadata(self, chart_id: str, properties: dict[Any, Any]) -> Any | None:
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
            logger.debug("Chart's metadata updated!")
            return None
        else:
            msg = f"Error. Status code: {update_properties_response.status_code}"
            logger.error(msg)
            text = json.loads(update_properties_response.text)
            logger.debug("Message: ", text["message"])
            logger.debug("Chart could not be updated.")
            raise Exception(msg)

    def update_chart(
        self,
        chart_id: str,
        title: str = "",
        theme: str = "",
        chart_type: str = "",
        language: str = "",
        folder_id: str = "",
        organization_id: str = "",
    ) -> Any | None:
        """Updates a chart's title, theme, type, language,
        or location (folder/organization).


        Parameters
        ----------
        chart_id : str
            ID Of chart, table, or map.
        title : str, optional
            New title, by default ""
        theme : str, optional
            New theme, by default ""
        chart_type : str, optional
            New chart type. See https://developer.datawrapper.de/docs/chart-types,
            by default ""
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
            logger.debug(f"Chart with id {chart_id} updated!")
            return self.publish_chart(chart_id)
        else:
            msg = "Chart could not be updated at the time."
            logger.debug(msg)
            raise Exception(msg)

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

    def get_iframe_code(self, chart_id: str, responsive: bool = False) -> str | Any:
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
            ]["embed-method-responsive"]
        else:
            iframe_code = _chart_properties["metadata"]["publish"][  # type: ignore
                "embed-codes"
            ]["embed-method-iframe"]
        return iframe_code

    def export_chart(
        self,
        chart_id: str,
        unit: str = "px",
        mode: str = "rgb",
        width: int = 400,
        plain: bool = False,
        zoom: int = 2,
        scale: int = 1,
        border_width: int = 20,
        transparent: bool = False,
        output: str = "png",
        filepath: str = "./image.png",
        display: bool = False,
    ) -> Any | None:
        """Exports a chart, table, or map.

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.
        unit : str, optional
            One of px, mm, inch. Defines the unit in which the borderwidth, height,
            and width will be measured in, by default "px"
        mode : str, optional
            One of rgb or cmyk. Which color mode the output should be in,
            by default "rgb"
        width : int, optional
            Width of visualization. If not specified, it takes the chart width,
            by default None
        plain : bool, optional
            Defines if only the visualization should be exported (True), or if it should
             include header and footer as well (False), by default False
        zoom : int, optional
            Defines the multiplier for the png size, by default 2
        scale : int, optional
            Defines the multiplier for the pdf size, by default 1
        border_width : int, optional
            Margin arouund the visualization, by default 20
        transparent : bool, optional
            Set to `True` to export your visualization with a transparent background.
        output : str, optional
            One of png, pdf, or svg, by default "png"
        filepath : str, optional
            Name/filepath to save output in, by default "./image.png"
        display : bool, optional
            Whether to display the exported image as output in the notebook cell,
            by default False

        Returns None
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
            "transparent": transparent,
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
                logger.debug(f"File exported at {_filepath}")
                return None
        elif export_chart_response.status_code == 403:
            msg = "You don't have access to the requested chart."
            logger.error(msg)
            raise Exception(msg)
        elif export_chart_response.status_code == 401:
            msg = "You couldn't be authenticated."
            logger.error(msg)
            raise Exception(msg)
        else:
            msg = "Chart could not be exported."
            logger.error(msg)
            raise Exception(msg)

    def get_folders(self) -> dict[Any, Any] | None | Any:
        """Get a list of folders in your Datawrapper account.

        Returns
        -------
        dict
            A dictionary containing the folders in your Datawrapper account and their
            information.
        """
        get_folders_response = r.get(
            url=self._FOLDERS_URL,
            headers=self._auth_header,
        )

        if get_folders_response.status_code == 200:
            return get_folders_response.json()
        else:
            msg = (
                "Couldn't retrieve folders in account. Make sure you have the right ",
                "authorization credentials (access token).",
            )
            logger.error(msg)
            raise Exception(msg)

    def get_folder(self, folder_id: str | int) -> dict[Any, Any]:
        """Get an existing folder.

        Parameters
        ----------
        folder_id : str | int
            ID of folder to get.

        Returns
        -------
        dict
            A dictionary containing the folder's information.
        """
        _header = self._auth_header
        _header["accept"] = "*/*"

        response = r.get(
            url=self._FOLDERS_URL + f"/{folder_id}",
            headers=_header,
        )

        if response.ok:
            folder_info = response.json()
            logger.debug(f"Folder {folder_info['name']} retrieved with id {folder_id}")
            return folder_info
        else:
            msg = "Folder could not be retrieved."
            logger.error(msg)
            raise Exception(msg)

    def create_folder(
        self,
        name: str,
        parent_id: str | int | None = None,
        team_id: str | int | None = None,
    ) -> dict[Any, Any]:
        """Create a new folder.

        Parameters
        ----------
        name: str
            Name of the folder to be created.
        parent_id: str | int, optional
            The parent folder that the folder belongs to.
        team_id: str | int, optional
            The team that the folder belongs to. If teamId is empty, the folder will
            belong to the user directly.

        Returns
        -------
        dict
            A dictionary containing the folder's information.
        """
        _header = self._auth_header
        _header["accept"] = "*/*"

        _query: dict[str, Any] = {"name": name}
        if parent_id:
            _query["parentId"] = parent_id
        if team_id:
            _query["teamId"] = team_id

        response = r.post(
            url=self._FOLDERS_URL,
            headers=_header,
            data=json.dumps(_query),
        )

        if response.ok:
            folder_info = response.json()
            logger.debug(
                f"Folder {folder_info['name']} created with id {folder_info['id']}"
            )
            return folder_info
        else:
            msg = "Folder could not be created."
            logger.error(msg)
            raise Exception(msg)

    def update_folder(
        self,
        folder_id: str | int,
        name: str | None = None,
        parent_id: str | int | None = None,
        team_id: str | int | None = None,
        user_id: str | int | None = None,
    ) -> dict[Any, Any]:
        """Update an existing folder.

        Parameters
        ----------
        folder_id : str | int
            ID of folder to update.
        name: str, optional
            Name to change the folder to.
        parent_id: str | int, optional
            The parent folder where this folder is stored.
        team_id: str | int, optional
            The team that the folder belongs to.
        user_id: str | int, optional
            The user that the folder belongs to.

        Returns
        -------
        r.Response.content
            The content of the requests.delete
        """
        _header = self._auth_header
        _header["accept"] = "*/*"

        _query: dict[str, Any] = {}
        if name:
            _query["name"] = name
        if parent_id:
            _query["parentId"] = parent_id
        if team_id:
            _query["teamId"] = team_id
        if user_id:
            _query["userId"] = user_id

        url = self._FOLDERS_URL + f"/{folder_id}"
        response = r.patch(
            url=url,
            headers=_header,
            data=json.dumps(_query),
        )

        if response.ok:
            folder_info = response.json()
            logger.debug(f"Folder {folder_id} updated")
            return folder_info
        else:
            msg = "Folder could not be updated."
            logger.error(msg)
            raise Exception(msg)

    def delete_folder(self, folder_id: str | int):
        """Delete an existing folder.

        Parameters
        ----------
        folder_id : str | int
            ID of folder to delete.

        Returns
        -------
        r.Response.content
            The content of the requests.delete
        """
        _header = self._auth_header
        _header["accept"] = "*/*"

        url = self._FOLDERS_URL + f"/{folder_id}"
        response = r.delete(
            url=url,
            headers=_header,
        )

        if response.ok:
            logger.debug(f"Folder {folder_id} deleted")
            return response.content
        else:
            msg = "Folder could not be deleted."
            logger.error(msg)
            raise Exception(msg)

    def move_chart(self, chart_id: str, folder_id: str) -> Any | None:
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
            logger.debug(f"Chart moved to folder {folder_id}")
            return None
        else:
            msg = "Chart could not be moved at the moment."
            logger.error(msg)
            raise Exception(msg)

    def copy_chart(self, chart_id: str) -> dict[Any, Any]:
        """Copy one of your charts, tables, or maps and create a new editable copy.

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.

        Returns
        -------
        dict
            A dictionary containing the information of the chart, table, or map.
        """
        _header = self._auth_header
        _header["accept"] = "*/*"

        url = f"{self._CHARTS_URL}/{chart_id}/copy"
        response = r.post(url=url, headers=_header)

        if response.ok:
            copy_id = response.json()
            logger.debug(f"Chart {chart_id} copied to {copy_id['id']}")
            return copy_id
        else:
            msg = "Chart could not be copied at the moment."
            logger.error(msg)
            raise Exception(msg)

    def fork_chart(self, chart_id: str) -> dict[Any, Any]:
        """Fork a chart, table, or map and create an editable copy.

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.

        Returns
        -------
        dict
            A dictionary containing the information of the chart, table, or map.
        """
        _header = self._auth_header
        _header["accept"] = "*/*"

        url = f"{self._CHARTS_URL}/{chart_id}/fork"
        response = r.post(url=url, headers=_header)

        if response.ok:
            fork = response.json()
            logger.debug(f"Chart {chart_id} copied to {fork['id']}")
            return fork
        else:
            msg = (
                "Chart could not be forked. If it's a chart you created, ",
                "you should trying copying it instead.",
            )
            logger.error(msg)
            raise Exception(msg)

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
            logger.debug(f"Successfully deleted chart with id {chart_id}")
            return None

    def get_charts(
        self,
        user_id: str = "",
        published: str = "true",
        search: str = "",
        order: str = "DESC",
        order_by: str = "createdAt",
        limit: int = 25,
        folder_id: str = "",
        team_id: str = "",
    ) -> None | list[Any]:
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
            Attribute to order by. One of createdAt, email, id, or name,
            by default "createdAt"
        limit : int, optional
            Maximum items to fetch, by default 25
        folder_id : str, optional
            ID of folder in Datawrapper.de where to list charts, by default ""
        team_id : str, optional
            ID of the team where to list charts. The authenticated user must have access
            to this team, by default ""

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
        if folder_id:
            _query["folderId"] = folder_id
        if team_id:
            _query["teamId"] = team_id

        get_charts_response = r.get(url=_url, headers=_header, params=_query)

        if get_charts_response.status_code == 200:
            return get_charts_response.json()["list"]  # type: ignore
        else:
            msg = "Could not retrieve charts at this moment."
            logger.error(msg)
            raise Exception(msg)
