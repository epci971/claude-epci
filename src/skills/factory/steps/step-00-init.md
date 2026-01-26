# Step 00: Init

> Parse arguments, detect mode (core/simple/standard), initialize session.

## Trigger

- Skill invocation: `/factory <skill-name> [--core] [--simple]`

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `skill-name` | User argument | Yes |
| `--core` | User flag | No |
| `--simple` | User flag | No |

## Protocol

### 1. Parse Arguments

```
Extract from user input:
  - skill_name: The skill name (kebab-case expected)
  - flags: --core, --simple

Validate:
  - skill_name is provided
  - skill_name is kebab-case (lowercase, hyphens only)
  - skill_name length <= 64 characters
```

### 2. Detect Mode

```
IF --core flag:
  → mode = "core"
  → location = "skills/core/{name}/"
  → user_invocable = false
  → generate_steps = false

ELSE IF --simple flag:
  → mode = "simple"
  → location = "skills/{name}/"
  → user_invocable = true
  → generate_steps = false

ELSE (default):
  → mode = "standard"
  → location = "skills/{name}/"
  → user_invocable = true
  → generate_steps = true
```

### 3. Check for Existing Skill

```
Check if skill already exists at target location:
  - IF exists → Error: "Skill already exists at {path}"
  - ELSE → Continue
```

### 4. Initialize Session State

```json
{
  "factory_id": "factory-{skill-name}-{timestamp}",
  "skill_name": "<parsed name>",
  "mode": "<core|simple|standard>",
  "location": "<target path>",
  "user_invocable": true|false,
  "generate_steps": true|false,
  "status": "initialized",
  "collected": {
    "purpose": null,
    "frequency": null,
    "triggers": null,
    "scope": null,
    "persona": null,
    "structure": null,
    "tools": null,
    "description": null,
    "workflow": null
  },
  "recommendations": {
    "stacks": [],
    "agents": []
  }
}
```

### 5. Launch @Explore (Background)

```
Task: Explore codebase for factory context
Focus:
  - Project stack (package.json, composer.json, etc.)
  - Existing skills structure
  - Naming conventions used
  - Related functionality
```

## Outputs

| Output | Destination |
|--------|-------------|
| Session state | Memory |
| Mode detection | For routing |
| @Explore task | Running in background |

## Next Step

→ `step-01-preanalysis.md`

## Error Handling

| Error | Resolution |
|-------|------------|
| Missing skill name | Ask user to provide name |
| Invalid skill name | Suggest corrected name (kebab-case) |
| Skill already exists | Ask to choose different name or confirm overwrite |
