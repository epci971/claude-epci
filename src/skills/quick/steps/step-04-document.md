---
name: step-04-document
description: Conditionally update CHANGELOG/README if visible feature change
prev_step: steps/step-03-code.md
next_step: steps/step-05-memory.md
---

# Step 04: Document [D] (Conditional)

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER create Feature Documents (that's /implement's job)
- :red_circle: NEVER over-document small changes
- :white_check_mark: ALWAYS evaluate if documentation update is needed
- :white_check_mark: ALWAYS follow existing doc conventions
- :thought_balloon: FOCUS on minimal documentation - only if truly needed

## EXECUTION PROTOCOLS:

### 1. Evaluate Documentation Need

Check if change warrants documentation:

```python
def should_update_docs(plan_objective: str, files_modified: list) -> bool:
    """Determine if documentation update is needed."""

    # Keywords indicating visible change
    visible_keywords = ["feature", "add", "new", "change", "breaking", "api"]

    # Keywords indicating internal change (skip docs)
    internal_keywords = ["fix", "bug", "refactor", "internal", "typo"]

    objective_lower = plan_objective.lower()

    # If clearly internal → skip
    if any(kw in objective_lower for kw in internal_keywords):
        if not any(kw in objective_lower for kw in visible_keywords):
            return False

    # If any visible keyword → update
    return any(kw in objective_lower for kw in visible_keywords)
```

### 2. Decision Matrix

| Change Type | CHANGELOG | README | Notes |
|-------------|-----------|--------|-------|
| New feature | Yes | If API change | Add under "Added" |
| Bug fix (internal) | No | No | Skip docs |
| Bug fix (user-facing) | Optional | No | "Fixed" section |
| API change | Yes | Yes | Breaking change note |
| Refactor | No | No | Skip docs |
| Performance | Optional | No | "Changed" section |

### 3. Update CHANGELOG (if needed)

If CHANGELOG exists and update warranted:

```markdown
## [Unreleased]

### Added
- {Description of new feature}

### Fixed
- {Description of bug fix}

### Changed
- {Description of change}
```

**Rules:**
- Add to "Unreleased" section
- Use present tense
- One line per change
- Reference issue if applicable

### 4. Update README (if needed)

Only update README if:
- New public API added
- Usage pattern changed
- Breaking change introduced

**Typically skip for /quick tasks.**

### 5. Skip Documentation

If no update needed, log decision:

```
DOCUMENTATION: SKIPPED

Reason: {internal fix | no visible change | refactor only}
```

## CONTEXT BOUNDARIES:

- This step expects: Implementation complete from step-03
- This step produces: Updated docs (if needed) or skip decision
- Time budget: < 5 seconds decision, < 10 seconds if updating

## OUTPUT FORMAT:

### If Updated:
```
## Documentation Updated

CHANGELOG: Updated (Added: {description})
README: Skipped (no API change)
```

### If Skipped:
```
## Documentation Skipped

Reason: Internal fix, no user-visible change
```

## NEXT STEP TRIGGER:

Proceed to step-05-memory.md regardless of documentation outcome.
