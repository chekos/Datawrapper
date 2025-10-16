"""Comprehensive tests for exception handling without requiring live API access."""

from unittest.mock import Mock, patch

import pytest

from datawrapper import Datawrapper
from datawrapper.exceptions import (
    FailedRequestError,
    InvalidRequestError,
    RateLimitError,
)


class TestFailedRequestError:
    """Tests for FailedRequestError exception."""

    def test_failed_request_error_message(self):
        """Test that FailedRequestError formats message correctly."""
        # Create a mock response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.content = b"Not Found"

        # Create the exception
        error = FailedRequestError(mock_response)

        # Verify the message
        expected_msg = (
            "Request failed with status code 404. Response content: b'Not Found'"
        )
        assert str(error) == expected_msg

    def test_failed_request_error_with_json_content(self):
        """Test FailedRequestError with JSON error response."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.content = b'{"error": "Invalid request"}'

        error = FailedRequestError(mock_response)

        assert "400" in str(error)
        assert "Invalid request" in str(error)


class TestInvalidRequestError:
    """Tests for InvalidRequestError exception."""

    def test_invalid_request_error_message(self):
        """Test that InvalidRequestError stores custom message."""
        message = "No updates submitted."
        error = InvalidRequestError(message)

        assert str(error) == message

    def test_invalid_request_error_custom_message(self):
        """Test InvalidRequestError with different custom messages."""
        messages = [
            "Missing required parameter",
            "Invalid chart type",
            "No data provided",
        ]

        for msg in messages:
            error = InvalidRequestError(msg)
            assert str(error) == msg


class TestRateLimitError:
    """Tests for RateLimitError exception."""

    def test_rate_limit_error_basic(self):
        """Test basic RateLimitError without resource type."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.content = b'{"message": "Too many requests"}'

        error = RateLimitError(mock_response)

        assert error.status_code == 429
        assert error.response == mock_response
        assert error.resource_type is None
        assert "Rate limit exceeded" in str(error)
        assert "Too many requests" in str(error)

    def test_rate_limit_error_with_resource_type(self):
        """Test RateLimitError with resource type specified."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.content = b'{"message": "Workspace limit reached"}'

        error = RateLimitError(mock_response, resource_type="workspaces")

        assert error.resource_type == "workspaces"
        assert "Rate limit exceeded for workspaces" in str(error)
        assert "Workspace limit reached" in str(error)

    def test_rate_limit_error_invalid_json(self):
        """Test RateLimitError with invalid JSON response."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.content = b"Not JSON content"

        error = RateLimitError(mock_response)

        assert "Rate limit exceeded" in str(error)
        assert error.error_message == "Rate limit exceeded"

    def test_rate_limit_error_no_message_in_json(self):
        """Test RateLimitError when JSON doesn't contain message field."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.content = b'{"error": "rate_limit"}'

        error = RateLimitError(mock_response)

        assert error.error_message == "Rate limit exceeded"

    def test_rate_limit_error_inherits_from_failed_request(self):
        """Test that RateLimitError is a subclass of FailedRequestError."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.content = b"{}"

        error = RateLimitError(mock_response)

        assert isinstance(error, FailedRequestError)
        assert isinstance(error, Exception)


class TestExceptionRaisingInGetMethod:
    """Tests for exception raising in GET requests."""

    def test_get_raises_failed_request_on_404(self):
        """Test that GET request raises FailedRequestError on 404."""
        with patch("datawrapper.__main__.r.get") as mock_get:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 404
            mock_response.content = b"Not Found"
            mock_get.return_value = mock_response

            dw = Datawrapper(access_token="test_token")

            with pytest.raises(FailedRequestError) as exc_info:
                dw.get("https://api.datawrapper.de/v3/charts/invalid")

            assert "404" in str(exc_info.value)

    def test_get_raises_rate_limit_on_429(self):
        """Test that GET request raises RateLimitError on 429."""
        with patch("datawrapper.__main__.r.get") as mock_get:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 429
            mock_response.content = b'{"message": "Rate limit exceeded"}'
            mock_get.return_value = mock_response

            dw = Datawrapper(access_token="test_token")

            with pytest.raises(RateLimitError) as exc_info:
                dw.get("https://api.datawrapper.de/v3/charts")

            assert exc_info.value.status_code == 429

    def test_get_raises_failed_request_on_500(self):
        """Test that GET request raises FailedRequestError on 500."""
        with patch("datawrapper.__main__.r.get") as mock_get:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 500
            mock_response.content = b"Internal Server Error"
            mock_get.return_value = mock_response

            dw = Datawrapper(access_token="test_token")

            with pytest.raises(FailedRequestError) as exc_info:
                dw.get("https://api.datawrapper.de/v3/charts")

            assert "500" in str(exc_info.value)


class TestExceptionRaisingInPostMethod:
    """Tests for exception raising in POST requests."""

    def test_post_raises_failed_request_on_400(self):
        """Test that POST request raises FailedRequestError on 400."""
        with patch("datawrapper.__main__.r.post") as mock_post:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 400
            mock_response.content = b"Bad Request"
            mock_post.return_value = mock_response

            dw = Datawrapper(access_token="test_token")

            with pytest.raises(FailedRequestError) as exc_info:
                dw.post("https://api.datawrapper.de/v3/charts", data={})

            assert "400" in str(exc_info.value)

    def test_post_raises_rate_limit_on_429(self):
        """Test that POST request raises RateLimitError on 429."""
        with patch("datawrapper.__main__.r.post") as mock_post:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 429
            mock_response.content = b'{"message": "Too many charts created"}'
            mock_post.return_value = mock_response

            dw = Datawrapper(access_token="test_token")

            with pytest.raises(RateLimitError) as exc_info:
                dw.post("https://api.datawrapper.de/v3/charts", data={})

            assert "Too many charts created" in str(exc_info.value)

    def test_post_raises_failed_request_on_403(self):
        """Test that POST request raises FailedRequestError on 403."""
        with patch("datawrapper.__main__.r.post") as mock_post:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 403
            mock_response.content = b"Forbidden"
            mock_post.return_value = mock_response

            dw = Datawrapper(access_token="test_token")

            with pytest.raises(FailedRequestError) as exc_info:
                dw.post("https://api.datawrapper.de/v3/charts", data={})

            assert "403" in str(exc_info.value)


class TestExceptionRaisingInPatchMethod:
    """Tests for exception raising in PATCH requests."""

    def test_patch_raises_failed_request_on_404(self):
        """Test that PATCH request raises FailedRequestError on 404."""
        with patch("datawrapper.__main__.r.patch") as mock_patch:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 404
            mock_response.content = b"Chart not found"
            mock_patch.return_value = mock_response

            dw = Datawrapper(access_token="test_token")

            with pytest.raises(FailedRequestError) as exc_info:
                dw.patch("https://api.datawrapper.de/v3/charts/abc123", data={})

            assert "404" in str(exc_info.value)

    def test_patch_raises_rate_limit_on_429(self):
        """Test that PATCH request raises RateLimitError on 429."""
        with patch("datawrapper.__main__.r.patch") as mock_patch:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 429
            mock_response.content = b'{"message": "Update rate limit exceeded"}'
            mock_patch.return_value = mock_response

            dw = Datawrapper(access_token="test_token")

            with pytest.raises(RateLimitError) as exc_info:
                dw.patch("https://api.datawrapper.de/v3/charts/abc123", data={})

            assert "Update rate limit exceeded" in str(exc_info.value)


class TestExceptionRaisingInPutMethod:
    """Tests for exception raising in PUT requests."""

    def test_put_raises_failed_request_on_400(self):
        """Test that PUT request raises FailedRequestError on 400."""
        with patch("datawrapper.__main__.r.put") as mock_put:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 400
            mock_response.content = b"Invalid data"
            mock_put.return_value = mock_response

            dw = Datawrapper(access_token="test_token")

            with pytest.raises(FailedRequestError) as exc_info:
                dw.put("https://api.datawrapper.de/v3/charts/abc123/data", data={})

            assert "400" in str(exc_info.value)

    def test_put_raises_rate_limit_on_429(self):
        """Test that PUT request raises RateLimitError on 429."""
        with patch("datawrapper.__main__.r.put") as mock_put:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 429
            mock_response.content = b'{"message": "Data upload rate limit"}'
            mock_put.return_value = mock_response

            dw = Datawrapper(access_token="test_token")

            with pytest.raises(RateLimitError) as exc_info:
                dw.put("https://api.datawrapper.de/v3/charts/abc123/data", data={})

            assert "Data upload rate limit" in str(exc_info.value)


class TestExceptionRaisingInDeleteMethod:
    """Tests for exception raising in DELETE requests."""

    def test_delete_raises_failed_request_on_404(self):
        """Test that DELETE request raises FailedRequestError on 404."""
        with patch("datawrapper.__main__.r.delete") as mock_delete:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 404
            mock_response.content = b"Resource not found"
            mock_delete.return_value = mock_response

            dw = Datawrapper(access_token="test_token")

            with pytest.raises(FailedRequestError) as exc_info:
                dw.delete("https://api.datawrapper.de/v3/charts/abc123")

            assert "404" in str(exc_info.value)

    def test_delete_raises_rate_limit_on_429(self):
        """Test that DELETE request raises RateLimitError on 429."""
        with patch("datawrapper.__main__.r.delete") as mock_delete:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 429
            mock_response.content = b'{"message": "Delete rate limit exceeded"}'
            mock_delete.return_value = mock_response

            dw = Datawrapper(access_token="test_token")

            with pytest.raises(RateLimitError) as exc_info:
                dw.delete("https://api.datawrapper.de/v3/charts/abc123")

            assert "Delete rate limit exceeded" in str(exc_info.value)


class TestInvalidRequestErrorInHighLevelMethods:
    """Tests for InvalidRequestError in high-level API methods."""

    def test_update_chart_raises_invalid_request_with_no_params(self):
        """Test that update_chart raises InvalidRequestError when no params provided."""
        dw = Datawrapper(access_token="test_token")

        with pytest.raises(InvalidRequestError) as exc_info:
            dw.update_chart("abc123")

        assert "No updates submitted" in str(exc_info.value)

    def test_update_description_with_only_hide_title_false_makes_api_call(self):
        """Test that update_description with only hide_title=False still makes API call."""
        # Note: update_description always includes hide_title in the query,
        # so it will always make an API call even with no other params.
        # This is different from update_chart which validates for empty params.
        with patch.object(Datawrapper, "patch") as mock_patch:
            mock_patch.return_value = {"id": "abc123", "title": "Test"}

            dw = Datawrapper(access_token="test_token")
            result = dw.update_description("abc123")

            # Verify the API call was made
            mock_patch.assert_called_once()
            assert result["id"] == "abc123"

    def test_update_my_settings_raises_exception_with_no_params(self):
        """Test that update_my_settings raises Exception when no params provided."""
        dw = Datawrapper(access_token="test_token")

        with pytest.raises(Exception) as exc_info:
            dw.update_my_settings()

        assert "No updates submitted" in str(exc_info.value)

    def test_update_workspace_raises_exception_with_no_params(self):
        """Test that update_workspace raises Exception when no params provided."""
        dw = Datawrapper(access_token="test_token")

        with pytest.raises(Exception) as exc_info:
            dw.update_workspace("test-workspace")

        assert "No parameters were supplied" in str(exc_info.value)

    def test_update_workspace_team_raises_exception_with_no_params(self):
        """Test that update_workspace_team raises Exception when no params provided."""
        dw = Datawrapper(access_token="test_token")

        with pytest.raises(Exception) as exc_info:
            dw.update_workspace_team("test-workspace", "team123")

        assert "No parameters were supplied" in str(exc_info.value)

    def test_update_user_raises_exception_with_no_params(self):
        """Test that update_user raises Exception when no params provided."""
        dw = Datawrapper(access_token="test_token")

        with pytest.raises(Exception) as exc_info:
            dw.update_user("user123")

        assert "No parameters were supplied" in str(exc_info.value)

    def test_update_settings_raises_exception_with_no_params(self):
        """Test that update_settings raises Exception when no params provided."""
        dw = Datawrapper(access_token="test_token")

        with pytest.raises(Exception) as exc_info:
            dw.update_settings("user123")

        assert "No updates submitted" in str(exc_info.value)


class TestPasswordValidationExceptions:
    """Tests for password validation exceptions."""

    def test_update_my_account_raises_exception_with_password_but_no_old_password(self):
        """Test that update_my_account raises Exception when password provided without old password."""
        dw = Datawrapper(access_token="test_token")

        with pytest.raises(Exception) as exc_info:
            dw.update_my_account(password="newpass123")

        assert "old password" in str(exc_info.value).lower()

    def test_update_my_account_raises_exception_with_old_password_but_no_password(self):
        """Test that update_my_account raises Exception when old password provided without new password."""
        dw = Datawrapper(access_token="test_token")

        with pytest.raises(Exception) as exc_info:
            dw.update_my_account(old_password="oldpass123")

        assert "new password" in str(exc_info.value).lower()

    def test_update_user_raises_exception_with_password_but_no_old_password(self):
        """Test that update_user raises Exception when password provided without old password."""
        dw = Datawrapper(access_token="test_token")

        with pytest.raises(Exception) as exc_info:
            dw.update_user("user123", password="newpass123")

        assert "old password" in str(exc_info.value).lower()

    def test_update_user_raises_exception_with_old_password_but_no_password(self):
        """Test that update_user raises Exception when old password provided without new password."""
        dw = Datawrapper(access_token="test_token")

        with pytest.raises(Exception) as exc_info:
            dw.update_user("user123", old_password="oldpass123")

        assert "old password" in str(exc_info.value).lower()


class TestExceptionAttributeAccess:
    """Tests for accessing exception attributes."""

    def test_rate_limit_error_attributes_accessible(self):
        """Test that RateLimitError attributes can be accessed."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.content = b'{"message": "Custom rate limit message"}'

        error = RateLimitError(mock_response, resource_type="charts")

        # Test all attributes are accessible
        assert error.status_code == 429
        assert error.response == mock_response
        assert error.resource_type == "charts"
        assert error.error_message == "Custom rate limit message"

    def test_failed_request_error_with_various_status_codes(self):
        """Test FailedRequestError with various HTTP status codes."""
        status_codes = [400, 401, 403, 404, 500, 502, 503]

        for code in status_codes:
            mock_response = Mock()
            mock_response.status_code = code
            mock_response.content = f"Error {code}".encode()

            error = FailedRequestError(mock_response)

            assert str(code) in str(error)
            assert f"Error {code}" in str(error)


class TestExceptionInRealWorldScenarios:
    """Tests for exceptions in realistic usage scenarios."""

    def test_get_chart_with_invalid_id_raises_failed_request(self):
        """Test that getting a chart with invalid ID raises FailedRequestError."""
        with patch("datawrapper.__main__.r.get") as mock_get:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 404
            mock_response.content = b'{"message": "Chart not found"}'
            mock_get.return_value = mock_response

            dw = Datawrapper(access_token="test_token")

            with pytest.raises(FailedRequestError):
                dw.get_chart("invalid_id")

    def test_create_chart_with_rate_limit_raises_rate_limit_error(self):
        """Test that creating a chart when rate limited raises RateLimitError."""
        with patch("datawrapper.__main__.r.post") as mock_post:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 429
            mock_response.content = b'{"message": "Chart creation limit reached"}'
            mock_post.return_value = mock_response

            dw = Datawrapper(access_token="test_token")

            with pytest.raises(RateLimitError) as exc_info:
                dw.create_chart(title="Test", chart_type="d3-bars")

            assert "Chart creation limit reached" in str(exc_info.value)

    def test_delete_chart_unauthorized_raises_failed_request(self):
        """Test that deleting a chart without permission raises FailedRequestError."""
        with patch("datawrapper.__main__.r.delete") as mock_delete:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 403
            mock_response.content = b"Forbidden"
            mock_delete.return_value = mock_response

            dw = Datawrapper(access_token="test_token")

            with pytest.raises(FailedRequestError) as exc_info:
                dw.delete_chart("abc123")

            assert "403" in str(exc_info.value)

    def test_publish_chart_server_error_raises_failed_request(self):
        """Test that publishing a chart with server error raises FailedRequestError."""
        with patch("datawrapper.__main__.r.post") as mock_post:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 500
            mock_response.content = b"Internal Server Error"
            mock_post.return_value = mock_response

            dw = Datawrapper(access_token="test_token")

            with pytest.raises(FailedRequestError) as exc_info:
                dw.publish_chart("abc123")

            assert "500" in str(exc_info.value)

    def test_add_data_bad_request_raises_failed_request(self):
        """Test that adding invalid data raises FailedRequestError."""
        with patch("datawrapper.__main__.r.put") as mock_put:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 400
            mock_response.content = b"Invalid CSV format"
            mock_put.return_value = mock_response

            dw = Datawrapper(access_token="test_token")

            with pytest.raises(FailedRequestError) as exc_info:
                dw.add_data("abc123", "invalid,data")

            assert "400" in str(exc_info.value)


class TestMultipleExceptionTypes:
    """Tests for handling multiple exception types in sequence."""

    def test_different_exceptions_have_different_types(self):
        """Test that different exception types are distinct."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.content = b"{}"

        rate_limit_error = RateLimitError(mock_response)
        failed_request_error = FailedRequestError(mock_response)
        invalid_request_error = InvalidRequestError("Test message")

        # RateLimitError is a FailedRequestError
        assert isinstance(rate_limit_error, RateLimitError)
        assert isinstance(rate_limit_error, FailedRequestError)

        # But FailedRequestError is not a RateLimitError
        assert isinstance(failed_request_error, FailedRequestError)
        assert not isinstance(failed_request_error, RateLimitError)

        # InvalidRequestError is separate
        assert isinstance(invalid_request_error, InvalidRequestError)
        assert not isinstance(invalid_request_error, FailedRequestError)
        assert not isinstance(invalid_request_error, RateLimitError)
