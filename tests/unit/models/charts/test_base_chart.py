import pytest

import datawrapper
from tests.utils import _test_class


def test_annotate():
    _test_class(datawrapper.Annotate)


def test_column_format():
    _test_class(datawrapper.ColumnFormat)

    # Expect an error when no column is provided
    with pytest.raises(ValueError):
        datawrapper.ColumnFormat.model_validate({})

    # Expect an error when the column is empty
    with pytest.raises(ValueError):
        datawrapper.ColumnFormat.model_validate({"column": ""})

    # Expect an error when the column is None
    with pytest.raises(ValueError):
        datawrapper.ColumnFormat.model_validate({"column": None})

    # Expect an error when the column is not a string
    with pytest.raises(ValueError):
        datawrapper.ColumnFormat.model_validate({"column": 123})

    # Expect an error when the type is not one of the allowed values
    with pytest.raises(ValueError):
        datawrapper.ColumnFormat.model_validate({"column": "sales", "type": "invalid"})


def test_transform():
    _test_class(datawrapper.Transform)

    # Expect an error when upload_method isn't in the literal
    with pytest.raises(ValueError):
        datawrapper.Transform(upload_method="foobar").model_validate()

    # Expect an error if you passed a malformed column_format
    with pytest.raises(ValueError):
        datawrapper.Transform(column_format={"foo": "bar"}).model_validate()


def test_describe():
    _test_class(datawrapper.Describe)


def test_base_chart():
    _test_class(datawrapper.BaseChart)

    # Expect an error when base chart types are provided
    with pytest.raises(ValueError):
        datawrapper.BaseChart.model_validate({})

    with pytest.raises(ValueError):
        datawrapper.BaseChart.model_validate({"chart_type": ""})

    with pytest.raises(ValueError):
        datawrapper.BaseChart.model_validate({"chart_type": None})

    with pytest.raises(ValueError):
        datawrapper.BaseChart.model_validate({"chart_type": 123})

    with pytest.raises(ValueError):
        datawrapper.BaseChart.model_validate({"chart_type": "invalid_type"})
