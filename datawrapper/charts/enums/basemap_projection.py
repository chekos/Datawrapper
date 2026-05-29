"""Basemap projection options for choropleth maps."""

from enum import Enum


class BasemapProjection(str, Enum):
    """Map projection types for custom basemaps in Datawrapper."""

    #: Azimuthal Equal Area projection
    AZIMUTHAL_EQUAL_AREA = "geoAzimuthalEqualArea"

    #: Natural Equal Area projection
    NATURAL_EQUAL_AREA = "geoNaturalEqualArea"

    #: Conic Equidistant projection
    CONIC_EQUIDISTANT = "geoConicEquidistant"

    #: Conic Conformal projection
    CONIC_CONFORMAL = "geoConicConformal"

    #: Albers USA projection (specific for US maps)
    ALBERS_USA = "geoAlbersUsa"
