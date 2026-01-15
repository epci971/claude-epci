# Frontmatter Rules — FM-001 to FM-015

> Validation rules for YAML frontmatter in EPCI commands

---

## Overview

Frontmatter is the YAML block at the beginning of a command file, delimited by `---`.
It contains metadata and configuration that affects command behavior.

```yaml
---
description: Audits commands against best practices
argument-hint: [file] [--strict] [--json]
allowed-tools: Read, Grep, Glob
---
```

---

## Rules Detail

### FM-001: Frontmatter YAML présent

**Severity**: BLOQUANT

**Check**: File starts with `---` and has closing `---`

**Regex**: `^---\n[\s\S]*?\n---`

**Pass Example**:
```yaml
---
description: My command
---
```

**Fail Example**:
```markdown
# My Command
No frontmatter here
```

**Fix**: Add frontmatter block at file start

---

### FM-002: Champ `description` obligatoire

**Severity**: BLOQUANT

**Check**: Frontmatter contains `description` key

**Pass Example**:
```yaml
---
description: Validates code quality
---
```

**Fail Example**:
```yaml
---
allowed-tools: Read
---
```

**Fix**: Add `description: [what the command does]`

---

### FM-003: Description ≤ 500 caractères

**Severity**: ERREUR

**Check**: `len(description) <= 500`

**Rationale**: Long descriptions pollute `/help` output and SlashCommand tool budget

**Pass Example**:
```yaml
description: Audits EPCI commands against 95 rules from official Anthropic best practices
```

**Fail Example**:
```yaml
description: >-
  This command performs a comprehensive audit of all EPCI slash commands
  by checking them against a complete set of 95 validation rules that
  have been carefully derived from the official Anthropic documentation
  published in January 2025, as well as community best practices from
  multiple frameworks including SuperClaude, Superpowers, and WD...
  [continues for 600+ chars]
```

**Fix**: Condense to essential information; move details to Overview section

---

### FM-004: Description commence par verbe infinitif

**Severity**: ERREUR

**Check**: First word is infinitive verb (FR) or base verb (EN)

**Valid Starts** (EN): Audit, Create, Generate, Validate, Check, Build, Run, Execute, Analyze
**Valid Starts** (FR): Auditer, Créer, Générer, Valider, Vérifier, Construire, Exécuter, Analyser

**Pass Example**:
```yaml
description: Audit commands against best practices
```

**Fail Example**:
```yaml
description: This command audits commands
description: A tool for auditing commands
description: Command auditor for EPCI
```

**Fix**: Start with action verb: "Audit...", "Validate...", "Generate..."

---

### FM-005: Frontmatter < 15 lignes

**Severity**: WARNING

**Check**: Count lines between `---` delimiters < 15

**Rationale**: Keep metadata concise; details belong in content

**Pass Example** (8 lines):
```yaml
---
description: >-
  Audit commands against best practices.
  Use when validating before merge.
argument-hint: [file] [--strict]
allowed-tools: Read, Grep, Glob
---
```

**Fail Example** (20+ lines):
```yaml
---
description: ...
argument-hint: ...
allowed-tools: ...
model: ...
hooks:
  PreToolUse:
    - matcher: Bash
      hooks:
        - type: command
          command: ./validate.sh
  PostToolUse:
    - matcher: Write
      hooks:
        - type: command
          command: ./format.sh
---
```

**Fix**: Move complex hooks to external config or simplify

---

### FM-006: `argument-hint` si commande accepte des args

**Severity**: ERREUR

**Check**: If `$ARGUMENTS` or `$1` used in content → `argument-hint` must exist

**Pass Example**:
```yaml
---
description: Fix GitHub issue
argument-hint: [issue-number]
---

Fix issue #$ARGUMENTS
```

**Fail Example**:
```yaml
---
description: Fix GitHub issue
---

Fix issue #$ARGUMENTS
```

**Fix**: Add `argument-hint: [issue-number]` to frontmatter

---

### FM-007: Format argument-hint correct

**Severity**: ERREUR

**Check**: Arguments follow convention:
- `[optional]` — square brackets for optional
- `<required>` — angle brackets for required
- `--flag` — double dash for flags

**Pass Example**:
```yaml
argument-hint: <file> [--strict] [--json] [output-dir]
```

**Fail Example**:
```yaml
argument-hint: file strict json output
argument-hint: (file) {strict}
```

**Fix**: Use `[optional]`, `<required>`, `--flag` format

---

### FM-008: `allowed-tools` si outils restreints

**Severity**: WARNING

**Check**: If command uses limited tools, declare them

**Rationale**: Security principle of least privilege

**When Required**:
- Read-only commands (no Write, Edit, Bash)
- Commands with specific bash restrictions

**Pass Example**:
```yaml
---
description: Review code quality
allowed-tools: Read, Grep, Glob
---
```

---

### FM-009: Outils déclarés valides

**Severity**: ERREUR

**Check**: All tools in `allowed-tools` exist in VALID_TOOLS list

**VALID_TOOLS**:
```
Read, Write, Edit, Bash, Grep, Glob, Task,
WebSearch, WebFetch, TodoWrite, AskUserQuestion,
NotebookEdit, Skill, EnterPlanMode, ExitPlanMode
```

**Pass Example**:
```yaml
allowed-tools: Read, Grep, Glob, Bash(git:*)
```

**Fail Example**:
```yaml
allowed-tools: Read, Search, FileWrite, Terminal
```

**Fix**: Use exact tool names from VALID_TOOLS list

---

### FM-010: Bash restreint par pattern

**Severity**: BLOQUANT

**Check**: If Bash in allowed-tools, must use pattern restriction

**Forbidden**: `Bash(*)` or just `Bash`

**Required**: `Bash(command:*)` pattern

**Pass Example**:
```yaml
allowed-tools: Read, Bash(git add:*), Bash(git commit:*), Bash(npm test:*)
```

**Fail Example**:
```yaml
allowed-tools: Read, Bash(*)
allowed-tools: Read, Bash
```

**Fix**: Specify exact commands: `Bash(git:*)`, `Bash(npm:*)`, etc.

---

### FM-011: Pas de tabs dans YAML

**Severity**: BLOQUANT

**Check**: No tab characters (`\t`) in frontmatter

**Rationale**: YAML spec requires spaces for indentation

**Detection**: `\t` found between `---` delimiters

**Fix**: Replace tabs with spaces (2 or 4 per level)

---

### FM-012: Caractères spéciaux échappés

**Severity**: BLOQUANT

**Check**: Special YAML characters properly handled

**Characters requiring care**:
- `:` in values → quote the value
- `#` in values → quote the value
- `"` in values → escape or use single quotes

**Pass Example**:
```yaml
description: "Check code: validate syntax"
argument-hint: "[file] # optional comment"
```

**Fail Example**:
```yaml
description: Check code: validate syntax
```

**Fix**: Quote values containing `:`, `#`, or special characters

---

### FM-013: Pas de champs non reconnus

**Severity**: WARNING

**Check**: All frontmatter fields are from known set

**Known Fields**:
```
description, argument-hint, allowed-tools, model,
disable-model-invocation, hooks
```

**Pass Example**:
```yaml
---
description: My command
allowed-tools: Read
---
```

**Fail Example**:
```yaml
---
description: My command
author: John Doe
version: 1.0.0
---
```

**Fix**: Remove unknown fields; use content sections for metadata

---

### FM-014: `!` requiert Bash dans allowed-tools

**Severity**: BLOQUANT

**Check**: If `!` used in content for bash execution → `Bash` in allowed-tools

**Pass Example**:
```yaml
---
allowed-tools: Read, Bash(git:*)
---

Current status: !`git status`
```

**Fail Example**:
```yaml
---
allowed-tools: Read, Grep
---

Current status: !`git status`
```

**Fix**: Add appropriate `Bash(command:*)` to allowed-tools

---

### FM-015: Budget description < 15,000 caractères

**Severity**: WARNING

**Check**: Total frontmatter description content < 15,000 chars

**Rationale**: SlashCommand tool has 15K char budget for all descriptions

**Note**: This is across ALL commands, not per-command

**Monitoring**: Track total description length in project

---

## Validation Pseudocode

```python
def validate_frontmatter(content: str) -> list[Violation]:
    violations = []

    # FM-001: Check presence
    match = re.match(r'^---\n([\s\S]*?)\n---', content)
    if not match:
        violations.append(Violation('FM-001', 'BLOQUANT', 'No frontmatter'))
        return violations  # Can't continue without frontmatter

    fm_content = match.group(1)

    # FM-011: Check tabs before parsing
    if '\t' in fm_content:
        violations.append(Violation('FM-011', 'BLOQUANT', 'Tabs in YAML'))

    # Parse YAML
    try:
        fm = yaml.safe_load(fm_content)
    except yaml.YAMLError as e:
        violations.append(Violation('FM-012', 'BLOQUANT', f'Invalid YAML: {e}'))
        return violations

    # FM-002: Description required
    if 'description' not in fm:
        violations.append(Violation('FM-002', 'BLOQUANT', 'Missing description'))
    else:
        desc = fm['description']
        # FM-003: Length check
        if len(desc) > 500:
            violations.append(Violation('FM-003', 'ERREUR', f'Description too long: {len(desc)}'))
        # FM-004: Verb check
        if not starts_with_verb(desc):
            violations.append(Violation('FM-004', 'ERREUR', 'Description should start with verb'))

    # FM-005: Line count
    if fm_content.count('\n') >= 15:
        violations.append(Violation('FM-005', 'WARNING', 'Frontmatter too long'))

    # Continue with other checks...

    return violations
```

---

*Frontmatter Rules v1.0.0 — Command Auditor*
