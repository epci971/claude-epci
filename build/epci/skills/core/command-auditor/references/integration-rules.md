# Integration Rules — IN-001 to IN-015

> Validation rules for skills, subagents, hooks, and external integrations

---

## Overview

Integration rules ensure commands properly document and use:
- Skills (loaded knowledge bases)
- Subagents (delegated AI agents)
- Hooks (pre/post execution scripts)
- MCP servers (external capabilities)
- Memory hooks (project context)

---

## Rules Detail

### IN-001: Skills chargés documentés

**Severity**: ERREUR

**Check**: If skills referenced → document in Configuration section

**Detection**: Look for skill names: `project-memory`, `epci-core`, `architecture-patterns`, etc.

**Pass Example**:
```markdown
## Configuration

| Element | Value |
|---------|-------|
| **Skills** | project-memory, epci-core, flags-system |
```

**Required Information**:
- Skill name
- When loaded (always or conditional)

---

### IN-002: Subagents invoqués documentés

**Severity**: ERREUR

**Check**: If `@agent` used → document with condition and role

**Pass Example**:
```markdown
## Configuration

| Element | Value |
|---------|-------|
| **Subagents** | @Explore (thorough), @clarifier (turbo mode) |
```

**Required Information**:
- Subagent handle (`@name`)
- Invocation condition
- Role/purpose

---

### IN-003: Hooks documentés

**Severity**: WARNING

**Check**: If hooks used → document with type and trigger

**Hook Types**:
- `pre-{command}` — Before command execution
- `post-{command}` — After command completion
- `on-{event}` — On specific event

**Pass Example**:
```markdown
**Execute `pre-brief` hooks** (if configured in `hooks/active/`)
```

---

### IN-004: MCP servers documentés

**Severity**: WARNING

**Check**: If MCP servers used → document with activation condition

**Known MCP Servers**:
- Context7 (`--c7`) — Documentation lookup
- Sequential (`--seq`) — Multi-step reasoning
- Magic (`--magic`) — UI generation
- Playwright (`--play`) — E2E testing

**Pass Example**:
```markdown
## Configuration

| Element | Value |
|---------|-------|
| **MCP** | Context7 (auto: architect persona) |
```

---

### IN-005: Personas suggérés documentés

**Severity**: WARNING

**Check**: If persona activation mentioned → document criteria

**Known Personas**: Architect, Frontend, Backend, Security, QA, Doc

**Pass Example**:
```markdown
## Persona Detection

Score all 6 personas using algorithm:
- If score > 0.6: Auto-activate
- If score 0.4-0.6: Suggest in breakpoint
```

---

### IN-006: Thinking level recommandé

**Severity**: WARNING

**Check**: Document recommended thinking level

**Levels**:
- `think` — Standard
- `think hard` — Complex (default for most)
- `ultrathink` — Very complex or uncertain

**Pass Example**:
```markdown
## Configuration

| Element | Value |
|---------|-------|
| **Thinking** | `think hard` (default) / `ultrathink` (LARGE) |
```

---

### IN-007: Workflow routing documenté

**Severity**: ERREUR

**Check**: If routing to other commands → document conditions

**Pass Example**:
```markdown
## Routing

| Category | Command | Flags |
|----------|---------|-------|
| TINY | `/quick --autonomous` | `--autonomous` |
| SMALL | `/quick` | `--think` if 3+ files |
| STANDARD | `/epci` | `--think-hard` |
| LARGE | `/epci --large` | `--think-hard --wave` |
```

**Required Information**:
- Routing condition
- Target command
- Flags passed

---

### IN-008: Breakpoints MANDATORY marqués

**Severity**: ERREUR

**Check**: Critical breakpoints marked as MANDATORY

**When Required**:
- User must make a choice
- Before irreversible action
- Required validation point

**Pass Example**:
```markdown
### Step 4: BREAKPOINT — Analysis Review (MANDATORY)

**MANDATORY:** Display this breakpoint and WAIT for user choice.
```

---

### IN-009: Output paths documentés

**Severity**: ERREUR

**Check**: Document where output is written

**Pass Example**:
```markdown
**Output Paths:**
- TINY/SMALL → Inline brief (no file created)
- STANDARD/LARGE → `docs/features/<slug>.md`
```

**Required Information**:
- Path pattern
- Conditions for each path
- File format

---

### IN-010: Error handling explicite

**Severity**: WARNING

**Check**: Document error scenarios and recovery

**Pass Example**:
```markdown
## Error Handling

| Error | Recovery |
|-------|----------|
| Detection fails | Fallback to generic templates |
| Template missing | Skip with warning |
| Validation fails | Report issues, don't abort |
```

---

### IN-011: Fallbacks documentés

**Severity**: WARNING

**Check**: Document fallback behavior for failures

**Pass Example**:
```markdown
IF @Explore fails or times out:
1. Log warning: "Exploration incomplete"
2. Continue with partial results
3. Mark complexity as UNKNOWN
4. Suggest `--think-hard` for safety
```

---

### IN-012: Context file schema documenté

**Severity**: ERREUR

**Check**: If using context files → document schema

**Pass Example**:
```markdown
## Context File Schema

```json
{
  "phase": "phase-3",
  "feature_slug": "<slug>",
  "complexity": "<TINY|SMALL|STANDARD|LARGE>",
  "files_modified": ["<files>"],
  "actual_time": "<duration>"
}
```
```

---

### IN-013: Session persistence expliquée

**Severity**: WARNING

**Check**: If state persists across steps → document mechanism

**Pass Example**:
```markdown
**Internal outputs** (store for Step 3):
- List of candidate files
- Detected technical stack
- Identified risks
```

---

### IN-014: Memory hooks documentés

**Severity**: ERREUR

**Check**: If command affects project memory → document hooks

**Critical Hook**: `post-phase-3` for feature history

**Pass Example**:
```markdown
**Execute `post-phase-3` hooks:**

```bash
python3 hooks/runner.py post-phase-3 --context '{
  "phase": "phase-3",
  "feature_slug": "<slug>",
  "complexity": "<category>",
  "files_modified": ["<files>"]
}'
```
```

---

### IN-015: Intégration validate_command.py

**Severity**: INFO

**Check**: Document if command integrates with validation script

**Pass Example**:
```markdown
## Validation

Run validation:
```bash
python scripts/validate_command.py commands/my-command.md
```
```

---

## Integration Points Matrix

| Integration | Section | Required When |
|-------------|---------|---------------|
| Skills | Configuration | Skills used |
| Subagents | Configuration | `@agent` invoked |
| Hooks | Process steps | Hooks executed |
| MCP | Configuration | MCP servers used |
| Personas | Configuration | Persona detection |
| Routing | Routing table | Multiple outputs |
| Memory | Process end | Affects memory |

---

## Validation Pseudocode

```python
def validate_integration(content: str) -> list[Violation]:
    violations = []

    # IN-001: Check skills documentation
    skill_refs = re.findall(r'(project-memory|epci-core|architecture-patterns)', content)
    has_skills_section = 'Skills' in content or '**Skills**' in content
    if skill_refs and not has_skills_section:
        violations.append(Violation('IN-001', 'ERREUR', 'Skills not documented'))

    # IN-002: Check subagent documentation
    subagent_refs = re.findall(r'@(\w+)', content)
    known_subagents = {'Explore', 'clarifier', 'planner', 'implementer'}
    used_subagents = [s for s in subagent_refs if s in known_subagents]
    if used_subagents:
        has_subagent_doc = any(s in content.upper() for s in ['SUBAGENT', 'CONFIGURATION'])
        if not has_subagent_doc:
            violations.append(Violation('IN-002', 'ERREUR', 'Subagents not documented'))

    # IN-008: Check MANDATORY markers
    breakpoints = re.findall(r'BREAKPOINT', content)
    mandatory_markers = re.findall(r'MANDATORY', content)
    if breakpoints and not mandatory_markers:
        violations.append(Violation('IN-008', 'ERREUR', 'Breakpoints not marked MANDATORY'))

    # IN-009: Check output paths
    if not re.search(r'Output|output.*path|→.*docs/', content, re.IGNORECASE):
        violations.append(Violation('IN-009', 'ERREUR', 'Output paths not documented'))

    return violations
```

---

*Integration Rules v1.0.0 — Command Auditor*
