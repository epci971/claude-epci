# Specification — S02: Techniques

> **Parent project**: brainstorm-v4.2
> **Spec ID**: S02
> **Estimated effort**: 3 jours
> **Dependencies**: — (parallélisable avec S01)
> **Blocks**: S03

---

## 1. Context

Cette spec implémente la bibliothèque étendue de techniques de brainstorming,
passant de 5 frameworks à 20 techniques réparties en 4 catégories.

**Source**: `brief-brainstorm-v4.2-2026-01-06.md` — Section 2.2

---

## 2. Scope

### Included

- Création de 4 fichiers techniques (analysis, ideation, perspective, breakthrough)
- Documentation de 20 techniques au format structuré
- Commande `technique [x]` pour appliquer une technique
- Mapping techniques → phases (Divergent/Convergent)
- Mise à jour SKILL.md pour référencer les techniques

### Excluded

- Session continuation (→ S01)
- Modes --random et --progressive (→ S03)
- Sélection automatique de techniques (→ S03)

---

## 3. Tasks

### 3.1 Structure Fichiers

- [ ] Créer dossier `references/techniques/`
- [ ] Créer `analysis.md` (8 techniques)
- [ ] Créer `ideation.md` (6 techniques)
- [ ] Créer `perspective.md` (3 techniques)
- [ ] Créer `breakthrough.md` (3 techniques)

**Structure:**
```
src/skills/core/brainstormer/references/techniques/
├── analysis.md      # 8 techniques
├── ideation.md      # 6 techniques
├── perspective.md   # 3 techniques
└── breakthrough.md  # 3 techniques
```

### 3.2 Format par Technique

Chaque technique doit suivre ce format:

```markdown
### [Nom Technique]

**Description:** [2-3 lignes explicatives]

**Quand utiliser:**
- [Situation 1]
- [Situation 2]

**Phase recommandée:** [Divergent | Convergent | Les deux]

**Questions types:**
1. [Question guidée 1]
2. [Question guidée 2]
3. [Question guidée 3]

**Exemple:**
> [Exemple concret d'application dans un contexte dev]
```

### 3.3 Techniques Analysis (8)

| Technique | Source | Description |
|-----------|--------|-------------|
| MoSCoW | EPCI v4.1 | Priorisation Must/Should/Could/Won't |
| 5 Whys | EPCI v4.1 | Analyse cause racine itérative |
| SWOT | EPCI v4.1 | Forces/Faiblesses/Opportunités/Menaces |
| Scoring | EPCI v4.1 | Matrice de décision pondérée |
| Pre-mortem | EPCI v4.1 | Anticipation des échecs |
| Constraint Mapping | BMAD | Visualisation de toutes les contraintes |
| Assumption Reversal | BMAD | Challenger les hypothèses de base |
| Question Storming | BMAD | Générer des questions avant les réponses |

- [ ] Documenter MoSCoW (existant, enrichir)
- [ ] Documenter 5 Whys (existant, enrichir)
- [ ] Documenter SWOT (existant, enrichir)
- [ ] Documenter Scoring (existant, enrichir)
- [ ] Documenter Pre-mortem (existant, enrichir)
- [ ] Documenter Constraint Mapping (nouveau)
- [ ] Documenter Assumption Reversal (nouveau)
- [ ] Documenter Question Storming (nouveau)

### 3.4 Techniques Ideation (6)

| Technique | Source | Description |
|-----------|--------|-------------|
| SCAMPER | BMAD | 7 lenses créatives (Substitute, Combine, Adapt...) |
| Six Thinking Hats | BMAD | 6 perspectives (White, Red, Black, Yellow, Green, Blue) |
| Mind Mapping | BMAD | Arborescence visuelle d'idées |
| What If Scenarios | BMAD | Exploration de scénarios hypothétiques |
| Analogical Thinking | BMAD | Transfert de patterns d'autres domaines |
| First Principles | BMAD | Déconstruction jusqu'aux fondamentaux |

- [ ] Documenter SCAMPER
- [ ] Documenter Six Thinking Hats
- [ ] Documenter Mind Mapping
- [ ] Documenter What If Scenarios
- [ ] Documenter Analogical Thinking
- [ ] Documenter First Principles

### 3.5 Techniques Perspective (3)

| Technique | Source | Description |
|-----------|--------|-------------|
| Role Playing | BMAD | Adopter le point de vue de stakeholders |
| Time Travel | BMAD | Se projeter dans le futur/passé |
| Reversal Inversion | BMAD | Inverser le problème pour révéler les assumptions |

- [ ] Documenter Role Playing
- [ ] Documenter Time Travel
- [ ] Documenter Reversal Inversion

### 3.6 Techniques Breakthrough (3)

| Technique | Source | Description |
|-----------|--------|-------------|
| Inner Child Conference | BMAD | Déblocage créatif par approche naïve |
| Chaos Engineering | BMAD | Stress-test des idées par injection de chaos |
| Nature's Solutions | BMAD | Bio-inspiration, patterns naturels |

- [ ] Documenter Inner Child Conference
- [ ] Documenter Chaos Engineering
- [ ] Documenter Nature's Solutions

### 3.7 Commande technique

- [ ] Ajouter `technique [x]` dans brainstorm.md
- [ ] Implémenter lookup technique par nom
- [ ] Afficher les questions types de la technique
- [ ] Intégrer dans le flow d'itération

**Usage:**
```
technique scamper
technique first-principles
technique reversal
```

### 3.8 Mapping Phases

- [ ] Définir association techniques → phases dans SKILL.md
- [ ] Divergent: Ideation, Perspective, Breakthrough
- [ ] Convergent: Analysis
- [ ] Les deux: Certaines techniques polyvalentes

**Mapping:**
```markdown
## Mapping Techniques → Phases

| Phase | Techniques Recommandées |
|-------|------------------------|
| 🔀 Divergent | SCAMPER, Six Hats, Mind Mapping, What If, Analogical, Time Travel, Inner Child, Chaos, Nature |
| 🎯 Convergent | MoSCoW, 5 Whys, SWOT, Scoring, Pre-mortem, Constraint, First Principles, Role Playing |
| Déblocage | Reversal, Assumption Reversal, Question Storming, Breakthrough* |
```

### 3.9 Mise à jour SKILL.md

- [ ] Ajouter références vers techniques/*.md
- [ ] Documenter la commande `technique [x]`
- [ ] Ajouter section "Bibliothèque de Techniques"

---

## 4. Acceptance Criteria

| ID | Criterion | Verification |
|----|-----------|--------------|
| S02-AC1 | 4 fichiers techniques créés | Vérifier existence dans references/techniques/ |
| S02-AC2 | 20 techniques documentées | Chaque technique suit le format structuré |
| S02-AC3 | Commande technique fonctionne | `technique scamper` affiche les questions SCAMPER |
| S02-AC4 | Mapping phases documenté | SKILL.md contient le mapping techniques → phases |
| S02-AC5 | Techniques existantes enrichies | MoSCoW, 5 Whys, SWOT, Scoring, Pre-mortem au nouveau format |
| S02-AC6 | Exemples concrets | Chaque technique a un exemple contexte dev |

---

## 5. Files Impacted

### Créations

| Fichier | Description |
|---------|-------------|
| `src/skills/core/brainstormer/references/techniques/analysis.md` | 8 techniques d'analyse |
| `src/skills/core/brainstormer/references/techniques/ideation.md` | 6 techniques d'idéation |
| `src/skills/core/brainstormer/references/techniques/perspective.md` | 3 techniques de perspective |
| `src/skills/core/brainstormer/references/techniques/breakthrough.md` | 3 techniques de déblocage |

### Modifications

| Fichier | Changements |
|---------|-------------|
| `src/skills/core/brainstormer/SKILL.md` | Références techniques, mapping phases |
| `src/commands/brainstorm.md` | Commande `technique [x]` |

---

## 6. Source Reference

> Extraits de `brief-brainstorm-v4.2-2026-01-06.md`

### Section 2.2 — Bibliothèque de Techniques

```markdown
**Techniques à implémenter (Top 15 + existants):**

| Catégorie | Techniques |
|-----------|------------|
| **Analysis** | MoSCoW*, 5 Whys*, SWOT*, Scoring*, Pre-mortem*, Constraint Mapping, Assumption Reversal, Question Storming |
| **Ideation** | SCAMPER, Six Thinking Hats, Mind Mapping, What If Scenarios, Analogical Thinking, First Principles |
| **Perspective** | Role Playing, Time Travel, Reversal Inversion |
| **Breakthrough** | Inner Child Conference, Chaos Engineering, Nature's Solutions |
```

### Confrontation BMAD (référence)

Les techniques nouvelles proviennent de l'analyse BMAD v6:
- `analyse-bmad-brainstorming-system.md`
- `confrontation-epci-vs-bmad.md` — Section 4

---

*Generated by /decompose — Project: brainstorm-v4.2*
