"""Unit tests for the flags utility module."""

import pytest

from datawrapper import get_country_flag


class TestGetCountryFlag:
    """Tests for the get_country_flag function."""

    def test_common_countries(self):
        """Test flag codes for commonly used countries."""
        assert get_country_flag("United States of America") == ":us:"
        assert get_country_flag("United Kingdom") == ":gb:"
        assert get_country_flag("Germany") == ":de:"
        assert get_country_flag("France") == ":fr:"
        assert get_country_flag("Japan") == ":jp:"
        assert get_country_flag("China") == ":cn:"
        assert get_country_flag("India") == ":in:"
        assert get_country_flag("Brazil") == ":br:"
        assert get_country_flag("Canada") == ":ca:"
        assert get_country_flag("Australia") == ":au:"

    def test_special_characters(self):
        """Test countries with special characters in their names."""
        assert get_country_flag("Côte d'Ivoire") == ":ci:"
        assert get_country_flag("Curaçao") == ":cw:"
        assert get_country_flag("Réunion") == ":re:"
        assert get_country_flag("Türkiye") == ":tr:"
        assert get_country_flag("Saint Barthélemy") == ":bl:"

    def test_long_country_names(self):
        """Test countries with long official names."""
        assert get_country_flag("Bolivia (Plurinational State of)") == ":bo:"
        assert get_country_flag("Iran (Islamic Republic of)") == ":ir:"
        assert get_country_flag("Venezuela (Bolivarian Republic of)") == ":ve:"
        assert get_country_flag("Democratic Republic of the Congo") == ":cd:"
        assert get_country_flag("Saint Vincent and the Grenadines") == ":vc:"

    def test_aliases(self):
        """Test common aliases for countries."""
        assert get_country_flag("U.S.") == ":us:"
        assert get_country_flag("UK") == ":gb:"
        assert get_country_flag("Euro zone") == ":eu:"

    def test_uk_subdivisions(self):
        """Test UK constituent countries."""
        assert get_country_flag("UK - England") == ":gb-eng:"
        assert get_country_flag("UK - Scotland") == ":gb-sct:"
        assert get_country_flag("UK - Wales") == ":gb-wls:"
        assert get_country_flag("UK - Northern Ireland") == ":gb-nir:"

    def test_territories_and_regions(self):
        """Test territories, dependencies, and special regions."""
        assert get_country_flag("Puerto Rico") == ":pr:"
        assert get_country_flag("Hong Kong") == ":hk:"
        assert get_country_flag("Greenland") == ":gl:"
        assert get_country_flag("French Guiana") == ":gf:"
        assert get_country_flag("Guam") == ":gu:"
        assert get_country_flag("Kosovo") == ":xk:"
        assert get_country_flag("European Union") == ":eu:"

    def test_small_island_nations(self):
        """Test small island nations and territories."""
        assert get_country_flag("Nauru") == ":nr:"
        assert get_country_flag("Tuvalu") == ":tv:"
        assert get_country_flag("Palau") == ":pw:"
        assert get_country_flag("Marshall Islands") == ":mh:"
        assert get_country_flag("Kiribati") == ":ki:"

    def test_african_countries(self):
        """Test a sample of African countries."""
        assert get_country_flag("South Africa") == ":za:"
        assert get_country_flag("Nigeria") == ":ng:"
        assert get_country_flag("Egypt") == ":eg:"
        assert get_country_flag("Kenya") == ":ke:"
        assert get_country_flag("Morocco") == ":ma:"
        assert get_country_flag("Ethiopia") == ":et:"

    def test_asian_countries(self):
        """Test a sample of Asian countries."""
        assert get_country_flag("South Korea") == ":kr:"
        assert get_country_flag("North Korea") == ":kp:"
        assert get_country_flag("Thailand") == ":th:"
        assert get_country_flag("Vietnam") == ":vn:"
        assert get_country_flag("Indonesia") == ":id:"
        assert get_country_flag("Singapore") == ":sg:"

    def test_european_countries(self):
        """Test a sample of European countries."""
        assert get_country_flag("Spain") == ":es:"
        assert get_country_flag("Italy") == ":it:"
        assert get_country_flag("Poland") == ":pl:"
        assert get_country_flag("Sweden") == ":se:"
        assert get_country_flag("Norway") == ":no:"
        assert get_country_flag("Switzerland") == ":ch:"

    def test_americas_countries(self):
        """Test countries from North and South America."""
        assert get_country_flag("Mexico") == ":mx:"
        assert get_country_flag("Argentina") == ":ar:"
        assert get_country_flag("Chile") == ":cl:"
        assert get_country_flag("Colombia") == ":co:"
        assert get_country_flag("Peru") == ":pe:"

    def test_oceania_countries(self):
        """Test countries from Oceania."""
        assert get_country_flag("New Zealand") == ":nz:"
        assert get_country_flag("Fiji") == ":fj:"
        assert get_country_flag("Papua New Guinea") == ":pg:"
        assert get_country_flag("Samoa") == ":ws:"

    def test_middle_east_countries(self):
        """Test Middle Eastern countries."""
        assert get_country_flag("Saudi Arabia") == ":sa:"
        assert get_country_flag("United Arab Emirates") == ":ae:"
        assert get_country_flag("Israel") == ":il:"
        assert get_country_flag("Jordan") == ":jo:"
        assert get_country_flag("Lebanon") == ":lb:"

    def test_invalid_country_raises_keyerror(self):
        """Test that invalid country names raise KeyError."""
        with pytest.raises(KeyError):
            get_country_flag("Invalid Country Name")

        with pytest.raises(KeyError):
            get_country_flag("Atlantis")

        with pytest.raises(KeyError):
            get_country_flag("Narnia")

    def test_case_sensitivity(self):
        """Test that the function is case-sensitive."""
        # Correct case works
        assert get_country_flag("United States of America") == ":us:"

        # Wrong case should raise KeyError
        with pytest.raises(KeyError):
            get_country_flag("united states of america")

        with pytest.raises(KeyError):
            get_country_flag("UNITED STATES OF AMERICA")

        with pytest.raises(KeyError):
            get_country_flag("germany")

    def test_empty_string_raises_keyerror(self):
        """Test that empty string raises KeyError."""
        with pytest.raises(KeyError):
            get_country_flag("")

    def test_whitespace_variations(self):
        """Test that extra whitespace is not handled."""
        # Exact match works
        assert get_country_flag("Germany") == ":de:"

        # Extra whitespace should fail
        with pytest.raises(KeyError):
            get_country_flag(" Germany")

        with pytest.raises(KeyError):
            get_country_flag("Germany ")

        with pytest.raises(KeyError):
            get_country_flag("  Germany  ")


class TestImportAccessibility:
    """Tests for import accessibility of get_country_flag."""

    def test_can_import_from_main_package(self):
        """Test that get_country_flag can be imported from main datawrapper package."""
        from datawrapper import get_country_flag as main_import

        # Should work and return correct value
        assert main_import("Germany") == ":de:"
        assert main_import("United States of America") == ":us:"

    def test_can_import_from_flags_module(self):
        """Test that get_country_flag can be imported directly from flags module."""
        from datawrapper.flags import get_country_flag as flags_import

        # Should work and return correct value
        assert flags_import("France") == ":fr:"
        assert flags_import("Japan") == ":jp:"

    def test_both_imports_are_same_function(self):
        """Test that both import paths reference the same function."""
        from datawrapper import get_country_flag as main_import
        from datawrapper.flags import get_country_flag as flags_import

        # Should be the same function object
        assert main_import is flags_import

    def test_function_in_all_export(self):
        """Test that get_country_flag is in __all__ export list."""
        import datawrapper

        assert "get_country_flag" in datawrapper.__all__
        assert hasattr(datawrapper, "get_country_flag")


class TestComprehensiveCoverage:
    """Tests to ensure good coverage of the lookup table."""

    def test_all_continents_represented(self):
        """Test that we have countries from all continents."""
        # Africa
        assert get_country_flag("Ghana") == ":gh:"

        # Asia
        assert get_country_flag("Mongolia") == ":mn:"

        # Europe
        assert get_country_flag("Iceland") == ":is:"

        # North America
        assert get_country_flag("Costa Rica") == ":cr:"

        # South America
        assert get_country_flag("Uruguay") == ":uy:"

        # Oceania
        assert get_country_flag("Vanuatu") == ":vu:"

        # Antarctica (territories)
        assert get_country_flag("French Southern Territories") == ":tf:"

    def test_various_flag_code_formats(self):
        """Test that different flag code formats are returned correctly."""
        # Standard two-letter codes
        assert get_country_flag("Germany") == ":de:"
        assert get_country_flag("France") == ":fr:"

        # UK subdivisions with special format
        assert get_country_flag("UK - England") == ":gb-eng:"

        # Special regions
        assert get_country_flag("European Union") == ":eu:"
        assert get_country_flag("Kosovo") == ":xk:"

    def test_countries_with_similar_names(self):
        """Test countries that have similar names."""
        assert get_country_flag("Republic of the Congo") == ":cg:"
        assert get_country_flag("Democratic Republic of the Congo") == ":cd:"

        assert get_country_flag("South Korea") == ":kr:"
        assert get_country_flag("North Korea") == ":kp:"

        assert get_country_flag("Virgin Islands (British)") == ":vg:"
        assert get_country_flag("Virgin Islands (U.S.)") == ":vi:"
