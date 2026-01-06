# Specification — S03: Modes & Finish

> **Parent project**: brainstorm-v4.2
> **Spec ID**: S03
> **Estimated effort**: 2 jours
> **Dependencies**: S01, S02
> **Blocks**: —

---

## 1. Context

Cette spec finalise le brainstormer v4.2 avec les modes avancés,
la parallélisation et les tests de validation.

**Source**: `brief-brainstorm-v4.2-2026-01-06.md` — Sections 2.6, 2.7, 2.8

---

## 2. Scope

### Included

- Flag `--random` (sélection aléatoire pondérée)
- Flag `--progressive` (3 phases structurées)
- Parallélisation @Explore en background
- Tests unitaires session + techniques
- Exemples de sessions complètes

### Excluded

- Implémentation session (→ S01, déjà fait)
- Documentation techniques (→ S02, déjà fait)

---

## 3. Tasks

### 3.1 Flag --random

- [ ] Ajouter flag `--random` dans brainstorm.md
- [ ] Implémenter sélection aléatoire de techniques
- [ ] Pondérer par phase:
  - Divergent → favorise Ideation, Perspective, Breakthrough
  - Convergent → favorise Analysis
- [ ] Exclure techniques déjà utilisées dans la session
- [ ] Afficher technique sélectionnée au début de l'itération

**Logique:**
```python
def select_random_technique(phase: str, used: list[str]) -> str:
    weights = {
        "divergent": {"ideation": 0.4, "perspective": 0.3, "breakthrough": 0.2, "analysis": 0.1},
        "convergent": {"analysis": 0.5, "ideation": 0.2, "perspective": 0.2, "breakthrough": 0.1}
    }
    available = [t for t in all_techniques if t not in used]
    return weighted_random_choice(available, weights[phase])
```

**Usage:**
```
/brainstorm --random "améliorer le système de cache"
```

**Affichage:**
```
-------------------------------------------------------
🎲 RANDOM MODE | Technique: SCAMPER (Ideation)
-------------------------------------------------------
[Questions SCAMPER appliquées au contexte]
```

### 3.2 Flag --progressive

- [ ] Ajouter flag `--progressive` dans brainstorm.md
- [ ] Implémenter 3 phases structurées:
  1. **Divergent** (EMS 0-50): Focus exploration, techniques Ideation
  2. **Transition** (EMS 50): Energy check obligatoire + résumé
  3. **Convergent** (EMS 50-100): Focus décisions, techniques Analysis
- [ ] Mapping automatique techniques par phase
- [ ] Transition forcée à EMS 50

**Flow --progressive:**
```
Phase 1: DIVERGENT (EMS 0-50)
├── Techniques: Ideation, Perspective, Breakthrough
├── Questions ouvertes
└── À EMS 50 → TRANSITION

Phase 2: TRANSITION
├── Energy check obligatoire
├── Résumé mi-parcours
├── Validation direction
└── → CONVERGENT

Phase 3: CONVERGENT (EMS 50-100)
├── Techniques: Analysis
├── Questions décisionnelles
└── À EMS 70+ → @planner disponible
```

**Usage:**
```
/brainstorm --progressive "nouveau module de paiement"
```

### 3.3 Parallélisation @Explore

- [ ] Lancer @Explore en background au démarrage
- [ ] Continuer avec questions pendant que @Explore analyse
- [ ] Intégrer résultats @Explore quand disponibles
- [ ] Pré-calculer suggestions techniques en parallèle

**Implémentation:**
```markdown
## Phase 1 — Initialisation (parallélisé)

1. **En parallèle:**
   - Task A: Lancer @Explore (Task tool, background)
   - Task B: Afficher premières questions de cadrage

2. **Quand @Explore termine:**
   - Intégrer fichiers pertinents dans le contexte
   - Enrichir suggestions avec patterns détectés
```

### 3.4 Tests Unitaires

- [ ] Créer `src/scripts/test_brainstorm_session.py`
- [ ] Tests session YAML:
  - Création session valide
  - Save/restore fonctionne
  - Validation format YAML
- [ ] Tests techniques:
  - Chaque technique a le bon format
  - Mapping phases correct
- [ ] Tests modes:
  - --random sélectionne correctement
  - --progressive suit les 3 phases

**Structure tests:**
```python
# test_brainstorm_session.py

import pytest
from pathlib import Path

class TestSessionFormat:
    def test_create_session_valid_yaml(self, tmp_path):
        """Session créée avec format YAML valide."""
        ...

    def test_save_restore_preserves_state(self, tmp_path):
        """Save puis restore préserve l'état complet."""
        ...

    def test_back_restores_previous_iteration(self, tmp_path):
        """Commande back restaure l'itération précédente."""
        ...

class TestTechniques:
    def test_all_techniques_have_required_fields(self):
        """Chaque technique a description, quand, questions, exemple."""
        ...

    def test_phase_mapping_complete(self):
        """Toutes les techniques sont mappées à une phase."""
        ...

class TestModes:
    def test_random_excludes_used_techniques(self):
        """Mode random n'utilise pas les techniques déjà utilisées."""
        ...

    def test_progressive_transitions_at_ems_50(self):
        """Mode progressive déclenche transition à EMS 50."""
        ...
```

### 3.5 Exemples Sessions

- [ ] Créer `docs/briefs/brainstorm-v4/examples/`
- [ ] Créer exemple session complète (divergent → convergent)
- [ ] Créer exemple session avec --random
- [ ] Créer exemple session avec --progressive

**Structure:**
```
docs/briefs/brainstorm-v4/examples/
├── session-example-standard.yaml
├── session-example-random.yaml
└── session-example-progressive.yaml
```

### 3.6 Documentation Finale

- [ ] Mettre à jour brainstorm.md avec tous les flags
- [ ] Documenter les 3 modes (standard, random, progressive)
- [ ] Ajouter exemples d'usage complets
- [ ] Vérifier cohérence avec SKILL.md

---

## 4. Acceptance Criteria

| ID | Criterion | Verification |
|----|-----------|--------------|
| S03-AC1 | --random fonctionne | Flag sélectionne technique aléatoire pondérée |
| S03-AC2 | --random exclut utilisées | Techniques déjà utilisées ne sont pas re-sélectionnées |
| S03-AC3 | --progressive 3 phases | Transition automatique à EMS 50 |
| S03-AC4 | @Explore parallélisé | Questions affichées pendant que @Explore tourne |
| S03-AC5 | Tests passent | 100% tests session + techniques + modes |
| S03-AC6 | Exemples valides | 3 fichiers exemples YAML valides |
| S03-AC7 | Pas de régression | Toutes features v4.1 fonctionnent encore |

---

## 5. Files Impacted

### Modifications

| Fichier | Changements |
|---------|-------------|
| `src/commands/brainstorm.md` | Flags --random, --progressive, parallélisation |

### Créations

| Fichier | Description |
|---------|-------------|
| `src/scripts/test_brainstorm_session.py` | Tests unitaires |
| `docs/briefs/brainstorm-v4/examples/session-example-standard.yaml` | Exemple session standard |
| `docs/briefs/brainstorm-v4/examples/session-example-random.yaml` | Exemple session random |
| `docs/briefs/brainstorm-v4/examples/session-example-progressive.yaml` | Exemple session progressive |

---

## 6. Source Reference

> Extraits de `brief-brainstorm-v4.2-2026-01-06.md`

### Section 2.6 — Modes de Sélection

```markdown
**--random**
- Sélection aléatoire de techniques
- Pondéré par phase (Divergent → Ideation, Convergent → Analysis)
- Exclut les techniques déjà utilisées dans la session

**--progressive**
- 3 phases structurées: Divergent → Transition → Convergent
- Transition = Energy check obligatoire + résumé mi-parcours
- Mapping automatique des techniques par phase
```

### Section 2.7 — Parallélisation

```markdown
**Parallélisation:**
- @Explore en background pendant les questions utilisateur
- Pré-calcul des techniques suggérées en parallèle
```

### Section 5 — Critères de Succès

```markdown
| Critère | Mesure |
|---------|--------|
| Modes random/progressive | Fonctionnent avec flags |
| Tests passent | 100% coverage sur session + techniques |
| Pas de régression | v4.1 features toujours fonctionnelles |
```

---

## 7. Pre-requisites Checklist

Avant de commencer S03, vérifier:

- [ ] S01 Core terminé et mergé
  - [ ] Session save/restore fonctionne
  - [ ] Energy checkpoints implémentés
  - [ ] Format 3-5 questions actif
- [ ] S02 Techniques terminé et mergé
  - [ ] 20 techniques documentées
  - [ ] Commande `technique [x]` fonctionne
  - [ ] Mapping phases défini

---

*Generated by /decompose — Project: brainstorm-v4.2*
