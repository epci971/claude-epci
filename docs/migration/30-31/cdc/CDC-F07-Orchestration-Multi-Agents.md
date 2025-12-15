# Cahier des Charges — F07: Orchestration Multi-Agents

> **Document**: CDC-F07-001
> **Version**: 1.0.0
> **Date**: 2025-12-15
> **Statut**: Validé
> **Feature ID**: F07
> **Version cible**: EPCI v4.0
> **Priorité**: P1

---

## 1. Contexte Global EPCI

### 1.1 Philosophie EPCI v4.0

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PHILOSOPHIE EPCI                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🎯 SIMPLICITÉ        — 5 commandes ciblées, pas 22                │
│  📋 TRAÇABILITÉ       — Feature Document pour chaque feature        │
│  ⏸️  BREAKPOINTS       — L'humain valide entre les phases           │
│  🔄 TDD               — Red → Green → Refactor systématique         │
│  🧩 MODULARITÉ        — Skills, Agents, Commands séparés            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 État Actuel (Baseline v3.0.0)

Les subagents EPCI s'exécutent **séquentiellement**. Pour les features LARGE, cela crée un goulot d'étranglement.

### 1.3 Glossaire Pertinent

| Terme | Définition |
|-------|------------|
| **Orchestrator** | Composant coordonnant l'exécution multi-agents |
| **DAG** | Directed Acyclic Graph — graphe d'exécution sans cycles |
| **Agent/Subagent** | Composant spécialisé effectuant une tâche de validation |
| **Wave** | Vague d'exécution dans une orchestration multi-étapes |

---

## 2. Description de la Feature

### 2.1 Contexte et Justification

**Problème** : L'exécution séquentielle des agents crée :
- Des temps d'attente inutiles
- Une sous-utilisation des ressources
- Un workflow rigide non adapté aux features complexes

**Solution** : Orchestrator intelligent permettant :
- Exécution parallèle des agents indépendants
- Graphe de dépendances (DAG) entre agents
- Gestion intelligente des erreurs et timeouts
- Configuration flexible par complexité

### 2.2 Objectif

Réduire le temps d'exécution des validations de **30-50%** pour les features STANDARD/LARGE via une orchestration intelligente.

---

## 3. Spécifications Fonctionnelles

### 3.1 Modes d'Orchestration

| Mode | Description | Quand utiliser |
|------|-------------|----------------|
| **Séquentiel** | Un agent après l'autre | Dépendances fortes entre agents |
| **Parallèle** | Agents indépendants simultanés | Validations indépendantes |
| **DAG** | Graphe de dépendances | Features complexes |

### 3.2 DAG d'Orchestration Standard

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DAG ORCHESTRATION                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│                    ┌──────────────────┐                            │
│                    │ @plan-validator  │                            │
│                    └────────┬─────────┘                            │
│                             │                                       │
│              ┌──────────────┼──────────────┐                       │
│              ▼              ▼              ▼                       │
│    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                │
│    │@code-review │ │@security   │ │@qa-reviewer │                │
│    └──────┬──────┘ └──────┬─────┘ └──────┬──────┘                │
│           │               │              │                         │
│           └───────────────┼──────────────┘                         │
│                           ▼                                         │
│                  ┌─────────────────┐                               │
│                  │ @doc-generator  │                               │
│                  └─────────────────┘                               │
│                                                                     │
│  Parallèle: code-review, security, qa (pas de dépendance)         │
│  Séquentiel: plan-validator → ... → doc-generator                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.3 Définition du DAG

```yaml
# dag-config.yaml
orchestration:
  default_mode: "dag"
  timeout_global: 300  # 5 minutes max

  agents:
    plan-validator:
      depends_on: []
      timeout: 60
      required: true

    code-reviewer:
      depends_on: ["plan-validator"]
      timeout: 90
      required: true

    security-auditor:
      depends_on: ["plan-validator"]
      timeout: 60
      required: false  # conditionnel
      condition: "has_sensitive_files"

    qa-reviewer:
      depends_on: ["plan-validator"]
      timeout: 60
      required: false  # conditionnel
      condition: "complexity >= STANDARD"

    doc-generator:
      depends_on: ["code-reviewer", "security-auditor", "qa-reviewer"]
      timeout: 60
      required: true
```

### 3.4 Composant Orchestrator

```python
# agents/orchestrator.py

from typing import Dict, List
from dataclasses import dataclass
from enum import Enum
import asyncio

class AgentStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class AgentResult:
    agent_name: str
    status: AgentStatus
    verdict: str  # APPROVED, REJECTED, WARNING
    duration_seconds: float
    output: dict

class Orchestrator:
    def __init__(self, dag: Dict[str, List[str]], config: dict):
        self.dag = dag
        self.config = config
        self.results: Dict[str, AgentResult] = {}

    async def execute(self, context: dict) -> Dict[str, AgentResult]:
        """
        Exécute les agents selon le DAG.
        Parallélise quand possible.
        """
        pending = set(self.dag.keys())
        completed = set()

        while pending:
            # Trouver agents exécutables (dépendances satisfaites)
            runnable = [
                agent for agent in pending
                if all(dep in completed for dep in self.dag[agent])
            ]

            if not runnable:
                raise OrchestrationError("Cycle détecté ou blocage")

            # Exécuter en parallèle
            tasks = [
                self._execute_agent(agent, context)
                for agent in runnable
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Traiter résultats
            for agent, result in zip(runnable, results):
                self.results[agent] = result
                pending.remove(agent)
                completed.add(agent)

                # Gestion erreur
                if isinstance(result, Exception):
                    if self.config[agent].get("required", True):
                        raise result

        return self.results

    async def _execute_agent(self, agent: str, context: dict) -> AgentResult:
        """Exécute un agent avec timeout."""
        timeout = self.config[agent].get("timeout", 60)
        # ... implémentation
```

### 3.5 Gestion des Erreurs

| Situation | Agent requis | Agent optionnel |
|-----------|--------------|-----------------|
| **Timeout** | Stop orchestration, rollback | Warning, continue |
| **Échec (exit ≠ 0)** | Stop orchestration | Warning, continue |
| **Verdict REJECTED** | Breakpoint utilisateur | Warning dans rapport |

---

## 4. Exigences Techniques

### 4.1 Orchestrator Core

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] DAG parsing | Parser configuration DAG | P1 |
| [MUST] Tri topologique | Ordonner exécution selon dépendances | P1 |
| [MUST] Exécution parallèle | asyncio/threading pour agents indépendants | P1 |
| [MUST] Timeout par agent | Configurable, avec fallback global | P1 |
| [MUST] Collecte résultats | Agréger verdicts de tous agents | P1 |

### 4.2 Gestion Erreurs

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Distinction required/optional | Comportement différencié | P1 |
| [MUST] Propagation erreurs | Stop propre si agent requis échoue | P1 |
| [SHOULD] Retry automatique | 1 retry pour erreurs transitoires | P2 |
| [SHOULD] Partial results | Retourner résultats partiels en cas d'erreur | P2 |

### 4.3 Configuration

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Config YAML | Format lisible humainement | P1 |
| [MUST] Conditions dynamiques | `condition: "has_sensitive_files"` | P1 |
| [SHOULD] Override par projet | `project-memory/orchestration.yaml` | P2 |

---

## 5. Critères d'Acceptation

| ID | Critère | Méthode de vérification |
|----|---------|-------------------------|
| F07-AC1 | Exécution parallèle effective | Temps < séquentiel pour 3+ agents |
| F07-AC2 | Respect dépendances DAG | Ordre correct vérifié par logs |
| F07-AC3 | Gestion erreur agent requis | Stop orchestration |
| F07-AC4 | Gestion erreur agent optionnel | Warning, continue |
| F07-AC5 | Timeout global respecté | Configurable, testé |

---

## 6. Dépendances

### 6.1 Dépendances Entrantes (cette feature dépend de)

| Feature | Type | Description |
|---------|------|-------------|
| F02 Hooks | Forte | Hooks dans orchestration (pre/post agent) |
| F03 Breakpoints | Forte | Breakpoints entre vagues |
| F09 Personas | Faible | Persona influence sélection agents |
| F10 Flags | Forte | Flags contrôlent mode orchestration |

### 6.2 Dépendances Sortantes (dépendent de cette feature)

| Feature | Type | Description |
|---------|------|-------------|
| F11 Wave Orchestration | **Forte** | Waves utilisent l'orchestrator |
| F12 MCP Integration | Faible | MCP routing intégré |

---

## 7. Effort Estimé

| Tâche | Effort |
|-------|--------|
| Orchestrator core | 12h |
| DAG builder et parser | 6h |
| Exécution parallèle (asyncio) | 8h |
| Gestion erreurs et timeouts | 4h |
| Tests | 4h |
| **Total** | **34h (4.5j)** |

---

## 8. Livrables

1. `agents/orchestrator.py` — Composant principal
2. `agents/dag_builder.py` — Constructeur de DAG
3. `config/dag-default.yaml` — Configuration par défaut
4. Documentation utilisateur
5. Tests unitaires et d'intégration

---

## 9. Exemples d'Orchestration

### 9.1 Feature SMALL (Séquentiel)

```
@code-reviewer → @doc-generator
```
Temps: ~2min (séquentiel simple)

### 9.2 Feature STANDARD (DAG Partiel)

```
@plan-validator
       │
       ├──────────────┐
       ▼              ▼
@code-reviewer  @qa-reviewer
       │              │
       └──────┬───────┘
              ▼
       @doc-generator
```
Temps: ~3min (parallélisation code + qa)

### 9.3 Feature LARGE (DAG Complet)

```
@plan-validator
       │
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
@code-reviewer  @security-auditor  @qa-reviewer
       │              │              │
       └──────────────┴──────────────┘
                      │
                      ▼
               @doc-generator
```
Temps: ~4min (vs ~7min séquentiel = **43% gain**)

---

## 10. Métriques de Performance

| Métrique | Cible | Mesure |
|----------|-------|--------|
| Gain parallélisation | > 30% | (temps_seq - temps_parallel) / temps_seq |
| Overhead orchestrator | < 5s | Temps setup + teardown |
| Taux succès | > 95% | Orchestrations complétées sans erreur |

---

## 11. Hors Périmètre

- Orchestration distribuée (multi-machines)
- Queue persistante de jobs
- Dashboard temps réel d'orchestration
- Orchestration cross-projets

---

*Document généré depuis CDC-EPCI-UNIFIE-v4.md*
