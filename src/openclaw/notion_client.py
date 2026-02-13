"""Notion API client — HTTP helper, query_database, update_page.

Uses Python stdlib only (urllib, json). No external dependencies.
Notion API version: 2022-06-28.
"""

import json
import re
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

    def read_page_blocks(self, page_id: str) -> list[dict]:
        """Read all blocks (children) of a Notion page with pagination.

        Args:
            page_id: The Notion page ID.

        Returns:
            List of all block objects across all pages.
        """
        all_blocks: list[dict] = []
        start_cursor: str | None = None

        while True:
            endpoint = f"blocks/{page_id}/children"
            if start_cursor:
                endpoint += f"?start_cursor={start_cursor}"

            response = self._notion_request("GET", endpoint)

            all_blocks.extend(response.get("results", []))

            if not response.get("has_more"):
                break
            start_cursor = response.get("next_cursor")

        return all_blocks

    def read_page_body(self, page_id: str) -> str:
        """Read a Notion page body and return it as Markdown.

        Convenience method combining read_page_blocks + blocks_to_markdown.

        Args:
            page_id: The Notion page ID.

        Returns:
            Markdown string of the page body.
        """
        raw_blocks = self.read_page_blocks(page_id)
        return blocks_to_markdown(raw_blocks)

    def create_page(
        self,
        database_id: str,
        properties: dict,
        body_markdown: str | None = None,
    ) -> dict:
        """Create a new page in a Notion database.

        Args:
            database_id: The parent database ID.
            properties: Dict of property name to {type, value} pairs.
            body_markdown: Optional Markdown string for the page body.

        Returns:
            Created page object from Notion API.
        """
        notion_props: dict = {}
        for name, prop in properties.items():
            notion_props[name] = _map_property(prop["type"], prop["value"])

        payload: dict = {
            "parent": {"database_id": database_id},
            "properties": notion_props,
        }

        if body_markdown:
            payload["children"] = markdown_to_blocks(body_markdown)

        return self._notion_request("POST", "pages", data=payload)

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


def _render_rich_text(rich_text_list: list[dict]) -> str:
    """Render a Notion rich_text array to Markdown inline text.

    Handles bold, italic, and inline code annotations.

    Args:
        rich_text_list: List of Notion rich_text objects.

    Returns:
        Markdown-formatted string.
    """
    parts: list[str] = []
    for segment in rich_text_list:
        text = segment.get("plain_text", "")
        annotations = segment.get("annotations", {})
        if annotations.get("code"):
            text = f"`{text}`"
        if annotations.get("bold"):
            text = f"**{text}**"
        if annotations.get("italic"):
            text = f"*{text}*"
        parts.append(text)
    return "".join(parts)


def blocks_to_markdown(blocks: list[dict]) -> str:
    """Convert a list of Notion block objects to a Markdown string.

    Supported block types: heading_1/2/3, paragraph, bulleted_list_item,
    numbered_list_item, to_do, code, divider.

    Args:
        blocks: List of Notion block objects.

    Returns:
        Markdown string.
    """
    if not blocks:
        return ""

    lines: list[str] = []
    numbered_counter = 0

    for block in blocks:
        block_type = block.get("type", "")
        block_data = block.get(block_type, {})

        if block_type in ("heading_1", "heading_2", "heading_3"):
            level = int(block_type[-1])
            prefix = "#" * level
            text = _render_rich_text(block_data.get("rich_text", []))
            lines.append(f"{prefix} {text}")
            numbered_counter = 0

        elif block_type == "paragraph":
            text = _render_rich_text(block_data.get("rich_text", []))
            lines.append(text)
            numbered_counter = 0

        elif block_type == "bulleted_list_item":
            text = _render_rich_text(block_data.get("rich_text", []))
            lines.append(f"- {text}")
            numbered_counter = 0

        elif block_type == "numbered_list_item":
            numbered_counter += 1
            text = _render_rich_text(block_data.get("rich_text", []))
            lines.append(f"{numbered_counter}. {text}")

        elif block_type == "to_do":
            text = _render_rich_text(block_data.get("rich_text", []))
            checked = block_data.get("checked", False)
            marker = "[x]" if checked else "[ ]"
            lines.append(f"- {marker} {text}")
            numbered_counter = 0

        elif block_type == "code":
            language = block_data.get("language", "")
            code_text = _render_rich_text(block_data.get("rich_text", []))
            lines.append(f"```{language}")
            lines.append(code_text)
            lines.append("```")
            numbered_counter = 0

        elif block_type == "divider":
            lines.append("---")
            numbered_counter = 0

        else:
            numbered_counter = 0

    return "\n".join(lines)


def _make_text_block(text: str) -> list[dict]:
    """Create a Notion rich_text array from a plain string."""
    return [{"text": {"content": text}}]


def markdown_to_blocks(markdown_text: str) -> list[dict]:
    """Convert basic Markdown text to a list of Notion block objects.

    Supports: headings (#/##/###), bulleted lists (- ), to-do (- [ ]/- [x]),
    and plain paragraphs. Empty lines are skipped.

    Args:
        markdown_text: Markdown string to convert.

    Returns:
        List of Notion block objects.
    """
    if not markdown_text.strip():
        return []

    blocks: list[dict] = []

    for line in markdown_text.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue

        heading_match = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2)
            block_type = f"heading_{level}"
            blocks.append({
                "type": block_type,
                block_type: {"rich_text": _make_text_block(text)},
            })
            continue

        todo_match = re.match(r"^- \[([ xX])\]\s+(.+)$", stripped)
        if todo_match:
            checked = todo_match.group(1).lower() == "x"
            text = todo_match.group(2)
            blocks.append({
                "type": "to_do",
                "to_do": {
                    "rich_text": _make_text_block(text),
                    "checked": checked,
                },
            })
            continue

        if stripped.startswith("- "):
            text = stripped[2:]
            blocks.append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": _make_text_block(text)},
            })
            continue

        blocks.append({
            "type": "paragraph",
            "paragraph": {"rich_text": _make_text_block(stripped)},
        })

    return blocks
