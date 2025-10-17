"""Unit tests for Annotate model."""

import pytest
from pydantic import ValidationError

import datawrapper
from tests.utils import _test_class


class TestAnnotate:
    """Test Annotate model validation and serialization."""

    def test_annotate_basic_validation(self):
        """Test basic Annotate validation."""
        _test_class(datawrapper.Annotate)

    def test_annotate_defaults(self):
        """Test Annotate default values."""
        annotate = datawrapper.Annotate()

        # Check defaults
        assert annotate.notes == ""

    def test_annotate_with_valid_data(self):
        """Test Annotate with valid data."""
        annotate = datawrapper.Annotate(notes="This is a note about the chart")

        assert annotate.notes == "This is a note about the chart"

    def test_annotate_empty_string(self):
        """Test Annotate with empty string."""
        annotate = datawrapper.Annotate(notes="")

        assert annotate.notes == ""

    def test_annotate_serialization(self):
        """Test Annotate serialization."""
        annotate = datawrapper.Annotate(notes="Test note")

        # Test model_dump
        data = annotate.model_dump(by_alias=True)
        assert isinstance(data, dict)
        assert data["notes"] == "Test note"

        # Test JSON serialization
        json_str = annotate.model_dump_json(by_alias=True)
        assert isinstance(json_str, str)

        # Test round-trip
        reconstructed = datawrapper.Annotate.model_validate_json(json_str)
        assert reconstructed.notes == annotate.notes

    def test_annotate_string_validation(self):
        """Test Annotate string field validation."""
        # Valid string values should work
        annotate = datawrapper.Annotate(notes="Valid note")
        assert annotate.notes == "Valid note"

        # Empty string should work
        annotate = datawrapper.Annotate(notes="")
        assert annotate.notes == ""

    def test_annotate_non_string_validation(self):
        """Test Annotate with non-string values."""
        # Non-string values should fail
        with pytest.raises(ValidationError):
            datawrapper.Annotate(notes=123)

        with pytest.raises(ValidationError):
            datawrapper.Annotate(notes=["not", "a", "string"])

        with pytest.raises(ValidationError):
            datawrapper.Annotate(notes={"not": "a string"})

    def test_annotate_multiline_text(self):
        """Test Annotate with multiline text."""
        multiline_notes = """This is a multiline
        note that spans
        multiple lines with details."""

        annotate = datawrapper.Annotate(notes=multiline_notes)
        assert annotate.notes == multiline_notes

        # Test serialization preserves multiline text
        data = annotate.model_dump()
        assert data["notes"] == multiline_notes

    def test_annotate_special_characters(self):
        """Test Annotate with special characters."""
        annotate = datawrapper.Annotate(
            notes="Note with émojis 🎉, ñ characters, and quotes 'single' \"double\""
        )

        assert "émojis 🎉" in annotate.notes
        assert "ñ characters" in annotate.notes
        assert "quotes 'single' \"double\"" in annotate.notes

    def test_annotate_long_text(self):
        """Test Annotate with long text."""
        long_note = "This is a very long note. " * 100  # 2700+ characters

        annotate = datawrapper.Annotate(notes=long_note)
        assert annotate.notes == long_note
        assert len(annotate.notes) > 2000

    def test_annotate_html_content(self):
        """Test Annotate with HTML-like content."""
        html_note = """
        <p>This note contains <strong>HTML</strong> tags.</p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
        """

        annotate = datawrapper.Annotate(notes=html_note)
        assert annotate.notes == html_note
        assert "<strong>" in annotate.notes
        assert "<li>" in annotate.notes

    def test_annotate_markdown_content(self):
        """Test Annotate with Markdown-like content."""
        markdown_note = """
        # Header

        This note contains **bold** and *italic* text.

        - List item 1
        - List item 2

        [Link](https://example.com)
        """

        annotate = datawrapper.Annotate(notes=markdown_note)
        assert annotate.notes == markdown_note
        assert "**bold**" in annotate.notes
        assert "[Link]" in annotate.notes

    def test_annotate_whitespace_handling(self):
        """Test Annotate with various whitespace scenarios."""
        # Leading/trailing whitespace
        annotate = datawrapper.Annotate(notes="  Note with spaces  ")
        assert annotate.notes == "  Note with spaces  "

        # Tabs and newlines
        annotate = datawrapper.Annotate(notes="Note\twith\ttabs\nand\nnewlines")
        assert "\t" in annotate.notes
        assert "\n" in annotate.notes

        # Only whitespace
        annotate = datawrapper.Annotate(notes="   \t\n   ")
        assert annotate.notes == "   \t\n   "
