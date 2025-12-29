"""
Wave Context Module (F11)

Provides data structures for wave execution context and accumulation.
Each wave inherits and enriches the context from previous waves.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..mcp.config import MCPContext as MCPContextType


class WaveStatus(Enum):
    """Status of a wave execution."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Issue:
    """Represents an issue found during wave execution."""
    severity: str  # critical, important, minor
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    source: str = ""  # agent name or tool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "severity": self.severity,
            "message": self.message,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "source": self.source,
        }


@dataclass
class Decision:
    """Represents a decision made during wave execution."""
    description: str
    rationale: str
    wave_number: int
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "rationale": self.rationale,
            "wave_number": self.wave_number,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class TaskResult:
    """Result of a single task execution within a wave."""
    task_name: str
    status: str  # completed, failed, skipped
    duration_seconds: float = 0.0
    files_created: List[str] = field(default_factory=list)
    files_modified: List[str] = field(default_factory=list)
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_name": self.task_name,
            "status": self.status,
            "duration_seconds": self.duration_seconds,
            "files_created": self.files_created,
            "files_modified": self.files_modified,
            "error": self.error,
        }


@dataclass
class Wave:
    """Represents a single wave in the orchestration."""
    wave_id: str
    name: str
    order: int
    tasks: List[str] = field(default_factory=list)
    status: WaveStatus = WaveStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    task_results: List[TaskResult] = field(default_factory=list)

    @property
    def duration_seconds(self) -> float:
        """Calculate wave duration."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return 0.0

    @property
    def is_complete(self) -> bool:
        return self.status == WaveStatus.COMPLETED

    @property
    def is_failed(self) -> bool:
        return self.status == WaveStatus.FAILED

    def to_dict(self) -> Dict[str, Any]:
        return {
            "wave_id": self.wave_id,
            "name": self.name,
            "order": self.order,
            "tasks": self.tasks,
            "status": self.status.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": self.duration_seconds,
            "task_results": [r.to_dict() for r in self.task_results],
        }


@dataclass
class WaveContext:
    """
    Accumulated context across wave executions.

    Each wave inherits the context from previous waves and can add
    new information. This enables progressive context enrichment.
    """
    wave_number: int = 0
    files_created: List[str] = field(default_factory=list)
    files_modified: List[str] = field(default_factory=list)
    patterns_used: List[str] = field(default_factory=list)
    tests_status: Dict[str, str] = field(default_factory=dict)
    issues_found: List[Issue] = field(default_factory=list)
    decisions_made: List[Decision] = field(default_factory=list)
    agent_results: Dict[str, Any] = field(default_factory=dict)

    # Metadata
    feature_slug: str = ""
    complexity: str = ""
    started_at: Optional[datetime] = None

    # MCP Context (F12)
    mcp_context: Optional[Any] = None  # MCPContext from src/mcp/config.py
    mcp_servers_used: List[str] = field(default_factory=list)

    def add_file_created(self, file_path: str) -> None:
        """Add a created file to the context."""
        if file_path not in self.files_created:
            self.files_created.append(file_path)

    def add_file_modified(self, file_path: str) -> None:
        """Add a modified file to the context."""
        if file_path not in self.files_modified:
            self.files_modified.append(file_path)

    def add_pattern(self, pattern: str) -> None:
        """Record a pattern used during implementation."""
        if pattern not in self.patterns_used:
            self.patterns_used.append(pattern)

    def add_issue(self, issue: Issue) -> None:
        """Add an issue found during execution."""
        self.issues_found.append(issue)

    def add_decision(self, description: str, rationale: str) -> None:
        """Record a decision made during the wave."""
        self.decisions_made.append(Decision(
            description=description,
            rationale=rationale,
            wave_number=self.wave_number,
        ))

    def update_test_status(self, test_name: str, status: str) -> None:
        """Update the status of a test."""
        self.tests_status[test_name] = status

    def store_agent_result(self, agent_name: str, result: Any) -> None:
        """Store the result from an agent execution."""
        self.agent_results[agent_name] = result

    def set_mcp_context(self, mcp_context: Any) -> None:
        """Set the MCP context for this wave (F12)."""
        self.mcp_context = mcp_context

    def record_mcp_usage(self, server_name: str) -> None:
        """Record that an MCP server was used (F12)."""
        if server_name not in self.mcp_servers_used:
            self.mcp_servers_used.append(server_name)

    def get_critical_issues(self) -> List[Issue]:
        """Get all critical issues."""
        return [i for i in self.issues_found if i.severity == "critical"]

    def get_important_issues(self) -> List[Issue]:
        """Get all important issues."""
        return [i for i in self.issues_found if i.severity == "important"]

    def advance_wave(self) -> "WaveContext":
        """
        Create a new context for the next wave, inheriting current state.

        Returns a new WaveContext with incremented wave number and
        all accumulated data preserved.
        """
        return WaveContext(
            wave_number=self.wave_number + 1,
            files_created=self.files_created.copy(),
            files_modified=self.files_modified.copy(),
            patterns_used=self.patterns_used.copy(),
            tests_status=self.tests_status.copy(),
            issues_found=self.issues_found.copy(),
            decisions_made=self.decisions_made.copy(),
            agent_results=self.agent_results.copy(),
            feature_slug=self.feature_slug,
            complexity=self.complexity,
            started_at=self.started_at,
            mcp_context=self.mcp_context,
            mcp_servers_used=self.mcp_servers_used.copy(),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary for serialization."""
        return {
            "wave_number": self.wave_number,
            "files_created": self.files_created,
            "files_modified": self.files_modified,
            "patterns_used": self.patterns_used,
            "tests_status": self.tests_status,
            "issues_found": [i.to_dict() for i in self.issues_found],
            "decisions_made": [d.to_dict() for d in self.decisions_made],
            "agent_results": self.agent_results,
            "feature_slug": self.feature_slug,
            "complexity": self.complexity,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "mcp_context": self.mcp_context.to_dict() if self.mcp_context and hasattr(self.mcp_context, 'to_dict') else None,
            "mcp_servers_used": self.mcp_servers_used,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WaveContext":
        """Create a WaveContext from a dictionary."""
        issues = [
            Issue(**i) for i in data.get("issues_found", [])
        ]
        decisions = [
            Decision(
                description=d["description"],
                rationale=d["rationale"],
                wave_number=d["wave_number"],
                timestamp=datetime.fromisoformat(d["timestamp"]) if d.get("timestamp") else datetime.now(),
            )
            for d in data.get("decisions_made", [])
        ]

        return cls(
            wave_number=data.get("wave_number", 0),
            files_created=data.get("files_created", []),
            files_modified=data.get("files_modified", []),
            patterns_used=data.get("patterns_used", []),
            tests_status=data.get("tests_status", {}),
            issues_found=issues,
            decisions_made=decisions,
            agent_results=data.get("agent_results", {}),
            feature_slug=data.get("feature_slug", ""),
            complexity=data.get("complexity", ""),
            started_at=datetime.fromisoformat(data["started_at"]) if data.get("started_at") else None,
        )

    def summary(self) -> str:
        """Generate a human-readable summary of the context."""
        mcp_info = f"  MCP servers used: {', '.join(self.mcp_servers_used) if self.mcp_servers_used else 'none'}\n" if self.mcp_servers_used else ""
        return (
            f"Wave {self.wave_number} Context:\n"
            f"  Files created: {len(self.files_created)}\n"
            f"  Files modified: {len(self.files_modified)}\n"
            f"  Patterns used: {len(self.patterns_used)}\n"
            f"  Tests: {len(self.tests_status)} ({sum(1 for s in self.tests_status.values() if s == 'passed')} passed)\n"
            f"  Issues: {len(self.issues_found)} ({len(self.get_critical_issues())} critical)\n"
            f"  Decisions: {len(self.decisions_made)}\n"
            f"{mcp_info}"
        ).rstrip()
