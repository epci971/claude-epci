# Taxonomy — Types de Recherche

> Classification des intentions de recherche pour Perplexitor

---

## Vue d'ensemble

8 types de recherche avec leurs indicateurs, mode Perplexity recommandé, et angles de génération.

---

## 1. Factuelle

**Intention** : Obtenir un fait précis, une définition, une valeur

### Indicateurs
- "c'est quoi", "qu'est-ce que"
- "combien", "quelle date", "quel prix"
- "qui est", "où se trouve"
- Questions courtes et précises

### Mode Perplexity
🔍 **Standard** — Réponse rapide suffit

### Angles de génération
| Priorité | Angle | Description |
|----------|-------|-------------|
| P1 | Réponse directe | Définition/fait avec contexte immédiat |
| P2 | Contexte élargi | Historique, évolution, origine |

### Exemple
**Input** : "C'est quoi le RGAA ?"

**P1** :
```
Qu'est-ce que le RGAA (Référentiel Général d'Amélioration de l'Accessibilité) ?
Définition officielle, version actuelle, champ d'application légal en France.
Obligations pour les sites publics et privés.
Format : définition concise puis points clés.
```

**P2** :
```
Historique et évolution du RGAA depuis sa création.
Versions successives, alignement avec les WCAG, comparaison avec les standards européens (EAA).
Sanctions en cas de non-conformité.
```

---

## 2. Exploratoire

**Intention** : Comprendre un domaine, cartographier un sujet large

### Indicateurs
- "parle-moi de", "qu'est-ce qu'on sait sur"
- Sujet large sans angle précis
- "état de l'art", "panorama"
- Absence de question spécifique

### Mode Perplexity
🔬 **Deep Research** — Nécessite synthèse multi-sources

### Angles de génération
| Priorité | Angle | Description |
|----------|-------|-------------|
| P1 | État de l'art | Vue d'ensemble complète du domaine |
| P2 | Acteurs clés | Leaders, entreprises, chercheurs |
| P3 | Limites/Controverses | Critiques, débats, zones d'ombre |

### Exemple
**Input** : "Les tendances IA en 2025"

**P1** :
```
État de l'art de l'intelligence artificielle en 2025.
Tendances majeures : grands modèles de langage (LLM), agents autonomes, 
IA multimodale, IA embarquée (edge AI).
Avancées significatives des 12 derniers mois.
Format : synthèse structurée par domaine avec exemples concrets.
Sources récentes (2024-2025) uniquement, en français et anglais.
```

---

## 3. Comparative

**Intention** : Comparer des options, évaluer des alternatives

### Indicateurs
- "vs", "versus", "ou"
- "différence entre", "comparer"
- "meilleur", "lequel choisir"
- Mention de 2+ options

### Mode Perplexity
🔬 **Deep Research** — Comparaison multi-critères

### Angles de génération
| Priorité | Angle | Description |
|----------|-------|-------------|
| P1 | Comparatif multi-critères | Tableau structuré avec verdict par critère |
| P2 | REX terrain | Retours d'expérience réels |
| P3 | Cas d'usage | Contextes où chaque option excelle |

### Enrichissement automatique
- Ajouter : "Critères : [pertinents au domaine]"
- Ajouter : "Format tableau comparatif si possible"
- Ajouter : "Sources 2024-2025"

### Exemple {#exemple-comparative}
**Input** : "Compare React et Vue pour un gros projet e-commerce"

**P1** :
```
Comparaison React vs Vue.js pour le développement d'une application 
e-commerce de grande envergure en 2025.

Critères de comparaison :
- Performance (rendu, taille du bundle, SSR/SSG)
- Écosystème (bibliothèques, outils, gestion d'état)
- Scalabilité (architecture, maintenabilité sur +100k lignes de code)
- Courbe d'apprentissage et facilité de recrutement
- Support entreprise et communauté

Format : tableau comparatif avec verdict par critère et 
recommandation finale selon le contexte.
Sources récentes (2024-2025) privilégiées.
```

---

## 4. Procédurale

**Intention** : Savoir comment faire quelque chose, étapes

### Indicateurs
- "comment", "comment faire"
- "étapes pour", "tuto", "guide"
- "mettre en place", "configurer", "installer"

### Mode Perplexity
🔍 **Standard** — Guide pas-à-pas

### Angles de génération
| Priorité | Angle | Description |
|----------|-------|-------------|
| P1 | Guide pas-à-pas | Étapes numérotées avec détails |
| P2 | Pièges courants | Erreurs à éviter, troubleshooting |
| P3 | Alternatives | Autres méthodes, outils complémentaires |

### Exemple
**Input** : "Comment configurer ESLint avec TypeScript"

**P1** :
```
Guide pas-à-pas pour configurer ESLint avec TypeScript en 2025.
Prérequis, installation des dépendances, configuration recommandée, 
intégration avec VS Code ou autre IDE.
Focus : projet React ou Node.js moderne.
Format : étapes numérotées avec extraits de code.
Sources : documentation officielle et articles récents.
```

---

## 5. Décisionnelle

**Intention** : Prendre une décision, évaluer une opportunité

### Indicateurs
- "dois-je", "faut-il"
- "vaut-il mieux", "est-ce une bonne idée"
- "quel choix", "quelle stratégie"
- Questions impliquant un jugement

### Mode Perplexity
🔬 **Deep Research** — Analyse approfondie requise

### Angles de génération
| Priorité | Angle | Description |
|----------|-------|-------------|
| P1 | Avantages/Inconvénients | Analyse équilibrée |
| P2 | Études de cas | REX concrets similaires |
| P3 | Framework de décision | Critères pour trancher |

### Exemple
**Input** : "Dois-je migrer vers Symfony 7 ?"

**P1** :
```
Analyse des avantages et inconvénients d'une migration vers Symfony 7 en 2025.
Nouvelles fonctionnalités, changements incompatibles (breaking changes), 
effort de migration estimé selon la taille du projet.
Retour sur investissement attendu vs risques.
Contexte : application Symfony 6.x en production.
Format : analyse structurée avec recommandation conditionnelle.
```

---

## 6. Veille / Tendances

**Intention** : Se tenir informé, suivre l'actualité d'un domaine

### Indicateurs
- "actualités", "news", "récent"
- "nouveautés", "dernières avancées"
- "évolutions", "changements"
- Mention de période récente

### Mode Perplexity
🔬 **Deep Research** — Synthèse temporelle

### Angles de génération
| Priorité | Angle | Description |
|----------|-------|-------------|
| P1 | Synthèse récente | Actualités des X derniers mois |
| P2 | Signaux faibles | Tendances émergentes |
| P3 | Prédictions | Analyses d'experts |

### Enrichissement automatique
- Ajouter période si non précisée : "6 derniers mois" ou "2024-2025"

### Exemple
**Input** : "Nouveautés Django 2024"

**P1** :
```
Synthèse des nouveautés et évolutions de Django en 2024.
Nouvelles versions sorties, fonctionnalités majeures, changements d'API.
Impact sur les projets Django existants et recommandations de mise à jour.
Sources : notes de version officielles, blogs de la core team, conférences DjangoCon.
```

---

## 7. Technique / API

**Intention** : Obtenir des specs, pricing, limites techniques

### Indicateurs
- Mention de produit/service spécifique
- "pricing", "tarif", "coût"
- "limites", "quotas", "rate limit"
- "specs", "spécifications", "documentation"

### Mode Perplexity
🔍 **Standard** — Données factuelles

### Angles de génération
| Priorité | Angle | Description |
|----------|-------|-------------|
| P1 | Données factuelles | Specs, pricing, limites |
| P2 | Comparatif alternatives | Options similaires |
| P3 | REX intégration | Retours sur qualité/support |

### Exemple
**Input** : "Limites API Notion"

**P1** :
```
Limites et quotas de l'API Notion en 2025.
Limitation de débit (rate limiting), taille maximale des requêtes, 
pagination, limites par endpoint et par type d'opération.
Différences selon les plans (gratuit, Plus, Business, Enterprise).
Sources : documentation officielle Notion.
```

---

## 8. Académique

**Intention** : Trouver des études, publications scientifiques

### Indicateurs
- "études", "recherches", "publications"
- "scientifique", "peer-reviewed"
- "consensus", "preuves", "evidence"
- Contexte universitaire/recherche

### Mode Perplexity
🎓 **Academic** — Sources scholarly uniquement

### Angles de génération
| Priorité | Angle | Description |
|----------|-------|-------------|
| P1 | Publications récentes | Études peer-reviewed |
| P2 | Méthodologies | Protocoles reconnus |
| P3 | Débats en cours | Consensus vs controverses |

### Exemple
**Input** : "Études sur l'impact du TDD"

**P1** :
```
Publications scientifiques revues par les pairs sur l'impact du 
Test-Driven Development (TDD).
Études empiriques mesurant : qualité du code, productivité des développeurs, 
maintenabilité à long terme.
Période : 2020-2025.
Format : pour chaque étude, indiquer auteurs, méthodologie, 
taille de l'échantillon et conclusions principales.
```

---

## Matrice de Sélection Rapide

| Si l'input contient... | Type | Mode |
|------------------------|------|------|
| "c'est quoi", "définition" | Factuelle | 🔍 |
| "parle-moi de", sujet large | Exploratoire | 🔬 |
| "vs", "comparer", "meilleur" | Comparative | 🔬 |
| "comment", "étapes", "tuto" | Procédurale | 🔍 |
| "dois-je", "faut-il" | Décisionnelle | 🔬 |
| "actualités", "nouveautés" | Veille | 🔬 |
| "pricing", "limites", "specs" | Technique | 🔍 |
| "études", "peer-reviewed" | Académique | 🎓 |
