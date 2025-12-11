---
description: >-
  Component Factory EPCI. Crée de nouveaux composants (skills, commands,
  subagents) en suivant les standards EPCI. Dispatcher vers le skill
  creator approprié.
argument-hint: skill|command|agent <name>
allowed-tools: [Read, Write, Glob, Bash]
---

# EPCI Create — Component Factory

## Overview

Commande dispatcher pour créer de nouveaux composants EPCI.
Route vers le skill creator approprié selon le type demandé.

## Usage

```
/epci:create <type> <name>
```

| Argument | Description | Exemples |
|----------|-------------|----------|
| `type` | Type de composant | `skill`, `command`, `agent` |
| `name` | Nom du composant (kebab-case) | `my-new-skill` |

## Routing

| Type | Skill invoqué | Output |
|------|---------------|--------|
| `skill` | `skills-creator` | `skills/<category>/<name>/SKILL.md` |
| `command` | `commands-creator` | `commands/<name>.md` |
| `agent` | `subagents-creator` | `agents/<name>.md` |

## Process

### 1. Validation des arguments

```
Si type manquant → Erreur + usage
Si name manquant → Erreur + usage
Si name pas kebab-case → Erreur + format attendu
Si composant existe déjà → Erreur + suggestion
```

### 2. Routing vers le skill creator

```
switch (type):
    case "skill":
        → Invoquer skill `skills-creator`
    case "command":
        → Invoquer skill `commands-creator`
    case "agent":
        → Invoquer skill `subagents-creator`
    default:
        → Erreur: type inconnu
```

### 3. Phase interactive (gérée par le skill)

Le skill creator invoqué guide l'utilisateur à travers :
- Questions sur le composant
- Génération du template
- Personnalisation
- Validation
- Tests

## Exemples

### Créer un skill

```
> /epci:create skill api-monitoring

→ Invoque skills-creator
→ Questions interactives sur le skill
→ Génère skills/custom/api-monitoring/SKILL.md
→ Valide avec validate_skill.py
→ Teste le triggering
```

### Créer une commande

```
> /epci:create command deploy

→ Invoque commands-creator
→ Questions sur la commande
→ Génère commands/deploy.md
→ Valide avec validate_command.py
```

### Créer un subagent

```
> /epci:create agent perf-analyzer

→ Invoque subagents-creator
→ Questions sur le subagent
→ Génère agents/perf-analyzer.md
→ Valide avec validate_subagent.py
```

## Validation

Après création, le script de validation approprié est exécuté :

| Type | Script |
|------|--------|
| skill | `python scripts/validate_skill.py <path>` |
| command | `python scripts/validate_command.py <path>` |
| agent | `python scripts/validate_subagent.py <path>` |

## Conventions de nommage

| Élément | Convention | Exemple |
|---------|------------|---------|
| Nom | kebab-case | `my-component` |
| Longueur | ≤ 64 caractères | - |
| Caractères | a-z, 0-9, - | - |

## Erreurs courantes

### Type invalide

```
❌ Type 'service' non reconnu.

Types supportés :
- skill    → Crée un nouveau skill
- command  → Crée une nouvelle commande
- agent    → Crée un nouveau subagent

Usage : /epci:create <type> <name>
```

### Nom invalide

```
❌ Nom 'MySkill' invalide.

Le nom doit être en kebab-case :
- Uniquement minuscules, chiffres et tirets
- Pas de tiret au début ou à la fin
- Maximum 64 caractères

Exemple correct : my-skill
```

### Composant existant

```
❌ Le skill 'api-monitoring' existe déjà.

Options :
1. Choisir un autre nom
2. Modifier le skill existant : skills/custom/api-monitoring/SKILL.md
3. Supprimer l'existant d'abord
```

## Output

```
✅ **COMPONENT CREATED**

Type : [skill | command | agent]
Nom : [name]
Fichier : [path]

Validation : ✅ PASSED (X/Y checks)

Prochaines étapes :
1. Personnaliser le contenu
2. Tester le composant
3. Documenter l'usage
```

## Arborescence des skills factory

```
skills/factory/
├── skills-creator/
│   ├── SKILL.md
│   ├── references/
│   │   └── skill-anatomy.md
│   ├── templates/
│   │   ├── core-skill.md
│   │   └── stack-skill.md
│   └── scripts/
│       └── post-create.py
│
├── commands-creator/
│   ├── SKILL.md
│   ├── references/
│   │   └── command-anatomy.md
│   └── templates/
│       └── command-template.md
│
├── subagents-creator/
│   ├── SKILL.md
│   ├── references/
│   │   └── agent-anatomy.md
│   └── templates/
│       └── agent-template.md
│
└── component-advisor/
    └── SKILL.md
```

## Skills chargés

- `component-advisor` (détection passive des opportunités)
- `[creator-skill]` (selon le type demandé)
