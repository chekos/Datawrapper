"""Color scale options for choropleth maps."""

from enum import Enum


class ColorScale(str, Enum):
    """Color scale type for choropleth map value mapping."""

    #: Linear scale
    LINEAR = "linear"

    #: Logarithmic scale
    LOG = "log"

    #: Square root scale
    SQRT = "sqrt"

    #: Quantile scale (equal count in each bucket)
    QUANTILE = "quantile"

    #: Jenks natural breaks optimization
    JENKS = "jenks"
