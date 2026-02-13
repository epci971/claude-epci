"""Notion API client — HTTP helper, query_database, update_page.

Uses Python stdlib only (urllib, json). No external dependencies.
Notion API version: 2022-06-28.
"""

import json
import time
import urllib.error
import urllib.request

BASE_URL = "https://api.notion.com/v1/"
NOTION_VERSION = "2022-06-28"


class NotionAPIError(Exception):
    """Raised when Notion API returns a non-2xx response."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"Notion API error {status_code}: {message}")


class NotionClient:
    """Notion API client with rate limiting and pagination support.

    Args:
        api_key: Notion integration token.
        rate_limit_sleep: Seconds to sleep between requests (default 0.35).
    """

    def __init__(self, api_key: str, rate_limit_sleep: float = 0.35) -> None:
        self._api_key = api_key
        self._rate_limit_sleep = rate_limit_sleep

    def _notion_request(
        self,
        method: str,
        endpoint: str,
        data: dict | None = None,
    ) -> dict:
        """Send an HTTP request to Notion API.

        Args:
            method: HTTP method (GET, POST, PATCH).
            endpoint: API endpoint relative to base URL.
            data: Optional JSON body.

        Returns:
            Parsed JSON response as dict.

        Raises:
            NotionAPIError: On non-2xx response.
        """
        url = BASE_URL + endpoint
        body = json.dumps(data).encode() if data else None

        request = urllib.request.Request(
            url,
            data=body,
            method=method,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Notion-Version": NOTION_VERSION,
                "Content-Type": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(request) as response:
                result = json.loads(response.read())
        except urllib.error.HTTPError as e:
            error_body = e.fp.read().decode() if e.fp else ""
            raise NotionAPIError(e.code, error_body) from e

        time.sleep(self._rate_limit_sleep)
        return result

    def query_database(
        self,
        database_id: str,
        filter_obj: dict | None = None,
        sorts: list[dict] | None = None,
    ) -> list[dict]:
        """Query a Notion database with optional filtering and pagination.

        Args:
            database_id: The Notion database ID.
            filter_obj: Optional Notion filter object.
            sorts: Optional list of sort objects.

        Returns:
            List of all page objects across all pages.
        """
        all_results: list[dict] = []
        start_cursor: str | None = None

        while True:
            payload: dict = {}
            if filter_obj:
                payload["filter"] = filter_obj
            if sorts:
                payload["sorts"] = sorts
            if start_cursor:
                payload["start_cursor"] = start_cursor

            response = self._notion_request(
                "POST",
                f"databases/{database_id}/query",
                data=payload,
            )

            all_results.extend(response.get("results", []))

            if not response.get("has_more"):
                break
            start_cursor = response.get("next_cursor")

        return all_results

    def update_page(self, page_id: str, properties: dict) -> dict:
        """Update Notion page properties with type mapping.

        Args:
            page_id: The Notion page ID.
            properties: Dict of property name to {type, value} pairs.
                Supported types: select, number, text, checkbox, url, date.

        Returns:
            Updated page object from Notion API.
        """
        notion_props: dict = {}

        for name, prop in properties.items():
            notion_props[name] = _map_property(prop["type"], prop["value"])

        return self._notion_request(
            "PATCH",
            f"pages/{page_id}",
            data={"properties": notion_props},
        )


PROPERTY_MAPPERS = {
    "select": lambda v: {"select": {"name": v}},
    "number": lambda v: {"number": v},
    "text": lambda v: {"rich_text": [{"text": {"content": v}}]},
    "checkbox": lambda v: {"checkbox": v},
    "url": lambda v: {"url": v},
    "date": lambda v: {"date": {"start": v}},
}


def _map_property(prop_type: str, value: object) -> dict:
    """Map a high-level property to Notion API format.

    Args:
        prop_type: Property type (select, number, text, checkbox, url, date).
        value: The property value.

    Returns:
        Notion API formatted property dict.

    Raises:
        ValueError: If prop_type is unknown.
    """
    mapper = PROPERTY_MAPPERS.get(prop_type)
    if not mapper:
        raise ValueError(f"Unknown property type: {prop_type}")
    return mapper(value)
