# Step Generic Template

> Template for generating intermediate step files (step-01 through step-98) in new skills.

## Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{{step_number}}` | Step number (2 digits) | `01`, `02` |
| `{{step_name}}` | Step name (kebab-case) | `analyze`, `execute` |
| `{{step_title}}` | Step title (Title Case) | `Analyze`, `Execute` |
| `{{step_description}}` | One-line description | `Analyze input and gather context` |
| `{{prev_step}}` | Previous step file | `step-00-init.md` |
| `{{next_step}}` | Next step file | `step-02-plan.md` |
| `{{protocols}}` | List of protocol steps | `[{verb: "Analyze", description: "..."}]` |
| `{{has_breakpoint}}` | Whether step has breakpoint | `true/false` |
| `{{breakpoint_type}}` | Breakpoint type | `validation`, `plan-review` |

---

## Template Content

```markdown
# Step {{step_number}}: {{step_title}}

> {{step_description}}

## Trigger

- Completion of {{prev_step}}

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Session state | From previous step | Yes |
| {additional inputs} | {source} | {Yes/No} |

## Protocol

{{#each protocols}}
### {{@index}}. {{this.verb}}

{{this.description}}

{{#if this.code}}
```
{{this.code}}
```
{{/if}}
{{/each}}

{{#if has_breakpoint}}
## BREAKPOINT

```
@skill:breakpoint-system
  type: {{breakpoint_type}}
  title: "{{step_title}} Validation"
  data: {
    // Step-specific data
  }
  ask: {
    question: "How would you like to proceed?",
    header: "Action",
    options: [
      { label: "Continue", description: "Proceed to next step" },
      { label: "Modify", description: "Adjust current step" },
      { label: "Cancel", description: "Stop workflow" }
    ]
  }
```
{{/if}}

## Outputs

| Output | Destination |
|--------|-------------|
| {output 1} | Session state |
| {output 2} | For next step |

## Next Step

{{#if conditional_next}}
| Condition | Next Step |
|-----------|-----------|
{{#each conditional_next}}
| `{{this.condition}}` | → `{{this.step}}` |
{{/each}}
| Default | → `{{next_step}}` |
{{else}}
→ `{{next_step}}`
{{/if}}

## Error Handling

| Error | Resolution |
|-------|------------|
| {error 1} | {resolution} |
| {error 2} | {resolution} |
```

---

## Usage

When Factory generates intermediate steps:

1. Set step number and name from workflow design
2. Link prev_step and next_step correctly
3. Fill in protocols from phase description
4. Add breakpoint if phase requires user validation
5. Define outputs that next step needs
