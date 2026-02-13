"""Tests for task selector — priority sorting, dependency resolution, circular detection."""

import pytest

from openclaw.task_selector import (
    detect_circular_dependencies,
    get_eligible_tasks,
    parse_task,
    resolve_dependencies,
    select_next_task,
    sort_by_priority,
)


def _make_notion_page(
    page_id: str,
    name: str,
    status: str = "A faire",
    priority: str = "P1",
    story_id: str = "",
    bloque_par: list[dict] | None = None,
    complexity: str = "Simple",
    spec_path: str = "",
    flags: list[str] | None = None,
) -> dict:
    """Build a mock Notion page object matching the API response format."""
    properties: dict = {
        "Name": {"title": [{"plain_text": name}]},
        "Statut": {"select": {"name": status}},
        "Priorite": {"select": {"name": priority}},
        "Story ID": {"rich_text": [{"plain_text": story_id}] if story_id else []},
        "Complexite": {"select": {"name": complexity}},
        "Bloque par": {"relation": bloque_par or []},
        "Spec Path": {"rich_text": [{"plain_text": spec_path}] if spec_path else []},
        "Flags": {"multi_select": [{"name": f} for f in (flags or [])]},
    }
    return {"id": page_id, "properties": properties}


class TestParseTask:
    """Tests for parse_task — extract fields from Notion page object."""

    def test_parses_all_fields(self):
        """parse_task extracts page_id, name, status, priority, story_id, bloque_par."""
        page = _make_notion_page(
            page_id="page-1",
            name="Build login",
            status="A faire",
            priority="P0",
            story_id="US-001",
            bloque_par=[{"id": "page-2"}],
            complexity="Moyenne",
            spec_path="specs/task-001.md",
            flags=["validate_plan"],
        )

        task = parse_task(page)

        assert task["page_id"] == "page-1"
        assert task["name"] == "Build login"
        assert task["status"] == "A faire"
        assert task["priority"] == "P0"
        assert task["story_id"] == "US-001"
        assert task["bloque_par"] == ["page-2"]
        assert task["complexity"] == "Moyenne"
        assert task["spec_path"] == "specs/task-001.md"
        assert task["flags"] == ["validate_plan"]

    def test_handles_empty_optional_fields(self):
        """parse_task returns empty defaults for missing optional fields."""
        page = _make_notion_page(page_id="page-3", name="Simple task")

        task = parse_task(page)

        assert task["story_id"] == ""
        assert task["bloque_par"] == []
        assert task["spec_path"] == ""
        assert task["flags"] == []

    def test_handles_missing_priority_select(self):
        """parse_task defaults to P3 when priority select is None."""
        page = _make_notion_page(page_id="page-4", name="No priority")
        page["properties"]["Priorite"] = {"select": None}

        task = parse_task(page)

        assert task["priority"] == "P3"

    def test_handles_missing_status_select(self):
        """parse_task defaults to 'A faire' when status select is None."""
        page = _make_notion_page(page_id="page-5", name="No status")
        page["properties"]["Statut"] = {"select": None}

        task = parse_task(page)

        assert task["status"] == "A faire"


class TestGetEligibleTasks:
    """Tests for get_eligible_tasks — filter by status 'A faire'."""

    def test_filters_a_faire_tasks(self):
        """get_eligible_tasks returns only tasks with status 'A faire'."""
        tasks = [
            {"page_id": "1", "status": "A faire", "name": "T1"},
            {"page_id": "2", "status": "Termine", "name": "T2"},
            {"page_id": "3", "status": "A faire", "name": "T3"},
            {"page_id": "4", "status": "Echoue", "name": "T4"},
        ]

        eligible = get_eligible_tasks(tasks)

        assert len(eligible) == 2
        assert eligible[0]["page_id"] == "1"
        assert eligible[1]["page_id"] == "3"

    def test_returns_empty_for_no_eligible(self):
        """get_eligible_tasks returns empty list when no tasks are 'A faire'."""
        tasks = [
            {"page_id": "1", "status": "Termine", "name": "T1"},
            {"page_id": "2", "status": "Bloque", "name": "T2"},
        ]

        eligible = get_eligible_tasks(tasks)

        assert eligible == []


class TestSortByPriority:
    """Tests for sort_by_priority — P0 > P1 > P2 > P3 with Story ID tiebreaker."""

    def test_sorts_by_priority_order(self):
        """AC1: sort_by_priority orders P0 first, then P1, P2, P3."""
        tasks = [
            {"page_id": "1", "priority": "P2", "story_id": "US-001"},
            {"page_id": "2", "priority": "P0", "story_id": "US-002"},
            {"page_id": "3", "priority": "P1", "story_id": "US-003"},
        ]

        sorted_tasks = sort_by_priority(tasks)

        assert sorted_tasks[0]["page_id"] == "2"  # P0
        assert sorted_tasks[1]["page_id"] == "3"  # P1
        assert sorted_tasks[2]["page_id"] == "1"  # P2

    def test_tiebreaker_by_story_id(self):
        """AC4: equal priority tasks sorted by Story ID alphanumerically."""
        tasks = [
            {"page_id": "1", "priority": "P1", "story_id": "US-003"},
            {"page_id": "2", "priority": "P1", "story_id": "US-001"},
        ]

        sorted_tasks = sort_by_priority(tasks)

        assert sorted_tasks[0]["page_id"] == "2"  # US-001
        assert sorted_tasks[1]["page_id"] == "1"  # US-003

    def test_missing_priority_defaults_to_p3(self):
        """Missing priority treated as P3 (lowest)."""
        tasks = [
            {"page_id": "1", "priority": "P3", "story_id": "US-002"},
            {"page_id": "2", "priority": "UNKNOWN", "story_id": "US-001"},
            {"page_id": "3", "priority": "P1", "story_id": "US-003"},
        ]

        sorted_tasks = sort_by_priority(tasks)

        assert sorted_tasks[0]["page_id"] == "3"  # P1
        # P3 and UNKNOWN (treated as P3) — tiebreaker by story_id
        assert sorted_tasks[1]["page_id"] == "2"  # US-001
        assert sorted_tasks[2]["page_id"] == "1"  # US-002


class TestResolveDependencies:
    """Tests for resolve_dependencies — check bloque_par targets."""

    def test_unblocked_task_passes(self):
        """Task with no dependencies is not blocked."""
        tasks = [
            {"page_id": "1", "bloque_par": [], "status": "A faire"},
        ]
        all_tasks = tasks

        unblocked = resolve_dependencies(tasks, all_tasks)

        assert len(unblocked) == 1
        assert unblocked[0]["page_id"] == "1"

    def test_blocked_by_unfinished_dependency(self):
        """AC2: Task blocked when dependency is not 'Termine'."""
        all_tasks = [
            {"page_id": "1", "bloque_par": ["2"], "status": "A faire"},
            {"page_id": "2", "bloque_par": [], "status": "A faire"},
        ]
        candidates = [all_tasks[0]]

        unblocked = resolve_dependencies(candidates, all_tasks)

        assert unblocked == []

    def test_unblocked_when_dependency_termine(self):
        """Task unblocked when all dependencies have status 'Termine'."""
        all_tasks = [
            {"page_id": "1", "bloque_par": ["2"], "status": "A faire"},
            {"page_id": "2", "bloque_par": [], "status": "Termine"},
        ]
        candidates = [all_tasks[0]]

        unblocked = resolve_dependencies(candidates, all_tasks)

        assert len(unblocked) == 1
        assert unblocked[0]["page_id"] == "1"

    def test_blocked_by_failed_dependency(self):
        """Task blocked when dependency has status 'Echoue'."""
        all_tasks = [
            {"page_id": "1", "bloque_par": ["2"], "status": "A faire"},
            {"page_id": "2", "bloque_par": [], "status": "Echoue"},
        ]
        candidates = [all_tasks[0]]

        unblocked = resolve_dependencies(candidates, all_tasks)

        assert unblocked == []


class TestDetectCircularDependencies:
    """Tests for detect_circular_dependencies — DFS cycle detection."""

    def test_no_cycle_returns_empty(self):
        """No circular dependencies returns empty set."""
        tasks = [
            {"page_id": "1", "bloque_par": ["2"]},
            {"page_id": "2", "bloque_par": []},
        ]

        circular = detect_circular_dependencies(tasks)

        assert circular == set()

    def test_detects_simple_cycle(self):
        """AC3: Detects circular dependency between two tasks."""
        tasks = [
            {"page_id": "1", "bloque_par": ["2"]},
            {"page_id": "2", "bloque_par": ["1"]},
        ]

        circular = detect_circular_dependencies(tasks)

        assert "1" in circular
        assert "2" in circular

    def test_detects_three_node_cycle(self):
        """Detects cycle involving three tasks: 1->2->3->1."""
        tasks = [
            {"page_id": "1", "bloque_par": ["2"]},
            {"page_id": "2", "bloque_par": ["3"]},
            {"page_id": "3", "bloque_par": ["1"]},
        ]

        circular = detect_circular_dependencies(tasks)

        assert circular == {"1", "2", "3"}

    def test_partial_cycle_only_marks_involved(self):
        """Only tasks in the cycle are marked, not unrelated ones."""
        tasks = [
            {"page_id": "1", "bloque_par": ["2"]},
            {"page_id": "2", "bloque_par": ["1"]},
            {"page_id": "3", "bloque_par": []},
        ]

        circular = detect_circular_dependencies(tasks)

        assert "1" in circular
        assert "2" in circular
        assert "3" not in circular


class TestSelectNextTask:
    """Tests for select_next_task — main entry point."""

    def test_selects_highest_priority(self):
        """AC1: Selects highest priority task from eligible tasks."""
        pages = [
            _make_notion_page("p1", "T1", priority="P2", story_id="US-001"),
            _make_notion_page("p2", "T2", priority="P0", story_id="US-002"),
            _make_notion_page("p3", "T3", priority="P1", story_id="US-003"),
        ]

        result = select_next_task(pages)

        assert result is not None
        assert result["page_id"] == "p2"

    def test_respects_dependencies(self):
        """AC2: Skips task blocked by unfinished dependency."""
        pages = [
            _make_notion_page("p1", "T1", priority="P0", bloque_par=[{"id": "p2"}]),
            _make_notion_page("p2", "T2", priority="P1"),
        ]

        result = select_next_task(pages)

        assert result is not None
        assert result["page_id"] == "p2"

    def test_skips_circular_dependencies(self):
        """AC3: Tasks in circular dependency are not selected."""
        pages = [
            _make_notion_page("p1", "T1", priority="P0", bloque_par=[{"id": "p2"}]),
            _make_notion_page("p2", "T2", priority="P1", bloque_par=[{"id": "p1"}]),
        ]

        result = select_next_task(pages)

        assert result is None

    def test_returns_none_when_no_eligible(self):
        """Returns None when no tasks are eligible."""
        pages = [
            _make_notion_page("p1", "T1", status="Termine"),
            _make_notion_page("p2", "T2", status="Echoue"),
        ]

        result = select_next_task(pages)

        assert result is None

    def test_returns_none_for_empty_list(self):
        """Returns None for empty task list."""
        result = select_next_task([])

        assert result is None

    def test_returns_none_when_all_blocked(self):
        """Returns None when all eligible tasks are blocked."""
        pages = [
            _make_notion_page("p1", "T1", priority="P0", bloque_par=[{"id": "p2"}]),
            _make_notion_page("p2", "T2", status="En cours"),
        ]

        result = select_next_task(pages)

        assert result is None

    def test_tiebreaker_story_id(self):
        """AC4: Equal priority uses Story ID tiebreaker."""
        pages = [
            _make_notion_page("p1", "T1", priority="P1", story_id="US-003"),
            _make_notion_page("p2", "T2", priority="P1", story_id="US-001"),
        ]

        result = select_next_task(pages)

        assert result is not None
        assert result["page_id"] == "p2"
