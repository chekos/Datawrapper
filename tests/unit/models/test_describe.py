"""Unit tests for Describe model."""

import pytest
from pydantic import ValidationError

import datawrapper
from tests.utils import _test_class


class TestDescribe:
    """Test Describe model validation and serialization."""

    def test_describe_basic_validation(self):
        """Test basic Describe validation."""
        _test_class(datawrapper.Describe)

    def test_describe_defaults(self):
        """Test Describe default values."""
        describe = datawrapper.Describe()

        # Check defaults
        assert describe.source_name == ""
        assert describe.source_url == ""
        assert describe.number_format == "-"
        assert describe.byline == ""
        assert describe.intro == ""

    def test_describe_with_valid_data(self):
        """Test Describe with valid data."""
        describe = datawrapper.Describe(
            **{"source-name": "Example Source"},  # Use alias
            **{"source-url": "https://example.com"},  # Use alias
            **{"number-format": "0,0"},  # Use alias
            byline="John Doe",
            intro="This is an introduction",
        )

        assert describe.source_name == "Example Source"
        assert describe.source_url == "https://example.com"
        assert describe.number_format == "0,0"
        assert describe.byline == "John Doe"
        assert describe.intro == "This is an introduction"

    def test_describe_empty_strings(self):
        """Test Describe with empty strings."""
        describe = datawrapper.Describe(
            **{"source-name": ""},
            **{"source-url": ""},
            **{"number-format": ""},
            byline="",
            intro="",
        )

        assert describe.source_name == ""
        assert describe.source_url == ""
        assert describe.number_format == ""
        assert describe.byline == ""
        assert describe.intro == ""

    def test_describe_serialization(self):
        """Test Describe serialization."""
        describe = datawrapper.Describe(
            **{"source-name": "Test Source"},
            **{"source-url": "https://test.com"},
            byline="Test Author",
        )

        # Test model_dump
        data = describe.model_dump(by_alias=True)
        assert isinstance(data, dict)

        # Test JSON serialization
        json_str = describe.model_dump_json(by_alias=True)
        assert isinstance(json_str, str)

        # Test round-trip
        reconstructed = datawrapper.Describe.model_validate_json(json_str)
        assert reconstructed.source_name == describe.source_name
        assert reconstructed.source_url == describe.source_url
        assert reconstructed.byline == describe.byline

    def test_describe_field_aliases(self):
        """Test Describe field aliases work correctly."""
        describe = datawrapper.Describe(
            **{"source-name": "Test Source"},
            **{"source-url": "https://test.com"},
            **{"number-format": "0,0.0"},
        )

        # Serialize with aliases
        data = describe.model_dump(by_alias=True)

        # Should contain API field names (aliases)
        assert "source-name" in data
        assert "source-url" in data
        assert "number-format" in data
        assert "byline" in data
        assert "intro" in data

    def test_describe_string_validation(self):
        """Test Describe string field validation."""
        # Valid string values should work
        describe = datawrapper.Describe(
            **{"source-name": "Valid Source"},
            **{"source-url": "https://valid.com"},
            byline="Valid Author",
            intro="Valid intro",
        )

        assert describe.source_name == "Valid Source"
        assert describe.source_url == "https://valid.com"
        assert describe.byline == "Valid Author"
        assert describe.intro == "Valid intro"

    def test_describe_non_string_validation(self):
        """Test Describe with non-string values."""
        # Non-string values should fail
        with pytest.raises(ValidationError):
            datawrapper.Describe(**{"source-name": 123})

        with pytest.raises(ValidationError):
            datawrapper.Describe(**{"source-url": 456})

        with pytest.raises(ValidationError):
            datawrapper.Describe(byline=789)

        with pytest.raises(ValidationError):
            datawrapper.Describe(intro=["not", "a", "string"])

    def test_describe_number_format_patterns(self):
        """Test Describe with various number format patterns."""
        valid_formats = [
            "-",  # default
            "0,0",  # thousands separator
            "0,0.0",  # one decimal
            "0,0.00",  # two decimals
            "0.0%",  # percentage
            "$0,0",  # currency
            "0a",  # abbreviated
            "",  # empty
        ]

        for fmt in valid_formats:
            describe = datawrapper.Describe(**{"number-format": fmt})
            assert describe.number_format == fmt

    def test_describe_url_formats(self):
        """Test Describe with various URL formats."""
        valid_urls = [
            "",  # empty (default)
            "https://example.com",
            "http://example.com",
            "https://example.com/path/to/data",
            "https://example.com/data.csv?param=value",
            "ftp://example.com/file.txt",
            "relative/path/to/file",
            "mailto:test@example.com",
        ]

        for url in valid_urls:
            describe = datawrapper.Describe(**{"source-url": url})
            assert describe.source_url == url

    def test_describe_multiline_text(self):
        """Test Describe with multiline text."""
        multiline_intro = """This is a multiline
        introduction that spans
        multiple lines."""

        describe = datawrapper.Describe(intro=multiline_intro)
        assert describe.intro == multiline_intro

        # Test serialization preserves multiline text
        data = describe.model_dump()
        assert data["intro"] == multiline_intro

    def test_describe_special_characters(self):
        """Test Describe with special characters."""
        describe = datawrapper.Describe(
            **{"source-name": "Source with émojis 🎉 and ñ"},
            byline="Author with 中文 characters",
            intro="Intro with quotes 'single' and \"double\"",
        )

        assert "émojis 🎉 and ñ" in describe.source_name
        assert "中文" in describe.byline
        assert "quotes 'single' and \"double\"" in describe.intro
