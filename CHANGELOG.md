# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.2.3] - 2026-01-15

### Added

- **New agent**: `@statusline-setup` for Claude Code status line configuration

### Changed

- **File references**: Added `@` syntax rule in CLAUDE.md (Section 9)
  - All file references must use `@path` instead of backticks or markdown links
  - Corrected 28 occurrences across 5 command files

### Fixed

- **plugin.json**: Added missing `statusline-setup.md` agent (16 agents total)
- **Subagents count**: Updated from 15 to 16 in CLAUDE.md

## [5.2.0] - 2026-01-15

### Changed

- **Brainstorm v5.2**: Breakpoint display improvements
  - ASCII box format (`┌─ │ ├─ └─`) instead of simple dashes
  - EMS 5-axis visual progress bars (`████████░░`)
  - `[WEAK]` markers on axes < 50
  - EMS progression history visible at checkpoints
  - Mandatory `ems_history` tracking in session_state
  - Journal corrected to use only standard axes

- **References reorganization**: Command-specific subdirectories
  - New structure: `references/brainstorm/`, `references/epci/`, etc.
  - Migrated 16 existing reference files to new structure
  - Created 3 new reference files: commands.md, flags.md, completion-summary.md
  - Changelog consolidated in root CHANGELOG.md

## [5.1.0] - 2026-01-XX

### Changed

- **Brainstorm v5.1**: Native question system
  - AskUserQuestion native tool integration (interactive QCM UI)
  - Maximum 3 questions per iteration (reduced from 5)
  - Priority headers: `🛑 Critical`, `⚠️ Important`, `ℹ️ Info`
  - Visual recommendations: `(Recommended)` in option labels
  - Separated breakpoint: Status as text, questions via AskUserQuestion
  - @technique-advisor returns JSON, main thread handles display

## [5.0.0] - 2026-01-XX

### Added

- **Brainstorm v5.0**: PRD Industry Standards v3.0
  - Executive Summary, Problem Statement, Goals/Non-Goals sections
  - Timeline & Milestones, FAQ, Assumptions, Appendix sections
  - `--competitive` flag for Competitive Analysis section
  - Finalization Checkpoint lowered to EMS >= 70 (blocking)
  - No automatic finalization — always requires explicit user choice

## [4.9.0] - 2026-01-XX

### Changed

- **Brainstorm v4.9**: Finalization Checkpoint
  - Mandatory checkpoint at EMS >= 85 (blocking)
  - No automatic finalization — explicit user choice required

## [4.8.0] - 2026-01-XX

### Added

- **Brainstorm v4.8**: Auto-technique system
  - Auto-selection of techniques based on weak EMS axes (< 50)
  - Mix of techniques when 2+ axes weak
  - Explicit transition check Divergent → Convergent
  - Preview @planner/@security in Convergent phase
  - Post-brainstorm hook documented

## [4.7.0] - 2026-01-06

### Added

- **Brainstorm v4.3 Optimization**: Major performance refactoring
  - 6 new reference files in `src/commands/references/` for modular documentation
  - 2 new Haiku agents: `@ems-evaluator` (EMS scoring), `@technique-advisor` (technique selection)
  - New brainstorm modes: `--random`, `--progressive`
  - Integrated spike process via `spike [duration] [question]` command
  - Session commands: `status`, `technique`, `finish`, `batch`
  - Energy checkpoints with automatic EMS evaluation

### Changed

- **Refactored `/brainstorm` command**: 949 → 164 lines (-83% tokens)
- **Refactored `brainstormer` skill**: 387 → 193 lines (-50% tokens)
- **Updated subagent count**: 10 → 12 agents (added @ems-evaluator, @technique-advisor)
- Brainstorm documentation externalized into modular reference files

### Technical Details

- New reference files:
  - `brainstorm-turbo-mode.md` - Turbo mode with @clarifier
  - `brainstorm-random-mode.md` - Random technique selection
  - `brainstorm-progressive-mode.md` - Progressive disclosure pattern
  - `brainstorm-spike-process.md` - Integrated spike exploration
  - `brainstorm-session-commands.md` - Session command reference
  - `brainstorm-energy-checkpoints.md` - EMS checkpoint system
- Agent allocation: Haiku for fast scoring/selection, preserves Opus budget
- Maintained backward compatibility with existing brainstorm flags

## [4.2.0] - 2024-12-31

### Changed

- **Command Renaming**: Removed redundant `epci-` prefix from all commands
    - `/epci:epci-brief` → `/epci:brief`
    - `/epci:epci-quick` → `/epci:quick`
    - `/epci:epci-spike` → `/epci:spike`
    - `/epci:epci-debug` → `/epci:debug`
    - `/epci:epci-decompose` → `/epci:decompose`
    - `/epci:epci-memory` → `/epci:memory`
    - `/epci:epci-learn` → `/epci:learn`
- Updated all internal references in commands, agents, skills, hooks, and documentation
- Maintained `/epci:epci` as the main workflow command (unchanged)
- Maintained `/epci:brainstorm` and `/epci:create` (already without prefix)

### Technical Details

- Renamed 7 command files in `src/commands/`
- Updated `plugin.json` with new command paths
- Updated all cross-references in 9 agent files, 15+ skill files, 4 hook files
- Updated `CLAUDE.md`, `README.md`, and `src/settings/flags.md`
- Version bumped to 4.2.0

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
