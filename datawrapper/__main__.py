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
from typing import Any

import IPython
import pandas as pd
import requests as r
from IPython.display import HTML, Image

from .exceptions import FailedRequest

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
    _ME_URL = _BASE_URL + "/v3/me"
    _CHARTS_URL = _BASE_URL + "/v3/charts"
    _PUBLISH_URL = _BASE_URL + "/charts"
    _BASEMAPS_URL = _BASE_URL + "/v3/basemaps"
    _FOLDERS_URL = _BASE_URL + "/v3/folders"
    _LOGIN_URL = _BASE_URL + "/v3/auth/login"
    _LOGIN_SCOPES_URL = _BASE_URL + "/v3/auth/token-scopes"
    _LOGIN_TOKENS_URL = _BASE_URL + "/v3/auth/login-tokens"
    _TEAMS_URL = _BASE_URL + "/v3/teams"
    _THEMES_URL = _BASE_URL + "/v3/themes"

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

    def delete(self, url: str, timeout: int = 15) -> bool:
        """Make a DELETE request to the Datawrapper API.

        Parameters
        ----------
        url : str
            The URL to request.
        timeout : int, optional
            The timeout for the request in seconds, by default 15

        Returns
        -------
        bool
            Whether the request was successful.
        """
        # Set the headers
        headers = self._auth_header
        headers["accept"] = "*/*"

        # Make the request
        response = r.delete(url, headers=headers)

        # Handle the response
        if response.ok:
            return True
        else:
            logger.error(
                f"Delete request failed with status code {response.status_code}."
            )
            raise FailedRequest(response)

    def get(self, url: str, params: dict | None = None, timeout: int = 15) -> Any:
        """Make a GET request to the Datawrapper API.

        Parameters
        ----------
        url : str
            The URL to request.
        params : dict, optional
            A dictionary of parameters to pass to the request, by default None
        timeout : int, optional
            The timeout for the request in seconds, by default 15

        Returns
        -------
        Any
            An object containing the response from the API.
        """
        # Set headers
        headers = self._auth_header
        headers["accept"] = "*/*"

        # Make the request
        response = r.get(
            url=url,
            headers=headers,
            params=params,
            timeout=timeout,
        )

        # Check if the request was successful
        if response.ok:
            # Return the data as json if the mimetype is json
            if "json" in response.headers["content-type"]:
                return response.json()
            # If it's a csv, read the text into a dataframe
            elif "text/csv" in response.headers["content-type"]:
                return pd.read_csv(StringIO(response.text))
            # Otherwise just return the text
            else:
                return response.text
        # If not, raise an exception
        else:
            logger.error(f"Get request failed with status code {response.status_code}.")
            raise FailedRequest(response)

    def patch(
        self,
        url: str,
        data: dict | None = None,
        timeout: int = 15,
        extra_headers: dict | None = None,
    ) -> dict:
        """Make a PATCH request to the Datawrapper API.

        Parameters
        ----------
        url : str
            The URL to request.
        data : dict
            A dictionary of data to pass to the request, by default None
        timeout : int, optional
            The timeout for the request in seconds, by default 15
        extra_headers : dict, optional
            A dictionary of extra headers to pass to the request, by default None
        """
        # Set headers
        headers = self._auth_header
        headers["accept"] = "*/*"
        headers["content-type"] = "application/json"

        # Add extra headers if provided
        if extra_headers:
            headers.update(extra_headers)

        # Set kwargs to post
        kwargs = {"headers": headers, "timeout": timeout}

        # Convert data to json
        if data:
            kwargs["data"] = json.dumps(data)

        # Make the request
        response = r.patch(url, **kwargs)

        # Check if the request was successful
        if response.ok:
            # Return the data as json
            return response.json()
        # If not, raise an exception
        else:
            logger.error(
                f"Patch request failed with status code {response.status_code}."
            )
            raise FailedRequest(response)

    def post(
        self,
        url: str,
        data: dict | None = None,
        timeout: int = 15,
        extra_headers: dict | None = None,
    ) -> dict:
        """Make a POST request to the Datawrapper API.

        Parameters
        ----------
        url : str
            The URL to request.
        data : dict
            A dictionary of data to pass to the request, by default None
        timeout : int, optional
            The timeout for the request in seconds, by default 15
        extra_headers : dict, optional
            A dictionary of extra headers to pass to the request, by default None

        Returns
        -------
        dict
            A dictionary containing the response from the API.
        """
        # Set headers
        headers = self._auth_header
        headers["accept"] = "*/*"

        # Add extra headers if provided
        if extra_headers:
            headers.update(extra_headers)

        # Set kwargs to post
        kwargs = {"headers": headers, "timeout": timeout}

        # Convert data to json
        if data:
            kwargs["data"] = json.dumps(data)

        # Make the request
        response = r.post(url, **kwargs)

        # Check if the request was successful
        if response.ok:
            # Return the data as json
            return response.json()
        # If not, raise an exception
        else:
            logger.error(
                f"Post request failed with status code {response.status_code}."
            )
            raise FailedRequest(response)

    def account_info(self) -> dict:
        """A deprecated method for calling get_my_account."""
        # Issue a deprecation warning
        logger.warning(
            "This method is deprecated and will be removed in a future version. "
            "Use get_account_info instead."
        )

        # Use the newer method
        return self.get_my_account()

    def get_my_account(self) -> dict:
        """Access your account information.

        Returns
        -------
        dict
            A dictionary containing your account information.
        """
        return self.get(self._ME_URL)

    def update_my_account(
        self,
        name: str | None = None,
        email: str | None = None,
        role: str | None = None,
        language: str | None = None,
        password: str | None = None,
        old_password: str | None = None,
    ) -> dict:
        """Update your account information.

        Parameters
        ----------
        name : str, optional
            Your new name, by default None
        email : str, optional
            Your new email, by default None
        role : str, optional
            Your new role, by default None
        language: str, optional
            Your new language, by default None
        password: str, optional
            Your new, strong password, by default None
        old_password: str, optional
            Your previous password, by default None

        Returns
        -------
        dict
            A dictionary containing your updated account information.
        """
        _query: dict = {}
        if name:
            _query["name"] = name
        if email:
            _query["email"] = email
        if role:
            _query["role"] = role
        if language:
            _query["language"] = language
        if password and old_password:
            _query["password"] = password
            _query["oldPassword"] = old_password
        if password and not old_password:
            msg = "You must provide your old password to change it."
            logger.error(msg)
            raise Exception(msg)
        if old_password and not password:
            msg = "You must provide a new password to change it."
            logger.error(msg)
            raise Exception(msg)

        return self.patch(
            self._ME_URL,
            data=_query,
        )

    def update_my_settings(
        self,
        active_team: str | None = None,
    ) -> dict:
        """Update your account information.

        Parameters
        ----------
        active_team: str, optional
            Your active team

        Returns
        -------
        dict
            The user settings dictionary following the change.
        """
        _query: dict = {}
        if active_team:
            _query["activeTeam"] = active_team

        if not _query:
            msg = "No updates submitted."
            logger.error(msg)
            raise Exception(msg)

        return self.patch(
            f"{self._ME_URL}/settings",
            data=_query,
        )

    def get_my_recently_edited_charts(
        self,
        limit: str | int = 100,
        offset: str | int = 0,
        min_last_edit_step: str | int = 0,
    ) -> dict:
        """Get a list of your recently edited charts.

        Parameters
        ----------
        limit: str | int
            Maximum items to fetch. Useful for pagination. 100 by default.
        offset: str | int
            Number of items to skip. Useful for pagination. Zero by default.
        min_last_edit_step: str | int
            Filter visualizations by the last editor step they've
            been opened in (1=upload, 2=describe, 3=visualize, etc).
            Zero by default.

        Returns
        -------
        dict
            A dictionary with the list of charts and metadata about the selection.
        """
        _query: dict = {}
        if limit:
            _query["limit"] = limit
        if offset:
            _query["offset"] = offset
        if min_last_edit_step:
            _query["minLastEditStep"] = min_last_edit_step

        return self.get(
            self._ME_URL + "/recently-edited-charts",
            params=_query,
        )

    def get_my_recently_published_charts(
        self,
        limit: str | int = 100,
        offset: str | int = 0,
        min_last_edit_step: str | int = 0,
    ) -> dict:
        """Get a list of your recently published charts.

        Parameters
        ----------
        limit: str | int
            Maximum items to fetch. Useful for pagination. 100 by default.
        offset: str | int
            Number of items to skip. Useful for pagination. Zero by default.
        min_last_edit_step: str | int
            Filter visualizations by the last editor step they've
            been opened in (1=upload, 2=describe, 3=visualize, etc).
            Zero by default.

        Returns
        -------
        dict
            A dictionary with the list of charts and metadata about the selection.
        """
        _query: dict = {}
        if limit:
            _query["limit"] = limit
        if offset:
            _query["offset"] = offset
        if min_last_edit_step:
            _query["minLastEditStep"] = min_last_edit_step

        return self.get(
            self._ME_URL + "/recently-published-charts",
            params=_query,
        )

    def get_themes(
        self, limit: str | int = 100, offset: str | int = 0, deleted: bool = False
    ) -> dict:
        """Get a list of themes in your Datawrapper account.

        Parameters
        ----------
        limit: str | int
            Maximum items to fetch. Useful for pagination. Default 100.
        offset: str | int
            Number of items to skip. Useful for pagination. Default zero.
        deleted: bool
            Whether to include deleted themes

        Returns
        -------
        dict
            A dictionary containing the themes in your Datawrapper account.
        """
        _query = {
            "limit": limit,
            "offset": offset,
            "deleted": json.dumps(deleted),
        }

        return self.get(
            self._THEMES_URL,
            params=_query,
        )

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

    def refresh_data(self, chart_id: str) -> dict:
        """Fetch configured external data and add it to the chart.

        Parameters
        ----------
        chart_id : str
            ID of chart, table or map to add data to.

        Returns
        -------
        dict
            A dictionary containing the chart's information.
        """
        return self.post(f"{self._CHARTS_URL}/{chart_id}/data/refresh")

    def create_chart(
        self,
        title: str = "New Chart",
        chart_type: str = "d3-bars-stacked",
        data: pd.DataFrame | str | None = None,
        folder_id: str = "",
        organization_id: str = "",
        metadata: dict | None = None,
    ) -> dict:
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
        # Set chart properties
        _data = {"title": title, "type": chart_type}
        if folder_id:
            _data["folderId"] = folder_id
        if organization_id:
            _data["organizationId"] = organization_id
        if metadata:
            _data["metadata"] = metadata  # type: ignore

        # Create chart
        chart_info = self.post(
            self._CHARTS_URL,
            data=_data,
            extra_headers={"content-type": "application/json"},
        )

        # Add data if provided
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
    ) -> dict:
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
        _query = {
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
        return self.patch(
            f"{self._CHARTS_URL}/{chart_id}",
            data=_query,
        )

    def publish_chart(self, chart_id: str, display: bool = True) -> dict | HTML:
        """Publishes a chart, table or map.

        Parameters
        ----------
        chart_id : str
            ID of chart, table or map.
        display : bool, optional
            Display the published chart as output in notebook cell, by default True

        Returns
        -------
        dict | HTML
            Either a dictionary containing the published chart's information or an HTML
            object displaying the chart.
        """
        chart_info = self.post(f"{self._PUBLISH_URL}/{chart_id}/publish")
        if display:
            iframe_code = chart_info["data"]["metadata"]["publish"]["embed-codes"][
                "embed-method-iframe"
            ]
            return HTML(iframe_code)
        else:
            return chart_info

    def chart_properties(self, chart_id: str) -> dict:
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
        return self.get(self._CHARTS_URL + f"/{chart_id}")

    def chart_data(self, chart_id: str):
        """Retrieve the data stored for a specific chart, table or map, which is typically CSV.

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.

        Returns
        -------
        dict
            A dictionary containing the information of the chart, table, or map.
        """
        return self.get(self._CHARTS_URL + f"/{chart_id}/data")

    def update_metadata(self, chart_id: str, properties: dict) -> dict:
        """Update a chart, table, or map's metadata.

        Example: https://developer.datawrapper.de/docs/creating-a-chart-new#edit-colors

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.
        properties : dict
            A python dictionary of properties to update.
        """
        return self.patch(
            f"{self._CHARTS_URL}/{chart_id}",
            data={"metadata": properties},
        )

    def update_chart(
        self,
        chart_id: str,
        title: str = "",
        theme: str = "",
        chart_type: str = "",
        language: str = "",
        folder_id: str = "",
        organization_id: str = "",
    ) -> dict | HTML:
        """Updates a chart's title, theme, type, language, folder or organization.

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

        self.patch(
            f"{self._CHARTS_URL}/{chart_id}",
            data=_query,
        )

        return self.publish_chart(chart_id)

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

    def get_basemaps(self) -> list[dict]:
        """Get a list of the available basemaps.

        Returns
        -------
        list[dict]
            A list of dictionaries containing the basemaps available in your Datawrapper account.
        """
        return self.get(self._BASEMAPS_URL)

    def get_basemap(self, basemap_id: str, wgs84: bool = False) -> dict:
        """Get the metdata of the requested basemap.

        Parameters
        ----------
        basemap_id : str
            ID of basemap to get.
        wgs84 : bool, optional
            Whether to return the basemap in the WGS84 project, by default False

        Returns
        -------
        dict
            A dictionary containing the requested basemap's metadata.
        """
        return self.get(
            f"{self._BASEMAPS_URL}/{basemap_id}",
            params={"wgs84": wgs84},
        )

    def get_basemap_key(self, basemap_id: str, basemap_key: str) -> dict:
        """Get the list of available values for a basemap's key.

        Parameters
        ----------
        basemap_id : str
            ID of basemap to get.
        basemap_key : str
            Metadata key of basemap to get.

        Returns
        -------
        dict
            A dictionary containing the requested data.
        """
        return self.get(f"{self._BASEMAPS_URL}/{basemap_id}/{basemap_key}")

    def get_folders(self) -> dict:
        """Get a list of folders in your Datawrapper account.

        Returns
        -------
        dict
            A dictionary containing the folders in your Datawrapper account and their
            information.
        """
        return self.get(self._FOLDERS_URL)

    def get_folder(self, folder_id: str | int) -> dict:
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
        return self.get(self._FOLDERS_URL + f"/{folder_id}")

    def create_folder(
        self,
        name: str,
        parent_id: str | int | None = None,
        team_id: str | int | None = None,
    ) -> dict:
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
        _query: dict = {"name": name}
        if parent_id:
            _query["parentId"] = parent_id
        if team_id:
            _query["teamId"] = team_id

        return self.post(
            self._FOLDERS_URL,
            data=_query,
            extra_headers={"content-type": "application/json"},
        )

    def update_folder(
        self,
        folder_id: str | int,
        name: str | None = None,
        parent_id: str | int | None = None,
        team_id: str | int | None = None,
        user_id: str | int | None = None,
    ) -> dict:
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
        dict
            A dictionary with the folder's updated metadata
        """
        _query: dict = {}
        if name:
            _query["name"] = name
        if parent_id:
            _query["parentId"] = parent_id
        if team_id:
            _query["teamId"] = team_id
        if user_id:
            _query["userId"] = user_id

        return self.patch(
            f"{self._FOLDERS_URL}/{folder_id}",
            data=_query,
        )

    def delete_folder(self, folder_id: str | int) -> bool:
        """Delete an existing folder.

        Parameters
        ----------
        folder_id : str | int
            ID of folder to delete.

        Returns
        -------
        bool
            True if the folder was deleted successfully.
        """
        return self.delete(f"{self._FOLDERS_URL }/{folder_id}")

    def move_chart(self, chart_id: str, folder_id: str) -> dict:
        """Moves a chart, table, or map to a specified folder.

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.
        folder_id : str
            ID of folder to move visualization to.
        """
        return self.patch(
            url=self._CHARTS_URL + f"/{chart_id}",
            data={"folderId": folder_id},
        )

    def copy_chart(self, chart_id: str) -> dict:
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
        return self.post(f"{self._CHARTS_URL}/{chart_id}/copy")

    def fork_chart(self, chart_id: str) -> dict:
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
        return self.post(f"{self._CHARTS_URL}/{chart_id}/fork")

    def delete_chart(self, chart_id: str) -> bool:
        """Deletes a specified chart, table or map.

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.

        Returns
        -------
        bool
            True if the chart was deleted successfully.
        """
        return self.delete(f"{self._CHARTS_URL}/{chart_id}")

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
        _query: dict = {}
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

        return self.get(self._CHARTS_URL, params=_query)

    def get_login_tokens(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Retrieves all login tokens associated to the current user.

        Parameters
        ----------
        limit : int, optional
            Maximum items to fetch, by default 100. Useful for pagination.
        offset : int, optional
            Offset for pagination, by default 0.

        Returns
        -------
        dict
            A dictionary containing the login tokens for your Datawrapper account.
        """
        _query: dict[str, Any] = {}
        if limit:
            _query["limit"] = limit
        if offset:
            _query["offset"] = offset

        return self.get(self._LOGIN_TOKENS_URL, params=_query)

    def create_login_token(
        self,
    ) -> dict:
        """Creates a new login token to authenticate a user, for use in CMS integrations.

        Login tokens are valid for five minutes and can only be used once.

        Returns
        -------
        dict
            A dictionary containing the login token's information.
        """
        return self.post(
            self._LOGIN_TOKENS_URL,
            extra_headers={"content-type": "application/json"},
        )

    def delete_login_token(self, token_id: str | int) -> bool:
        """Deletes a login token.

        Parameters
        ----------
        token_id : str | int
            ID of login token to delete.

        Returns
        -------
        bool
            True if the login token was deleted successfully.
        """
        return self.delete(f"{self._LOGIN_TOKENS_URL}/{token_id}")

    def login(self, token: str) -> str:
        """Login using a one-time login token and redirect to the URL associated with the token.

        For use in CMS integrations.

        Parameters
        ----------
        token : str
            Login token.

        Returns
        -------
        str
            The HTML of the page that the token redirects to.
        """
        return self.get(f"{self._LOGIN_URL}/{token}")

    def get_token_scopes(self) -> list:
        """Get the scopes that are available to the current user.

        Returns
        -------
        list
            A list containing the scopes available to the current user.
        """
        return self.get(self._LOGIN_SCOPES_URL)

    def get_teams(
        self,
        search: str | None = None,
        order: str = "ASC",
        order_by: str = "name",
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Get a list of teams in your Datawrapper account.

        Parameters
        ----------
        search : str, optional
            Search for teams with a specific name, by default no search filter is applied.
        order : str, optional
            Result order (ascending or descending), by default "ASC." Supply "DESC" for descending order.
        order_by : str, optional
            Attribute to order by. By default "name"
        limit : int, optional
            Maximum items to fetch, by default 100. Useful for pagination.
        offset : int, optional
            Offset for pagination, by default 0.

        Returns
        -------
        dict
            A dictionary containing the teams in your Datawrapper account.
        """
        _query: dict = {}
        if search:
            _query["search"] = search
        if order:
            _query["order"] = order
        if order_by:
            _query["orderBy"] = order_by
        if limit:
            _query["limit"] = limit
        if offset:
            _query["offset"] = offset

        return self.get(self._TEAMS_URL, params=_query)

    def create_team(
        self,
        name: str,
        default_theme: str | None = None,
    ) -> dict:
        """Create a new team.

        Parameters
        ----------
        name : str
            Name of the team.
        default_theme : str, optional
            Default theme of charts made by the team, optional.

        Returns
        -------
        dict
            A dictionary containing the team's information.
        """
        _query: dict = {"name": name}
        if default_theme:
            _query["defaultTheme"] = default_theme

        return self.post(
            self._TEAMS_URL,
            data=_query,
            extra_headers={"content-type": "application/json"},
        )

    def get_team(self, team_id: str) -> dict:
        """Get an existing team.

        Parameters
        ----------
        team_id : str
            ID of team to get.

        Returns
        -------
        dict
            A dictionary containing the team's information.
        """
        return self.get(self._TEAMS_URL + f"/{team_id}")

    def update_team(
        self,
        team_id: str,
        name: str | None = None,
        default_theme: str | None = None,
    ) -> dict:
        """Update an existing team.

        Parameters
        ----------
        team_id : str
            ID of team to update.
        name : str, optional
            Name to change the team to.
        default_theme : str, optional
            Default theme of charts made by the team.

        Returns
        -------
        dict
            A dictionary with the team's updated metadata
        """
        _query = {}
        if name:
            _query["name"] = name
        if default_theme:
            _query["defaultTheme"] = default_theme

        if not _query:
            msg = "No parameters were supplied to update the team."
            logger.error(msg)
            raise Exception(msg)

        return self.patch(
            f"{self._TEAMS_URL}/{team_id}",
            data=_query,
        )

    def delete_team(self, team_id: str) -> bool:
        """Delete an existing team.

        Parameters
        ----------
        team_id : str
            ID of team to delete.

        Returns
        -------
        bool
            True if team was deleted successfully.
        """
        return self.delete(f"{self._TEAMS_URL}/{team_id}")
