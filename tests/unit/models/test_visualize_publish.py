"""Tests for Visualize and Publish models."""

import pytest
from pydantic import ValidationError

from datawrapper.charts.models import (
    Logo,
    Publish,
    PublishBlocks,
    Sharing,
    Visualize,
)


class TestSharing:
    """Tests for the Sharing model."""

    def test_sharing_defaults(self):
        """Test that Sharing model has correct default values."""
        sharing = Sharing()
        assert sharing.enabled is False
        assert sharing.url == ""
        assert sharing.auto is False

    def test_sharing_with_values(self):
        """Test Sharing model with custom values."""
        sharing = Sharing(
            enabled=True,
            url="https://example.com",
            auto=True,
        )
        assert sharing.enabled is True
        assert sharing.url == "https://example.com"
        assert sharing.auto is True

    def test_sharing_serialization(self):
        """Test that Sharing serializes correctly."""
        sharing = Sharing(
            enabled=True,
            url="https://example.com",
            auto=False,
        )
        data = sharing.model_dump()
        assert data == {
            "enabled": True,
            "url": "https://example.com",
            "auto": False,
        }

    def test_sharing_validation_error(self):
        """Test that Sharing raises validation error for invalid types."""
        with pytest.raises(ValidationError):
            Sharing(enabled="not a boolean")


class TestVisualize:
    """Tests for the Visualize model."""

    def test_visualize_defaults(self):
        """Test that Visualize model has correct default values."""
        visualize = Visualize()
        assert visualize.dark_mode_invert is True
        assert isinstance(visualize.sharing, Sharing)
        assert visualize.sharing.enabled is False

    def test_visualize_with_values(self):
        """Test Visualize model with custom values."""
        visualize = Visualize(
            dark_mode_invert=False,
            sharing=Sharing(enabled=True, url="https://example.com"),
        )
        assert visualize.dark_mode_invert is False
        assert visualize.sharing.enabled is True
        assert visualize.sharing.url == "https://example.com"

    def test_visualize_with_dict_sharing(self):
        """Test Visualize model accepts dict for sharing."""
        visualize = Visualize(
            dark_mode_invert=False,
            sharing={"enabled": True, "url": "https://example.com", "auto": True},
        )
        assert visualize.dark_mode_invert is False
        assert visualize.sharing.enabled is True
        assert visualize.sharing.url == "https://example.com"
        assert visualize.sharing.auto is True

    def test_visualize_serialization_with_alias(self):
        """Test that Visualize serializes correctly with aliases."""
        visualize = Visualize(
            dark_mode_invert=False,
            sharing=Sharing(enabled=True, url="https://example.com"),
        )
        data = visualize.model_dump(by_alias=True)
        assert data == {
            "dark-mode-invert": False,
            "sharing": {
                "enabled": True,
                "url": "https://example.com",
                "auto": False,
            },
        }

    def test_visualize_from_api_format(self):
        """Test creating Visualize from API response format."""
        api_data = {
            "dark-mode-invert": True,
            "sharing": {
                "enabled": False,
                "url": "",
                "auto": False,
            },
        }
        visualize = Visualize.model_validate(api_data)
        assert visualize.dark_mode_invert is True
        assert visualize.sharing.enabled is False


class TestLogo:
    """Tests for the Logo model."""

    def test_logo_defaults(self):
        """Test that Logo model has correct default values."""
        logo = Logo()
        assert logo.id == ""
        assert logo.enabled is False

    def test_logo_with_values(self):
        """Test Logo model with custom values."""
        logo = Logo(id="logo-123", enabled=True)
        assert logo.id == "logo-123"
        assert logo.enabled is True

    def test_logo_serialization(self):
        """Test that Logo serializes correctly."""
        logo = Logo(id="logo-123", enabled=True)
        data = logo.model_dump()
        assert data == {
            "id": "logo-123",
            "enabled": True,
        }


class TestPublishBlocks:
    """Tests for the PublishBlocks model."""

    def test_publish_blocks_defaults(self):
        """Test that PublishBlocks model has correct default values."""
        blocks = PublishBlocks()
        assert blocks.get_the_data is False
        assert blocks.download_image is False
        assert blocks.download_pdf is False
        assert blocks.download_svg is False
        assert blocks.embed is False
        assert isinstance(blocks.logo, Logo)
        assert blocks.logo.enabled is False

    def test_publish_blocks_with_values(self):
        """Test PublishBlocks model with custom values."""
        blocks = PublishBlocks(
            get_the_data=True,
            download_image=True,
            download_pdf=True,
            download_svg=True,
            embed=True,
            logo=Logo(id="logo-123", enabled=True),
        )
        assert blocks.get_the_data is True
        assert blocks.download_image is True
        assert blocks.download_pdf is True
        assert blocks.download_svg is True
        assert blocks.embed is True
        assert blocks.logo.id == "logo-123"
        assert blocks.logo.enabled is True

    def test_publish_blocks_with_dict_logo(self):
        """Test PublishBlocks model accepts dict for logo."""
        blocks = PublishBlocks(
            get_the_data=True,
            logo={"id": "logo-456", "enabled": True},
        )
        assert blocks.get_the_data is True
        assert blocks.logo.id == "logo-456"
        assert blocks.logo.enabled is True

    def test_publish_blocks_serialization_with_alias(self):
        """Test that PublishBlocks serializes correctly with aliases."""
        blocks = PublishBlocks(
            get_the_data=True,
            download_image=True,
            download_pdf=False,
            download_svg=False,
            embed=True,
            logo=Logo(id="logo-789", enabled=True),
        )
        data = blocks.model_dump(by_alias=True)
        assert data == {
            "get-the-data": True,
            "download-image": True,
            "download-pdf": False,
            "download-svg": False,
            "embed": True,
            "logo": {
                "id": "logo-789",
                "enabled": True,
            },
        }

    def test_publish_blocks_from_api_format(self):
        """Test creating PublishBlocks from API response format."""
        api_data = {
            "get-the-data": True,
            "download-image": False,
            "download-pdf": False,
            "download-svg": False,
            "embed": True,
            "logo": {
                "id": "logo-abc",
                "enabled": True,
            },
        }
        blocks = PublishBlocks.model_validate(api_data)
        assert blocks.get_the_data is True
        assert blocks.download_image is False
        assert blocks.embed is True
        assert blocks.logo.id == "logo-abc"
        assert blocks.logo.enabled is True


class TestPublish:
    """Tests for the Publish model."""

    def test_publish_defaults(self):
        """Test that Publish model has correct default values."""
        publish = Publish()
        assert publish.auto_dark_mode is False
        assert publish.force_attribution is False
        assert isinstance(publish.blocks, PublishBlocks)
        assert publish.blocks.get_the_data is False

    def test_publish_with_values(self):
        """Test Publish model with custom values."""
        publish = Publish(
            auto_dark_mode=True,
            force_attribution=True,
            blocks=PublishBlocks(
                get_the_data=True,
                download_image=True,
                logo=Logo(id="logo-xyz", enabled=True),
            ),
        )
        assert publish.auto_dark_mode is True
        assert publish.force_attribution is True
        assert publish.blocks.get_the_data is True
        assert publish.blocks.download_image is True
        assert publish.blocks.logo.id == "logo-xyz"

    def test_publish_with_dict_blocks(self):
        """Test Publish model accepts dict for blocks."""
        publish = Publish(
            auto_dark_mode=True,
            blocks={
                "get-the-data": True,
                "download-image": False,
                "download-pdf": True,
                "download-svg": False,
                "embed": True,
                "logo": {"id": "logo-def", "enabled": True},
            },
        )
        assert publish.auto_dark_mode is True
        assert publish.blocks.get_the_data is True
        assert publish.blocks.download_pdf is True
        assert publish.blocks.logo.id == "logo-def"

    def test_publish_serialization_with_alias(self):
        """Test that Publish serializes correctly with aliases."""
        publish = Publish(
            auto_dark_mode=True,
            force_attribution=False,
            blocks=PublishBlocks(
                get_the_data=True,
                embed=True,
                logo=Logo(id="logo-ghi", enabled=False),
            ),
        )
        data = publish.model_dump(by_alias=True)
        assert data == {
            "autoDarkMode": True,
            "force-attribution": False,
            "blocks": {
                "get-the-data": True,
                "download-image": False,
                "download-pdf": False,
                "download-svg": False,
                "embed": True,
                "logo": {
                    "id": "logo-ghi",
                    "enabled": False,
                },
            },
        }

    def test_publish_from_api_format(self):
        """Test creating Publish from API response format."""
        api_data = {
            "autoDarkMode": True,
            "force-attribution": True,
            "blocks": {
                "get-the-data": False,
                "download-image": True,
                "download-pdf": False,
                "download-svg": True,
                "embed": False,
                "logo": {
                    "id": "logo-jkl",
                    "enabled": True,
                },
            },
        }
        publish = Publish.model_validate(api_data)
        assert publish.auto_dark_mode is True
        assert publish.force_attribution is True
        assert publish.blocks.get_the_data is False
        assert publish.blocks.download_image is True
        assert publish.blocks.download_svg is True
        assert publish.blocks.logo.id == "logo-jkl"
        assert publish.blocks.logo.enabled is True


class TestIntegration:
    """Integration tests for Visualize and Publish models together."""

    def test_complete_metadata_structure(self):
        """Test creating a complete metadata structure with both models."""
        visualize = Visualize(
            dark_mode_invert=False,
            sharing=Sharing(enabled=True, url="https://example.com", auto=False),
        )
        publish = Publish(
            auto_dark_mode=True,
            force_attribution=False,
            blocks=PublishBlocks(
                get_the_data=True,
                download_image=True,
                download_pdf=False,
                download_svg=True,
                embed=True,
                logo=Logo(id="custom-logo", enabled=True),
            ),
        )

        # Serialize both
        visualize_data = visualize.model_dump(by_alias=True)
        publish_data = publish.model_dump(by_alias=True)

        # Verify structure matches Datawrapper API format
        assert "dark-mode-invert" in visualize_data
        assert "sharing" in visualize_data
        assert "autoDarkMode" in publish_data
        assert "force-attribution" in publish_data
        assert "blocks" in publish_data
        assert "logo" in publish_data["blocks"]

    def test_nested_validation_errors(self):
        """Test that validation errors propagate from nested models."""
        with pytest.raises(ValidationError):
            Publish(
                blocks={
                    "get-the-data": "not a boolean",  # Invalid type
                }
            )

        with pytest.raises(ValidationError):
            Visualize(
                sharing={
                    "enabled": "not a boolean",  # Invalid type
                }
            )
