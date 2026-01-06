# Brief — Orchestrateur Automatique EPCI

> **Version**: 1.0
> **Date**: 2026-01-06
> **Complexité**: LARGE
> **Effort estimé**: 8h
> **EMS Final**: 75/100

---

## 1. Objectif

Créer une commande `/orchestrate` capable d'exécuter automatiquement le workflow EPCI complet sur un répertoire de specs, sans intervention humaine, avec auto-correction et rapport détaillé.

**Use case principal** : Lancer avant la nuit, revenir le matin avec toutes les features implémentées.

---

## 2. Description Fonctionnelle

### 2.1 Vue d'ensemble

```
/orchestrate ./specs/
    │
    ├─ PARSE: Lire INDEX.md, construire DAG
    ├─ PLAN: Afficher ordre, estimer durée
    ├─ EXECUTE: Boucle séquentielle avec auto-correction
    └─ REPORT: Journal + rapport final
```

### 2.2 Flux d'exécution

Pour chaque spec dans l'ordre du DAG :

1. **Brief** → Routing automatique (EPCI vs Quick)
2. **Implémentation** → Phases 1-2-3 sans breakpoints
3. **Validation** → Tests + Lint + Review (full loop)
4. **Auto-correction** → Jusqu'à 3 retries si échec
5. **Commit** → Si validation OK
6. **Update** → INDEX.md Progress en temps réel
7. **Clear** → Libération contexte avant spec suivante

### 2.3 Gestion des dépendances

- Respect du DAG défini dans INDEX.md
- Si S01 échoue et S03 dépend de S01 → skip S03
- Specs indépendantes tentées même si autres échouent
- Exemple : S01 fail → S02 tenté → S03 skipped (dépend S01)

---

## 3. Exigences Fonctionnelles

### 3.1 Parsing INDEX.md

| Requirement | Description |
|-------------|-------------|
| FR-01 | Parser le tableau Overview (ID, Effort, Dépendances) |
| FR-02 | Construire DAG à partir des dépendances |
| FR-03 | Valider que toutes les specs référencées existent |
| FR-04 | Détecter cycles dans le DAG |

### 3.2 Exécution autonome

| Requirement | Description |
|-------------|-------------|
| FR-05 | Exécuter /brief avec contenu de la spec |
| FR-06 | Router automatiquement vers /epci ou /quick |
| FR-07 | Désactiver tous les breakpoints (mode --autonomous) |
| FR-08 | Valider via tests + lint + review après Phase 2 |
| FR-09 | Auto-corriger jusqu'à 3 retries (configurable) |
| FR-10 | Committer automatiquement si validation OK |
| FR-11 | Skipper et logger si 3 retries échouent |

### 3.3 Gestion contexte

| Requirement | Description |
|-------------|-------------|
| FR-12 | Libérer contexte entre chaque spec (équivalent /clear) |
| FR-13 | Conserver uniquement le journal cross-specs |
| FR-14 | Permettre reprise après interruption (--continue) |

### 3.4 Journalisation

| Requirement | Description |
|-------------|-------------|
| FR-15 | Journal temps réel (.md) lisible humain |
| FR-16 | Journal structuré (.json) pour tooling |
| FR-17 | Mise à jour INDEX.md Progress après chaque spec |
| FR-18 | Rapport final avec métriques complètes |

---

## 4. Format des fichiers

### 4.1 Journal d'exécution (orchestration-journal.md)

```markdown
# Orchestration Journal — 2026-01-06T22:15:00

## Configuration
- Source: ./docs/briefs/brainstorm-v4/specs/
- Specs: 3 (S01, S02, S03)
- Mode: sequential
- Max retries: 3

---

## S01-core
- Started: 22:15:00
- Routing: /epci (STANDARD)
- Phase 1: ✅ 3min
- Phase 2: ✅ 12min (1 retry - test fix)
- Phase 3: ✅ 2min
- Commit: abc1234 "feat(brainstorm): implement session continuation"
- Duration: 17min
- Status: SUCCESS

## S02-techniques
- Started: 22:32:00
- Routing: /quick (SMALL)
- EPCT: ✅ 8min
- Commit: def5678 "feat(brainstorm): add 20 techniques library"
- Duration: 8min
- Status: SUCCESS

## S03-modes-finish
- Started: 22:40:00
- Routing: /epci (STANDARD)
- Phase 1: ✅ 2min
- Phase 2: ❌ Tests failed
- Retry 1/3: ❌ Still failing
- Retry 2/3: ✅ Fixed
- Phase 3: ✅ 3min
- Commit: ghi9012 "feat(brainstorm): add random and progressive modes"
- Duration: 15min
- Status: SUCCESS

---

## Summary
- Total: 3/3 specs completed
- Duration: 40min
- Commits: 3
- Retries: 2 (1 on S01, 1 on S03)
```

### 4.2 Journal structuré (orchestration-journal.json)

```json
{
  "orchestration_id": "orch-2026-01-06-221500",
  "started_at": "2026-01-06T22:15:00Z",
  "completed_at": "2026-01-06T22:55:00Z",
  "source_dir": "./docs/briefs/brainstorm-v4/specs/",
  "config": {
    "mode": "sequential",
    "max_retries": 3,
    "auto_commit": true
  },
  "specs": [
    {
      "id": "S01",
      "file": "S01-core.md",
      "started_at": "2026-01-06T22:15:00Z",
      "routing": "epci",
      "complexity": "STANDARD",
      "phases": {
        "phase1": {"status": "success", "duration_sec": 180},
        "phase2": {"status": "success", "duration_sec": 720, "retries": 1},
        "phase3": {"status": "success", "duration_sec": 120}
      },
      "commit": {
        "sha": "abc1234",
        "message": "feat(brainstorm): implement session continuation"
      },
      "duration_sec": 1020,
      "status": "success"
    }
  ],
  "summary": {
    "total_specs": 3,
    "succeeded": 3,
    "failed": 0,
    "skipped": 0,
    "total_duration_sec": 2400,
    "total_retries": 2,
    "commits": ["abc1234", "def5678", "ghi9012"]
  }
}
```

### 4.3 Rapport final (orchestration-report.md)

```markdown
# Orchestration Report — 2026-01-06

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Specs | 3 |
| Succeeded | 3 (100%) |
| Failed | 0 |
| Skipped | 0 |
| Total Duration | 40min |
| Commits Created | 3 |

## Results by Spec

| Spec | Status | Duration | Retries | Commit |
|------|--------|----------|---------|--------|
| S01-core | ✅ SUCCESS | 17min | 1 | abc1234 |
| S02-techniques | ✅ SUCCESS | 8min | 0 | def5678 |
| S03-modes-finish | ✅ SUCCESS | 15min | 1 | ghi9012 |

## Errors Encountered

### S01-core (Retry 1)
- Phase: Phase 2
- Error: Test `test_session_save` failed - missing field `updated`
- Resolution: Added `updated` field to session YAML

### S03-modes-finish (Retry 1)
- Phase: Phase 2
- Error: Type error in `select_random_technique`
- Resolution: Fixed return type annotation

## Files Modified

| File | Specs | Changes |
|------|-------|---------|
| src/commands/brainstorm.md | S01, S02, S03 | +450 lines |
| src/skills/core/brainstormer/SKILL.md | S01, S02 | +120 lines |
| src/skills/core/brainstormer/references/session-format.md | S01 | Created |
| src/skills/core/brainstormer/references/techniques/*.md | S02 | 4 files created |
| src/scripts/test_brainstorm_session.py | S03 | Created |

## Metrics

| Metric | Value |
|--------|-------|
| Lines Added | 892 |
| Lines Removed | 45 |
| Tests Added | 12 |
| Tests Passing | 12/12 |

## Recommendations

- S01 et S03 ont nécessité des retries → Améliorer les tests en amont
- Temps moyen par spec: 13min → Conforme aux estimations

---
*Generated by /orchestrate — 2026-01-06T22:55:00*
```

---

## 5. Interface CLI

### 5.1 Commande principale

```bash
/orchestrate [specs-dir] [flags]
```

### 5.2 Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--dry-run` | Affiche le plan sans exécuter | false |
| `--max-retries N` | Nombre max de retries par spec | 3 |
| `--continue` | Reprend une orchestration interrompue | false |
| `--skip S01,S02` | Ignore certaines specs | - |
| `--only S01` | Exécute uniquement certaines specs | - |
| `--no-commit` | Désactive les commits automatiques | false |
| `--verbose` | Journal détaillé en temps réel | false |

### 5.3 Exemples

```bash
# Exécution complète
/orchestrate ./docs/briefs/brainstorm-v4/specs/

# Dry-run pour voir le plan
/orchestrate ./docs/briefs/brainstorm-v4/specs/ --dry-run

# Reprendre après interruption
/orchestrate ./docs/briefs/brainstorm-v4/specs/ --continue

# Exécuter uniquement S03
/orchestrate ./docs/briefs/brainstorm-v4/specs/ --only S03

# Mode verbeux avec 5 retries max
/orchestrate ./docs/briefs/brainstorm-v4/specs/ --verbose --max-retries 5
```

---

## 6. Architecture Technique

### 6.1 Nouveaux fichiers

| Fichier | Description |
|---------|-------------|
| `src/commands/orchestrate.md` | Définition commande |
| `src/skills/core/orchestrator/SKILL.md` | Logique orchestration |
| `src/skills/core/orchestrator/references/dag-parser.md` | Parsing INDEX.md |
| `src/skills/core/orchestrator/references/journal-format.md` | Formats journal |
| `src/orchestration/batch_orchestrator.py` | Orchestrateur Python |
| `src/scripts/test_orchestrator.py` | Tests unitaires |

### 6.2 Réutilisation existante

| Composant | Usage |
|-----------|-------|
| `src/orchestration/dag_builder.py` | Construction DAG |
| `src/orchestration/wave_context.py` | Pattern contexte |
| `src/hooks/runner.py` | Lifecycle events |
| `src/project-memory/manager.py` | Persistence état |

### 6.3 Intégration hooks

| Hook | Trigger | Action |
|------|---------|--------|
| `pre-orchestrate` | Avant démarrage | Validation config |
| `post-spec` | Après chaque spec | Update INDEX.md |
| `post-orchestrate` | À la fin | Génération rapport |

---

## 7. Gestion des erreurs

### 7.1 Stratégie retry

```
Échec validation
    │
    ├── Retry 1: Re-run avec erreur en contexte
    │   └── Claude analyse l'erreur et corrige
    │
    ├── Retry 2: Re-run avec historique retries
    │   └── Claude essaie approche alternative
    │
    ├── Retry 3: Dernière tentative
    │   └── Approche minimaliste
    │
    └── Skip: Log erreur complète, passe à la suite
```

### 7.2 Erreurs non-récupérables

| Erreur | Action |
|--------|--------|
| INDEX.md invalide | Abort immédiat |
| Spec file manquant | Skip spec, continuer |
| Git conflict | Abort, demande intervention |
| Cycle dans DAG | Abort immédiat |

---

## 8. Critères d'acceptation

| ID | Critère | Vérification |
|----|---------|--------------|
| AC-01 | Parse INDEX.md avec dépendances | DAG construit correctement |
| AC-02 | Exécute specs dans l'ordre DAG | S01 → S02 → S03 (selon deps) |
| AC-03 | Skip specs si dépendance échoue | S01 fail → S03 skipped |
| AC-04 | Auto-correction jusqu'à 3 retries | Test échec → retry → succès |
| AC-05 | Commit automatique si succès | SHA dans journal |
| AC-06 | Journal MD lisible | Format documenté respecté |
| AC-07 | Journal JSON parsable | Structure validée |
| AC-08 | INDEX.md mis à jour temps réel | Progress visible pendant run |
| AC-09 | Rapport final complet | Toutes métriques présentes |
| AC-10 | --dry-run affiche plan sans exécuter | Aucune modification |
| AC-11 | --continue reprend après interruption | État restauré |
| AC-12 | Libération contexte entre specs | Pas de pollution cross-spec |

---

## 9. Exploration Summary

### 9.1 Stack existante

- **Orchestration**: `asyncio` + DAG (Kahn's algorithm)
- **Hooks**: Runner Python avec discovery auto
- **Memory**: `.project-memory/` avec manager Python
- **Strategies**: Progressive + Systematic (réutilisables)

### 9.2 Patterns exploitables

| Pattern | Source | Usage |
|---------|--------|-------|
| WaveContext | wave_context.py | Accumulation état cross-specs |
| DAGBuilder | dag_builder.py | Validation dépendances |
| HookRunner | runner.py | Lifecycle events |
| ProgressiveStrategy | strategies/ | Exécution par vagues |

### 9.3 Points d'extension

- Hook `post-phase-3` déjà prévu pour mémoire
- WaveOrchestrator extensible pour batch
- Project memory prêt pour queue persistante

---

## 10. Risques et mitigations

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Contexte saturé | HIGH | Clear agressif entre specs |
| Git conflicts | MEDIUM | Mode séquentiel strict |
| Boucle retry infinie | LOW | Max 3 retries hard-coded |
| Spec mal formatée | LOW | Validation upfront |
| Interruption mid-run | MEDIUM | Checkpoint après chaque spec |

---

## 11. Plan d'implémentation suggéré

### Phase 1 — Fondations (3h)
- [ ] Créer `src/commands/orchestrate.md`
- [ ] Créer `src/skills/core/orchestrator/SKILL.md`
- [ ] Implémenter parser INDEX.md
- [ ] Intégrer DAGBuilder existant

### Phase 2 — Exécution (3h)
- [ ] Implémenter boucle séquentielle
- [ ] Intégrer appels /brief + /epci + /quick
- [ ] Implémenter logique retry
- [ ] Gérer libération contexte

### Phase 3 — Journalisation (1.5h)
- [ ] Implémenter journal MD temps réel
- [ ] Implémenter journal JSON
- [ ] Implémenter mise à jour INDEX.md
- [ ] Générer rapport final

### Phase 4 — Tests (0.5h)
- [ ] Tests parser INDEX.md
- [ ] Tests DAG dépendances
- [ ] Test dry-run
- [ ] Test --continue

---

*Generated by /brainstorm — EMS: 75/100*
