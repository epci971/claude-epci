---
name: step-02-architecture
description: Determine structure, select tools, and provide context-aware recommendations
prev_step: steps/step-01-preanalysis.md
next_step: steps/step-03-description.md
---

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

## 🔴 MANDATORY: Task Tool for Subagent Delegation

### Rule: When to Use Task Tool

Skills with phases that can be delegated MUST use the Task tool:

| Situation | Task tool | Notes |
|-----------|-----------|-------|
| Planning phase | `Task(subagent_type: "planner")` | ✅ Delegable |
| Plan validation | `Task(subagent_type: "plan-validator")` | ✅ Delegable |
| Review phase | `Task(subagent_type: "code-reviewer")` | ✅ Delegable |
| Security audit | `Task(subagent_type: "security-auditor")` | ✅ Delegable |
| **Implementation** | ❌ Thread principal | Needs stack skills access |
| **QA validation** | ❌ Thread principal | Not prioritized |

### Exception: Implementation Phase

Implementation (`@implementer`) MUST NOT be delegated because:
- Subagents don't have access to the Skill tool
- Cannot load stack skills (python-django, javascript-react, etc.)
- Main thread has access to all skills

### Why This is CRITICAL

- **Context isolation**: Agent receives only its prompt
- **Cost optimization**: Uses optimal model (Sonnet vs Opus)
- **Parallelization**: Multiple agents can run in parallel
- **Memory preservation**: Main context window not saturated

### Mandatory Pattern in Steps

Each step that delegates to an agent MUST include:

LANCE Task({
  subagent_type: "{agent-name}",
  prompt: `
## Objective
{clear objective}

## Context
{necessary context}

## Expected Output
{format expected}
  `
})

### Anti-pattern: Description without Invocation

❌ FORBIDDEN:
```markdown
### Invoke @code-reviewer
- Pass files
- Request review
```

✅ REQUIRED:

LANCE Task({
  subagent_type: "code-reviewer",
  prompt: "..."
})

## 🔵 Native Agents (Built-in Claude Code)

Claude Code provides built-in agents optimized for specific tasks. Use these for generic operations before considering custom agents.

### Available Native Agents

| Agent | Identifier | Model | Tools | Best For |
|-------|------------|-------|-------|----------|
| **Explore** | `Explore` | Haiku | Read-only (Read, Glob, Grep) | Fast codebase exploration |
| **Plan** | `Plan` | Inherits | Read-only | Research for planning |
| **General-purpose** | `general-purpose` | Inherits | All tools | Complex multi-step tasks |
| **Bash** | `Bash` | Inherits | Bash only | Isolated terminal commands |

### Key Characteristics

- **Explore**: Optimized for speed (Haiku model), perfect for read-only search
- **Plan**: Context isolation for safe planning research
- **General-purpose**: Full tool access for complex autonomous tasks

### Rule: Native vs Custom

| Use Native When | Use Custom When |
|-----------------|-----------------|
| Generic exploration | EPCI-specific format needed |
| General research | Domain-specific validation |
| Multi-step autonomous | Custom checklist required |
| No special format needed | Structured output required |

**Guideline**: Use native agents when the task is **generic**, use custom agents when **EPCI-specific** formatting or validation is required.

### Invocation Pattern

LANCE Task({
  subagent_type: "Explore",
  prompt: `
## Exploration Objective
{objective}

## Search Focus
1. {focus_1}
2. {focus_2}

## Thoroughness Level
{quick | medium | very thorough}

## Expected Output
- Relevant files with purpose
- Patterns identified
- Dependencies mapped
  `
})

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

@../references/stacks-catalog.md
@../references/agents-catalog.md

| Reference | Purpose |
|-----------|---------|
| stacks-catalog.md | Stack detection rules |
| agents-catalog.md | Agent recommendation logic |

## Error Handling

| Error | Resolution |
|-------|------------|
| @Explore timeout | Continue with manual detection |
| Multiple stacks detected | List all, ask user to confirm primary |
| Unknown project type | Use generic recommendations |
