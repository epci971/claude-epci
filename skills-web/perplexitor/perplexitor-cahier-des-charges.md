# Cahier des Charges — Skill Perplexitor

## Métadonnées

| Champ | Valeur |
|-------|--------|
| **Nom** | `perplexitor` |
| **Version cible** | 1.0.0 |
| **Auteur** | Édouard |
| **Date** | 2025-01-23 |
| **Source** | Brainstorming session EMS 88/100 |

---

## 1. Vue d'ensemble

### 1.1 Description

Perplexitor transforme une demande de recherche floue (y compris dictée vocale) en 2-3 prompts Perplexity optimisés, prêts à copier-coller. Le skill détecte automatiquement l'intention de recherche, choisit le mode Perplexity approprié (🔍 Standard / 🔬 Deep Research / 🎓 Academic), et propose des angles d'attaque complémentaires.

### 1.2 Philosophie

- **Standalone** : Skill autonome, pas d'intégration avec d'autres skills
- **Neutre** : Pas d'enrichissement basé sur le profil utilisateur
- **Frictionless** : Plus rapide que de réfléchir soi-même au prompt
- **Best effort** : Toujours produire un résultat, même avec peu d'informations

### 1.3 Proposition de Valeur

| Sans Perplexitor | Avec Perplexitor |
|------------------|------------------|
| "Je cherche des trucs sur les tests e2e" | Prompt structuré avec critères, temporalité, format |
| Oubli du mode Deep Research | Sélection automatique du bon mode |
| Un seul angle de recherche | 2-3 angles complémentaires |
| Dictée vocale = prompt brut | Nettoyage + reformulation |

---

## 2. Spécifications Fonctionnelles

### 2.1 Déclenchement

**Mode** : Détection automatique d'intention de recherche

#### Signaux d'activation

| Catégorie | Patterns | Confiance |
|-----------|----------|-----------|
| **Explicites** | "recherche", "cherche", "trouve", "infos sur", "renseigne-toi" | Haute |
| **Interrogatifs** | "c'est quoi", "qu'est-ce que", "comment", "pourquoi", "qui est" | Moyenne |
| **Comparatifs** | "vs", "versus", "différence entre", "comparer", "meilleur" | Haute |
| **Exploratoires** | "parle-moi de", "état de l'art", "tendances", "actualités" | Haute |
| **Décisionnels** | "dois-je", "faut-il", "vaut-il mieux", "quel choix" | Moyenne |

#### Règle de non-activation

Si Claude peut répondre directement avec ses connaissances ET que l'utilisateur ne demande pas explicitement une recherche → Ne pas activer le skill.

### 2.2 Pipeline de Traitement

```
┌─────────────────────────────────────────────────────────────┐
│  INPUT: Demande floue (texte ou dictée)                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: Analyse & Classification                           │
│  ├─ Nettoyage (hésitations, répétitions si dictée)          │
│  ├─ Extraction d'intention (taxonomie 8 types)              │
│  ├─ Détection du domaine/contexte                           │
│  └─ Score de clarté (0-100)                                 │
└─────────────────────────────────────────────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
┌──────────────────────┐      ┌──────────────────────┐
│  Score clarté ≥ 60   │      │  Score clarté < 60   │
│  → Mode EXPRESS      │      │  → Mode GUIDÉ        │
│  Génération directe  │      │  Question + P1       │
└──────────────────────┘      └──────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: Enrichissement                                     │
│  ├─ Expansion sémantique (termes liés, synonymes)           │
│  ├─ Contextualisation (temporalité, secteur, région)        │
│  ├─ Sélection du mode Perplexity (🔍/🔬/🎓)                 │
│  └─ Choix des angles d'attaque (2-3 perspectives)           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 3: Génération                                         │
│  ├─ Application des 5 composants Perplexity                 │
│  ├─ Structuration (framework CLEAR si pertinent)            │
│  └─ Tri par pertinence estimée                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT: 2-3 prompts triés par pertinence                    │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Taxonomie des Types de Recherche

| Type | Indicateurs | Mode Perplexity | Angles générés |
|------|-------------|-----------------|----------------|
| **Factuelle** | "c'est quoi", "combien", "quelle date" | 🔍 Standard | Définition + Contexte élargi |
| **Exploratoire** | "parle-moi de", sujet large | 🔬 Deep | État de l'art + Acteurs + Limites |
| **Comparative** | "vs", "différence", "meilleur" | 🔬 Deep | Multi-critères + REX + Cas d'usage |
| **Procédurale** | "comment", "étapes pour", "tuto" | 🔍 Standard | Guide + Pièges + Alternatives |
| **Décisionnelle** | "dois-je", "vaut-il mieux" | 🔬 Deep | Avantages/Inconvénients + REX + Critères |
| **Veille/Tendances** | "actualités", "récent", "nouveautés" | 🔬 Deep | Synthèse récente + Signaux faibles |
| **Technique/API** | specs, pricing, limites | 🔍 Standard | Données factuelles + Comparatif |
| **Académique** | études, publications, consensus | 🎓 Academic | Sources peer-reviewed + Méthodologies |

### 2.4 Mode Guidé — Questions de Clarification

#### Seuil de déclenchement

Score de clarté < 60

#### Banque de questions contextuelles

| Ambiguïté détectée | Question |
|--------------------|----------|
| **Temporalité floue** | "Tu cherches des infos récentes (2024-2025) ou un historique plus large ?" |
| **Scope trop large** | "Tu veux une vue d'ensemble ou un aspect précis de [sujet] ?" |
| **Intention incertaine** | "Tu cherches à comprendre, comparer, ou décider quelque chose ?" |
| **Contexte manquant** | "C'est pour quel contexte : perso, pro, technique, académique ?" |
| **Niveau de détail** | "Tu veux des données chiffrées/sources ou une synthèse générale ?" |

#### Règles du Mode Guidé

1. **Maximum 1 question composite** (jamais d'interrogatoire)
2. **Toujours générer P1 en parallèle** (best effort)
3. **Proposer de continuer sans répondre** : "Tu peux aussi taper `go` pour que je génère avec ce que j'ai compris"

### 2.5 Les 5 Composants Perplexity (Systématiques)

Chaque prompt généré doit intégrer :

| Composant | Description | Exemple |
|-----------|-------------|---------|
| **1. Instruction** | Verbe d'action clair | "Compare", "Analyse", "Identifie" |
| **2. Contexte** | Situation/domaine | "pour une application React en production" |
| **3. Input** | Données spécifiques | "entre Vitest et Jest" |
| **4. Mots-clés** | Termes techniques | "performance, DX, écosystème" |
| **5. Format** | Structure attendue | "Format tableau avec critères pondérés" |

---

## 3. Format de Sortie

### 3.1 Structure Hiérarchique

```markdown
## 🔎 Perplexitor

**Demande** : [reformulation nettoyée]
**Type** : [Factuelle | Exploratoire | Comparative | ...]
**Clarté** : [Score]/100

---

### 🎯 P1 — [Angle principal] 🔬 Deep Research

```
[Prompt optimisé - GROS, VISIBLE, COPIABLE]
```

⏱️ ~3-5 min | 📊 20-30 sources

---

### P2 — [Angle alternatif] 🔍 Standard

```
[Prompt optimisé]
```

⏱️ ~30-60 sec | 📊 5-10 sources

---

### P3 — [Angle complémentaire] 🔍 Standard

```
[Prompt optimisé]
```

⏱️ ~30-60 sec | 📊 5-10 sources

---

**💡 Pourquoi ces choix ?**

- **P1** en Deep Research car [justification basée sur le type détecté]
- **P2** couvre l'angle [X] souvent négligé dans ce type de recherche
- **P3** permet de [bénéfice spécifique]

**🔄 Pour aller plus loin**

- "[Suggestion follow-up 1]"
- "[Suggestion follow-up 2]"
- "[Suggestion follow-up 3]"
```

### 3.2 Hiérarchie Visuelle

- **P1 = Hero** : Le plus visible, le plus gros, immédiatement copiable
- **P2, P3** : Présents mais visuellement secondaires
- **Justifications** : En fin, pour ceux qui veulent comprendre
- **Follow-ups** : Suggestions pour approfondir

### 3.3 Estimations de Temps

| Mode | Temps estimé | Sources attendues |
|------|--------------|-------------------|
| 🔍 Standard | 30-60 secondes | 5-10 |
| 🔬 Deep Research | 3-5 minutes | 20-30 |
| 🎓 Academic | 2-4 minutes | 10-20 (peer-reviewed) |

---

## 4. Logique de Génération Multi-Prompts

### 4.1 Règles par Type

```
Si Type = Factuelle
  → P1: Réponse directe avec contexte (🔍)
  → P2: Historique / évolution du sujet (🔍)

Si Type = Exploratoire
  → P1: État de l'art complet (🔬)
  → P2: Acteurs clés / leaders du domaine (🔬)
  → P3: Controverses / limites / critiques (🔍)

Si Type = Comparative
  → P1: Comparatif multi-critères structuré (🔬)
  → P2: Retours d'expérience terrain (🔬)
  → P3: Cas d'usage spécifiques / contextes (🔍)

Si Type = Procédurale
  → P1: Guide pas-à-pas détaillé (🔍)
  → P2: Pièges courants / erreurs à éviter (🔍)
  → P3: Outils / alternatives complémentaires (🔍)

Si Type = Décisionnelle
  → P1: Analyse avantages / inconvénients (🔬)
  → P2: Études de cas / REX concrets (🔬)
  → P3: Framework de décision / critères (🔍)

Si Type = Veille/Tendances
  → P1: Synthèse actualités récentes (🔬)
  → P2: Signaux faibles / émergents (🔬)
  → P3: Prédictions analystes / experts (🔍)

Si Type = Technique/API
  → P1: Specs / pricing / limites factuelles (🔍)
  → P2: Comparatif alternatives (🔍)
  → P3: REX intégration / qualité doc (🔍)

Si Type = Académique
  → P1: Publications peer-reviewed récentes (🎓)
  → P2: Méthodologies / protocoles reconnus (🎓)
  → P3: Consensus vs débats en cours (🔍)
```

### 4.2 Enrichissement Systématique

Pour chaque prompt, ajouter automatiquement :

| Élément | Quand l'ajouter | Exemple |
|---------|-----------------|---------|
| **Temporalité** | Toujours si non précisé | "Sources 2024-2025" |
| **Critères** | Type Comparative ou Décisionnelle | "Critères : performance, coût, maintenance" |
| **Format tableau** | Type Comparative | "Format tableau comparatif si possible" |
| **Sources variées** | Type Exploratoire | "Blogs techniques, docs officielles, REX" |
| **Données chiffrées** | Type Décisionnelle ou Technique | "Avec métriques et benchmarks si disponibles" |

---

## 5. Gestion des Cas Limites

### 5.1 Dictée Vocale — Nettoyage

| Pattern à nettoyer | Action |
|--------------------|--------|
| Hésitations ("euh", "hum", "donc euh") | Supprimer |
| Répétitions ("je veux je veux") | Dédupliquer |
| Faux départs ("non en fait", "plutôt") | Garder la dernière version |
| Ponctuations manquantes | Reconstituer |

### 5.2 Demande Trop Vague

**Seuil** : Score clarté < 30

**Comportement** :
1. Générer P1 best effort quand même
2. Poser 1 question composite
3. Indiquer clairement : "Ma compréhension est limitée, le P1 ci-dessus est une approximation"

### 5.3 Demande Hors Scope

Si la demande n'est clairement pas une recherche (ex: "écris-moi un email") :
- Ne pas activer le skill
- Laisser Claude répondre normalement

### 5.4 Skip / Best Effort

Si l'utilisateur ne répond pas aux questions de clarification ou tape "go", "continue", "génère" :
- Utiliser les informations disponibles
- Générer les prompts avec la meilleure interprétation possible
- Mentionner les hypothèses faites

---

## 6. Exemples d'Usage

### 6.1 Exemple Express (Clarté ≥ 60)

**Input** :
> "Compare React et Vue pour un gros projet e-commerce"

**Output** :

```markdown
## 🔎 Perplexitor

**Demande** : Comparaison React vs Vue pour projet e-commerce de grande envergure
**Type** : Comparative
**Clarté** : 78/100

---

### 🎯 P1 — Comparatif multi-critères 🔬 Deep Research

```
Compare React et Vue.js pour le développement d'une application 
e-commerce large scale en 2025.

Critères de comparaison :
- Performance (rendu, bundle size, SSR)
- Écosystème (librairies, outils, state management)
- Scalabilité (architecture, maintenabilité code base 100k+ LOC)
- Courbe d'apprentissage et recrutement
- Support entreprise et communauté

Format : Tableau comparatif avec verdict par critère et 
recommandation finale selon le contexte.
Sources récentes (2024-2025) privilégiées.
```

⏱️ ~3-5 min | 📊 20-30 sources

---

### P2 — Retours d'expérience terrain 🔬 Deep Research

```
Retours d'expérience d'entreprises ayant migré ou choisi 
entre React et Vue pour leur plateforme e-commerce.

Recherche : études de cas, témoignages tech leads, post-mortems.
Focus : défis rencontrés, regrets, facteurs de succès.
Exemples concrets avec taille d'équipe et complexité projet.
```

⏱️ ~3-5 min | 📊 20-30 sources

---

### P3 — Cas d'usage spécifiques e-commerce 🔍 Standard

```
Quelles fonctionnalités e-commerce spécifiques (panier, checkout, 
catalogue produits, recherche) sont mieux supportées par React 
ou Vue ? Librairies dédiées, intégrations headless CMS/commerce.
```

⏱️ ~30-60 sec | 📊 5-10 sources

---

**💡 Pourquoi ces choix ?**

- **P1** en Deep Research car une comparaison complète nécessite de croiser de nombreuses sources et critères
- **P2** couvre l'angle REX souvent plus utile que les comparatifs théoriques
- **P3** permet de zoomer sur les aspects spécifiques au e-commerce

**🔄 Pour aller plus loin**

- "Quels sites e-commerce majeurs utilisent React vs Vue ?"
- "Comment migrer de Vue 2 à React progressivement ?"
- "Coût total de possession React vs Vue sur 3 ans"
```

### 6.2 Exemple Guidé (Clarté < 60)

**Input** :
> "cherche moi des trucs sur les tests"

**Output** :

```markdown
## 🔎 Perplexitor

**Demande** : Recherche sur les tests (domaine non précisé)
**Type** : Exploratoire (incertain)
**Clarté** : 35/100

---

### 🎯 P1 — Best effort (tests logiciels) 🔬 Deep Research

```
État de l'art des pratiques de tests logiciels en 2025.
Types de tests (unitaires, intégration, E2E, performance), 
outils populaires, tendances (AI-assisted testing, shift-left).
Focus développement web/applications.
```

⏱️ ~3-5 min | 📊 20-30 sources

---

**❓ Pour affiner** :

Tu parles de quel type de tests ?
- **Tests logiciels** (unitaires, E2E, intégration) → le P1 ci-dessus est adapté
- **Tests médicaux / cliniques** → je reformule
- **Tests A/B / UX** → je reformule
- **Autre chose** → précise-moi

Tu peux aussi taper `go` pour continuer avec mon interprétation (tests logiciels).
```

---

## 7. Critères de Succès du Skill

| Critère | Mesure | Cible |
|---------|--------|-------|
| **Rapidité perçue** | Temps avant P1 copiable | < 5 secondes |
| **Pertinence P1** | % de fois où P1 est utilisé tel quel | > 70% |
| **Valeur ajoutée** | Prompt généré ≠ ce que l'utilisateur aurait écrit | Toujours |
| **Friction Mode Guidé** | Abandon après question | < 10% |
| **Choix de mode correct** | 🔍/🔬/🎓 approprié au besoin | > 85% |

---

## 8. Évolutions Futures (v1.1+)

| Feature | Description | Priorité |
|---------|-------------|----------|
| **Historique** | Mémoriser les recherches précédentes pour éviter doublons | Moyenne |
| **Feedback loop** | "Ce prompt a bien marché" → amélioration patterns | Basse |
| **Multi-langue** | Support EN natif pour recherches internationales | Moyenne |
| **Export Notion** | Sauvegarder les prompts générés dans une DB Notion | Basse |

---

## 9. Références Techniques

### 9.1 Patterns Perplexity (à maintenir à jour)

- Guide officiel : https://www.perplexity.ai/help-center
- Modes disponibles : Quick Search, Pro Search, Academic Focus, Deep Research, Labs
- Limites : contexte, rate limiting selon plan

### 9.2 Sources du Brainstorming

- Taxonomie Rose & Levinson (2004) : 6 sous-types informationnels
- Taxonomie Broder (2002) : Informational / Navigational / Transactional
- Modèle Taylor (1968) : 4 niveaux de besoin informationnel
- Framework CLEAR : Contexte, Langage, Exemples, Action, Résultat

---

## 10. Checklist Skill-Factory

Éléments requis pour la création du skill :

- [x] Nom : `perplexitor`
- [x] Description courte et longue
- [x] Déclencheurs (patterns de détection)
- [x] Pipeline de traitement
- [x] Taxonomie des types
- [x] Format de sortie
- [x] Exemples d'usage
- [x] Gestion des cas limites
- [x] Critères de succès
- [ ] Tests de validation (à créer par skill-factory)
- [ ] Fichier SKILL.md (à générer par skill-factory)

---

*Document généré le 2025-01-23 via Brainstormer v3.1*
*EMS final : 88/100 🌳*
