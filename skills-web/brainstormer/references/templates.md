# Templates — Configurations par Type d'Exploration

> Chaque template adapte le comportement de Brainstormer au type d'exploration

---

## Vue d'ensemble

Les templates pré-configurent Brainstormer pour différents types d'exploration. Chaque template définit :
- La structure du brief initial
- Les frameworks suggérés
- Le nombre d'itérations typique
- Les critères de succès par défaut
- Les questions HMW typiques

**Nouveaux templates v3.2** : `decision`, `problem`, `strategy`

---

## Catalogue des Templates

| Template | Type | Usage | Itérations typiques |
|----------|------|-------|---------------------|
| **feature** | Technique + Créatif | Nouvelle fonctionnalité, user story | 4-6 |
| **audit** | Analytique | Revue, diagnostic, évaluation | 3-5 |
| **project** | Business + Technique | Nouveau projet, initiative | 5-8 |
| **research** | Exploratoire | Veille, investigation, état de l'art | 4-7 |
| **decision** | Analytique | Choix binaire ou N options (NOUVEAU) | 2-4 |
| **problem** | Analytique | Quelque chose est cassé, trouver la cause (NOUVEAU) | 3-5 |
| **strategy** | Business + Créatif | Vision long terme, positionnement (NOUVEAU) | 5-8 |

---

## Template: Feature

**Usage** : Explorer et spécifier une nouvelle fonctionnalité, user story, ou amélioration produit.

**Type détecté** : Technique + Créatif

**Trigger phrases** :
- "Je veux ajouter une fonctionnalité..."
- "Comment implémenter..."
- "User story pour..."
- "Feature de sync/export/import..."

### Structure du Brief

```markdown
## Brief — Feature : [Nom]

**Contexte** : [Pourquoi cette feature est nécessaire]
**Utilisateurs cibles** : [Qui va l'utiliser]
**Problème résolu** : [Quel problème ça adresse]

**Périmètre** :
- ✅ Inclus : [Ce qui est dans le scope]
- ❌ Exclus : [Ce qui est hors scope]

**Contraintes** :
- [Contrainte technique 1]
- [Contrainte business 1]

**Critères de succès** :
- [ ] [Critère mesurable 1]
- [ ] [Critère mesurable 2]
```

### HMW Typiques

```markdown
💡 **Questions "How Might We"**

1. HMW permettre à [utilisateur] de [action] sans [friction] ?
2. HMW intégrer cette feature avec [système existant] de façon transparente ?
3. HMW garantir [critère qualité] même en cas de [condition limite] ?
4. HMW rendre l'utilisation intuitive pour [utilisateur novice] ?
5. HMW mesurer l'adoption et le succès de cette feature ?
```

### Frameworks suggérés

| Priorité | Framework | Moment |
|----------|-----------|--------|
| 🔴 Obligatoire | MoSCoW | Avant `finish` si fonctionnalités listées |
| 🟡 Recommandé | Scoring | Si 3+ variantes émergent |
| 🟢 Optionnel | Pre-mortem | Si feature critique |

### Itérations typiques

| Itération | Focus |
|-----------|-------|
| 1 | Comprendre le besoin, reformuler |
| 2 | Explorer les approches possibles |
| 3 | Approfondir l'approche choisie |
| 4 | Définir les specs, edge cases |
| 5 | Prioriser (MoSCoW), valider |
| 6 | Finaliser, risques, plan d'action |

---

## Template: Audit

**Usage** : Analyser, diagnostiquer, évaluer un existant (code, process, situation).

**Type détecté** : Analytique

**Trigger phrases** :
- "Revue de..."
- "Audit de..."
- "Diagnostic..."
- "Évaluer la qualité de..."
- "Analyser le code/process..."

### Structure du Brief

```markdown
## Brief — Audit : [Sujet]

**Périmètre audité** : [Ce qui est examiné]
**Objectif** : [Ce qu'on cherche à évaluer/améliorer]
**Sources disponibles** : [Documents, code, accès]

**Critères d'évaluation** :
- [Critère 1 avec échelle]
- [Critère 2 avec échelle]
- [Critère 3 avec échelle]

**Livrables attendus** :
- [ ] [Livrable 1]
- [ ] [Livrable 2]
```

### HMW Typiques

```markdown
💡 **Questions "How Might We"**

1. HMW identifier rapidement les 20% de problèmes causant 80% des impacts ?
2. HMW prioriser les améliorations par rapport coût/bénéfice ?
3. HMW créer un plan d'amélioration réaliste avec les ressources disponibles ?
4. HMW mesurer les gains de façon convaincante pour les stakeholders ?
5. HMW éviter que ces problèmes se reproduisent à l'avenir ?
```

### Frameworks suggérés

| Priorité | Framework | Moment |
|----------|-----------|--------|
| 🟡 Recommandé | Starbursting | Début pour couvrir tous les angles |
| 🟡 Recommandé | Scoring | Pour prioriser les findings |
| 🟢 Optionnel | SWOT | Pour synthétiser |

### Itérations typiques

| Itération | Focus |
|-----------|-------|
| 1 | Comprendre le périmètre, critères |
| 2 | Analyser les sources, identifier les patterns |
| 3 | Approfondir les problèmes majeurs |
| 4 | Prioriser les findings |
| 5 | Recommandations et plan d'action |

---

## Template: Project

**Usage** : Cadrer un nouveau projet, une initiative, une transformation.

**Type détecté** : Business + Technique

**Trigger phrases** :
- "Nouveau projet..."
- "Lancer une initiative..."
- "Monter un projet de..."
- "Cadrage projet..."

### Structure du Brief

```markdown
## Brief — Project : [Nom]

**Vision** : [En une phrase, à quoi ressemble le succès]
**Sponsor** : [Qui porte le projet]
**Budget indicatif** : [Enveloppe ou "à définir"]
**Timeline** : [Jalons clés ou deadline]

**Parties prenantes** :
- [Stakeholder 1] : [Rôle/Intérêt]
- [Stakeholder 2] : [Rôle/Intérêt]

**Objectifs** :
- [Objectif 1 — SMART si possible]
- [Objectif 2]

**Contraintes** :
- [Contrainte 1]
- [Contrainte 2]

**Risques identifiés** :
- [Risque 1]
- [Risque 2]
```

### HMW Typiques

```markdown
💡 **Questions "How Might We"**

1. HMW livrer de la valeur rapidement tout en construisant pour le long terme ?
2. HMW aligner toutes les parties prenantes sur une vision commune ?
3. HMW gérer les risques sans paralyser l'avancement ?
4. HMW mesurer le succès du projet de façon objective ?
5. HMW s'assurer que le projet reste pertinent si le contexte change ?
```

### Frameworks suggérés

| Priorité | Framework | Moment |
|----------|-----------|--------|
| 🔴 Obligatoire | Pre-mortem | Avant `finish` |
| 🟡 Recommandé | SWOT | Début de cadrage |
| 🟡 Recommandé | MoSCoW | Pour le scope |
| 🟢 Optionnel | Six Hats | Si sujet complexe |

### Itérations typiques

| Itération | Focus |
|-----------|-------|
| 1 | Comprendre la vision, les parties prenantes |
| 2 | Explorer les approches, contraintes |
| 3 | Définir le scope, prioriser |
| 4 | Identifier les risques |
| 5 | Pre-mortem, mitigations |
| 6-7 | Plan d'action, jalons |
| 8 | Validation finale, livrables |

---

## Template: Research

**Usage** : Exploration libre, veille, investigation sur un sujet.

**Type détecté** : Exploratoire

**Trigger phrases** :
- "Je veux explorer..."
- "Qu'est-ce que tu sais sur..."
- "État de l'art de..."
- "Recherche sur..."
- "Veille technologique..."

### Structure du Brief

```markdown
## Brief — Research : [Sujet]

**Question de recherche** : [Question principale à répondre]
**Contexte** : [Pourquoi cette recherche]
**Profondeur attendue** : [Surface / Intermédiaire / Expert]

**Axes d'exploration** :
- [Axe 1]
- [Axe 2]
- [Axe 3]

**Critères de succès** :
- [ ] Avoir une vision claire de [X]
- [ ] Identifier les [Y] principales options
- [ ] Pouvoir décider si [Z]
```

### HMW Typiques

```markdown
💡 **Questions "How Might We"**

1. HMW synthétiser les informations clés sans se perdre dans les détails ?
2. HMW identifier les sources les plus fiables et à jour ?
3. HMW distinguer ce qui est établi de ce qui est spéculatif ?
4. HMW appliquer ces learnings à notre contexte spécifique ?
5. HMW maintenir cette connaissance à jour dans le temps ?
```

### Frameworks suggérés

| Priorité | Framework | Moment |
|----------|-----------|--------|
| 🟡 Recommandé | Starbursting | Début pour cartographier le sujet |
| 🟡 Recommandé | Six Hats | Pour explorer sous tous les angles |
| 🟢 Optionnel | Scoring | Si comparaison de solutions |

### Itérations typiques

| Itération | Focus |
|-----------|-------|
| 1 | Cadrer la recherche, identifier les sources |
| 2 | Web search, collecte d'informations |
| 3 | Analyse, synthèse des findings |
| 4 | Deep dive sur points clés |
| 5-6 | Connexions, implications |
| 7 | Conclusions, recommandations |

---

## Template: Decision

**Usage** : Choix binaire (go/no-go) ou sélection parmi N options.

**Type détecté** : Analytique

**Trigger phrases** :
- "Je dois choisir entre..."
- "A ou B ?"
- "On fait ou on fait pas ?"
- "Quelle option..."
- "Arbitrer entre..."

### Structure du Brief

```markdown
## Brief — Decision : [Question]

**Décision à prendre** : [Formulation claire de la question]
**Deadline** : [Date limite pour décider]
**Décideur final** : [Qui tranche]

**Options identifiées** :
1. [Option A] — [Description courte]
2. [Option B] — [Description courte]
3. [Option C si applicable]

**Critères de décision** :
- [Critère 1] (poids: X%)
- [Critère 2] (poids: Y%)
- [Critère 3] (poids: Z%)

**Contraintes** :
- [Contrainte 1]
- [Contrainte 2]
```

### HMW Typiques

```markdown
💡 **Questions "How Might We"**

1. HMW prendre cette décision de façon objective et défendable ?
2. HMW minimiser les regrets quelle que soit l'option choisie ?
3. HMW garder de la flexibilité si le contexte change ?
4. HMW s'assurer qu'on n'a pas oublié une option ?
5. HMW valider cette décision avec les parties prenantes ?
```

### Frameworks suggérés

| Priorité | Framework | Moment |
|----------|-----------|--------|
| 🔴 Obligatoire | Weighted Criteria | Comparaison des options |
| 🟡 Recommandé | SWOT | Si 2 options (un SWOT par option) |
| 🟡 Recommandé | Pre-mortem | Sur l'option privilégiée |

### Itérations typiques

| Itération | Focus |
|-----------|-------|
| 1 | Clarifier la question, lister les options |
| 2 | Définir les critères, pondérer |
| 3 | Évaluer chaque option |
| 4 | Recommandation + Pre-mortem sur l'option choisie |

### Output spécifique

Le rapport pour `decision` inclut :
- Tableau comparatif des options
- Recommandation avec niveau de confiance (Haute/Moyenne/Faible)
- Risques de l'option choisie
- Plan B si l'option échoue

---

## Template: Problem

**Usage** : Quelque chose est cassé, ne fonctionne pas comme prévu. Trouver la cause et la solution.

**Type détecté** : Analytique

**Trigger phrases** :
- "Ça ne marche pas..."
- "Problème avec..."
- "Bug récurrent..."
- "On n'arrive pas à..."
- "Pourquoi ça échoue..."

### Structure du Brief

```markdown
## Brief — Problem : [Symptôme]

**Symptôme observé** : [Ce qu'on voit]
**Impact** : [Conséquences du problème]
**Depuis quand** : [Date d'apparition]
**Fréquence** : [Toujours / Parfois / Rare]

**Contexte** :
- [Ce qui a changé récemment]
- [Tentatives de résolution déjà faites]

**Critères de succès** :
- [ ] Cause racine identifiée
- [ ] Solution implémentable définie
- [ ] Plan de prévention établi
```

### HMW Typiques

```markdown
💡 **Questions "How Might We"**

1. HMW identifier la vraie cause plutôt que traiter les symptômes ?
2. HMW résoudre ce problème de façon durable ?
3. HMW éviter que ce problème se reproduise ?
4. HMW détecter ce problème plus tôt à l'avenir ?
5. HMW minimiser l'impact pendant qu'on cherche la solution ?
```

### Frameworks suggérés

| Priorité | Framework | Moment |
|----------|-----------|--------|
| 🔴 Obligatoire | 5 Whys | Pour trouver la cause racine |
| 🟡 Recommandé | Fishbone (implicite) | Pour structurer les causes possibles |
| 🟢 Optionnel | Scoring | Pour prioriser les solutions |

### Itérations typiques

| Itération | Focus |
|-----------|-------|
| 1 | Comprendre le symptôme, collecter les faits |
| 2 | 5 Whys — remonter à la cause racine |
| 3 | Valider la cause, explorer les solutions |
| 4 | Choisir la solution, définir le plan |
| 5 | Prévention, monitoring |

### Output spécifique

Le rapport pour `problem` inclut :
- Symptôme → Cause racine (chaîne des 5 Whys)
- Solution recommandée
- Plan d'implémentation
- Actions de prévention

---

## Template: Strategy

**Usage** : Vision long terme, positionnement, roadmap multi-années.

**Type détecté** : Business + Créatif

**Trigger phrases** :
- "Stratégie pour..."
- "Vision à 3 ans..."
- "Positionnement..."
- "Direction stratégique..."
- "Roadmap long terme..."

### Structure du Brief

```markdown
## Brief — Strategy : [Sujet]

**Horizon temporel** : [1 an / 3 ans / 5 ans]
**Contexte actuel** : [Situation de départ]
**Ambition** : [Où on veut être à l'horizon]

**Parties prenantes** :
- [Stakeholder 1] : [Intérêt]
- [Stakeholder 2] : [Intérêt]

**Contraintes stratégiques** :
- [Contrainte 1]
- [Contrainte 2]

**Questions clés** :
- [Question stratégique 1]
- [Question stratégique 2]
```

### HMW Typiques

```markdown
💡 **Questions "How Might We"**

1. HMW créer un avantage compétitif durable ?
2. HMW rester agiles face aux évolutions du marché ?
3. HMW aligner toute l'organisation sur cette vision ?
4. HMW mesurer notre progression vers la cible ?
5. HMW équilibrer court terme et long terme ?
```

### Frameworks suggérés

| Priorité | Framework | Moment |
|----------|-----------|--------|
| 🔴 Obligatoire | SWOT | Analyse de situation |
| 🔴 Obligatoire | Vision Statement | Définition de l'ambition |
| 🟡 Recommandé | Pre-mortem | Sur le plan stratégique |
| 🟢 Optionnel | Six Hats | Pour explorer les angles |

### Itérations typiques

| Itération | Focus |
|-----------|-------|
| 1 | Comprendre le contexte, l'ambition |
| 2 | SWOT de la situation actuelle |
| 3 | Vision cible, différenciation |
| 4 | Piliers stratégiques |
| 5 | Roadmap phasée |
| 6 | Pre-mortem, risques stratégiques |
| 7 | OKRs ou indicateurs de succès |
| 8 | Validation, communication |

### Output spécifique

Le rapport pour `strategy` inclut :
- Vision statement (1 phrase inspirante)
- SWOT de situation
- Piliers stratégiques (3-5 max)
- Roadmap phasée (année par année)
- Indicateurs de succès (OKRs ou KPIs)
- Risques stratégiques et mitigations

---

## Auto-détection du Template

Brainstormer suggère le template basé sur les mots-clés et le contexte :

| Mots-clés | Template suggéré |
|-----------|------------------|
| feature, fonctionnalité, user story, implémenter | `feature` |
| audit, revue, diagnostic, évaluer, analyser | `audit` |
| projet, initiative, lancer, cadrage | `project` |
| explorer, recherche, veille, état de l'art | `research` |
| choisir, décider, option, A ou B | `decision` |
| problème, bug, erreur, ne marche pas, pourquoi | `problem` |
| stratégie, vision, positionnement, long terme | `strategy` |

L'utilisateur peut toujours forcer un template avec `--template [nom]`.

---

## Comparatif des Templates

| Aspect | feature | audit | project | research | decision | problem | strategy |
|--------|---------|-------|---------|----------|----------|---------|----------|
| **Itérations** | 4-6 | 3-5 | 5-8 | 4-7 | 2-4 | 3-5 | 5-8 |
| **Focus** | Spécifier | Diagnostiquer | Cadrer | Explorer | Trancher | Résoudre | Visionner |
| **Framework obligatoire** | MoSCoW | - | Pre-mortem | - | Weighted | 5 Whys | SWOT |
| **Persona dominant** | 📐🛠️ | 📐 | 📐🛠️ | 🧒📐 | 🥊🛠️ | 📐🥊 | 🧒📐 |
| **Phase finale** | Convergent | Convergent | Convergent | Variable | Convergent | Convergent | Convergent |

---

*Templates v3.2 — Brainstormer v3.2*
