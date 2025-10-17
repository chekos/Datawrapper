# End-to-End API Tests

This directory contains end-to-end tests that create actual charts with the Datawrapper API.

## Setup

To run these tests, you need a Datawrapper API access token:

1. Get a Datawrapper API access token from https://app.datawrapper.de/account/api-tokens
2. Set the environment variable:
   ```bash
   export DATAWRAPPER_ACCESS_TOKEN="your_token_here"
   ```

## Running the Tests

Run all API tests:
```bash
pytest tests/functional/ -v -s -m api
```

Run a specific test:
```bash
pytest tests/functional/test_api_end_to_end.py::test_create_sample_bar_chart_with_datawrapper -v -s
```

## Test Description

### `test_create_sample_bar_chart_with_datawrapper`
Creates a comprehensive bar chart based on the European turnout sample data:
- Loads sample configuration from `tests/samples/bar/european-turnout.json`
- Creates a DataFrame with European election turnout data
- Creates and publishes the chart via Datawrapper API
- Prints the chart URL for manual inspection

### `test_create_simple_bar_chart_with_api`
Creates a simple bar chart to verify basic API integration:
- Uses minimal test data (5 categories with values)
- Tests the core create/publish workflow
- Verifies the API integration works with basic configuration

## Output

When tests run successfully, they will:
1. Print progress messages to the console
2. Create actual charts on Datawrapper
3. Publish the charts and print the public URLs
4. Verify the charts were created successfully

**Note:** These tests create real charts on Datawrapper, so they should be run sparingly to avoid cluttering your account.

## Known Issues

### SSL Certificate Verification (macOS)
On some macOS systems, you may encounter SSL certificate verification errors:
```
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate
```

**Workarounds:**
1. **Install certificates** (recommended):
   ```bash
   /Applications/Python\ 3.x/Install\ Certificates.command
   ```

2. **Use mocked tests instead**:
   ```bash
   pytest tests/functional/test_api_mock.py -v -s
   ```
   The mocked tests verify the same functionality without making real API calls.

3. **Update certificates via Homebrew** (if using Homebrew Python):
   ```bash
   brew install ca-certificates
   ```

## Skipping Tests

Tests are automatically skipped if no `DATAWRAPPER_ACCESS_TOKEN` environment variable is set. This prevents accidental API calls during regular test runs.

## Alternative: Mocked API Tests

If you encounter SSL issues or want to test without making real API calls, use the mocked tests:
```bash
pytest tests/functional/test_api_mock.py -v -s
```

These tests verify the same functionality using mocked HTTP responses, ensuring the code works correctly without requiring network access or API tokens.
