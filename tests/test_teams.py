"""Test the teams functions."""
import random
import string

import pytest

from datawrapper import Datawrapper


def test_get_teams():
    # Connect
    dw = Datawrapper()

    # Get all teams
    teams = dw.get_teams()

    # Verify format of data
    assert isinstance(teams['list'], list)


def test_edit_teams():
    # Connect
    dw = Datawrapper()

    # Get a randoms string suffix to use in our names
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))

    # Create a team
    team = dw.create_team(f"Test Team {suffix}")
    assert isinstance(team, dict)

    # Get the team
    team = dw.get_team(team["id"])

    # Update the team
    team = dw.update_team(team["id"], f"Test Team 2 {suffix}")

    # Get the team again
    team = dw.get_team(team["id"])

    # Verify that the name changed
    assert team["name"] == f"Test Team 2 {suffix}"

    # Delete the team
    dw.delete_team(team["id"])

    # Verify that if you try to get this team it will now raise an exception
    with pytest.raises(Exception):
        dw.get_team(team["id"])
