# Prompt Patterns — Génération par Type

> Patterns et templates pour générer des prompts Perplexity optimisés

---

## Les 5 Composants Perplexity

Chaque prompt généré DOIT intégrer ces 5 éléments :

| # | Composant | Description | Exemple |
|---|-----------|-------------|---------|
| 1 | **Instruction** | Verbe d'action clair | "Compare", "Analyse", "Identifie" |
| 2 | **Contexte** | Situation/domaine | "pour une application React en production" |
| 3 | **Input** | Données spécifiques | "entre Vitest et Jest" |
| 4 | **Mots-clés** | Termes techniques | "performance, DX, écosystème" |
| 5 | **Format** | Structure attendue | "Format tableau avec critères pondérés" |

---

## Enrichissements Automatiques

Ajouter systématiquement selon le contexte :

| Élément | Quand | Template |
|---------|-------|----------|
| **Temporalité** | Toujours si non précisé | "Sources 2024-2025" |
| **Critères** | Comparative, Décisionnelle | "Critères : [liste]" |
| **Format tableau** | Comparative | "Format tableau comparatif si possible" |
| **Sources variées** | Exploratoire | "Blogs techniques, docs officielles, REX" |
| **Données chiffrées** | Décisionnelle, Technique | "Avec métriques et benchmarks si disponibles" |

---

## Templates par Type

### Factuelle

```
Qu'est-ce que [SUJET] ? / Définition de [SUJET].
[Contexte si pertinent : domaine, pays, secteur].
Format : [définition concise | points clés | liste structurée].
```

**Exemple** :
```
Qu'est-ce que le pattern Repository en architecture logicielle ?
Définition, cas d'usage typiques, avantages et inconvénients.
Exemples d'implémentation en PHP/Symfony si possible.
Format : définition concise puis points clés.
```

---

### Exploratoire

```
État de l'art de [DOMAINE] en [ANNÉE].
Aspects à couvrir : [tendances, acteurs, technologies, défis].
[Scope géographique si pertinent : France, Europe, mondial].
Format : synthèse structurée par [thème | domaine d'application].
Sources récentes ([PÉRIODE]) uniquement.
```

**Exemple** :
```
État de l'art de l'edge computing en 2025.
Technologies dominantes, cas d'usage émergents, acteurs majeurs du marché.
Focus Europe et États-Unis.
Format : synthèse structurée par domaine d'application 
(IoT industriel, véhicules autonomes, retail, santé).
Sources récentes (2024-2025) uniquement, en français et anglais.
```

---

### Comparative

```
Comparaison de [OPTION A] et [OPTION B] [et OPTION C] pour [CONTEXTE].

Critères de comparaison :
- [Critère 1]
- [Critère 2]
- [Critère 3]
- [Critère 4]

Format : tableau comparatif avec verdict par critère et 
recommandation finale selon le contexte d'utilisation.
Sources récentes ([PÉRIODE]) privilégiées.
```

**Critères par domaine** :

| Domaine | Critères suggérés |
|---------|-------------------|
| **Frameworks JS** | Performance, expérience développeur, écosystème, SSR/SSG, support TypeScript, communauté |
| **Bases de données** | Performance, scalabilité, facilité d'administration, coût, requêtes complexes |
| **Fournisseurs cloud** | Tarification, services disponibles, régions, support, dépendance fournisseur |
| **Bibliothèques** | Taille du bundle, qualité de l'API, maintenance active, popularité, documentation |

---

### Procédurale

```
Guide pas-à-pas pour [ACTION] dans [CONTEXTE].
Prérequis nécessaires, [étapes clés à couvrir].
Focus : [stack technique / environnement spécifique].
Format : étapes numérotées [avec extraits de code si pertinent].
Sources : documentation officielle et tutoriels récents.
```

**Exemple** :
```
Guide pas-à-pas pour déployer une application Django sur Railway en 2025.
Prérequis, configuration du projet, variables d'environnement, 
connexion à la base de données PostgreSQL.
Focus : projet Django 5.x avec PostgreSQL.
Format : étapes numérotées avec commandes et fichiers de configuration.
Sources : documentation officielle Railway et articles récents.
```

---

### Décisionnelle

```
Analyse des avantages et inconvénients de [DÉCISION] en [ANNÉE].
Aspects à évaluer : [coût, risque, bénéfice, effort de mise en œuvre].
Retour sur investissement attendu vs risques identifiés.
Contexte : [situation actuelle de l'utilisateur].
Format : [tableau avantages/inconvénients | analyse structurée avec recommandation].
```

**Exemple** :
```
Analyse des avantages et inconvénients de passer de REST à GraphQL en 2025.
Impact sur : performance, expérience développeur, maintenance, 
courbe d'apprentissage de l'équipe.
Retour sur investissement attendu vs effort de migration.
Contexte : API REST existante avec plus de 50 endpoints.
Format : analyse structurée avec recommandation conditionnelle selon le contexte.
```

---

### Veille / Tendances

```
Synthèse des [nouveautés | actualités | évolutions] de [DOMAINE] sur [PÉRIODE].
Aspects à couvrir : [versions, fonctionnalités, changements majeurs].
Impact sur [contexte de l'utilisateur].
Sources : [types de sources privilégiées].
```

**Exemple** :
```
Synthèse des nouveautés React en 2024-2025.
Nouvelles versions, React Compiler, Server Components, nouveaux hooks.
Impact sur les projets React existants et recommandations de migration.
Sources : notes de version officielles, blogs de la core team, 
conférences React Conf et React Summit.
```

---

### Technique / API

```
[Spécifications | Tarification | Limites] de [PRODUIT/SERVICE] en [ANNÉE].
Aspects spécifiques à couvrir : [liste des informations recherchées].
Sources : [documentation officielle | source préférée].
Format : [liste structurée | tableau comparatif].
```

**Exemple** :
```
Tarification et limites de l'API OpenAI (GPT-4, GPT-4o) en janvier 2025.
Coût par token (entrée/sortie), limites de débit, taille de la fenêtre 
de contexte, quotas par niveau d'abonnement.
Sources : documentation officielle OpenAI.
Format : tableau comparatif par modèle avec tous les paramètres.
```

---

### Académique

```
Publications scientifiques revues par les pairs sur [SUJET].
Critères de sélection : [méthodologie, période, facteur d'impact].
Période : [ANNÉES].
Format : pour chaque étude, indiquer [auteurs, méthodologie, conclusions].
```

**Exemple** :
```
Publications scientifiques revues par les pairs sur l'efficacité 
du pair programming (programmation en binôme).
Études empiriques avec groupes de contrôle et mesures quantitatives.
Période : 2018-2025.
Format : pour chaque étude, indiquer auteurs, méthodologie, 
taille de l'échantillon et conclusions principales.
```

---

## Logique Multi-Prompts

### Règle générale

| Type | P1 | P2 | P3 |
|------|----|----|-----|
| Factuelle | Réponse directe 🔍 | Contexte élargi 🔍 | — |
| Exploratoire | État de l'art 🔬 | Acteurs clés 🔬 | Limites/Critiques 🔍 |
| Comparative | Multi-critères 🔬 | REX terrain 🔬 | Cas d'usage 🔍 |
| Procédurale | Guide pas-à-pas 🔍 | Pièges courants 🔍 | Alternatives 🔍 |
| Décisionnelle | Avantages/Inconvénients 🔬 | Études de cas 🔬 | Critères décision 🔍 |
| Veille | Synthèse récente 🔬 | Signaux faibles 🔬 | Prédictions 🔍 |
| Technique | Données factuelles 🔍 | Comparatif 🔍 | REX intégration 🔍 |
| Académique | Publications 🎓 | Méthodologies 🎓 | Débats 🔍 |

---

## Nettoyage Dictée Vocale

### Patterns à nettoyer

| Pattern | Action |
|---------|--------|
| "euh", "hum", "donc euh" | Supprimer |
| "je veux je veux" | Dédupliquer |
| "non en fait", "plutôt" | Garder dernière version |
| Ponctuation manquante | Reconstituer |

### Exemple

**Input brut** :
> "euh cherche moi des infos sur euh les tests e2e non en fait plutôt les tests d'intégration pour React"

**Nettoyé** :
> "Recherche sur les tests d'intégration pour React"

---

## Estimations de Temps

| Mode | Icône | Temps | Sources |
|------|-------|-------|---------|
| Standard | 🔍 | 30-60 sec | 5-10 |
| Deep Research | 🔬 | 3-5 min | 20-30 |
| Academic | 🎓 | 2-4 min | 10-20 |

---

## Suggestions de Follow-up par Type

| Type | Suggestions typiques |
|------|---------------------|
| **Factuelle** | "Des exemples concrets ?", "Quel historique ?", "Quelles alternatives ?" |
| **Exploratoire** | "Qui sont les acteurs majeurs ?", "Quelles controverses ?", "Quelles prédictions ?" |
| **Comparative** | "Retours d'expérience utilisateurs ?", "Dans quels cas [A] gagne ?", "Coût total de possession ?" |
| **Procédurale** | "Erreurs courantes à éviter ?", "Outils alternatifs ?", "Possibilité d'automatiser ?" |
| **Décisionnelle** | "Études de cas similaires ?", "Risques cachés ?", "Plan B si échec ?" |
| **Veille** | "Signaux faibles à surveiller ?", "Prédictions des experts ?", "Impact sur mon stack ?" |
| **Technique** | "Alternatives moins chères ?", "Limites non documentées ?", "Qualité du support ?" |
| **Académique** | "Méta-analyses disponibles ?", "Critiques méthodologiques ?", "Consensus actuel ?" |
