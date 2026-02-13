"""Tests for Notion API client — HTTP helper, query_database, update_page."""

import json
import time
from unittest.mock import MagicMock, patch

import pytest


class TestNotionRequest:
    """Tests for _notion_request HTTP helper."""

    def test_sends_correct_headers(self):
        """HTTP helper sets Authorization, Notion-Version, Content-Type headers."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"object": "page"}'
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_response) as mock_urlopen:
            client._notion_request("GET", "pages/abc")

            request_obj = mock_urlopen.call_args[0][0]
            assert request_obj.get_header("Authorization") == "Bearer test-key"
            assert request_obj.get_header("Notion-version") == "2022-06-28"
            assert request_obj.get_header("Content-type") == "application/json"

    def test_builds_correct_url(self):
        """HTTP helper builds URL from base + endpoint."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"ok": true}'
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_response) as mock_urlopen:
            client._notion_request("GET", "databases/db-123")

            request_obj = mock_urlopen.call_args[0][0]
            assert request_obj.full_url == "https://api.notion.com/v1/databases/db-123"

    def test_sends_json_body_for_post(self):
        """HTTP helper sends JSON-encoded body for POST requests."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"results": []}'
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)

        body = {"filter": {"property": "Statut"}}

        with patch("urllib.request.urlopen", return_value=mock_response) as mock_urlopen:
            client._notion_request("POST", "databases/db-123/query", data=body)

            request_obj = mock_urlopen.call_args[0][0]
            assert json.loads(request_obj.data) == body

    def test_raises_on_http_error(self):
        """HTTP helper raises NotionAPIError on non-2xx response."""
        from urllib.error import HTTPError

        from openclaw.notion_client import NotionAPIError, NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        error = HTTPError(
            url="https://api.notion.com/v1/pages/abc",
            code=404,
            msg="Not Found",
            hdrs={},
            fp=MagicMock(read=MagicMock(return_value=b'{"message": "not found"}')),
        )

        with patch("urllib.request.urlopen", side_effect=error):
            with pytest.raises(NotionAPIError, match="404"):
                client._notion_request("GET", "pages/abc")

    def test_applies_rate_limiting(self):
        """HTTP helper sleeps for rate_limit_sleep between calls."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0.1)

        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"ok": true}'
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_response):
            with patch("time.sleep") as mock_sleep:
                client._notion_request("GET", "pages/abc")
                mock_sleep.assert_called_once_with(0.1)


def _make_mock_response(body: dict) -> MagicMock:
    """Create a mock urllib response returning given JSON body."""
    mock = MagicMock()
    mock.status = 200
    mock.read.return_value = json.dumps(body).encode()
    mock.__enter__ = MagicMock(return_value=mock)
    mock.__exit__ = MagicMock(return_value=False)
    return mock


class TestQueryDatabase:
    """Tests for query_database with filtering and pagination."""

    def test_query_with_status_filter(self):
        """AC1: query_database with status filter returns page results."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        response_body = {
            "results": [
                {"id": "page-1", "properties": {"Name": {"title": [{"plain_text": "Task 1"}]}}},
                {"id": "page-2", "properties": {"Name": {"title": [{"plain_text": "Task 2"}]}}},
            ],
            "has_more": False,
            "next_cursor": None,
        }

        with patch("urllib.request.urlopen", return_value=_make_mock_response(response_body)):
            results = client.query_database(
                database_id="db-123",
                filter_obj={"property": "Statut", "select": {"equals": "A faire"}},
            )

        assert len(results) == 2
        assert results[0]["id"] == "page-1"
        assert results[1]["id"] == "page-2"

    def test_query_sends_filter_in_body(self):
        """query_database sends filter object in POST body."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        response_body = {"results": [], "has_more": False, "next_cursor": None}

        filter_obj = {"property": "Statut", "select": {"equals": "A faire"}}

        with patch("urllib.request.urlopen", return_value=_make_mock_response(response_body)) as mock_urlopen:
            client.query_database(database_id="db-123", filter_obj=filter_obj)

            request_obj = mock_urlopen.call_args[0][0]
            sent_body = json.loads(request_obj.data)
            assert sent_body["filter"] == filter_obj

    def test_query_sends_sorts_in_body(self):
        """query_database sends sorts array in POST body."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        response_body = {"results": [], "has_more": False, "next_cursor": None}

        sorts = [{"property": "Priorite", "direction": "ascending"}]

        with patch("urllib.request.urlopen", return_value=_make_mock_response(response_body)) as mock_urlopen:
            client.query_database(database_id="db-123", sorts=sorts)

            request_obj = mock_urlopen.call_args[0][0]
            sent_body = json.loads(request_obj.data)
            assert sent_body["sorts"] == sorts

    def test_query_handles_pagination(self):
        """AC3: Pagination handled via has_more/start_cursor for 100+ results."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        page1 = {
            "results": [{"id": f"page-{i}"} for i in range(100)],
            "has_more": True,
            "next_cursor": "cursor-abc",
        }
        page2 = {
            "results": [{"id": f"page-{i}"} for i in range(100, 150)],
            "has_more": False,
            "next_cursor": None,
        }

        call_count = 0

        def mock_urlopen(request):
            nonlocal call_count
            body = page1 if call_count == 0 else page2
            call_count += 1
            return _make_mock_response(body)

        with patch("urllib.request.urlopen", side_effect=mock_urlopen) as mock_open:
            results = client.query_database(database_id="db-123")

        assert len(results) == 150
        assert call_count == 2

    def test_query_sends_start_cursor_on_pagination(self):
        """Pagination sends start_cursor in subsequent requests."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        page1 = {"results": [{"id": "p1"}], "has_more": True, "next_cursor": "cursor-xyz"}
        page2 = {"results": [{"id": "p2"}], "has_more": False, "next_cursor": None}

        responses = [_make_mock_response(page1), _make_mock_response(page2)]

        with patch("urllib.request.urlopen", side_effect=responses) as mock_urlopen:
            client.query_database(database_id="db-123")

            second_request = mock_urlopen.call_args_list[1][0][0]
            second_body = json.loads(second_request.data)
            assert second_body["start_cursor"] == "cursor-xyz"


class TestUpdatePage:
    """Tests for update_page with property type mapping."""

    def test_update_select_property(self):
        """AC2: update_page maps select property to Notion API format."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        with patch("urllib.request.urlopen", return_value=_make_mock_response({"object": "page"})) as mock_urlopen:
            client.update_page("page-abc", {"Statut": {"type": "select", "value": "En cours"}})

            request_obj = mock_urlopen.call_args[0][0]
            sent_body = json.loads(request_obj.data)
            assert sent_body["properties"]["Statut"] == {"select": {"name": "En cours"}}

    def test_update_number_property(self):
        """update_page maps number property to Notion API format."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        with patch("urllib.request.urlopen", return_value=_make_mock_response({"object": "page"})) as mock_urlopen:
            client.update_page("page-abc", {"Attempts": {"type": "number", "value": 3}})

            request_obj = mock_urlopen.call_args[0][0]
            sent_body = json.loads(request_obj.data)
            assert sent_body["properties"]["Attempts"] == {"number": 3}

    def test_update_text_property(self):
        """update_page maps text property to rich_text Notion API format."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        with patch("urllib.request.urlopen", return_value=_make_mock_response({"object": "page"})) as mock_urlopen:
            client.update_page("page-abc", {"Erreurs": {"type": "text", "value": "timeout error"}})

            request_obj = mock_urlopen.call_args[0][0]
            sent_body = json.loads(request_obj.data)
            expected = {"rich_text": [{"text": {"content": "timeout error"}}]}
            assert sent_body["properties"]["Erreurs"] == expected

    def test_update_checkbox_property(self):
        """update_page maps checkbox property to Notion API format."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        with patch("urllib.request.urlopen", return_value=_make_mock_response({"object": "page"})) as mock_urlopen:
            client.update_page("page-abc", {"Passes": {"type": "checkbox", "value": True}})

            request_obj = mock_urlopen.call_args[0][0]
            sent_body = json.loads(request_obj.data)
            assert sent_body["properties"]["Passes"] == {"checkbox": True}

    def test_update_url_property(self):
        """update_page maps url property to Notion API format."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        with patch("urllib.request.urlopen", return_value=_make_mock_response({"object": "page"})) as mock_urlopen:
            client.update_page("page-abc", {"PR URL": {"type": "url", "value": "https://github.com/pr/1"}})

            request_obj = mock_urlopen.call_args[0][0]
            sent_body = json.loads(request_obj.data)
            assert sent_body["properties"]["PR URL"] == {"url": "https://github.com/pr/1"}

    def test_update_date_property(self):
        """update_page maps date property to Notion API format."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        with patch("urllib.request.urlopen", return_value=_make_mock_response({"object": "page"})) as mock_urlopen:
            client.update_page("page-abc", {"Demarre le": {"type": "date", "value": "2026-02-13T16:00:00Z"}})

            request_obj = mock_urlopen.call_args[0][0]
            sent_body = json.loads(request_obj.data)
            assert sent_body["properties"]["Demarre le"] == {"date": {"start": "2026-02-13T16:00:00Z"}}

    def test_update_uses_patch_method(self):
        """update_page sends PATCH request to pages/{page_id}."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        with patch("urllib.request.urlopen", return_value=_make_mock_response({"object": "page"})) as mock_urlopen:
            client.update_page("page-xyz", {"Passes": {"type": "checkbox", "value": True}})

            request_obj = mock_urlopen.call_args[0][0]
            assert request_obj.method == "PATCH"
            assert "pages/page-xyz" in request_obj.full_url

    def test_update_multiple_properties(self):
        """update_page handles multiple properties in a single call."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        properties = {
            "Statut": {"type": "select", "value": "Termine"},
            "Passes": {"type": "checkbox", "value": True},
            "Attempts": {"type": "number", "value": 1},
        }

        with patch("urllib.request.urlopen", return_value=_make_mock_response({"object": "page"})) as mock_urlopen:
            client.update_page("page-abc", properties)

            request_obj = mock_urlopen.call_args[0][0]
            sent_body = json.loads(request_obj.data)
            assert sent_body["properties"]["Statut"] == {"select": {"name": "Termine"}}
            assert sent_body["properties"]["Passes"] == {"checkbox": True}
            assert sent_body["properties"]["Attempts"] == {"number": 1}
