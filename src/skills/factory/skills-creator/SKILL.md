---
name: skills-creator
description: >-
  Création guidée de nouveaux Skills Claude Code. Workflow en 6 phases avec
  templates, validation et tests de triggering. Use when: /epci:create skill
  invoqué. Not for: modification de skills existants, autres composants.
---

# Skills Creator

## Overview

Guide la création de nouveaux skills avec validation automatique.

## Workflow en 6 phases

### Phase 1 : Qualification

Questions pour définir le skill :

1. **Domaine** : Quel domaine technique couvre ce skill ?
2. **Trigger** : Quand ce skill doit-il être auto-invoqué ?
3. **Exclusions** : Quand NE doit-il PAS être invoqué ?
4. **Catégorie** : core | stack | factory | custom ?
5. **Outils** : Quels outils sont nécessaires ?

### Phase 2 : Définition

Définir les éléments du frontmatter :

```yaml
---
name: [kebab-case, ≤64 chars]
description: >-
  [Capacité]. [Auto-invoke when: conditions].
  [Not for: exclusions].
allowed-tools: [Read, Write, ...]  # Si nécessaire
---
```

**Formule description obligatoire :**
```
[Ce que fait le skill]. Use when: [conditions d'activation].
Not for: [exclusions claires].
```

### Phase 3 : Contenu

Générer le contenu du skill :

```markdown
# [Nom du Skill]

## Overview
[Description en 2-3 phrases]

## [Section principale 1]
[Contenu structuré avec tables, code, exemples]

## [Section principale 2]
[...]

## Quick Reference
[Cheatsheet, checklist, table de référence rapide]

## Common Patterns
[Patterns fréquents, exemples pratiques]

## Anti-patterns
[Ce qu'il faut éviter]
```

**Contraintes :**
- < 5000 tokens
- Structure avec headers
- Tables pour les références
- Exemples de code si applicable

### Phase 4 : Références (optionnel)

Si le skill nécessite des références :

```
skills/<category>/<name>/
├── SKILL.md
└── references/
    ├── reference-1.md
    └── reference-2.md
```

### Phase 5 : Validation

Exécuter le script de validation :

```bash
python scripts/validate_skill.py skills/<category>/<name>/
```

**Critères :**
- [ ] YAML frontmatter valide
- [ ] Nom kebab-case ≤ 64 chars
- [ ] Description avec "Use when:" et "Not for:"
- [ ] Description ≤ 1024 chars
- [ ] Contenu < 5000 tokens
- [ ] Références existent si mentionnées

### Phase 6 : Test de triggering

Tester l'auto-invocation :

```bash
python scripts/test_triggering.py skills/<category>/<name>/
```

**Tests automatiques :**
- Requêtes qui DOIVENT trigger → vérifié
- Requêtes qui NE doivent PAS trigger → vérifié

## Templates

### Template Core Skill

```markdown
---
name: [name]
description: >-
  [Capacité générique]. Use when: [contextes généraux].
  Not for: [exclusions].
---

# [Name] Skill

## Overview
[Description]

## Concepts
[Concepts fondamentaux]

## Patterns
[Patterns applicables]

## Quick Reference
[Table de référence]
```

### Template Stack Skill

```markdown
---
name: [stack]-[framework]
description: >-
  Patterns et conventions pour [Stack/Framework]. Inclut [outils].
  Use when: développement [stack], [detection file] détecté.
  Not for: [autres stacks/frameworks].
---

# [Stack] Development Patterns

## Overview
[Description]

## Auto-détection
[Comment le skill est détecté]

## Architecture
[Structure recommandée]

## Patterns
[Patterns spécifiques]

## Testing
[Patterns de test]

## Commands
[Commandes utiles]
```

## Exemples de descriptions

### Bon ✅

```
Patterns d'architecture pour microservices. Inclut service mesh,
circuit breaker, saga patterns. Use when: conception microservices,
architecture distribuée. Not for: monolithes, applications simples.
```

### Mauvais ❌

```
Un skill pour les microservices.
```
(Manque "Use when:" et "Not for:")

## Output

```markdown
✅ **SKILL CREATED**

Skill : [name]
Catégorie : [category]
Fichier : skills/[category]/[name]/SKILL.md

Validation : ✅ PASSED (6/6 checks)
Triggering : ✅ PASSED (X/Y tests)

Prochaines étapes :
1. Personnaliser le contenu
2. Ajouter des références si nécessaire
3. Tester avec des requêtes réelles
```

## Règles de conception

### Les 10 Golden Rules

1. **Nom kebab-case** — `my-skill` pas `MySkill`
2. **Description formulée** — "Use when:" + "Not for:"
3. **Focus unique** — Un skill = un domaine
4. **Auto-détectable** — Conditions de trigger claires
5. **Exclusions explicites** — Éviter les faux positifs
6. **Contenu < 5000 tokens** — Chargement rapide
7. **Structure avec headers** — Navigation facile
8. **Exemples pratiques** — Code, tables, patterns
9. **Quick Reference** — Lookup rapide
10. **Anti-patterns** — Ce qu'il faut éviter
