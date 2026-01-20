# Content Rules — RD-001 to RD-025 + WF-001 to WF-010

> Validation rules for content quality and workflow logic

---

## Part 1: Rédaction Rules (RD)

### RD-001: Longueur totale < 5000 tokens

**Severity**: BLOQUANT

**Check**: Estimated token count < 5000

**Estimation**: `len(content) // 4` (rough approximation)

**Rationale**: Commands exceeding 5000 tokens consume too much context window

**Fix**: Extract content to skills or references

---

### RD-002: Pas de contenu dupliqué

**Severity**: ERREUR

**Check**: No significant text blocks repeated between sections

**Detection**: Find sequences > 50 chars appearing twice

**Fix**: Consolidate duplicate content; reference from one location

---

### RD-003: Code blocks avec langage spécifié

**Severity**: WARNING

**Check**: Code blocks specify language after opening backticks

**Pass Example**:
````markdown
```yaml
description: My command
```
````

**Fail Example**:
````markdown
```
description: My command
```
````

**Fix**: Add language identifier: `yaml`, `markdown`, `bash`, `python`, etc.

---

### RD-004: Tables pour données structurées

**Severity**: WARNING

**Check**: When presenting multiple items with consistent attributes → use tables

**Pass Example**:
```markdown
| Flag | Effect | Default |
|------|--------|---------|
| `--strict` | Enable strict | Yes |
```

**Fail Example**:
```markdown
The --strict flag enables strict mode and is on by default.
The --lenient flag disables strict mode.
```

**Fix**: Convert parallel structures to tables

---

### RD-005: Références externes avec syntaxe `@`

**Severity**: ERREUR

**Check**: File references use `@path/to/file` syntax

**Pass Example**:
```markdown
Review the implementation in @utils/helpers.js
```

**Fail Example**:
```markdown
Review the implementation in `src/utils/helpers.js`
Review the implementation in [helpers.js](src/utils/helpers.js)
```

**Fix**: Use `@` prefix for file references

---

### RD-006: Pas de liens markdown pour refs internes

**Severity**: ERREUR

**Check**: No `[text](path)` for internal file references

**Rationale**: Claude Code uses `@` syntax, not markdown links

**Exception**: Links to reference files within skill are OK

**Pass Example**:
```markdown
See @commands/brief.md
See [details](references/details.md)  # OK for skill refs
```

**Fail Example**:
```markdown
See [brief.md](src/commands/brief.md)
```

---

### RD-007: Invocations subagents format `@name`

**Severity**: ERREUR

**Check**: Subagent references use `@subagent-name` format

**Valid Subagents**: `@Explore`, `@clarifier`, `@planner`, `@implementer`, `@plan-validator`, `@code-reviewer`, `@security-auditor`, `@qa-reviewer`, `@doc-generator`

**Pass Example**:
```markdown
Invoke @Explore via Task tool with thoroughness: thorough
```

**Fail Example**:
```markdown
Invoke the Explore agent
Use Explore subagent
```

**Fix**: Use `@name` format consistently

---

### RD-008: Impératifs pour instructions

**Severity**: WARNING

**Check**: Instructions use imperative verbs

**Good**: Use, Create, Run, Check, Validate, Generate, Extract
**Avoid**: You should use, Claude will create, The system runs

**Pass Example**:
```markdown
Read the target file.
Parse YAML frontmatter.
Validate against rules.
```

**Fail Example**:
```markdown
The command will read the target file.
Claude should parse the YAML frontmatter.
```

---

### RD-009: Conditions explicites

**Severity**: ERREUR

**Check**: Conditional logic uses explicit keywords

**Required Keywords**: `IF`, `WHEN`, `UNLESS`, `ELSE`, `OTHERWISE`

**Pass Example**:
```markdown
IF frontmatter missing → mark FM-001 BLOQUANT
WHEN score < 70 → verdict = FAIL
```

**Fail Example**:
```markdown
If the frontmatter is missing, mark it as blocking.
```

**Fix**: Use uppercase conditional keywords for clarity

---

### RD-010: Pas de double négation

**Severity**: WARNING

**Check**: No double negative constructions

**Fail Examples**:
- "Don't not include..."
- "Never fail to not..."
- "Unless not specified..."

**Fix**: Rewrite positively

---

### RD-011: Flags format `--flag-name`

**Severity**: ERREUR

**Check**: Flags use double-dash kebab-case format

**Pass Example**: `--strict`, `--no-mermaid`, `--output-json`

**Fail Example**: `-strict`, `--StrictMode`, `strict`

---

### RD-012: Pas de chemins hardcodés absolus

**Severity**: ERREUR

**Check**: No absolute paths like `/home/user/`, `/Users/`, `C:\`

**Exception**: Example paths clearly marked as examples

**Pass Example**:
```markdown
Output to `docs/audits/{command}-audit.md`
```

**Fail Example**:
```markdown
Output to `/home/epci/apps/docs/audits/audit.md`
```

**Fix**: Use relative paths or placeholders

---

### RD-013: Variables placeholders format correct

**Severity**: WARNING

**Check**: Placeholders use `{variable}` or `$variable` format

**Pass Example**:
```markdown
Output: `docs/audits/{command_name}-audit.md`
Score: $SCORE/100
```

**Fail Example**:
```markdown
Output: `docs/audits/<command_name>-audit.md`
Score: SCORE/100
```

---

### RD-014: Cohérence terminologie

**Severity**: ERREUR

**Check**: Consistent term usage throughout

**Common Inconsistencies**:
- "command" vs "commande" (pick one language)
- "BLOQUANT" vs "blocking" vs "critical"
- "file" vs "fichier"

**Fix**: Use consistent terminology; define in glossary if needed

---

### RD-015: Pas de TODO/FIXME/XXX

**Severity**: ERREUR

**Check**: No development markers in final content

**Detection**: Case-insensitive search for `TODO`, `FIXME`, `XXX`, `HACK`

**Fix**: Complete the TODO or remove the marker

---

### RD-016: Pas de commentaires personnels

**Severity**: ERREUR

**Check**: No personal notes or opinions

**Fail Examples**:
- "I think this should..."
- "We might want to..."
- "Note to self:..."

**Fix**: Use objective, instructional language

---

### RD-017: Emojis limités

**Severity**: WARNING

**Check**: Emojis only in breakpoints and section headers

**Allowed Locations**:
- Breakpoint headers: `⏸️ BREAKPOINT`
- Section indicators: `📊 EXPLORATION`

**Not Allowed**: Inline text emojis

---

### RD-018: Références `@` pointent vers fichiers existants

**Severity**: BLOQUANT

**Check**: All `@path/to/file` references resolve to actual files

**Detection**: Extract `@` references; verify file existence

**Fix**: Correct path or remove broken reference

---

### RD-019: Contexte dynamique `!` < 30 lignes

**Severity**: WARNING

**Check**: Section with `!` commands < 30 lines

**Rationale**: Excessive bash injection pollutes context

**Pass Example**:
```markdown
## Context
- Status: !`git status --short`
- Branch: !`git branch --show-current`
```

**Fail Example**: 50+ lines of `!` commands

---

### RD-020: Instructions < 100 lignes

**Severity**: WARNING

**Check**: Individual instruction sections < 100 lines

**Fix**: Break into steps or extract to reference

---

### RD-021: Frontmatter < 15 lignes

**Severity**: WARNING

**Check**: Same as FM-005 (cross-reference)

---

### RD-022: Spécificité

**Severity**: ERREUR

**Check**: Command has single, clear purpose

**Detection**: Look for "and also", "additionally can", multiple unrelated outputs

**Pass**: "Audit commands against best practices"
**Fail**: "Audit commands and generate documentation and run tests"

---

### RD-023: Déterminisme

**Severity**: WARNING

**Check**: Same inputs produce same outputs

**Detection**: Look for random elements, uncontrolled external dependencies

---

### RD-024: Testabilité

**Severity**: WARNING

**Check**: Output can be verified by user

**Pass**: Clear success/failure criteria
**Fail**: Vague "it should work better"

---

### RD-025: Maintenabilité

**Severity**: WARNING

**Check**: Command is easy to modify

**Indicators**:
- Clear section separation
- No magic numbers
- Documented dependencies

---

## Part 2: Workflow Rules (WF) {#workflow-rules}

### WF-001: Workflow cohérent

**Severity**: BLOQUANT

**Check**: No orphan steps (steps not connected to main flow)

**Detection**: Build step graph; verify all steps reachable from start

**Pass Example**:
```markdown
### Step 1: Load → Step 2: Validate → Step 3: Report
```

**Fail Example**:
```markdown
### Step 1: Load
### Step 2: Validate
### Step X: Orphan step (never referenced)
```

---

### WF-002: Séquence logique

**Severity**: ERREUR

**Check**: Steps follow logical order

**Detection**: Verify no step references results from later step

**Pass**: Step 2 uses output of Step 1
**Fail**: Step 1 uses output of Step 3

---

### WF-003: Pas de boucles infinies

**Severity**: BLOQUANT

**Check**: No unconditional loops back without exit condition

**Pass Example**:
```markdown
IF errors found → retry (max 3 times) → ELSE continue
```

**Fail Example**:
```markdown
IF errors found → go back to Step 1
```

**Fix**: Add loop limits or exit conditions

---

### WF-004: Points de sortie explicites

**Severity**: ERREUR

**Check**: All paths lead to explicit end state

**Required**: At least one "End", "Complete", "Output" terminal

**Detection**: Build flow graph; verify all paths terminate

---

### WF-005: Conditions IF/ELSE complètes

**Severity**: ERREUR

**Check**: All conditionals have both branches documented

**Pass Example**:
```markdown
IF score >= 90 → PASS
ELSE IF score >= 70 → WARN
ELSE → FAIL
```

**Fail Example**:
```markdown
IF score >= 90 → PASS
(what happens otherwise?)
```

---

### WF-006: Étapes critiques marquées MANDATORY

**Severity**: ERREUR

**Check**: Important steps marked as mandatory

**Detection**: Look for breakpoints, user interaction → should be MANDATORY

**Pass Example**:
```markdown
### Step 4: BREAKPOINT (MANDATORY)
```

---

### WF-007: Breakpoints aux points de décision

**Severity**: WARNING

**Check**: User decision points have breakpoints

**When Required**:
- Before destructive operations
- When multiple paths available
- Before external actions (commits, deploys)

---

### WF-008: Fallbacks documentés

**Severity**: WARNING

**Check**: Error scenarios have documented recovery

**Pass Example**:
```markdown
| Error | Recovery |
|-------|----------|
| File not found | Skip with warning |
| Parse error | Mark as FAIL, continue |
```

---

### WF-009: Workflow représentable en DAG

**Severity**: ERREUR

**Check**: Workflow is a Directed Acyclic Graph (no cycles)

**Detection**: Topological sort possible

**Exception**: Explicit retry loops with limits are OK

---

### WF-010: Routing documenté

**Severity**: WARNING

**Check**: When routing to other commands, document conditions

**Pass Example**:
```markdown
| Category | Route To |
|----------|----------|
| TINY/SMALL | `/quick` |
| STANDARD/LARGE | `/epci` |
```

---

## Validation Pseudocode

```python
def validate_content(content: str) -> list[Violation]:
    violations = []

    # RD-001: Token estimate
    tokens = len(content) // 4
    if tokens >= 5000:
        violations.append(Violation('RD-001', 'BLOQUANT', f'Too many tokens: ~{tokens}'))

    # RD-015: TODO markers
    if re.search(r'\b(TODO|FIXME|XXX|HACK)\b', content, re.IGNORECASE):
        violations.append(Violation('RD-015', 'ERREUR', 'Development markers found'))

    # RD-018: Verify @ references
    refs = re.findall(r'@([\w/.-]+)', content)
    for ref in refs:
        if not Path(ref).exists():
            violations.append(Violation('RD-018', 'BLOQUANT', f'Broken reference: @{ref}'))

    # WF-001: Check step connectivity
    steps = extract_steps(content)
    if has_orphan_steps(steps):
        violations.append(Violation('WF-001', 'BLOQUANT', 'Orphan steps detected'))

    return violations
```

---

*Content Rules v1.0.0 — Command Auditor*
