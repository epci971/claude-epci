---
name: subagents-creator
description: >-
  Création guidée de nouveaux subagents Claude Code. Workflow avec templates,
  validation et principe de moindre privilège. Use when: /epci:create agent
  invoqué. Not for: skills ou commandes, subagents natifs Claude Code.
---

# Subagents Creator

## Overview

Guide la création de nouveaux subagents avec validation automatique.
Focus sur le principe de moindre privilège et la mission unique.

## Concepts clés

### Qu'est-ce qu'un subagent ?

Un subagent est un agent spécialisé avec :
- **Mission unique** — Un seul objectif bien défini
- **Outils restreints** — Minimum nécessaire
- **Modèle adapté** — Haiku (rapide) ou Sonnet (complex)
- **Format de sortie** — Structuré et prévisible

### Subagents natifs vs Custom

| Type | Exemples | Usage |
|------|----------|-------|
| **Natifs** | @Explore, @Plan | Fournis par Claude Code |
| **Custom** | @code-reviewer, @security-auditor | Créés par EPCI |

## Workflow

### Phase 1 : Qualification

Questions pour définir le subagent :

1. **Mission** : Quelle est la tâche unique ?
2. **Invocation** : Quand est-il appelé ?
3. **Input** : Que reçoit-il en entrée ?
4. **Output** : Que produit-il ?
5. **Outils** : De quels outils a-t-il besoin ?

### Phase 2 : Définition du frontmatter

```yaml
---
name: [kebab-case]
description: >-
  [Mission en 1-2 phrases]. [Quand il est invoqué].
  [Ce qu'il produit comme output].
model: claude-sonnet-4-20250514  # ou haiku pour tâches simples
allowed-tools: [Read, Grep]  # MINIMUM NÉCESSAIRE
---
```

### Phase 3 : Structure du contenu

```markdown
# [Nom] Agent

## Mission
[Description claire de la mission unique]

## Conditions d'invocation
[Quand ce subagent est appelé]

## Checklist
### [Catégorie 1]
- [ ] Critère 1
- [ ] Critère 2

### [Catégorie 2]
- [ ] Critère 3

## Niveaux de sévérité
| Niveau | Critères | Action |
|--------|----------|--------|
| 🔴 Critical | ... | Must fix |
| 🟠 Important | ... | Should fix |
| 🟡 Minor | ... | Nice to have |

## Format de sortie
```markdown
## [Output Report Title]

### Summary
[...]

### Findings
[...]

### Verdict
**[APPROVED | NEEDS_FIXES | ...]**
```
```

### Phase 4 : Validation

```bash
python scripts/validate_subagent.py agents/[name].md
```

**Critères :**
- [ ] Fichier .md existe
- [ ] YAML frontmatter valide
- [ ] Nom kebab-case ≤ 64 chars
- [ ] Description claire
- [ ] Outils restrictifs (principe de moindre privilège)
- [ ] Contenu focalisé (< 2000 tokens)

## Principe de moindre privilège

### Outils par type de mission

| Mission | Outils recommandés |
|---------|-------------------|
| Lecture/Analyse | `Read`, `Grep`, `Glob` |
| Validation | `Read`, `Grep` |
| Génération | `Read`, `Write` |
| Exécution | `Read`, `Bash` |

### ⚠️ Outils à éviter sauf nécessité

- `Write` — Éviter si le subagent n'a pas besoin de créer des fichiers
- `Edit` — Éviter si le subagent ne modifie pas de fichiers
- `Bash` — Éviter si pas d'exécution de commandes nécessaire

## Template

```markdown
---
name: [name]
description: >-
  [Mission unique et claire]. [Contexte d'invocation].
  [Output produit].
model: claude-sonnet-4-20250514
allowed-tools: [Read, Grep]
---

# [Name] Agent

## Mission

[Description de la mission unique en 2-3 phrases.
Ce que le subagent fait et pourquoi.]

## Conditions d'invocation

Invoqué automatiquement si :
- [Condition 1]
- [Condition 2]

OU invoqué manuellement par :
- [Commande/contexte]

## Input attendu

- [Input 1] — [Description]
- [Input 2] — [Description]

## Checklist

### [Catégorie 1]
- [ ] Critère vérifiable 1
- [ ] Critère vérifiable 2
- [ ] Critère vérifiable 3

### [Catégorie 2]
- [ ] Critère vérifiable 4
- [ ] Critère vérifiable 5

## Niveaux de sévérité

| Niveau | Critères | Action requise |
|--------|----------|----------------|
| 🔴 Critical | [Définition] | Must fix |
| 🟠 Important | [Définition] | Should fix |
| 🟡 Minor | [Définition] | Nice to have |

## Format de sortie

```markdown
## [Report Title]

### Summary
[1-2 phrases résumant le résultat]

### [Section principale]
[Détails structurés]

### Issues (si applicable)

#### 🔴 Critical
1. **[Titre]**
   - **Location** : [file:line]
   - **Issue** : [Description]
   - **Fix** : [Solution suggérée]

### Verdict
**[APPROVED | NEEDS_FIXES | REJECTED]**

**Reasoning:** [Justification technique]
```

## Process

1. [Étape 1]
2. [Étape 2]
3. [Étape 3]
```

## Bonnes pratiques

### Mission

| Faire | Éviter |
|-------|--------|
| Mission unique | Multi-tâches |
| Verbe d'action | Description vague |
| Scope limité | "Tout vérifier" |

### Outils

| Faire | Éviter |
|-------|--------|
| Minimum nécessaire | Tous les outils |
| Read-only si possible | Write sans raison |
| Justifier chaque outil | Copier d'autres agents |

### Output

| Faire | Éviter |
|-------|--------|
| Format structuré | Texte libre |
| Verdicts clairs | Ambiguïté |
| Preuves/locations | Affirmations sans preuve |

## Output

```markdown
✅ **SUBAGENT CREATED**

Agent : [name]
Fichier : agents/[name].md

Validation : ✅ PASSED (5/5 checks)
- Mission : Unique et claire
- Outils : Restrictifs (X outils)
- Contenu : < 2000 tokens

Prochaines étapes :
1. Personnaliser la checklist
2. Définir les niveaux de sévérité
3. Tester avec des cas réels
```
