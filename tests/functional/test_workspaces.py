"""Test the workspace functions."""

import random
import string

from datawrapper import Datawrapper


def test_get_workspaces():
    """Test the get_workspaces method."""
    # Connect
    dw = Datawrapper()

    # Get all workspaces
    workspaces = dw.get_workspaces()

    # Verify format of data
    assert isinstance(workspaces["list"], list)

    # If there are workspaces, test get_workspace with the first one
    if len(workspaces["list"]) > 0:
        workspace_slug = workspaces["list"][0]["slug"]
        workspace = dw.get_workspace(workspace_slug)
        assert isinstance(workspace, dict)
        assert workspace["slug"] == workspace_slug


def test_edit_workspaces():
    """Test creating, updating, and deleting workspaces."""
    # Connect
    dw = Datawrapper()

    # Generate random suffix for unique names
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))

    # Create a workspace
    workspace = dw.create_workspace(f"Test Workspace {suffix}")
    assert isinstance(workspace, dict)

    try:
        # Get the workspace
        workspace = dw.get_workspace(workspace["slug"])

        # Update the workspace
        workspace = dw.update_workspace(
            workspace["slug"], name=f"Test Workspace 2 {suffix}"
        )

        # Get the workspace again
        workspace = dw.get_workspace(workspace["slug"])

        # Verify that the name changed
        assert workspace["name"] == f"Test Workspace 2 {suffix}"

        # Delete the workspace
        delete = dw.delete_workspace(workspace["slug"])
        assert delete is True
    except Exception:
        # Ensure cleanup even if test fails
        try:
            dw.delete_workspace(workspace["slug"])
        except Exception:
            pass  # Ignore cleanup errors
        raise


def test_workspace_members():
    """Test workspace membership operations."""
    # Connect
    dw = Datawrapper()

    # Get all workspaces
    workspaces = dw.get_workspaces()

    # If there are workspaces, test membership operations
    if len(workspaces["list"]) > 0:
        workspace_slug = workspaces["list"][0]["slug"]

        # Get workspace members
        members = dw.get_workspace_members(workspace_slug)
        assert isinstance(members["list"], list)

        # Note: We won't test update/remove in automated tests
        # as they require actual members and could disrupt real workspaces


def test_workspace_teams():
    """Test workspace team operations."""
    # Connect
    dw = Datawrapper()

    # Get all workspaces
    workspaces = dw.get_workspaces()

    # If there are workspaces, test team operations
    if len(workspaces["list"]) > 0:
        workspace_slug = workspaces["list"][0]["slug"]

        # Get workspace teams
        teams = dw.get_workspace_teams(workspace_slug)
        assert isinstance(teams["list"], list)

        # If there are teams, test getting a single team
        if len(teams["list"]) > 0:
            team_id = teams["list"][0]["id"]
            team = dw.get_workspace_team(workspace_slug, team_id)
            assert isinstance(team, dict)
            assert team["id"] == team_id


def test_workspace_team_members():
    """Test workspace team member operations."""
    # Connect
    dw = Datawrapper()

    # Get all workspaces
    workspaces = dw.get_workspaces()

    # If there are workspaces, test team member operations
    if len(workspaces["list"]) > 0:
        workspace_slug = workspaces["list"][0]["slug"]

        # Get workspace teams
        teams = dw.get_workspace_teams(workspace_slug)

        # If there are teams, test member operations
        if len(teams["list"]) > 0:
            team_id = teams["list"][0]["id"]

            # Get team members
            members = dw.get_workspace_team_members(workspace_slug, team_id)
            assert isinstance(members["list"], list)

            # Note: We won't test add/update/remove in automated tests
            # as they require actual users and could disrupt real teams
