"""Test the teams functions."""
import random
import string

from datawrapper import Datawrapper


def test_get_teams():
    """Test the get_teams method."""
    # Connect
    dw = Datawrapper()

    # Get all teams
    teams = dw.get_teams()

    # Verify format of data
    assert isinstance(teams["list"], list)

    # Get members of the first team
    members = dw.get_team_members(teams["list"][0]["id"])
    assert isinstance(members["list"], list)

    # Update team member
    update = dw.update_team_member(
        teams["list"][0]["id"],
        members["list"][0]["id"],
        "admin",
    )
    assert isinstance(update, bool) and update is True


def test_edit_teams():
    """Test the edit_teams method."""
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

    # Invite a user to the team
    invite = dw.send_invite(
        team["id"],
        "foo@example.com",
        "member",
    )
    assert invite is True

    # Delete the team
    delete = dw.delete_team(team["id"])
    assert delete is True
