# Least Privilege Guide - Subagent Tool Restriction

> Principle and application of minimal tool access for subagents

---

## Core Principle

**Least Privilege**: Grant only the minimum tools necessary for a subagent to complete its mission.

```
Maximum Security = Minimum Tools + Maximum Focus
```

### Why It Matters

| Benefit | Impact |
|---------|--------|
| **Security** | Reduces attack surface and unintended modifications |
| **Predictability** | Subagent behavior is constrained and expected |
| **Performance** | Fewer capabilities = faster, focused execution |
| **Debugging** | Limited scope makes issues easier to trace |

---

## Tool Classification

### Risk Levels

| Risk | Tools | When to Allow |
|------|-------|---------------|
| **Low** | Read, Grep, Glob | Default for analysis |
| **Medium** | Write, Task | When generation is needed |
| **High** | Edit, Bash | Only when modification is essential |

### Tool Capabilities Matrix

| Tool | Reads | Creates | Modifies | Executes |
|------|-------|---------|----------|----------|
| Read | ✅ | - | - | - |
| Grep | ✅ | - | - | - |
| Glob | ✅ | - | - | - |
| Write | ✅ | ✅ | - | - |
| Edit | ✅ | - | ✅ | - |
| Task | - | - | - | ✅ |
| Bash | ✅ | ✅ | ✅ | ✅ |

---

## Tools by Mission Type

### Analysis Missions

**Examples**: Code review, security audit, quality assessment

```yaml
allowed-tools: Read, Grep, Glob
```

**Justification**: Analysis only needs to read and search, never modify.

### Validation Missions

**Examples**: Plan validation, configuration check, format verification

```yaml
allowed-tools: Read, Grep
```

**Justification**: Validation reads and compares, no file discovery needed.

### Generation Missions

**Examples**: Documentation generation, report creation

```yaml
allowed-tools: Read, Write, Glob
```

**Justification**: Needs to read inputs and create new files.

### Review + Fix Missions

**Examples**: Auto-fix linting, automatic corrections

```yaml
allowed-tools: Read, Edit, Grep
```

**Justification**: Must read, find, and modify existing files.

### Orchestration Missions

**Examples**: Workflow coordination, multi-step delegation

```yaml
allowed-tools: Read, Task, Glob
```

**Justification**: Coordinates other agents, delegates work.

---

## Decision Framework

### Step 1: Identify Mission Type

```
Is the mission about...
├── Understanding code?     → Analysis
├── Checking correctness?   → Validation
├── Creating new content?   → Generation
├── Fixing existing code?   → Modification
└── Coordinating agents?    → Orchestration
```

### Step 2: Select Base Tools

| Mission Type | Base Tools |
|--------------|------------|
| Analysis | Read, Grep |
| Validation | Read, Grep |
| Generation | Read, Write |
| Modification | Read, Edit |
| Orchestration | Read, Task |

### Step 3: Add Only If Needed

| Additional Need | Tool to Add |
|-----------------|-------------|
| Find files by pattern | +Glob |
| Search code | +Grep |
| Create new files | +Write |
| Modify existing | +Edit |
| Run tests/commands | +Bash |
| Delegate subtasks | +Task |

---

## Anti-Patterns

### Over-Permissive

```yaml
# ❌ BAD: All tools for a simple reviewer
name: code-reviewer
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
```

```yaml
# ✅ GOOD: Only what's needed
name: code-reviewer
allowed-tools: Read, Grep, Glob
```

### Copy-Paste Tools

```yaml
# ❌ BAD: Copied from another agent without thinking
name: doc-checker
allowed-tools: Read, Write, Edit, Bash  # Why Bash?
```

```yaml
# ✅ GOOD: Justified for this mission
name: doc-checker
allowed-tools: Read, Grep  # Only reads and searches
```

### Unnecessary Write Access

```yaml
# ❌ BAD: Write for a validation agent
name: plan-validator
allowed-tools: Read, Write, Grep
```

```yaml
# ✅ GOOD: Validation doesn't write
name: plan-validator
allowed-tools: Read, Grep
```

---

## Justification Template

When requesting tools beyond the minimum, document why:

```markdown
## Tool Justification

| Tool | Reason |
|------|--------|
| Read | Read source files for analysis |
| Grep | Search for patterns in codebase |
| Glob | Find test files by pattern |
| Bash | **Needed to run test suite** |
```

---

## EPCI Subagent Examples

### @code-reviewer

```yaml
allowed-tools: Read, Grep, Glob
```
- **Read**: Examine source files
- **Grep**: Find patterns and usages
- **Glob**: Locate files by type
- **No Write/Edit**: Reviewer suggests, doesn't fix

### @security-auditor

```yaml
allowed-tools: Read, Grep
```
- **Read**: Inspect code for vulnerabilities
- **Grep**: Search for dangerous patterns
- **No Glob**: Security patterns are searched, not discovered
- **No Write**: Reports findings, doesn't modify

### @doc-generator

```yaml
allowed-tools: Read, Write, Glob
```
- **Read**: Extract information from source
- **Write**: Create documentation files
- **Glob**: Find source files to document
- **No Edit**: Creates new docs, doesn't modify code

### @plan-validator

```yaml
allowed-tools: Read, Grep
```
- **Read**: Review plan document
- **Grep**: Cross-reference with codebase
- **No Write**: Validates, doesn't create
- **No Glob**: Plan specifies files directly

---

## Audit Checklist

Before finalizing subagent tools:

- [ ] Can mission be accomplished with Read only?
- [ ] Is Grep needed or can specific files be read?
- [ ] Is Glob needed or are paths known?
- [ ] Is Write absolutely necessary for output?
- [ ] Is Edit needed or should fixes be suggested?
- [ ] Is Bash justified for command execution?
- [ ] Is Task needed or can main agent orchestrate?

---

## Quick Reference

```
+------------------------------------------+
|         TOOL SELECTION BY MISSION         |
+------------------------------------------+
| ANALYZE code   → Read, Grep, Glob        |
| VALIDATE plan  → Read, Grep              |
| GENERATE docs  → Read, Write, Glob       |
| MODIFY code    → Read, Edit, Grep        |
| ORCHESTRATE    → Read, Task, Glob        |
+------------------------------------------+
| NEVER give more than needed              |
| ALWAYS justify each tool                 |
+------------------------------------------+
```
