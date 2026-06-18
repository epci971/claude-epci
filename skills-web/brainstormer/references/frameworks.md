# Frameworks Catalog

> Outils de réflexion structurée pour enrichir le brainstorming

---

## Vue d'ensemble

Les frameworks sont des méthodes de pensée structurée que Brainstormer peut appliquer pour approfondir l'exploration. Ils sont suggérés proactivement ou activés sur demande.

---

## Catalogue des Frameworks

| Framework | Type | Quand l'utiliser | Commande |
|-----------|------|------------------|----------|
| **SWOT** | Analytique | Évaluer une option, un projet, une décision | `framework swot` |
| **5 Whys** | Analytique | Trouver la cause racine d'un problème | `framework 5whys` |
| **MoSCoW** | Décision | Prioriser des fonctionnalités ou tâches | `framework moscow` |
| **Six Hats** | Exploration | Explorer un sujet sous tous les angles | `framework hats` |
| **Pre-mortem** | Risques | Anticiper les causes d'échec | `premortem` |
| **Weighted Criteria** | Décision | Comparer des options avec critères pondérés | `framework weighted` |
| **Scoring** | Décision | Évaluer et classer des idées | `scoring` |
| **Starbursting** | Exploration | Générer des questions (Who/What/Where/When/Why/How) | `framework starbursting` |
| **Reverse Brainstorming** | Créatif | Trouver des solutions en inversant le problème | `framework reverse` |

---

## SWOT Analysis

**Purpose** : Évaluer les Forces, Faiblesses, Opportunités et Menaces d'une option.

**Quand l'utiliser** :
- Évaluer un projet avant de s'engager
- Comparer 2 options stratégiques
- Faire un état des lieux d'une situation

**Process** :
1. Identifier les **S**trengths (forces internes)
2. Identifier les **W**eaknesses (faiblesses internes)
3. Identifier les **O**pportunities (opportunités externes)
4. Identifier les **T**hreats (menaces externes)
5. Croiser les quadrants pour définir des stratégies

**Format de sortie** :

```markdown
## SWOT : [Sujet]

|  | Positif | Négatif |
|--|---------|---------|
| **Interne** | **Forces** | **Faiblesses** |
|  | • Force 1 | • Faiblesse 1 |
|  | • Force 2 | • Faiblesse 2 |
| **Externe** | **Opportunités** | **Menaces** |
|  | • Opportunité 1 | • Menace 1 |
|  | • Opportunité 2 | • Menace 2 |

### Stratégies croisées
- **S+O** : [Exploiter les forces pour saisir les opportunités]
- **W+O** : [Améliorer les faiblesses via les opportunités]
- **S+T** : [Utiliser les forces pour contrer les menaces]
- **W+T** : [Plan défensif pour éviter le pire scénario]
```

**Best for** : Templates `project`, `strategy`, `decision`

---

## 5 Whys

**Purpose** : Remonter à la cause racine d'un problème en demandant "pourquoi" de manière itérative.

**Quand l'utiliser** :
- Un problème récurrent qu'on n'arrive pas à résoudre
- Symptômes visibles mais cause floue
- Besoin de comprendre le "vrai" problème

**Process** :
1. Énoncer le problème clairement
2. Demander "Pourquoi ?" et noter la réponse
3. Répéter 5 fois (ou jusqu'à la cause racine)
4. Valider la cause racine trouvée
5. Définir une action sur la cause racine

**Format de sortie** :

```markdown
## 5 Whys : [Problème initial]

**Problème** : [Énoncé du problème]

1. **Pourquoi ?** → [Réponse 1]
2. **Pourquoi ?** → [Réponse 2]
3. **Pourquoi ?** → [Réponse 3]
4. **Pourquoi ?** → [Réponse 4]
5. **Pourquoi ?** → [Réponse 5]

🎯 **Cause racine identifiée** : [Cause racine]

**Action corrective** : [Action sur la cause racine]
```

**Best for** : Templates `problem`, `audit`

---

## MoSCoW Prioritization

**Purpose** : Classer les éléments par priorité en 4 catégories.

**Quand l'utiliser** :
- Liste de fonctionnalités à prioriser
- Scope trop large à réduire
- Besoin de distinguer l'essentiel du nice-to-have

**Catégories** :
- **M**ust have : Indispensable, bloquant si absent
- **S**hould have : Important mais pas bloquant
- **C**ould have : Nice-to-have, si temps/budget
- **W**on't have : Hors scope pour cette itération

**Format de sortie** :

```markdown
## MoSCoW : [Sujet]

### 🔴 Must Have (Indispensable)
- [ ] Élément 1
- [ ] Élément 2

### 🟠 Should Have (Important)
- [ ] Élément 3
- [ ] Élément 4

### 🟡 Could Have (Nice-to-have)
- [ ] Élément 5
- [ ] Élément 6

### ⚪ Won't Have (Hors scope)
- [ ] Élément 7
- [ ] Élément 8

**Rationale** : [Justification des choix de priorisation]
```

**Règle** : MoSCoW doit être appliqué avant `finish` si le template est `feature` et que des fonctionnalités ont été listées.

**Best for** : Templates `feature`, `project`

---

## Six Thinking Hats

**Purpose** : Explorer un sujet sous 6 angles différents pour garantir une vision complète.

**Quand l'utiliser** :
- Sujet complexe avec multiples perspectives
- Besoin de sortir d'un mode de pensée unique
- Équilibrer émotion, faits, créativité, critique

**Les 6 chapeaux** :
- 🎩 **Blanc** : Faits, données, informations objectives
- 🎩 **Rouge** : Émotions, intuitions, réactions viscérales
- 🎩 **Noir** : Critique, risques, points négatifs
- 🎩 **Jaune** : Optimisme, bénéfices, points positifs
- 🎩 **Vert** : Créativité, alternatives, nouvelles idées
- 🎩 **Bleu** : Méta, processus, synthèse

**Format de sortie** :

```markdown
## Six Hats : [Sujet]

### 🎩 Chapeau Blanc — Faits
- [Données objectives]
- [Informations vérifiables]

### 🎩 Chapeau Rouge — Émotions
- [Réactions émotionnelles]
- [Intuitions]

### 🎩 Chapeau Noir — Critique
- [Risques]
- [Points négatifs]
- [Obstacles]

### 🎩 Chapeau Jaune — Optimisme
- [Bénéfices]
- [Opportunités]
- [Points positifs]

### 🎩 Chapeau Vert — Créativité
- [Alternatives]
- [Idées nouvelles]
- [Approches différentes]

### 🎩 Chapeau Bleu — Synthèse
- [Conclusions]
- [Prochaines étapes]
- [Décisions]
```

**Best for** : Templates `project`, `strategy`, `decision`

---

## Pre-mortem

**Purpose** : Anticiper les causes d'échec en imaginant que le projet a échoué, puis définir des mitigations préventives.

**Quand l'utiliser** :
- Avant de finaliser un plan d'action
- Pour des projets à risque élevé (budget important, deadline serrée, nouveau domaine)
- Quand le client demande des garanties
- En complément de l'analyse de risques classique

**Différence avec l'analyse de risques classique** :
- Analyse de risques : "Quels sont les risques possibles ?"
- Pre-mortem : "Le projet a échoué. Qu'est-ce qui s'est passé ?"

La projection dans l'échec libère la pensée et permet d'identifier des risques qu'on n'oserait pas mentionner autrement.

**Process** :
1. **Projection** : "Nous sommes dans [6 mois/1 an]. Le projet a complètement échoué."
2. **Identification** : "Qu'est-ce qui s'est passé ? Listez toutes les causes possibles."
3. **Priorisation** : Classer les causes par Probabilité × Impact
4. **Mitigation** : Pour chaque cause majeure, définir une action préventive
5. **Intégration** : Ajouter les mitigations au plan d'action

**Format de sortie** :

```markdown
## ⚰️ Pre-mortem : [Sujet]

**Projection** : Nous sommes le [date future]. Le projet [nom] a échoué.

### Causes d'échec identifiées

| # | Cause | Probabilité | Impact | Score |
|---|-------|-------------|--------|-------|
| 1 | [Cause 1] | 🔴 Haute | 🔴 Critique | 9 |
| 2 | [Cause 2] | 🟡 Moyenne | 🔴 Critique | 6 |
| 3 | [Cause 3] | 🟡 Moyenne | 🟡 Modéré | 4 |
| 4 | [Cause 4] | 🟢 Faible | 🟡 Modéré | 2 |

### Plan de mitigation

| Cause | Mitigation préventive | Owner | Deadline |
|-------|----------------------|-------|----------|
| [Cause 1] | [Action préventive] | [Qui] | [Quand] |
| [Cause 2] | [Action préventive] | [Qui] | [Quand] |

### Signaux d'alerte à surveiller

- 🚨 [Signal 1] → Déclenche [action corrective]
- 🚨 [Signal 2] → Déclenche [action corrective]
```

**Scoring Probabilité × Impact** :
- 🔴 Haute/Critique = 3
- 🟡 Moyenne/Modéré = 2
- 🟢 Faible/Mineur = 1
- Score = Probabilité × Impact (max 9)

**Lien avec autres skills** :
- Les mitigations alimentent la section "Risques" de **Propositor**
- Les actions préventives peuvent être chiffrées par **Estimator**

**Best for** : Templates `project`, `feature`, `strategy`

**Déclenchement** : Commande `premortem` — Active automatiquement le persona 🥊 Sparring

---

## Weighted Criteria Grid

**Purpose** : Comparer des options avec des critères pondérés pour une décision objective.

**Quand l'utiliser** :
- Choix entre plusieurs options équivalentes
- Besoin de justifier une décision de manière rationnelle
- Multiples critères à considérer

**Process** :
1. Lister les options à comparer
2. Définir les critères de comparaison
3. Pondérer les critères (total = 100%)
4. Noter chaque option sur chaque critère (1-5)
5. Calculer le score pondéré
6. Identifier le gagnant

**Format de sortie** :

```markdown
## Weighted Criteria : [Décision]

### Critères et pondération

| Critère | Poids | Description |
|---------|-------|-------------|
| [Critère 1] | 30% | [Description] |
| [Critère 2] | 25% | [Description] |
| [Critère 3] | 25% | [Description] |
| [Critère 4] | 20% | [Description] |

### Évaluation

| Option | Critère 1 | Critère 2 | Critère 3 | Critère 4 | **Score** |
|--------|-----------|-----------|-----------|-----------|-----------|
| Option A | 4 (1.2) | 3 (0.75) | 5 (1.25) | 2 (0.4) | **3.60** |
| Option B | 3 (0.9) | 5 (1.25) | 3 (0.75) | 4 (0.8) | **3.70** ✅ |
| Option C | 5 (1.5) | 2 (0.5) | 4 (1.0) | 3 (0.6) | **3.60** |

### Recommandation

🎯 **Option B** avec un score de 3.70/5

**Rationale** : [Justification qualitative au-delà du score]
```

**Best for** : Templates `decision`, `feature`, `strategy`

---

## Scoring (Ideas Evaluation)

**Purpose** : Évaluer et classer des idées sur des critères standards.

**Critères par défaut** :
- **Impact** : Effet potentiel si implémenté (1-5)
- **Effort** : Ressources nécessaires (1-5, inversé)
- **Risk** : Niveau de risque (1-5, inversé)
- **Alignment** : Cohérence avec les objectifs (1-5)

**Formule** :
```
Score = (Impact × 0.35) + ((6-Effort) × 0.25) + ((6-Risk) × 0.20) + (Alignment × 0.20)
```

**Format de sortie** :

```markdown
## Scoring : [Sujet]

| Idée | Impact | Effort | Risk | Align. | **Score** |
|------|--------|--------|------|--------|-----------|
| Idée 1 | 5 | 2 | 2 | 4 | **4.15** ✅ |
| Idée 2 | 4 | 4 | 3 | 5 | **3.45** |
| Idée 3 | 3 | 3 | 1 | 3 | **3.60** |

### Top 3

1. 🥇 **Idée 1** (4.15) — [Raison]
2. 🥈 **Idée 3** (3.60) — [Raison]
3. 🥉 **Idée 2** (3.45) — [Raison]
```

**Déclenchement** : Commande `scoring` — Proposé automatiquement si 3+ idées ont émergé

---

## Starbursting

**Purpose** : Générer des questions exhaustives autour d'un sujet avec les 6 interrogatifs.

**Quand l'utiliser** :
- Début d'exploration pour couvrir tous les angles
- Vérifier qu'on n'a rien oublié
- Préparer un brief ou une spécification

**Les 6 branches** :
- **Who** : Qui est concerné ?
- **What** : Qu'est-ce que c'est exactement ?
- **Where** : Où ça se passe ?
- **When** : Quand ça arrive ?
- **Why** : Pourquoi c'est important ?
- **How** : Comment ça fonctionne ?

**Format de sortie** :

```markdown
## Starbursting : [Sujet]

### 👤 Who (Qui)
- Qui utilise ça ?
- Qui décide ?
- Qui est impacté ?

### 📦 What (Quoi)
- C'est quoi exactement ?
- Ça inclut quoi ?
- Ça exclut quoi ?

### 📍 Where (Où)
- Où ça se passe ?
- Où c'est déployé ?
- Où sont les utilisateurs ?

### 📅 When (Quand)
- Quand c'est utilisé ?
- Quelle est la deadline ?
- Quelle fréquence ?

### ❓ Why (Pourquoi)
- Pourquoi c'est nécessaire ?
- Pourquoi maintenant ?
- Pourquoi cette approche ?

### ⚙️ How (Comment)
- Comment ça fonctionne ?
- Comment on mesure le succès ?
- Comment on implémente ?
```

**Best for** : Templates `audit`, `project`

---

## Reverse Brainstorming

**Purpose** : Trouver des solutions en inversant le problème ("Comment empirer ?").

**Quand l'utiliser** :
- Blocage créatif, pas d'idées
- Besoin de voir le problème autrement
- Identifier des risques cachés

**Process** :
1. Inverser le problème : "Comment faire pour que ça échoue ?"
2. Lister toutes les façons de créer le problème
3. Inverser chaque réponse pour trouver des solutions
4. Évaluer et retenir les meilleures

**Format de sortie** :

```markdown
## Reverse Brainstorming : [Problème]

**Problème original** : [Énoncé]
**Problème inversé** : "Comment s'assurer que [problème] arrive ?"

### Façons de créer le problème

| # | Comment empirer | Inversion → Solution |
|---|-----------------|---------------------|
| 1 | [Façon d'empirer 1] | [Solution 1] |
| 2 | [Façon d'empirer 2] | [Solution 2] |
| 3 | [Façon d'empirer 3] | [Solution 3] |

### Solutions retenues

1. **[Solution 1]** — [Justification]
2. **[Solution 2]** — [Justification]
```

**Best for** : Templates `problem`, `feature`

---

## Suggestions Automatiques

Brainstormer suggère proactivement les frameworks selon le contexte :

| Contexte | Framework suggéré |
|----------|-------------------|
| Multiples options à comparer | Weighted Criteria, Scoring |
| Problème récurrent | 5 Whys |
| Projet à risque | Pre-mortem |
| Liste de fonctionnalités | MoSCoW |
| Sujet complexe, multifacette | Six Hats |
| Blocage créatif | Reverse Brainstorming |
| Début d'exploration | Starbursting |
| Évaluation stratégique | SWOT |

---

*Frameworks Catalog v3.2 — Brainstormer v3.2*
