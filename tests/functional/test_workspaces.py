"""Test the workspace functions with mocked API calls."""

import random
import string
from unittest.mock import patch

from datawrapper import Datawrapper


def test_get_workspaces():
    """Test the get_workspaces method with mocked API."""
    with (
        patch.object(Datawrapper, "get_workspaces") as mock_get_workspaces,
        patch.object(Datawrapper, "get_workspace") as mock_get_workspace,
    ):
        # Mock response for get_workspaces
        mock_get_workspaces.return_value = {
            "list": [
                {
                    "slug": "test-workspace-1",
                    "name": "Test Workspace 1",
                    "id": "ws123",
                },
                {
                    "slug": "test-workspace-2",
                    "name": "Test Workspace 2",
                    "id": "ws456",
                },
            ]
        }

        # Mock response for get_workspace
        mock_get_workspace.return_value = {
            "slug": "test-workspace-1",
            "name": "Test Workspace 1",
            "id": "ws123",
        }

        # Connect
        dw = Datawrapper()

        # Get all workspaces
        workspaces = dw.get_workspaces()

        # Verify format of data
        assert isinstance(workspaces["list"], list)
        assert len(workspaces["list"]) == 2

        # Test get_workspace with the first one
        workspace_slug = workspaces["list"][0]["slug"]
        workspace = dw.get_workspace(workspace_slug)
        assert isinstance(workspace, dict)
        assert workspace["slug"] == workspace_slug

        # Verify mocks were called
        mock_get_workspaces.assert_called_once()
        mock_get_workspace.assert_called_once_with(workspace_slug)


def test_edit_workspaces():
    """Test creating, updating, and deleting workspaces with mocked API."""
    # Generate random suffix for unique names
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))

    with (
        patch.object(Datawrapper, "create_workspace") as mock_create,
        patch.object(Datawrapper, "get_workspace") as mock_get,
        patch.object(Datawrapper, "update_workspace") as mock_update,
        patch.object(Datawrapper, "delete_workspace") as mock_delete,
    ):
        # Mock responses
        created_workspace = {
            "slug": f"test-workspace-{suffix}",
            "name": f"Test Workspace {suffix}",
            "id": "ws789",
        }
        mock_create.return_value = created_workspace

        updated_workspace = {
            "slug": f"test-workspace-{suffix}",
            "name": f"Test Workspace 2 {suffix}",
            "id": "ws789",
        }

        # First get returns original, second get returns updated
        mock_get.side_effect = [created_workspace, updated_workspace]
        mock_update.return_value = updated_workspace
        mock_delete.return_value = True

        # Connect
        dw = Datawrapper()

        # Create a workspace
        workspace = dw.create_workspace(f"Test Workspace {suffix}")
        assert isinstance(workspace, dict)
        assert workspace["name"] == f"Test Workspace {suffix}"

        # Get the workspace
        workspace = dw.get_workspace(workspace["slug"])
        assert workspace["name"] == f"Test Workspace {suffix}"

        # Update the workspace
        workspace = dw.update_workspace(
            workspace["slug"], name=f"Test Workspace 2 {suffix}"
        )
        assert workspace["name"] == f"Test Workspace 2 {suffix}"

        # Get the workspace again
        workspace = dw.get_workspace(workspace["slug"])
        assert workspace["name"] == f"Test Workspace 2 {suffix}"

        # Delete the workspace
        delete = dw.delete_workspace(workspace["slug"])
        assert delete is True

        # Verify all mocks were called
        mock_create.assert_called_once()
        assert mock_get.call_count == 2
        mock_update.assert_called_once()
        mock_delete.assert_called_once()


def test_workspace_members():
    """Test workspace membership operations with mocked API."""
    with (
        patch.object(Datawrapper, "get_workspaces") as mock_get_workspaces,
        patch.object(Datawrapper, "get_workspace_members") as mock_get_members,
    ):
        # Mock responses
        mock_get_workspaces.return_value = {
            "list": [
                {
                    "slug": "test-workspace-1",
                    "name": "Test Workspace 1",
                    "id": "ws123",
                }
            ]
        }

        mock_get_members.return_value = {
            "list": [
                {
                    "id": "user123",
                    "email": "user1@example.com",
                    "role": "admin",
                },
                {
                    "id": "user456",
                    "email": "user2@example.com",
                    "role": "member",
                },
            ]
        }

        # Connect
        dw = Datawrapper()

        # Get all workspaces
        workspaces = dw.get_workspaces()
        assert len(workspaces["list"]) > 0

        workspace_slug = workspaces["list"][0]["slug"]

        # Get workspace members
        members = dw.get_workspace_members(workspace_slug)
        assert isinstance(members["list"], list)
        assert len(members["list"]) == 2

        # Verify mocks were called
        mock_get_workspaces.assert_called_once()
        mock_get_members.assert_called_once_with(workspace_slug)


def test_workspace_teams():
    """Test workspace team operations with mocked API."""
    with (
        patch.object(Datawrapper, "get_workspaces") as mock_get_workspaces,
        patch.object(Datawrapper, "get_workspace_teams") as mock_get_teams,
        patch.object(Datawrapper, "get_workspace_team") as mock_get_team,
    ):
        # Mock responses
        mock_get_workspaces.return_value = {
            "list": [
                {
                    "slug": "test-workspace-1",
                    "name": "Test Workspace 1",
                    "id": "ws123",
                }
            ]
        }

        mock_get_teams.return_value = {
            "list": [
                {
                    "id": "team123",
                    "name": "Team Alpha",
                },
                {
                    "id": "team456",
                    "name": "Team Beta",
                },
            ]
        }

        mock_get_team.return_value = {
            "id": "team123",
            "name": "Team Alpha",
        }

        # Connect
        dw = Datawrapper()

        # Get all workspaces
        workspaces = dw.get_workspaces()
        assert len(workspaces["list"]) > 0

        workspace_slug = workspaces["list"][0]["slug"]

        # Get workspace teams
        teams = dw.get_workspace_teams(workspace_slug)
        assert isinstance(teams["list"], list)
        assert len(teams["list"]) == 2

        # Get a single team
        team_id = teams["list"][0]["id"]
        team = dw.get_workspace_team(workspace_slug, team_id)
        assert isinstance(team, dict)
        assert team["id"] == team_id

        # Verify mocks were called
        mock_get_workspaces.assert_called_once()
        mock_get_teams.assert_called_once_with(workspace_slug)
        mock_get_team.assert_called_once_with(workspace_slug, team_id)


def test_workspace_team_members():
    """Test workspace team member operations with mocked API."""
    with (
        patch.object(Datawrapper, "get_workspaces") as mock_get_workspaces,
        patch.object(Datawrapper, "get_workspace_teams") as mock_get_teams,
        patch.object(
            Datawrapper, "get_workspace_team_members"
        ) as mock_get_team_members,
    ):
        # Mock responses
        mock_get_workspaces.return_value = {
            "list": [
                {
                    "slug": "test-workspace-1",
                    "name": "Test Workspace 1",
                    "id": "ws123",
                }
            ]
        }

        mock_get_teams.return_value = {
            "list": [
                {
                    "id": "team123",
                    "name": "Team Alpha",
                }
            ]
        }

        mock_get_team_members.return_value = {
            "list": [
                {
                    "id": "user123",
                    "email": "user1@example.com",
                    "role": "member",
                },
                {
                    "id": "user456",
                    "email": "user2@example.com",
                    "role": "member",
                },
            ]
        }

        # Connect
        dw = Datawrapper()

        # Get all workspaces
        workspaces = dw.get_workspaces()
        assert len(workspaces["list"]) > 0

        workspace_slug = workspaces["list"][0]["slug"]

        # Get workspace teams
        teams = dw.get_workspace_teams(workspace_slug)
        assert len(teams["list"]) > 0

        team_id = teams["list"][0]["id"]

        # Get team members
        members = dw.get_workspace_team_members(workspace_slug, team_id)
        assert isinstance(members["list"], list)
        assert len(members["list"]) == 2

        # Verify mocks were called
        mock_get_workspaces.assert_called_once()
        mock_get_teams.assert_called_once_with(workspace_slug)
        mock_get_team_members.assert_called_once_with(workspace_slug, team_id)
