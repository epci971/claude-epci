---
description: >-
  Workflow EPCI condensé pour features TINY et SMALL. Single-pass sans
  Feature Document formel. Mode TINY: <50 LOC, 1 fichier, pas de tests.
  Mode SMALL: <200 LOC, 2-3 fichiers, tests optionnels.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---

# EPCI Quick — Workflow Condensé

## Overview

Workflow simplifié pour les petites modifications.
Pas de Feature Document formel, pas de breakpoints.

## Modes

### Mode TINY

| Critère | Valeur |
|---------|--------|
| Fichiers | 1 seul |
| LOC | < 50 |
| Tests | Non requis |
| Durée | < 15 minutes |
| Exemples | Typo, config, petit fix |

### Mode SMALL

| Critère | Valeur |
|---------|--------|
| Fichiers | 2-3 |
| LOC | < 200 |
| Tests | Optionnels |
| Durée | 15-60 minutes |
| Exemples | Petite feature, refactor local |

## Process

### 1. Détection du mode

```
Si brief mentionne :
- 1 seul fichier + modification simple → TINY
- 2-3 fichiers OU tests demandés → SMALL
```

### 2. Analyse rapide

- Identifier le(s) fichier(s) à modifier
- Vérifier les dépendances directes
- Estimer l'impact

### 3. Implémentation

#### Mode TINY

```
1. Lire le fichier cible
2. Identifier la modification
3. Appliquer le changement
4. Vérifier (lint, syntax)
5. Terminé
```

#### Mode SMALL

```
1. Lire les fichiers concernés
2. Planifier mentalement (pas de doc formelle)
3. Pour chaque modification :
   a. Si test demandé → écrire test d'abord
   b. Implémenter le changement
   c. Vérifier
4. Exécuter les tests existants
5. Review rapide si nécessaire
```

### 4. Review (optionnel)

Pour SMALL uniquement, invoquer @code-reviewer en mode light :
- Focus sur bugs évidents
- Erreurs de syntaxe/typage
- Tests manquants (si demandés)

**Pas de revue architecture ou optimisation.**

### 5. Commit

Format Conventional Commits simplifié :

```
fix(scope): description courte
```

ou

```
feat(scope): description courte
```

## Output

### Mode TINY

```markdown
✅ **TINY COMPLETE**

Modification appliquée à `path/to/file.ext`
- Changement : [description]
- Lignes : +X / -Y

Prêt à committer.
```

### Mode SMALL

```markdown
✅ **SMALL COMPLETE**

Fichiers modifiés :
- `path/to/file1.ext` (+X / -Y)
- `path/to/file2.ext` (+Z / -W)

Tests : [X passing | Non requis]
Review : [@code-reviewer light | Non requis]

Prêt à committer.
```

## Exemples

### Exemple TINY

**Brief :** "Corriger le typo 'recieve' en 'receive' dans UserService"

```
→ Mode : TINY
→ Fichier : src/Service/UserService.php
→ Action : Rechercher/remplacer
→ Commit : fix(user): correct typo in UserService
```

### Exemple SMALL

**Brief :** "Ajouter une méthode isActive() à l'entité User"

```
→ Mode : SMALL
→ Fichiers :
  - src/Entity/User.php (ajouter méthode)
  - tests/Unit/Entity/UserTest.php (ajouter test)
→ Actions :
  1. Écrire test pour isActive()
  2. Implémenter isActive()
  3. Vérifier tests
→ Commit : feat(user): add isActive method
```

## Décision de mode

```
                    ┌─────────────┐
                    │ Brief reçu  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Combien de  │
                    │  fichiers?  │
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
      ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
      │    1    │    │   2-3   │    │   4+    │
      └────┬────┘    └────┬────┘    └────┬────┘
           │               │               │
      ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
      │  TINY   │    │  SMALL  │    │→ /epci  │
      └─────────┘    └─────────┘    └─────────┘
```

## Quand escalader vers /epci

Escalader si durant l'implémentation :
- Plus de 3 fichiers impactés découverts
- Risque de régression identifié
- Complexité sous-estimée
- Tests d'intégration nécessaires

```
⚠️ **ESCALADE RECOMMANDÉE**

La modification est plus complexe qu'anticipé :
- [Raison 1]
- [Raison 2]

Recommandation : Passer à `/epci` pour un workflow structuré.
```

## Skills chargés

- `epci-core` (concepts base)
- `code-conventions` (standards)
- `[stack-skill]` (auto-détecté)

## Différences avec /epci

| Aspect | /epci-quick | /epci |
|--------|-------------|-------|
| Feature Document | Non | Oui |
| Breakpoints | Non | Oui (2) |
| @plan-validator | Non | Oui |
| @code-reviewer | Light (SMALL) | Full |
| @security-auditor | Non | Conditionnel |
| @qa-reviewer | Non | Conditionnel |
| @doc-generator | Non | Oui |
| Thinking | Standard | think / think hard |
