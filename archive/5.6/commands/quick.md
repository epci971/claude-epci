---
description: >-
  Execute autonomous EPCT workflow for TINY and SMALL features. Four phases:
  Explore, Plan, Code, Test with adaptive model switching (Haiku/Sonnet).
  TINY mode: <50 LOC, 1 file. SMALL mode: <200 LOC, 2-3 files.
argument-hint: "[--confirm] [--quick-turbo] [--uc] [--turbo] [--no-hooks]"
allowed-tools: [Read, Write, Edit, Bash(npm:*), Bash(pytest:*), Bash(php:*), Bash(eslint:*), Bash(flake8:*), Bash(git:*), Grep, Glob, Task]
---

# EPCI Quick — EPCT Workflow

## Overview

Workflow autonome suivant la logique EPCT (Explore, Plan, Code, Test) pour features TINY et SMALL.
Optimise pour la vitesse avec switching de modele adaptatif et breakpoints minimaux.

**Caracteristiques cles:**
- Structure 4 phases EPCT
- Switching de modele adaptatif (Haiku pour vitesse, Sonnet pour qualite)
- Breakpoint leger avec auto-continue 3s
- Persistence de session pour reprise/suivi

---

## Modes

### Mode TINY

| Critere | Valeur |
|---------|--------|
| Fichiers | 1 seul |
| LOC | < 50 |
| Tests | Non requis |
| Duree | < 30 secondes cible |
| Exemples | Typo, config, petite correction |

### Mode SMALL

| Critere | Valeur |
|---------|--------|
| Fichiers | 2-3 |
| LOC | < 200 |
| Tests | Optionnels |
| Duree | < 90 secondes cible |
| Exemples | Petite feature, refactor local |

---

## Flags Supportes

### Flags Specifiques Quick (F13)

| Flag | Effet | Auto-Declenchement |
|------|-------|-------------------|
| `--confirm` | Activer breakpoint plan avec attente utilisateur | Jamais (explicite) |
| `--quick-turbo` | Forcer modele Haiku partout (TINY uniquement) | Jamais (explicite) |
| `--bp` | Alias pour `--confirm` | - (alias) |

### Flags Herites

| Flag | Effet | Auto-Declenchement |
|------|-------|-------------------|
| `--uc` | Sortie compressee | contexte > 75% |
| `--turbo` | Mode turbo existant (@implementer, auto-commit) | Jamais |
| `--no-hooks` | Desactiver execution de tous les hooks | Jamais |
| `--safe` | Forcer breakpoints meme avec `--autonomous` | Fichiers sensibles |

**Note:** Les flags thinking (`--think-hard`, `--ultrathink`) declenchent une escalade vers `/epci`.

> Voir @references/quick/flags-matrix.md pour les interactions de flags et matrices completes.

---

## Configuration

| Element | Valeur |
|---------|--------|
| **Thinking** | Adaptatif par phase (voir matrice modeles) |
| **Skills** | project-memory, epci-core, code-conventions, flags-system, breakpoint-display, complexity-calculator, tdd-workflow, [stack] |
| **Subagents** | @Explore, @clarifier, @planner, @implementer (conditionnel) |

> Voir @references/quick/flags-matrix.md pour les matrices modeles et subagents.

---

## EPCT Workflow

**⚠️ IMPORTANT: Suivre TOUTES les phases en sequence.**

```
/quick "description" [@docs/plans/plan.md]
    │
    ▼
[PRE] Detection plan natif ────────────────────────────────────────────
    │
    ├── Plan natif detecte? ───────────────────────┐
    │                                              │
   NON                                            OUI
    │                                              │
    ▼                                              │
[E] EXPLORE ───────────────────────────────────    │
    │                                              │
    ▼                                              │
[P] PLAN ──────────────────────────────────────    │
    │       ⏸️ BP leger (SI --confirm)            │
    │                                              │
    └──────────────────────────────────────────────┘
                        │
                        ▼
[C] CODE ─────────────────────────────────────────────────────────────
    │         (Sonnet pour plan natif / Adaptatif sinon)
    ▼
[T] TEST ─────────────────────────────────────────────────────────────
    │
    ▼
[RESUME FINAL] ───────────────────────────────────────────────────────
```

### [PRE] Detection Plan Natif (AVANT [E])

**⚠️ Cette phase s'execute AVANT [E] et determine le chemin d'execution.**

**SI argument contient `@<path>`:**

```python
path = extract_path(argument)
IF is_native_plan(path):
    # === FAST PATH: Skip [E] et [P] ===
    native_plan_content = read_file(path)
    tasks = extract_tasks_from_plan(native_plan_content)
    complexity = "SMALL"  # Defaut — plan natif implique complexite minimale
    native_plan_mode = True

    # Afficher info
    print("⚡ Plan natif detecte → Mode accelere [C][T]")
    print(f"   Source: {path}")
    print(f"   Taches extraites: {len(tasks)}")

    # GOTO Phase [C] directement
    GOTO_PHASE_C(tasks, complexity)

ELSE:
    # Standard path — continuer vers [E]
    native_plan_mode = False
    GOTO_PHASE_E()
```

**Algorithme `is_native_plan()`:**
```python
def is_native_plan(file_path):
    if "docs/plans/" in file_path:
        return True
    frontmatter = parse_yaml_frontmatter(read_file(file_path))
    if frontmatter and "saved_at" in frontmatter:
        return True
    return False
```

**Algorithme `extract_tasks_from_plan(content)`:**
```python
def extract_tasks_from_plan(content):
    """
    Extrait les taches d'un plan natif.
    Supporte plusieurs formats courants.
    """
    tasks = []

    # Format 1: Checkboxes markdown
    # - [ ] Task description
    # - [x] Completed task
    checkbox_pattern = r'- \[[ x]\] (.+)'
    tasks.extend(re.findall(checkbox_pattern, content))

    # Format 2: Numbered lists
    # 1. Task description
    # 2. Another task
    numbered_pattern = r'^\d+\.\s+(.+)'
    if not tasks:
        tasks.extend(re.findall(numbered_pattern, content, re.MULTILINE))

    # Format 3: Section headers as tasks
    # ## Task 1: Description
    # ### Implementation step
    header_pattern = r'^##+ (?:Task|Step|Etape).*?:\s*(.+)'
    if not tasks:
        tasks.extend(re.findall(header_pattern, content, re.MULTILINE | re.IGNORECASE))

    # Format 4: Bullet points under "Tasks" or "Plan" section
    if not tasks:
        section_match = re.search(r'(?:Tasks|Plan|Implementation):\s*\n((?:[-*]\s+.+\n?)+)', content, re.IGNORECASE)
        if section_match:
            bullets = re.findall(r'[-*]\s+(.+)', section_match.group(1))
            tasks.extend(bullets)

    # Fallback: Si aucune tache trouvee, creer une tache unique
    if not tasks:
        first_header = re.search(r'^#\s+(.+)', content, re.MULTILINE)
        if first_header:
            tasks = [f"Implementer: {first_header.group(1)}"]
        else:
            tasks = ["Implementer selon le plan fourni"]

    return tasks[:5]  # Maximum 5 taches pour SMALL
```

---

### [E] EXPLORE Phase (5-10s)

**⚠️ Phase sautee si plan natif detecte en [PRE]**

**Modele:** Haiku (TINY et SMALL)

**Skill:** `complexity-calculator`

Collecte rapide du contexte et verification de la complexite via skill.

**Step 1: Collecte contexte**

1. Collecter contexte via @Explore (quick mode)
2. Invoquer `@skill:complexity-calculator` avec donnees exploration:
   ```yaml
   @skill:complexity-calculator
     input:
       brief: "{brief_text}"
       files_impacted: [{path: "...", action: "..."}]
       exploration_results: {...}
   ```
3. Analyser resultat:
   - SI brief absent → Suggerer `/brief` d'abord
   - SI category > SMALL → Escalader vers `/epci`
   - SI category == TINY/SMALL → Continuer workflow
4. Stocker category pour resume final

> Voir documentation du skill `complexity-calculator` pour details.

### [P] PLAN Phase (10-15s)

**⚠️ Phase sautee si plan natif detecte en [PRE]**

**Modele:** Haiku (TINY) | Sonnet + `think` (SMALL)

Generation du decoupage atomique des taches.

**Taches:**
- TINY: 1-2 taches maximum (inline, sans subagent)
- SMALL: 3-5 taches atomiques
- SMALL+ (proche limite): Invoquer @planner (Sonnet) via Task tool

**⏸️ Breakpoint leger** (SI `--confirm`): via `@skill:breakpoint-display type:lightweight`

```yaml
@skill:breakpoint-display
  type: lightweight
  title: "QUICK PLAN"
  data:
    mode: "{TINY|SMALL}"
    tasks:
      - {id: 1, description: "{task 1}"}
      - {id: 2, description: "{task 2}"}
      - {id: 3, description: "{task 3}"}
    auto_continue: 3  # seconds
  ask:  # Only if --confirm flag
    question: "Plan OK ?"
    header: "⏸️ Plan"
    options:
      - {label: "Continuer (Recommended)", description: "Auto-continue dans 3s..."}
      - {label: "Modifier", description: "Ajuster le plan"}
      - {label: "Annuler", description: "Abandonner"}
```

### [C] CODE Phase (variable)

**Modele:** Haiku (TINY) | Sonnet (SMALL et Plan Natif)

**Skill:** `tdd-workflow` (SMALL uniquement)

Execution des taches d'implementation.

**SI `native_plan_mode == true`:**
- Taches = `extracted_tasks` (du plan natif via [PRE])
- Modele = Sonnet (SMALL par defaut pour plan natif)
- Contexte complet = contenu du plan natif (accessible pour reference)

**SINON:**
- Comportement existant (taches de Phase [P])

- **TINY**: Implementation directe (skip TDD formel)
- **SMALL**: Invoquer `@skill:tdd-workflow` avec mode="quick":
  ```yaml
  @skill:tdd-workflow
    input:
      task: "{task_description}"
      mode: "quick"
      stack: "{detected_stack}"
  ```
  - RED: Test simple
  - GREEN: Implementation minimale
  - REFACTOR: Skip (optionnel pour vitesse)
- SI erreur: Reessayer (max 2x), activer recovery du skill

> Voir documentation du skill `tdd-workflow` pour integration /quick.

### [T] TEST Phase (5-10s)

**Modele:** Haiku (validation) | Sonnet + `think hard` (SI correction necessaire)

**Skill:** `tdd-workflow` (phase VERIFY)

Verification de la correction de l'implementation.

- Executer phase VERIFY du skill:
  ```yaml
  @skill:tdd-workflow
    phase: "verify"
    input:
      test_command: "{auto_detected}"
      lint_command: "{auto_detected}"
  ```
- Verification lint/format integree
- SI echec tests: Activer recovery du skill (max 2 retries)

> Voir documentation du skill `tdd-workflow` pour error recovery.

> Voir @references/quick/epct-workflow.md pour le detail complet de chaque phase.

---

## Resume Final (MANDATORY)

**⚠️ OBLIGATOIRE:** Toujours afficher le message de completion et executer le hook memoire.

> Voir @references/quick/resume-completion.md pour les formats de sortie et hooks.

---

## Gestion des Erreurs

### Strategie de Reessai

| Situation | Action |
|-----------|--------|
| Erreur detectee | Activer mode `think` |
| 1er reessai echoue | Escalader modele (Haiku→Sonnet) |
| 2eme reessai echoue | Arreter, demander intervention |
| Tests echouent | Activer `think hard`, tenter auto-correction |
| Tests echouent encore | Rapporter echec, arreter |

### Escalade vers /epci

Escalader SI pendant l'implementation vous decouvrez:
- Plus de 3 fichiers impactes
- Risque de regression identifie
- Complexite sous-estimee
- Tests d'integration necessaires
- Changements sensibles securite

```
⚠️ **ESCALADE RECOMMANDEE**

La modification est plus complexe qu'anticipee:
- [Raison 1]
- [Raison 2]

Recommandation: Basculer vers `/epci` pour workflow structure.
```

---

## Comparaison avec /epci

| Aspect | /quick | /epci |
|--------|--------|-------|
| Workflow | EPCT (4 phases) | 3 phases |
| Feature Document | Non | Oui |
| Breakpoints | 1 leger (3s) | 3 complets |
| Switching modele | Adaptatif Haiku/Sonnet | Base sur flags |
| @plan-validator | Non | Oui |
| @code-reviewer | Non | Complet |
| @security-auditor | Non | Conditionnel |
| Persistence session | Oui (.project-memory/sessions/) | Via hooks |
| Duree cible | <30s TINY, <90s SMALL | Variable |

---

## Exemples

### Exemple TINY

**Brief:** "Corriger typo 'recieve' vers 'receive' dans UserService"

```
[E] Explore: UserService.php identifie, TINY confirme
[P] Plan: 1 tache — Remplacer typo ligne 42
    (--autonomous: BP ignore)
[C] Code: Edit applique, syntaxe OK
[T] Test: Tests existants passent

✅ QUICK COMPLETE — TINY
Fichier: src/Service/UserService.php
Temps: 12s
```

### Exemple SMALL

**Brief:** "Ajouter methode isActive() a l'entite User"

```
[E] Explore: 2 fichiers identifies, SMALL confirme
    @Explore (Haiku): patterns detectes
[P] Plan: 3 taches generees
    @skill:breakpoint-display type:lightweight
    Tasks: [1] Ecrire test, [2] Implementer, [3] Verifier
    (Auto-continue dans 3s si --confirm)
[C] Code: @implementer (Sonnet) execute
[T] Test: 3/3 tests reussis

✅ QUICK COMPLETE — SMALL
Fichiers: User.php (+15/-0), UserTest.php (+22/-0)
Temps: 67s
```

### Exemple Plan Natif (Fast Path)

**Commande:** `/quick "fix auth" @docs/plans/fix-auth-20260120.md`

```
[PRE] Detection plan natif
      ⚡ Plan natif detecte → Mode accelere [C][T]
         Source: docs/plans/fix-auth-20260120.md
         Taches extraites: 3
      → Skip [E][P]

[C] Code: Execution taches du plan (Sonnet)
    [1] Corriger validation token → Done
    [2] Ajouter test unitaire → Done
    [3] Mettre a jour config → Done
[T] Test: 5/5 tests reussis, lint OK

✅ QUICK COMPLETE — SMALL (Plan Natif)
Fichiers: AuthService.php (+8/-3), AuthTest.php (+15/-0)
Temps: 42s (accelere)
```

---

## References

| Materiel | Emplacement |
|----------|-------------|
| Workflow EPCT detaille | @references/quick/epct-workflow.md |
| Resume et completion | @references/quick/resume-completion.md |
| Flags et matrices | @references/quick/flags-matrix.md |
