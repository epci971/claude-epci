# Feature Document — Auto-Détection Plans Natifs

> **Slug:** auto-detection-plans-natifs
> **Created:** 2026-01-20T19:18:23Z
> **Category:** STANDARD
> **Source:** docs/plans/auto-detection-plans-natifs-20260120-191419.md (plan natif)

---

## §1 — Brief Fonctionnel

### Objectif

Supprimer le flag `--from-native-plan` et implémenter une détection automatique des plans natifs dans les 3 commandes EPCI :
- `/brief` — détecte et utilise comme contexte, route intelligemment
- `/epci` — détecte et intègre en §2 automatiquement
- `/quick` — détecte et utilise comme contexte pour phase [P]

### Principe

Si le fichier passé via argument `@<path>` est dans `docs/plans/` ou contient un frontmatter YAML avec `saved_at`, c'est un plan natif → traitement automatique sans flag explicite.

### Contexte

Actuellement, `/epci` nécessite le flag `--from-native-plan` pour intégrer un plan sauvegardé via `/save-plan`. Cette approche est verbeuse et nécessite de mémoriser le flag. La détection automatique simplifie le workflow.

### Contraintes

- Rétrocompatibilité totale (workflow sans `@path` inchangé)
- Logique de détection commune aux 3 commandes
- Mise à jour de la documentation CLAUDE.md
- Synchronisation src/ et build/

### Critères de Succès

1. `/brief @docs/plans/*.md` détecte plan natif et route avec contexte
2. `/epci slug @docs/plans/*.md` intègre automatiquement en §2
3. `/quick @docs/plans/*.md` utilise comme contexte phase [P]
4. Workflow standard sans `@path` fonctionne identiquement
5. Tests de vérification passent (4 scénarios)

### Fichiers Impactés

| Fichier | Action | Priorité |
|---------|--------|----------|
| `src/commands/epci.md` | Modify | CRITIQUE |
| `src/commands/brief.md` | Modify | ÉLEVÉ |
| `src/commands/quick.md` | Modify | MOYEN |
| `src/commands/references/epci/native-plan-import.md` | Rename + Modify | MOYEN |
| `CLAUDE.md` | Modify | MOYEN |
| `src/commands/save-plan.md` | Modify | BAS |
| `src/commands/references/epci/feature-document-templates.md` | Modify | BAS |
| `src/commands/references/epci/phase-1-planning.md` | Verify | BAS |
| `build/epci/commands/epci.md` | Sync | CRITIQUE |
| `build/epci/commands/brief.md` | Sync | ÉLEVÉ |
| `src/.claude-plugin/plugin.json` | Version bump | BAS |
| `build/epci/.claude-plugin/plugin.json` | Version bump | BAS |

### Stack Technique

- **Fichiers:** Markdown (commandes EPCI)
- **Détection:** YAML frontmatter parsing
- **Pattern:** Argument de contexte `@<path>`

---

## §2 — Plan Original (Natif)

> Source: `~/.claude/plans/resilient-kindling-hanrahan.md`
> Sauvegardé: `docs/plans/auto-detection-plans-natifs-20260120-191419.md`

### Logique de Détection (commune aux 3 commandes)

```python
def is_native_plan(file_path):
    """Détection automatique d'un plan natif sauvegardé."""
    # Critère 1: Chemin dans docs/plans/
    if "docs/plans/" in file_path:
        return True

    # Critère 2 (fallback): Frontmatter avec saved_at
    content = read_file(file_path)
    frontmatter = parse_yaml_frontmatter(content)
    if frontmatter and "saved_at" in frontmatter:
        return True

    return False

def extract_native_plan_metadata(file_path):
    """Extrait slug et contenu du plan natif."""
    content = read_file(file_path)
    frontmatter = parse_yaml_frontmatter(content)

    return {
        "slug": frontmatter.get("slug") or extract_slug_from_filename(file_path),
        "source": frontmatter.get("source", "unknown"),
        "content": content_after_frontmatter(content),
        "path": file_path
    }
```

### Implémentation par Commande

#### 1. `/brief` — Détection + Routing intelligent

**Step 0.5 — Détection Type Input (mise à jour)**

| Pattern | INPUT_TYPE | Traitement |
|---------|------------|------------|
| `docs/plans/*.md` | `native_plan` | Auto-détecté, extraire slug + contenu |
| `docs/briefs/*/*.md` | `brainstorm_output` | Workflow existant |
| Autre `.md` | `external_file` | Brief brut |
| Texte libre | `text` | Brief inline |

**Step 6 — Routing (sans flag explicite)**

| Catégorie | Commande | Slug |
|-----------|----------|------|
| TINY | `/quick "{brief}" @{native_plan_path}` | Auto |
| SMALL | `/quick "{brief}" @{native_plan_path}` | Auto |
| STANDARD | `/epci {detected_slug} @{native_plan_path}` | Depuis metadata |
| LARGE | `/epci --large {detected_slug} @{native_plan_path}` | Depuis metadata |

#### 2. `/epci` — Suppression flag + Détection locale

**argument-hint (ligne 6)**
```yaml
# AVANT
argument-hint: "[--large] [--turbo] [--from-native-plan <file>] ..."

# APRÈS
argument-hint: "[--large] [--turbo] [--think|--think-hard|--ultrathink] ..."
```

**Step 0.5 — Détection automatique**

Condition: Argument de contexte `@<file>` fourni

1. Vérifier si `<file>` est dans `docs/plans/` OU a frontmatter `saved_at`
2. SI plan natif détecté:
   - Extraire slug depuis frontmatter ou filename
   - Extraire contenu du plan
   - Créer/mettre à jour Feature Document avec §2
   - Vérifier §1 → lancer @Explore si manquant
3. SINON: Traitement standard

#### 3. `/quick` — Ajouter détection locale

**Phase [E] EXPLORE**

SI argument de contexte `@<file>` fourni:
1. Vérifier si fichier est dans `docs/plans/` (auto-détection)
2. SI plan natif: Extraire contenu comme contexte, stocker `native_plan_context`
3. SINON: Traiter comme contexte additionnel standard

**Phase [P] PLAN**

SI `native_plan_context` existe:
- Utiliser le plan natif comme base pour générer les tâches
- Affiner/adapter au contexte découvert en phase [E]

### Vérification

1. Test détection `/brief`: `/brief @docs/plans/integration-perplexity-research-20260120-160914.md`
2. Test détection `/epci`: `/epci auth-feature @docs/plans/auth-20260120.md`
3. Test détection `/quick`: `/quick "small fix" @docs/plans/fix-20260120.md`
4. Test rétrocompatibilité: `/epci feature-slug` (sans @path)

### Version Bump

`5.4.1` → `5.5.0` (changement de comportement majeur)

---

## §2.1 — Plan d'Implémentation Raffiné (v2)

> Révision suite à validation @plan-validator

### Vue d'ensemble

14 fichiers à modifier en 3 phases d'implémentation + 1 phase tests, ordonnées par dépendances.

---

### Algorithme de Détection (Spécification)

**Logique commune aux 3 commandes:**

```python
def is_native_plan(file_path: str) -> bool:
    """Détection automatique d'un plan natif sauvegardé."""
    # Critère 1: Chemin contient docs/plans/
    if "docs/plans/" in file_path:
        return True

    # Critère 2 (fallback): Frontmatter avec saved_at
    content = read_file(file_path)
    if has_yaml_frontmatter(content):
        frontmatter = parse_frontmatter(content)
        if "saved_at" in frontmatter:
            return True

    return False

def extract_native_plan_metadata(file_path: str) -> dict:
    """Extrait métadonnées du plan natif."""
    content = read_file(file_path)
    frontmatter = parse_frontmatter(content)

    return {
        "slug": frontmatter.get("slug") or slug_from_filename(file_path),
        "source": frontmatter.get("source", "unknown"),
        "content": content_after_frontmatter(content),
        "path": file_path
    }
```

**Mécanisme de passage de contexte:**

Le contexte est passé via **argument de commande** avec syntaxe `@<path>`:

```bash
# /brief détecte et route vers:
/epci {slug} @docs/plans/my-plan.md

# /epci reçoit l'argument et:
1. Détecte @docs/plans/... comme argument de contexte
2. Appelle is_native_plan("docs/plans/my-plan.md")
3. Si true: extrait metadata, intègre en §2

# /quick reçoit l'argument et:
1. Détecte @docs/plans/... comme argument de contexte
2. Si native plan: stocke dans native_plan_context
3. Phase [P] utilise native_plan_context comme base
```

**Note:** Pas de variable d'environnement ni fichier temporaire — passage explicite via argument.

### Phase A: Core Commands (CRITIQUE)

#### Task A1: Modifier `/epci` argument-hint (3 min)

**Fichier:** `src/commands/epci.md`
**Ligne:** 6

**Action:** Supprimer `[--from-native-plan <file>]` de argument-hint

```yaml
# AVANT
argument-hint: "[--large] [--turbo] [--from-native-plan <file>] [--think..."

# APRÈS
argument-hint: "[--large] [--turbo] [--think|--think-hard|--ultrathink] [--safe]..."
```

**Done when:** Flag absent de la ligne 6

---

#### Task A2: Modifier `/epci` tableau Arguments (2 min)

**Fichier:** `src/commands/epci.md`
**Ligne:** ~72

**Action:** Supprimer ligne du tableau

```markdown
| `--from-native-plan <file>` | Import native Claude Code plan... |
```

**Done when:** Ligne absente du tableau Arguments

---

#### Task A3: Modifier `/epci` Step 0.5 — Nouvelle logique (10 min)

**Fichier:** `src/commands/epci.md`
**Lignes:** 166-178

**Action:** Remplacer Step 0.5 entier par:

```markdown
## Step 0.5: Auto-Detect Native Plan (CONDITIONAL)

**Condition:** Argument de contexte `@<file>` fourni

**Process:**
1. Extraire chemin depuis argument `@<path>`
2. Appeler `is_native_plan(path)` (voir Algorithme de Détection)
3. SI native plan détecté:
   - Appeler `extract_native_plan_metadata(path)`
   - Créer/mettre à jour Feature Document avec §2 "Plan Original (Natif)"
   - Vérifier §1 → lancer @Explore si manquant
4. SINON: Ignorer, traitement standard

**Note:** Pas de flag nécessaire — détection basée sur chemin/frontmatter.
```

**Done when:** Step 0.5 utilise logique auto-detect sans mention du flag

---

#### Task A4: Modifier `/brief` Step 0.5 — Détection native_plan (5 min)

**Fichier:** `src/commands/brief.md`
**Lignes:** ~95-118

**Action:** Ajouter `native_plan` dans tableau INPUT_TYPE

```markdown
| Pattern | INPUT_TYPE | Traitement |
|---------|------------|------------|
| `docs/plans/*.md` ou frontmatter `saved_at` | `native_plan` | Auto-détecté, extraire slug + contenu |
| `docs/briefs/*/*.md` | `brainstorm_output` | Workflow existant |
| Autre `.md` | `external_file` | Brief brut |
| Texte libre | `text` | Brief inline |
```

**Done when:** Tableau inclut ligne `native_plan`

---

#### Task A5: Modifier `/brief` Step 6 — Routing avec contexte (5 min)

**Fichier:** `src/commands/brief.md`
**Lignes:** ~434-458

**Action:** Ajouter section routing pour native_plan

```markdown
**SI INPUT_TYPE == "native_plan":**

| Catégorie | Commande |
|-----------|----------|
| TINY | `/quick "{brief}" @{native_plan_path}` |
| SMALL | `/quick "{brief}" @{native_plan_path}` |
| STANDARD | `/epci {detected_slug} @{native_plan_path}` |
| LARGE | `/epci --large {detected_slug} @{native_plan_path}` |

**Note:** Le `@{path}` est passé comme argument de contexte.
Chaque commande cible fait sa propre détection locale.
```

**Done when:** Table de routing inclut colonne pour native_plan avec syntaxe `@path`

---

#### Task A6: Modifier `/quick` Phase [E] — Détection (5 min)

**Fichier:** `src/commands/quick.md`
**Lignes:** ~109-133

**Action:** Ajouter bloc de détection avant complexity-calculator

```markdown
### [E] EXPLORE Phase (5-10s)

**Step 0: Détection Native Plan (SI argument `@<file>`)**

```
IF argument starts with "@":
   path = extract_path(argument)
   IF is_native_plan(path):
      native_plan_context = extract_native_plan_metadata(path)
      # Sera utilisé en Phase [P]
   ELSE:
      # Ignorer, traiter comme contexte additionnel
```

**Step 1: Collecte contexte via @Explore...**
```

**Done when:** Phase [E] inclut Step 0 détection native plan

---

#### Task A7: Modifier `/quick` Phase [P] — Utilisation contexte (5 min)

**Fichier:** `src/commands/quick.md`
**Lignes:** ~134-165

**Action:** Ajouter condition native_plan_context

```markdown
### [P] PLAN Phase (10-15s)

**SI `native_plan_context` existe:**
- Utiliser le plan natif comme **base** pour générer les tâches
- Affiner/adapter au contexte découvert en phase [E]
- Ne pas repartir de zéro

**SINON:**
- Génération standard des tâches (comportement existant)
```

**Done when:** Phase [P] conditionne sur native_plan_context

---

### Phase B: Documentation & Références (MOYEN)

#### Task B1: Renommer native-plan-import.md (2 min)

**Action:** Renommer fichier via git mv

```bash
git mv src/commands/references/epci/native-plan-import.md \
       src/commands/references/epci/native-plan-detection.md
```

**Done when:** Fichier renommé, git tracked

---

#### Task B2: Refactoriser native-plan-detection.md (8 min)

**Fichier:** `src/commands/references/epci/native-plan-detection.md`

**Modifications:**
1. **Ligne 9:** Remplacer trigger
   - AVANT: `**Triggered by:** \`--from-native-plan <file>\` flag`
   - APRÈS: `**Triggered by:** Auto-detection when argument \`@<path>\` contains \`docs/plans/\` or has \`saved_at\` frontmatter`

2. **Lignes 203-220:** Mettre à jour exemples workflows
   - AVANT: `/epci --from-native-plan ~/.claude/plans/plan.md --slug feature-name`
   - APRÈS: `/epci feature-name @docs/plans/plan.md`

3. Supprimer toutes références à `--from-native-plan`

**Done when:** Aucune mention du flag dans le fichier

---

#### Task B3: Mettre à jour save-plan.md exemples (5 min)

**Fichier:** `src/commands/save-plan.md`

**Modifications:**
- **Ligne ~279:** Remplacer `/epci --from-native-plan {destination_path} --slug {slug}` par `/epci {slug} @{destination_path}`
- **Ligne ~331:** Mettre à jour exemple complet

**Done when:** Exemples utilisent syntaxe `@path`

---

#### Task B4: Clarifier feature-document-templates.md (3 min)

**Fichier:** `src/commands/references/epci/feature-document-templates.md`

**Modification:**
- Remplacer "Use when `--from-native-plan` flag was used" par "Use when native plan detected (path contains `docs/plans/` or has `saved_at` frontmatter)"

**Done when:** Description mise à jour

---

### Phase C: Synchronisation Build (CRITIQUE)

#### Task C1: Sync build/epci/commands/epci.md (5 min)

Appliquer Tasks A1 + A2 + A3 au fichier build.

**Done when:** build/epci/commands/epci.md identique à src/

---

#### Task C2: Sync build/epci/commands/brief.md (5 min)

Appliquer Tasks A4 + A5 au fichier build.

**Done when:** build/epci/commands/brief.md identique à src/

---

#### Task C3: Sync build/epci/commands/quick.md (5 min)

Appliquer Tasks A6 + A7 au fichier build.

**Done when:** build/epci/commands/quick.md identique à src/

---

#### Task C4: Renommer + Sync build native-plan-detection.md (3 min)

```bash
git mv build/epci/commands/references/epci/native-plan-import.md \
       build/epci/commands/references/epci/native-plan-detection.md
```

Puis appliquer Task B2.

**Done when:** Fichier renommé et mis à jour

---

#### Task C5: Sync build/epci/commands/save-plan.md (3 min)

Appliquer Task B3 au fichier build.

**Done when:** Exemples synchronisés

---

### Phase D: Version & Documentation Globale (FINAL)

#### Task D1: Ajouter section Nouveautés v5.5.0 dans CLAUDE.md (5 min)

**Fichier:** `CLAUDE.md`

**Action:** Après section "Nouveautés v5.4.1", ajouter:

```markdown
### Nouveautés v5.5.0 (Native Plan Auto-Detection)

- **Détection automatique plans natifs** : Suppression du flag `--from-native-plan`
- **Passage par argument `@<path>`** : Détection automatique si chemin dans `docs/plans/` ou frontmatter `saved_at`
- **Support unifié 3 commandes** : `/brief`, `/epci`, `/quick` détectent automatiquement
- **Workflow simplifié** : Plus besoin de mémoriser le flag, passage transparent
```

**Done when:** Section ajoutée après v5.4.1

---

#### Task D2: Mettre à jour section Workflow Plan Natif dans CLAUDE.md (10 min)

**Fichier:** `CLAUDE.md`
**Section:** "Workflow avec Plan Natif" (lignes ~240-298)

**Action:** Remplacer par workflow sans flag (voir §2 Plan Original)

**Done when:** Section mise à jour avec syntaxe `@path`

---

#### Task D3: Version bump CLAUDE.md header (2 min)

**Fichier:** `CLAUDE.md`
**Ligne:** ~7

**Action:** `> **Version** : 5.4.1` → `> **Version** : 5.5.0`

**Done when:** Version mise à jour

---

#### Task D4: Version bump plugin.json x2 (2 min)

**Fichiers:**
- `src/.claude-plugin/plugin.json`: `"version": "5.5.0"`
- `build/epci/.claude-plugin/plugin.json`: `"version": "5.5.0"`

**Done when:** Les deux fichiers ont version 5.5.0

---

### Phase T: Tests de Validation

#### Task T1: Test détection /brief avec plan (3 min)

```bash
/brief @docs/plans/auto-detection-plans-natifs-20260120-191419.md
```

**Attendu:** Détecte native plan, extrait slug, route vers /epci avec `@path`

---

#### Task T2: Test détection /epci avec plan (3 min)

```bash
/epci test-feature @docs/plans/auto-detection-plans-natifs-20260120-191419.md
```

**Attendu:** Détecte native plan, intègre en §2

---

#### Task T3: Test rétrocompatibilité /epci standard (2 min)

```bash
/epci test-feature
```

**Attendu:** Workflow standard sans erreur, pas de détection

---

#### Task T4: Test rétrocompatibilité /brief texte (2 min)

```bash
/brief "Test feature description"
```

**Attendu:** Workflow standard, INPUT_TYPE = text

---

### Ordre d'exécution

```
Phase A (Core) — Dépendances: aucune
├── A1: epci.md argument-hint (3 min)
├── A2: epci.md tableau (2 min)
├── A3: epci.md Step 0.5 (10 min)
├── A4: brief.md Step 0.5 (5 min)
├── A5: brief.md Step 6 (5 min)
├── A6: quick.md Phase [E] (5 min)
└── A7: quick.md Phase [P] (5 min)
    SUBTOTAL: 35 min

Phase B (Références) — Après Phase A
├── B1: Renommer native-plan-import.md (2 min)
├── B2: Refactoriser contenu (8 min)
├── B3: save-plan.md exemples (5 min)
└── B4: feature-document-templates.md (3 min)
    SUBTOTAL: 18 min

Phase C (Sync Build) — Après Phases A+B
├── C1: build/epci.md (5 min)
├── C2: build/brief.md (5 min)
├── C3: build/quick.md (5 min)
├── C4: build/native-plan-detection.md (3 min)
└── C5: build/save-plan.md (3 min)
    SUBTOTAL: 21 min

Phase D (Version) — DERNIER
├── D1: CLAUDE.md Nouveautés (5 min)
├── D2: CLAUDE.md Workflow (10 min)
├── D3: CLAUDE.md version (2 min)
└── D4: plugin.json x2 (2 min)
    SUBTOTAL: 19 min

Phase T (Tests) — Après tout
├── T1: Test /brief avec plan (3 min)
├── T2: Test /epci avec plan (3 min)
├── T3: Test rétrocompat /epci (2 min)
└── T4: Test rétrocompat /brief (2 min)
    SUBTOTAL: 10 min

TOTAL: ~103 min estimé
```

---

### Critères de validation

| Test | Commande | Résultat attendu |
|------|----------|------------------|
| T1 | `/brief @docs/plans/test.md` | Détecte native plan, route avec `@path` |
| T2 | `/epci slug @docs/plans/test.md` | Détecte native plan, intègre en §2 |
| T3 | `/epci feature-slug` | Workflow standard sans erreur |
| T4 | `/brief "texte"` | Workflow standard, INPUT_TYPE = text |

---

## §3 — Implementation

### Implementation Summary (Phase 2)

**Status:** ✅ COMPLETED

#### Phase A: Core Commands (CRITIQUE) — 7/7 Tasks

| Task | File | Change | Status |
|------|------|--------|--------|
| A1 | `src/commands/epci.md` | Removed `--from-native-plan` from argument-hint | ✅ |
| A2 | `src/commands/epci.md` | Removed flag from Arguments table | ✅ |
| A3 | `src/commands/epci.md` | Replaced Step 0.5 with auto-detection logic | ✅ |
| A4 | `src/commands/brief.md` | Added native_plan detection to Step 0.5 | ✅ |
| A5 | `src/commands/brief.md` | Added routing with `@{native_plan_path}` context | ✅ |
| A6 | `src/commands/quick.md` | Added native plan detection in Phase [E] | ✅ |
| A7 | `src/commands/quick.md` | Added `native_plan_context` usage in Phase [P] | ✅ |

#### Phase B: Documentation (MOYEN) — 4/4 Tasks

| Task | File | Change | Status |
|------|------|--------|--------|
| B1 | `native-plan-import.md` | Renamed to `native-plan-detection.md` | ✅ |
| B2 | `native-plan-detection.md` | Refactored content (removed flag refs, updated workflows) | ✅ |
| B3 | `save-plan.md` | Updated "Next steps" examples | ✅ |
| B4 | `feature-document-templates.md` | Updated scenario references | ✅ |

#### Phase C: Build Sync — 5/5 Tasks

| Task | File | Status |
|------|------|--------|
| C1 | `build/epci/commands/epci.md` | ✅ Synced |
| C2 | `build/epci/commands/brief.md` | ✅ Synced |
| C3 | `build/epci/commands/quick.md` | ✅ Synced |
| C4 | `build/...native-plan-detection.md` | ✅ Renamed + Synced |
| C5 | `build/epci/commands/save-plan.md` | ✅ Synced |

#### Phase D: Version Bump — 4/4 Tasks

| Task | File | Change | Status |
|------|------|--------|--------|
| D1 | `CLAUDE.md` | Added Nouveautés v5.5.0 section | ✅ |
| D2 | `CLAUDE.md` | Updated Workflow Plan Natif section | ✅ |
| D3 | `CLAUDE.md` | Version bump 5.4.1 → 5.5.0 | ✅ |
| D4 | `plugin.json` (x2) | Version bump 5.4.1 → 5.5.0 | ✅ |

#### Phase T: Tests de Validation — 4/4 Tests

| Test | Command | Expected | Actual | Status |
|------|---------|----------|--------|--------|
| T1 | `grep --from-native-plan src/commands/` | No matches | No matches | ✅ |
| T2 | `grep is_native_plan src/commands/` | 4 files | 4 files (epci, brief, quick, detection.md) | ✅ |
| T3 | `validate_all.py` | All commands pass | All 14 commands ✅ | ✅ |
| T4 | Routing format check | `@{native_plan_path}` present | Found in brief.md:474-477 | ✅ |

### Code Review (Phase 2)

**@code-reviewer verdict:** PENDING (BP2)

### Files Modified

| File | Lines Changed |
|------|---------------|
| `src/commands/epci.md` | ~40 |
| `src/commands/brief.md` | ~50 |
| `src/commands/quick.md` | ~30 |
| `src/commands/references/epci/native-plan-detection.md` | ~80 (renamed + refactored) |
| `src/commands/save-plan.md` | ~20 |
| `src/commands/references/epci/feature-document-templates.md` | ~10 |
| `CLAUDE.md` | ~80 |
| `src/.claude-plugin/plugin.json` | 1 |
| `build/epci/.claude-plugin/plugin.json` | 1 |
| `build/epci/commands/*` | Synced from src |

**Total:** ~300+ lines modified across 15+ files

### Commit Context

```json
{
  "type": "feat",
  "scope": "commands",
  "description": "implement auto-detection for native plans",
  "breaking_change": true,
  "breaking_description": "--from-native-plan flag removed, use @path argument instead",
  "files_modified": 15,
  "version_bump": "5.4.1 → 5.5.0"
}
```
