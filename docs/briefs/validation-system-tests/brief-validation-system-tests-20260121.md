# PRD — Systeme de Tests Unitaires Complet pour Plugin EPCI

| Metadata | Value |
|----------|-------|
| **Document ID** | PRD-2026-001 |
| **Version** | 1.0 |
| **Status** | Draft |
| **Owner** | EPCI Team |
| **Created** | 2026-01-21 |
| **Last Updated** | 2026-01-21 |
| **Slug** | validation-system-tests |
| **EMS Score** | 82/100 |
| **Template** | feature |

### Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-21 | EPCI Brainstormer | Initial generation from /brainstorm |

---

## Executive Summary

**TL;DR** : Mettre en place un systeme de 31 validations unitaires pour garantir l'integrite du plugin EPCI a chaque modification dans `src/`.

| Aspect | Description |
|--------|-------------|
| **Problem** | Les modifications dans src/ peuvent introduire des incoherences non detectees (liens casses, fichiers orphelins, desynchronisation plugin.json) |
| **Solution** | Enrichir validate_all.py avec 16 nouvelles validations + hook pre-commit bloquant |
| **Impact** | Zero regression sur l'integrite du plugin, detection immediate des erreurs |
| **Target Launch** | v5.7.0 |

---

## Background & Strategic Fit

### Why Now?

Le plugin EPCI a atteint une complexite significative :
- 14 commandes, 16 agents, 34 skills
- References croisees multiples entre composants
- 3 fichiers de version a synchroniser (CLAUDE.md, src/plugin.json, build/plugin.json)
- Breakpoints avec syntaxe specifique `@skill:xxx`

Les validations actuelles (validate_skill.py, validate_command.py, etc.) couvrent les aspects individuels mais pas l'integrite globale.

### Strategic Alignment

Cette feature s'aligne avec :
- [x] **Qualite** : Garantir la stabilite du plugin avant chaque commit
- [x] **DX** : Feedback immediat aux developpeurs sur les erreurs
- [x] **Maintenance** : Reduire le temps de debug des incoherences

---

## Problem Statement

### Current Situation

Les validations actuelles dans `src/scripts/` :
- `validate_skill.py` : 6 checks (YAML, name, desc, tokens, refs, structure)
- `validate_command.py` : 5 checks (file, YAML, desc, tools, content)
- `validate_subagent.py` : 5 checks (similaire)
- `validate_all.py` : Orchestre les validateurs individuels

**Gaps critiques** :
1. Pas de validation de synchronisation plugin.json
2. Pas de detection des references croisees cassees
3. Pas de validation de la syntaxe breakpoints
4. Pas de detection des fichiers orphelins
5. Pas de detection de secrets dans le code

### Problem Definition

Un developpeur peut :
- Ajouter un skill sans le declarer dans plugin.json
- Referencer un agent inexistant dans une commande
- Utiliser un mauvais format pour `@skill:breakpoint-display`
- Committer avec des versions desynchronisees
- Introduire accidentellement une cle API dans le code

Ces erreurs ne sont detectees qu'a l'execution, creant de la friction.

### Evidence & Data

- **Quantitative** : 17 scripts de validation existants, mais 0 pour cross-refs
- **Qualitative** : Documentation mentionne explicitement la regle de sync des 3 fichiers version

### Impact of Not Solving

- **Dev Experience** : Debugging long pour trouver la source d'erreurs
- **Qualite** : Regressions potentielles en production
- **Maintenance** : Dette technique accumulee

---

## Goals

### Business Goals

- [ ] Zero regression d'integrite sur le plugin apres v5.7.0

### User Goals (Developpeur)

- [ ] Feedback immediat sur erreurs d'integrite avant commit
- [ ] Auto-correction des problemes simples avec `--fix`

### Technical Goals

- [ ] 31 validations couvrant tous les aspects d'integrite
- [ ] Hook pre-commit bloquant avec exit code 1 sur erreur
- [ ] Temps d'execution < 10s pour validation complete

---

## Non-Goals (Out of Scope v1)

| Exclusion | Raison | Future Version |
|-----------|--------|----------------|
| Tests d'integration multi-composants | Complexite | v2 |
| Validation semantique du contenu | Necessite IA | Non prevu |
| CI/CD integration (GitHub Actions) | Hors scope local | v2 |
| Hot-reload des validations | Over-engineering | Non prevu |

---

## Personas

### Persona Primaire — Developpeur Plugin EPCI

- **Role**: Developpeur maintenant le plugin EPCI
- **Contexte**: Travaille sur src/, modifie skills/commands/agents regulierement
- **Pain points**: Doit verifier manuellement la coherence, risque d'oublis
- **Objectifs**: Committer en confiance, sans regressions
- **Quote**: "Je veux savoir immediatement si j'ai casse quelque chose"

---

## Stack Detecte

- **Language**: Python 3
- **Framework**: Scripts standalone avec dataclasses
- **Patterns**: ValidationReport, fonctions de validation individuelles
- **Outils**: yaml, re, pathlib, subprocess

---

## Exploration Summary

### Codebase Analysis

- **Structure**: Monorepo avec src/ contenant commands/, skills/, agents/
- **Architecture**: Scripts de validation avec pattern commun (ValidationReport)
- **Test patterns**: pytest pour tests existants

### Fichiers Impactes

| Fichier | Action | Notes |
|---------|--------|-------|
| `src/scripts/validate_all.py` | Modify | Ajouter 16 nouvelles fonctions de validation |
| `.git/hooks/pre-commit` | Create | Script shell appelant validate_all.py |

### Risques Identifies

- **Medium** : Performance si trop de validations sequentielles
- **Low** : Faux positifs sur certaines validations

---

## User Stories

### US1 — Validation plugin.json sync bidirectionnelle

**En tant que** developpeur plugin,
**Je veux** que validate_all.py verifie la synchronisation plugin.json,
**Afin de** detecter les composants non declares ou fichiers manquants.

**Acceptance Criteria:**
- [ ] Given plugin.json liste skill X, When skill X n'existe pas dans src/skills/, Then erreur "Missing file: skill X"
- [ ] Given skill Y existe dans src/skills/, When skill Y absent de plugin.json, Then erreur "Undeclared in plugin.json: skill Y"
- [ ] Given `--fix` flag, When composant manquant dans plugin.json, Then ajouter automatiquement

**Priorite**: Must-have
**Complexite**: M

### US2 — Validation version sync 3 fichiers

**En tant que** developpeur plugin,
**Je veux** verifier que les 3 fichiers de version sont synchronises,
**Afin de** eviter les incoherences de versioning.

**Acceptance Criteria:**
- [ ] Given CLAUDE.md version 5.6.3, When plugin.json version 5.6.2, Then erreur "Version mismatch"
- [ ] Given `--fix` flag, When versions differentes, Then aligner sur la plus recente

**Priorite**: Must-have
**Complexite**: S

### US3 — Validation cross-references skills<->commands

**En tant que** developpeur plugin,
**Je veux** verifier que les references `@skill:xxx` dans commands pointent vers des skills existants,
**Afin de** eviter les erreurs d'execution.

**Acceptance Criteria:**
- [ ] Given command brief.md contient @skill:breakpoint-display, When skill breakpoint-display existe, Then OK
- [ ] Given command epci.md contient @skill:inexistant, When skill inexistant n'existe pas, Then erreur "Unknown skill reference"

**Priorite**: Must-have
**Complexite**: M

### US4 — Validation syntaxe breakpoints

**En tant que** developpeur plugin,
**Je veux** verifier que les invocations `@skill:breakpoint-display` suivent le format YAML correct,
**Afin de** garantir le bon fonctionnement des breakpoints.

**Acceptance Criteria:**
- [ ] Given @skill:breakpoint-display avec type: analysis, When format YAML valide, Then OK
- [ ] Given @skill:breakpoint-display sans type:, When champ obligatoire manquant, Then warning "Missing type field"

**Priorite**: Must-have
**Complexite**: M

### US5 — Detection secrets dans code

**En tant que** developpeur plugin,
**Je veux** detecter les patterns de secrets (API keys, tokens) dans les fichiers,
**Afin de** eviter les fuites accidentelles.

**Acceptance Criteria:**
- [ ] Given fichier contenant sk-12345abcdef, When pattern API key detecte, Then erreur "Potential secret detected"
- [ ] Given fichier contenant password=xxx, When pattern password detecte, Then erreur

**Priorite**: Must-have
**Complexite**: S

### US6 — Detection fichiers orphelins

**En tant que** developpeur plugin,
**Je veux** detecter les fichiers dans src/ non references par plugin.json,
**Afin de** maintenir un codebase propre.

**Acceptance Criteria:**
- [ ] Given skill orphan/ existe mais non liste dans plugin.json, When validation, Then warning "Orphan file"

**Priorite**: Should-have
**Complexite**: S

### US7 — Hook pre-commit bloquant

**En tant que** developpeur plugin,
**Je veux** un hook pre-commit qui bloque le commit si validations echouent,
**Afin de** garantir la qualite avant chaque commit.

**Acceptance Criteria:**
- [ ] Given erreur de validation, When git commit, Then commit refuse avec message d'erreur
- [ ] Given toutes validations OK, When git commit, Then commit accepte

**Priorite**: Must-have
**Complexite**: S

### US8 — Auto-fix frontmatter manquant

**En tant que** developpeur plugin,
**Je veux** que `--fix` genere un frontmatter par defaut si manquant,
**Afin de** corriger rapidement les oublis.

**Acceptance Criteria:**
- [ ] Given skill sans frontmatter YAML, When `--fix`, Then generer frontmatter minimal

**Priorite**: Should-have
**Complexite**: S

---

## Regles Metier

- **RM1**: Un composant (skill/command/agent) DOIT etre declare dans plugin.json pour etre valide
- **RM2**: Les 3 fichiers de version DOIVENT avoir la meme valeur
- **RM3**: Toute reference `@skill:xxx` DOIT pointer vers un skill existant
- **RM4**: Le token count DOIT etre < 5000 pour skills/commands, < 2000 pour agents
- **RM5**: Aucun pattern de secret ne DOIT etre present dans les fichiers

---

## Cas Limites & Edge Cases

| Cas | Comportement attendu |
|-----|---------------------|
| Fichier .md vide | Warning "Empty file" |
| Frontmatter YAML invalide | Erreur bloquante |
| Skill avec references/ vide | OK (dossier optionnel) |
| Plusieurs versions dans un fichier | Utiliser la premiere occurrence |
| Hook pre-commit deja existant | Append ou merger |

---

## Success Metrics

| Metrique | Baseline | Cible | Methode |
|----------|----------|-------|---------|
| Validations couvertes | 17 | 31 | Count dans validate_all.py |
| Temps execution | ~5s | <10s | Benchmark |
| Faux positifs | N/A | <5% | Feedback developpeur |

---

## User Flow

### Current Experience (As-Is)

```
Modification src/
       |
       v
  git add + commit --> Pas de validation
                            |
                            v
                       Push --> Erreur runtime decouverte tard
```

### Proposed Experience (To-Be)

```
Modification src/
       |
       v
  git add
       |
       v
  git commit --> Hook pre-commit
                      |
              [Validations OK?]
                  |         |
               [Oui]     [Non]
                  |         |
                  v         v
              Commit    Erreur affichee
              OK        Commit refuse
```

### Key Improvements

| Pain Point Actuel | Solution Proposee | Impact |
|-------------------|-------------------|--------|
| Pas de validation pre-commit | Hook pre-commit bloquant | Detection immediate |
| Desync plugin.json manuelle | Validation automatique | Zero oubli |
| Secrets potentiels non detectes | Regex detection | Securite |

---

## Contraintes Techniques Identifiees

| Contrainte | Impact | Mitigation |
|------------|--------|------------|
| Performance 31 validations | Temps d'execution | Paralleliser si >10s |
| Git hook portable | Cross-platform | Script shell simple |

---

## Dependances

- **Internes**: validate_skill.py, validate_command.py, validate_subagent.py (existants)
- **Externes**: Aucune nouvelle dependance Python

---

## Assumptions

- [x] **Technical** : Python 3 disponible sur toutes les machines dev
- [x] **Technical** : Git hooks fonctionnent sur Linux/Mac/WSL
- [x] **Resources** : Un developpeur alloue pour implementation

---

## Criteres d'Acceptation Globaux

- [ ] 31 validations implementees dans validate_all.py
- [ ] Hook pre-commit installe et fonctionnel
- [ ] Flag `--fix` corrige plugin.json, version sync, frontmatter
- [ ] Documentation mise a jour (CLAUDE.md si necessaire)
- [ ] Tests pytest pour nouvelles validations

---

## Questions Ouvertes

- [ ] Faut-il un flag `--skip-secrets` pour certains cas legitimes ?
- [ ] Le hook doit-il etre installe automatiquement ou manuellement ?

---

## FAQ

### Internal FAQ (Equipe)

**Q: Pourquoi enrichir validate_all.py plutot que creer de nouveaux fichiers ?**
A: Simplicite de maintenance, pattern existant respecte, pas de nouvelle dependance.

**Q: Et si le hook pre-commit est trop lent ?**
A: Paralleliser les validations independantes. Objectif <10s.

**Q: Comment gerer les faux positifs sur secrets ?**
A: Ajouter un `.validation-ignore` si necessaire (v2).

### External FAQ (Utilisateurs)

**Q: Comment installer le hook pre-commit ?**
A: `cp src/hooks/pre-commit .git/hooks/ && chmod +x .git/hooks/pre-commit`

**Q: Comment desactiver temporairement le hook ?**
A: `git commit --no-verify` (usage exceptionnel)

---

## Estimation Preliminaire

| Metrique | Valeur |
|----------|--------|
| Complexite estimee | STANDARD |
| Fichiers impactes | 2 principaux + tests |
| Risque global | Low |

---

## Timeline & Milestones

### Target Launch

**Objectif** : v5.7.0

### Key Milestones

| Milestone | Target | Owner | Status |
|-----------|--------|-------|--------|
| PRD Review | 2026-01-21 | PM | In Progress |
| Implementation | TBD | Dev | Not Started |
| Tests | TBD | Dev | Not Started |
| Documentation | TBD | Dev | Not Started |

### Phasing Strategy

**Phase 1 (MVP)** : US1-US5, US7 (validations critiques + hook)
**Phase 2** : US6, US8 (orphelins, auto-fix)

---

## Appendix

### Liste Complete des 31 Validations

| # | Categorie | Validation | Severite |
|---|-----------|------------|----------|
| 1 | Integrite | plugin.json sync (files exist) | Error |
| 2 | Integrite | plugin.json sync (all declared) | Error |
| 3 | Integrite | Version sync 3 files | Error |
| 4 | Integrite | Duplicate detection | Error |
| 5 | Cross-ref | Skills in commands exist | Error |
| 6 | Cross-ref | Agents in commands exist | Error |
| 7 | Cross-ref | references/ files exist | Warning |
| 8 | Cross-ref | Template paths valid | Warning |
| 9 | Format | Breakpoint syntax | Warning |
| 10 | Format | Skill invocation syntax | Warning |
| 11 | Format | Frontmatter completeness | Error |
| 12 | Format | Description <= 1024 | Warning |
| 13 | Coherence | Model consistency (agents) | Warning |
| 14 | Coherence | Hook references exist | Warning |
| 15 | Coherence | MCP server validity | Warning |
| 16 | Coherence | When-to-use section (skills) | Warning |
| 17 | Coherence | Dependencies declared | Warning |
| 18 | Coherence | Permissions documented | Warning |
| 19 | Qualite | Token count < limit | Error |
| 20 | Qualite | Orphan files detection | Warning |
| 21 | Qualite | Naming conventions | Warning |
| 22 | Securite | Secret detection | Error |
| 23 | Securite | Path traversal check | Error |
| 24 | Doc | Idempotent flag documented | Warning |
| 25 | Doc | Error codes standardises | Warning |
| 26 | Doc | Output format defined | Warning |
| 27 | Doc | Usage section present | Warning |
| 28 | Doc | Error cases documented | Warning |
| 29 | Perf | Context size tracking | Warning |
| 30 | Perf | Timeout per step | Warning |
| 31 | Auto-fix | plugin.json, version, frontmatter | N/A |

### Glossary

| Terme | Definition |
|-------|------------|
| EMS | Exploration Maturity Score (0-100) |
| Cross-ref | Reference croisee entre composants |
| Orphan | Fichier existant mais non reference |
| Pre-commit | Hook Git execute avant chaque commit |

---

*PRD pret pour EPCI — Lancer `/brief @docs/briefs/validation-system-tests/brief-validation-system-tests-20260121.md`*
*Details du processus de brainstorming dans le Journal d'Exploration.*
