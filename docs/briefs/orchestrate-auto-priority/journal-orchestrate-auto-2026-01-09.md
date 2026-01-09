# Journal d'Exploration — Orchestrateur Automatique EPCI

> **Feature**: Orchestrateur Automatique EPCI
> **Date**: 2026-01-09
> **Iterations**: 6 (reprise session du 2026-01-06)

---

## Résumé

Session de brainstorm reprise pour compléter la spécification de la commande `/orchestrate`. Focus sur la **priorisation des specs indépendantes** et l'**UX du plan interactif**. EMS passé de 75 à 87/100 en 2 itérations supplémentaires.

## Progression EMS

| Iteration | Score | Delta | Focus |
|-----------|-------|-------|-------|
| Init | 35 | - | Cadrage initial |
| 1 | 50 | +15 | Autonomie, erreurs, source |
| 2 | 66 | +16 | Formats, retries, validation |
| 3 | 75 | +9 | Architecture finale, DAG |
| 4 (reprise) | 75 | +0 | Début session prioritisation |
| 5 | 84 | +9 | Décisions D8-D11 (prioritisation) |
| 6 (final) | 87 | +3 | Décisions D12-D13 (UX plan) |

## EMS Final Détaillé

| Axe | Score |
|-----|-------|
| Clarté | 90/100 |
| Profondeur | 85/100 |
| Couverture | 82/100 |
| Décisions | 88/100 |
| Actionnabilité | 86/100 |

## Métadonnées Brainstormer

| Métrique | Valeur |
|----------|--------|
| Version | v4.9 |
| Template | feature |
| Techniques appliquées | Cadrage initial, Exemple concret, DAG analysis |
| Durée exploration | ~30min (total 2 sessions) |
| Session originale | 2026-01-06 |
| Session reprise | 2026-01-09 |

## Décisions Clés

### Session 1 (2026-01-06) — Décisions D1-D7

#### Decision D1 — Niveau d'autonomie

- **Contexte**: Définir le degré d'intervention humaine
- **Options considérées**: Full auto, Semi-auto, Supervisé
- **Choix**: Full auto avec auto-correction via tests
- **Justification**: Use case "overnight" nécessite autonomie complète

#### Decision D2 — Gestion des erreurs

- **Contexte**: Que faire quand une spec échoue
- **Options considérées**: Stop, Skip, Retry
- **Choix**: Retry-then-skip (max 3)
- **Justification**: Robustesse sans blocage total

#### Decision D3 — Parallélisme

- **Contexte**: Exécuter plusieurs specs en parallèle?
- **Options considérées**: Parallèle, Séquentiel, Hybride
- **Choix**: Séquentiel strict
- **Justification**: Évite les conflits git

#### Decision D4 — Format journal

- **Contexte**: Comment logger l'exécution
- **Options considérées**: MD only, JSON only, Dual
- **Choix**: Dual (MD + JSON)
- **Justification**: Lisibilité humaine + intégration tooling

#### Decision D5 — Gestion dépendances

- **Contexte**: Que faire si une dépendance échoue
- **Options considérées**: Skip aveugle, DAG-aware skip
- **Choix**: DAG-aware skip
- **Justification**: Skip intelligent des specs dépendantes

#### Decision D6 — Mise à jour INDEX.md

- **Contexte**: Quand mettre à jour la progression
- **Options considérées**: À la fin, Temps réel
- **Choix**: Temps réel après chaque spec
- **Justification**: Visibilité pendant l'exécution

#### Decision D7 — Validation

- **Contexte**: Quoi valider avant commit
- **Options considérées**: Tests only, Tests + Lint, Full loop
- **Choix**: Full loop (tests + lint + review)
- **Justification**: Qualité maximale

### Session 2 (2026-01-09) — Décisions D8-D13

#### Decision D8 — Tri des specs indépendantes

- **Contexte**: Comment ordonner les specs au même niveau DAG
- **Options considérées**: Alphabétique, Effort croissant, Par dépendants
- **Choix**: Effort croissant (TINY → SMALL → STANDARD → LARGE)
- **Justification**: Quick wins d'abord, feedback rapide

#### Decision D9 — Override priorité

- **Contexte**: Permettre de surcharger l'ordre automatique
- **Options considérées**: Via flag CLI, Via INDEX.md, Pas d'override
- **Choix**: Champ optionnel `priority: 1-99` dans INDEX.md
- **Justification**: Flexibilité sans refonte du DAG

#### Decision D10 — Affichage plan

- **Contexte**: Comment présenter le plan à l'utilisateur
- **Options considérées**: Simple affichage, Interactif, Dry-run only
- **Choix**: Plan interactif avec confirmation
- **Justification**: Validation avant exécution, réduit erreurs

#### Decision D11 — Conflit priorité/dépendance

- **Contexte**: Spec haute priorité dépend de spec basse priorité
- **Options considérées**: DAG prime, Warning, Propagation auto
- **Choix**: Propagation automatique de la priorité
- **Justification**: Gestion systématique des cas complexes

#### Decision D12 — Format plan interactif

- **Contexte**: Comment afficher le plan
- **Options considérées**: Liste simple, Tableau, Gantt ASCII
- **Choix**: Tableau avec ordre, effort, priorité, dépendances
- **Justification**: Affichage clair et complet

#### Decision D13 — Actions prompt

- **Contexte**: Quelles actions permettre avant lancement
- **Options considérées**: Y/n, Y/n/skip, Y/n/edit/reorder/skip
- **Choix**: Actions complètes (Y/n/edit/reorder/skip)
- **Justification**: Contrôle complet utilisateur

## Questions Résolues

| Question | Réponse | Iteration |
|----------|---------|-----------|
| Peut-on enchaîner les commandes EPCI ? | Oui, via Task tool et skills | 1 |
| Skills peuvent s'appeler mutuellement ? | Oui, via invocation Task | 1 |
| Gestion contexte entre features ? | Clear équivalent entre specs | 2 |
| Format specs existant ? | INDEX.md + Sxx-name.md | 2 |
| Hooks disponibles ? | Oui, post-phase-3 réutilisable | 3 |
| Comment trier specs indépendantes ? | Effort croissant + priority override | 5 |
| Conflit priorité/dépendance ? | Propagation automatique | 5 |
| Format plan interactif ? | Tableau + actions complètes | 6 |

## Patterns Découverts (codebase)

### Infrastructure existante

| Pattern | Fichier | Réutilisable |
|---------|---------|--------------|
| DAGBuilder | `orchestration/dag_builder.py` | Directement |
| WaveContext | `orchestration/wave_context.py` | Pattern applicable |
| HookRunner | `hooks/runner.py` | Extensible |
| ProgressiveStrategy | `orchestration/strategies/` | Adaptable |
| ProjectMemory | `project-memory/manager.py` | Pour persistence |

### Points d'extension identifiés

1. Hook `post-phase-3` → Update mémoire batch
2. WaveOrchestrator → Extensible pour batch
3. DAG → Validation inter-features + priorités
4. Project-memory → Queue persistante pour --continue

## Exemple UX Final

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ORCHESTRATION PLAN — 3 specs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| # | Spec | Effort | Priority | Deps | Est. |
|---|------|--------|----------|------|------|
| 1 | S02-techniques | 2h | 1 | - | 15min |
| 2 | S01-core | 4h | 2* | - | 25min |
| 3 | S03-modes | 3h | - | S01,S02 | 20min |

* Priority hérité de S03

Total estimé: ~60min | Max retries: 3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Y] Lancer  [n] Annuler  [edit] Modifier  [skip X] Ignorer
> _
```

---

*Journal généré automatiquement par Brainstormer v4.9*
