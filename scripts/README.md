# Datawrapper Scripts

This directory contains utility scripts for managing the Datawrapper project.

## cleanup_test_workspaces.py

A cleanup script to remove orphaned test workspaces that may have been left behind by failed test runs.

### Purpose

During test execution, if a test fails before completing its cleanup, test workspaces (those starting with "Test Workspace") can accumulate in your Datawrapper account. This can eventually lead to hitting workspace limits and causing rate limit errors (429 status code).

### Usage

```bash
# Make sure you have DATAWRAPPER_ACCESS_TOKEN set
export DATAWRAPPER_ACCESS_TOKEN="your-token-here"

# Run the cleanup script
python scripts/cleanup_test_workspaces.py
```

### What It Does

1. Connects to the Datawrapper API using your access token
2. Lists all workspaces in your account
3. Identifies workspaces that start with "Test Workspace"
4. Deletes each test workspace
5. Stops if it hits a rate limit to avoid further issues
6. Provides a summary of deleted, skipped, and failed workspaces

### When to Use

- **Before running tests**: Clean up any orphaned workspaces from previous test runs
- **After test failures**: Remove workspaces left behind by failed tests
- **When hitting rate limits**: If you see "Too many workspaces" errors in CI/CD

### Automatic Cleanup

The test suite also includes automatic cleanup:

- **Session-level cleanup**: `tests/conftest.py` includes a pytest fixture that runs before and after the entire test session
- **Test-level cleanup**: Individual tests use try-finally blocks to ensure cleanup even on failure

### Example Output

```
Scanning for test workspaces...
✓ Deleted: Test Workspace abc12 (test-workspace-abc12)
✓ Deleted: Test Workspace xyz89 (test-workspace-xyz89)
✗ Failed to delete Test Workspace old99: Workspace not found

============================================================
Cleanup Summary:
  Deleted: 2
  Skipped: 15
  Errors: 1
============================================================
```

### Error Handling

The script handles several error scenarios:

- **Rate limits**: Stops cleanup immediately to avoid further rate limiting
- **Missing workspaces**: Continues with other workspaces
- **API errors**: Reports errors but continues cleanup
- **Missing token**: Exits with error message

### Integration with CI/CD

You can add this script to your CI/CD pipeline:

```yaml
# GitHub Actions example
- name: Cleanup test workspaces
  run: python scripts/cleanup_test_workspaces.py
  env:
    DATAWRAPPER_ACCESS_TOKEN: ${{ secrets.DATAWRAPPER_ACCESS_TOKEN }}
  continue-on-error: true  # Don't fail the build if cleanup fails
