# Step Finish Template

> Template for generating step-99-finish.md files in new skills.

## Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{{skill_name}}` | Skill name (kebab-case) | `auth-handler` |
| `{{skill_title}}` | Skill title (Title Case) | `Auth Handler` |
| `{{prev_step}}` | Previous step file | `step-03-execute.md` |
| `{{outputs}}` | List of outputs to verify | `[{name: "report.md", type: "file"}]` |
| `{{next_actions}}` | Suggested next actions | `["Test", "Commit"]` |

---

## Template Content

```markdown
# Step 99: Finish

> Finalize workflow, verify outputs, present summary.

## Trigger

- Completion of {{prev_step}}

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Session state | All previous steps | Yes |
| All step outputs | Previous steps | Yes |

## Protocol

### 1. Verify Outputs

Check all expected outputs exist:

```python
outputs_to_verify = [
{{#each outputs}}
    {"name": "{{this.name}}", "type": "{{this.type}}"},
{{/each}}
]

for output in outputs_to_verify:
    if output.type == "file":
        verify file_exists(output.name)
    elif output.type == "state":
        verify state_has(output.name)
```

### 2. Run Final Validation

```
IF any output missing:
  → Report error, suggest recovery
ELSE:
  → Continue to summary
```

### 3. Update Project Memory (Optional)

```python
@skill:project-memory
  store_artifact({
    type: "{{skill_name}}-output",
    data: session.outputs,
    timestamp: now()
  })
```

### 4. Generate Completion Summary

```
┌─────────────────────────────────────────────────────────────────┐
│ [WORKFLOW COMPLETE] {{skill_title}}                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ OUTPUTS:                                                        │
{{#each outputs}}
│ [OK] {{this.name}}                                              │
{{/each}}
│                                                                  │
│ SUMMARY:                                                        │
│ • {key result 1}                                                │
│ • {key result 2}                                                │
│                                                                  │
│ NEXT STEPS:                                                     │
{{#each next_actions}}
│ {{@index}}. {{this}}                                            │
{{/each}}
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Outputs

| Output | Destination |
|--------|-------------|
| Completion summary | Display to user |
| Final state | Archive |

## Next Step

→ Workflow complete (no next step)

## Error Handling

| Error | Resolution |
|-------|------------|
| Missing output | Report which output, suggest re-run step |
| Validation fails | List issues, offer partial completion |
```

---

## Usage

When Factory generates step-99-finish.md:

1. Set prev_step to the last main step
2. List all outputs the skill should produce
3. Define appropriate next actions
4. Include project-memory integration if skill produces artifacts
