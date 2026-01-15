# Native Plan Import — Complete Workflow

> Detailed workflow for importing Claude Code's native plan mode output into EPCI.

## Overview

Import a native Claude Code plan as the base for EPCI Phase 1 planning. The native plan is copied into the Feature Document for full traceability and team collaboration.

**Triggered by:** `--from-native-plan <file>` flag on `/epci` command

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
  "doc_exists": exists(docs/features/<slug>.md),
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

**Use Write or Edit tool** to create/update `docs/features/<slug>.md`:

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

📄 Feature Document: docs/features/<slug>.md
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

### Workflow A: Standalone Native Plan
```bash
<generate plan in Claude Code native mode>
/epci --from-native-plan ~/.claude/plans/plan.md --slug feature-name
# → Creates §1 via @Explore
# → Imports native plan to §2
# → Refines in Phase 1
```

### Workflow B: Hybrid (after /brief)
```bash
/brief "feature description"
# → Creates §1

<generate additional native plan>
/epci --from-native-plan ~/.claude/plans/plan.md --slug feature-name
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

- **Main command**: `src/commands/epci.md`
- **Brief workflow**: `src/commands/brief.md`
- **@Explore agent**: Native Claude Code agent
- **@plan-validator**: `src/agents/plan-validator.md`
- **Project memory**: `src/skills/core/project-memory/SKILL.md`
