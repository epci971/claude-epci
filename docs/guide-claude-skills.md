# Guide Claude Skills — Version Optimisée Claude Code

> **Version** : 4.1-lite  
> **Optimisé pour** : Claude Code (fenêtre de contexte réduite)  
> **Source** : Guide v4.0 (67 Ko → ~25 Ko)

---

## TL;DR — 10 Règles d'Or

1. **Un Skill = Une capacité focalisée** — Pas de couteau suisse
2. **SKILL.md < 5000 tokens** — Détails dans `references/`
3. **Description = Capacités + "Use when..." + "Not for..."** — Critique pour le triggering
4. **Nom en kebab-case** — Max 64 caractères, jamais d'espaces
5. **Liens explicites** — Claude ne charge que ce qui est référencé
6. **Progressive Disclosure** — Informations chargées à la demande
7. **Pas de secrets en dur** — Variables d'environnement uniquement
8. **Tester le triggering** — Explicite, implicite, et hors périmètre
9. **Versionner** — Semantic versioning + changelog dans SKILL.md
10. **Auditer les sources** — Ne jamais installer un Skill non vérifié

---

## 1. Glossaire Essentiel

| Terme | Définition |
|-------|------------|
| **Skill** | Package modulaire chargé dynamiquement via matching sémantique |
| **Project** | Contexte persistant (documents, enjeux métier, instructions haut niveau) |
| **MCP** | Model Context Protocol — connexion systèmes externes (BDD, APIs) |
| **Triggering** | Sélection automatique du Skill basée sur correspondance sémantique |
| **Context Window** | Quantité max de tokens traitables simultanément (~200K Claude 3.5) |
| **Frontmatter** | Bloc YAML en début de SKILL.md (name, description, allowed-tools) |
| **Progressive Disclosure** | Chargement progressif : métadonnées → instructions → références |

---

## 2. Quand Créer un Skill ?

### Critères de Décision

| Critère | Seuil |
|---------|-------|
| Récurrence | ≥5 fois passées OU ≥10 fois futures |
| Complexité | ≥3 règles métier non triviales |
| Standardisation | ≥2 personnes concernées |
| Stabilité | Procédures stables depuis ≥1 mois |
| ROI | Gain de temps ≥30% vs prompt direct |

### Quand NE PAS Créer

- Tâche ponctuelle → Prompt direct
- Simple instruction suffisante → Instructions Project
- Procédures volatiles → Prompt adaptatif
- Duplication capacité native Claude → Utiliser le natif

### Principe Fondamental : Un Skill = Une Capacité

| ❌ Anti-pattern | ✅ Meilleure approche |
|-----------------|----------------------|
| `document-helper` (PDF + synthèses + contrats) | `pdf-extractor` + `contract-analyzer` |
| `data-tools` (SQL + Excel + reporting) | `sql-analytics` + `excel-kpi-analyst` |
| `dev-helper` (debug + review + refactor) | `python-debugger` + `security-auditor` |

---

## 3. Contraintes Techniques

### Limites Impératives

| Contrainte | Valeur | Impact |
|------------|--------|--------|
| Champ `name` | Max 64 chars | kebab-case, pas d'espaces |
| Champ `description` | Max 1024 chars | Chaque mot compte |
| SKILL.md | < 5000 tokens (~15-20 Ko) | Au-delà : latence et coûts |
| Profondeur arborescence | 2 niveaux max | Au-delà : navigation complexe |
| `allowed-tools` | Claude Code uniquement | Non supporté API/claude.ai |

### Estimation Tokens

| Type | Approximation |
|------|---------------|
| Anglais | 1 token ≈ 4 chars ≈ 0.75 mot |
| Français | 1 token ≈ 3.5 chars ≈ 0.6 mot |
| Code | 1 token ≈ 3 chars |

### Différences Plateformes

| Feature | claude.ai | Claude Code | API |
|---------|-----------|-------------|-----|
| Skills custom | Oui (Settings) | Oui (fichiers) | Oui |
| `allowed-tools` | Non | Oui | Non |
| Accès fichiers | Non | Oui | Variable |
| MCP | Oui | Oui | Oui |

### Limitations Conception

| Limitation | Contournement |
|------------|---------------|
| Pas de mémoire entre sessions | Stocker via MCP/fichiers |
| Pas d'accès réseau arbitraire | Utiliser MCP |
| Context window limité | Progressive disclosure |
| Pas de persistance variables | Recalculer ou stocker externe |

---

## 4. Structure et Architecture

### Hiérarchie Standard

```
my-skill/
├── SKILL.md                    # OBLIGATOIRE (<5000 tokens)
├── references/                 # Documentation détaillée (à la demande)
│   ├── schemas.md
│   ├── api-reference.md
│   ├── edge-cases.md
│   └── examples.md
├── scripts/                    # Scripts exécutables (optionnel)
│   └── validator.py
└── templates/                  # Templates sortie (optionnel)
    └── output-template.json
```

### Emplacements

| Type | Chemin | Scope |
|------|--------|-------|
| Personnel | `~/.claude/skills/skill-name/` | Tous vos projets |
| Projet | `.claude/skills/skill-name/` | Projet courant (partagé via Git) |
| Organisation | Dépôt Git dédié | Multi-projets |

### Conventions Nommage

| Élément | Convention | Exemple |
|---------|------------|---------|
| Dossier Skill | kebab-case | `sql-analytics/` |
| SKILL.md | Majuscules exactes | `SKILL.md` |
| Références | kebab-case | `edge-cases.md` |
| Scripts | snake_case ou kebab-case | `validate_query.py` |

### Pièges à Éviter

- Tout dans SKILL.md → Découper en références
- Fichiers sans lien → Liens explicites `[](path)`
- Arborescence >2 niveaux → Aplatir
- Noms avec espaces → Tirets ou underscores
- Duplication entre fichiers → Information à UN seul endroit

---

## 5. Syntaxe SKILL.md

### Structure Recommandée

```yaml
---
name: nom-du-skill
description: >-
  [CAPACITÉS] + [Use when contexte1, contexte2] + 
  [Not for exclusion1, exclusion2].
allowed-tools: Read, Grep, Glob    # Claude Code uniquement
---

# Titre du Skill

## Overview
Présentation concise (2-3 phrases).

## Quick Start
Exemple rapide ou decision tree.

## Workflow
1. Étape 1 : [action]
2. Étape 2 : [action]
3. Étape 3 : [action]

## Critical Rules
- Règle impérative 1
- Règle impérative 2

## Knowledge Base
- [Schémas](references/schemas.md)
- [Exemples](references/examples.md)

## Limitations
- Ce que le Skill ne fait PAS

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-01 | Initial release |

## Current: v1.0.0
```

### Validation YAML

```bash
python3 -c "
import yaml
content = open('SKILL.md').read()
parts = content.split('---')
if len(parts) >= 3:
    fm = yaml.safe_load(parts[1])
    print('✅ YAML valide:', fm.get('name'))
else:
    print('❌ Frontmatter mal formé')
"
```

### Erreurs YAML Fréquentes

| Erreur | Solution |
|--------|----------|
| TAB au lieu d'espaces | Remplacer par espaces |
| Caractères spéciaux (`:`, `"`) | Encadrer avec guillemets |
| Frontmatter non fermé | Ajouter `---` de fermeture |
| Indentation incohérente | Aligner correctement |

---

## 6. Description et Triggering

### Mécanisme de Sélection

Claude effectue un **matching sémantique** (pas de mots-clés stricts) entre la requête utilisateur et les descriptions de tous les Skills disponibles. Une description vague = triggering imprévisible.

### Formule Efficace

```
[CAPACITÉS 30%] + [USE CASES 30%] + [TRIGGERS 20%] + [BOUNDARIES 20%]
```

### Anatomie Description Optimale

```yaml
description: >-
  Extract text and tables from PDF files, fill interactive forms, 
  merge and split documents. Provides structured output with 
  preserved formatting. Use when working with PDF documents, 
  when user mentions forms, extraction, document merging, or 
  needs to process multiple PDFs. Not for image-only PDFs 
  (scanned documents), video files, or simple PDF viewing.
```

### Comparaison Descriptions

| ❌ Faible | ✅ Forte |
|----------|---------|
| `Helps with documents` | `Extract text/tables from PDFs, fill forms, merge docs. Use when working with PDFs. Not for scanned images.` |
| `For data analysis` | `Analyze Excel, create pivot tables, calculate KPIs. Use when .xlsx files. Not for CSV or DB queries.` |
| `Code helper` | `Review Python for security (OWASP). Use when auditing. Not for refactoring.` |

### Anti-patterns

| Anti-pattern | Conséquence |
|--------------|-------------|
| Description vague | Triggering aléatoire |
| Keywords trop génériques | Conflits avec autres Skills |
| Pas de "Use when..." | Faux négatifs |
| Pas de "Not for..." | Faux positifs |
| Chevauchement autre Skill | Comportement imprévisible |

---

## 7. Gestion Context Window

### Progressive Disclosure

| Niveau | Contenu | Tokens | Chargement |
|--------|---------|--------|------------|
| 1 | Frontmatter | ~100 | Toujours (scan) |
| 2 | Corps SKILL.md | < 5000 | Au triggering |
| 3 | Références | Variable | À la demande |

### Limites Recommandées

| Élément | Limite |
|---------|--------|
| SKILL.md | < 5000 tokens |
| Fichier référence | < 3000 tokens |
| Total Skill | < 20000 tokens |
| Description | < 1024 caractères |

### Hiérarchie Information

1. **Overview** (2-3 phrases) — Qu'est-ce que ça fait ?
2. **Quick Start** — Comment commencer ?
3. **Workflow** (étapes numérotées) — Processus standard ?
4. **Règles critiques** — Ne jamais ignorer ?
5. **Liens références** — Plus d'info ?
6. **Limitations** — Ce que ça ne fait PAS ?

### Référencement Efficace

```markdown
## Validation
Pour les règles complètes, voir [filtres-obligatoires.md](references/filtres-obligatoires.md).

## Schémas
Consultez [schemas.md](references/schemas.md) pour les tables et relations.
```

---

## 8. Scripts et Fichiers Externes

### Types Supportés

| Type | Extensions | Usage |
|------|------------|-------|
| Documentation | `.md` | Schémas, guides |
| Scripts | `.py`, `.sh`, `.js` | Validation, calculs |
| Templates | `.json`, `.yaml` | Structures sortie |
| Données | `.csv`, `.json` | Référentiels |

### Règle : Déterminisme vs Raisonnement

| Besoin | Solution |
|--------|----------|
| Calculs précis, formatage strict, validation règles fixes | **Script externe** |
| Analyse sémantique, synthèse, décisions contextuelles | **Instructions LLM** |

### Documentation Dépendances

```markdown
## Dependencies
```bash
pip install pandas sqlalchemy pyyaml
```

### Environment variables
```bash
export ACME_DB_HOST="your-host"
export ACME_DB_USER="your-user"
```
```

### Pièges Scripts

| Piège | Solution |
|-------|----------|
| Scripts sans permissions | `chmod +x` ou appeler via interpréteur |
| Chemins Windows (`\`) | Toujours utiliser `/` |
| Dépendances non documentées | Section Dependencies explicite |
| Hardcoded paths | Chemins relatifs ou env vars |

---

## 9. Sécurité

### Principes Fondamentaux

| Principe | Application |
|----------|-------------|
| Sources fiables | Skills internes ou repos validés uniquement |
| Review avant install | Lire SKILL.md ET scripts avant activation |
| Moindre privilège | `allowed-tools` au minimum nécessaire |
| Pas de secrets en dur | Variables d'environnement |
| Audit scripts | Vérifier tout code avant exécution |

### Restriction Outils (Claude Code)

```yaml
allowed-tools: Read, Grep, Glob  # Read-only
```

| Outil | Risque |
|-------|--------|
| `Bash` | Peut modifier/supprimer fichiers |
| `Read`, `Grep`, `Glob`, `LS` | Faible (lecture seule) |
| `Write` | Peut créer fichiers |
| `Edit` | Peut corrompre fichiers |

### Configurations Recommandées

| Type Skill | Outils |
|------------|--------|
| Analyse/Audit (read-only) | `Read, Grep, Glob, LS` |
| Génération code | `Read, Write, Grep, Glob` |
| Refactoring | `Read, Edit, Grep, Glob` |

### Pattern Credentials Sécurisé

```markdown
## Configuration
Set environment variables (~/.bashrc):
```bash
export ACME_DB_HOST="host"
export ACME_DB_USER="user"
export ACME_DB_PASSWORD="pass"  # Consider secrets manager
```

Verification (sans afficher valeurs):
```bash
echo "DB_HOST is ${ACME_DB_HOST:+set}"
```
```

---

## 10. Tests et Debugging

### Matrice Tests Obligatoire

| Type | Objectif | Exemple |
|------|----------|---------|
| Triggering explicite | S'active sur demande directe | "Use sql-analytics to..." |
| Triggering implicite | S'active en langage naturel | "What was our ARR?" |
| Out-of-scope | NE s'active PAS hors périmètre | "Write VBA macro" → NON |
| Edge cases | Comportement sur entrées inhabituelles | Données manquantes |
| Workflow complet | Exécution bout en bout | Requête → Résultat validé |

### Procédure Test

```markdown
## Tests [nom-skill]

### Triggering explicite (doit activer)
- [ ] "Use [skill] to [action]"

### Triggering implicite (doit activer)
- [ ] "[Phrase naturelle 1]"
- [ ] "[Phrase naturelle 2]"

### Out-of-scope (NE doit PAS activer)
- [ ] "[Requête hors périmètre]"

### Fonctionnel
- [ ] Cas nominal : Input → Expected output
- [ ] Edge case : Données manquantes → Comportement attendu
```

### Debugging

```bash
# Valider YAML
head -n 15 SKILL.md

# Mode debug Claude Code
claude --debug

# Forcer déclenchement
"Utilise le skill [nom] pour [action]"

# Vérifier chargement
"Quels fichiers as-tu chargés pour ce skill ?"
```

---

## 11. Erreurs Fréquentes

### Triggering

| Symptôme | Cause | Solution |
|----------|-------|----------|
| Skill jamais activé | Description vague | Ajouter "Use when..." |
| Mauvais Skill activé | Descriptions se chevauchent | Ajouter "Not for..." |
| Activation intempestive | Keywords trop génériques | Affiner boundaries |

### Syntaxe

| Symptôme | Cause | Solution |
|----------|-------|----------|
| YAML parse error | Tabs/chars spéciaux | Espaces, guillemets |
| Frontmatter ignoré | `---` manquants | Ajouter délimiteurs |
| Description tronquée | >1024 chars | Condenser |

### Exécution

| Symptôme | Cause | Solution |
|----------|-------|----------|
| Références non chargées | Liens cassés | Ajouter `[](path)` |
| Scripts échouent | Dépendances manquantes | Documenter dependencies |
| Permission denied | Scripts non exécutables | `chmod +x` ou interpréteur |

### Conception

| Symptôme | Cause | Solution |
|----------|-------|----------|
| Skill lent | SKILL.md volumineux | Découper en références |
| Comportement imprévisible | Scope trop large | Diviser en Skills spécialisés |
| Conflits entre Skills | Périmètres flous | Clarifier "Not for..." |

---

## 12. Maintenance et Versioning

### Semantic Versioning

| Version | Usage |
|---------|-------|
| MAJOR (X.0.0) | Breaking changes |
| MINOR (0.X.0) | Nouvelles fonctionnalités (rétrocompatibles) |
| PATCH (0.0.X) | Corrections bugs |

### Section Version History

```markdown
## Version History
| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-11-20 | **BREAKING**: Nouvelle méthode calcul ARR |
| 1.1.0 | 2025-10-10 | Ajout schémas pipeline |
| 1.0.0 | 2025-09-01 | Initial release |

## Current: v2.0.0
```

### Workflow Mise à Jour

```bash
git checkout -b feat/skill-update
# Éditer, tester, mettre à jour version + changelog
git commit -m "feat(my-skill): add validation v1.2.0"
git push && PR
```

### Ce Qu'il Ne Faut JAMAIS Changer

| Élément | Raison |
|---------|--------|
| `name` une fois déployé | Perte historique usage |
| Triggers principaux | Confusion utilisateurs |
| Comportement de base | Breaking change silencieux |

Si changement nécessaire : créer nouveau Skill, déprécier ancien, période transition, supprimer après migration.

---

## 13. Migration Prompt → Skill

### Critères Migration

| Critère | Seuil |
|---------|-------|
| Fréquence | ≥5 fois/semaine |
| Utilisateurs | ≥2 personnes |
| Stabilité | Inchangé depuis ≥2 semaines |
| Complexité | ≥50 lignes ou ≥3 étapes |

### Workflow 5 Étapes

1. **Identifier** : Analyser inputs/outputs/comportements
2. **Extraire** : Identifier invariants (règles, style)
3. **Simplifier** : Réduire verbiage, garder opérationnel
4. **Encapsuler** : Créer frontmatter + corps structuré
5. **Déporter** : Déplacer exemples dans `references/`

### Checklist Migration

- [ ] Prompt analysé et comportements identifiés
- [ ] Instructions condensées
- [ ] Frontmatter YAML créé
- [ ] Workflow structuré en étapes
- [ ] Exemples déportés dans references/
- [ ] Tests triggering validés

---

## 14. Checklist Finale

### Structure
- [ ] Dossier `skill-name/` avec `SKILL.md` à la racine
- [ ] Nom kebab-case, sans espaces ni majuscules
- [ ] Arborescence ≤2 niveaux
- [ ] Tous fichiers référencés existent
- [ ] Chemins Unix (`/`)

### Frontmatter
- [ ] `name` : ≤64 chars, kebab-case
- [ ] `description` : ≤1024 chars
- [ ] YAML valide (espaces, pas tabs)
- [ ] Frontmatter fermé avec `---`
- [ ] `allowed-tools` configuré si restriction

### Description
- [ ] Verbes d'action (extract, analyze, create...)
- [ ] Types fichiers/données concernés
- [ ] "Use when..." avec ≥2 contextes
- [ ] "Not for..." avec ≥2 exclusions
- [ ] Pas de chevauchement autre Skill

### Instructions
- [ ] Overview 2-3 phrases
- [ ] Workflow étapes numérotées
- [ ] ≥1 exemple concret
- [ ] Règles critiques documentées
- [ ] Limitations listées

### Context Window
- [ ] SKILL.md < 5000 tokens
- [ ] Détails dans references/ avec liens
- [ ] Pas de duplication SKILL.md ↔ références

### Scripts
- [ ] Permissions ou appel via interpréteur
- [ ] Chemins Unix
- [ ] Dependencies documentées
- [ ] Gestion erreurs présente

### Sécurité
- [ ] Aucun credential en dur
- [ ] `allowed-tools` au minimum
- [ ] Scripts audités
- [ ] Source vérifiée

### Tests
- [ ] Triggering explicite ✓
- [ ] Triggering implicite ✓
- [ ] Pas de faux positifs ✓
- [ ] Workflow complet testé
- [ ] ≥3 formulations différentes

### Versioning
- [ ] Version documentée
- [ ] Version History à jour
- [ ] Owner identifié

---

## Ressources

| Ressource | URL |
|-----------|-----|
| Documentation Claude | `https://docs.anthropic.com/` |
| GitHub Anthropic | `https://github.com/anthropics` |

---

## Version History (ce guide)

| Version | Date | Changes |
|---------|------|---------|
| 4.1-lite | 2025-12-11 | Version optimisée Claude Code (~60% réduction) |
| 4.0.0 | 2025-12-11 | Version complète originale |

## Current: v4.1-lite

**Author** : Édouard | **Optimisation** : Claude | **Décembre 2025**
