"""
MCP Activation Matrix (F12)

Defines the Persona × MCP mapping as specified in CDC-F12 Section 6.
Each persona has preferred MCP servers for enhanced context.
"""

from typing import Dict, List, Optional, Tuple


# Persona × MCP Mapping from CDC-F12 Section 6
# Key: persona name
# Value: tuple of (primary_mcp, secondary_mcp or None)
PERSONA_MCP_MAPPING: Dict[str, Tuple[str, Optional[str]]] = {
    "architect": ("context7", "sequential"),
    "frontend": ("magic", "playwright"),
    "backend": ("context7", "sequential"),
    "security": ("sequential", None),
    "qa": ("playwright", None),
    "doc": ("context7", None),
}


# Auto-activation matrix (True = auto-activated with persona)
# From CDC-F12 Section 6: ● = Auto-activé, ○ = Disponible sur demande
PERSONA_AUTO_ACTIVATION: Dict[str, Dict[str, bool]] = {
    "architect": {"context7": True, "sequential": True, "magic": False, "playwright": False},
    "frontend": {"context7": True, "sequential": False, "magic": True, "playwright": True},
    "backend": {"context7": True, "sequential": True, "magic": False, "playwright": False},
    "security": {"context7": False, "sequential": True, "magic": False, "playwright": False},
    "qa": {"context7": False, "sequential": False, "magic": False, "playwright": True},
    "doc": {"context7": True, "sequential": False, "magic": False, "playwright": False},
}


# MCP trigger keywords (from CDC-F12 Section 3)
MCP_TRIGGER_KEYWORDS: Dict[str, List[str]] = {
    "context7": [
        "import", "require", "use", "library", "framework",
        "documentation", "docs", "api", "package", "dependency",
    ],
    "sequential": [
        "debug", "analyze", "investigate", "complex", "think",
        "reason", "step", "systematic", "diagnose", "trace",
    ],
    "magic": [
        "component", "button", "form", "modal", "table",
        "ui", "interface", "design", "layout", "widget",
    ],
    "playwright": [
        "e2e", "browser", "accessibility", "test", "automation",
        "screenshot", "click", "navigate", "a11y", "wcag",
    ],
}


# MCP trigger file patterns (from CDC-F12 Section 3)
MCP_TRIGGER_FILES: Dict[str, List[str]] = {
    "context7": [
        "package.json", "composer.json", "requirements.txt",
        "pyproject.toml", "pom.xml", "build.gradle", "Cargo.toml",
    ],
    "sequential": [],  # No file triggers, only flags
    "magic": [
        "*.jsx", "*.tsx", "*.vue", "*.svelte",
        "**/components/**", "**/ui/**",
    ],
    "playwright": [
        "*.spec.ts", "*.e2e.ts", "*.test.ts",
        "**/tests/**", "**/e2e/**",
    ],
}


# MCP trigger flags
MCP_TRIGGER_FLAGS: Dict[str, List[str]] = {
    "context7": [],  # No specific flags
    "sequential": ["--think-hard", "--ultrathink"],
    "magic": ["--persona-frontend"],
    "playwright": ["--persona-qa"],
}


def get_mcps_for_persona(persona_name: str) -> List[str]:
    """
    Get list of MCP servers to activate for a given persona.

    Args:
        persona_name: Name of the persona (e.g., "architect", "frontend")

    Returns:
        List of MCP server names to activate (primary first, then secondary if exists)
    """
    if persona_name not in PERSONA_MCP_MAPPING:
        return []

    primary, secondary = PERSONA_MCP_MAPPING[persona_name]
    result = [primary]
    if secondary:
        result.append(secondary)
    return result


def get_auto_activated_mcps(persona_name: str) -> List[str]:
    """
    Get list of MCPs that should be auto-activated for a persona.

    Only returns MCPs marked with ● (auto) in the matrix, not ○ (on-demand).

    Args:
        persona_name: Name of the persona

    Returns:
        List of auto-activated MCP server names
    """
    if persona_name not in PERSONA_AUTO_ACTIVATION:
        return []

    return [
        mcp_name
        for mcp_name, auto in PERSONA_AUTO_ACTIVATION[persona_name].items()
        if auto
    ]


def get_suggested_mcps(persona_name: str) -> List[str]:
    """
    Get list of MCPs that should be suggested (not auto-activated) for a persona.

    Returns MCPs marked with ○ (on-demand) in the matrix.

    Args:
        persona_name: Name of the persona

    Returns:
        List of suggested MCP server names
    """
    if persona_name not in PERSONA_AUTO_ACTIVATION:
        return []

    return [
        mcp_name
        for mcp_name, auto in PERSONA_AUTO_ACTIVATION[persona_name].items()
        if not auto
    ]


def check_keyword_triggers(text: str) -> Dict[str, float]:
    """
    Check text for MCP trigger keywords and return scores.

    Args:
        text: Text to analyze (e.g., brief content)

    Returns:
        Dictionary mapping MCP name to score (0.0-1.0)
    """
    text_lower = text.lower()
    scores = {}

    for mcp_name, keywords in MCP_TRIGGER_KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw in text_lower)
        # Score is min(1.0, matches / 3) following F09 pattern
        scores[mcp_name] = min(1.0, matches / 3)

    return scores


def check_file_triggers(file_paths: List[str]) -> Dict[str, bool]:
    """
    Check file paths for MCP triggers.

    Args:
        file_paths: List of file paths to check

    Returns:
        Dictionary mapping MCP name to whether it's triggered
    """
    import fnmatch

    triggered = {mcp: False for mcp in MCP_TRIGGER_FILES}

    for file_path in file_paths:
        file_lower = file_path.lower()
        for mcp_name, patterns in MCP_TRIGGER_FILES.items():
            for pattern in patterns:
                if fnmatch.fnmatch(file_lower, pattern.lower()):
                    triggered[mcp_name] = True
                    break

    return triggered


def check_flag_triggers(flags: List[str]) -> Dict[str, bool]:
    """
    Check flags for MCP triggers.

    Args:
        flags: List of active flags (e.g., ["--think-hard", "--safe"])

    Returns:
        Dictionary mapping MCP name to whether it's triggered
    """
    triggered = {mcp: False for mcp in MCP_TRIGGER_FLAGS}

    for mcp_name, trigger_flags in MCP_TRIGGER_FLAGS.items():
        for flag in flags:
            if flag in trigger_flags:
                triggered[mcp_name] = True
                break

    return triggered
