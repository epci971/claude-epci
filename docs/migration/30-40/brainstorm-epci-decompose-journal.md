# 📓 Journal d'Exploration — Feature `epci-decompose`

> **Session**: Brainstorming EPCI Decompose
> **Date**: 18 décembre 2025
> **Durée**: 5 itérations
> **EMS Final**: 88/100

---

## Métadonnées Session

| Champ | Valeur |
|-------|--------|
| **Sujet initial** | Commande pour découper PRD complexe en sous-cahiers des charges |
| **Type détecté** | Technique (extension plugin EPCI) |
| **Template** | Feature |
| **Mode** | Standard + Coaching |
| **Critères de succès** | Sous-specs utilisables par `/epci-brief`, dépendances visualisées |

---

## Progression EMS

```
100 ┤
 90 ┤                                        ●━━━ 88 (Final)
 80 ┤                              ●━━━━━━━━━┛ 82
 70 ┤                    ●━━━━━━━━━┛ 71
 60 ┤
 50 ┤          ●━━━━━━━━━┛ 52
 40 ┤
 30 ┤ ●━━━━━━━━┛ 28
 20 ┤
 10 ┤
  0 ┼────┬────┬────┬────┬────┬────
       I1   I2   I3   I4   I5
```

| Itération | EMS | Delta | Focus |
|-----------|-----|-------|-------|
| Init | 0 | — | Brief validé |
| I1 | 28 | +28 | Questions de clarification |
| I2 | 52 | +24 | Analyse cas réel (Gardel) |
| I3 | 71 | +19 | Workflow & format sortie |
| I4 | 82 | +11 | Signature commande & edge cases |
| I5 | 88 | +6 | Finalisation |

---

## Itération 1 — Exploration du Workflow Core

### Questions Posées

| ID | Question | Réponse |
|----|----------|---------|
| Q1 | Format d'entrée du PRD ? | Feature Doc trop gros OU PRD complexe |
| Q2 | Détection des frontières ? | Sémantique (domaines fonctionnels) |
| Q3 | Organisation sortie ? | Dossier `docs/specs/{slug}/` |
| Q4 | Niveau des dépendances ? | Technique + Fonctionnel + Données |
| Q5 | Metadata des sous-specs ? | Minimum : tableau dépendances |
| Q6 | Mode de découpage ? | Top-down (analyse → plan → validation) |

### Risques Identifiés

- PRD mal structuré
- Dépendances circulaires
- Sur-découpage

### Challenge Coaching

> "Un sous-cahier = une session EPCI" — toujours vrai ?

**Réponse** : Oui, mais découpage récursif autorisé si sous-spec encore trop grosse.

### EMS Détail

```
Clarté       40/100
Profondeur   30/100 ⚠️
Couverture   28/100 ⚠️
Décisions    18/100 ⚠️
Actionnab.   20/100
```

---

## Itération 2 — Analyse du Cas Réel

### Documents Analysés

| Document | Lignes | Effort | Verdict |
|----------|--------|--------|---------|
| `migration_architecture_gardel.md` | 1738 | 25 jours | Trop complexe |
| `architecture_django_gardel_v2.md` | 920 | (référence) | — |
| CDC-F03 à F08 (exemples) | ~200 chacun | 2-5 jours | Bonne granularité |

### Découpage Proposé (Gardel)

| ID | Domaine | Effort | Dépendances |
|----|---------|--------|-------------|
| S01 | Settings Splitting | 1j | — |
| S02 | App Datawarehouse | 1j | S01 |
| S03 | Modèles Base | 2j | S02 |
| S04 | Modèles Analyses | 2j | S03 |
| S05 | Modèles Sources | 2j | S03 |
| S06 | Modèles Users | 2j | S03 |
| S07 | Admin + Services | 3j | S04,S05,S06 |
| S08 | Migration ETL | 2j | S07 |
| S09 | Tests + Docs | 2j | S08 |

### Patterns Détectés

1. **Phases séquentielles** : Le doc source a déjà une structure → la détecter
2. **Sous-découpage nécessaire** : Phase 2 = 10j → trop gros
3. **Parallélisation possible** : S04, S05, S06 en parallèle après S03
4. **Gates de validation** : Frontières naturelles

### EMS Détail

```
Clarté       75/100 (+35)
Profondeur   68/100 (+38) ✅
Couverture   55/100 (+27)
Décisions    38/100 (+20) ⚠️
Actionnab.   32/100 (+12) ⚠️
```

---

## Itération 3 — Workflow & Format de Sortie

### Workflow Défini

```
Phase A: Analyse
  └── Détection structure, dépendances, estimations

Phase B: Proposition
  └── Tableau + Mermaid + Breakpoint validation

Phase C: Génération
  └── INDEX.md + sous-specs
```

### Format INDEX.md

- Vue d'ensemble (tableau)
- Graphe dépendances (Mermaid flowchart)
- Planning Gantt (Mermaid gantt)
- Progression (statuts)

### Format Sous-Spec

- Header avec metadata (projet parent, ID, effort, dépendances)
- Contexte + source
- Périmètre (inclus/exclus)
- Tâches (checklist)
- Critères d'acceptation
- Référence source condensée

### Questions Ouvertes Résolues

| Question | Décision |
|----------|----------|
| Localisation fichiers | `docs/specs/{slug}/` |
| Mise à jour INDEX | Manuelle |
| Intégration `/epci-brief` | Aucune (autonome) |

### EMS Détail

```
Clarté       85/100 (+10)
Profondeur   78/100 (+10)
Couverture   68/100 (+13)
Décisions    65/100 (+27) ✅
Actionnab.   58/100 (+26) ✅
```

---

## Itération 4 — Signature Commande & Edge Cases

### Signature Finale

```
/epci-decompose <fichier.md> [--output <dir>] [--think <level>] [--min-days <n>] [--max-days <n>]
```

### Flags

| Flag | Défaut | Description |
|------|--------|-------------|
| `--output` | `docs/specs/{slug}/` | Dossier sortie |
| `--think` | `think` | Niveau réflexion |
| `--min-days` | `1` | Effort min/spec |
| `--max-days` | `5` | Effort max/spec |

### Edge Cases Définis

| EC | Situation | Comportement |
|----|-----------|--------------|
| EC1 | PRD sans structure | Proposition structuration d'abord |
| EC2 | PRD trop petit | Message → utiliser `/epci-brief` directement |
| EC3 | Sous-spec trop grosse | Suggestion sous-découpage |
| EC4 | Dépendance circulaire | Erreur + options résolution |
| EC5 | Estimations manquantes | Estimations par défaut + avertissement |

### Décision Retirée

- Flag `--dry-run` : Inutile (breakpoint suffit)

### EMS Détail

```
Clarté       92/100 (+7)
Profondeur   85/100 (+7)
Couverture   78/100 (+10)
Décisions    80/100 (+15) ✅
Actionnab.   75/100 (+17) ✅
```

---

## Itération 5 — Finalisation

### Ajustements Finaux

| Aspect | Ajustement |
|--------|------------|
| Flag `--think` | Ajouté (niveaux de réflexion) |
| PRD trop petit | Pas de découpage, redirection vers brief |
| Nom commande | Confirmé `/epci-decompose` |

### Niveaux de Pensée

| Niveau | Usage |
|--------|-------|
| `quick` | PRD bien structuré |
| `think` | Cas général (défaut) |
| `think-hard` | PRD complexe |
| `ultrathink` | Migration critique |

### EMS Final

```
Clarté       95/100 (+3)
Profondeur   88/100 (+3)
Couverture   85/100 (+7)
Décisions    88/100 (+8)
Actionnab.   82/100 (+7)
───────────────────────
Total        88/100
```

---

## Décisions Chronologiques

| # | Décision | Itération | Justification |
|---|----------|-----------|---------------|
| D1 | Format entrée = MD | I1 | Standard EPCI |
| D2 | Découpage sémantique | I1 | Plus intelligent que par headers |
| D3 | Sortie dans `docs/specs/` | I1 | Versionnable, visible |
| D4 | Granularité 1-5 jours | I2 | Aligné exemples F03-F08 |
| D5 | Breakpoint obligatoire | I3 | L'humain valide |
| D6 | INDEX.md avec Mermaid | I3 | Double vue tableau + graphique |
| D7 | Pas d'intégration brief | I3 | Commande autonome |
| D8 | Nom = `/epci-decompose` | I4 | Explicite |
| D9 | Retrait `--dry-run` | I4 | Redondant avec breakpoint |
| D10 | Ajout `--think` | I5 | Flexibilité analyse |

---

## Pivots & Réorientations

Aucun pivot majeur. L'exploration est restée focalisée sur le sujet initial.

**Ajustements mineurs :**
- I3 : Simplification de l'intégration (pas de `/epci-done`, pas de lien auto avec brief)
- I4 : Retrait du dry-run

---

## Sources Consultées

### Documents Utilisateur

| Document | Usage |
|----------|-------|
| `migration_architecture_gardel.md` | Cas d'exemple "trop complexe" |
| `architecture_django_gardel_v2.md` | Contexte architecture cible |
| `CDC-F03-Breakpoints-Enrichis.md` | Exemple bonne granularité |
| `CDC-F04-Project-Memory.md` | Exemple bonne granularité |
| `CDC-F05-Clarification-Intelligente.md` | Exemple bonne granularité |
| `CDC-F06-Suggestions-Proactives.md` | Exemple bonne granularité |
| `CDC-F08-Apprentissage-Continu.md` | Exemple bonne granularité |

### Historique Conversation

| Chat | Contenu |
|------|---------|
| Audit EPCI | Structure plugin, commandes existantes |
| Component Factory | Pattern création skills/commands |

---

## Livrables Générés

| Fichier | Description |
|---------|-------------|
| `brainstorm-epci-decompose-report.md` | Rapport de synthèse (ce qu'il faut pour implémenter) |
| `brainstorm-epci-decompose-journal.md` | Ce fichier (historique exploration) |

---

## Recommandations Post-Brainstorm

### Pour l'Implémentation

1. **Commencer par** : Parser de structure (headers, phases)
2. **Tester avec** : Le cas Gardel comme validation
3. **Prioriser** : Edge case EC2 (PRD trop petit) — c'est le plus fréquent

### Skill Bridges Suggérés

| Skill | Pertinence |
|-------|------------|
| `estimator` | Pourrait affiner les estimations automatiques |
| `skill-factory` | Si on veut packager decompose comme skill |

### Améliorations Futures (Hors Scope V1)

- Détection automatique des FK Django pour dépendances
- Intégration avec Project Memory pour historique découpage
- Export Notion de l'INDEX

---

## Statistiques Session

| Métrique | Valeur |
|----------|--------|
| Itérations | 5 |
| Questions posées | 18 |
| Décisions prises | 10 |
| Edge cases identifiés | 5 |
| Documents analysés | 7 |
| Lignes de spec analysées | ~3500 |
| Durée estimée session | ~45 min |

---

*Journal généré par Brainstormer v2.0.0*
*Session: epci-decompose — 18/12/2025*
