# Journal d'Exploration — Optimisation Workflow EPCI

> **Date**: 2025-12-23
> **Durée**: ~45 min
> **Iterations**: 4
> **EMS Final**: 92/100

---

## Objectif Initial

Auditer le workflow EPCI pour identifier :
- Étapes redondantes (notamment exploration)
- Éléments qui se marchent dessus
- Pertes de temps évitables
- Opportunités de réorganisation

---

## Iteration 1 — Analyse Initiale (EMS: 35/100)

### Exploration Codebase

Fichiers analysés :
- `src/commands/epci-brief.md`
- `src/commands/epci.md`
- `src/commands/epci-quick.md`
- `src/skills/core/epci-core/SKILL.md`
- `docs/features/refonte-exploration-epci-brief.md`

### Constats

1. **Exploration** : Redondance identifiée entre epci-brief (@Explore) et epci Phase 1 (@Plan)
   - Découverte : Refonte DÉJÀ IMPLÉMENTÉE — @Plan supprimé de Phase 1

2. **Mémoire** : Chargée 3 fois par workflow (epci-brief, epci, epci-quick)

3. **Agents** : Exécution séquentielle → F07 (parallélisme) déjà implémenté

4. **Breakpoints** : 4 points d'arrêt, tous nécessaires

### Questions Posées

- Exploration exhaustive vs analytique ?
- Breakpoints tous nécessaires ?
- Mémoire à optimiser ?
- Subagents parallèles prioritaires ?

---

## Iteration 2 — Dives Profonds (EMS: 65/100)

### Décisions Utilisateur

1. **Exploration** : Reste exhaustive (thorough), routing APRÈS explore
2. **Breakpoints** : OK sauf ajouter pre-commit dans epci-quick
3. **Mémoire** : Charger 1 seule fois dans epci-brief
4. **Agents** : F07 déjà fait, OK

### Dive Exploration

- Problème séquençage : TINY déterminé APRÈS explore
- Option pré-évaluation discutée puis rejetée (trop risqué)
- Décision : Statu quo, explore thorough systématique

### Dive Mémoire

- Actuellement : 3 chargements par workflow
- Solution : Charger dans epci-brief, passer via Feature Doc/brief
- Gain estimé : -30-60 sec

### Dive Agents

- F07 implémenté : DAG avec 3 waves
- Gain : -40% temps Phase 2
- Pas d'action supplémentaire nécessaire

---

## Iteration 3 — Dives Complémentaires (EMS: 75/100)

### Dive Hooks

Fichier analysé : `src/hooks/README.md`

**Constats** :
- 9 types de hooks existants
- pre-phase-3 redondant avec post-phase-2
- Pas de hooks sur epci-brief

**Décisions** :
- Supprimer pre-phase-3
- Ajouter pre-brief, post-brief
- Garder on-breakpoint

### Dive Feature Document

**Constats** :
- §4 très léger (surtout commit)
- Tableaux fichiers redondants §1 et §2

**Décisions** :
- Fusionner §3 + §4
- Garder tableau uniquement dans §2
- Format Markdown conservé

### Dive Flags

Fichier analysé : `src/settings/flags.md`

**Constats** :
- 10 flags actuels
- --fast et --dry-run jamais utilisés
- Auto-activation bien documentée

**Décisions** :
- Supprimer --fast, --dry-run
- Ajouter --no-hooks

### Dive Skills

**Constats** :
- 21 skills (13 core + 4 stack + 4 factory)
- project-memory et project-memory-loader distincts (pourquoi ?)
- Rechargement = coût tokens

**Décisions** :
- Fusionner project-memory + project-memory-loader
- Implémenter cache session
- Implémenter lazy-load

---

## Iteration 4 — Finalisation (EMS: 92/100)

### Récapitulatif Complet

| Sujet | Décision |
|-------|----------|
| Mémoire | 1x chargement dans epci-brief |
| Exploration | Statu quo (thorough systématique) |
| Breakpoints | Ajouter pre-commit dans epci-quick |
| Hooks | +pre/post-brief, -pre-phase-3 |
| Feature Doc | Fusionner §3+§4, supprimer tableau §1 |
| Flags | -fast, -dry-run, +no-hooks |
| Skills | Fusionner project-memory*, cache, lazy-load |

### Découpage Features

5 features identifiées :
1. F-Memory-Single-Load (SMALL, HIGH)
2. F-Hooks-Restructure (SMALL, MEDIUM)
3. F-Feature-Doc-V2 (SMALL, MEDIUM)
4. F-Flags-Cleanup (TINY, LOW)
5. F-Skills-Consolidate (STANDARD, LOW)

---

## Décisions Clés

### Validées

| # | Décision | Justification |
|---|----------|---------------|
| 1 | Mémoire 1x dans epci-brief | Évite 2 rechargements inutiles |
| 2 | Explore toujours thorough | Évaluation complexité nécessite données complètes |
| 3 | Routing POST exploration | Impossible de connaître TINY avant analyse |
| 4 | Breakpoint pre-commit epci-quick | Cohérence avec epci Phase 3 |
| 5 | Supprimer pre-phase-3 | Redondant avec post-phase-2 |
| 6 | Ajouter hooks epci-brief | Permet intégration externe |
| 7 | Fusionner §3+§4 | §4 trop léger seul |
| 8 | Supprimer --fast, --dry-run | Jamais utilisés |
| 9 | Ajouter --no-hooks | Besoin identifié |
| 10 | Fusionner project-memory skills | Évite confusion |

### Rejetées

| # | Proposition | Raison du rejet |
|---|-------------|-----------------|
| 1 | Pré-évaluation complexité | Estimation imprécise sans explore |
| 2 | Explore "quick" pour TINY | TINY inconnu avant explore |
| 3 | Breakpoints entre waves agents | Trop granulaire, pre/post phases suffisent |
| 4 | Format YAML/JSON Feature Doc | Markdown préféré |

---

## Métriques Session

| Métrique | Valeur |
|----------|--------|
| Fichiers analysés | 12 |
| Dives réalisés | 7 |
| Décisions prises | 10 |
| Propositions rejetées | 4 |
| Features identifiées | 5 |
| Gain estimé total | -1-2 min/workflow |

---

## Prochaines Actions

1. Créer les 5 features dans `docs/features/`
2. Prioriser F-Memory-Single-Load (impact maximal)
3. Implémenter par ordre de priorité

---

*Journal généré par /brainstorm — Session du 2025-12-23*
