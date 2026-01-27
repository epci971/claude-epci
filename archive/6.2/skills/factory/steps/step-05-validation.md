# Step 05: Validation

> Run 12-point checklist, preview structure, get user approval via BREAKPOINT.

## Trigger

- Completion of step-04-workflow.md

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Session state | All previous steps | Yes |
| Skill name | From step-00 | Yes |
| Description | From step-03 | Yes |
| Structure | From step-02 | Yes |
| Workflow | From step-04 | Yes |

## Protocol

### 1. Run 12-Point Checklist

| # | Check | Required | Status |
|---|-------|----------|--------|
| 1 | `name` is unique and kebab-case | Yes | |
| 2 | `name` length <= 64 characters | Yes | |
| 3 | `description` is specific (not vague) | Yes | |
| 4 | `description` length < 1024 chars | Yes | |
| 5 | Description has trigger words (3+) | Yes | |
| 6 | SKILL.md body < 500 lines | Yes | |
| 7 | All referenced files exist or will be created | Yes | |
| 8 | `allowed-tools` is appropriate | Yes | |
| 9 | Workflow steps are numbered | Yes | |
| 10 | Examples included | Recommended | |
| 11 | Error handling defined | Recommended | |
| 12 | Limitations documented | Recommended | |

**Validation Logic:**

```python
def validate_skill(session):
    errors = []
    warnings = []

    # Required checks (1-9)
    if not is_kebab_case(session.skill_name):
        errors.append("#1: Name must be kebab-case")
    if len(session.skill_name) > 64:
        errors.append("#2: Name exceeds 64 characters")
    if is_vague(session.description):
        errors.append("#3: Description too vague")
    if len(session.description) >= 1024:
        errors.append("#4: Description exceeds 1024 chars")
    if count_triggers(session.description) < 3:
        errors.append("#5: Need 3+ trigger words")
    # ... etc

    # Recommended checks (10-12)
    if not session.examples:
        warnings.append("#10: No examples provided")
    if not session.error_handling:
        warnings.append("#11: No error handling defined")
    if not session.limitations:
        warnings.append("#12: No limitations documented")

    return errors, warnings
```

### 2. Generate Structure Preview

**For simple/standard without steps:**

```
skills/{name}/
├── SKILL.md
└── references/       (if standard)
    └── {ref}.md
```

**For standard with steps (default):**

```
skills/{name}/
├── SKILL.md                    # Router (~200 lines)
├── steps/
│   ├── step-00-init.md
│   ├── step-01-{phase1}.md
│   ├── step-02-{phase2}.md
│   └── step-99-finish.md
└── references/
    └── {domain}.md
```

### 3. Generate SKILL.md Preview

Show first 50 lines of generated SKILL.md:

```yaml
---
name: {skill-name}
description: >-
  {validated description}
user-invocable: {true|false}
argument-hint: "{hint}"
allowed-tools: {tools}
---

# {Skill Name}

{one-line description}

## Quick Start

...
```

### 4. Display Validation Report

```
┌─────────────────────────────────────────────────────────────────┐
│ [VALIDATION REPORT]                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Skill: {name}                                                   │
│ Type: {user | core}                                             │
│ Mode: {simple | standard}                                       │
│ Structure: {simple | standard | advanced}                       │
│ Steps: {N files to generate}                                    │
│                                                                  │
│ ─────────────────────────────────────────────────────────────── │
│                                                                  │
│ CHECKLIST: {9}/9 required | {3}/3 recommended                   │
│                                                                  │
│ Required Checks:                                                │
│ [PASS] #1 Name is kebab-case                                    │
│ [PASS] #2 Name length <= 64                                     │
│ [PASS] #3 Description is specific                               │
│ ...                                                             │
│                                                                  │
│ Recommended Checks:                                             │
│ [PASS] #10 Examples included                                    │
│ [WARN] #11 Error handling not defined                           │
│ [PASS] #12 Limitations documented                               │
│                                                                  │
│ ─────────────────────────────────────────────────────────────── │
│                                                                  │
│ STRUCTURE PREVIEW:                                              │
│ skills/{name}/                                                  │
│ ├── SKILL.md                                                    │
│ ├── steps/ ({N} files)                                          │
│ └── references/                                                 │
│                                                                  │
│ ─────────────────────────────────────────────────────────────── │
│                                                                  │
│ Overall: {PASS | FAIL (N errors)}                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5. BREAKPOINT: User Approval

```
@skill:epci:breakpoint-system
  type: validation
  title: "Skill Ready for Generation"
  data: {
    skill_name: "{name}",
    validation_status: "{PASS|FAIL}",
    errors_count: N,
    warnings_count: N
  }
  ask: {
    question: "How would you like to proceed?",
    header: "Action",
    options: [
      { label: "Generate", description: "Create all files now" },
      { label: "Modify", description: "Go back and adjust settings" },
      { label: "Cancel", description: "Abort skill creation" }
    ]
  }
```

### 6. Handle User Response

| Response | Action |
|----------|--------|
| Generate | → `step-06-generation.md` |
| Modify | → Go back to specified step |
| Cancel | → End workflow |

## Outputs

| Output | Destination |
|--------|-------------|
| Validation results | Session state |
| User decision | For routing |

## Next Step

| Condition | Next Step |
|-----------|-----------|
| Generate | → `step-06-generation.md` |
| Modify | → Previous step (user choice) |
| Cancel | → End workflow |

## Reference Files

- [references/checklist-validation.md](../references/checklist-validation.md) — Detailed validation rules

## Error Handling

| Error | Resolution |
|-------|------------|
| Required check fails | Block generation, show fix |
| All recommended fail | Warn but allow proceed |
| User requests changes | Navigate to appropriate step |
