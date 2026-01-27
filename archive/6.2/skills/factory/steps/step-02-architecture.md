# Step 02: Architecture

> Determine structure, select tools, and provide context-aware recommendations.

## Trigger

- Completion of step-01-preanalysis.md (PROCEED or Override)

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Session state | From step-01 | Yes |
| Mode | From step-00 | Yes |
| @Explore results | Background task | No (use if available) |

## Protocol

### 1. Determine Structure

Based on collected data and mode:

```
IF mode == "core":
  → structure = "simple"
  → No references needed (self-contained)

ELSE IF mode == "simple":
  → structure = "simple" OR "standard"
  → Based on estimated lines

ELSE (standard mode):
  → Analyze complexity:
    - Workflow steps count
    - External references needed
    - Templates required
```

**Structure Options:**

| Structure | When to Use | Files |
|-----------|-------------|-------|
| **Simple** | < 200 lines, single workflow | `SKILL.md` only |
| **Standard** | Multi-step, references needed | `SKILL.md` + `references/` |
| **Advanced** | Templates, scripts, multi-workflow | Full structure + `steps/` |

### 2. Select Tools

Based on skill purpose and scope:

```python
TOOL_MAPPING = {
    "read-only": ["Read", "Glob", "Grep"],
    "file-modifications": ["Read", "Write", "Edit"],
    "user-interaction": ["AskUserQuestion"],
    "commands": ["Bash"],
    "exploration": ["Read", "Glob", "Grep", "Task"]
}

# Suggest based on purpose keywords
if "analyze" in purpose or "read" in purpose:
    suggest tools from "read-only"
if "create" in purpose or "generate" in purpose:
    suggest tools from "file-modifications"
if "interactive" in purpose or "guided" in purpose:
    suggest "user-interaction"
# etc.
```

Present recommendation:
```
Recommended tools: Read, Write, Edit, AskUserQuestion
Reason: Skill generates files and requires user input

[Accept] [Modify]
```

### 3. Auto-Detect Stack Context

Check project for stack signatures:

```python
STACK_DETECTION = {
    "python-django": ["manage.py", "django" in requirements],
    "javascript-react": ["react" in package.json],
    "java-springboot": ["spring-boot" in pom.xml or build.gradle],
    "php-symfony": ["symfony" in composer.json],
    "frontend-editor": ["tailwind.config.*"]
}
```

### 4. Recommend Agents

Based on skill type and domain:

```python
AGENT_RECOMMENDATIONS = {
    "code-generation": ["code-reviewer"],
    "auth-domain": ["security-auditor"],
    "complex-workflow": ["plan-validator"],
    "testing": ["qa-reviewer"]
}
```

### 5. Display Recommendations

```
┌─────────────────────────────────────────────────────────────────┐
│ [RECOMMENDATIONS] Context-Aware Suggestions                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ STRUCTURE: {simple|standard|advanced}                            │
│ Reason: {why this structure}                                    │
│                                                                  │
│ TOOLS:                                                          │
│ • {tool1} - {reason}                                            │
│ • {tool2} - {reason}                                            │
│                                                                  │
│ DETECTED STACK:                                                  │
│ • {stack} ({trigger file})                                      │
│                                                                  │
│ SUGGESTED AGENTS for this skill type:                            │
│ • {agent1} ({reason})                                           │
│ • {agent2} ({reason})                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6. Store Architecture Decisions

```json
{
  "collected": {
    "structure": "<simple|standard|advanced>",
    "tools": ["<tool1>", "<tool2>", ...],
    "references_needed": ["<ref1>", ...],
    "templates_needed": ["<template1>", ...]
  },
  "recommendations": {
    "stacks": ["<stack1>"],
    "agents": ["<agent1>", "<agent2>"]
  }
}
```

## Outputs

| Output | Destination |
|--------|-------------|
| Structure decision | Session state |
| Tools list | Session state |
| Recommendations | Session state |

## Next Step

→ `step-03-description.md`

## Reference Files

- [references/stacks-catalog.md](../references/stacks-catalog.md) — Stack detection rules
- [references/agents-catalog.md](../references/agents-catalog.md) — Agent recommendation logic

## Error Handling

| Error | Resolution |
|-------|------------|
| @Explore timeout | Continue with manual detection |
| Multiple stacks detected | List all, ask user to confirm primary |
| Unknown project type | Use generic recommendations |
