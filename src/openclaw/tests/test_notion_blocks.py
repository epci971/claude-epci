"""Tests for Notion blocks reading, Markdown conversion, and page creation."""

import json
from unittest.mock import MagicMock, patch

import pytest


def _make_mock_response(body: dict) -> MagicMock:
    """Create a mock urllib response returning given JSON body."""
    mock = MagicMock()
    mock.status = 200
    mock.read.return_value = json.dumps(body).encode()
    mock.__enter__ = MagicMock(return_value=mock)
    mock.__exit__ = MagicMock(return_value=False)
    return mock


class TestReadPageBlocks:
    """Tests for read_page_blocks with pagination."""

    def test_returns_all_blocks_single_page(self):
        """read_page_blocks returns block list from single API response."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        blocks = [
            {"type": "heading_1", "heading_1": {"rich_text": [{"plain_text": "Title"}]}},
            {"type": "paragraph", "paragraph": {"rich_text": [{"plain_text": "Hello"}]}},
        ]
        response = {"results": blocks, "has_more": False, "next_cursor": None}

        with patch("urllib.request.urlopen", return_value=_make_mock_response(response)):
            result = client.read_page_blocks("page-123")

        assert len(result) == 2
        assert result[0]["type"] == "heading_1"
        assert result[1]["type"] == "paragraph"

    def test_handles_pagination(self):
        """AC3: read_page_blocks handles pagination via has_more/start_cursor."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        page1 = {
            "results": [{"type": "paragraph", "id": f"block-{i}"} for i in range(100)],
            "has_more": True,
            "next_cursor": "cursor-abc",
        }
        page2 = {
            "results": [{"type": "paragraph", "id": f"block-{i}"} for i in range(100, 120)],
            "has_more": False,
            "next_cursor": None,
        }

        call_count = 0

        def mock_urlopen(request):
            nonlocal call_count
            body = page1 if call_count == 0 else page2
            call_count += 1
            return _make_mock_response(body)

        with patch("urllib.request.urlopen", side_effect=mock_urlopen):
            result = client.read_page_blocks("page-123")

        assert len(result) == 120
        assert call_count == 2

    def test_sends_correct_endpoint(self):
        """read_page_blocks calls GET /v1/blocks/{page_id}/children."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        response = {"results": [], "has_more": False, "next_cursor": None}

        with patch("urllib.request.urlopen", return_value=_make_mock_response(response)) as mock_urlopen:
            client.read_page_blocks("page-xyz")

            request_obj = mock_urlopen.call_args[0][0]
            assert "blocks/page-xyz/children" in request_obj.full_url
            assert request_obj.method == "GET"


class TestBlocksToMarkdown:
    """Tests for blocks_to_markdown converter."""

    def test_heading_blocks(self):
        """AC1: heading_1/2/3 convert to #/##/### Markdown."""
        from openclaw.notion_client import blocks_to_markdown

        blocks = [
            {"type": "heading_1", "heading_1": {"rich_text": [{"plain_text": "H1", "annotations": {"bold": False, "italic": False, "code": False}}]}},
            {"type": "heading_2", "heading_2": {"rich_text": [{"plain_text": "H2", "annotations": {"bold": False, "italic": False, "code": False}}]}},
            {"type": "heading_3", "heading_3": {"rich_text": [{"plain_text": "H3", "annotations": {"bold": False, "italic": False, "code": False}}]}},
        ]

        result = blocks_to_markdown(blocks)
        assert "# H1" in result
        assert "## H2" in result
        assert "### H3" in result

    def test_paragraph_block(self):
        """AC1: paragraph converts to plain text with newline."""
        from openclaw.notion_client import blocks_to_markdown

        blocks = [
            {"type": "paragraph", "paragraph": {"rich_text": [{"plain_text": "Hello world", "annotations": {"bold": False, "italic": False, "code": False}}]}},
        ]

        result = blocks_to_markdown(blocks)
        assert "Hello world" in result

    def test_bulleted_list_item(self):
        """AC1: bulleted_list_item converts to '- item'."""
        from openclaw.notion_client import blocks_to_markdown

        blocks = [
            {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"plain_text": "Item one", "annotations": {"bold": False, "italic": False, "code": False}}]}},
            {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"plain_text": "Item two", "annotations": {"bold": False, "italic": False, "code": False}}]}},
        ]

        result = blocks_to_markdown(blocks)
        assert "- Item one" in result
        assert "- Item two" in result

    def test_numbered_list_item(self):
        """numbered_list_item converts to '1. item'."""
        from openclaw.notion_client import blocks_to_markdown

        blocks = [
            {"type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"plain_text": "First", "annotations": {"bold": False, "italic": False, "code": False}}]}},
            {"type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"plain_text": "Second", "annotations": {"bold": False, "italic": False, "code": False}}]}},
        ]

        result = blocks_to_markdown(blocks)
        assert "1. First" in result
        assert "2. Second" in result

    def test_todo_blocks(self):
        """AC1: to_do converts to '- [ ] item' / '- [x] item'."""
        from openclaw.notion_client import blocks_to_markdown

        blocks = [
            {"type": "to_do", "to_do": {"rich_text": [{"plain_text": "Unchecked", "annotations": {"bold": False, "italic": False, "code": False}}], "checked": False}},
            {"type": "to_do", "to_do": {"rich_text": [{"plain_text": "Checked", "annotations": {"bold": False, "italic": False, "code": False}}], "checked": True}},
        ]

        result = blocks_to_markdown(blocks)
        assert "- [ ] Unchecked" in result
        assert "- [x] Checked" in result

    def test_code_block(self):
        """AC1: code block converts to triple-backtick with language."""
        from openclaw.notion_client import blocks_to_markdown

        blocks = [
            {"type": "code", "code": {"rich_text": [{"plain_text": "print('hello')", "annotations": {"bold": False, "italic": False, "code": False}}], "language": "python"}},
        ]

        result = blocks_to_markdown(blocks)
        assert "```python" in result
        assert "print('hello')" in result
        assert "```" in result

    def test_divider_block(self):
        """divider block converts to '---'."""
        from openclaw.notion_client import blocks_to_markdown

        blocks = [
            {"type": "divider", "divider": {}},
        ]

        result = blocks_to_markdown(blocks)
        assert "---" in result

    def test_rich_text_bold_italic_code(self):
        """Rich text annotations produce **bold**, *italic*, `code`."""
        from openclaw.notion_client import blocks_to_markdown

        blocks = [
            {"type": "paragraph", "paragraph": {"rich_text": [
                {"plain_text": "bold", "annotations": {"bold": True, "italic": False, "code": False}},
                {"plain_text": " and ", "annotations": {"bold": False, "italic": False, "code": False}},
                {"plain_text": "italic", "annotations": {"bold": False, "italic": True, "code": False}},
                {"plain_text": " and ", "annotations": {"bold": False, "italic": False, "code": False}},
                {"plain_text": "code", "annotations": {"bold": False, "italic": False, "code": True}},
            ]}},
        ]

        result = blocks_to_markdown(blocks)
        assert "**bold**" in result
        assert "*italic*" in result
        assert "`code`" in result

    def test_empty_blocks_list(self):
        """Empty blocks list returns empty string."""
        from openclaw.notion_client import blocks_to_markdown

        result = blocks_to_markdown([])
        assert result == ""

    def test_unknown_block_type_skipped(self):
        """Unknown block types are silently skipped."""
        from openclaw.notion_client import blocks_to_markdown

        blocks = [
            {"type": "unsupported_type", "unsupported_type": {}},
            {"type": "paragraph", "paragraph": {"rich_text": [{"plain_text": "After", "annotations": {"bold": False, "italic": False, "code": False}}]}},
        ]

        result = blocks_to_markdown(blocks)
        assert "After" in result


class TestReadPageBody:
    """Tests for read_page_body convenience function."""

    def test_returns_markdown_from_page(self):
        """read_page_body combines read_page_blocks + blocks_to_markdown."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        blocks = [
            {"type": "heading_1", "heading_1": {"rich_text": [{"plain_text": "Title", "annotations": {"bold": False, "italic": False, "code": False}}]}},
            {"type": "paragraph", "paragraph": {"rich_text": [{"plain_text": "Content here", "annotations": {"bold": False, "italic": False, "code": False}}]}},
        ]
        response = {"results": blocks, "has_more": False, "next_cursor": None}

        with patch("urllib.request.urlopen", return_value=_make_mock_response(response)):
            result = client.read_page_body("page-123")

        assert "# Title" in result
        assert "Content here" in result
        assert isinstance(result, str)


class TestMarkdownToBlocks:
    """Tests for markdown_to_blocks converter."""

    def test_heading_levels(self):
        """Headings convert to heading_1/2/3 blocks."""
        from openclaw.notion_client import markdown_to_blocks

        md = "# Title\n## Subtitle\n### Section"
        blocks = markdown_to_blocks(md)

        assert len(blocks) == 3
        assert blocks[0]["type"] == "heading_1"
        assert blocks[0]["heading_1"]["rich_text"][0]["text"]["content"] == "Title"
        assert blocks[1]["type"] == "heading_2"
        assert blocks[2]["type"] == "heading_3"

    def test_paragraph(self):
        """Plain text converts to paragraph blocks."""
        from openclaw.notion_client import markdown_to_blocks

        md = "Hello world"
        blocks = markdown_to_blocks(md)

        assert len(blocks) == 1
        assert blocks[0]["type"] == "paragraph"
        assert blocks[0]["paragraph"]["rich_text"][0]["text"]["content"] == "Hello world"

    def test_bulleted_list(self):
        """Lines starting with '- ' convert to bulleted_list_item blocks."""
        from openclaw.notion_client import markdown_to_blocks

        md = "- Item one\n- Item two"
        blocks = markdown_to_blocks(md)

        assert len(blocks) == 2
        assert blocks[0]["type"] == "bulleted_list_item"
        assert blocks[0]["bulleted_list_item"]["rich_text"][0]["text"]["content"] == "Item one"
        assert blocks[1]["type"] == "bulleted_list_item"

    def test_todo_unchecked(self):
        """Lines starting with '- [ ] ' convert to unchecked to_do blocks."""
        from openclaw.notion_client import markdown_to_blocks

        md = "- [ ] Task to do"
        blocks = markdown_to_blocks(md)

        assert len(blocks) == 1
        assert blocks[0]["type"] == "to_do"
        assert blocks[0]["to_do"]["checked"] is False
        assert blocks[0]["to_do"]["rich_text"][0]["text"]["content"] == "Task to do"

    def test_todo_checked(self):
        """Lines starting with '- [x] ' convert to checked to_do blocks."""
        from openclaw.notion_client import markdown_to_blocks

        md = "- [x] Done task"
        blocks = markdown_to_blocks(md)

        assert len(blocks) == 1
        assert blocks[0]["type"] == "to_do"
        assert blocks[0]["to_do"]["checked"] is True

    def test_empty_string(self):
        """Empty string returns empty list."""
        from openclaw.notion_client import markdown_to_blocks

        assert markdown_to_blocks("") == []

    def test_skips_empty_lines(self):
        """Empty lines are skipped."""
        from openclaw.notion_client import markdown_to_blocks

        md = "# Title\n\nParagraph"
        blocks = markdown_to_blocks(md)

        assert len(blocks) == 2
        assert blocks[0]["type"] == "heading_1"
        assert blocks[1]["type"] == "paragraph"


class TestCreatePage:
    """Tests for create_page with properties and body."""

    def test_creates_page_with_properties(self):
        """AC2: create_page sends POST /v1/pages with database parent and properties."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        response_body = {"id": "new-page-id", "object": "page"}

        with patch("urllib.request.urlopen", return_value=_make_mock_response(response_body)) as mock_urlopen:
            result = client.create_page(
                database_id="db-123",
                properties={"Statut": {"type": "select", "value": "A faire"}},
            )

            request_obj = mock_urlopen.call_args[0][0]
            assert request_obj.method == "POST"
            assert "pages" in request_obj.full_url

            sent_body = json.loads(request_obj.data)
            assert sent_body["parent"] == {"database_id": "db-123"}
            assert sent_body["properties"]["Statut"] == {"select": {"name": "A faire"}}

        assert result["id"] == "new-page-id"

    def test_creates_page_with_body_markdown(self):
        """AC2: create_page includes body blocks from Markdown."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        response_body = {"id": "new-page-id", "object": "page"}

        with patch("urllib.request.urlopen", return_value=_make_mock_response(response_body)) as mock_urlopen:
            client.create_page(
                database_id="db-123",
                properties={},
                body_markdown="# Hello\nWorld",
            )

            request_obj = mock_urlopen.call_args[0][0]
            sent_body = json.loads(request_obj.data)
            assert "children" in sent_body
            assert len(sent_body["children"]) == 2
            assert sent_body["children"][0]["type"] == "heading_1"
            assert sent_body["children"][1]["type"] == "paragraph"

    def test_creates_page_without_body(self):
        """create_page with no body_markdown sends no children."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        response_body = {"id": "new-page-id", "object": "page"}

        with patch("urllib.request.urlopen", return_value=_make_mock_response(response_body)) as mock_urlopen:
            client.create_page(
                database_id="db-123",
                properties={"Name": {"type": "text", "value": "Test"}},
            )

            request_obj = mock_urlopen.call_args[0][0]
            sent_body = json.loads(request_obj.data)
            assert "children" not in sent_body

    def test_returns_created_page_object(self):
        """create_page returns the full page object from API."""
        from openclaw.notion_client import NotionClient

        client = NotionClient(api_key="test-key", rate_limit_sleep=0)

        response_body = {"id": "page-abc", "object": "page", "url": "https://notion.so/page-abc"}

        with patch("urllib.request.urlopen", return_value=_make_mock_response(response_body)):
            result = client.create_page(
                database_id="db-123",
                properties={},
            )

        assert result["id"] == "page-abc"
        assert result["url"] == "https://notion.so/page-abc"
