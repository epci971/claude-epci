#!/usr/bin/env python3
"""
EPCI Deployment Script

Copies src/ to build/epci/, validates structure, and checks version consistency.

Usage:
    python deploy.py [--dry-run] [--force] [--verbose]

Exit Codes:
    0: Success
    1: Validation failed
    2: Copy failed
    3: Version mismatch
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

# ANSI color codes for console output
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


# Patterns to exclude from copy
EXCLUDE_PATTERNS = [
    "__pycache__",
    "*.pyc",
    "tests",
    ".pytest_cache",
    "*.egg-info",
]


def log(msg: str, color: str = "", verbose: bool = True) -> None:
    """Print colored log message."""
    if verbose:
        print(f"{color}{msg}{Colors.RESET}")


def make_ignore_patterns():
    """Create ignore function for shutil.copytree."""
    def ignore_patterns(directory: str, files: list[str]) -> set[str]:
        ignored = set()
        for pattern in EXCLUDE_PATTERNS:
            if "*" in pattern:
                # Wildcard pattern (e.g., *.pyc)
                suffix = pattern.replace("*", "")
                for f in files:
                    if f.endswith(suffix):
                        ignored.add(f)
            else:
                # Exact match (e.g., __pycache__, tests)
                if pattern in files:
                    ignored.add(pattern)
        return ignored
    return ignore_patterns


def copy_tree_safe(src: Path, dst: Path, *, force: bool = False, dry_run: bool = False, verbose: bool = True) -> None:
    """
    Copy source directory to destination with exclusions.

    Args:
        src: Source directory path
        dst: Destination directory path
        force: If True, overwrite existing destination
        dry_run: If True, only simulate the copy
        verbose: If True, print progress messages

    Raises:
        ValueError: If source doesn't exist or isn't a directory
        FileExistsError: If destination exists and force=False
    """
    if not src.exists() or not src.is_dir():
        raise ValueError(f"Source '{src}' is not a valid directory")

    if dst.exists() and not force:
        raise FileExistsError(
            f"Destination '{dst}' already exists. Use --force to overwrite."
        )

    if dry_run:
        log(f"[DRY-RUN] Would copy {src} -> {dst}", Colors.BLUE, verbose)
        log(f"[DRY-RUN] Would exclude: {EXCLUDE_PATTERNS}", Colors.BLUE, verbose)
        return

    # Remove existing destination if force
    if dst.exists() and force:
        log(f"Removing existing {dst}...", Colors.YELLOW, verbose)
        shutil.rmtree(dst)

    log(f"Copying {src} -> {dst}...", Colors.BLUE, verbose)
    shutil.copytree(src, dst, ignore=make_ignore_patterns())
    log(f"Copy complete.", Colors.GREEN, verbose)


def validate_destination(dst: Path, verbose: bool = True) -> list[str]:
    """
    Validate the copied destination using validate.py functions.

    Args:
        dst: Destination directory to validate

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    # Import validation functions from validate.py
    script_dir = Path(__file__).parent
    sys.path.insert(0, str(script_dir))

    try:
        from validate import validate_plugin_json, validate_skill
    except ImportError:
        errors.append("Could not import validation functions from validate.py")
        return errors

    # Validate plugin.json
    plugin_path = dst / ".claude-plugin" / "plugin.json"
    plugin_errors = validate_plugin_json(plugin_path)
    errors.extend(plugin_errors)

    # Validate skills
    skills_dir = dst / "skills"
    if skills_dir.exists():
        for skill_dir in sorted(skills_dir.iterdir()):
            if skill_dir.is_dir():
                skill_path = skill_dir / "SKILL.md"
                if skill_path.exists():
                    skill_errors = validate_skill(skill_path)
                    errors.extend(skill_errors)
                # Check nested skills (core/, stack/)
                for nested_dir in sorted(skill_dir.iterdir()):
                    if nested_dir.is_dir():
                        nested_skill_path = nested_dir / "SKILL.md"
                        if nested_skill_path.exists():
                            nested_errors = validate_skill(nested_skill_path)
                            errors.extend(nested_errors)

    return errors


def check_version_consistency(src: Path, verbose: bool = True) -> list[str]:
    """
    Check version consistency across plugin.json, README.md, and CHANGELOG.md.

    Args:
        src: Source directory containing the files

    Returns:
        List of version mismatch errors (empty if consistent)
    """
    errors = []

    # Get version from plugin.json (source of truth)
    plugin_path = src / ".claude-plugin" / "plugin.json"
    if not plugin_path.exists():
        errors.append("plugin.json not found for version check")
        return errors

    try:
        with open(plugin_path) as f:
            plugin_data = json.load(f)
        plugin_version = plugin_data.get("version", "")
    except (json.JSONDecodeError, KeyError) as e:
        errors.append(f"Could not read version from plugin.json: {e}")
        return errors

    log(f"Plugin version: {plugin_version}", Colors.BLUE, verbose)

    # Check README.md (in project root, one level up from src)
    project_root = src.parent
    readme_path = project_root / "README.md"
    if readme_path.exists():
        readme_content = readme_path.read_text()
        # Look for version pattern like "Version : 6.0.0" or "**Version**: 6.0.0"
        version_patterns = [
            r"\*\*Version\*\*\s*[:=]\s*(\d+\.\d+\.\d+)",
            r"Version\s*[:=]\s*(\d+\.\d+\.\d+)",
            r"v(\d+\.\d+\.\d+)",
        ]
        readme_version = None
        for pattern in version_patterns:
            match = re.search(pattern, readme_content, re.IGNORECASE)
            if match:
                readme_version = match.group(1)
                break

        if readme_version and readme_version != plugin_version:
            errors.append(
                f"Version mismatch: plugin.json={plugin_version}, README.md={readme_version}"
            )
            log(f"README version: {readme_version} (MISMATCH)", Colors.RED, verbose)
        elif readme_version:
            log(f"README version: {readme_version} (OK)", Colors.GREEN, verbose)
        else:
            log("README version: not found (skipping)", Colors.YELLOW, verbose)

    return errors


def rollback(dst: Path, verbose: bool = True) -> None:
    """Remove destination directory after failed validation."""
    if dst.exists():
        log(f"Rolling back: removing {dst}...", Colors.RED, verbose)
        shutil.rmtree(dst)
        log("Rollback complete.", Colors.YELLOW, verbose)


def deploy(
    src: Path,
    dest: Path,
    *,
    dry_run: bool = False,
    force: bool = False,
    verbose: bool = True,
    skip_version_check: bool = False,
) -> int:
    """
    Main deployment function.

    Args:
        src: Source directory (src/)
        dest: Destination directory (build/epci/)
        dry_run: If True, only simulate actions
        force: If True, overwrite existing destination
        verbose: If True, print progress messages
        skip_version_check: If True, skip version consistency check

    Returns:
        Exit code (0=success, 1=validation failed, 2=copy failed, 3=version mismatch)
    """
    log(f"\n{Colors.BOLD}EPCI Deployment Script{Colors.RESET}", verbose=verbose)
    log("=" * 50, verbose=verbose)

    # Check version consistency first (on source)
    if not skip_version_check and not dry_run:
        log("\n[1/3] Checking version consistency...", Colors.BLUE, verbose)
        version_errors = check_version_consistency(src, verbose)
        if version_errors:
            for err in version_errors:
                log(f"  ERROR: {err}", Colors.RED, verbose)
            log("\nVersion mismatch detected. Use --skip-version-check to override.", Colors.YELLOW, verbose)
            return 3
        log("  Version check passed.", Colors.GREEN, verbose)
    elif dry_run:
        log("\n[1/3] [DRY-RUN] Would check version consistency", Colors.BLUE, verbose)

    # Copy source to destination
    log("\n[2/3] Copying files...", Colors.BLUE, verbose)
    try:
        copy_tree_safe(src, dest, force=force, dry_run=dry_run, verbose=verbose)
    except (ValueError, FileExistsError) as e:
        log(f"  ERROR: {e}", Colors.RED, verbose)
        return 2

    # Skip validation for dry-run
    if dry_run:
        log("\n[3/3] [DRY-RUN] Would validate destination", Colors.BLUE, verbose)
        log(f"\n{Colors.GREEN}[DRY-RUN] Deployment simulation complete.{Colors.RESET}", verbose=verbose)
        return 0

    # Validate destination
    log("\n[3/3] Validating destination...", Colors.BLUE, verbose)
    validation_errors = validate_destination(dest, verbose)
    if validation_errors:
        for err in validation_errors:
            log(f"  ERROR: {err}", Colors.RED, verbose)
        log("\nValidation failed. Rolling back...", Colors.RED, verbose)
        rollback(dest, verbose)
        return 1

    log("  Validation passed.", Colors.GREEN, verbose)
    log(f"\n{Colors.GREEN}{Colors.BOLD}Deployment complete!{Colors.RESET}", verbose=verbose)
    log(f"  Source: {src}", verbose=verbose)
    log(f"  Destination: {dest}", verbose=verbose)

    return 0


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="EPCI Deployment Script - Copy and validate src/ to build/epci/"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate deployment without making changes",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing destination",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        default=True,
        help="Enable verbose output (default: True)",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Disable verbose output",
    )
    parser.add_argument(
        "--skip-version-check",
        action="store_true",
        help="Skip version consistency check",
    )
    parser.add_argument(
        "--src",
        type=Path,
        default=None,
        help="Source directory (default: src/ relative to script)",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=None,
        help="Destination directory (default: build/epci/ relative to project root)",
    )

    args = parser.parse_args()

    # Determine paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent  # src/scripts -> src -> project_root

    src = args.src or (project_root / "src")
    dest = args.dest or (project_root / "build" / "epci")

    verbose = not args.quiet

    return deploy(
        src=src,
        dest=dest,
        dry_run=args.dry_run,
        force=args.force,
        verbose=verbose,
        skip_version_check=args.skip_version_check,
    )


if __name__ == "__main__":
    sys.exit(main())
