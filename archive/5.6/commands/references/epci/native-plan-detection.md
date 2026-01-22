# Native Plan Detection — Complete Workflow

> Detailed workflow for auto-detecting and integrating Claude Code's native plan mode output into EPCI.

## Overview

Auto-detect and import a native Claude Code plan as the base for EPCI Phase 1 planning. The native plan is copied into the Feature Document for full traceability and team collaboration.

**Triggered by:** Auto-detection when argument `@<path>` contains `docs/plans/` or has `saved_at` frontmatter

**Detection Algorithm:**
```python
def is_native_plan(file_path):
    """Auto-detect a saved native plan."""
    # Criterion 1: Path in docs/plans/
    if "docs/plans/" in file_path:
        return True

    # Criterion 2 (fallback): Frontmatter with saved_at
    content = read_file(file_path)
    frontmatter = parse_yaml_frontmatter(content)
    if frontmatter and "saved_at" in frontmatter:
        return True

    return False
```

**Benefits:**
- Native plan preserved in git (full traceability)
- Phase 1 refines high-level plan into atomic tasks
- Team can see original reasoning
- Project remains autonomous (no external dependencies)

---

## Process (5 Steps)

### Step 1: Read Native Plan File

**Action:** Use Read tool to read the native plan file

```
Read <file-path>
  → File can be anywhere (e.g., ~/.claude/plans/plan.md)
  → Extract full content
  → Store in memory as native_plan_content
```

**Error handling:**

```
IF file not found OR unreadable:
  ╔══════════════════════════════════════════════════════════════╗
  ║ ❌ ERROR: Native Plan File Not Found                         ║
  ╠══════════════════════════════════════════════════════════════╣
  ║ File: <file-path>                                            ║
  ║                                                              ║
  ║ → Verify the file path is correct                            ║
  ║ → Ensure you have read permissions                           ║
  ╚══════════════════════════════════════════════════════════════╝
  ABORT workflow
```

---

### Step 2: Check Feature Document Status

**Action:** Determine if Feature Document exists and if §1 is complete

```
status = {
  "doc_exists": exists(docs/features/<slug>-*.md),
  "section1_exists": contains_section("## §1 — Brief Fonctionnel"),
  "section1_complete": has_required_fields(§1)
}
```

**Decision tree:**

| Status | Action |
|--------|--------|
| Doc missing | Create Feature Document + Generate §1 via @Explore |
| Doc exists, §1 missing | Generate §1 via @Explore |
| Doc exists, §1 incomplete | Generate complete §1 via @Explore |
| Doc exists, §1 complete | Use existing §1 (skip exploration) |

---

### Step 3: Conditional Exploration (if §1 missing or incomplete)

**When to run:** §1 does not exist or is incomplete

**Action:** Invoke @Explore agent to generate §1

```
Invoke @Explore via Task tool with:
  - Subagent: "Explore"
  - Model: haiku (if --turbo) OR default
  - Prompt: "Analyze project for: <brief-from-native-plan>
    - Scan complete project structure
    - Identify all technologies, frameworks, versions
    - Map architectural patterns
    - Identify files potentially impacted
    - Estimate dependencies and coupling
    - Detect existing test patterns"
```

**Generate §1 from @Explore results:**

Use the exploration results to create a complete §1 Brief Fonctionnel with:
- **Objectif**: Extracted from native plan summary
- **Contexte Technique**: From @Explore (stack, dependencies)
- **Fichiers Identifiés**: From @Explore
- **Patterns Architecturaux**: From @Explore
- **Critères d'Acceptation**: From native plan
- **Risques**: From @Explore
- **Memory Summary**: From project-memory skill

---

### Step 4: Create/Update Feature Document with Native Plan

**Action:** Write or update Feature Document with §1 and §2 (native plan)

**Use Write or Edit tool** to create/update `docs/features/<slug>-<YYYYMMDD-HHmmss>.md`:

```markdown
# Feature Document — [Title from native plan]

## §1 — Brief Fonctionnel

### Objectif
[Extracted from native plan or user input]

### Contexte Technique
**Stack détecté**: [From @Explore]
**Frameworks**: [From @Explore]
**Patterns**: [From @Explore]

### Fichiers Identifiés
[From @Explore - list of impacted files]

### Critères d'Acceptation
[From native plan]

### Risques Identifiés
[From @Explore]

### Memory Summary
[From project-memory skill]

---

## §2 — Plan d'Implémentation

### 📋 Source du Plan

- **Type**: Plan natif Claude Code
- **Fichier source**: `<file-path>`
- **Importé le**: [Current date/time]
- **Statut**: ⚠️ Base à raffiner par EPCI Phase 1

---

### 📝 Plan Original (Natif)

<details>
<summary>Voir le plan natif complet</summary>

[FULL NATIVE PLAN CONTENT COPIED HERE]

</details>

---

### ✅ Plan Raffiné & Validé

_[À remplir par Phase 1 — Planification]_

Phase 1 will:
- Break down native plan into atomic tasks (2-15 min each)
- Add test planning for each task
- Order by dependencies
- Validate with @plan-validator

---

## §3 — Implementation & Finalization

_[À remplir par Phases 2-3]_
```

**Confirmation message:**

```
✅ Native plan imported successfully

📄 Feature Document: docs/features/<slug>-<YYYYMMDD-HHmmss>.md
  ├─ §1 Brief Fonctionnel: [CREATED from @Explore | EXISTING]
  └─ §2 Plan Original (Natif): IMPORTED

🔄 Next: Phase 1 will refine the native plan into atomic tasks
```

---

### Step 5: Proceed to Feature Document Prerequisite Check

After import is complete, continue to the normal "Feature Document Prerequisite Check" section in the main `/epci` workflow.

Since the Feature Document was just created or updated, the prerequisite check should pass automatically.

---

## Workflows Supported

### Workflow A: Via /brief (Recommended)
```bash
# 1. Create plan in Claude Code native mode
<mode plan natif>
# → ~/.claude/plans/random-name.md

# 2. Save to project
/save-plan
# → docs/plans/auth-oauth-20260120-143052.md

# 3. Use directly with /brief (AUTO-DETECTION)
/brief @docs/plans/auth-oauth-20260120-143052.md
# → Detects native plan automatically
# → Creates §1 via @Explore
# → Routes to /quick or /epci with context
```

### Workflow B: Direct /epci with context
```bash
# After saving plan to docs/plans/
/epci auth-oauth @docs/plans/auth-oauth-20260120-143052.md
# → Auto-detects native plan (docs/plans/ path)
# → Uses existing §1 or creates via @Explore
# → Imports native plan to §2
# → Refines in Phase 1
```

### Workflow C: /quick with native plan (Fast Path)
```bash
/quick "small fix" @docs/plans/fix-20260120.md
# → Auto-detects native plan (docs/plans/ path)
# → Skips [E] and [P] phases
# → Extracts tasks from plan content
# → Goes directly to [C] with Sonnet (SMALL)
# → Executes [T] for validation
```

**Comportement Fast Path:**

| Phase | Action |
|-------|--------|
| [PRE] | Detection + extraction taches du plan |
| [E] | **SKIP** |
| [P] | **SKIP** |
| [C] | Execution des taches extraites (Sonnet) |
| [T] | Validation tests + lint |

### Workflow D: Hybrid (after /brief without plan)
```bash
/brief "feature description"
# → Creates §1

# Later: generate additional native plan
<mode plan natif>
/save-plan

# Use with existing Feature Document
/epci feature-slug @docs/plans/plan-20260120.md
# → Uses existing §1
# → Imports native plan to §2
# → Refines in Phase 1
```

---

## Quality Guarantees

- ✅ **Traceability**: Native plan archived in project git
- ✅ **Exploration**: §1 always complete (via @Explore if needed)
- ✅ **Validation**: Phase 1 validates with @plan-validator
- ✅ **Team visibility**: All developers see original reasoning
- ✅ **No external dependencies**: Plan copied into project

---

## Related Documentation

- **Main command**: `/epci`
- **Brief workflow**: `/brief`
- **@Explore agent**: Native Claude Code agent
- **@plan-validator**: subagent `plan-validator`
- **Project memory**: skill `project-memory`
