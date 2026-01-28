# Step 00: Init

> Parse arguments, detect mode (core/simple/standard/audit), initialize session.

## Trigger

- Skill invocation: `/factory <skill-name> [--core] [--simple] [--audit]`

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `skill-name` | User argument | Yes |
| `--core` | User flag | No |
| `--simple` | User flag | No |
| `--audit` | User flag | No |
| `--refactor` | User flag | No |

## Protocol

### 1. Parse Arguments

```
Extract from user input:
  - skill_name: The skill name (kebab-case expected)
  - flags: --core, --simple, --audit

Validate:
  - skill_name is provided
  - skill_name is kebab-case (lowercase, hyphens only)
  - skill_name length <= 64 characters
```

### 2. Detect Mode

```
IF --audit flag:
  → mode = "audit"
  → GOTO: Audit Mode (section 2b below)

IF --refactor flag:
  → mode = "refactor"
  → GOTO: Refactor Mode (section 2c below)

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

### 2b. Audit Mode (--audit flag)

When `--audit` flag is detected:

1. **Resolve skill path**:
   ```
   Search for existing skill in order:
     1. src/skills/{skill-name}/
     2. src/skills/core/{skill-name}/
     3. src/skills/stack/{skill-name}/

   IF skill not found:
     → Error: "Skill '{skill-name}' not found"
     → EXIT
   ```

2. **Run audit script**:
   ```bash
   python src/skills/factory/scripts/audit_skill.py <resolved_skill_path>
   ```

3. **Display audit report** (ASCII format with phases):
   - Phase 1: Structure (12-point checklist)
   - Phase 2: Breakpoint Compliance
   - Phase 3: Core Skills Usage
   - Phase 4: Stack Skills Detection
   - Phase 5: Step Chain Validation

4. **EXIT workflow** - Do not continue to step-01

**Example output**:
```
+----------------------------------------------------------------------+
| AUDIT SKILL: brainstorm                                               |
+----------------------------------------------------------------------+
| Phase 1: Structure (12-point)                          [OK] 12/12     |
| Phase 2: Breakpoint Compliance                         [OK] 4/4       |
| Phase 3: Core Skills Usage                             [WARN] 5/6     |
| Phase 4: Stack Skills Detection                        [OK] N/A       |
| Phase 5: Step Chain Validation                         [OK] 10/10     |
+----------------------------------------------------------------------+
| RESULT: PASS WITH WARNINGS (1 warning)                                |
+----------------------------------------------------------------------+
```

### 2c. Refactor Mode (--refactor flag)

When `--refactor` flag is detected:

1. **Resolve skill path**:
   ```
   Search for existing skill in order:
     1. src/skills/{skill-name}/
     2. src/skills/core/{skill-name}/
     3. src/skills/stack/{skill-name}/

   IF skill not found:
     → Error: "Skill '{skill-name}' not found"
     → EXIT
   ```

2. **Initialize refactor session**:
   ```json
   {
     "factory_id": "refactor-{skill-name}-{timestamp}",
     "skill_name": "<parsed name>",
     "skill_path": "<resolved path>",
     "mode": "refactor",
     "status": "initialized"
   }
   ```

3. **Route to step-07-refactor.md**:
   ```
   → GOTO: step-07-refactor.md
   → Skip steps 01-06 (creation workflow)
   ```

**Example invocation**:
```
/factory debug --refactor
→ Resolves: src/skills/debug/
→ Routes to: step-07-refactor.md
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
