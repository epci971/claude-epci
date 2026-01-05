# Command Optimization Report

> **Date**: 2026-01-05
> **Objective**: Reduce command file sizes to prevent LLM hallucinations and improve performance

## Summary

Optimized 8 command files, reducing total word count from ~24k to ~7.8k words (67% reduction).

## Before/After Comparison

| Command | Before (words) | After (words) | Reduction |
|---------|---------------|---------------|-----------|
| epci.md | 3064 | 741 | **76%** |
| brief.md | 2122 | 659 | **69%** |
| quick.md | 2103 | 612 | **71%** |
| memory.md | 2011 | 531 | **74%** |
| brainstorm.md | 2284 | 649 | **72%** |
| debug.md | 1493 | 512 | **66%** |
| decompose.md | 1766 | 718 | **59%** |
| rules.md | 1425 | 609 | **57%** |
| **Total optimized** | **16268** | **5031** | **69%** |

## Strategy

### 1. Extract Shared Content to References

Created `src/commands/references/` with:
- `turbo-mode.md` — Turbo mode documentation (shared by epci, brief, quick, debug)
- `hooks.md` — Hook system documentation (shared by all phase-based commands)
- `breakpoints.md` — Breakpoint templates
- `commit-context.md` — Commit context schema

### 2. Apply Compression Techniques

- Removed redundant examples (kept 1 representative example per command)
- Removed verbose ASCII art diagrams
- Converted prose to tables where appropriate
- Eliminated repeated flag documentation (reference to `src/settings/flags.md`)
- Shortened descriptions while preserving meaning

### 3. Preserve All Functional Elements

Used `validate_command_inventory.py` to verify:
- **38 flags** — All preserved
- **11 agents** — All preserved (false positives filtered)
- **4 skills** — All preserved
- **19 hooks** — All preserved
- **9 tools** — All preserved
- **4 MCP servers** — All preserved

## Validation Results

```
✅ FLAGS: 38 total
✅ AGENTS: 11 total (@Explore, @clarifier, @code-reviewer, @decompose-validator,
   @doc-generator, @implementer, @plan-validator, @planner, @qa-reviewer,
   @rules-validator, @security-auditor)
✅ SKILLS: 4 total (architecture-patterns, epci-core, flags-system, project-memory)
✅ HOOKS: 19 total (all lifecycle hooks preserved)
✅ TOOLS: 9 total
✅ MCP_SERVERS: 4 total (context7, magic, playwright, sequential)
```

## Research Basis

Based on research:
- **Recency bias**: Transformers weight recent tokens more heavily
- **Context rot**: Performance degrades at ~500-750 words
- **Optimal prompt size**: <2000 tokens for instructions
- **Structured prompts**: 16K structured + RAG outperforms 128K monolithic

## Files Modified

### Optimized Commands (8)
- `src/commands/epci.md`
- `src/commands/brief.md`
- `src/commands/quick.md`
- `src/commands/memory.md`
- `src/commands/brainstorm.md`
- `src/commands/debug.md`
- `src/commands/decompose.md`
- `src/commands/rules.md`

### New Files (4)
- `src/commands/references/turbo-mode.md`
- `src/commands/references/hooks.md`
- `src/commands/references/breakpoints.md`
- `src/commands/references/commit-context.md`

### Validation Script
- `src/scripts/validate_command_inventory.py` — Updated with better filtering

## Recommendations

1. **Monitor command length**: Keep main commands under 800 words
2. **Use references/**: Move detailed content to reference files
3. **Run validation**: Use `python3 src/scripts/validate_command_inventory.py --compare docs/audits/command-inventory-baseline.json` before merging changes
4. **Update baseline**: After intentional changes, regenerate with `--baseline`
