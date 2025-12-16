# Cahier des Charges — Resumator v2.0.0

> Document de spécifications issu du brainstorming du 2025-12-16
> À utiliser comme entrée pour skill-factory

---

## 1. Contexte et Objectif

### Problème résolu
Transformer les transcriptions de réunions, articles et documents en comptes-rendus exhaustifs, enrichis et **proactifs** qui apportent de la valeur ajoutée au-delà du simple résumé.

### Évolution par rapport à v1.0.0
Le skill passe d'un outil de résumé "passif" à un **assistant de réunion proactif** qui :
- Détecte automatiquement les flux et génère des diagrammes Mermaid
- Propose des insights proactifs (suggestions, dette technique, idées)
- Extrait un glossaire technique automatique
- Produit un artifact `.md` téléchargeable

### Persona cible
Développeur fullstack, chef de projet technique, consultant IT qui :
- Participe à des réunions techniques fréquentes
- A besoin de documentation structurée pour ses projets
- Utilise Notion ou un système de `/docs` pour archiver

### Fréquence d'utilisation estimée
- Passé : 20+ réunions documentées avec v1.0.0
- Futur : 5-10 réunions/semaine

---

## 2. Triggers et Déclenchement

### Mots-clés déclencheurs
- "transcription"
- "compte-rendu" / "CR"
- "meeting" / "réunion"
- "résumé" / "summary"
- "CR proactif"
- "analyse ma réunion" / "analyze my meeting"

### Autres déclencheurs
- Long texte collé (>500 mots)
- URL d'article
- PDF/document uploadé

### Exclusions explicites (NOT for)
- Transcription audio → texte (traite uniquement le texte)
- Traduction de contenu
- Génération d'ordre du jour
- Contenu vidéo direct

---

## 3. Modes de Fonctionnement

### Mode 1 : Transcription de réunion (Principal)
- Détection automatique du type de réunion
- Application du plan correspondant
- Génération complète avec diagrammes et insights

### Mode 2 : Analyse d'URL (Secondaire)
- Fetch du contenu
- Résumé structuré
- Diagrammes si flux détectés

### Mode 3 : PDF/Document (Secondaire)
- Extraction du contenu
- Résumé structuré
- Diagrammes si flux détectés

---

## 4. Fonctionnalités Détaillées

### 4.1 Détection et Génération de Diagrammes Mermaid

**Comportement** :
- Détection automatique des flux évoqués dans le contenu
- Génération de diagrammes Mermaid appropriés
- Maximum 5-6 diagrammes par CR (priorisation si plus)
- Placement contextuel dans les sections + récapitulatif en fin

**Types de diagrammes supportés** :

| Pattern | Type Mermaid | Indicateurs |
|---------|--------------|-------------|
| Processus séquentiel | `flowchart TD/LR` | "workflow", "étapes", "processus", "d'abord...ensuite" |
| Échanges systèmes | `sequenceDiagram` | "API", "envoie à", "requête", "appel" |
| Structure données | `erDiagram` | "MCD", "table", "relation", "entité" |
| États/transitions | `stateDiagram-v2` | "statut", "état", "passe de X à Y" |
| Planning | `gantt` | "planning", "jalons", "phases" |
| Architecture objet | `classDiagram` | "classe", "service", "hérite" |
| Hiérarchie | `flowchart TD` | "contient", "composé de" |
| Décisions | `flowchart` + losanges | "si...alors", "condition" |

**Règles de complétion** :
- SI flux détecté mais infos incomplètes → compléter intelligemment avec connaissances du domaine
- TOUJOURS marquer les éléments complétés avec `⚠️ *Completed by skill*`
- Recherche web autorisée pour enrichir, marquée avec `🌐`

**Priorisation (si >6 détectés)** :
1. Diagrammes liés aux décisions prises
2. Diagrammes liés aux actions à mener
3. Architecture système
4. Processus métier
5. Autres

### 4.2 Insights Proactifs

**Catégories** :

#### 🔧 Suggestions d'amélioration
- Détecter processus manuels → suggérer automatisation
- Détecter échanges fichiers → suggérer intégration directe
- Détecter validations multiples → suggérer workflow

#### 🔶 Dette technique
Patterns à détecter :
- "pour l'instant", "solution temporaire", "on verra plus tard"
- "workaround", "en attendant", "quick fix"
- "ça marche mais c'est pas propre"

#### 💭 Idées évoquées
- Capturer les idées mentionnées mais non actionnées
- Attribuer à l'auteur si identifiable

#### 🌐 Enrichissements web
- Rechercher termes techniques inconnus
- Trouver best practices du domaine
- Toujours sourcer avec URL

### 4.3 Glossaire Automatique

**Catégories de termes** :
1. Acronymes (ETL, API, MCD...)
2. Termes techniques (DataFrame, orchestrateur...)
3. Outils/Librairies (Pandas, Django, OpenPyXL...)
4. Termes métier spécifiques au contexte

**Règles d'extraction** :
- Extraire si terme apparaît 2+ fois OU central au sujet
- Définition concise (1-2 phrases max)
- Contextualiser par rapport à la réunion si pertinent

### 4.4 Score de Complétude des Actions

**Indicateurs de statut** :

| Indicateur | Signification |
|------------|---------------|
| 🟢 | Responsable ET échéance définis |
| 🟡 | Responsable OU échéance (un manquant) |
| 🔴 | Ni responsable ni échéance |

**Affichage** :
```
📊 **Completeness Score**: X% of actions have both owner AND deadline
```

### 4.5 Suggestions Prochaine Réunion

- Basées sur les questions ouvertes
- Inclure vérifications d'actions
- Format checkbox pour suivi facile

### 4.6 Métadonnées YAML

```yaml
---
type: meeting-report
date: YYYY-MM-DD
project: [Nom du projet si identifiable]
participants: [Liste]
tags: [Tags extraits du contenu]
version: resumator-v2.0.0
---
```

### 4.7 Sortie Artifact

- Format : fichier `.md` téléchargeable
- Nommage : `CR_[YYYY-MM-DD]_[slug-from-object].md`
- Prêt pour Notion ou archivage `/docs`

---

## 5. Template de Sortie

### Sections (toutes obligatoires)

| # | Section | Description |
|---|---------|-------------|
| 0 | Métadonnées YAML | Type, date, projet, participants, tags |
| 1 | En-tête | Titre, Objet (<80 chars), Type, Participants, Durée |
| 2 | Synthèse exécutive | 3-5 points clés |
| 3 | Contexte | Cadre de la réunion, enjeux (3-6 phrases) |
| 4 | Points abordés | Couverture exhaustive avec diagrammes contextuels |
| 5 | Décisions prises | Liste claire et actionnable |
| 6 | Actions à mener | Tableau avec statut 🟢/🟡/🔴 + score |
| 7 | Diagrammes — Récap | Tous les diagrammes regroupés |
| 8 | Insights & Pistes | Suggestions, idées, dette, enrichissements |
| 9 | Points de vigilance | Risques, blocages, dépendances |
| 10 | Questions ouvertes | Éléments non résolus |
| 11 | Suggestions prochaine réunion | Basées sur questions ouvertes |
| 12 | Glossaire | Termes avec définitions |
| 13 | Verbatims clés | Citations marquantes |
| 14 | Footer | Info de génération |

### Gestion des sections vides
- NE PAS omettre les sections
- Afficher "[No items identified]" ou équivalent

---

## 6. Types de Réunions Supportés

1. **Steering/Decision** : décisions, validations, arbitrages
2. **Information** : updates, présentations, annonces
3. **Brainstorming** : idées, exploration, créativité
4. **Training/Workshop** : formation, ateliers, apprentissage
5. **Individual Review / 1:1** : feedback, objectifs, évaluation
6. **Technical/Architecture** : conception, workflows, API, BDD
7. **Generic** : fallback si pas de type clair

---

## 7. Règles Critiques (Hiérarchie)

### 🔴 CRITIQUES (jamais enfreindre)
1. **Exhaustivité des actions** : CHAQUE engagement doit apparaître
2. **Fidélité** : Ne jamais inventer d'information
3. **Marquage des enrichissements** : Toujours indiquer ce qui vient du skill
4. **Limite diagrammes** : Maximum 5-6
5. **Sortie artifact** : Toujours générer fichier `.md`
6. **Langue** : Répondre dans la langue du contenu source

### 🟡 IMPORTANTES
7. Placement contextuel des diagrammes
8. Cohérence inter-diagrammes
9. Score de complétude des actions
10. Glossaire exhaustif
11. Détection dette technique
12. Couverture détaillée du contenu

### 🟢 SOUHAITABLES
13. Suggestions prochaine réunion
14. Liens vers réunions précédentes
15. Enrichissement web
16. Verbatims clés

---

## 8. Options Utilisateur (sur demande uniquement)

| Option | Effet | Défaut |
|--------|-------|--------|
| `--no-diagrams` | Désactiver les diagrammes | Activé |
| `--concise` | Version allégée (synthèse + actions) | Complet |
| `--no-glossary` | Désactiver le glossaire | Activé |
| `--max-diagrams N` | Limiter le nombre de diagrammes | 6 |

---

## 9. Structure de Fichiers Attendue

```
resumator/
├── SKILL.md                         # Fichier principal
└── references/
    ├── output-template.md           # Template v2.0.0 complet
    ├── meeting-plans.md             # 7 plans de réunion
    ├── mermaid-detection.md         # Matrice de détection
    ├── proactive-rules.md           # Règles d'insights
    └── glossary-extraction.md       # Logique de glossaire
```

---

## 10. Critères de Succès

- [ ] CR généré contient tous les points substantifs de la transcription
- [ ] Diagrammes Mermaid pertinents générés automatiquement
- [ ] Insights proactifs utiles et non génériques
- [ ] Glossaire complet des termes techniques
- [ ] Score de complétude affiché pour les actions
- [ ] Artifact `.md` téléchargeable et prêt pour Notion
- [ ] Langue de sortie = langue du contenu source

---

## 11. Hors Périmètre Explicite

- ❌ Transcription audio → texte
- ❌ Traduction de contenu
- ❌ Génération d'ordre du jour (futur)
- ❌ Traitement vidéo direct
- ❌ Plus de 6 diagrammes par CR
- ❌ Génération de présentations à partir du CR

---

## 12. Version

**Skill** : resumator  
**Version cible** : 2.0.0  
**Date** : 2025-12-16  
**Auteur du CDC** : Brainstormer (EMS 82/100, 4 itérations)

---

*Ce cahier des charges est prêt à être consommé par skill-factory pour générer le skill complet.*
