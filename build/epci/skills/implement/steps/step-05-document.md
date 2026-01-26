---
name: step-05-document
description: Documentation update phase
prev_step: steps/step-04-review.md
next_step: steps/step-06-finish.md
---

# Step 05: Document

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER skip Feature Document update
- 🔴 NEVER leave outdated documentation
- ✅ ALWAYS complete Feature Document
- ✅ ALWAYS update related docs if affected
- ✅ ALWAYS document breaking changes
- 🔵 YOU ARE A DOCUMENTOR ensuring future maintainability
- 💭 FOCUS on what the next developer needs to know

## EXECUTION PROTOCOLS:

1. **Complete** Feature Document
   - Update status to COMPLETED
   - Add final implementation details
   - Record test coverage achieved
   - Document any deviations from plan

2. **Update** related documentation
   - API docs if endpoints changed
   - README if usage changed
   - CHANGELOG if significant
   - Architecture docs if structure changed

3. **Document** breaking changes
   - Migration steps if needed
   - Deprecated code notices
   - Compatibility notes

4. **Review** documentation quality
   - Clear and concise
   - Code examples where helpful
   - No outdated references

## CONTEXT BOUNDARIES:

- This step expects: Reviewed and approved code
- This step produces: Complete Feature Document, updated related docs

## FEATURE DOCUMENT TEMPLATE:

```markdown
# Feature: {feature-slug}

## Status: COMPLETED

## Overview
{Brief description of what this feature does}

## Implementation Details

### Architecture
{Key architectural decisions}

### Components
| Component | File | Purpose |
|-----------|------|---------|
| {name} | {path} | {purpose} |

### Dependencies
- {dependency 1}
- {dependency 2}

## Testing

### Coverage
- Unit: {%}
- Integration: {%}

### Key Test Cases
- {test case 1}
- {test case 2}

## Usage

### Example
```{language}
{usage example}
```

## Changelog
- {date}: Initial implementation

## Related Docs
- {link to related doc 1}
- {link to related doc 2}
```

## OUTPUT FORMAT:

```
## Documentation Complete

### Feature Document
- Location: `.epci/features/{feature-slug}/FEATURE.md`
- Status: COMPLETED

### Updated Docs
- {doc 1}: {changes}
- {doc 2}: {changes}

### Breaking Changes
{none | list of changes with migration steps}
```

## NEXT STEP TRIGGER:

When documentation is complete, proceed to `step-06-finish.md`.
