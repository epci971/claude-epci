"""Task selector — priority sorting, dependency resolution, circular detection.

Determines which Notion task to execute next based on status, priority,
dependency relations, and circular dependency detection.
Uses Python stdlib only. No external dependencies.
"""

PRIORITY_ORDER: dict[str, int] = {
    "P0": 0,
    "P1": 1,
    "P2": 2,
    "P3": 3,
}

DONE_STATUSES = frozenset({"Termine"})
BLOCKING_STATUSES = frozenset({"A faire", "Bloque", "En cours", "En review", "En review (partiel)", "Echoue"})


def _extract_plain_text(prop: dict) -> str:
    """Extract plain text from a Notion rich_text or title property."""
    items = prop.get("rich_text") or prop.get("title") or []
    if not items:
        return ""
    return items[0].get("plain_text", "")


def _extract_select(prop: dict, default: str = "") -> str:
    """Extract value from a Notion select property, with fallback."""
    select = prop.get("select")
    if not select:
        return default
    return select.get("name", default)


def _extract_relation_ids(prop: dict) -> list[str]:
    """Extract list of page IDs from a Notion relation property."""
    return [rel["id"] for rel in prop.get("relation", [])]


def _extract_multi_select(prop: dict) -> list[str]:
    """Extract list of names from a Notion multi_select property."""
    return [item["name"] for item in prop.get("multi_select", [])]


def parse_task(notion_page: dict) -> dict:
    """Parse a Notion page object into a flat task dict.

    Args:
        notion_page: Raw Notion page object from query_database.

    Returns:
        Dict with keys: page_id, name, story_id, status, priority,
        complexity, bloque_par, spec_path, flags.
    """
    props = notion_page.get("properties", {})

    return {
        "page_id": notion_page["id"],
        "name": _extract_plain_text(props.get("Name", {})),
        "story_id": _extract_plain_text(props.get("Story ID", {})),
        "status": _extract_select(props.get("Statut", {}), default="A faire"),
        "priority": _extract_select(props.get("Priorite", {}), default="P3"),
        "complexity": _extract_select(props.get("Complexite", {}), default="Simple"),
        "bloque_par": _extract_relation_ids(props.get("Bloque par", {})),
        "spec_path": _extract_plain_text(props.get("Spec Path", {})),
        "flags": _extract_multi_select(props.get("Flags", {})),
    }


def get_eligible_tasks(tasks: list[dict]) -> list[dict]:
    """Filter tasks to only those with status 'A faire'.

    Args:
        tasks: List of parsed task dicts.

    Returns:
        List of tasks eligible for execution.
    """
    return [t for t in tasks if t["status"] == "A faire"]


def sort_by_priority(tasks: list[dict]) -> list[dict]:
    """Sort tasks by priority (P0 highest) then by Story ID as tiebreaker.

    Unknown priorities are treated as P3 (lowest).

    Args:
        tasks: List of parsed task dicts.

    Returns:
        New list sorted by priority then story_id.
    """
    def sort_key(task: dict) -> tuple[int, str]:
        priority_rank = PRIORITY_ORDER.get(task.get("priority", "P3"), 3)
        story_id = task.get("story_id", "")
        return (priority_rank, story_id)

    return sorted(tasks, key=sort_key)


def resolve_dependencies(
    candidates: list[dict],
    all_tasks: list[dict],
) -> list[dict]:
    """Filter out tasks whose dependencies are not all 'Termine'.

    A task is blocked if any of its "Bloque par" targets has a status
    other than "Termine". Failed dependencies also block downstream.

    Args:
        candidates: Tasks to evaluate (already filtered as eligible).
        all_tasks: Full list of parsed tasks (for status lookups).

    Returns:
        List of unblocked tasks.
    """
    status_by_id = {t["page_id"]: t["status"] for t in all_tasks}

    unblocked: list[dict] = []
    for task in candidates:
        blocked = False
        for dep_id in task.get("bloque_par", []):
            dep_status = status_by_id.get(dep_id)
            if dep_status not in DONE_STATUSES:
                blocked = True
                break
        if not blocked:
            unblocked.append(task)

    return unblocked


def detect_circular_dependencies(tasks: list[dict]) -> set[str]:
    """Detect tasks involved in circular dependency chains using DFS.

    Builds a dependency graph from bloque_par relations and finds cycles.

    Args:
        tasks: List of parsed task dicts.

    Returns:
        Set of page_ids that are part of cycles.
    """
    graph: dict[str, list[str]] = {}
    task_ids = {t["page_id"] for t in tasks}

    for task in tasks:
        deps = [d for d in task.get("bloque_par", []) if d in task_ids]
        graph[task["page_id"]] = deps

    in_cycle: set[str] = set()
    visited: set[str] = set()
    rec_stack: set[str] = set()
    path: list[str] = []

    def dfs(node: str) -> bool:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                cycle_start = path.index(neighbor)
                in_cycle.update(path[cycle_start:])
                return True

        path.pop()
        rec_stack.discard(node)
        return False

    for node in graph:
        if node not in visited:
            dfs(node)

    return in_cycle


def select_next_task(notion_pages: list[dict]) -> dict | None:
    """Select the next task to execute from raw Notion page objects.

    Pipeline: parse -> filter eligible -> detect cycles -> resolve deps
    -> sort by priority -> return first.

    Args:
        notion_pages: Raw Notion page objects from query_database.

    Returns:
        Parsed task dict for the next task to execute, or None.
    """
    if not notion_pages:
        return None

    all_tasks = [parse_task(page) for page in notion_pages]

    circular_ids = detect_circular_dependencies(all_tasks)

    eligible = get_eligible_tasks(all_tasks)

    eligible = [t for t in eligible if t["page_id"] not in circular_ids]

    unblocked = resolve_dependencies(eligible, all_tasks)

    if not unblocked:
        return None

    sorted_tasks = sort_by_priority(unblocked)
    return sorted_tasks[0]
