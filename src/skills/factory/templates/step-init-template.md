# Step Init Template

> Template for generating step-00-init.md files in new skills.

## Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{{skill_name}}` | Skill name (kebab-case) | `auth-handler` |
| `{{skill_title}}` | Skill title (Title Case) | `Auth Handler` |
| `{{flags}}` | List of supported flags | `--turbo, --dry-run` |
| `{{next_step}}` | Default next step file | `step-01-analyze.md` |
| `{{conditional_next}}` | Conditional routing | `--quick → step-quick.md` |

---

## Template Content

```markdown
# Step 00: Init

> Parse arguments, initialize context, detect mode.

## Trigger

- Skill invocation: `/{{skill_name}} <args> [--flags]`

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `args` | User argument | Yes |
{{#each flags}}
| `--{{this.name}}` | User flag | No |
{{/each}}

## Protocol

### 1. Parse Arguments

```
Extract from user input:
  - args: The main arguments
  - flags: All --flag arguments

Validate:
  - Required arguments are present
  - Arguments are valid format
```

### 2. Initialize State

```json
{
  "session_id": "{{skill_name}}-{timestamp}",
  "args": "<parsed args>",
  "flags": {
{{#each flags}}
    "{{this.name}}": {{this.default}}{{#unless @last}},{{/unless}}
{{/each}}
  },
  "status": "initialized"
}
```

### 3. Launch @Explore (Background)

```
Task: Explore codebase for context
Focus:
  - Relevant files
  - Existing patterns
  - Dependencies
```

## Outputs

| Output | Destination |
|--------|-------------|
| Session state | Memory |
| @Explore task | Running in background |

## Next Step

| Condition | Next Step |
|-----------|-----------|
{{#if conditional_next}}
{{#each conditional_next}}
| `{{this.condition}}` | → `{{this.step}}` |
{{/each}}
{{/if}}
| Default | → `{{next_step}}` |

## Error Handling

| Error | Resolution |
|-------|------------|
| Missing required args | Ask user to provide |
| Invalid format | Suggest correction |
```

---

## Usage

When Factory generates a new skill with steps, use this template for `step-00-init.md`:

1. Replace all `{{variables}}` with skill-specific values
2. Add skill-specific flags to the Inputs table
3. Add skill-specific state fields
4. Define conditional routing if needed
