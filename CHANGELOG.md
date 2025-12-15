# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **F02: Système de Hooks** - Extensibility system for EPCI workflow with:
  - 7 hook points: pre/post-phase-1/2/3, on-breakpoint
  - Python runner (`hooks/runner.py`) with subprocess execution, timeout, JSON I/O
  - Safe interpreter whitelist for shebang security
  - 3 example hooks: linter, notification, logging
  - Full documentation in `hooks/README.md`
  - Integration with `/epci` command at all phase transitions

- **F03: Enriched Breakpoints** - Enhanced `/epci` workflow breakpoints with:
  - Complexity scoring algorithm (files×0.3 + LOC×0.3 + deps×0.2 + risk×0.2)
  - Time estimation heuristics (TINY=15min, SMALL=1h, STANDARD=3h, LARGE=8h+)
  - Agent verdict summaries with clear status indicators
  - Preview of next phase tasks (3-5 upcoming tasks displayed)
  - Interactive options with guided text instructions
  - ASCII-art formatted breakpoint displays for terminal readability
  - New `breakpoint-metrics` skill with BP1/BP2 templates
  - Integration with both Phase 1→2 and Phase 2→3 breakpoints

### Changed

- Enhanced `/epci` command breakpoints from simple text prompts to comprehensive decision dashboards
- Updated `epci-core` skill with new "Breakpoint Format" section documenting enriched breakpoint structure
- Improved breakpoint user experience with metrics-driven decision support

### Technical Details

- Added `src/skills/core/breakpoint-metrics/SKILL.md` with scoring algorithms and time estimation logic
- Added breakpoint templates: `bp1-template.md` (Post-Phase 1) and `bp2-template.md` (Post-Phase 2)
- Modified `/epci` command to invoke `breakpoint-metrics` skill at BP1 and BP2 checkpoints
- All changes maintain backward compatibility with existing `/epci` workflow

## [3.0.0] - 2024-12

### Added

- Complete rewrite from v2.7 to v3.0 with simplified architecture
- 5 core commands: `/epci-brief`, `/epci`, `/epci-quick`, `/epci-spike`, `/epci:create`
- 5 custom subagents: plan-validator, code-reviewer, security-auditor, qa-reviewer, doc-generator
- 13 skills system: 5 core, 4 stack-specific, 4 factory skills
- Component Factory system for creating new skills, commands, and agents
- Feature Document pattern for STANDARD/LARGE features
- Unified entry point via `/epci-brief` with intelligent routing

### Changed

- Simplified from 12 commands to 5 commands
- Consolidated routing from 5 levels to 3 workflows
- Replaced custom flags/personas with native Claude Code features
- Enhanced subagent integration with conditional activation

### Removed

- v2.7 commands: epci-discover, epci-0-briefing, epci-micro, epci-soft, epci-hotfix
- Custom flags and personas systems (replaced by native Claude Code)
- Pre-stage workflows (integrated into epci-brief)

### Migration

- `epci-discover` → `epci-brief`
- `epci-0-briefing` → `epci-brief`
- `epci-micro` → `epci-quick` (TINY mode)
- `epci-soft` → `epci-quick` (SMALL mode)
- `epci-1-analyse` → `epci` Phase 1
- `epci-2-code` → `epci` Phase 2
- `epci-3-finalize` → `epci` Phase 3