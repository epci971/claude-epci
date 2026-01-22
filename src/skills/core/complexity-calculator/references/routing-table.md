# Table de Decision Workflow

Table de routage pour diriger les taches vers le workflow approprie.

## Decision Tree Principal

```
                    ┌─────────────────────────────┐
                    │   Nouvelle Tache Recue      │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │  complexity.calculate(task) │
                    └─────────────┬───────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
        ┌──────────┐       ┌──────────────┐    ┌──────────┐
        │  < 25    │       │   25-74      │    │   75+    │
        │  TINY    │       │ SMALL/STD    │    │  LARGE   │
        └────┬─────┘       └──────┬───────┘    └────┬─────┘
             │                    │                  │
             ▼                    ▼                  ▼
        ┌──────────┐       ┌──────────────┐    ┌──────────┐
        │  /quick  │       │   /quick ou  │    │/implement│
        │          │       │  /implement  │    │  --large │
        └──────────┘       └──────────────┘    └──────────┘
```

---

## Table de Routage Detaillee

| Score | Categorie | Workflow | Conditions | Caracteristiques |
|-------|-----------|----------|------------|------------------|
| 0-24 | TINY | `/quick` | Toujours | Single file, minimal change |
| 25-49 | SMALL | `/quick` | Default | Few files, bounded scope |
| 25-49 | SMALL | `/implement` | Si multi-phase explicite | User prefers structure |
| 50-74 | STANDARD | `/implement` | Default | Multi-file, clear phases |
| 50-74 | STANDARD | `/quick` | Si explicitement simple | User prefers speed |
| 75-100 | LARGE | `/implement --large` | Toujours | Needs decomposition |

---

## Regles de Routage

### Rule 1: Force TINY → /quick

```
IF score < 25:
  RETURN "/quick"
  # Pas de discussion, execution directe
```

### Rule 2: SMALL Decision

```
IF 25 <= score < 50:
  IF user_prefers_structure OR multi_phase_required:
    RETURN "/implement"
  ELSE:
    RETURN "/quick"
```

### Rule 3: STANDARD Decision

```
IF 50 <= score < 75:
  IF user_prefers_speed AND single_phase_possible:
    RETURN "/quick"  # Rare, requires explicit request
  ELSE:
    RETURN "/implement"
```

### Rule 4: Force LARGE → /implement --large

```
IF score >= 75:
  RETURN "/implement --large"
  # Requires decomposition en sous-taches
```

---

## Indicateurs par Workflow

### /quick - Fast Path

**Indicateurs positifs**:
- Bug fix simple
- Ajout mineur (typo, config)
- Refactoring localise
- 1-3 fichiers maximum
- Pas de nouveaux tests requis
- Risque faible

**Indicateurs negatifs**:
- Nouvelle feature complete
- Impact multi-modules
- Changement d'architecture
- Tests complexes requis

### /implement - Standard Path

**Indicateurs positifs**:
- Feature complete avec scope defini
- 4-10 fichiers
- Tests unitaires et integration
- Documentation requise
- Changements coordonnes

**Indicateurs negatifs**:
- Scope mal defini
- Trop simple (TINY/SMALL)
- Trop complexe (needs decomposition)

### /implement --large - Decomposition Path

**Indicateurs positifs**:
- 10+ fichiers
- Changement architectural
- Multiple stories/PRs
- Risque eleve
- Dependencies complexes

**Requis**:
- Decomposition en sous-taches
- Planning multi-phase
- Checkpoints intermediaires
- Review obligatoire

---

## Overrides Utilisateur

L'utilisateur peut forcer un workflow different.

| Demande | Action |
|---------|--------|
| "quick fix" + STANDARD task | Proposer /quick si faisable |
| "implement properly" + SMALL task | Utiliser /implement |
| "split this up" + LARGE task | Decomposer avant /implement |

### Syntax

```
# Force /quick sur tache SMALL
/quick "add email validation"

# Force /implement sur tache SMALL
/implement "add email validation"

# Force decomposition
/implement --large "refactor auth system"
```

---

## Integration avec Skills

### Brainstorm → Routing

```
# Apres exploration d'idee
result = complexity.calculate(brainstorm_output)
IF result.category in ["TINY", "SMALL"]:
  suggest "/quick"
ELSE:
  suggest "/spec → /implement"
```

### Spec → Routing

```
# Apres creation specification
result = complexity.calculate(prd)
IF result.category == "LARGE":
  suggest "decompose into smaller tasks"
ELSE:
  proceed_to "/implement"
```

### Debug → Routing

```
# Apres diagnostic
IF fix_is_simple:
  route_to "/quick"
ELSE:
  route_to "/implement"
```

---

## Tableau Recapitulatif

| Source | TINY | SMALL | STANDARD | LARGE |
|--------|------|-------|----------|-------|
| /brainstorm | /quick | /quick | /spec | /spec + decompose |
| /spec | /quick | /quick or /implement | /implement | /implement --large |
| /debug | /quick | /quick | /implement | /implement --large |
| Direct | /quick | /quick | /implement | /implement --large |

---

## Validation de Scope

Avant execution, valider que le scope correspond:

```python
def validate_scope(category, files_list):
    """
    Verifie coherence entre categorie et fichiers.

    Returns:
        True si coherent
        False si mismatch (demander re-evaluation)
    """
    limits = {
        "TINY": 1,
        "SMALL": 3,
        "STANDARD": 10,
        "LARGE": float('inf')
    }

    return len(files_list) <= limits[category]
```

### Mismatch Handling

| Situation | Action |
|-----------|--------|
| TINY avec 5 fichiers | Re-evaluer → probablement STANDARD |
| LARGE avec 2 fichiers | Re-evaluer → probablement SMALL |
| STANDARD mais risque HIGH | Upgrade → LARGE |

---

## Risk Elevation Table

Le risque peut elever automatiquement la categorie de base.

| Base Category | + Risk > 30 | + Risk > 50 |
|---------------|-------------|-------------|
| TINY | → SMALL | → STANDARD |
| SMALL | → STANDARD | → STANDARD |
| STANDARD | → STANDARD | → LARGE |
| LARGE | → LARGE | → LARGE |

**Logique:**
```
final_category = base_category
IF risk_score > 50:
  final_category = elevate(base_category, 2)
ELIF risk_score > 30:
  final_category = elevate(base_category, 1)
```

**Exemples:**
- TINY + auth file (risk=30) → SMALL
- SMALL + migration + no tests (risk=40) → STANDARD
- STANDARD + security + breaking API (risk=55) → LARGE

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│           COMPLEXITY → WORKFLOW MAPPING             │
├─────────────────────────────────────────────────────┤
│                                                     │
│  TINY (< 25)     →  /quick                         │
│  SMALL (25-49)   →  /quick (default)               │
│  STANDARD (50-74)→  /implement                     │
│  LARGE (75+)     →  /implement --large             │
│                                                     │
├─────────────────────────────────────────────────────┤
│  OVERRIDE RULES:                                    │
│  - User can force /quick on SMALL                  │
│  - User can force /implement on SMALL              │
│  - LARGE always requires decomposition             │
│  - TINY never needs /implement                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```
