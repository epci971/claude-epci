# Structure Rules — ST-001 to ST-020

> Validation rules for section organization in EPCI commands

---

## Overview

Structure rules ensure commands have consistent, navigable organization.
Well-structured commands are easier to understand, maintain, and audit.

**Required Sections**: Overview, Process/Workflow, Output
**Conditional Sections**: Arguments, Skills, Subagents, Flags, Error Handling

---

## Rules Detail

### ST-001: Section `## Overview` présente

**Severity**: BLOQUANT

**Check**: Content contains `## Overview` header (case-insensitive)

**Rationale**: Overview provides essential context for command purpose

**Pass Example**:
```markdown
## Overview

This command audits slash commands against best practices.
```

**Fail Example**:
```markdown
# My Command

This command does things.

## Process
...
```

**Fix**: Add `## Overview` section after title

---

### ST-002: Overview: 2-4 phrases maximum

**Severity**: ERREUR

**Check**: Overview section contains 2-4 sentences

**Detection**: Count `.` or `!` or `?` followed by space or newline

**Pass Example**:
```markdown
## Overview

This command audits EPCI commands against 95 validation rules.
It produces a structured report with score and recommendations.
```

**Fail Example**:
```markdown
## Overview

This command audits EPCI commands against 95 validation rules derived from
official Anthropic documentation published in January 2025. It checks
frontmatter syntax, section structure, content quality, workflow logic,
and integration patterns. The audit produces a comprehensive report in
Markdown format with a score from 0-100. Results include a Mermaid
diagram of the detected workflow. Each violation is categorized by
severity: BLOQUANT, ERREUR, WARNING, or SUGGESTION. The tool supports
multiple modes including STRICT (default), LENIENT, and JSON output.
```

**Fix**: Keep to 2-4 concise sentences; move details to other sections

---

### ST-003: Section `## Process` ou `## Workflow` présente

**Severity**: BLOQUANT

**Check**: Content contains `## Process` or `## Workflow` header

**Rationale**: Commands must document their execution flow

**Pass Example**:
```markdown
## Process

### Step 1: Load Command
...

### Step 2: Validate
...
```

**Fail Example**:
```markdown
## Overview
...

## Output
...
```

**Fix**: Add `## Process` or `## Workflow` section

---

### ST-004: Process: étapes numérotées

**Severity**: ERREUR

**Check**: Process section contains numbered steps or `### Step N:` headers

**Valid Patterns**:
- `### Step 1:`, `### Step 2:`, ...
- `1. First step`, `2. Second step`, ...
- `### Phase 1:`, `### Phase 2:`, ...

**Pass Example**:
```markdown
## Process

### Step 1: Load Command
Read and parse the target file.

### Step 2: Validate Frontmatter
Check YAML syntax and required fields.
```

**Fail Example**:
```markdown
## Process

First we load the command. Then we validate the frontmatter.
After that we check the structure. Finally we generate the report.
```

**Fix**: Use numbered steps with headers or numbered lists

---

### ST-005: Section `## Output` présente

**Severity**: ERREUR

**Check**: Content contains `## Output` header

**Rationale**: Commands must document what they produce

**Pass Example**:
```markdown
## Output

```markdown
# Audit Report — command.md

Score: 85/100
Verdict: PASS
```
```

**Fix**: Add `## Output` section describing expected output

---

### ST-006: Section `## Arguments` si argument-hint présent

**Severity**: ERREUR

**Check**: If frontmatter has `argument-hint` → content has `## Arguments`

**Pass Example**:
```yaml
---
argument-hint: [file] [--strict]
---
```
```markdown
## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `file` | Path | Target command file |
| `--strict` | Flag | Enable strict mode |
```

**Fail Example**: Has `argument-hint` but no `## Arguments` section

**Fix**: Add `## Arguments` section documenting each argument

---

### ST-007: Arguments en format tableau

**Severity**: WARNING

**Check**: Arguments section uses table or structured list format

**Pass Example**:
```markdown
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `file` | Path | Yes | Target file |
```

**Fail Example**:
```markdown
## Arguments

The file argument is the target file to audit.
The strict flag enables strict mode.
```

**Fix**: Use table format for argument documentation

---

### ST-008: Section `## Skills Loaded` si skills utilisés

**Severity**: ERREUR

**Check**: If `**Skill**:` or skill names referenced → document in dedicated section

**Detection**: Look for skill references like `project-memory`, `epci-core`

**Pass Example**:
```markdown
## Configuration

| Element | Value |
|---------|-------|
| **Skills** | project-memory, epci-core, architecture-patterns |
```

**Fix**: Add skills to Configuration table or dedicated section

---

### ST-009: Section `## Subagents` si subagents invoqués

**Severity**: ERREUR

**Check**: If `@agent-name` used → document in Configuration or dedicated section

**Detection**: Look for patterns like `@Explore`, `@clarifier`, `@plan-validator`

**Pass Example**:
```markdown
## Configuration

| Element | Value |
|---------|-------|
| **Subagents** | @Explore (thorough), @clarifier (turbo mode) |
```

**Fix**: Document subagents with their invocation conditions

---

### ST-010: Au moins 1 exemple concret

**Severity**: WARNING

**Check**: Content contains at least one code block with example

**Detection**: Look for ` ``` ` blocks with realistic content

**Pass Example**:
```markdown
## Invocation

```bash
/audit-command commands/brief.md --strict
```
```

**Fail Example**: No code blocks or only abstract placeholders

**Fix**: Add concrete invocation example or output sample

---

### ST-011: Longueur totale 50-200 lignes (idéal)

**Severity**: WARNING

**Check**: Total line count between 50 and 200

**Rationale**:
- < 50 lines: Likely incomplete
- > 200 lines: Consider splitting or using references

**Fix**:
- If too short: Add missing sections
- If too long: Extract to skill or references

---

### ST-012: Longueur totale < 500 lignes

**Severity**: ERREUR

**Check**: Total line count < 500

**Rationale**: Long commands pollute context window

**Detection**: `content.count('\n') < 500`

**Fix**: Extract complex logic to skills; use references for details

---

### ST-013: Headers corrects

**Severity**: ERREUR

**Check**:
- Main sections use `##`
- Subsections use `###`
- No skipped levels (no `####` directly under `##`)

**Pass Example**:
```markdown
## Process

### Step 1: Load
Content...

### Step 2: Validate
Content...
```

**Fail Example**:
```markdown
## Process

#### Step 1: Load
Content...
```

**Fix**: Use consistent header hierarchy

---

### ST-014: Pas de sections vides

**Severity**: ERREUR

**Check**: No headers followed immediately by another header

**Pass Example**:
```markdown
## Overview

This command does X.

## Process
```

**Fail Example**:
```markdown
## Overview

## Process
```

**Fix**: Add content to section or remove header

---

### ST-015: Ordre logique des sections

**Severity**: WARNING

**Check**: Sections follow logical order

**Recommended Order**:
1. Overview
2. Configuration (if applicable)
3. Arguments (if applicable)
4. Process / Workflow
5. Output
6. Error Handling (if applicable)
7. References (if applicable)

**Detection**: Check section order against recommendation

---

### ST-016: Section `## Error Handling` pour commandes complexes

**Severity**: WARNING

**Check**: If command is > 100 lines → should have Error Handling section

**Rationale**: Complex commands need documented failure modes

**Pass Example**:
```markdown
## Error Handling

| Error | Recovery |
|-------|----------|
| File not found | Report error, skip |
| Invalid YAML | Mark BLOQUANT, continue |
```

---

### ST-017: Section `## Constraints` ou `## Boundaries`

**Severity**: WARNING

**Check**: Document limitations or boundaries

**Pass Example**:
```markdown
## Constraints

- Maximum 500 lines per command
- Only audits .md files
- Does not auto-fix issues
```

---

### ST-018: Breakpoints en format ASCII box

**Severity**: ERREUR

**Check**: If breakpoints present → use ASCII box format

**Required Format**:
```
┌─────────────────────────────────────┐
│ ⏸️  BREAKPOINT — TITLE               │
├─────────────────────────────────────┤
│ Content                             │
├─────────────────────────────────────┤
│ OPTIONS:                            │
│   [1] Option 1                      │
│   [2] Option 2                      │
└─────────────────────────────────────┘
```

**Detection**: Look for `BREAKPOINT` keyword; verify box characters

**Fail Example**:
```markdown
**BREAKPOINT**

Options:
- 1. Option 1
- 2. Option 2
```

**Fix**: Use ASCII box format with `┌`, `│`, `├`, `└` characters

---

### ST-019: Section `## See Also` si commandes liées

**Severity**: WARNING

**Check**: If references other commands → document in See Also

**Pass Example**:
```markdown
## See Also

- `/epci:brief` — Entry point, uses this for validation
- `/epci:quick` — Quick workflow for TINY/SMALL
```

---

### ST-020: Section `## Flags` si flags documentés

**Severity**: ERREUR

**Check**: If `--flag` patterns used → document in Flags section

**Pass Example**:
```markdown
## Flags

| Flag | Effect | Default |
|------|--------|---------|
| `--strict` | Enable strict mode | Yes |
| `--lenient` | Suggestions only | No |
| `--json` | JSON output | No |
```

---

## Section Detection Pseudocode

```python
def validate_structure(content: str, frontmatter: dict) -> list[Violation]:
    violations = []
    headers = re.findall(r'^(#{1,4})\s+(.+)$', content, re.MULTILINE)

    # ST-001: Overview required
    if not any(h[1].lower() == 'overview' for h in headers if h[0] == '##'):
        violations.append(Violation('ST-001', 'BLOQUANT', 'Missing ## Overview'))

    # ST-003: Process/Workflow required
    process_headers = ['process', 'workflow']
    if not any(h[1].lower() in process_headers for h in headers if h[0] == '##'):
        violations.append(Violation('ST-003', 'BLOQUANT', 'Missing ## Process'))

    # ST-006: Arguments section if argument-hint
    if 'argument-hint' in frontmatter:
        if not any('argument' in h[1].lower() for h in headers):
            violations.append(Violation('ST-006', 'ERREUR', 'Missing ## Arguments'))

    # ST-012: Line count
    line_count = content.count('\n')
    if line_count >= 500:
        violations.append(Violation('ST-012', 'ERREUR', f'Too long: {line_count} lines'))

    # ST-014: Empty sections
    for i, (level, title) in enumerate(headers[:-1]):
        next_level, _ = headers[i + 1]
        if level == '##' and next_level == '##':
            # Check if section is empty
            # ... implementation
            pass

    return violations
```

---

*Structure Rules v1.0.0 — Command Auditor*
