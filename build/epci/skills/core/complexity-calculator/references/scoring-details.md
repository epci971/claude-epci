# Formule de Scoring Detaillee

Scoring detaille pour le calcul de complexite des taches EPCI v6.0.

## Vue d'ensemble

Le score final determine la categorie de complexite:
- **< 25**: TINY
- **25-49**: SMALL
- **50-74**: STANDARD
- **75+**: LARGE

---

## Conversion des Facteurs en Scores (0-100)

### Files Score (Poids: 30%)

Nombre de fichiers impactes par la modification.

| Files | Score | Justification |
|-------|-------|---------------|
| 1 | 10 | Modification isolee |
| 2-3 | 30 | Changement localise |
| 4-6 | 50 | Impact multi-composants |
| 7-10 | 70 | Refactoring significatif |
| 10+ | 100 | Changement architectural |

### LOC Score (Poids: 25%)

Estimation des lignes de code modifiees/ajoutees.

| LOC | Score | Justification |
|-----|-------|---------------|
| < 20 | 10 | Micro-changement |
| 20-50 | 25 | Petit changement |
| 51-200 | 50 | Changement moyen |
| 201-500 | 70 | Changement important |
| 501-1000 | 85 | Feature majeure |
| > 1000 | 100 | Projet significatif |

### Dependencies Score (Poids: 20%)

Nombre de dependances inter-modules affectees.

| Dependencies | Score | Justification |
|--------------|-------|---------------|
| 0 | 0 | Changement isole |
| 1 | 20 | Impact limite |
| 2-3 | 40 | Impact modere |
| 4-6 | 70 | Impact etendu |
| 7+ | 100 | Impact systemique |

### Tests Score (Poids: 15%)

Nombre de tests a ajouter/modifier.

| Tests | Score | Justification |
|-------|-------|---------------|
| 0 | 0 | Pas de tests requis |
| 1-2 | 20 | Tests minimaux |
| 3-5 | 40 | Couverture standard |
| 6-10 | 70 | Couverture extensive |
| 10+ | 100 | Suite de tests complete |

### Risk Score (Poids: 10%)

Niveau de risque base sur le chemin critique.

| Risk Level | Score | Indicateurs |
|------------|-------|-------------|
| low | 10 | Code non-critique, facilement reversible |
| medium | 50 | Code business, tests existants |
| high | 100 | Code critique, peu de tests, production |

---

## Risk Factors Detailles

Detection automatique des zones a risque par patterns de fichiers.

| Factor | Weight | Detection Pattern |
|--------|--------|-------------------|
| **Security patterns** | +30 | `**/auth/**`, `**/security/**`, `**/payment/**` |
| **Database migration** | +25 | `**/migrations/**`, schema changes |
| **Breaking API** | +25 | API endpoint modification, contract changes |
| **Multi-service** | +20 | Cross-service dependencies |
| **No tests** | +15 | Test coverage < 30% for affected files |
| **Legacy code** | +10 | Files > 500 LOC without recent changes |

**Calcul du Risk Score:**

```
risk_score = min(100, sum(detected_factors))
```

**Exemples:**
- Auth file + no tests → 30 + 15 = 45 → medium-high risk
- Migration + breaking API → 25 + 25 = 50 → high risk
- Legacy code only → 10 → low risk

**Max cumulative risk:** 100 (capped)

---

## Formule de Calcul

```
score_final = (
  files_score * 0.30 +
  loc_score * 0.25 +
  deps_score * 0.20 +
  tests_score * 0.15 +
  risk_score * 0.10
)
```

### Seuils de Categories

| Score Final | Categorie | Workflow |
|-------------|-----------|----------|
| 0-24 | TINY | `/quick` |
| 25-49 | SMALL | `/quick` |
| 50-74 | STANDARD | `/implement` |
| 75-100 | LARGE | `/implement --large` |

---

## Exemples de Calcul

### Exemple 1: Bug Fix Simple (TINY)

**Contexte**: Corriger une typo dans un message d'erreur

| Facteur | Valeur | Score |
|---------|--------|-------|
| Files | 1 | 10 |
| LOC | 5 | 10 |
| Dependencies | 0 | 0 |
| Tests | 0 | 0 |
| Risk | low | 10 |

**Calcul**:
```
score = (10 * 0.30) + (10 * 0.25) + (0 * 0.20) + (0 * 0.15) + (10 * 0.10)
score = 3 + 2.5 + 0 + 0 + 1
score = 6.5 → TINY
```

**Resultat**: TINY → `/quick`

---

### Exemple 2: Ajout Validation (SMALL)

**Contexte**: Ajouter validation email sur un formulaire existant

| Facteur | Valeur | Score |
|---------|--------|-------|
| Files | 2 | 30 |
| LOC | 40 | 25 |
| Dependencies | 1 | 20 |
| Tests | 3 | 40 |
| Risk | low | 10 |

**Calcul**:
```
score = (30 * 0.30) + (25 * 0.25) + (20 * 0.20) + (40 * 0.15) + (10 * 0.10)
score = 9 + 6.25 + 4 + 6 + 1
score = 26.25 → SMALL
```

**Resultat**: SMALL → `/quick`

---

### Exemple 3: Nouvelle Feature API (STANDARD)

**Contexte**: Ajouter endpoint CRUD pour une nouvelle entite

| Facteur | Valeur | Score |
|---------|--------|-------|
| Files | 6 | 50 |
| LOC | 350 | 70 |
| Dependencies | 3 | 40 |
| Tests | 8 | 70 |
| Risk | medium | 50 |

**Calcul**:
```
score = (50 * 0.30) + (70 * 0.25) + (40 * 0.20) + (70 * 0.15) + (50 * 0.10)
score = 15 + 17.5 + 8 + 10.5 + 5
score = 56 → STANDARD
```

**Resultat**: STANDARD → `/implement`

---

### Exemple 4: Refactoring Systeme Auth (LARGE)

**Contexte**: Migrer d'une auth session vers JWT

| Facteur | Valeur | Score |
|---------|--------|-------|
| Files | 15 | 100 |
| LOC | 1200 | 100 |
| Dependencies | 8 | 100 |
| Tests | 20 | 100 |
| Risk | high | 100 |

**Calcul**:
```
score = (100 * 0.30) + (100 * 0.25) + (100 * 0.20) + (100 * 0.15) + (100 * 0.10)
score = 30 + 25 + 20 + 15 + 10
score = 100 → LARGE
```

**Resultat**: LARGE → `/implement --large`

---

## Cas Limites

### Ajustements Automatiques

| Condition | Ajustement |
|-----------|------------|
| Files > 10 et Risk = high | Score minimum 75 (force LARGE) |
| Files = 1 et LOC < 20 | Score maximum 24 (force TINY) |
| Dependencies > 5 | +10 au score final |

### Indicateur de Confiance

| Confiance | Condition |
|-----------|-----------|
| 0.9+ | Tous facteurs connus avec precision |
| 0.7-0.9 | 1-2 facteurs estimes |
| 0.5-0.7 | 3+ facteurs estimes |
| < 0.5 | Analyse insuffisante, demander plus de contexte |

---

## Quick Reference

```
TINY (< 25):     1 fichier, < 50 LOC, aucune dependance
SMALL (25-49):   2-3 fichiers, < 200 LOC, dependances limitees
STANDARD (50-74): 4-10 fichiers, < 1000 LOC, impact modere
LARGE (75+):     10+ fichiers, > 1000 LOC, impact systemique
```
