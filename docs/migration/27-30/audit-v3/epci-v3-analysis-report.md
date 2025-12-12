# EPCI v3 — Rapport d'Analyse Détaillé

## Comparaison Implémentation vs Cahier des Charges

**Date d'analyse** : 2025-12-11  
**Version analysée** : EPCI v3.0.0 (première implémentation Claude Code)

---

## 🔴 PROBLÈME CRITIQUE #1 : LANGUE

### Constat
**TOUT le contenu est rédigé en FRANÇAIS** alors que le cahier des charges prévoyait :
- Contenu des fichiers en **anglais**
- Claude répond dans la **langue de l'utilisateur**

### Fichiers impactés (TOUS)

| Catégorie | Fichiers | État actuel | État attendu |
|-----------|----------|-------------|--------------|
| Commands | 5 fichiers | 🔴 Français | Anglais |
| Agents | 5 fichiers | 🔴 Français | Anglais |
| Skills Core | 5 fichiers | 🔴 Français | Anglais |
| Skills Stack | 4 fichiers | 🟡 Mix FR/EN | Anglais |
| Skills Factory | 4 fichiers | 🔴 Français | Anglais |
| Scripts | 5 fichiers | 🟢 Anglais | Anglais ✅ |

### Exemples de texte à traduire

```yaml
# AVANT (actuel)
description: >-
  Point d'entrée EPCI. Analyse le brief brut, clarifie les ambiguïtés via
  questions itératives, évalue la complexité et route vers le workflow
  approprié (/epci-quick, /epci, /epci-spike).

# APRÈS (attendu)
description: >-
  EPCI entry point. Analyzes raw brief, clarifies ambiguities through
  iterative questions, evaluates complexity and routes to appropriate
  workflow (/epci-quick, /epci, /epci-spike).
```

### Action requise
**Traduire TOUS les fichiers .md en anglais** (sauf scripts Python qui sont déjà OK)

---

## 🔴 PROBLÈME CRITIQUE #2 : Fichiers Factory Manquants

### Constat
Les dossiers `references/`, `templates/`, `scripts/` dans les skills factory sont **VIDES** (créés mais sans contenu).

### Tableau des fichiers manquants

#### skills-creator/

| Chemin | Statut | Contenu attendu |
|--------|--------|-----------------|
| `references/best-practices.md` | ❌ MANQUANT | Golden rules, anti-patterns |
| `references/description-formulas.md` | ❌ MANQUANT | Formules "Use when" + "Not for" |
| `references/yaml-rules.md` | ❌ MANQUANT | Règles YAML frontmatter |
| `references/checklist.md` | ❌ MANQUANT | Checklist validation |
| `templates/skill-simple.md` | ❌ MANQUANT | Template skill basique |
| `templates/skill-advanced.md` | ❌ MANQUANT | Template skill avec références |
| `scripts/` | ⚠️ VIDE | Scripts locaux (ou référence vers /scripts/) |

#### commands-creator/

| Chemin | Statut | Contenu attendu |
|--------|--------|-----------------|
| `references/best-practices.md` | ❌ MANQUANT | Bonnes pratiques commandes |
| `references/frontmatter-guide.md` | ❌ MANQUANT | Guide frontmatter engineering |
| `references/argument-patterns.md` | ❌ MANQUANT | Patterns d'arguments |
| `references/checklist.md` | ❌ MANQUANT | Checklist validation |
| `templates/command-simple.md` | ❌ MANQUANT | Template commande basique |
| `templates/command-advanced.md` | ❌ MANQUANT | Template commande complexe |
| `scripts/` | ⚠️ VIDE | Scripts locaux |

#### subagents-creator/

| Chemin | Statut | Contenu attendu |
|--------|--------|-----------------|
| `references/best-practices.md` | ❌ MANQUANT | Bonnes pratiques subagents |
| `references/delegation-patterns.md` | ❌ MANQUANT | Patterns de délégation |
| `references/tools-restriction.md` | ❌ MANQUANT | Principe moindre privilège |
| `references/checklist.md` | ❌ MANQUANT | Checklist validation |
| `templates/subagent-template.md` | ❌ MANQUANT | Template subagent |
| `scripts/` | ⚠️ VIDE | Scripts locaux |

#### component-advisor/

| Chemin | Statut | Note |
|--------|--------|------|
| `references/` | ⚠️ VIDE | Optionnel selon CDC |
| `templates/` | ⚠️ VIDE | Optionnel selon CDC |

### Total fichiers manquants : **~18 fichiers**

---

## 🟠 PROBLÈME IMPORTANT #3 : plugin.json Incomplet

### Constat actuel

```json
{
  "name": "epci",
  "version": "3.0.0",
  "description": "...",
  "commands": ["./commands/epci-brief.md", ...],
  "agents": ["./agents/plan-validator.md", ...]
}
```

### Format attendu (selon cahier des charges)

```json
{
  "name": "epci",
  "version": "3.0.0",
  "description": "EPCI (Explore → Plan → Code → Inspect) - Structured development workflow",
  "commands": [
    {"name": "epci-brief", "file": "./commands/epci-brief.md", "description": "..."},
    ...
  ],
  "agents": [
    {"name": "plan-validator", "file": "./agents/plan-validator.md", "description": "..."},
    ...
  ],
  "skills": [
    {"name": "epci-core", "path": "./skills/core/epci-core/", "description": "..."},
    ...
  ],
  "keywords": ["epci", "workflow", "development", "tdd", "code-review", "documentation"]
}
```

### Problèmes identifiés

| Élément | État actuel | État attendu |
|---------|-------------|--------------|
| commands | ✅ Liste simple | 🟡 Objets avec name/file/description |
| agents | ✅ Liste simple | 🟡 Objets avec name/file/description |
| skills | ❌ ABSENT | Liste des 13 skills |
| keywords | ❌ ABSENT | Mots-clés pour recherche |

---

## 🟠 PROBLÈME IMPORTANT #4 : Scripts validate_all.py

### Constat
Le script `validate_all.py` cherche dans `src/` qui n'existe pas :

```python
src_path = project_root / "src"  # ← N'existe pas dans la structure actuelle
```

### Structure actuelle
```
epci-plugin/
├── commands/      # Pas dans src/
├── agents/        # Pas dans src/
├── skills/        # Pas dans src/
└── scripts/
```

### Correction requise
```python
# Chercher à la racine du plugin, pas dans src/
src_path = project_root  # ou project_root / ""
```

---

## 🟡 PROBLÈMES MINEURS

### 4.1 Dossier hooks/ vide

| État | Action |
|------|--------|
| Dossier créé mais vide | Soit supprimer, soit documenter l'usage futur |

### 4.2 Champ `activation` manquant dans agents

Le cahier des charges prévoyait un champ pour distinguer :
- `auto` : Claude décide quand invoquer
- `explicit` : L'utilisateur déclenche

**Agents concernés** : @security-auditor, @qa-reviewer (conditionnels)

### 4.3 Format Feature Document ID

| Prévu dans CDC | Implémenté |
|----------------|------------|
| `FD-YYYY-MM-DD-XXX` | `<feature-slug>.md` |

### 4.4 Sections "Subagents & Skills" dans commandes

Le CDC prévoyait des tableaux explicites :

```markdown
## Subagents & Skills

| Phase | Subagents | Skills |
|-------|-----------|--------|
| Phase 1 | @Plan, @plan-validator | epci-core, architecture-patterns |
```

**État actuel** : Information présente mais pas dans ce format tableau.

---

## ✅ CE QUI EST BIEN IMPLÉMENTÉ

### Structure globale

| Élément | État | Détail |
|---------|------|--------|
| Arborescence | ✅ OK | commands/, agents/, skills/, scripts/ |
| plugin.json | ✅ Existe | Format à enrichir |
| .claude-plugin/ | ✅ OK | Dossier correct |

### Commandes (5/5)

| Commande | Fichier | Frontmatter | Contenu | Breakpoints |
|----------|---------|-------------|---------|-------------|
| /epci-brief | ✅ | ✅ | ✅ | N/A |
| /epci | ✅ | ✅ | ✅ | ✅ Phase 1 & 2 |
| /epci-quick | ✅ | ✅ | ✅ | N/A (correct) |
| /epci-spike | ✅ | ✅ | ✅ | N/A |
| /epci:create | ✅ | ✅ | ✅ | N/A |

### Agents (5/5)

| Agent | Frontmatter | Mission | Checklist | Format Output | Sévérités |
|-------|-------------|---------|-----------|---------------|-----------|
| @plan-validator | ✅ | ✅ | ✅ | ✅ | ✅ |
| @code-reviewer | ✅ | ✅ | ✅ | ✅ | ✅ |
| @security-auditor | ✅ | ✅ | ✅ OWASP | ✅ | ✅ CVSS |
| @qa-reviewer | ✅ | ✅ | ✅ | ✅ Pyramide | ✅ |
| @doc-generator | ✅ | ✅ | ✅ | ✅ Templates | N/A |

### Skills (13/13)

#### Core (5/5)
| Skill | SKILL.md | Description formule | Contenu |
|-------|----------|---------------------|---------|
| epci-core | ✅ | ✅ Use when + Not for | ✅ Complet |
| architecture-patterns | ✅ | ✅ | ✅ SOLID, Clean Arch |
| code-conventions | ✅ | ✅ | ✅ Nommage, structure |
| testing-strategy | ✅ | ✅ | ✅ TDD, pyramide |
| git-workflow | ✅ | ✅ | ✅ Conventional Commits |

#### Stack (4/4)
| Skill | SKILL.md | Auto-détection | Patterns | Tests |
|-------|----------|----------------|----------|-------|
| php-symfony | ✅ | ✅ composer.json | ✅ Doctrine | ✅ PHPUnit |
| javascript-react | ✅ | ✅ package.json | ✅ Hooks | ✅ Jest/RTL |
| python-django | ✅ | ✅ requirements.txt | ✅ DRF | ✅ pytest |
| java-springboot | ✅ | ✅ pom.xml | ✅ Spring | ✅ JUnit |

#### Factory (4/4)
| Skill | SKILL.md | Workflow 6 phases | Template intégré |
|-------|----------|-------------------|------------------|
| skills-creator | ✅ | ✅ | ✅ (dans SKILL.md) |
| commands-creator | ✅ | ✅ | ✅ (dans SKILL.md) |
| subagents-creator | ✅ | ✅ | ✅ (dans SKILL.md) |
| component-advisor | ✅ | N/A (passif) | N/A |

### Scripts Python (5/5)

| Script | Existe | Fonctionnel | Dataclass | Exit codes |
|--------|--------|-------------|-----------|------------|
| validate_skill.py | ✅ | ✅ | ✅ ValidationReport | ✅ 0/1 |
| validate_command.py | ✅ | ✅ | ✅ ValidationReport | ✅ 0/1 |
| validate_subagent.py | ✅ | ✅ | ✅ ValidationReport | ✅ 0/1 |
| test_triggering.py | ✅ | ✅ | ✅ | ✅ 0/1 |
| validate_all.py | ✅ | ⚠️ Path src/ | ✅ ValidationSummary | ✅ 0/1 |

---

## 📋 TABLEAU RÉCAPITULATIF DES ACTIONS

### Actions CRITIQUES (🔴)

| # | Action | Effort | Fichiers impactés |
|---|--------|--------|-------------------|
| 1 | **Traduire tous les .md en anglais** | Élevé | ~25 fichiers |
| 2 | **Créer fichiers references/ dans factory** | Moyen | ~12 fichiers |
| 3 | **Créer fichiers templates/ dans factory** | Moyen | ~6 fichiers |

### Actions IMPORTANTES (🟠)

| # | Action | Effort | Fichiers impactés |
|---|--------|--------|-------------------|
| 4 | Enrichir plugin.json avec skills | Faible | 1 fichier |
| 5 | Corriger path dans validate_all.py | Faible | 1 fichier |
| 6 | Ajouter keywords dans plugin.json | Faible | 1 fichier |

### Actions MINEURES (🟡)

| # | Action | Effort | Fichiers impactés |
|---|--------|--------|-------------------|
| 7 | Supprimer ou documenter hooks/ | Trivial | 1 dossier |
| 8 | Ajouter champ activation aux agents | Faible | 2 fichiers |
| 9 | Uniformiser format tableaux Subagents & Skills | Faible | 4 fichiers |

---

## 📊 MÉTRIQUES DE CONFORMITÉ

| Catégorie | Conforme | Partiel | Manquant | % Conformité |
|-----------|----------|---------|----------|--------------|
| Structure | 8 | 1 | 0 | 94% |
| Commandes | 5 | 0 | 0 | 100% |
| Agents | 5 | 0 | 0 | 100% |
| Skills Core | 5 | 0 | 0 | 100% |
| Skills Stack | 4 | 0 | 0 | 100% |
| Skills Factory | 0 | 4 | 0 | 50% |
| Factory References | 0 | 0 | 12 | 0% |
| Factory Templates | 0 | 0 | 6 | 0% |
| Scripts | 4 | 1 | 0 | 90% |
| **Langue** | 0 | 4 | 21 | **16%** |

### Score global : **~65%** de conformité

Le problème majeur est la **langue** (tout en français au lieu d'anglais).

---

## 🎯 PLAN D'ACTION RECOMMANDÉ

### Phase 1 : Corrections critiques (Priorité HAUTE)

```
1. Traduire TOUS les fichiers en anglais
   - commands/*.md (5 fichiers)
   - agents/*.md (5 fichiers)
   - skills/**/*.md (13 fichiers)
   
2. Créer les fichiers references/ manquants
   - skills-creator/references/ (4 fichiers)
   - commands-creator/references/ (4 fichiers)
   - subagents-creator/references/ (4 fichiers)

3. Créer les fichiers templates/ manquants
   - skills-creator/templates/ (2 fichiers)
   - commands-creator/templates/ (2 fichiers)
   - subagents-creator/templates/ (1 fichier)
```

### Phase 2 : Améliorations importantes (Priorité MOYENNE)

```
4. Enrichir plugin.json
   - Ajouter section skills[]
   - Ajouter keywords[]
   - Enrichir commands[] et agents[] avec descriptions

5. Corriger validate_all.py
   - Modifier src_path pour pointer vers la racine
```

### Phase 3 : Polissage (Priorité BASSE)

```
6. Uniformiser le format des commandes
   - Ajouter tableaux "Subagents & Skills" explicites

7. Nettoyer
   - Supprimer hooks/ ou ajouter README
   - Ajouter champ activation aux agents conditionnels
```

---

## 📝 NOTES POUR CLAUDE CODE

Pour implémenter ces corrections, exécuter dans cet ordre :

```bash
# 1. Lister tous les fichiers à traduire
find . -name "*.md" -type f | grep -v node_modules

# 2. Pour chaque fichier, traduire le contenu FR → EN
# Conserver la structure, traduire le texte

# 3. Créer les fichiers references/ et templates/ manquants
# Utiliser le contenu du cahier des charges comme base

# 4. Mettre à jour plugin.json

# 5. Corriger validate_all.py

# 6. Exécuter la validation
python scripts/validate_all.py --verbose
```

---

## ANNEXE : Liste complète des fichiers à modifier

### Fichiers à TRADUIRE (25)

```
commands/epci-brief.md
commands/epci.md
commands/epci-quick.md
commands/epci-spike.md
commands/create.md
agents/plan-validator.md
agents/code-reviewer.md
agents/security-auditor.md
agents/qa-reviewer.md
agents/doc-generator.md
skills/core/epci-core/SKILL.md
skills/core/architecture-patterns/SKILL.md
skills/core/code-conventions/SKILL.md
skills/core/testing-strategy/SKILL.md
skills/core/git-workflow/SKILL.md
skills/stack/php-symfony/SKILL.md
skills/stack/javascript-react/SKILL.md
skills/stack/python-django/SKILL.md
skills/stack/java-springboot/SKILL.md
skills/factory/skills-creator/SKILL.md
skills/factory/commands-creator/SKILL.md
skills/factory/subagents-creator/SKILL.md
skills/factory/component-advisor/SKILL.md
```

### Fichiers à CRÉER (18)

```
skills/factory/skills-creator/references/best-practices.md
skills/factory/skills-creator/references/description-formulas.md
skills/factory/skills-creator/references/yaml-rules.md
skills/factory/skills-creator/references/checklist.md
skills/factory/skills-creator/templates/skill-simple.md
skills/factory/skills-creator/templates/skill-advanced.md
skills/factory/commands-creator/references/best-practices.md
skills/factory/commands-creator/references/frontmatter-guide.md
skills/factory/commands-creator/references/argument-patterns.md
skills/factory/commands-creator/references/checklist.md
skills/factory/commands-creator/templates/command-simple.md
skills/factory/commands-creator/templates/command-advanced.md
skills/factory/subagents-creator/references/best-practices.md
skills/factory/subagents-creator/references/delegation-patterns.md
skills/factory/subagents-creator/references/tools-restriction.md
skills/factory/subagents-creator/references/checklist.md
skills/factory/subagents-creator/templates/subagent-template.md
```

### Fichiers à MODIFIER (2)

```
.claude-plugin/plugin.json
scripts/validate_all.py
```
