"""Custom exceptions for the datawrapper package."""


class FailedRequest(Exception):
    """Custom exception for failed API requests."""

    def __init__(self, response):
        """Initialize the exception."""
        msg = f"Request failed with status code {response.status_code}. Response content: {response.content}"
        super().__init__(msg)


class InvalidRequest(Exception):
    """Custom exception for invalid API requests."""

    def __init__(self, message):
        """Initialize the exception."""
        super().__init__(message)
