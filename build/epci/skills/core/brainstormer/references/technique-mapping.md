# Technique Mapping — EMS Axes to Categories

> Mapping des axes EMS faibles vers les categories de techniques appropriees.
> Utilise par `@technique-advisor` pour l'auto-selection v5.0.

## Mapping EMS → Categories

| Axe EMS < 50 | Categories Primaires | Categories Secondaires | Rationale |
|--------------|---------------------|------------------------|-----------|
| **Clarte** | deep, structured | creative, prioritization | Clarifier le besoin via analyse profonde |
| **Profondeur** | deep, introspective | creative, theatrical | Explorer en profondeur via introspection |
| **Couverture** | creative, collaborative, wild | theatrical, biomimetic | Elargir via creativite et collaboration |
| **Decisions** | structured, deep, prioritization | collaborative | Structurer les choix via frameworks |
| **Actionnabilite** | structured, prioritization | collaborative, wild | Concretiser via contraintes et action |

## Selection par Phase

### Phase Divergent (EMS < 50)

Privilegier les categories generatives:
- `creative` — Expansion d'idees
- `collaborative` — Perspectives multiples
- `wild` — Rupture creative
- `theatrical` — Jeu de roles et scenarios
- `biomimetic` — Inspiration nature
- `introspective` — Exploration personnelle

### Phase Convergent (EMS >= 50)

Privilegier les categories decisionnelles:
- `structured` — Frameworks de decision
- `deep` — Analyse approfondie
- `quantum` — Resolution de paradoxes

### Phase Transition (EMS = 50)

Mix equilibre:
- 1 technique divergent + 1 technique convergent
- Ou technique `deep` (fonctionne dans les deux phases)

## Regles de Selection

### Mode Standard (auto-select)

1. Identifier `weak_axes[]` depuis `@ems-evaluator`
2. Pour chaque axe faible, collecter categories primaires
3. Filtrer par phase compatible
4. Exclure techniques utilisees dans les 2 dernieres iterations
5. Scorer par pertinence (axe faible le plus bas = priorite)
6. Proposer meilleure technique

### Mode Random (`--random`)

1. Filtrer par phase compatible
2. Selection aleatoire avec equilibrage categories
3. Eviter 2 techniques de meme categorie consecutives
4. Tracking: `source: "random"`

### Mode Progressive (`--progressive`)

| Phase Progressive | Categories Autorisees | Objectif |
|-------------------|----------------------|----------|
| **Phase 1** (Divergent) | creative, wild, collaborative | Maximum d'idees |
| **Phase 2** (Exploration) | deep, theatrical, introspective | Approfondir |
| **Phase 3** (Convergent) | structured, deep | Decider |
| **Phase 4** (Action) | structured uniquement | Concretiser |

Transition automatique basee sur EMS:
- Phase 1: EMS 0-30
- Phase 2: EMS 31-50
- Phase 3: EMS 51-75
- Phase 4: EMS 76+

## Mix de Techniques (2+ axes faibles)

Quand 2+ axes ont score < 50:

1. Selectionner 1 technique par axe faible (max 2)
2. Privilegier combinaisons complementaires:
   - 1 Divergent + 1 Convergent (ideal)
   - Eviter 2 techniques meme categorie
3. Ordre d'application: Divergent d'abord, puis Convergent

### Combinaisons Recommandees

| Axes Faibles | Technique 1 | Technique 2 |
|--------------|-------------|-------------|
| Clarte + Couverture | question-storming | six-hats |
| Profondeur + Decisions | 5whys | moscow |
| Couverture + Actionnabilite | what-if | premortem |
| Clarte + Profondeur | first-principles | 5whys |
| Decisions + Actionnabilite | scoring | constraint-mapping |

## Categories et Difficultes

| Categorie | Easy | Medium | Hard | Total |
|-----------|------|--------|------|-------|
| collaborative | 3 | 1 | 1 | 5 |
| creative | 3 | 6 | 2 | 11 |
| deep | 2 | 3 | 3 | 8 |
| introspective | 2 | 3 | 1 | 6 |
| structured | 4 | 7 | 0 | 11 |
| theatrical | 2 | 3 | 1 | 6 |
| wild | 2 | 3 | 3 | 8 |
| biomimetic | 0 | 1 | 2 | 3 |
| quantum | 0 | 0 | 3 | 3 |
| cultural | 0 | 2 | 2 | 4 |
| prioritization | 2 | 1 | 0 | 3 |
| **Total** | **20** | **30** | **18** | **68** |

## Integration Session YAML

```yaml
techniques_history:
  - iteration: 3
    technique_slug: "six-hats"
    category: "structured"
    suggested_reason: "Couverture 35%"
    applied: true
    source: "auto"  # auto | manual | random | progressive
    weak_axes: ["Couverture", "Decisions"]
```

## Anti-patterns

- **Ne pas** proposer technique de meme categorie 2 fois de suite
- **Ne pas** proposer technique hard si EMS < 30 (trop tot)
- **Ne pas** forcer technique si EMS > 80 (proche finish)
- **Toujours** respecter exclusion des 2 dernieres iterations
