"""Test map creation and manipulation."""

import json
from unittest.mock import mock_open, patch

from datawrapper import Datawrapper


def test_locator_map_points():
    """Test locator maps with points."""
    with (
        patch.object(Datawrapper, "post") as mock_post,
        patch.object(Datawrapper, "patch") as mock_patch,
        patch.object(Datawrapper, "put") as mock_put,
    ):
        # Setup mock response for create_chart
        mock_post.return_value = {
            "id": "test123",
            "title": "My locator map with points",
            "type": "locator-map",
            "metadata": {},
        }

        # Setup mock response for update_chart
        mock_patch.return_value = {
            "id": "test123",
            "title": "My locator map with points",
            "type": "locator-map",
            "metadata": {
                "data": {"json": True},
                "visualize": {"view": {"center": [-0.106, 51.523], "zoom": 8}},
            },
        }

        # Setup mock response for add_json (which calls put)
        mock_put.return_value = {"status": "ok"}

        # Create client
        dw = Datawrapper()

        # Create a map
        obj = dw.create_chart(
            "My locator map with points",
            "locator-map",
        )

        # Set map metadata
        metadata = {
            "data": {"json": True},
            "visualize": {
                "view": {
                    "center": [-0.106, 51.523],
                    "zoom": 8,
                    "fit": {
                        "top": [0.176, 53.408],
                        "right": [1.368, 51.779],
                        "bottom": [0.241, 51.1425],
                        "left": [-0.920, 51.754],
                    },
                    "height": 120,
                    "pitch": 0,
                    "bearing": 0,
                },
                "style": "dw-light",
                "defaultMapSize": 500,
                "visibility": {
                    "boundary_country": True,
                    "boundary_state": True,
                    "building": True,
                    "green": True,
                    "mountains": True,
                    "roads": True,
                    "urban": True,
                    "water": True,
                    "building3d": True,
                },
                "mapLabel": True,
                "scale": False,
                "compass": False,
                "miniMap": {"enabled": False, "bounds": []},
                "key": {"enabled": False, "title": "", "items": []},
            },
        }
        dw.update_chart(obj["id"], metadata=metadata)

        # Add markers
        data = {
            "markers": [
                {
                    "type": "point",
                    "title": "Buckingham Palace",
                    "icon": {
                        "path": "M1000 350a500 500 0 0 0-500-500 500 500 0 0 0-500 500 500 500 0 0 0 500 500 500 500 0 0 0 500-500z",
                        "height": 700,
                        "width": 1000,
                    },
                    "scale": 1,
                    "markerColor": "#cc0000",
                    "anchor": "bottom-right",
                    "offsetY": 0,
                    "offsetX": 0,
                    "text": {"color": "#333333", "fontSize": 15, "halo": "#f2f3f0"},
                    "rotate": 0,
                    "visible": True,
                    "visibility": {"mobile": True, "desktop": True},
                    "coordinates": [-0.140634, 51.501476],
                    "tooltip": {
                        "text": "Some information about Buckingham Palace that shows up when hovering over the marker"
                    },
                }
            ]
        }

        # Post it
        dw.add_json(obj["id"], data)

        # Verify mocks were called
        mock_post.assert_called_once()  # create_chart
        assert (
            mock_patch.call_count == 2
        )  # update_chart and add_json (which also calls patch)
        mock_put.assert_called_once()  # add_json


def test_locator_map_areas():
    """Test locator maps with areas."""
    with (
        patch.object(Datawrapper, "post") as mock_post,
        patch.object(Datawrapper, "patch") as mock_patch,
        patch.object(Datawrapper, "put") as mock_put,
        patch("builtins.open", mock_open(read_data='{"markers": []}')),
    ):
        # Setup mock response for create_chart
        mock_post.return_value = {
            "id": "test456",
            "title": "My locator map with areas",
            "type": "locator-map",
            "metadata": {},
        }

        # Setup mock response for update_chart (called by add_json)
        mock_patch.return_value = {
            "id": "test456",
            "title": "My locator map with areas",
            "type": "locator-map",
            "metadata": {"data": {"json": True}},
        }

        # Setup mock response for add_json (which calls put)
        mock_put.return_value = {"status": "ok"}

        # Create client
        dw = Datawrapper()

        # Create a map
        obj = dw.create_chart(
            "My locator map with areas",
            "locator-map",
        )

        # Open markers
        with open("./tests/area_markers.json") as f:
            data = json.load(f)

        # Add markers
        dw.add_json(obj["id"], data)

        # Verify mocks were called
        mock_post.assert_called_once()  # create_chart
        mock_patch.assert_called_once()  # add_json calls update_chart
        mock_put.assert_called_once()  # add_json


def test_locator_map_lines():
    """Test locator maps with lines."""
    with (
        patch.object(Datawrapper, "post") as mock_post,
        patch.object(Datawrapper, "patch") as mock_patch,
        patch.object(Datawrapper, "put") as mock_put,
    ):
        # Setup mock response for create_chart
        mock_post.return_value = {
            "id": "test789",
            "title": "My locator map with lines",
            "type": "locator-map",
            "metadata": {},
        }

        # Setup mock response for update_chart (called by add_json)
        mock_patch.return_value = {
            "id": "test789",
            "title": "My locator map with lines",
            "type": "locator-map",
            "metadata": {"data": {"json": True}},
        }

        # Setup mock response for add_json (which calls put)
        mock_put.return_value = {"status": "ok"}

        # Create client
        dw = Datawrapper()

        # Create a map
        obj = dw.create_chart(
            "My locator map with lines",
            "locator-map",
        )

        # Add markers
        data = {
            "markers": [
                {
                    "id": "m1",
                    "title": "Line Marker",
                    "type": "line",
                    "visible": True,
                    "properties": {
                        "stroke": "#fa8c00",
                        "stroke-width": 3,
                        "stroke-opacity": 1,
                        "stroke-dasharray": "100000",
                    },
                    "visibility": {"mobile": True, "desktop": True},
                    "feature": {
                        "type": "Feature",
                        "properties": [],
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [
                                [-74.006, 40.7128],
                                [-80.2994982, 25.7823907],
                            ],
                        },
                    },
                }
            ]
        }
        dw.add_json(obj["id"], data)

        # Verify mocks were called
        mock_post.assert_called_once()  # create_chart
        mock_patch.assert_called_once()  # add_json calls update_chart
        mock_put.assert_called_once()  # add_json
