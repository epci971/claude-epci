#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Hook Runner - Executes hooks at workflow checkpoints.

This module provides the infrastructure for running user-defined hooks
at specific points in the EPCI workflow (pre/post phases, breakpoints).

Usage:
    python runner.py <hook-type> [--context <json>] [--timeout <seconds>]

    # Example:
    python runner.py pre-phase-2 --context '{"phase": "phase-2", "feature_slug": "auth"}'

Hook Types:
    - pre-phase-1, post-phase-1
    - pre-phase-2, post-phase-2
    - pre-phase-3, post-phase-3
    - on-breakpoint
"""

import sys
import os
import json
import argparse
import subprocess
import stat
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


# =============================================================================
# DATACLASSES
# =============================================================================

@dataclass
class HookConfig:
    """Configuration for hook execution."""
    enabled: bool = True
    timeout_seconds: int = 30
    fail_on_error: bool = False
    active_hooks: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> 'HookConfig':
        """Create config from dictionary."""
        return cls(
            enabled=data.get('enabled', True),
            timeout_seconds=data.get('timeout_seconds', 30),
            fail_on_error=data.get('fail_on_error', False),
            active_hooks=data.get('active', [])
        )


@dataclass
class HookContext:
    """Context passed to hooks via stdin."""
    phase: str
    hook_type: str = ""
    feature_slug: str = ""
    files_modified: List[str] = field(default_factory=list)
    test_results: Dict[str, Any] = field(default_factory=dict)
    breakpoint_type: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    # Flags support (v3.1+)
    active_flags: List[str] = field(default_factory=list)
    flag_sources: Dict[str, str] = field(default_factory=dict)  # flag -> "auto"|"explicit"|"alias"
    # Project memory support (v3.5+)
    project_memory: Dict[str, Any] = field(default_factory=dict)  # context, conventions
    detected_stack: str = ""  # php-symfony, javascript-react, etc.
    detected_conventions: Dict[str, Any] = field(default_factory=dict)  # naming, structure
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'phase': self.phase,
            'hook_type': self.hook_type,
            'feature_slug': self.feature_slug,
            'files_modified': self.files_modified,
            'test_results': self.test_results,
            'breakpoint_type': self.breakpoint_type,
            'timestamp': self.timestamp,
            'active_flags': self.active_flags,
            'flag_sources': self.flag_sources,
            'project_memory': self.project_memory,
            'detected_stack': self.detected_stack,
            'detected_conventions': self.detected_conventions,
            **self.extra
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class HookResult:
    """Result from hook execution."""
    hook_name: str
    hook_path: str
    status: str  # success, warning, error, timeout, skipped
    message: str
    duration_ms: int = 0
    raw_output: str = ""
    raw_stderr: str = ""
    exit_code: int = 0

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'hook_name': self.hook_name,
            'hook_path': self.hook_path,
            'status': self.status,
            'message': self.message,
            'duration_ms': self.duration_ms,
            'exit_code': self.exit_code
        }


# =============================================================================
# CONSTANTS
# =============================================================================

VALID_HOOK_TYPES = [
    'pre-phase-1', 'post-phase-1',
    'pre-phase-2', 'post-phase-2',
    'pre-phase-3', 'post-phase-3',
    'on-breakpoint'
]

SUPPORTED_EXTENSIONS = ['.py', '.sh', '.js']


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def get_hooks_dir() -> Path:
    """Get the hooks directory path."""
    # First, try relative to this script
    script_dir = Path(__file__).resolve().parent
    if script_dir.name == 'hooks':
        return script_dir

    # Try to find src/hooks from project root
    current = script_dir
    while current != current.parent:
        hooks_dir = current / 'src' / 'hooks'
        if hooks_dir.exists():
            return hooks_dir
        current = current.parent

    # Fallback to script directory
    return script_dir


def is_executable(path: Path) -> bool:
    """Check if a file is executable (has shebang or known extension)."""
    # Check file extension
    if path.suffix in SUPPORTED_EXTENSIONS:
        return True

    # Check for shebang
    try:
        with open(path, 'r') as f:
            first_line = f.readline()
            return first_line.startswith('#!')
    except (IOError, UnicodeDecodeError):
        return False


def discover_hooks(hooks_dir: Path, hook_type: str) -> List[Path]:
    """
    Discover active hooks for a given type.

    Looks in hooks/active/ directory for files/symlinks matching the hook type.
    Pattern: {hook-type}* (e.g., pre-phase-2-lint.sh, pre-phase-2.py)

    Args:
        hooks_dir: Path to hooks directory
        hook_type: Type of hook to find (e.g., 'pre-phase-2')

    Returns:
        List of paths to matching hook scripts, sorted alphabetically
    """
    active_dir = hooks_dir / 'active'

    if not active_dir.exists():
        return []

    hooks = []

    # Find all files/symlinks starting with hook_type
    for item in active_dir.iterdir():
        # Skip directories and hidden files
        if item.is_dir() or item.name.startswith('.'):
            continue

        # Check if name matches hook type pattern
        # e.g., "pre-phase-2" matches "pre-phase-2.sh", "pre-phase-2-lint.py"
        base_name = item.stem  # filename without extension
        if base_name == hook_type or base_name.startswith(f"{hook_type}-"):
            # Resolve symlinks and check if executable
            resolved = item.resolve() if item.is_symlink() else item
            if resolved.exists() and is_executable(resolved):
                hooks.append(item)

    return sorted(hooks, key=lambda p: p.name)


# Safe interpreters whitelist for shebang parsing
SAFE_INTERPRETERS = {
    'python': sys.executable,
    'python3': sys.executable,
    'bash': '/bin/bash',
    'sh': '/bin/sh',
    'node': 'node',
    'ruby': 'ruby',
    'perl': 'perl',
}


def _get_safe_interpreter(path: Path) -> Optional[str]:
    """
    Parse shebang line and return a safe interpreter if recognized.

    Returns None if shebang is not recognized or file is not readable.
    """
    try:
        with open(path, 'r') as f:
            first_line = f.readline().strip()
            if not first_line.startswith('#!'):
                return None

            # Parse shebang: #!/usr/bin/env python3 or #!/bin/bash
            shebang = first_line[2:].strip()

            # Handle /usr/bin/env style
            if shebang.startswith('/usr/bin/env '):
                interpreter = shebang.split()[1] if len(shebang.split()) > 1 else None
            else:
                # Direct path: /bin/bash -> bash
                interpreter = Path(shebang.split()[0]).name

            if interpreter and interpreter in SAFE_INTERPRETERS:
                return SAFE_INTERPRETERS[interpreter]

            return None
    except (IOError, UnicodeDecodeError):
        return None


def build_context(
    phase: str,
    hook_type: str = "",
    feature_slug: str = "",
    files_modified: List[str] = None,
    test_results: Dict[str, Any] = None,
    breakpoint_type: str = "",
    **extra
) -> HookContext:
    """Build context object for hooks."""
    return HookContext(
        phase=phase,
        hook_type=hook_type,
        feature_slug=feature_slug,
        files_modified=files_modified or [],
        test_results=test_results or {},
        breakpoint_type=breakpoint_type,
        extra=extra
    )


def execute_hook(
    hook_path: Path,
    context: HookContext,
    config: HookConfig
) -> HookResult:
    """
    Execute a single hook with timeout and error handling.

    Args:
        hook_path: Path to hook script
        context: Context to pass via stdin
        config: Execution configuration

    Returns:
        HookResult with status, message, and timing
    """
    hook_name = hook_path.stem
    start_time = datetime.now()

    # Resolve symlink if needed
    resolved_path = hook_path.resolve() if hook_path.is_symlink() else hook_path

    # Determine how to execute based on extension
    # Use explicit interpreters for security (avoid arbitrary shebang execution)
    if resolved_path.suffix == '.py':
        cmd = [sys.executable, str(resolved_path)]
    elif resolved_path.suffix == '.js':
        cmd = ['node', str(resolved_path)]
    elif resolved_path.suffix == '.sh':
        # Explicit bash interpreter for shell scripts
        cmd = ['/bin/bash', str(resolved_path)]
    else:
        # For other files, try to parse shebang and use known interpreters
        interpreter = _get_safe_interpreter(resolved_path)
        if interpreter:
            cmd = [interpreter, str(resolved_path)]
        else:
            # Fallback: execute directly (file must be executable)
            cmd = [str(resolved_path)]

    try:
        # Execute hook with context via stdin
        result = subprocess.run(
            cmd,
            input=context.to_json(),
            capture_output=True,
            text=True,
            timeout=config.timeout_seconds,
            cwd=resolved_path.parent
        )

        duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

        # Parse JSON output if possible
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if result.returncode == 0:
            # Try to parse JSON response
            try:
                output_data = json.loads(stdout) if stdout else {}
                status = output_data.get('status', 'success')
                message = output_data.get('message', 'Hook completed successfully')
            except json.JSONDecodeError:
                status = 'success'
                message = stdout if stdout else 'Hook completed successfully'

            return HookResult(
                hook_name=hook_name,
                hook_path=str(hook_path),
                status=status,
                message=message,
                duration_ms=duration_ms,
                raw_output=stdout,
                raw_stderr=stderr,
                exit_code=result.returncode
            )
        else:
            # Non-zero exit code
            try:
                output_data = json.loads(stdout) if stdout else {}
                message = output_data.get('message', stderr or f'Exit code {result.returncode}')
            except json.JSONDecodeError:
                message = stderr or stdout or f'Exit code {result.returncode}'

            return HookResult(
                hook_name=hook_name,
                hook_path=str(hook_path),
                status='error',
                message=message,
                duration_ms=duration_ms,
                raw_output=stdout,
                raw_stderr=stderr,
                exit_code=result.returncode
            )

    except subprocess.TimeoutExpired:
        duration_ms = config.timeout_seconds * 1000
        return HookResult(
            hook_name=hook_name,
            hook_path=str(hook_path),
            status='timeout',
            message=f'Hook timed out after {config.timeout_seconds}s',
            duration_ms=duration_ms,
            exit_code=-1
        )

    except FileNotFoundError:
        return HookResult(
            hook_name=hook_name,
            hook_path=str(hook_path),
            status='error',
            message=f'Hook file not found: {resolved_path}',
            exit_code=-1
        )

    except PermissionError:
        return HookResult(
            hook_name=hook_name,
            hook_path=str(hook_path),
            status='error',
            message=f'Permission denied executing hook',
            exit_code=-1
        )

    except Exception as e:
        return HookResult(
            hook_name=hook_name,
            hook_path=str(hook_path),
            status='error',
            message=f'Unexpected error: {str(e)}',
            exit_code=-1
        )


def run_hooks(
    hook_type: str,
    context_dict: dict = None,
    config: HookConfig = None
) -> List[HookResult]:
    """
    Run all active hooks for a given type.

    Args:
        hook_type: Type of hook to run (e.g., 'pre-phase-2')
        context_dict: Context dictionary to pass to hooks
        config: Execution configuration (uses defaults if None)

    Returns:
        List of HookResult objects
    """
    if hook_type not in VALID_HOOK_TYPES:
        return [HookResult(
            hook_name='runner',
            hook_path='',
            status='error',
            message=f'Invalid hook type: {hook_type}. Valid types: {", ".join(VALID_HOOK_TYPES)}'
        )]

    config = config or HookConfig()

    if not config.enabled:
        return [HookResult(
            hook_name='runner',
            hook_path='',
            status='skipped',
            message='Hooks are disabled'
        )]

    hooks_dir = get_hooks_dir()
    hooks = discover_hooks(hooks_dir, hook_type)

    if not hooks:
        return []  # No hooks found is not an error

    # Build context
    context_dict = context_dict or {}
    context = build_context(
        phase=context_dict.get('phase', ''),
        hook_type=hook_type,
        feature_slug=context_dict.get('feature_slug', ''),
        files_modified=context_dict.get('files_modified', []),
        test_results=context_dict.get('test_results', {}),
        breakpoint_type=context_dict.get('breakpoint_type', ''),
        **{k: v for k, v in context_dict.items()
           if k not in ['phase', 'feature_slug', 'files_modified', 'test_results', 'breakpoint_type']}
    )

    results = []

    for hook_path in hooks:
        result = execute_hook(hook_path, context, config)
        results.append(result)

        # Stop on error if configured
        if config.fail_on_error and result.status in ('error', 'timeout'):
            break

    return results


def print_results(results: List[HookResult], verbose: bool = False) -> int:
    """
    Print hook execution results.

    Returns:
        Exit code (0 if all success/warning, 1 if any error)
    """
    if not results:
        print("No hooks executed")
        return 0

    has_error = False

    for result in results:
        status_icon = {
            'success': '✅',
            'warning': '⚠️',
            'error': '❌',
            'timeout': '⏱️',
            'skipped': '⏭️'
        }.get(result.status, '❓')

        print(f"{status_icon} [{result.hook_name}] {result.status}: {result.message}")

        if verbose and result.raw_output:
            print(f"   Output: {result.raw_output[:200]}")

        if result.duration_ms > 0:
            print(f"   Duration: {result.duration_ms}ms")

        if result.status in ('error', 'timeout'):
            has_error = True

    return 1 if has_error else 0


# =============================================================================
# CLI
# =============================================================================

def main():
    """CLI entry point for testing hooks."""
    parser = argparse.ArgumentParser(
        description='EPCI Hook Runner - Execute hooks at workflow checkpoints',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Hook Types:
  {', '.join(VALID_HOOK_TYPES)}

Examples:
  # Run pre-phase-2 hooks with context
  python runner.py pre-phase-2 --context '{{"phase": "phase-2", "feature_slug": "auth"}}'

  # Run with custom timeout
  python runner.py post-phase-3 --timeout 60

  # List available hooks
  python runner.py --list
"""
    )

    parser.add_argument(
        'hook_type',
        nargs='?',
        help=f'Hook type to execute. One of: {", ".join(VALID_HOOK_TYPES)}'
    )

    parser.add_argument(
        '--context', '-c',
        type=str,
        default='{}',
        help='JSON context to pass to hooks (default: {})'
    )

    parser.add_argument(
        '--timeout', '-t',
        type=int,
        default=30,
        help='Timeout in seconds (default: 30)'
    )

    parser.add_argument(
        '--fail-on-error', '-f',
        action='store_true',
        help='Stop on first hook error'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )

    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all discovered hooks'
    )

    args = parser.parse_args()

    hooks_dir = get_hooks_dir()

    # List mode
    if args.list:
        print(f"Hooks directory: {hooks_dir}")
        print(f"Active directory: {hooks_dir / 'active'}")
        print()

        for hook_type in VALID_HOOK_TYPES:
            hooks = discover_hooks(hooks_dir, hook_type)
            if hooks:
                print(f"{hook_type}:")
                for h in hooks:
                    target = f" -> {h.resolve()}" if h.is_symlink() else ""
                    print(f"  - {h.name}{target}")
            else:
                print(f"{hook_type}: (none)")
        return 0

    # Require hook type for execution
    if not args.hook_type:
        parser.print_help()
        return 1

    # Parse context
    try:
        context_dict = json.loads(args.context)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON context: {e}")
        return 1

    # Build config
    config = HookConfig(
        timeout_seconds=args.timeout,
        fail_on_error=args.fail_on_error
    )

    # Execute hooks
    results = run_hooks(args.hook_type, context_dict, config)

    # Print results
    return print_results(results, args.verbose)


if __name__ == "__main__":
    sys.exit(main())
