# Step 07: Validate

> Validate brief section by section before final generation.

## Trigger

- Previous step: `step-06-preview.md` completed
- `--quick` flag: Skip this step

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `brief_v0` | Session state | Yes |
| `decisions[]` | Session state | Yes |
| `ems` | Session state | Yes |
| `complexity_estimate` | From step-06 | Yes |
| `security_audit` | From step-06 | No |
| `--quick` flag | From step-00 | No |

## Protocol

### 1. Check Quick Mode

```
IF --quick flag:
  → Skip validation, proceed to step-08-generate.md
  → Log: "Validation skipped (--quick mode)"
```

### 2. Prepare Brief Sections

Structure brief into validatable sections:

```markdown
## Brief Sections

### 1. Executive Summary
{one-paragraph overview}

### 2. Problem Statement
{what problem this solves}

### 3. Proposed Solution
{high-level approach}

### 4. Scope
- In scope: {...}
- Out of scope: {...}

### 5. Requirements
- Functional: {...}
- Non-functional: {...}

### 6. Constraints
{technical, business, timeline}

### 7. Success Criteria
{measurable outcomes}

### 8. Implementation Notes
- Complexity: {estimate}
- Security: {notes if any}
- Dependencies: {...}
```

### 3. BREAKPOINT: Section-by-Section Validation

For each major section (unless --quick):

```typescript
@skill:epci:breakpoint-system
  type: validation
  title: "Validate: {section_name}"
  data: {
    section: "{section_name}",
    content: "{section_content}",
    source: "{decisions that informed this section}",
    confidence: "{HIGH|MEDIUM|LOW}"
  }
  ask: {
    question: "Is this {section_name} accurate?",
    header: "{section}",
    options: [
      {label: "Approve", description: "Section is correct"},
      {label: "Edit", description: "Make changes"},
      {label: "Skip remaining", description: "Auto-approve rest"}
    ]
  }
```

Sections to validate (in order):
1. Executive Summary
2. Problem Statement
3. Proposed Solution
4. Scope
5. Requirements (if complex)
6. Success Criteria

### 4. Handle Edits

```
IF user edits a section:
  - Record original and edited version
  - Update brief_v0 with changes
  - Note in journal: "User edited {section}"
  - Continue to next section
```

### 5. Handle Skip Remaining

```
IF "Skip remaining" selected:
  - Auto-approve remaining sections
  - Note in journal: "Remaining sections auto-approved"
  - Proceed to generation
```

### 6. Compile Validation Summary

```markdown
## Validation Summary

| Section | Status | Notes |
|---------|--------|-------|
| Executive Summary | Approved | - |
| Problem Statement | Edited | {change summary} |
| Proposed Solution | Approved | - |
| Scope | Approved | - |
| Requirements | Auto-approved | Skipped |
| Success Criteria | Auto-approved | Skipped |

**Sections validated**: 4/6
**Sections edited**: 1
**Sections auto-approved**: 2
```

### 7. Finalize Brief Content

```json
{
  "validation_complete": true,
  "sections_validated": 4,
  "sections_edited": 1,
  "sections_auto_approved": 2,
  "brief_final": "{compiled validated brief}",
  "edit_history": [
    {
      "section": "Problem Statement",
      "original": "...",
      "edited": "...",
      "reason": "User correction"
    }
  ]
}
```

## Outputs

| Output | Destination |
|--------|-------------|
| `validation_complete` | Session state |
| `brief_final` | Session state |
| `edit_history` | Session state |
| Validation summary | Session state |

## Next Step

→ `step-08-generate.md`

## Error Handling

| Error | Resolution |
|-------|------------|
| User abandons validation | Offer to save checkpoint |
| Too many edits (> 3) | Suggest returning to iteration |
| Conflicting edits | Highlight conflict, ask to resolve |
