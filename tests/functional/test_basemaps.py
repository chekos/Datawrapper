"""Test basemaps related API enpoints with mocked API calls."""

from unittest.mock import patch

from datawrapper import Datawrapper


def test_get_basemaps():
    """Test the get_basemaps method with mocked API."""
    with patch.object(Datawrapper, "get") as mock_get:
        # Mock the get_basemaps response
        mock_basemaps = [
            {
                "id": "basemap1",
                "slug": "usa-iowa-counties",
                "title": "Iowa Counties",
            },
            {
                "id": "basemap2",
                "slug": "usa-california-counties",
                "title": "California Counties",
            },
        ]
        mock_get.return_value = mock_basemaps

        # Create client and call method
        dw = Datawrapper()
        basemaps_list = dw.get_basemaps()

        # Verify the call was made
        mock_get.assert_called_once()

        # Verify the result
        assert len(basemaps_list) > 0
        assert basemaps_list == mock_basemaps


def test_get_basemap():
    """Test the get_basemap method with mocked API."""
    with patch.object(Datawrapper, "get") as mock_get:
        # Mock basemap info with standard projection
        mock_basemap_standard = {
            "meta": {
                "slug": "usa-iowa-counties",
                "projection": {
                    "rotate": [93.49589653689938, -42.075128883839746],
                    "type": "geoAzimuthalEqualArea",
                },
            }
        }

        # Mock basemap info with wgs84 projection
        mock_basemap_wgs84 = {
            "meta": {
                "slug": "usa-iowa-counties",
                "projection": {"type": "geoAzimuthalEqualArea"},
            }
        }

        # Set up side_effect to return different values for each call
        mock_get.side_effect = [mock_basemap_standard, mock_basemap_wgs84]

        # Create client
        dw = Datawrapper()

        # Test the standard query
        basemap_info = dw.get_basemap("iowa-counties")
        assert isinstance(basemap_info, dict)
        assert basemap_info["meta"]["slug"] == "usa-iowa-counties"
        assert basemap_info["meta"]["projection"] == {
            "rotate": [93.49589653689938, -42.075128883839746],
            "type": "geoAzimuthalEqualArea",
        }

        # Test the projection kwarg
        basemap_info = dw.get_basemap("iowa-counties", wgs84=True)
        assert basemap_info["meta"]["projection"] == {"type": "geoAzimuthalEqualArea"}

        # Verify both calls were made
        assert mock_get.call_count == 2


def test_get_basemap_key():
    """Test the get_basemap_key method with mocked API."""
    with patch.object(Datawrapper, "get") as mock_get:
        # Mock the get_basemap_key response
        mock_key_info = {
            "label": "FIPS",
            "values": [f"19{i:03d}" for i in range(1, 100)],  # 99 FIPS codes
        }
        mock_get.return_value = mock_key_info

        # Create client and call method
        dw = Datawrapper()
        basemap_key = dw.get_basemap_key("iowa-counties", "GEOID")

        # Verify the call was made
        mock_get.assert_called_once()

        # Verify the result
        assert isinstance(basemap_key, dict)
        assert basemap_key["label"] == "FIPS"
        assert len(basemap_key["values"]) == 99
