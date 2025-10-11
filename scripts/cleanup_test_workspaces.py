#!/usr/bin/env python3
"""Cleanup script to remove orphaned test workspaces.

This script deletes all workspaces that start with "Test Workspace" which
may have been left behind by failed test runs.

Usage:
    python scripts/cleanup_test_workspaces.py
"""

import os
import sys

# Add parent directory to path to import datawrapper
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datawrapper import Datawrapper
from datawrapper.exceptions import RateLimitError


def cleanup_test_workspaces():
    """Delete all workspaces that start with 'Test Workspace'."""
    try:
        dw = Datawrapper()
        workspaces = dw.get_workspaces()

        deleted = 0
        skipped = 0
        errors = 0

        print("Scanning for test workspaces...")

        for workspace in workspaces["list"]:
            if workspace["name"].startswith("Test Workspace"):
                try:
                    dw.delete_workspace(workspace["slug"])
                    deleted += 1
                    print(f"✓ Deleted: {workspace['name']} ({workspace['slug']})")
                except RateLimitError as e:
                    print(f"✗ Rate limit hit: {e}")
                    print("  Stopping cleanup to avoid further rate limiting.")
                    break
                except Exception as e:
                    errors += 1
                    print(f"✗ Failed to delete {workspace['name']}: {e}")
            else:
                skipped += 1

        print(f"\n{'=' * 60}")
        print("Cleanup Summary:")
        print(f"  Deleted: {deleted}")
        print(f"  Skipped: {skipped}")
        print(f"  Errors: {errors}")
        print(f"{'=' * 60}")

        return deleted

    except Exception as e:
        print(f"Error during cleanup: {e}")
        return 0


if __name__ == "__main__":
    if not os.getenv("DATAWRAPPER_ACCESS_TOKEN"):
        print("Error: DATAWRAPPER_ACCESS_TOKEN environment variable not set")
        sys.exit(1)

    deleted_count = cleanup_test_workspaces()
    sys.exit(0 if deleted_count >= 0 else 1)
