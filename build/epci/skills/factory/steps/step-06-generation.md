# Step 06: Generation

> Create all files, update plugin.json, generate conformity report.

## Trigger

- User approval from step-05-validation.md

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Session state | All previous steps | Yes |
| Validated skill data | From step-05 | Yes |
| Steps to generate | From step-04 | Yes |

## Protocol

### 1. Create Directory Structure

```bash
# For simple mode
mkdir -p skills/{name}/

# For standard mode without steps
mkdir -p skills/{name}/references/

# For standard mode with steps (default)
mkdir -p skills/{name}/steps/
mkdir -p skills/{name}/references/
```

### 2. Generate SKILL.md

**For simple/core mode:**
- Generate complete SKILL.md with all content
- No steps/ directory

**For standard mode with steps (default):**
- Generate SKILL.md as router/orchestrator (~200 lines)
- Include steps table and references

**Router SKILL.md Template:**

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

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER execute steps out of order
- :red_circle: NEVER skip breakpoints
- :white_check_mark: ALWAYS start with step-00-init.md
- :white_check_mark: ALWAYS follow next_step from each step

## EXECUTION PROTOCOLS:

1. **Load** step-00-init.md
2. **Execute** current step protocols
3. **Present** breakpoint if specified
4. **Evaluate** next step trigger
5. **Proceed** to next_step

## CONTEXT BOUNDARIES:

- IN scope: {scope.in}
- OUT scope: {scope.out}

## Workflow Overview

{workflow diagram}

## Flags

{flags table}

## Steps

{steps table}

## Step Files

{step file links}

## Reference Files

{reference links}

## Limitations

{limitations list}
```

### 3. Generate Step Files (if standard mode)

For each step in `steps_to_generate`:

```python
for step in steps_to_generate:
    if step == "step-00-init.md":
        template = "step-init-template.md"
    elif step == "step-99-finish.md":
        template = "step-finish-template.md"
    else:
        template = "step-generic-template.md"

    content = render_template(template, {
        "step_name": step.name,
        "step_number": step.number,
        "description": step.description,
        "prev_step": step.prev,
        "next_step": step.next,
        "protocols": step.protocols
    })

    write_file(f"skills/{name}/steps/{step}", content)
```

### 4. Generate Reference Files (if needed)

Based on structure and domain:

```python
if structure in ["standard", "advanced"]:
    for ref in references_needed:
        content = generate_reference(ref)
        write_file(f"skills/{name}/references/{ref}.md", content)
```

### 5. Update plugin.json

Add skill to plugin manifest:

```json
{
  "skills": [
    // ... existing skills ...
    {
      "path": "skills/{name}/SKILL.md",
      "name": "{skill-name}"
    }
  ]
}
```

### 6. Run Post-Generation Validation

```bash
python3 src/scripts/validate_skill.py skills/{name}/
```

Check:
- All files created successfully
- SKILL.md parses correctly
- Step files have valid frontmatter
- References exist

### 7. Generate Conformity Report

```
┌─────────────────────────────────────────────────────────────────┐
│ [GENERATION COMPLETE]                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ FILES CREATED:                                                  │
│ [OK] skills/{name}/SKILL.md                                     │
│ [OK] skills/{name}/steps/step-00-init.md                        │
│ [OK] skills/{name}/steps/step-01-{phase1}.md                    │
│ [OK] skills/{name}/steps/step-02-{phase2}.md                    │
│ [OK] skills/{name}/steps/step-99-finish.md                      │
│ [OK] skills/{name}/references/{ref}.md                          │
│                                                                  │
│ PLUGIN.JSON:                                                    │
│ [OK] Skill entry added                                          │
│                                                                  │
│ VALIDATION:                                                     │
│ [OK] Post-generation validation passed                          │
│                                                                  │
│ ─────────────────────────────────────────────────────────────── │
│                                                                  │
│ SKILL SUMMARY                                                   │
│ • Name: {name}                                                  │
│ • Type: {user | core}                                           │
│ • Mode: {simple | standard}                                     │
│ • Lines: {total lines}                                          │
│ • Files: {total files}                                          │
│ • Steps: {steps count}                                          │
│ • References: {refs count}                                      │
│                                                                  │
│ ─────────────────────────────────────────────────────────────── │
│                                                                  │
│ NEXT STEPS                                                      │
│ 1. Test: /{name} [args]                                         │
│ 2. Verify auto-triggering works                                 │
│ 3. Refine step content as needed                                │
│ 4. Add to documentation if public                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Outputs

| Output | Destination |
|--------|-------------|
| SKILL.md | `skills/{name}/SKILL.md` |
| Step files | `skills/{name}/steps/` |
| Reference files | `skills/{name}/references/` |
| plugin.json update | `src/.claude-plugin/plugin.json` |
| Conformity report | Display to user |

## Next Step

→ Workflow complete

## Error Handling

| Error | Resolution |
|-------|------------|
| Directory exists | Ask to overwrite or rename |
| Write permission denied | Report error, suggest fix |
| plugin.json parse error | Report error, manual fix needed |
| Validation fails | List issues, offer to fix |
