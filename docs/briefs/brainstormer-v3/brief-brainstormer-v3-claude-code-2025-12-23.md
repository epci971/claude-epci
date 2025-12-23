# Cahier des Charges — Brainstormer v3 Claude Code

> **Date** : 2025-12-23
> **Version cible** : 3.0.0
> **Basé sur** : Brainstormer Web v3.0 + Analyse contextuelle Claude Code

---

## 1. Contexte et Objectif

### 1.1 Situation Actuelle

Le skill Brainstormer actuel dans Claude Code (`src/skills/core/brainstormer/`) est une version allégée (~5K) du Brainstormer Web (~155K). Il manque de personnalité, de structure de processus créatif, et de frameworks d'analyse.

**Commande associée** : `/brainstorm` (`src/commands/brainstorm.md`)

### 1.2 Objectif

Créer un Brainstormer v3 spécifiquement adapté au contexte **développement logiciel** dans Claude Code, en intégrant les fonctionnalités à haute valeur ajoutée de la version Web tout en les adaptant au CLI et au workflow EPCI.

### 1.3 Critères de Succès

1. Skill < 5000 tokens (chargement rapide)
2. Commande `/brainstorm` cohérente avec l'écosystème EPCI
3. Intégration fluide avec `/epci-brief` (output compatible)
4. 3 personas adaptés au contexte dev
5. Phases Divergent/Convergent explicites
6. Pre-mortem comme framework clé
7. EMS avec ancres objectives simplifiées

---

## 2. Architecture Cible

### 2.1 Structure des Fichiers

```
src/
├── commands/
│   └── brainstorm.md              # Mise à jour (v3)
│
└── skills/
    └── core/
        └── brainstormer/
            ├── SKILL.md            # Refonte complète (v3)
            └── references/
                ├── brief-format.md # Conservé
                ├── ems-system.md   # Mise à jour (ancres objectives)
                ├── frameworks.md   # Mise à jour (+ pre-mortem)
                └── personas.md     # NOUVEAU
```

### 2.2 Dépendances Skills

| Skill | Usage |
|-------|-------|
| `project-memory-loader` | Charger contexte projet |
| `architecture-patterns` | Suggestions architecturales |
| `clarification-intelligente` | Système de questions (optionnel) |

### 2.3 Subagent

| Subagent | Usage |
|----------|-------|
| `@Explore` | Analyse codebase en Phase 1 |

---

## 3. Spécifications Fonctionnelles

### 3.1 Système de Personas (3 modes)

Simplification de la version Web (4 → 3 personas) pour le contexte dev.

| Persona | Icône | Philosophie | Quand l'activer |
|---------|-------|-------------|-----------------|
| **Architecte** | 📐 | Structurant, frameworks, synthèse (DÉFAUT) | Sujets complexes, synthèse |
| **Sparring** | 🥊 | Challenger, stress-test | Certitudes non étayées, pre-mortem |
| **Pragmatique** | 🛠️ | Action, débloquer | Stagnation, itération ≥ 5 |

**Bascule automatique** (règles simplifiées) :

| Contexte | Persona |
|----------|---------|
| Début session, sujet complexe | 📐 Architecte |
| Mots "évidemment", "forcément" | 🥊 Sparring |
| Pre-mortem déclenché | 🥊 Sparring |
| Stagnation EMS (< 5 pts / 2 iter) | 🛠️ Pragmatique |
| Itération ≥ 5 sans décision | 🛠️ Pragmatique |
| Phase Convergent | 📐 + 🛠️ |

**Commandes** :

| Commande | Action |
|----------|--------|
| `modes` | Afficher les 3 personas + état actuel |
| `mode [nom]` | Forcer un persona |
| `mode auto` | Retour à bascule automatique |

**Signalement** (début de message) :
```
📐 [Structure] Organisons ce qu'on a exploré...
🥊 [Challenge] Attends — qu'est-ce qui te fait dire ça ?
🛠️ [Action] Assez analysé. Quelle est la décision ?
```

### 3.2 Phases Divergent/Convergent

**Les 2 phases** :

| Phase | Icône | Comportement |
|-------|-------|--------------|
| **Divergent** | 🔀 | Générer, explorer, pas de jugement, quantité |
| **Convergent** | 🎯 | Évaluer, prioriser, décider, qualité |

**Affichage en header de breakpoint** :
```
-------------------------------------------------------
🔀 DIVERGENT | Iteration 3 | EMS: 58/100 (+12) 🌿
-------------------------------------------------------
```

**Transition automatique** :
- Start → 🔀 Divergent
- Couverture ≥ 60% ET iter ≥ 3 → Suggérer 🎯 Convergent
- `finish` → 🎯 Convergent

**Commandes** :

| Commande | Action |
|----------|--------|
| `diverge` | Forcer phase Divergent |
| `converge` | Forcer phase Convergent |

### 3.3 HMW (How Might We) — Simplifié

En phase d'initialisation, après validation du brief, générer **3 questions HMW** orientées développement :

```
💡 **Questions "How Might We"**

1. HMW [simplifier/automatiser] [processus actuel] sans [compromis] ?
2. HMW garantir [qualité/performance] même si [contrainte] ?
3. HMW permettre [fonctionnalité] dans [contexte difficile] ?

→ Laquelle on explore en premier ?
```

**Flag** : `--no-hmw` pour désactiver.

### 3.4 Pre-mortem Framework

**Nouveau framework critique pour le développement** :

```markdown
## ⚰️ Pre-mortem : [Feature]

**Projection** : Nous sommes dans 3 mois. L'implémentation a échoué.

### Causes d'échec identifiées

| # | Cause technique | Proba | Impact | Score |
|---|-----------------|-------|--------|-------|
| 1 | [Cause 1] | 🔴 Haute | 🔴 Critique | 9 |
| 2 | [Cause 2] | 🟡 Moyenne | 🔴 Critique | 6 |

### Mitigations préventives

| Cause | Mitigation | Qui | Quand |
|-------|------------|-----|-------|
| [Cause 1] | [Action] | Dev | Sprint 1 |

### Signaux d'alerte

- 🚨 [Signal 1] → [Action corrective]
```

**Déclencheur** : Commande `premortem`
**Persona activé** : 🥊 Sparring automatiquement

### 3.5 EMS v2 — Ancres Objectives Simplifiées

**Les 5 axes** (poids ajustés pour dev) :

| Axe | Poids | Question |
|-----|-------|----------|
| **Clarté** | 25% | Le besoin est-il bien défini ? |
| **Profondeur** | 20% | A-t-on creusé les détails techniques ? |
| **Couverture** | 20% | A-t-on exploré tous les angles ? |
| **Décisions** | 20% | A-t-on tranché les choix techniques ? |
| **Actionnabilité** | 15% | Peut-on implémenter avec ces infos ? |

**Ancres par axe (simplifiées)** :

| Score | Clarté | Profondeur | Décisions |
|-------|--------|------------|-----------|
| 20 | Sujet énoncé | Questions surface | Tout ouvert |
| 40 | Brief validé + scope | 1 "pourquoi" creusé | 1-2 orientations |
| 60 | + Contraintes (≥2) | Framework appliqué | Choix clés verrouillés |
| 80 | + Critères acceptation | Insights non-évidents | Priorisation faite |
| 100 | Zéro ambiguïté | Cause racine identifiée | Tous threads fermés |

**Recommandations phase-aware** :
- 🔀 Divergent → Focus Couverture, Profondeur
- 🎯 Convergent → Focus Décisions, Actionnabilité

### 3.6 Frameworks Retenus (5)

| Framework | Type | Usage | Commande |
|-----------|------|-------|----------|
| **5 Whys** | Analytique | Cause racine | `framework 5whys` |
| **MoSCoW** | Décision | Priorisation features | `framework moscow` |
| **SWOT** | Analytique | Évaluation options | `framework swot` |
| **Pre-mortem** | Risques | Anticipation échecs | `premortem` |
| **Scoring** | Décision | Évaluer/classer idées | `scoring` |

**Retirés** : Six Hats, Starbursting, Reverse, Weighted Criteria (trop "atelier créatif")

### 3.7 Biais Cognitifs (4 focus dev)

| Biais | Signal | Action |
|-------|--------|--------|
| **Over-engineering** | "Ajoutons X au cas où" | Suggérer MVP |
| **Scope creep** | Expansion continue | Rappeler focus initial |
| **Sunk cost** | "On a déjà fait X" | Challenger l'attachment |
| **Bikeshedding** | Focus sur détails triviaux | Recentrer sur critique |

**Règle** : Max 1 alerte par type par session.

### 3.8 Templates (3)

| Template | Usage | Auto-détection |
|----------|-------|----------------|
| **feature** | Nouvelle fonctionnalité | Mots : "ajouter", "créer", "implémenter" |
| **problem** | Bug, issue à résoudre | Mots : "bug", "erreur", "ne fonctionne pas" |
| **decision** | Choix technique | Mots : "choisir", "comparer", "entre X et Y" |

**Retirés** : audit, project, research, strategy (hors scope dev immédiat)

---

## 4. Workflow Détaillé

### 4.1 Phase 1 — Initialisation

```
1. Charger contexte projet (project-memory-loader)
2. Invoquer @Explore (medium) pour analyser codebase
3. Reformuler le besoin
4. Détecter template (feature/problem/decision)
5. Générer 3-5 questions de cadrage
6. Initialiser EMS ~25/100
7. Définir phase → 🔀 Divergent
8. Définir persona → 📐 Architecte
9. Générer HMW (si pas --no-hmw)
10. Afficher breakpoint compact
```

### 4.2 Phase 2 — Itérations

**Boucle jusqu'à `finish`** :

```
1. Intégrer réponses utilisateur
2. Mettre à jour EMS (5 axes)
3. Évaluer bascule persona (auto)
4. Évaluer transition phase
5. Détecter frameworks applicables
6. Détecter biais potentiels
7. Générer questions suivantes (3-5 max)
8. Afficher breakpoint compact
```

### 4.3 Phase 3 — Génération

```
1. Passer en phase 🎯 Convergent
2. Vérifier EMS ≥ 70 (sinon warning)
3. Proposer scoring si multiples idées
4. Générer brief fonctionnel (brief-format.md)
5. Générer journal d'exploration
6. Écrire fichiers dans ./docs/briefs/
7. Afficher résumé + EMS final
8. Suggérer commande EPCI suivante
```

### 4.4 Format Breakpoint (CLI optimisé)

```
-------------------------------------------------------
🔀 DIVERGENT | 📐 Architecte | Iter 3 | EMS: 58/100 (+12) 🌿
-------------------------------------------------------
Done: [Stack identifié: React+TypeScript, 3 endpoints définis]
Open: [Gestion d'erreurs, caching strategy]

Questions:
1. Pour le cache, Redis externe ou in-memory ? → Suggestion: Redis si multi-instance
2. Quelle stratégie de retry pour les appels API ?
3. Faut-il un fallback offline ?

-> continue | dive [topic] | premortem | modes | finish
-------------------------------------------------------
```

---

## 5. Commandes Utilisateur

### 5.1 Pendant Session

| Commande | Action |
|----------|--------|
| `continue` | Itération suivante |
| `dive [topic]` | Deep dive sur un point |
| `pivot` | Réorienter l'exploration |
| `diverge` | Forcer phase Divergent |
| `converge` | Forcer phase Convergent |
| `modes` | Afficher/changer persona |
| `mode [nom]` | Forcer un persona |
| `premortem` | Lancer exercice pre-mortem |
| `framework [name]` | Appliquer un framework |
| `scoring` | Évaluer les idées |
| `status` | EMS détaillé (radar) |
| `finish` | Générer les livrables |

### 5.2 Flags de Lancement

| Flag | Effet |
|------|-------|
| `--template [name]` | Forcer template (feature/problem/decision) |
| `--no-hmw` | Désactiver génération HMW |
| `--quick` | Mode rapide (3 iter max, EMS simplifié) |

---

## 6. Livrables

### 6.1 Brief Fonctionnel

**Fichier** : `./docs/briefs/brief-[slug]-[date].md`

**Structure** :
```markdown
# Brief — [Titre]

## Contexte
[Reformulation + stack + fichiers identifiés]

## Objectifs
[Objectifs SMART si possible]

## Spécifications
[Détails fonctionnels]

## Décisions Techniques
[Choix actés avec rationale]

## Risques & Mitigations
[Issu du pre-mortem si fait]

## Critères d'Acceptation
[Liste vérifiable]

## Hors Scope
[Explicite]

## EMS Final
[Score + radar simplifié]
```

### 6.2 Journal d'Exploration

**Fichier** : `./docs/briefs/journal-[slug]-[date].md`

**Structure** :
```markdown
# Journal — [Titre]

## Métadonnées
- Date: [date]
- Itérations: [N]
- EMS final: [score]
- Template: [type]

## Historique Itérations
[Résumé de chaque itération avec décisions]

## Progression EMS
[Graphe ASCII]

## Frameworks Appliqués
[Liste avec résultats]

## Points de Pivot
[Si applicable]
```

---

## 7. Intégration EPCI

### 7.1 Flux vers `/epci-brief`

Le brief généré par `/brainstorm` est **directement compatible** avec `/epci-brief` :
- Peut être passé en argument
- Ou copié dans la conversation

### 7.2 Synergie Pre-mortem

Les risques identifiés via pre-mortem alimentent :
- La section "Risques" du Feature Document EPCI
- L'estimation de contingence dans Estimator
- La section "Risques" dans Propositor

---

## 8. Migration

### 8.1 Fichiers à Modifier

| Fichier | Action |
|---------|--------|
| `src/commands/brainstorm.md` | Mise à jour workflow + commandes |
| `src/skills/core/brainstormer/SKILL.md` | Refonte complète |
| `src/skills/core/brainstormer/references/ems-system.md` | Ancres objectives |
| `src/skills/core/brainstormer/references/frameworks.md` | + pre-mortem |

### 8.2 Fichiers à Créer

| Fichier | Contenu |
|---------|---------|
| `src/skills/core/brainstormer/references/personas.md` | 3 personas + règles |

### 8.3 Rétrocompatibilité

- Commandes existantes (`continue`, `finish`, etc.) → Conservées
- Format breakpoint → Compatible (ajout phase/persona en header)
- Output briefs → Compatible avec workflow EPCI existant

---

## 9. Estimation Effort

| Tâche | Complexité | Estimation |
|-------|------------|------------|
| SKILL.md refonte | Moyenne | 2h |
| personas.md création | Simple | 1h |
| ems-system.md update | Simple | 30min |
| frameworks.md + pre-mortem | Simple | 30min |
| brainstorm.md update | Moyenne | 1h |
| Tests manuels | Simple | 1h |
| **Total** | | **~6h** |

---

## 10. Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| SKILL.md dépasse 5K tokens | Moyenne | Moyen | Déplacer détails dans references/ |
| Bascule persona confuse | Faible | Faible | Override manuel toujours disponible |
| Overhead cognitif (trop de commandes) | Faible | Moyen | Commandes optionnelles, défauts intelligents |

---

## 11. Critères de Validation

- [ ] SKILL.md < 5000 tokens
- [ ] `/brainstorm` fonctionne end-to-end
- [ ] 3 personas avec bascule auto testée
- [ ] Phases Divergent/Convergent affichées
- [ ] Pre-mortem génère output structuré
- [ ] EMS avec ancres objectives fonctionne
- [ ] Brief généré compatible `/epci-brief`
- [ ] Journal d'exploration créé
- [ ] Mode `--quick` fonctionne

---

*Cahier des charges généré le 2025-12-23*
*Basé sur l'analyse de Brainstormer Web v3.0 + contexte Claude Code*
