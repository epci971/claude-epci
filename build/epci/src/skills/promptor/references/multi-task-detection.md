# Multi-Task Detection — Algorithm Reference

> Aggressive multi-task detection for dictation segmentation

---

## Overview

Promptor uses **aggressive** multi-task detection. The skill tends toward detecting
multiple tasks when ambiguous, allowing users to merge if needed.

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

## Rupture Markers

### Explicit (+30 points)

| Category | French | English |
|----------|--------|---------|
| **Addition** | "aussi", "également", "en plus", "et puis" | "also", "plus", "and then" |
| **Rupture** | "sinon", "autre chose", "autrement", "à part ça" | "otherwise", "besides" |
| **Transition** | "ah et", "oh et", "tiens", "au fait" | "oh and", "by the way" |
| **Enumeration** | "premièrement... deuxièmement", "d'abord... ensuite" | "first... then" |

### Implicit (+15-25 points)

| Pattern | Points |
|---------|--------|
| Subject change | +15 |
| Action verb repetition | +15 |
| Domain change | +25 |

---

## Independence Score

```
SCORE = SUBJECT_DIFFERENT × 25 +
        ACTION_DIFFERENT × 20 +
        DOMAIN_DIFFERENT × 25 +
        EXPLICIT_MARKER × 30 +
        IMPLICIT_MARKER × 15
```

### Domain Detection

| Domain | Keywords |
|--------|----------|
| **Backend** | API, service, endpoint, BDD, Symfony, Django, controller, model |
| **Frontend** | UI, interface, composant, React, Vue, formulaire, bouton, page |
| **DevOps** | déploiement, CI/CD, Docker, serveur, infra |
| **Data** | export, import, CSV, Excel, PDF, rapport |
| **Auth** | login, authentification, mot de passe, token, SSO |

---

## Decision Threshold

```
IF (segments_with_score_≥40 >= 2) THEN
    RESULT = MULTI-TASK
ELSE
    RESULT = MONO-TASK
```

### Parameters

| Parameter | Value |
|-----------|-------|
| Multi-task threshold | 40 |
| Explicit marker weight | 30 |
| Domain change weight | 25 |
| Maximum tasks per dictation | 5 |

---

## Examples

| Input | Segments | Decision |
|-------|----------|----------|
| "fixer le bug login" | 1 | MONO |
| "fixer le bug login et aussi ajouter export" | 2 | MULTI (2) |
| "bug login, export PDF, refacto auth" | 3 | MULTI (3) |
| "créer l'API et le bouton frontend" | 2 | MULTI (2) |
| "refacto module: service, tests, docs" | 1 | MONO |

---

## Confidence Levels

| Level | Criteria |
|-------|----------|
| HIGH | Score > 60, no ambiguity |
| MEDIUM | Score > 40, minor ambiguity |
| LOW | Score < 40 or contradictions |
