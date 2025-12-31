# Multi-Task Detection — Algorithm Reference

> Complete specification for aggressive multi-task detection

---

## Overview

Code-Promptor v2.1 uses **aggressive** multi-task detection. The skill tends toward detecting multiple tasks when ambiguous, allowing users to merge if needed.

---

## Detection Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    DICTATION RECEIVED                            │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: CLEANING                                               │
│  - Remove hesitations (euh, hum, bon, bah...)                   │
│  - Normalize repetitions                                         │
│  - KEEP rupture markers intact                                  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 2: SEGMENTATION                                           │
│  - Split on RUPTURE MARKERS                                     │
│  - Identify distinct segments                                    │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 3: SEGMENT ANALYSIS                                       │
│  For each segment:                                               │
│  - Identify PRIMARY SUBJECT                                      │
│  - Identify ACTION VERB                                          │
│  - Identify TECHNICAL DOMAIN                                     │
│  - Calculate INDEPENDENCE SCORE                                  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 4: DECISION                                               │
│  ≥2 segments with score ≥40 → MULTI-TASK                        │
│  Otherwise → MONO-TASK                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Cleaning

### Artifacts to Remove

| Type | Examples | Action |
|------|----------|--------|
| Hesitations | "euh", "hum", "uh", "um" | Delete |
| Fillers | "tu vois", "genre", "quoi", "voilà", "en fait" | Delete |
| Self-corrections | "non en fait", "je veux dire" | Keep corrected version |
| Repetitions | "il faut, il faut que..." | Keep once |
| Tangents | Unrelated personal comments | Delete |

### Markers to PRESERVE

**Critical**: Keep all rupture markers during cleaning.

```
KEEP: "aussi", "et puis", "autre chose", "ah et", "sinon", 
      "autrement", "à part ça", "au fait", "tiens"
```

---

## Phase 2: Segmentation

### Explicit Rupture Markers (+30 points)

| Category | French | English |
|----------|--------|---------|
| **Addition** | "aussi", "également", "en plus", "et puis" | "also", "plus", "and then" |
| **Rupture** | "sinon", "autre chose", "autrement", "à part ça" | "otherwise", "besides", "apart from that" |
| **Transition** | "ah et", "oh et", "tiens", "au fait" | "oh and", "by the way" |
| **Enumeration** | "premièrement... deuxièmement", "d'abord... ensuite" | "first... then", "firstly... secondly" |
| **Contrast** | "par contre", "mais aussi", "d'un autre côté" | "on the other hand", "but also" |

### Implicit Rupture Markers (+15-25 points)

| Pattern | Points | Example |
|---------|--------|---------|
| Subject change | +15 | "le login... les rapports..." |
| Long pause (in voice) | +15 | "... [pause] ..." |
| Action verb repetition | +15 | "il faut créer... il faut aussi créer..." |
| Tense change | +15 | "on a fait... il faudra faire..." |
| Domain change | +25 | Backend → Frontend |

---

## Phase 3: Segment Analysis

### Independence Score Formula

```
SCORE_SEGMENT = 
    SUBJECT_DIFFERENT × 25 +
    ACTION_DIFFERENT × 20 +
    DOMAIN_DIFFERENT × 25 +
    EXPLICIT_MARKER × 30 +
    IMPLICIT_MARKER × 15
```

### Subject Analysis

Compare main subjects between segments:
- **Same subject** → 0 points
- **Related subject** (same module) → +10 points
- **Different subject** → +25 points

Examples:
| Segment 1 | Segment 2 | Score |
|-----------|-----------|-------|
| "le login" | "l'authentification" | 0 (same) |
| "le login" | "le dashboard" | +25 (different) |
| "les users" | "les permissions" | +10 (related) |

### Action Analysis

Compare action verbs:
- **Same action** → 0 points
- **Similar action** (synonyms) → +5 points
- **Different action** → +20 points

Examples:
| Segment 1 | Segment 2 | Score |
|-----------|-----------|-------|
| "créer" | "ajouter" | +5 (similar) |
| "créer" | "corriger" | +20 (different) |
| "fixer" | "réparer" | 0 (same) |

### Domain Detection

| Domain | Keywords |
|--------|----------|
| **Backend** | API, service, endpoint, BDD, base de données, Symfony, Django, controller, repository, model, migration |
| **Frontend** | UI, interface, composant, React, Vue, affichage, formulaire, bouton, page, écran, CSS, style |
| **DevOps** | déploiement, deploy, CI/CD, Docker, config, environnement, serveur, infra |
| **Data** | export, import, CSV, Excel, PDF, rapport, données, migration de données |
| **Auth** | login, authentification, mot de passe, session, token, SSO, permission |
| **Test** | test, QA, validation, vérification, coverage, spec |

**Domain change between segments** → +25 points

---

## Phase 4: Decision

### Multi-Task Threshold

```
IF (segments_with_score_≥40 >= 2) THEN
    RESULT = MULTI-TASK
ELSE
    RESULT = MONO-TASK
```

### Aggressive Mode Parameters

| Parameter | Value |
|-----------|-------|
| Multi-task threshold | 40 |
| Explicit marker weight | 30 |
| Implicit marker weight | 15 |
| Domain change weight | 25 |
| Minimum segments for multi | 2 |
| Maximum tasks per dictation | 5 |

---

## Decision Matrix

### Examples

| Scenario | Dictation | Segments | Scores | Decision |
|----------|-----------|----------|--------|----------|
| Mono simple | "Fixer le bug de login" | 1 | - | MONO |
| Mono complex | "Fixer le bug login et améliorer les messages d'erreur" | 1 | Same subject | MONO |
| Multi explicit | "Fixer le login. **Aussi**, ajouter l'export PDF" | 2 | [40, 55] | MULTI (2) |
| Multi implicit | "Le login est cassé... les rapports ne s'affichent plus" | 2 | [40, 40] | MULTI (2) |
| Multi complex | "Bug login, **et puis** export PDF, **ah et** refacto auth" | 3 | [40, 55, 50] | MULTI (3) |

---

## Edge Cases

### Handled as MONO-TASK

| Pattern | Reason | Example |
|---------|--------|---------|
| Parent + children | Colon indicates subtasks | "Refacto du module: séparer service, nettoyer tests" |
| Feature + dependency | Same logical unit | "Créer l'API, puis le bouton qui l'appelle" → See note |
| Correction + improvement | Same context | "Fixer le bug et en profiter pour refacto" |

**Note on dependencies**: "Créer l'API export, puis le bouton frontend" is detected as **MULTI (2)** because domains differ (Backend vs Frontend), even though there's dependency.

### Handled as MULTI-TASK

| Pattern | Reason | Example |
|---------|--------|---------|
| Bug list | Distinct issues | "Login cassé, dashboard lent, export plante" → 3 |
| Different domains | Backend + Frontend | "API export et bouton frontend" → 2 |
| Explicit enumeration | Clear separation | "Premièrement X, deuxièmement Y" → 2 |

### Low Confidence Handling

| Condition | Action |
|-----------|--------|
| Vague dictation | MONO + confidence LOW |
| All segments < 40 | MONO |
| > 5 tasks detected | Warning: "Dictée très dense, vérifier découpage" |
| Task < 10 words | Warning: "Tâche très courte, contexte manquant?" |

---

## Confidence Calculation

### Per-Detection Confidence

```
CONFIDENCE = 
    IF (highest_score > 60 AND no_ambiguity) → HIGH
    ELIF (highest_score > 40 AND minor_ambiguity) → MEDIUM
    ELSE → LOW
```

### Display in Checkpoint

```
📋 **3 tâches détectées** (confiance: HAUTE)
```

or

```
📋 **2 tâches détectées** (⚠️ confiance: MOYENNE)
Vérifiez le découpage avant validation.
```

---

## Checkpoint Commands Reference

| Command | Syntax | Effect |
|---------|--------|--------|
| Validate all | `ok` | Generate all briefs |
| Validate partial | `ok N,M` | Generate only N and M |
| Merge | `merge N,M` | Combine N and M into single task |
| Edit title | `edit N "new title"` | Change title of task N |
| Drop | `drop N` | Remove task N from batch |
| Split | `split N` | Request sub-split of task N |
| Reanalyze | `reanalyze` | Re-run detection from start |
| Free correction | (text) | Interpreted naturally |

---

## Testing Detection

### Test Cases

| Input | Expected |
|-------|----------|
| "fixer le bug login" | MONO |
| "fixer le bug login et aussi ajouter export" | MULTI (2) |
| "bug login, export PDF, refacto auth" | MULTI (3) |
| "créer l'API et le bouton frontend" | MULTI (2) |
| "refacto module: service, tests, docs" | MONO |
| "premièrement X, deuxièmement Y" | MULTI (2) |
