---
description: >-
  Generate .claude/rules/ structure for a project. Performs 3-level detection
  (stack, architecture, conventions), generates CLAUDE.md and contextual rules,
  then validates via @rules-validator. Also supports incremental rule addition
  via auto-detection or --add flag.
argument-hint: "[--force] [--validate-only] [--dry-run] [--stack <name>] [--add] [\"rule text\"]"
allowed-tools: [Read, Write, Glob, Grep, Bash, Task]
---

# EPCI Rules — Rules Generator

## Overview

This command generates the `.claude/rules/` structure for a project.
It detects the technology stack, analyzes architecture, and creates
contextual rules files tailored to the project.

## Configuration

| Element       | Value                                                    |
| ------------- | -------------------------------------------------------- |
| **Thinking**  | `think` (default) / `think hard` (complex monorepo)      |
| **Skills**    | rules-generator, project-memory, [stack-skill detected]  |
| **Subagents** | @Explore (quick), @rules-validator, @rule-clarifier      |

## Arguments

| Argument          | Description                                      |
| ----------------- | ------------------------------------------------ |
| `--force`         | Overwrite existing `.claude/` directory          |
| `--validate-only` | Only validate existing rules, no generation      |
| `--dry-run`       | Show what would be generated without writing     |
| `--stack <name>`  | Force stack detection (django, symfony, react, springboot, frontend-editor) |
| `--no-validate`   | Skip validation step after generation            |
| `--add`           | Force incremental rule addition mode (auto-detected otherwise) |

## Process

### Step 0: Input Classification & Routing

**Reference**: `rules-generator/references/rule-classifier.md`

1. **Parse input and flags**
   - If `--add` flag present → **Mode ADD** (Step A1)
   - If explicit flags (`--force`, `--validate-only`, `--dry-run`, `--stack`) → **Mode GENERATE** (Step 1)
   - Else → Classify input text

2. **Auto-detect rule input** (if no explicit flags)
   
   Score the input for rule indicators:
   
   | Indicateur | Score |
   |------------|-------|
   | "toujours", "jamais", "doit", "ne pas" | +0.2 each |
   | "devrait", "préférer", "éviter", "convention" | +0.2 each |
   | Structure [contexte] + [action] | +0.2 |
   | "?" en fin (question) | -0.3 |
   
   **Routing**:
   - Score >= 0.7 → **Mode ADD** (Step A1)
   - Score 0.4-0.7 → Demander confirmation
   - Score < 0.4 → **Mode GENERATE** (Step 1)

3. **Pre-checks (Mode GENERATE only)**
   - If `.claude/` exists and `--force` not provided:
     ```
     ⚠️  .claude/ existe déjà. Utilisez --force pour écraser.
     ```
   - If `--validate-only`: Skip to Step 4 (Validation)

4. **Load project memory** (if `.project-memory/` exists)
   - Extract project name, conventions, patterns

---

### Mode ADD: Incremental Rule Addition

> **Skip to Step 1 if Mode GENERATE**

#### Step A1: Clarity Assessment

**Reference**: `rules-generator/references/rule-classifier.md`

Calculate clarity score:

| Élément | Score |
|---------|-------|
| Scope explicite ("fichiers Python", "dans backend/") | +0.4 |
| Scope déductible du contexte | +0.2 |
| Sévérité détectable (mots-clés) | +0.3 |
| Contenu actionnable (verbe d'action) | +0.2 |
| Longueur > 5 mots | +0.1 |

**Routing**:
- Clarity >= 0.8 → Step A3 (Reformulation directe)
- Clarity < 0.8 → Step A2 (Clarification)

---

#### Step A2: Clarification

**Subagent**: `@rule-clarifier` (Haiku)

Invoke @rule-clarifier for fast clarification:

```
Task: Clarifier la règle suivante
Input: "[user input]"
Context: Structure projet, fichiers .claude/rules/ existants
```

**Questions possibles** (max 3, one-at-a-time):

1. **Scope** (si non détecté):
   ```
   Quel scope pour cette règle ?
     A) Tous les fichiers Python (**/*.py)
     B) Backend uniquement (backend/**/*.py)
     C) Frontend (frontend/**/*.tsx)
     D) Autre (précisez)
   
   Suggestion: [B] basé sur la structure projet
   ```

2. **Sévérité** (si non détectée):
   ```
   Quelle sévérité ?
     A) 🔴 CRITICAL — Ne jamais violer
     B) 🟡 CONVENTIONS — Standard du projet
     C) 🟢 PREFERENCES — Recommandé mais flexible
   
   Suggestion: [B] basé sur "devrait"
   ```

3. **Formulation** (si trop vague):
   ```
   Pouvez-vous préciser la règle ?
   Actuel: "Faire attention aux injections"
   Suggestion: "Toujours utiliser des requêtes paramétrées pour éviter les injections SQL"
   ```

---

#### Step A3: Reformulation & Validation

Afficher la règle reformulée :

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📝 RÈGLE DÉTECTÉE                                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Contenu  : "Toujours utiliser des type hints pour les fonctions    │
│             publiques"                                              │
│ Sévérité : 🟡 CONVENTIONS                                           │
│ Scope    : backend/**/*.py                                          │
│ Placement: .claude/rules/python-conventions.md (existant)           │
│                                                                     │
│ [1] ✅ Valider et ajouter                                           │
│ [2] ✏️  Modifier                                                     │
│ [3] ❌ Annuler                                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Si [2] Modifier** → Retour Step A2 avec input modifié
**Si [3] Annuler** → Fin
**Si [1] Valider** → Step A4

---

#### Step A4: Placement Decision

**Logique de placement** (automatique):

```
IF scope est global (vide ou **/*):
   → CLAUDE.md
ELSE:
   → Chercher fichier .claude/rules/*.md avec paths similaires
   
   IF overlap >= 70%:
      → Append au fichier existant
   ELSE:
      → Créer nouveau fichier rules/*.md
```

**Naming nouveau fichier**:

| Scope | Nom fichier |
|-------|-------------|
| `**/*.py` | `python-conventions.md` |
| `backend/**/*.py` | `backend-python.md` |
| `frontend/**/*.tsx` | `frontend-react.md` |
| `**/test_*.py` | `testing-python.md` |
| Autre | `rules-custom.md` |

---

#### Step A5: Integration

1. **Si CLAUDE.md**:
   - Lire le fichier existant
   - Identifier section appropriée (créer si nécessaire)
   - Ajouter la règle en format bullet point

2. **Si rules/*.md existant**:
   - Lire le fichier
   - Identifier section sévérité (🔴/🟡/🟢)
   - Append à la fin de la section
   - Vérifier limite tokens (< 2000)

3. **Si nouveau rules/*.md**:
   ```markdown
   ---
   paths:
     - [extracted_scope]
   ---
   
   # [Category] Conventions
   
   > Règles pour [scope description]
   
   ## 🔴 CRITICAL
   
   ## 🟡 CONVENTIONS
   
   - [new_rule]
   
   ## 🟢 PREFERENCES
   ```

---

#### Step A6: Validation & Completion

**Subagent**: `@rules-validator`

Valider le fichier modifié/créé.

**Si échec**:
```
❌ Validation échouée: [erreur]
💡 Suggestion: [fix]

Voulez-vous corriger ? [O/n]
```

**Si succès**:
```
┌─────────────────────────────────────────────────────────────────────┐
│ ✅ RÈGLE AJOUTÉE                                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📁 Fichier  : .claude/rules/python-conventions.md                   │
│ 📍 Section  : 🟡 CONVENTIONS                                        │
│ 📊 Tokens   : 1450/2000                                             │
│                                                                     │
│ 💡 La règle sera active pour : backend/**/*.py                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Warning si limite proche**:
```
⚠️  Fichier à 90% de la limite (1800/2000 tokens)
💡 Envisagez de créer un nouveau fichier pour les prochaines règles
```

---

### Step 1: Stack Detection (3 Levels)

**Skill**: `rules-generator`

#### Level 1 — Technology Stack

Detect primary stack by analyzing project files:

| Stack         | Detection Pattern                                       |
| ------------- | ------------------------------------------------------- |
| Python/Django | `requirements.txt` OR `pyproject.toml` + django         |
| PHP/Symfony   | `composer.json` + symfony/*                             |
| JS/React      | `package.json` + react                                  |
| Java/Spring   | `pom.xml` OR `build.gradle` + spring-boot               |
| Frontend      | `tailwind.config.*` OR postcss + tailwind               |

**Monorepo detection:**
```
IF backend/ AND frontend/:
   → Detect both stacks
   → Generate combined rules
```

#### Level 2 — Architecture

Analyze project structure:

| Pattern       | Detection                              | Impact           |
| ------------- | -------------------------------------- | ---------------- |
| Clean Arch    | `domain/`, `application/`, `infra/`    | Layer rules      |
| Hexagonal     | `ports/`, `adapters/`                  | Port/adapter rules |
| MVC           | `controllers/`, `views/`, `models/`    | MVC rules        |
| DDD           | `aggregates/`, `valueobjects/`         | DDD rules        |
| Modular       | Multiple independent modules           | Module boundaries |

#### Level 3 — Conventions (AST)

For each detected stack, run AST analysis:

**Python:**
```bash
# Detect naming conventions, decorators, type hints
grep -r "def [a-z_]*(" backend/ | head -20
grep -r "@dataclass\|@validator" backend/ | head -10
```

**TypeScript/React:**
```bash
# Detect component patterns, hooks usage
grep -r "export (default |const )" frontend/src/ | head -20
grep -r "use[A-Z][a-zA-Z]*" frontend/src/ | head -10
```

---

### Step 2: Template Selection

Based on detection, select templates from skill stack folders:

| Detection                | Templates to Use                                            |
| ------------------------ | ----------------------------------------------------------- |
| Django                   | `python-django/rules-templates/backend-django.md`, etc.     |
| Symfony                  | `php-symfony/rules-templates/backend-symfony.md`, etc.      |
| React                    | `javascript-react/rules-templates/frontend-react.md`, etc.  |
| SpringBoot               | `java-springboot/rules-templates/backend-spring.md`, etc.   |
| Frontend (Tailwind)      | `frontend-editor/rules-templates/styling-tailwind.md`, etc. |
| Monorepo (Django+React)  | Django templates + React templates + Frontend templates     |

**Template paths:**
```
src/skills/stack/<stack>/rules-templates/
src/skills/core/rules-generator/templates/  (global templates)
```

---

### Step 3: Generation

Generate `.claude/` structure:

#### 3.1 Create Directory Structure

```bash
mkdir -p .claude/rules
```

#### 3.2 Generate CLAUDE.md

Use template from `src/skills/core/rules-generator/templates/claude-md.md`

**Variables to substitute:**
- `{{project_name}}` → From `.project-memory/context.json` or directory name
- `{{stack}}` → Detected stack(s)
- `{{architecture}}` → Detected patterns
- `{{generated_date}}` → Current date

**Content focus (>50 lines):**
- Project overview
- Architecture decisions
- Development workflow
- Key commands
- Testing strategy
- Deployment notes

#### 3.3 Generate Rules Files

For each selected template:

1. **Read template** from skill folder
2. **Adapt paths** for project structure
3. **Substitute variables** (project name, date, stack)
4. **Write to `.claude/rules/`**

**File naming:**
```
Template: backend-django.md → Output: .claude/rules/backend-django.md
Template: testing-pytest.md → Output: .claude/rules/testing-pytest.md
```

#### 3.4 Generate Global Rules

From `src/skills/core/rules-generator/templates/`:
- `global-quality.md` → `.claude/rules/global-quality.md`
- `global-git-workflow.md` → `.claude/rules/global-git-workflow.md`
- `domain-glossary.md` → `.claude/rules/domain-glossary.md` (if domain terms detected)

---

### Step 4: Validation

**Subagent**: `@rules-validator`

Invoke @rules-validator to validate generated structure:

```
Task: Validate .claude/rules/ structure
Input: Path to .claude/ directory
Expected: VALID | VALID_WITH_WARNINGS | INVALID
```

**If INVALID:**
- Display issues
- Suggest fixes
- Option to regenerate

**If VALID_WITH_WARNINGS:**
- Display warnings
- Continue with completion

---

### Step 5: Completion

Display summary:

```
┌─────────────────────────────────────────────────────────────────────┐
│ ✅  RULES GÉNÉRÉES                                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📁 STRUCTURE CRÉÉE                                                  │
│ ├── .claude/CLAUDE.md (850 tokens)                                 │
│ └── .claude/rules/                                                 │
│     ├── backend-django.md (1200 tokens)                            │
│     ├── testing-pytest.md (980 tokens)                             │
│     ├── api-drf.md (750 tokens)                                    │
│     ├── global-quality.md (600 tokens)                             │
│     └── global-git-workflow.md (450 tokens)                        │
│                                                                     │
│ 📊 DÉTECTION                                                        │
│ ├── Stack: Python/Django + JavaScript/React                        │
│ ├── Architecture: Clean Architecture                               │
│ └── Conventions: snake_case, type hints, functional components     │
│                                                                     │
│ ✅ VALIDATION: VALID                                                │
│                                                                     │
│ 💡 Les rules seront auto-activées selon les fichiers édités        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Integration with Brief

When `/brief` is called on a project without `.claude/`:

1. **Suggest rules generation:**
   ```
   💡 Aucune règle projet détectée. Voulez-vous générer .claude/rules/ ?
      → Lancez /rules pour créer les conventions projet
   ```

2. **Auto-suggest after Feature completion:**
   - After `/epci` Phase 3, if no `.claude/` exists, suggest `/rules`

---

## Hook Integration

**Post-rules-init hook** (`hooks/active/post-rules-init.py`):
- Log rules generation
- Update `.project-memory/settings.json` with `rules_initialized: true`
- Optional: Notify team (webhook)

---

## Examples

### Basic Usage (Mode GENERATE)

```bash
# Detect stack and generate rules
/epci:rules

# Force regeneration
/epci:rules --force

# Validate existing rules only
/epci:rules --validate-only

# Preview without writing
/epci:rules --dry-run
```

### Incremental Addition (Mode ADD)

```bash
# Auto-detected as rule (high confidence)
/epci:rules "Toujours utiliser des type hints dans le code Python"
→ Reformulation directe, validation, ajout

# Auto-detected as rule (needs clarification)
/epci:rules "Faire attention aux injections SQL"
→ @rule-clarifier asks: scope? severity?

# Force add mode explicitly
/epci:rules --add "Préférer les composants fonctionnels en React"

# Clear rule with explicit scope
/epci:rules "Les fichiers dans backend/ doivent avoir des docstrings"
→ Scope: backend/**/*.py, Severity: CRITICAL (doit)
```

### Mode ADD - Flow Example

```
User: /epci:rules "éviter les any en TypeScript"

Step 0: Auto-detection
├── Score: 0.7 (éviter = rule indicator)
└── → Mode ADD

Step A1: Clarity
├── Scope: non explicite (→ déductible: **/*.ts)
├── Severity: CONVENTIONS (éviter)
└── Clarity: 0.7 → Clarification rapide

Step A2: @rule-clarifier
└── Q1: Quel scope ?
    A) Tous fichiers TS (**/*.ts, **/*.tsx)
    B) Frontend uniquement
    → User: A

Step A3: Reformulation
┌─────────────────────────────────────────┐
│ Contenu  : "Éviter l'utilisation de any"│
│ Sévérité : 🟡 CONVENTIONS               │
│ Scope    : **/*.ts, **/*.tsx            │
│ Placement: .claude/rules/typescript.md  │
└─────────────────────────────────────────┘
→ User: [1] Valider

Step A4-A6: Integration + Validation
→ ✅ Règle ajoutée à typescript.md
```

### Force Specific Stack

```bash
# Force Django detection (when auto-detection fails)
/epci:rules --stack django

# Force multiple stacks for monorepo
/epci:rules --stack django --stack react
```

### Monorepo Example

For project structure:
```
myproject/
├── backend/          # Django
│   ├── apps/
│   └── requirements.txt
├── frontend/         # React
│   ├── src/
│   └── package.json
└── shared/           # Common
```

Detection output:
```
Stack détecté:
├── Backend: Python/Django (backend/)
├── Frontend: JavaScript/React (frontend/)
└── Styling: Tailwind CSS (frontend/tailwind.config.js)

Rules générées:
├── backend-django.md (paths: backend/**/*.py)
├── testing-pytest.md (paths: backend/**/test_*.py)
├── frontend-react.md (paths: frontend/**/*.tsx)
├── styling-tailwind.md (paths: frontend/**/*.css)
└── global-quality.md (paths: **/*)
```

---

## Error Handling

| Error                        | Message                                      | Solution                  |
| ---------------------------- | -------------------------------------------- | ------------------------- |
| No stack detected            | "Aucun stack reconnu"                        | Use `--stack` flag        |
| .claude/ exists              | ".claude/ existe déjà"                       | Use `--force`             |
| Template not found           | "Template manquant: {name}"                  | Check skill installation  |
| Validation failed            | "Règles invalides"                           | Fix issues, regenerate    |
| Permission denied            | "Impossible de créer .claude/"               | Check directory perms     |

---

## Validation Script Integration

Use the validation script for CI/CD:

```bash
# Validate rules after generation
python3 src/scripts/validate_rules.py .claude/rules/ --verbose

# Expected output:
# [OK] CLAUDE.md: Valid structure
# [OK] rules/backend-django.md: Valid frontmatter, 1200 tokens
# [OK] rules/testing-pytest.md: Valid frontmatter, 980 tokens
# VALIDATION REPORT: PASSED (5/5 files valid)
```
