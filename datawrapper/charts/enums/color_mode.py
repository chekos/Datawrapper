"""Color mode options for choropleth maps."""

from enum import Enum


class ColorMode(str, Enum):
    """Color mode for choropleth map coloring."""

    #: Continuous gradient coloring
    GRADIENT = "gradient"

    #: Discrete buckets/intervals coloring
    BUCKETS = "buckets"
