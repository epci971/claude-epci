# Brief Fonctionnel — Orchestrateur Automatique EPCI

> **Brainstormer**: v4.9 | **EMS**: 87/100 | **Template**: feature
> **Date**: 2026-01-09 | **Slug**: orchestrate-auto-priority

---

## Contexte

Le workflow EPCI actuel traite les features une par une avec intervention humaine à chaque étape. Pour les projets avec de nombreuses specs indépendantes (issues de `/decompose`), ce mode manuel devient un goulot d'étranglement.

L'objectif est de pouvoir lancer une orchestration automatique avant la nuit et revenir le matin avec toutes les features implémentées, testées et committées.

## Objectif

Créer une commande `/orchestrate` capable d'exécuter automatiquement le workflow EPCI complet sur un répertoire de specs, sans intervention humaine, avec auto-correction intelligente, priorisation configurable et rapport détaillé.

## Personas

### Persona Primaire — Développeur Lead

- **Role**: Tech Lead ou Senior Developer gérant un projet multi-features
- **Contexte**: Utilise EPCI quotidiennement, a décomposé un projet en 5-15 specs via `/decompose`
- **Pain points**: Doit lancer manuellement chaque spec, surveiller les breakpoints, relancer après erreurs
- **Objectifs**: Automatiser le workflow nocturne, maximiser le throughput, minimiser l'intervention manuelle
- **Quote**: "Je veux lancer avant de partir et avoir tout implémenté le lendemain matin"

### Persona Secondaire — Contributeur CI/CD

- **Role**: DevOps ou développeur intégrant EPCI dans une pipeline
- **Contexte**: Veut déclencher EPCI via scripts ou webhooks
- **Pain points**: Pas d'interface programmatique, pas de format de sortie parsable
- **Objectifs**: Intégrer `/orchestrate` dans des workflows automatisés

## Stack Detecté

- **Framework**: Plugin EPCI pour Claude Code
- **Language**: Python 3 (orchestration), Markdown (specs, commandes)
- **Patterns**: DAG (dépendances), WaveContext (accumulation état), HookRunner (lifecycle)
- **Outils**: asyncio, project-memory, hook system

## Exploration Summary

### Codebase Analysis

- **Structure**: Monorepo avec src/ organisé par fonction
- **Architecture**: Plugin modulaire (commands, skills, agents, hooks)
- **Test patterns**: pytest pour scripts Python

### Fichiers Potentiels

| Fichier | Action | Notes |
|---------|--------|-------|
| `src/commands/orchestrate.md` | Create | Définition commande |
| `src/skills/core/orchestrator/SKILL.md` | Create | Logique orchestration |
| `src/skills/core/orchestrator/references/dag-parser.md` | Create | Parsing INDEX.md |
| `src/skills/core/orchestrator/references/journal-format.md` | Create | Formats journal |
| `src/orchestration/batch_orchestrator.py` | Create | Orchestrateur Python |
| `src/scripts/test_orchestrator.py` | Create | Tests unitaires |

### Patterns Réutilisables

| Pattern | Source | Usage |
|---------|--------|-------|
| DAGBuilder | `orchestration/dag_builder.py` | Validation dépendances |
| WaveContext | `orchestration/wave_context.py` | Accumulation état cross-specs |
| HookRunner | `hooks/runner.py` | Lifecycle events |
| ProgressiveStrategy | `orchestration/strategies/` | Exécution par vagues |

### Risques Identifiés

- **HIGH**: Contexte saturé entre specs → Mitigation: clear agressif
- **MEDIUM**: Git conflicts → Mitigation: mode séquentiel strict
- **MEDIUM**: Interruption mid-run → Mitigation: checkpoint après chaque spec

## User Stories

### US1 — Exécution automatique de specs

**En tant que** développeur lead,
**Je veux** lancer `/orchestrate ./specs/` et voir toutes mes specs s'exécuter automatiquement,
**Afin de** ne pas avoir à surveiller et relancer manuellement chaque feature.

**Acceptance Criteria:**
- [ ] Given un répertoire avec INDEX.md et specs S01-S03, When `/orchestrate ./specs/`, Then les 3 specs sont exécutées dans l'ordre du DAG
- [ ] Given une spec TINY, When orchestration, Then routing vers `/quick`
- [ ] Given une spec STANDARD, When orchestration, Then routing vers `/epci` sans breakpoints
- [ ] Given validation réussie, When spec terminée, Then commit automatique créé

**Priorité**: Must-have
**Complexité**: L

### US2 — Priorisation intelligente des specs

**En tant que** développeur lead,
**Je veux** que les specs indépendantes soient triées par effort croissant avec possibilité d'override,
**Afin de** maximiser les quick wins et avoir du feedback rapide.

**Acceptance Criteria:**
- [ ] Given S01 (4h) et S02 (2h) sans dépendances, When orchestration, Then S02 exécutée avant S01
- [ ] Given S02 avec `priority: 1` dans INDEX.md, When orchestration, Then S02 exécutée en premier
- [ ] Given S03 (priority:1) dépend de S01 (priority:5), When calcul ordre, Then S01 hérite priority:1

**Priorité**: Must-have
**Complexité**: M

### US3 — Plan interactif de confirmation

**En tant que** développeur lead,
**Je veux** voir le plan d'exécution calculé et pouvoir le modifier avant lancement,
**Afin de** valider l'ordre et ajuster si nécessaire.

**Acceptance Criteria:**
- [ ] Given `/orchestrate ./specs/`, When démarrage, Then affiche tableau avec ordre, effort, priorité, dépendances
- [ ] Given prompt affiché, When `Y`, Then lancement exécution
- [ ] Given prompt affiché, When `skip S01,S02`, Then specs ignorées
- [ ] Given prompt affiché, When `edit`, Then modification des priorités en ligne
- [ ] Given prompt affiché, When `reorder`, Then réorganisation manuelle de l'ordre

**Priorité**: Must-have
**Complexité**: M

### US4 — Auto-correction sur échec

**En tant que** développeur lead,
**Je veux** que les erreurs de tests/lint soient auto-corrigées jusqu'à 3 fois,
**Afin de** ne pas bloquer l'orchestration sur des erreurs mineures.

**Acceptance Criteria:**
- [ ] Given test failed après Phase 2, When retry 1, Then Claude analyse l'erreur et corrige
- [ ] Given retry 1 failed, When retry 2, Then approche alternative tentée
- [ ] Given 3 retries failed, When skip, Then spec marquée failed et suivante lancée
- [ ] Given S01 failed et S03 dépend de S01, When S01 skip, Then S03 aussi skipped

**Priorité**: Must-have
**Complexité**: M

### US5 — Journalisation dual format

**En tant que** contributeur CI/CD,
**Je veux** un journal MD lisible et un journal JSON parsable,
**Afin de** suivre l'exécution visuellement ET l'intégrer dans des outils.

**Acceptance Criteria:**
- [ ] Given orchestration terminée, When fin, Then `orchestration-journal.md` créé avec format documenté
- [ ] Given orchestration terminée, When fin, Then `orchestration-journal.json` créé avec structure parsable
- [ ] Given spec terminée, When succès, Then INDEX.md mis à jour en temps réel
- [ ] Given orchestration terminée, When fin, Then `orchestration-report.md` généré avec métriques

**Priorité**: Should-have
**Complexité**: M

### US6 — Reprise après interruption

**En tant que** développeur lead,
**Je veux** pouvoir reprendre une orchestration interrompue,
**Afin de** ne pas perdre le travail déjà effectué.

**Acceptance Criteria:**
- [ ] Given orchestration interrompue à S02, When `/orchestrate ./specs/ --continue`, Then reprend à S02
- [ ] Given checkpoint sauvegardé, When `--continue`, Then état restauré correctement
- [ ] Given S01 déjà committed, When `--continue`, Then S01 non re-exécutée

**Priorité**: Should-have
**Complexité**: M

## Règles Métier

- **RM1**: Le DAG prime toujours sur la priorité — une spec ne peut s'exécuter que si ses dépendances sont résolues
- **RM2**: La priorité ne sert qu'à départager les specs au même niveau DAG
- **RM3**: Maximum 3 retries par spec (configurable via `--max-retries`)
- **RM4**: Un commit = une spec validée, jamais de commit groupé
- **RM5**: Libération contexte obligatoire entre chaque spec (équivalent `/clear`)

## Cas Limites & Edge Cases

| Cas | Comportement attendu |
|-----|---------------------|
| INDEX.md invalide | Abort immédiat avec erreur explicite |
| Spec file manquant | Skip spec, warning, continuer les autres |
| Cycle dans DAG | Abort immédiat avec visualisation du cycle |
| Git conflict | Abort, demande intervention manuelle |
| Toutes specs failed | Rapport avec 0/N succès, exit code 1 |
| Spec vide (0 requirements) | Skip avec warning "empty spec" |
| Timeout spec (>1h) | Skip après timeout, marquer "timeout" |

## Hors Scope (v1)

- **Parallélisme inter-features** — Mode séquentiel uniquement pour éviter conflits git
- **Orchestration cross-repos** — Un seul répertoire de specs à la fois
- **Notifications externes** — Pas de Slack/email/webhook en v1
- **Rollback automatique** — Si échec, pas de git revert automatique

## Success Metrics

| Métrique | Baseline | Cible | Méthode de mesure |
|----------|----------|-------|-------------------|
| Taux de succès specs | N/A | > 80% | Rapport final |
| Temps moyen par spec | ~15min manuel | < 20min auto | Journal JSON |
| Retries nécessaires | N/A | < 1 par spec en moyenne | Journal JSON |
| Interventions manuelles | 100% specs | 0% (sauf abort) | Logs |

## User Flow

```
/orchestrate ./specs/
       |
       v
  [Parse INDEX.md]
       |
       v
  [Build DAG + Sort]
       |
       v
  [Afficher plan]
       |
       +--[Y]--> [Boucle specs]
       |              |
  [n/edit/skip]       v
       |         [/brief spec]
       v              |
    [Exit]            v
                 [/epci ou /quick]
                      |
                      v
                 [Validation]
                      |
              [OK?]---+---[KO?]
                |           |
                v           v
           [Commit]    [Retry 1-3]
                |           |
                v           v
           [Update]    [Skip if 3x]
                |           |
                +-----+-----+
                      |
                      v
                 [Clear context]
                      |
                      v
                 [Next spec]
                      |
                      v
                 [Rapport final]
```

## Contraintes Techniques Identifiées

| Contrainte | Impact | Mitigation |
|------------|--------|------------|
| Contexte LLM limité | Specs longues peuvent saturer | Clear agressif entre specs |
| Git single-thread | Conflits si parallèle | Mode séquentiel strict |
| Hooks synchrones | Peuvent ralentir | Hooks légers, async si possible |

## Dépendances

- **Internes**: dag_builder.py, wave_context.py, hooks/runner.py, project-memory/manager.py
- **Externes**: Aucune nouvelle dépendance externe

## Critères d'Acceptation Globaux

- [ ] Parse INDEX.md avec dépendances → DAG construit correctement
- [ ] Exécute specs dans l'ordre DAG + priorité
- [ ] Skip specs si dépendance échoue
- [ ] Auto-correction jusqu'à 3 retries
- [ ] Commit automatique si succès
- [ ] Journal MD lisible avec format documenté
- [ ] Journal JSON parsable avec structure validée
- [ ] INDEX.md mis à jour temps réel
- [ ] Rapport final complet avec métriques
- [ ] --dry-run affiche plan sans exécuter
- [ ] --continue reprend après interruption
- [ ] Libération contexte entre specs

## Questions Ouvertes

- [ ] Format exact du champ `priority` dans INDEX.md (entier 1-99 ou labels low/medium/high?)
- [ ] Stratégie de timeout par spec (fixe 1h ou proportionnel à l'effort?)

## Estimation Préliminaire

| Métrique | Valeur |
|----------|--------|
| Complexité estimée | LARGE |
| Fichiers impactés | ~8-10 |
| Risque global | Medium |

---

## Interface CLI

### Commande principale

```bash
/orchestrate [specs-dir] [flags]
```

### Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--dry-run` | Affiche le plan sans exécuter | false |
| `--max-retries N` | Nombre max de retries par spec | 3 |
| `--continue` | Reprend une orchestration interrompue | false |
| `--skip S01,S02` | Ignore certaines specs | - |
| `--only S01` | Exécute uniquement certaines specs | - |
| `--no-commit` | Désactive les commits automatiques | false |
| `--verbose` | Journal détaillé en temps réel | false |

### Exemples

```bash
# Exécution complète
/orchestrate ./docs/briefs/brainstorm-v4/specs/

# Dry-run pour voir le plan
/orchestrate ./docs/briefs/brainstorm-v4/specs/ --dry-run

# Reprendre après interruption
/orchestrate ./docs/briefs/brainstorm-v4/specs/ --continue

# Mode verbeux avec 5 retries max
/orchestrate ./docs/briefs/brainstorm-v4/specs/ --verbose --max-retries 5
```

---

## Plan d'Implémentation Suggéré

### Phase 1 — Fondations (3h)
- [ ] Créer `src/commands/orchestrate.md`
- [ ] Créer `src/skills/core/orchestrator/SKILL.md`
- [ ] Implémenter parser INDEX.md avec priority
- [ ] Intégrer DAGBuilder existant avec propagation priorité

### Phase 2 — Exécution (3h)
- [ ] Implémenter boucle séquentielle
- [ ] Intégrer appels /brief + /epci + /quick
- [ ] Implémenter logique retry
- [ ] Gérer libération contexte

### Phase 3 — UX & Journalisation (1.5h)
- [ ] Implémenter plan interactif avec tableau
- [ ] Implémenter actions Y/n/edit/reorder/skip
- [ ] Implémenter journal MD temps réel
- [ ] Implémenter journal JSON
- [ ] Générer rapport final

### Phase 4 — Tests & Polish (0.5h)
- [ ] Tests parser INDEX.md
- [ ] Tests DAG + priorité
- [ ] Test dry-run
- [ ] Test --continue

---

## Décisions Clés

| # | Décision | Justification |
|---|----------|---------------|
| D1 | Full auto sans breakpoints | Use case overnight |
| D2 | Retry-then-skip (max 3) | Robustesse sans blocage |
| D3 | Séquentiel strict | Évite conflits git |
| D4 | Journal dual (MD + JSON) | Lisibilité + tooling |
| D5 | DAG-aware skip | Intelligence sur dépendances |
| D6 | Update INDEX.md temps réel | Visibilité progression |
| D7 | Full loop validation | Tests + lint + review |
| D8 | Tri par effort croissant | Quick wins d'abord |
| D9 | Override via priority | Flexibilité sans refonte DAG |
| D10 | Plan interactif | Validation avant exécution |
| D11 | Propagation priorité | Gestion cas complexes DAG |
| D12 | Format tableau | Affichage clair du plan |
| D13 | Actions Y/n/edit/reorder/skip | Contrôle complet utilisateur |

---

*Brief prêt pour EPCI — Lancer `/brief` avec ce contenu.*
*Détails du processus de brainstorming dans le Journal d'Exploration.*
