"""Custom exceptions for the datawrapper package."""


class FailedRequestError(Exception):
    """Custom exception for failed API requests."""

    def __init__(self, response):
        """Initialize the exception."""
        msg = f"Request failed with status code {response.status_code}. Response content: {response.content}"
        super().__init__(msg)


class InvalidRequestError(Exception):
    """Custom exception for invalid API requests."""

    def __init__(self, message):
        """Initialize the exception."""
        super().__init__(message)


class RateLimitError(FailedRequestError):
    """Custom exception for API rate limit errors (429 status code)."""

    def __init__(self, response, resource_type=None):
        """Initialize the rate limit exception.

        Args:
            response: The HTTP response object
            resource_type: Optional string describing what resource hit the limit
                          (e.g., 'workspaces', 'charts', 'API calls')
        """
        self.status_code = response.status_code
        self.response = response
        self.resource_type = resource_type

        # Try to parse the error message from response
        try:
            import json

            error_data = json.loads(response.content)
            self.error_message = error_data.get("message", "Rate limit exceeded")
        except (json.JSONDecodeError, AttributeError):
            self.error_message = "Rate limit exceeded"

        # Build helpful error message
        if resource_type:
            msg = f"Rate limit exceeded for {resource_type}. {self.error_message}"
        else:
            msg = f"Rate limit exceeded. {self.error_message}"

        # Call Exception.__init__ directly to avoid FailedRequestError's formatting
        Exception.__init__(self, msg)
