"""Integration tests for ColumnFormatList with number_divisor field."""

from datawrapper.charts import ColumnFormat, ColumnFormatList, NumberDivisor


class TestColumnFormatListNumberDivisor:
    """Test ColumnFormatList serialization with number_divisor."""

    def test_serialize_with_enum_value(self):
        """Test serializing ColumnFormatList with enum number_divisor."""
        formats = ColumnFormatList(
            formats=[
                ColumnFormat(
                    column="sales",
                    type="number",
                    number_divisor=NumberDivisor.DIVIDE_BY_MILLION,
                    number_prepend="$",
                )
            ]
        )

        serialized = formats.serialize_to_dict()
        assert "sales" in serialized
        assert serialized["sales"]["type"] == "number"
        assert serialized["sales"]["number-divisor"] == "6"  # Enum value
        assert serialized["sales"]["number-prepend"] == "$"

    def test_serialize_with_raw_int_value(self):
        """Test serializing ColumnFormatList with raw int number_divisor."""
        formats = ColumnFormatList(
            formats=[
                ColumnFormat(
                    column="revenue",
                    type="number",
                    number_divisor=6,
                )
            ]
        )

        serialized = formats.serialize_to_dict()
        assert "revenue" in serialized
        assert serialized["revenue"]["number-divisor"] == 6

    def test_serialize_with_auto_value(self):
        """Test serializing ColumnFormatList with 'auto' number_divisor."""
        formats = ColumnFormatList(
            formats=[
                ColumnFormat(
                    column="population",
                    type="number",
                    number_divisor="auto",
                )
            ]
        )

        serialized = formats.serialize_to_dict()
        assert "population" in serialized
        assert serialized["population"]["number-divisor"] == "auto"

    def test_serialize_with_negative_value(self):
        """Test serializing ColumnFormatList with negative number_divisor."""
        formats = ColumnFormatList(
            formats=[
                ColumnFormat(
                    column="percentage",
                    type="number",
                    number_divisor=NumberDivisor.MULTIPLY_BY_HUNDRED,
                )
            ]
        )

        serialized = formats.serialize_to_dict()
        assert "percentage" in serialized
        assert serialized["percentage"]["number-divisor"] == "-2"

    def test_serialize_default_value_excluded(self):
        """Test that default number_divisor (0) is excluded from serialization."""
        formats = ColumnFormatList(
            formats=[
                ColumnFormat(
                    column="count",
                    type="number",
                    number_divisor=0,  # Default value
                )
            ]
        )

        serialized = formats.serialize_to_dict()
        assert "count" in serialized
        assert "number-divisor" not in serialized["count"]

    def test_serialize_string_zero_excluded(self):
        """Test that string '0' is also excluded from serialization."""
        formats = ColumnFormatList(
            formats=[
                ColumnFormat(
                    column="count",
                    type="number",
                    number_divisor="0",  # String zero
                )
            ]
        )

        serialized = formats.serialize_to_dict()
        assert "count" in serialized
        assert "number-divisor" not in serialized["count"]

    def test_serialize_multiple_columns_with_divisors(self):
        """Test serializing multiple columns with different divisors."""
        formats = ColumnFormatList(
            formats=[
                ColumnFormat(
                    column="sales",
                    number_divisor=NumberDivisor.DIVIDE_BY_MILLION,
                    number_prepend="$",
                ),
                ColumnFormat(
                    column="units",
                    number_divisor=NumberDivisor.DIVIDE_BY_THOUSAND,
                ),
                ColumnFormat(
                    column="percentage",
                    number_divisor=NumberDivisor.MULTIPLY_BY_HUNDRED,
                    number_append="%",
                ),
            ]
        )

        serialized = formats.serialize_to_dict()
        assert serialized["sales"]["number-divisor"] == "6"
        assert serialized["sales"]["number-prepend"] == "$"
        assert serialized["units"]["number-divisor"] == "3"
        assert serialized["percentage"]["number-divisor"] == "-2"
        assert serialized["percentage"]["number-append"] == "%"

    def test_deserialize_from_api_format(self):
        """Test deserializing ColumnFormatList from API format with number_divisor."""
        api_data = {
            "sales": {
                "type": "number",
                "number-divisor": 6,
                "number-prepend": "$",
            },
            "units": {
                "type": "number",
                "number-divisor": "auto",
            },
        }

        formats = ColumnFormatList.model_validate(api_data)
        assert len(formats.formats) == 2

        # Find the sales format
        sales_format = next(f for f in formats.formats if f.column == "sales")
        assert sales_format.number_divisor == 6
        assert sales_format.number_prepend == "$"

        # Find the units format
        units_format = next(f for f in formats.formats if f.column == "units")
        assert units_format.number_divisor == "auto"

    def test_round_trip_serialization(self):
        """Test that serialization and deserialization are symmetric."""
        original = ColumnFormatList(
            formats=[
                ColumnFormat(
                    column="revenue",
                    type="number",
                    number_divisor=NumberDivisor.DIVIDE_BY_BILLION,
                    number_prepend="$",
                    number_append="B",
                )
            ]
        )

        # Serialize to API format
        serialized = original.serialize_to_dict()

        # Deserialize back
        deserialized = ColumnFormatList.model_validate(serialized)

        # Check values match
        assert len(deserialized.formats) == 1
        revenue_format = deserialized.formats[0]
        assert revenue_format.column == "revenue"
        assert revenue_format.type == "number"
        assert revenue_format.number_divisor == "9"  # String from API
        assert revenue_format.number_prepend == "$"
        assert revenue_format.number_append == "B"
