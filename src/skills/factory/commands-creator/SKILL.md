---
name: commands-creator
description: >-
  Création guidée de nouvelles commandes Claude Code. Workflow avec templates,
  validation du frontmatter et structure. Use when: /epci:create command invoqué.
  Not for: modification de commandes existantes, skills ou subagents.
---

# Commands Creator

## Overview

Guide la création de nouvelles commandes avec validation automatique.

## Workflow

### Phase 1 : Qualification

Questions pour définir la commande :

1. **Objectif** : Que fait cette commande ?
2. **Arguments** : Quels arguments accepte-t-elle ?
3. **Outils** : Quels outils sont nécessaires ?
4. **Output** : Quel est le résultat attendu ?
5. **Intégrations** : Quels skills/subagents utilise-t-elle ?

### Phase 2 : Définition du frontmatter

```yaml
---
description: >-
  [Action en infinitif]. [Contexte d'usage]. [Résultat attendu].
  [Contraintes ou limitations éventuelles].
argument-hint: [arg1] [arg2] [--flag]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---
```

### Phase 3 : Structure du contenu

```markdown
# [Nom de la commande]

## Overview
[Description en 2-3 phrases]

## Arguments
| Argument | Description | Défaut |
|----------|-------------|--------|
| `arg1` | Description | - |
| `--flag` | Description | false |

## Process
### Étape 1 : [Nom]
[Description détaillée]

### Étape 2 : [Nom]
[Description détaillée]

## Skills chargés
- `skill-1` (raison)
- `skill-2` (raison)

## Subagents invoqués
- `@subagent-1` — Rôle

## Output
[Format de sortie attendu]

## Exemples
[Exemples d'utilisation]
```

### Phase 4 : Validation

```bash
python scripts/validate_command.py commands/[name].md
```

**Critères :**
- [ ] Fichier .md existe
- [ ] YAML frontmatter valide
- [ ] Description présente et claire
- [ ] allowed-tools valides
- [ ] Structure avec headers

## Template

```markdown
---
description: >-
  [Action principale de la commande]. [Contexte d'utilisation].
  [Ce que la commande produit comme résultat].
argument-hint: [arguments-et-flags]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---

# [Nom de la Commande]

## Overview

[Description de la commande en 2-3 phrases. Inclure le cas d'usage
principal et le type de projet/contexte où elle est utile.]

## Arguments

| Argument | Description | Requis | Défaut |
|----------|-------------|--------|--------|
| `[arg]` | Description | Oui/Non | - |
| `--[flag]` | Description | Non | false |

## Process

### 1. [Première étape]

[Description de l'étape]

```
[Code ou pseudo-code si applicable]
```

### 2. [Deuxième étape]

[Description de l'étape]

### 3. [Troisième étape]

[Description de l'étape]

## Skills chargés

- `[skill-1]` — [Raison du chargement]
- `[skill-2]` — [Raison du chargement]

## Subagents invoqués

| Subagent | Condition | Rôle |
|----------|-----------|------|
| `@[name]` | [Quand] | [Ce qu'il fait] |

## Output

[Description du format de sortie]

```markdown
[Exemple de sortie]
```

## Exemples

### Exemple 1 : [Cas d'usage]

```
> /[commande] [arguments]

[Résultat attendu]
```

### Exemple 2 : [Autre cas]

```
> /[commande] --[flag] [arguments]

[Résultat attendu]
```

## Erreurs courantes

| Erreur | Cause | Solution |
|--------|-------|----------|
| [Erreur 1] | [Cause] | [Solution] |

## Voir aussi

- `/[commande-liée]` — [Relation]
```

## Bonnes pratiques

### Description

| Faire | Éviter |
|-------|--------|
| Verbe à l'infinitif | Forme passive |
| Concis (< 200 chars) | Description trop longue |
| Contexte clair | Jargon technique |

### Arguments

| Faire | Éviter |
|-------|--------|
| Noms explicites | Abréviations cryptiques |
| Valeurs par défaut | Tous obligatoires |
| Documentation complète | Args sans description |

### Process

| Faire | Éviter |
|-------|--------|
| Étapes numérotées | Flux confus |
| Conditions claires | Logique implicite |
| Exemples concrets | Descriptions abstraites |

## Output

```markdown
✅ **COMMAND CREATED**

Commande : [name]
Fichier : commands/[name].md

Validation : ✅ PASSED (5/5 checks)

Prochaines étapes :
1. Personnaliser le process
2. Ajouter des exemples
3. Tester la commande
```

## Outils disponibles

| Outil | Usage |
|-------|-------|
| `Read` | Lecture de fichiers |
| `Write` | Création de fichiers |
| `Edit` | Modification de fichiers |
| `Bash` | Commandes shell |
| `Grep` | Recherche dans le code |
| `Glob` | Pattern matching fichiers |
| `Task` | Invocation de subagents |
| `WebFetch` | Requêtes HTTP |
| `TodoRead/Write` | Gestion des tâches |
