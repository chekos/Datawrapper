"""A lightweight Python wrapper for the Datawrapper API."""

from __future__ import annotations

import json
import logging
import os
import warnings
from io import StringIO
from pathlib import Path
from typing import Any

import pandas as pd
import requests as r
from IPython.display import IFrame, Image

from .exceptions import FailedRequestError, InvalidRequestError, RateLimitError

logger = logging.getLogger(__name__)


class Datawrapper:
    """Handles working with the Datawrapper API.

    Your main interface for configuring Datawrapper, creating, editing and
    publishing charts, maps and tables.
    """

    _BASE_URL = "https://api.datawrapper.de"  #: The base URL for all API methods
    _API_TOKEN_URL = (
        _BASE_URL + "/v3/auth/tokens"
    )  #: The endpoint for API token methods
    _ME_URL = (
        _BASE_URL + "/v3/me"
    )  #: The endpoint for methods related to the logged in user
    _CHARTS_URL = (
        _BASE_URL + "/v3/charts"
    )  #: The endpoint for methods related to charts
    _BASEMAPS_URL = _BASE_URL + "/v3/basemaps"  #: The endpoint for basemap methods
    _FOLDERS_URL = _BASE_URL + "/v3/folders"  #: The endpoint for folder methods
    _LOGIN_URL = _BASE_URL + "/v3/auth/login"  #: The endpoint for login methods
    _LOGIN_SCOPES_URL = (
        _BASE_URL + "/v3/auth/token-scopes"
    )  #: The endpoint for login scopes
    _LOGIN_TOKENS_URL = (
        _BASE_URL + "/v3/auth/login-tokens"
    )  #: The endpoint for login tokens
    _OEMBED_URL = _BASE_URL + "/v3/oembed"  #: The endpoint for oembed methods
    _RIVER_URL = _BASE_URL + "/v3/river"  #: The endpoint for river methods
    _WORKSPACES_URL = (
        _BASE_URL + "/v3/workspaces"
    )  #: The endpoint for workspace methods
    _THEMES_URL = _BASE_URL + "/v3/themes"  #: The endpoint for theme methods
    _USERS_URL = _BASE_URL + "/v3/users"  #: The endpoint for user methods

    _ACCESS_TOKEN = os.getenv("DATAWRAPPER_ACCESS_TOKEN")  #: The access token to use

    def __init__(self, access_token=_ACCESS_TOKEN):
        """Initalize a connection with the Datawrapper API.

        Parameters
        ----------
        access_token : str, optional
            The access token to use, by default it will look for DATAWRAPPER_ACCESS_TOKEN environment variable.
            To create a token head to app.datawrapper.de/account/api-tokens.
        """

        self._access_token = access_token

    def _get_auth_header(self) -> dict:
        """Get the authentication header for the Datawrapper API.

        Returns
        -------
        dict
            The authentication header for the Datawrapper API.
        """
        return {"Authorization": f"Bearer {self._access_token}"}

    #
    # Web request methods
    #

    def delete(
        self,
        url: str,
        timeout: int = 15,
        data: dict | None = None,
        extra_headers: dict | None = None,
    ) -> bool:
        """Make a DELETE request to the Datawrapper API.

        Parameters
        ----------
        url : str
            The URL to request.
        timeout : int, optional
            The timeout for the request in seconds, by default 15
        data : dict, optional
            A dictionary of data to pass to the request, by default None
        extra_headers : dict, optional
            A dictionary of extra headers to pass to the request, by default None

        Returns
        -------
        bool
            Whether the request was successful.
        """
        # Set the headers
        headers = self._get_auth_header()
        headers["accept"] = "*/*"

        # Add extra headers if provided
        if extra_headers:
            headers.update(extra_headers)

        # Set kwargs
        kwargs = {"headers": headers, "timeout": timeout}

        # Add data if provided
        if data:
            kwargs["json"] = data

        # Make the request
        response = r.delete(url, **kwargs)  # type: ignore[arg-type]

        # Handle the response
        if response.ok:
            return True
        logger.error(f"Delete request failed with status code {response.status_code}.")
        if response.status_code == 429:
            raise RateLimitError(response)
        raise FailedRequestError(response)

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
        headers = self._get_auth_header()
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
            if "text/csv" in response.headers["content-type"]:
                return pd.read_csv(StringIO(response.text))
            # Otherwise just return the content
            return response.content
        # If not, raise an exception
        logger.error(f"Get request failed with status code {response.status_code}.")
        if response.status_code == 429:
            raise RateLimitError(response)
        raise FailedRequestError(response)

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

        Returns
        -------
        dict
            A dictionary containing the response from the API.
        """
        # Set headers
        headers = self._get_auth_header()
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
        response = r.patch(url, **kwargs)  # type: ignore[arg-type]

        # Check if the request was successful
        if response.ok:
            # Return the data as json
            return response.json()
        # If not, raise an exception
        logger.error(f"Patch request failed with status code {response.status_code}.")
        if response.status_code == 429:
            raise RateLimitError(response)
        raise FailedRequestError(response)

    def post(
        self,
        url: str,
        data: dict | None = None,
        timeout: int = 30,
        extra_headers: dict | None = None,
    ) -> dict | bool:
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
        dict | bool
            A dictionary containing the response from the API or True if the request was
            successful but did not return any data.
        """
        # Set headers
        headers = self._get_auth_header()
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
        response = r.post(url, **kwargs)  # type: ignore[arg-type]

        # Check if the request was successful
        if response.ok:
            # Return the data as json
            if response.text:
                return response.json()
            return True
        # If not, raise an exception
        logger.error(f"Post request failed with status code {response.status_code}.")
        if response.status_code == 429:
            raise RateLimitError(response)
        raise FailedRequestError(response)

    def put(
        self,
        url: str,
        data: dict | bytes | None = None,
        timeout: int = 15,
        extra_headers: dict | None = None,
        dump_data: bool = True,
    ) -> bool:
        """Make a PUT request to the Datawrapper API.

        Parameters
        ----------
        url : str
            The URL to request.
        data : dict | bytes
            A dictionary of data to pass to the request, or raw bytes when dump_data is False, by default None
        timeout : int, optional
            The timeout for the request in seconds, by default 15
        extra_headers : dict, optional
            A dictionary of extra headers to pass to the request, by default None
        dump_data: bool, optional
            Whether to dump the data to json, by default True

        Returns
        -------
        bool
            Whether the request was successful.
        """
        # Set headers
        headers = self._get_auth_header()
        headers["accept"] = "*/*"

        # Add extra headers if provided
        if extra_headers:
            headers.update(extra_headers)

        # Set kwargs to post
        kwargs = {"headers": headers, "timeout": timeout}

        # Convert data to json
        if data:
            if dump_data:
                kwargs["data"] = json.dumps(data)
            else:
                kwargs["data"] = data

        # Make the request
        response = r.put(url, **kwargs)  # type: ignore[arg-type]

        # Handle the response
        if response.ok:
            return True
        logger.error(f"Put request failed with status code {response.status_code}.")
        if response.status_code == 429:
            raise RateLimitError(response)
        raise FailedRequestError(response)

    #
    # Login token actions
    #

    def get_login_tokens(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
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
        _query: dict = {}
        if limit:
            _query["limit"] = limit
        if offset:
            _query["offset"] = offset

        return self.get(self._LOGIN_TOKENS_URL, params=_query)

    def create_login_token(self) -> dict:
        """Creates a new login token to authenticate a user, for use in CMS integrations.

        Login tokens are valid for five minutes and can only be used once.

        Returns
        -------
        dict
            A dictionary containing the login token's information.
        """
        response = self.post(
            self._LOGIN_TOKENS_URL,
            extra_headers={"content-type": "application/json"},
        )
        assert isinstance(response, dict)
        return response

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

    #
    # API token methods
    #

    def get_api_tokens(self, limit: int = 100, offset: int = 0) -> dict:
        """Retrieves all API tokens associated to the current user.

        Response will not include full tokens for security reasons. Requires scope `auth:read`.

        Parameters
        ----------
        limit : int, optional
            Maximum items to fetch, by default 100. Useful for pagination.
        offset : int, optional
            Offset for pagination, by default 0.

        Returns
        -------
        dict
            A dictionary containing the API tokens for your Datawrapper account.
        """
        _query: dict = {}
        if limit:
            _query["limit"] = limit
        if offset:
            _query["offset"] = offset

        return self.get(self._API_TOKEN_URL, params=_query)

    def create_api_token(self, comment: str, scopes: list[str]) -> dict:
        """Create a new API Token.

        Make sure to save the token somewhere, since you won't be able to see it again. Requires scope `auth:write`.

        Parameters
        ----------
        comment : str
            Comment to describe the API token. Tip: Use something to remember where this specific token is used.
        scopes : list[str]
            List of scopes for the API token.

        Returns
        -------
        dict
            A dictionary containing the API token's information.
        """
        response = self.post(
            self._API_TOKEN_URL,
            data={"comment": comment, "scopes": scopes},
            extra_headers={"content-type": "application/json"},
        )
        assert isinstance(response, dict)
        return response

    def update_api_token(
        self, id: str | int, comment: str, scopes: list[str] | None = None
    ) -> bool:
        """Updates an existing API token.

        Parameters
        ----------
        id : str | int
            ID of API token to update.
        comment : str
            Comment to describe the API token. Tip: Use something to remember where this specific token is used.
        scopes : list[str], optional
            List of scopes for the API token.

        Returns
        -------
        bool
            True if the API token was updated successfully.
        """
        _query: dict = {"comment": comment}
        if scopes:
            _query["scopes"] = scopes

        return self.put(
            f"{self._API_TOKEN_URL}/{id}",
            data=_query,
            extra_headers={"content-type": "application/json"},
        )

    def delete_api_token(self, token_id: str | int) -> bool:
        """Deletes an API token.

        Parameters
        ----------
        token_id : str | int
            ID of API token to delete.

        Returns
        -------
        bool
            True if the API token was deleted successfully.
        """
        return self.delete(f"{self._API_TOKEN_URL}/{token_id}")

    def get_token_scopes(self) -> list[str]:
        """Get the scopes that are available to the current user.

        Returns
        -------
        list[str]
            A list containing the scopes available to the current user.
        """
        return self.get(self._LOGIN_SCOPES_URL)

    #
    # Basemap actions
    #

    def get_basemaps(self) -> list[dict]:
        """Get a list of the available basemaps.

        Returns
        -------
        list[dict]
            A list of dictionaries containing the basemaps available in your Datawrapper account.
        """
        return self.get(self._BASEMAPS_URL)

    def get_basemap(self, basemap_id: str, wgs84: bool = False) -> dict:
        """Get the metadata of the requested basemap.

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

    #
    # Charts methods
    #

    def get_charts(
        self,
        user_id: str = "",
        published: bool = True,
        search: str = "",
        order: str = "DESC",
        order_by: str = "createdAt",
        limit: int = 25,
        folder_id: int | None = None,
        team_id: str = "",
    ) -> None | list[Any]:
        """Retrieves a list of charts by User

        Parameters
        ----------
        user_id : str, optional
            ID of the user to fetch charts for, by default ""
        published : bool, optional
            Flag to filter resutls by publish status, by default True
        search : str, optional
            Search for charts with a specific title, by default ""
        order : str, optional
            Result order (ascending or descending), by default "DESC"
        order_by : str, optional
            Attribute to order by. One of createdAt, email, id, or name,
            by default "createdAt"
        limit : int, optional
            Maximum items to fetch, by default 25
        folder_id : int, optional
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
            _query["published"] = json.dumps(published)
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

    def get_chart(self, chart_id: str) -> dict:
        """Retrieve information of a specific chart, table or map.

        .. deprecated::
            Use the chart factory function instead to get typed chart instances.
            This method will be removed in a future version.

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.

        Returns
        -------
        dict
            A dictionary containing the information of the chart, table, or map.
        """
        warnings.warn(
            "get_chart() is deprecated and will be removed in a future version. "
            "Use the chart factory function instead to get typed chart instances. "
            "Example: import datawrapper as dw; chart = dw.get_chart(chart_id='abc123')",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get(f"{self._CHARTS_URL}/{chart_id}")

    def chart_properties(self, chart_id: str) -> dict:
        """A deprecated method of the get_chart method."""
        # Issue a deprecation warning
        logger.warning(
            "This method is deprecated and will be removed in a future version. "
            "Use get_chart instead."
        )

        # Use the newer method
        return self.get_chart(chart_id)

    def create_chart(
        self,
        title: str,
        chart_type: str,
        theme: str | None = None,
        data: pd.DataFrame | str | None = None,
        external_data_url: str | None = None,
        folder_id: int | None = None,
        organization_id: str | None = None,
        forkable: bool | None = None,
        language: str | None = None,
        metadata: dict | None = None,
    ) -> dict:
        """Creates a new Datawrapper chart, table or map.

        .. deprecated::
            Use the object-oriented chart classes instead (e.g., BarChart, LineChart).
            This method will be removed in a future version.

        Parameters
        ----------
        title : str
            Title for new chart, table or map, by default "New Chart"
        chart_type : str
            Chart type to be created. See https://developer.datawrapper.de/docs/chart-types
        theme : str, optional
            Theme to use for new chart, table or map, by default None
        data : pd.DataFrame | str, optional
            A pandas DataFrame or string containing the data to be added,
            by default None
        external_data_url: str, optional
            URL to external data to be added to the chart, table or map,
        folder_id : int, optional
            ID of folder in Datawrapper.de for the chart, table or map to be created in,
            by default ""
        organization_id : str, optional
            ID of the team where the chart should be created. The authenticated user
            must have access to this team.
        forkable : bool, optional
            Whether the chart should be forkable or not, by default None
        language: str, optional
            Locale of the chart (i.e. en-US), by default None
        metadata: dict, optional
            A Python dictionary of properties to add.

        Returns
        -------
        dict
            A dictionary containing the created chart's information.
        """
        warnings.warn(
            "create_chart() is deprecated and will be removed in a future version. "
            "Use the object-oriented chart classes instead. "
            "Example: chart = BarChart(title='My Chart', data=df).create()",
            DeprecationWarning,
            stacklevel=2,
        )

        # Set chart properties
        _query: dict[str, Any] = {"title": title, "type": chart_type}
        if theme:
            _query["theme"] = theme
        if folder_id:
            _query["folderId"] = folder_id
        if organization_id:
            _query["organizationId"] = organization_id
        if forkable:
            _query["forkable"] = json.dumps(forkable)
        if language:
            _query["language"] = language
        if external_data_url:
            _query["externalData"] = external_data_url
        if metadata:
            _query["metadata"] = metadata

        # Create chart
        obj = self.post(
            self._CHARTS_URL,
            data=_query,
            extra_headers={"content-type": "application/json"},
        )
        assert isinstance(obj, dict)

        # Add data, if provided
        if data is not None:
            self.add_data(chart_id=obj["id"], data=data)

        # Return the result
        return obj

    def update_chart(
        self,
        chart_id: str,
        title: str | None = None,
        chart_type: str | None = None,
        theme: str | None = None,
        data: pd.DataFrame | str | None = None,
        external_data_url: str | None = None,
        folder_id: int | None = None,
        organization_id: str | None = None,
        forkable: bool | None = None,
        language: str | None = None,
        metadata: dict | None = None,
    ) -> dict:
        """Updates a chart's title, theme, type, language, folder or organization.

        .. deprecated::
            Use the object-oriented chart classes instead (e.g., BarChart, LineChart).
            This method will be removed in a future version.

        Parameters
        ----------
        chart_id: str
            ID Of chart, table, or map.
        title: str, optional
            New title
        chart_type: str, optional
            New chart type. See https://developer.datawrapper.de/docs/chart-types
        theme: str, optional
            New theme
        data: pd.DataFrame | str, optional
            A pandas DataFrame or string containing the data to be added,
            by default None
        external_data_url: str, optional
            URL to external data to be added to the chart, table or map,
        folder_id: int, optional
            New folder's ID
        organization_id: str, optional
            New organization's ID
        forkable: bool, optional
            Whether the chart should be forkable or not, by default None
        language : str, optional
            New language
        metadata: dict, optional
            A Python dictionary of properties to add.

        Return
        ------
        dict
            A dictionary containing the updated chart's information.

        Raises
        ------
        InvalidRequestError
            If no updates are submitted.
        """
        warnings.warn(
            "update_chart() is deprecated and will be removed in a future version. "
            "Use the object-oriented chart classes instead. "
            "Example: chart = BarChart.get(chart_id='abc123'); chart.title = 'New Title'; chart.update()",
            DeprecationWarning,
            stacklevel=2,
        )

        # Load the query with the provided parameters
        _query: dict[str, Any] = {}
        if title:
            _query["title"] = title
        if chart_type:
            _query["type"] = chart_type
        if theme:
            _query["theme"] = theme
        if external_data_url:
            _query["externalData"] = external_data_url
        if folder_id:
            _query["folderId"] = folder_id
        if organization_id:
            _query["organizationId"] = organization_id
        if forkable:
            _query["forkable"] = json.dumps(forkable)
        if language:
            _query["language"] = language
        if metadata:
            _query["metadata"] = metadata

        # If there's nothing there to update, raise an exception
        if not _query and data is None:
            msg = "No updates submitted."
            logger.error(msg)
            raise InvalidRequestError(msg)

        # Update the chart
        if _query:
            obj = self.patch(
                f"{self._CHARTS_URL}/{chart_id}",
                data=_query,
                extra_headers={"content-type": "application/json"},
            )
        else:
            obj = self.get_chart(chart_id)

        # Add data, if provided
        if data is not None:
            self.add_data(chart_id=obj["id"], data=data)

        # Return the result
        return obj

    def update_metadata(self, chart_id: str, metadata: dict) -> dict:
        """A deprecated method of the update_chart method."""
        # Issue a deprecation warning
        logger.warning(
            "This method is deprecated and will be removed in a future version. "
            "Use update_chart instead."
        )

        # Use the newer method
        return self.update_chart(chart_id, metadata=metadata)

    def update_description(
        self,
        chart_id: str,
        source_name: str | None = None,
        source_url: str | None = None,
        intro: str | None = None,
        byline: str | None = None,
        aria_description: str | None = None,
        number_prepend: str | None = None,
        number_append: str | None = None,
        number_format: str | None = None,
        number_divisor: int | None = None,
        hide_title: bool = False,
    ) -> dict:
        """Update a chart's description attributes

        A convienece method for updating the 'describe' key of a chart's metadata.

        Parameters
        ----------
        chart_id : str
            ID of chart, table or map.
        source_name : str, optional
            Source of data
        source_url : str, optional
            URL of source of data
        intro : str, optional
            Introduction of your chart, table or map
        byline : str, optional
            Who made this?
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
        hide_title : bool
            Whether or not to hide the chart title

        Returns
        -------
        dict
            A dictionary containing the updated chart's information.

        Raises
        ------
        InvalidRequestError
            If no updates are submitted.
        """
        # Load the query with the provided parameters
        _query: dict[str, Any] = {"hide-title": hide_title}
        if source_name:
            _query["source-name"] = source_name
        if source_url:
            _query["source-url"] = source_url
        if intro:
            _query["intro"] = intro
        if byline:
            _query["byline"] = byline
        if aria_description:
            _query["aria-description"] = aria_description
        if number_prepend:
            _query["number-prepend"] = number_prepend
        if number_append:
            _query["number-append"] = number_append
        if number_format:
            _query["number-format"] = number_format
        if number_divisor:
            _query["number-divisor"] = number_divisor

        # If there's nothing there to update, raise an exception
        if not _query:
            msg = "No updates submitted."
            logger.error(msg)
            raise InvalidRequestError(msg)

        # Update the chart using the update_chart method
        return self.update_chart(chart_id, metadata={"describe": _query})

    def delete_chart(self, chart_id: str) -> bool:
        """Deletes a chart, table or map.

        .. deprecated::
            Use the object-oriented chart classes instead (e.g., BarChart, LineChart).
            This method will be removed in a future version.

        Parameters
        ----------
        chart_id : str
            ID of chart, table or map.

        Returns
        -------
        bool
            True if the chart was deleted successfully.
        """
        warnings.warn(
            "delete_chart() is deprecated and will be removed in a future version. "
            "Use the object-oriented chart classes instead. "
            "Example: chart = BarChart.get(chart_id='abc123'); chart.delete()",
            DeprecationWarning,
            stacklevel=2,
        )

        return self.delete(f"{self._CHARTS_URL}/{chart_id}")

    def display_chart(self, chart_id: str) -> IFrame:
        """Displays a datawrapper chart.

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.

        Returns
        -------
        IPython.display.IFrame
            IFrame displaying the chart.
        """
        obj = self.get_chart(chart_id)
        src = obj["publicUrl"]
        width = obj["metadata"]["publish"]["embed-width"]
        height = obj["metadata"]["publish"]["embed-height"]
        return IFrame(src, width=width, height=height)

    def copy_chart(self, chart_id: str) -> dict:
        """Copy one of your charts, tables, or maps and create a new editable copy.

        .. deprecated::
            Use the object-oriented chart classes instead (e.g., BarChart, LineChart).
            This method will be removed in a future version.

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.

        Returns
        -------
        dict
            A dictionary containing the information of the chart, table, or map.
        """
        warnings.warn(
            "copy_chart() is deprecated and will be removed in a future version. "
            "Use the object-oriented chart classes instead. "
            "Example: chart = BarChart.get(chart_id='abc123'); duplicate = chart.duplicate()",
            DeprecationWarning,
            stacklevel=2,
        )

        response = self.post(f"{self._CHARTS_URL}/{chart_id}/copy")
        assert isinstance(response, dict)
        return response

    def fork_chart(self, chart_id: str) -> dict:
        """Fork a chart, table, or map and create an editable copy.

        .. deprecated::
            Use the object-oriented chart classes instead (e.g., BarChart, LineChart).
            This method will be removed in a future version.

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.

        Returns
        -------
        dict
            A dictionary containing the information of the chart, table, or map.
        """
        warnings.warn(
            "fork_chart() is deprecated and will be removed in a future version. "
            "Use the object-oriented chart classes instead. "
            "Example: chart = BarChart.get(chart_id='abc123'); fork = chart.fork()",
            DeprecationWarning,
            stacklevel=2,
        )

        response = self.post(f"{self._CHARTS_URL}/{chart_id}/fork")
        assert isinstance(response, dict)
        return response

    def move_chart(self, chart_id: int, folder_id: int) -> dict:
        """Moves a chart, table, or map to a specified folder.

        Parameters
        ----------
        chart_id : int
            ID of chart, table, or map.
        folder_id : int
            ID of folder to move visualization to.
        """
        return self.patch(
            f"{self._CHARTS_URL}/{chart_id}",
            data={"folderId": folder_id},
        )

    def publish_chart(self, chart_id: str, display: bool = False) -> dict | IFrame:
        """Publishes a chart, table or map.

        .. deprecated::
            Use the object-oriented chart classes instead (e.g., BarChart, LineChart).
            This method will be removed in a future version.

        Parameters
        ----------
        chart_id : str
            ID of chart, table or map.
        display : bool, optional
            Display the published chart as output in notebook cell, by default False

        Returns
        -------
        dict | IFrame
            Either a dictionary containing the published chart's information or an IFrame
            object displaying the chart.
        """
        warnings.warn(
            "publish_chart() is deprecated and will be removed in a future version. "
            "Use the object-oriented chart classes instead. "
            "Example: chart = BarChart.get(chart_id='abc123'); chart.publish()",
            DeprecationWarning,
            stacklevel=2,
        )

        obj = self.post(f"{self._CHARTS_URL}/{chart_id}/publish")
        assert isinstance(obj, dict)
        if display:
            src = obj["data"]["publicUrl"]
            width = obj["data"]["metadata"]["publish"]["embed-width"]
            height = obj["data"]["metadata"]["publish"]["embed-height"]
            return IFrame(src, width=width, height=height)
        return obj

    def export_chart(
        self,
        chart_id: str,
        unit: str = "px",
        mode: str = "rgb",
        width: int = 400,
        height: int | str | None = None,
        plain: bool = False,
        zoom: int = 2,
        scale: int = 1,
        border_width: int = 20,
        border_color: str | None = None,
        transparent: bool = False,
        download: bool = False,
        full_vector: bool = False,
        ligatures: bool = True,
        logo: str = "auto",
        logo_id: str | None = None,
        dark: bool = False,
        output: str = "png",
        filepath: str = "./image.png",
        display: bool = False,
    ) -> Path | Image:
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
            by default 400
        height : int | str, optional
            Height of visualization. Can be a number or "auto", by default None
        plain : bool, optional
            Defines if only the visualization should be exported (True), or if it should
             include header and footer as well (False), by default False
        zoom : int, optional
            Defines the multiplier for the png size, by default 2
        scale : int, optional
            Defines the multiplier for the pdf size, by default 1
        border_width : int, optional
            Margin around the visualization, by default 20
        border_color : str, optional
            Color of the border around the visualization, by default None
        transparent : bool, optional
            Set to `True` to export your visualization with a transparent background,
            by default False
        download : bool, optional
            Whether to trigger a download, by default False
        full_vector : bool, optional
            Export as full vector graphic (for supported formats), by default False
        ligatures : bool, optional
            Enable typographic ligatures, by default True
        logo : str, optional
            Logo display setting. One of "auto", "on", or "off", by default "auto"
        logo_id : str, optional
            Custom logo ID to use, by default None
        dark : bool, optional
            Export in dark mode, by default False
        output : str, optional
            One of png, pdf, or svg, by default "png"
        filepath : str, optional
            Name/filepath to save output in, by default "./image.png"
        display : bool, optional
            Whether to display the exported image as output in the notebook cell,
            by default False

        Returns
        -------
        Path | Image
            The file path to the exported image or an Image object displaying the image.
        """
        _query = {
            "unit": unit,
            "mode": mode,
            "width": width,
            "plain": json.dumps(plain),
            "zoom": zoom,
            "scale": scale,
            "borderWidth": border_width,
            "transparent": json.dumps(transparent),
            "download": json.dumps(download),
            "fullVector": json.dumps(full_vector),
            "ligatures": json.dumps(ligatures),
            "logo": logo,
            "dark": json.dumps(dark),
        }

        # Add optional parameters only if provided
        if height is not None:
            _query["height"] = height
        if border_color is not None:
            _query["borderColor"] = border_color
        if logo_id is not None:
            _query["logoId"] = logo_id

        content = self.get(
            f"{self._CHARTS_URL}/{chart_id}/export/{output}", params=_query
        )

        # Set the file path
        _filepath = Path(filepath)
        _filepath = _filepath.with_suffix(f".{output}")

        # Write the file to the file path
        with open(_filepath, "wb") as fh:
            fh.write(content)

        # Display the image if requested
        if display:
            return Image(_filepath)
        # Otherwise return the file path
        logger.debug(f"File exported at {_filepath}")
        return _filepath

    def get_chart_display_urls(self, chart_id: str) -> list[dict]:
        """Get the URLs for the published chart, table or map.

        Parameters
        ----------
        chart_id : str
            ID of chart, table, or map.

        Returns
        -------
        list[dict]
            A list of dictionaries containing the URLs for the published chart, table, or map.
        """
        return self.get(f"{self._CHARTS_URL}/{chart_id}/display-urls")

    def get_iframe_code(self, chart_id: str, responsive: bool = False) -> str:
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
        obj = self.get_chart(chart_id)
        if responsive:
            iframe = obj["metadata"]["publish"]["embed-codes"][
                "embed-method-responsive"
            ]
        else:
            iframe = obj["metadata"]["publish"]["embed-codes"]["embed-method-iframe"]
        return iframe

    def get_data(self, chart_id: str):
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
        return self.get(f"{self._CHARTS_URL}/{chart_id}/data")

    def chart_data(self, chart_id: str):
        """A deprecated method of the get_data method."""
        # Issue a deprecation warning
        logger.warning(
            "This method is deprecated and will be removed in a future version. "
            "Use get_data instead."
        )

        # Use the newer method
        return self.get_data(chart_id)

    def add_data(self, chart_id: str, data: pd.DataFrame | str) -> bool:
        """Add data to a specified chart.

        .. deprecated::
            Use the object-oriented chart classes instead (e.g., BarChart, LineChart).
            This method will be removed in a future version.

        Parameters
        ----------
        chart_id : str
            ID of chart, table or map to add data to.
        data : pd.DataFrame | str
            A pandas dataframe containing the data to be added or a string that contains
            the data.

        Returns
        -------
        bool
            True if the data was added successfully.
        """
        warnings.warn(
            "add_data() is deprecated and will be removed in a future version. "
            "Use the object-oriented chart classes instead. "
            "Example: chart = BarChart(title='My Chart', data=df).create() or chart.data = df; chart.update()",
            DeprecationWarning,
            stacklevel=2,
        )

        # If data is a pandas dataframe, convert to csv
        if isinstance(data, pd.DataFrame):
            _data = data.to_csv(index=False, encoding="utf-8")
        # If data is a string, use that
        else:
            _data = data

        # Add data to chart
        return self.put(
            f"{self._CHARTS_URL}/{chart_id}/data",
            data=_data.encode("utf-8"),
            extra_headers={"content-type": "text/csv"},
            dump_data=False,
        )

    def add_json(self, chart_id: str, data: Any) -> bool:
        """Add JSON data to a specified chart.

        Can be used to add point, area and line markers to a locator map or other chart.

        Parameters
        ----------
        chart_id : str
            ID of chart, table or map to add data to.
        data : Any
            JSON data to add to the chart.

        Returns
        -------
        bool
            True if the data was added successfully.
        """
        # Set the chart metadata to accept JSON data
        self.update_chart(
            chart_id=chart_id,
            metadata={
                "data": {"json": True},
            },
        )

        # Dump the provided data as a JSON string
        json_data = json.dumps(data)

        # Post it to the chart via the add_data method
        return self.add_data(chart_id, json_data)

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
        response = self.post(f"{self._CHARTS_URL}/{chart_id}/data/refresh")
        assert isinstance(response, dict)
        return response

    #
    # Folder methods
    #

    def get_folders(self) -> dict:
        """Get a list of folders in your Datawrapper account.

        Returns
        -------
        dict
            A dictionary containing the folders in your Datawrapper account and their
            information.
        """
        return self.get(self._FOLDERS_URL)

    def get_folder(self, folder_id: int) -> dict:
        """Get an existing folder.

        Parameters
        ----------
        folder_id : int
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
        parent_id: int | None = None,
        team_id: int | None = None,
    ) -> dict:
        """Create a new folder.

        Parameters
        ----------
        name: str
            Name of the folder to be created.
        parent_id: int, optional
            The parent folder that the folder belongs to.
        team_id: int, optional
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

        response = self.post(
            self._FOLDERS_URL,
            data=_query,
            extra_headers={"content-type": "application/json"},
        )
        assert isinstance(response, dict)
        return response

    def update_folder(
        self,
        folder_id: str | int,
        name: str | None = None,
        parent_id: int | None = None,
        team_id: int | None = None,
        user_id: int | None = None,
    ) -> dict:
        """Update an existing folder.

        Parameters
        ----------
        folder_id : str | int
            ID of folder to update.
        name: str, optional
            Name to change the folder to.
        parent_id: int, optional
            The parent folder where this folder is stored.
        team_id: int, optional
            The team that the folder belongs to.
        user_id: int, optional
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

    def delete_folder(self, folder_id: int) -> bool:
        """Delete an existing folder.

        Parameters
        ----------
        folder_id : int
            ID of folder to delete.

        Returns
        -------
        bool
            True if the folder was deleted successfully.
        """
        return self.delete(f"{self._FOLDERS_URL}/{folder_id}")

    #
    # "Me" methods
    #

    def get_my_account(self) -> dict:
        """Access your account information.

        Returns
        -------
        dict
            A dictionary containing your account information.
        """
        return self.get(self._ME_URL)

    def account_info(self) -> dict:
        """A deprecated method for calling get_my_account."""
        # Issue a deprecation warning
        logger.warning(
            "This method is deprecated and will be removed in a future version. "
            "Use get_account_info instead."
        )

        # Use the newer method
        return self.get_my_account()

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
        limit: int = 100,
        offset: int = 0,
        min_last_edit_step: str | int = 0,
    ) -> dict:
        """Get a list of your recently edited charts.

        Parameters
        ----------
        limit: int
            Maximum items to fetch. Useful for pagination. 100 by default.
        offset: int
            Number of items to skip. Useful for pagination. Zero by default.
        min_last_edit_step: int
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
        limit: int = 100,
        offset: int = 0,
        min_last_edit_step: int = 0,
    ) -> dict:
        """Get a list of your recently published charts.

        Parameters
        ----------
        limit: int
            Maximum items to fetch. Useful for pagination. 100 by default.
        offset: int
            Number of items to skip. Useful for pagination. Zero by default.
        min_last_edit_step: int
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

    #
    # Oembed methods
    #

    def get_oembed(
        self,
        url: str,
        max_width: int | None = None,
        max_height: int | None = None,
        iframe: bool | None = None,
    ) -> dict:
        """Get an oEmbed object for a chart, table, or map.

        Parameters
        ----------
        url : str
            URL of chart, table, or map.
        max_width : int, optional
            Maximum width of the oEmbed object, by default None
        max_height : int, optional
            Maximum height of the oEmbed object, by default None
        iframe : bool, optional
            Whether to return an iframe embed code, by default None, which will return a responsive embed.

        Returns
        -------
        dict
            A dictionary containing the oEmbed object.
        """
        _query: dict = {"url": url, "format": "json"}
        if max_width:
            _query["maxwidth"] = max_width
        if max_height:
            _query["maxheight"] = max_height
        if iframe:
            _query["iframe"] = json.dumps(True)

        return self.get(self._OEMBED_URL, params=_query)

    #
    # River methods
    #

    def get_river(
        self,
        approved: bool | None = None,
        limit: int = 100,
        offset: int = 0,
        search: str | None = None,
    ) -> dict:
        """Search and filter a list of your River charts.

        Parameters
        ----------
        approved : bool, optional
            Filter by approved status, by default None
        limit : int
            Maximum items to fetch, by default 100
        offset : int
            Offset for pagination, by default 0
        search : str, optional
            Search for charts with a specific title, by default None

        Returns
        -------
        dict
            A dictionary containing the River charts.
        """
        _query: dict = {}
        if approved:
            _query["approved"] = json.dumps(approved)
        if limit:
            _query["limit"] = limit
        if offset:
            _query["offset"] = offset
        if search:
            _query["search"] = search

        return self.get(self._RIVER_URL, params=_query)

    def get_river_chart(self, chart_id: str) -> dict:
        """Get a River chart by ID.

        Parameters
        ----------
        chart_id : str
            ID of River chart to get.

        Returns
        -------
        dict
            A dictionary containing the River chart.
        """
        return self.get(self._RIVER_URL + f"/{chart_id}")

    def update_river_chart(
        self,
        chart_id: str,
        description: str,
        byline: str,
        tags: list[str],
        forkable: bool,
    ) -> bool:
        """Update a River chart's approved status.

        Parameters
        ----------
        chart_id : str
            ID of River chart to update.
        description : str
            Description of the River chart.
        byline : str
            Byline of the River chart.
        tags : list[str]
            Tags of the River chart.
        forkable : bool
            Whether the River chart is forkable.

        Returns
        -------
        bool
            True if the River chart was updated successfully.
        """
        _query: dict = {
            "description": description,
            "byline": byline,
            "tags": tags,
            "forkable": json.dumps(forkable),
        }

        return self.put(
            f"{self._RIVER_URL}/{chart_id}",
            data=_query,
            extra_headers={"content-type": "application/json"},
        )

    #
    # Theme methods
    #

    def get_themes(
        self, limit: int = 100, offset: int = 0, deleted: bool = False
    ) -> dict:
        """Get a list of themes in your Datawrapper account.

        Parameters
        ----------
        limit: int
            Maximum items to fetch. Useful for pagination. Default 100.
        offset: int
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

    #
    # Workspace methods
    #

    def get_workspaces(
        self,
        search: str | None = None,
        order: str = "ASC",
        order_by: str = "name",
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Get a list of workspaces in your Datawrapper account.

        Parameters
        ----------
        search : str, optional
            Search for a workspace name or slug including this term, by default None
        order : str, optional
            Result order (ascending or descending), by default "ASC." Supply "DESC" for descending order.
        order_by : str, optional
            Attribute to order by. One of "name", "slug", or "created_at". By default "name"
        limit : int, optional
            Maximum items to fetch, by default 100. Useful for pagination.
        offset : int, optional
            Number of items to skip, by default 0. Useful for pagination.

        Returns
        -------
        dict
            A dictionary containing the workspaces in your Datawrapper account.
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

        return self.get(self._WORKSPACES_URL, params=_query)

    def get_workspace(self, workspace_slug: str) -> dict:
        """Get an existing workspace by its slug.

        Parameters
        ----------
        workspace_slug : str
            Slug of workspace to get.

        Returns
        -------
        dict
            A dictionary containing the workspace's information.
        """
        return self.get(f"{self._WORKSPACES_URL}/{workspace_slug}")

    def create_workspace(
        self,
        name: str,
        slug: str | None = None,
    ) -> dict:
        """Create a new workspace.

        Parameters
        ----------
        name : str
            Name of the workspace to be created (2-100 characters).
        slug : str, optional
            Slug for the workspace (2-100 characters). If not provided,
            will be auto-generated from the name.

        Returns
        -------
        dict
            A dictionary containing the workspace's information.
        """
        _query: dict = {"name": name}
        if slug:
            _query["slug"] = slug

        response = self.post(
            self._WORKSPACES_URL,
            data=_query,
            extra_headers={"content-type": "application/json"},
        )
        assert isinstance(response, dict)
        return response

    def update_workspace(
        self,
        workspace_slug: str,
        name: str | None = None,
        slug: str | None = None,
        settings: dict | None = None,
        secrets: dict | None = None,
        color: str | None = None,
    ) -> dict:
        """Update an existing workspace.

        Parameters
        ----------
        workspace_slug : str
            Slug of workspace to update.
        name : str, optional
            New name for the workspace.
        slug : str, optional
            New slug for the workspace.
        settings : dict, optional
            Settings object for the workspace.
        secrets : dict, optional
            Secrets object for the workspace.
        color : str, optional
            Color for the workspace.

        Returns
        -------
        dict
            A dictionary with the workspace's updated metadata.

        Raises
        ------
        Exception
            If no parameters are supplied to update the workspace.
        """
        _query: dict = {}
        if name:
            _query["name"] = name
        if slug:
            _query["slug"] = slug
        if settings:
            _query["settings"] = settings
        if secrets:
            _query["secrets"] = secrets
        if color:
            _query["color"] = color

        if not _query:
            msg = "No parameters were supplied to update the workspace."
            logger.error(msg)
            raise Exception(msg)

        return self.patch(
            f"{self._WORKSPACES_URL}/{workspace_slug}",
            data=_query,
        )

    def delete_workspace(self, workspace_slug: str) -> bool:
        """Delete an existing workspace.

        Parameters
        ----------
        workspace_slug : str
            Slug of workspace to delete.

        Returns
        -------
        bool
            True if the workspace was deleted successfully.
        """
        return self.delete(f"{self._WORKSPACES_URL}/{workspace_slug}")

    def get_workspace_members(
        self,
        workspace_slug: str,
        search: str | None = None,
        order: str = "ASC",
        order_by: str = "name",
        limit: int = 100,
        offset: int = 0,
        role: str | None = None,
        include_invites: bool = False,
    ) -> dict:
        """Get a list of members in a workspace.

        Parameters
        ----------
        workspace_slug : str
            Slug of workspace to get members for.
        search : str, optional
            Search for a user email or name including this term.
        order : str, optional
            Result order (ascending or descending), by default "ASC."
        order_by : str, optional
            Attribute to order by. One of "name", "visCount", "lastSeen", or "role". By default "name"
        limit : int, optional
            Maximum items to fetch, by default 100. Useful for pagination.
        offset : int, optional
            Number of items to skip, by default 0. Useful for pagination.
        role : str, optional
            Filter by workspace role. One of "member", "manager", or "admin".
        include_invites : bool, optional
            Include pending invites, by default False.

        Returns
        -------
        dict
            A dictionary containing the members in the workspace.
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
        if role:
            _query["role"] = role
        if include_invites:
            _query["includeInvites"] = include_invites

        return self.get(
            f"{self._WORKSPACES_URL}/{workspace_slug}/members", params=_query
        )

    def update_workspace_members(
        self,
        workspace_slug: str,
        member_ids: list[int],
        role: str,
    ) -> dict:
        """Update workspace members' roles.

        Parameters
        ----------
        workspace_slug : str
            Slug of workspace to update members for.
        member_ids : list[int]
            Array of member user IDs to update.
        role : str
            New role to assign to the members. One of "member", "manager", or "admin".

        Returns
        -------
        bool
            True if the workspace members were updated successfully.
        """
        _query = {
            "memberIds": member_ids,
            "role": role,
        }

        return self.patch(
            f"{self._WORKSPACES_URL}/{workspace_slug}/members",
            data=_query,
        )

    def remove_workspace_members(
        self,
        workspace_slug: str,
        member_ids: list[int],
    ) -> bool:
        """Remove members from a workspace.

        Parameters
        ----------
        workspace_slug : str
            Slug of workspace to remove members from.
        member_ids : list[int]
            Array of member user IDs to remove.

        Returns
        -------
        bool
            True if the members were removed successfully.
        """
        return self.delete(
            f"{self._WORKSPACES_URL}/{workspace_slug}/members",
            data={"memberIds": member_ids},
            extra_headers={"content-type": "application/json"},
        )

    def get_workspace_teams(
        self,
        workspace_slug: str,
        search: str | None = None,
        order: str = "ASC",
        order_by: str = "name",
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Get a list of teams in a workspace.

        Parameters
        ----------
        workspace_slug : str
            Slug of workspace to get teams for.
        search : str, optional
            Search for a team name or id including this term.
        order : str, optional
            Result order (ascending or descending), by default "ASC."
        order_by : str, optional
            Attribute to order by. One of "name" or "createdAt". By default "name"
        limit : int, optional
            Maximum items to fetch, by default 100. Useful for pagination.
        offset : int, optional
            Number of items to skip, by default 0. Useful for pagination.

        Returns
        -------
        dict
            A dictionary containing the teams in the workspace.
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

        return self.get(f"{self._WORKSPACES_URL}/{workspace_slug}/teams", params=_query)

    def get_workspace_team(self, workspace_slug: str, team_id: str) -> dict:
        """Get a team within a workspace.

        Parameters
        ----------
        workspace_slug : str
            Slug of workspace the team belongs to.
        team_id : str
            ID of team to get.

        Returns
        -------
        dict
            A dictionary containing the team's information.
        """
        return self.get(f"{self._WORKSPACES_URL}/{workspace_slug}/teams/{team_id}")

    def create_workspace_team(
        self,
        workspace_slug: str,
        name: str,
        is_private: bool = False,
        icon: str | None = None,
    ) -> dict:
        """Create a new team in a workspace.

        Parameters
        ----------
        workspace_slug : str
            Slug of workspace to create team in.
        name : str
            Name of the team to be created.
        is_private : bool, optional
            Whether the team should be private, by default False.
        icon : str, optional
            Icon for the team (one of 183 available icons).

        Returns
        -------
        dict
            A dictionary containing the team's information.
        """
        _query: dict = {"name": name, "isPrivate": is_private}
        if icon:
            _query["icon"] = icon

        response = self.post(
            f"{self._WORKSPACES_URL}/{workspace_slug}/teams",
            data=_query,
            extra_headers={"content-type": "application/json"},
        )
        assert isinstance(response, dict)
        return response

    def update_workspace_team(
        self,
        workspace_slug: str,
        team_id: str,
        name: str | None = None,
        is_private: bool | None = None,
        settings: dict | None = None,
        secrets: dict | None = None,
        icon: str | None = None,
    ) -> dict:
        """Update a team within a workspace.

        Parameters
        ----------
        workspace_slug : str
            Slug of workspace the team belongs to.
        team_id : str
            ID of team to update.
        name : str, optional
            New name for the team.
        is_private : bool, optional
            Whether the team should be private.
        settings : dict, optional
            Settings object for the team.
        secrets : dict, optional
            Secrets object for the team.
        icon : str, optional
            Icon for the team.

        Returns
        -------
        dict
            A dictionary with the team's updated metadata.

        Raises
        ------
        Exception
            If no parameters are supplied to update the team.
        """
        _query: dict = {}
        if name:
            _query["name"] = name
        if is_private is not None:
            _query["isPrivate"] = is_private
        if settings:
            _query["settings"] = settings
        if secrets:
            _query["secrets"] = secrets
        if icon:
            _query["icon"] = icon

        if not _query:
            msg = "No parameters were supplied to update the team."
            logger.error(msg)
            raise Exception(msg)

        return self.patch(
            f"{self._WORKSPACES_URL}/{workspace_slug}/teams/{team_id}",
            data=_query,
        )

    def delete_workspace_team(
        self,
        workspace_slug: str,
        team_id: str,
        migration_team_id: str | None = None,
    ) -> bool:
        """Delete a team within a workspace.

        Parameters
        ----------
        workspace_slug : str
            Slug of workspace the team belongs to.
        team_id : str
            ID of team to delete.
        migration_team_id : str, optional
            Target team ID for migrating team content. If not provided,
            content will be migrated to the user's archive.

        Returns
        -------
        bool
            True if the team was deleted successfully.
        """
        _data = {}
        if migration_team_id:
            _data["migrationTeamId"] = migration_team_id

        return self.delete(
            f"{self._WORKSPACES_URL}/{workspace_slug}/teams/{team_id}",
            data=_data if _data else None,
            extra_headers={"content-type": "application/json"} if _data else None,
        )

    def get_workspace_team_members(
        self,
        workspace_slug: str,
        team_id: str,
        search: str | None = None,
        order: str = "ASC",
        order_by: str = "name",
        limit: int = 100,
        offset: int = 0,
        role: str | None = None,
        include_invites: bool = False,
    ) -> dict:
        """Get a list of members in a workspace team.

        Parameters
        ----------
        workspace_slug : str
            Slug of workspace the team belongs to.
        team_id : str
            ID of team to get members for.
        search : str, optional
            Search for a user email or name including this term.
        order : str, optional
            Result order (ascending or descending), by default "ASC."
        order_by : str, optional
            Attribute to order by. One of "name", "visCount", "lastSeen",
            "workspaceRole", or "role". By default "name"
        limit : int, optional
            Maximum items to fetch, by default 100. Useful for pagination.
        offset : int, optional
            Number of items to skip, by default 0. Useful for pagination.
        role : str, optional
            Filter by team role. One of "manager" or "member".
        include_invites : bool, optional
            Include pending invites for this team, by default False.

        Returns
        -------
        dict
            A dictionary containing the members in the workspace team.
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
        if role:
            _query["role"] = role
        if include_invites:
            _query["includeInvites"] = include_invites

        return self.get(
            f"{self._WORKSPACES_URL}/{workspace_slug}/teams/{team_id}/members",
            params=_query,
        )

    def add_workspace_team_members(
        self,
        workspace_slug: str,
        team_id: str,
        user_ids: list[int],
        role: str = "member",
    ) -> bool:
        """Add one or multiple users to a workspace team.

        Parameters
        ----------
        workspace_slug : str
            Slug of workspace the team belongs to.
        team_id : str
            ID of team to add users to.
        user_ids : list[int]
            Array of user IDs to add to the team.
        role : str, optional
            Role to assign to the users in the team. One of "manager" or "member".
            By default "member".

        Returns
        -------
        bool
            True if the users were added successfully.
        """
        _query = {
            "userIds": user_ids,
            "role": role,
        }

        response = self.post(
            f"{self._WORKSPACES_URL}/{workspace_slug}/teams/{team_id}/members",
            data=_query,
            extra_headers={"content-type": "application/json"},
        )
        assert isinstance(response, bool)
        return response

    def update_workspace_team_members(
        self,
        workspace_slug: str,
        team_id: str,
        member_ids: list[int],
        role: str = "member",
    ) -> dict:
        """Modify the role of users in a workspace team.

        Parameters
        ----------
        workspace_slug : str
            Slug of workspace the team belongs to.
        team_id : str
            ID of team to update members in.
        member_ids : list[int]
            IDs of the users to modify in the team.
        role : str, optional
            Role to assign to the users in the team. One of "manager" or "member".
            By default "member".

        Returns
        -------
        bool
            True if the members were updated successfully.
        """
        _query = {
            "memberIds": member_ids,
            "role": role,
        }

        return self.patch(
            f"{self._WORKSPACES_URL}/{workspace_slug}/teams/{team_id}/members",
            data=_query,
        )

    def remove_workspace_team_members(
        self,
        workspace_slug: str,
        team_id: str,
        member_ids: list[int],
    ) -> bool:
        """Remove multiple users from a workspace team.

        Parameters
        ----------
        workspace_slug : str
            Slug of workspace the team belongs to.
        team_id : str
            ID of team to remove users from.
        member_ids : list[int]
            IDs of the users to remove from the team.

        Returns
        -------
        bool
            True if the members were removed successfully.
        """
        return self.delete(
            f"{self._WORKSPACES_URL}/{workspace_slug}/teams/{team_id}/members",
            data={"memberIds": member_ids},
            extra_headers={"content-type": "application/json"},
        )

    #
    # User methods
    #

    def get_users(
        self,
        team_id: str | None = None,
        search: str | None = None,
        order: str = "ASC",
        order_by: str = "id",
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Get a list of users in your Datawrapper account.

        Parameters
        ----------
        team_id : str, optional
            ID of team to get users for, by default None
        search : str, optional
            Search for users with a specific name, by default None
        order : str, optional
            Result order (ascending or descending), by default "ASC." Supply "DESC" for descending order.
        order_by : str, optional
            Attribute to order by. By default "id"
        limit : int, optional
            Maximum items to fetch, by default 100. Useful for pagination.
        offset : int, optional
            Offset for pagination, by default 0.

        Returns
        -------
        dict
            A dictionary containing the users in your Datawrapper account.
        """
        _query: dict = {}
        if team_id:
            _query["teamId"] = team_id
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

        return self.get(self._USERS_URL, params=_query)

    def get_user(self, user_id: str) -> dict:
        """Get an existing user.

        Parameters
        ----------
        user_id : str
            ID of user to get.

        Returns
        -------
        dict
            A dictionary containing the user's information.
        """
        return self.get(f"{self._USERS_URL}/{user_id}")

    def update_user(
        self,
        user_id: str,
        name: str | None = None,
        email: str | None = None,
        role: str | None = None,
        language: str | None = None,
        activate_token: str | None = None,
        password: str | None = None,
        old_password: str | None = None,
    ):
        """Update an existing user.

        Parameters
        ----------
        user_id : str
            ID of user to update.
        name : str, optional
            Name to change the user to.
        email : str, optional
            Email to change the user to.
        role : str, optional
            Role to change the user to. One of owner, admin, or member.
        language : str, optional
            Language to change the user preference to.
        activate_token : str, optional
            Activate token, typically used to unset it when activating user.
        password : str, optional
            Password to change the user to.
        old_password : str, optional
            Old password to change the user to.

        Returns
        -------
        dict
            A dictionary with the user's updated metadata
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
        if activate_token:
            _query["activateToken"] = activate_token
        if password:
            _query["password"] = password
        if old_password:
            _query["oldPassword"] = old_password

        if not _query:
            msg = "No parameters were supplied to update the user."
            logger.error(msg)
            raise Exception(msg)

        if (password and not old_password) or (old_password and not password):
            msg = "You must supply the old password to change the password."
            logger.error(msg)
            raise Exception(msg)

        return self.patch(
            f"{self._USERS_URL}/{user_id}",
            data=_query,
        )

    def update_settings(
        self,
        user_id: int | str,
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
            f"{self._USERS_URL}/{user_id}/settings",
            data=_query,
        )

    def get_recently_edited_charts(
        self,
        user_id: int | str,
        limit: int = 100,
        offset: int = 0,
        min_last_edit_step: str | int = 0,
    ) -> dict:
        """Get a list of your recently edited charts.

        Parameters
        ----------
        user_id: int | str
            ID of user to get recently edited charts for.
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
            self._USERS_URL + f"/{user_id}/recently-edited-charts",
            params=_query,
        )

    def get_recently_published_charts(
        self,
        user_id: int | str,
        limit: int = 100,
        offset: int = 0,
        min_last_edit_step: str | int = 0,
    ) -> dict:
        """Get a list of your recently published charts.

        Parameters
        ----------
        user_id: int | str
            ID of user to get recently published charts for.
        limit: int
            Maximum items to fetch. Useful for pagination. 100 by default.
        offset: int
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
            self._USERS_URL + f"/{user_id}/recently-published-charts",
            params=_query,
        )
