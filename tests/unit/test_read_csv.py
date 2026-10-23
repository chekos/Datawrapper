"""Tests for read_csv, which parses chart data with any delimiter Datawrapper accepts."""

from unittest.mock import Mock, patch

import pandas as pd

from datawrapper import BaseChart, Datawrapper
from datawrapper.__main__ import read_csv


def test_comma():
    df = read_csv("Party,Seats\nA,24\nB,18\n")
    assert list(df.columns) == ["Party", "Seats"]
    assert df["Seats"].tolist() == [24, 18]


def test_semicolon_with_decimal_commas():
    """Spreadsheets in many locales export semicolon-separated CSV with decimal commas."""
    df = read_csv("Year;Rate\n2020;1,5\n2021;2,3\n")
    assert list(df.columns) == ["Year", "Rate"]
    assert df["Rate"].tolist() == ["1,5", "2,3"]


def test_semicolon_with_spaces_in_header():
    """Sniffing only the header line picked a wrong delimiter for this range plot data."""
    text = (
        "Event;Days before the vote;Vote day;Actor\n"
        "Brazil · 40 % tariff;-431;0;US government\n"
        "Brazil · Sanction;-354;0;US government\n"
    )
    df = read_csv(text)
    assert list(df.columns) == ["Event", "Days before the vote", "Vote day", "Actor"]
    assert df["Days before the vote"].tolist() == [-431, -354]


def test_tab():
    """The Datawrapper editor stores data pasted from a spreadsheet as TSV."""
    df = read_csv("City\t2022\t2026\nBogotá\t61.2\t58.4\nCali\t47.3\t52.1\n")
    assert list(df.columns) == ["City", "2022", "2026"]
    assert df["2026"].tolist() == [58.4, 52.1]


def test_quoted_commas_stay_in_their_cell():
    df = read_csv('Group,Victims\nTeens,"7,649"\n"Early; childhood","3,207"\n')
    assert list(df.columns) == ["Group", "Victims"]
    assert df["Victims"].tolist() == ["7,649", "3,207"]
    assert df["Group"].tolist() == ["Teens", "Early; childhood"]


def test_single_column_falls_back_to_comma():
    df = read_csv("Value\n3\n2\n")
    assert list(df.columns) == ["Value"]
    assert df["Value"].tolist() == [3, 2]


def test_blank_headers_get_datawrapper_names():
    """Settings such as axes refer to a column with a blank header as X.<position>."""
    df = read_csv("Item,,\nFunding,10,62%\nDebt,5,24%\n")
    assert list(df.columns) == ["Item", "X.1", "X.2"]


def test_deserialize_data_uses_the_sniffed_delimiter():
    df = BaseChart.deserialize_data("a;b\n1;2\n")
    assert list(df.columns) == ["a", "b"]


def test_client_get_parses_semicolon_csv_responses():
    with patch("datawrapper.__main__.r.get") as mock_get:
        mock_response = Mock()
        mock_response.ok = True
        mock_response.headers = {"content-type": "text/csv; charset=utf-8"}
        mock_response.text = "a;b\n1;2\n3;4\n"
        mock_get.return_value = mock_response

        dw = Datawrapper(access_token="test_token")
        df = dw.get("https://api.datawrapper.de/v3/charts/abc12/data")

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["a", "b"]
    assert df["b"].tolist() == [2, 4]
