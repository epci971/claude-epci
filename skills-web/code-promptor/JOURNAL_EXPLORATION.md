# Journal d'Exploration — Code-Promptor v2.1

> **Session Brainstormer** : 31 décembre 2025
> **Durée** : ~45 minutes
> **Itérations** : 4 + 2 Dives + Pre-mortem
> **EMS Final** : 95/100 🌳

---

## 📊 Résumé exécutif

### Objectif initial
Faire évoluer le skill code-promptor pour :
1. Enchaîner plusieurs briefs sans contexte partagé (mode session)
2. Intégrer directement avec Notion (création automatique de tâches)
3. Détecter automatiquement les dictées multi-tâches

### Résultat
Cahier des charges complet pour code-promptor v2.1 incluant :
- Mode session avec cloisonnement total
- Détection multi-tâches agressive avec checkpoint validation
- 3 niveaux de complexité adaptatifs
- Sous-tâches auto-générées intelligemment
- Export Notion direct avec mapping Types

---

## 🔄 Progression des itérations

### Iteration 1 — Exploration initiale
**Phase** : 🔀 Divergent
**EMS** : 42/100

**Questions explorées** :
- Comment signaler la détection multi-tâches ?
- Format des sous-tâches (checklist, arborescence) ?
- Critères de classification de complexité ?
- Métadonnées Notion-ready ?

**Décisions prises** :
- ✅ Checkpoint validation avant génération multi-tâches
- ✅ Hybride checklist + arborescence pour sous-tâches
- ✅ Afficher le niveau de complexité détecté

**Idées rejetées** :
- ❌ Tags Notion générés (laissés à l'IA Notion)
- ❌ Option forcer mono-tâche (skill intelligent)

---

### Iteration 2 — Enrichissement utilisateur
**Phase** : 🔀 Divergent
**EMS** : 68/100 (+26)

**Apports utilisateur** :
- Auto-détection si plusieurs tâches dans une dictée
- Listing des tâches détectées → validation → génération
- Sous-tâches générées par le skill (pas dictées)
- Export direct vers Notion (comme notion-task-enricher)
- Projet défini à l'init session

**Analyse base Notion** :
- Propriétés identifiées : Nom, Description, Type, État, Temps estimé, Priorité, Difficulté, Étiquettes, Projet
- Mapping Types : Bloquant, Evolution, Tache, Backend, Frontend
- Propriétés IA Notion : Priorité, Difficulté, Étiquettes (non gérées par skill)

---

### Iteration 3 — Structuration
**Phase** : 🔀 Divergent
**EMS** : 82/100 (+14)

**Décisions finalisées** :

| Élément | Décision |
|---------|----------|
| Cache projet | Dans références du skill (pas partagé) |
| Checkpoint | Tableau + segments + commandes |
| Sous-tâches | Sans estimation temps |
| Temps estimé | Basé sur complexité (1h/4h/8h) |
| État initial | Géré par Notion (défaut "En attente") |
| Session sans projet | Optionnel |

---

### Iteration 4 — Pre-mortem
**Phase** : 🔀 Divergent → 🥊 Challenge
**EMS** : 88/100 (+6)

**Scénarios d'échec identifiés** :

| # | Scénario | Probabilité | Mitigation |
|---|----------|-------------|------------|
| 1 | Détection trop agressive | Moyenne | Commande `merge` |
| 2 | Détection trop passive | Moyenne | Marqueurs explicites |
| 3 | Checkpoint trop verbeux | Faible | Version compacte |
| 4 | Sous-tâches non pertinentes | Moyenne | Templates par type |
| 5 | Erreur Notion API | Faible | Afficher brief + retry |
| 6 | Oubli projet init | Faible | Rappel + set en cours |
| 7 | Cloisonnement trop strict | Faible | Commande `ref [n]` |

**Décisions pre-mortem** :
- ✅ Mode agressif (tend vers multi-tâches)
- ✅ Afficher brief si erreur Notion
- ✅ Plan adaptatif (Standard + Majeure)
- ✅ Commande `ref [n]` pour dépendances

---

### Dive 1 — Détection Multi-tâches
**Phase** : 🔀 Divergent (profondeur)
**EMS** : 90/100 (+2)

**Algorithme défini** :
1. Nettoyage dictée (garder marqueurs)
2. Segmentation sur marqueurs de rupture
3. Scoring par segment (sujet, action, domaine, marqueurs)
4. Décision : ≥ 2 segments avec score ≥ 40 → MULTI

**Marqueurs explicites** (+30 pts) :
- "aussi", "et puis", "autre chose", "ah et", "sinon"

**Marqueurs implicites** (+15-25 pts) :
- Changement sujet, domaine technique, verbe d'action

**Commandes checkpoint** :
- `ok`, `ok N,M`, `merge N,M`, `edit N "x"`, `drop N`, `split N`, `reanalyze`

**Edge cases résolus** :
- API + bouton frontend → 2 tâches (domaines différents)
- Tâche parent + enfants (":") → 1 tâche
- Liste de bugs → N tâches

---

### Dive 2 — Format de sortie
**Phase** : 🔀 Divergent (profondeur)
**EMS** : 93/100 (+3)

**3 formats définis** :

| Format | Critères | Temps | Plan |
|--------|----------|-------|------|
| Quick fix | < 50 mots, correctif | 1h | Non |
| Standard | 50-200 mots | 4h | Oui |
| Majeure | > 200 mots, complexe | 8h | Détaillé |

**Templates sous-tâches** :
- Par type : Backend API, Frontend Composant, Bug fix, Refacto
- Par stack : Symfony, Django, React

**Format checkpoint** :
- Tableau avec #, Titre, Type, Complexité, Temps
- Segments extraits affichés
- Commandes documentées

---

## 📈 Évolution EMS

```
Iteration 1    ████████░░░░░░░░░░░░ 42/100
Iteration 2    █████████████░░░░░░░ 68/100 (+26)
Iteration 3    ████████████████░░░░ 82/100 (+14)
Pre-mortem     █████████████████░░░ 88/100 (+6)
Dive Multi     ██████████████████░░ 90/100 (+2)
Dive Format    ██████████████████░░ 93/100 (+3)
Convergence    ███████████████████░ 95/100 (+2)
```

---

## 💡 Questions "How Might We" (début de session)

| HMW | Réponse |
|-----|---------|
| HMW simplifier le workflow dictée → Notion ? | Mode session + export auto |
| HMW adapter le niveau de détail selon contexte ? | 3 niveaux de complexité |
| HMW permettre catégorisation auto ? | Mapping Types Notion |
| HMW gérer dictées multi-tâches ? | Détection agressive + checkpoint |
| HMW rendre utile au-delà de Notion ? | Hors scope v2.1 (évolution future) |

---

## ✅ Décisions clés

### Validées par l'utilisateur

| Décision | Iteration | Justification |
|----------|-----------|---------------|
| Mode agressif multi-tâches | Pre-mortem | Préférence utilisateur, merge facile |
| Sous-tâches sans temps | Iteration 3 | Claude Code plus rapide que estimations |
| Plan adaptatif (Standard+) | Pre-mortem | Base de notes, évolutif en brainstorm |
| Commande `ref [n]` | Pre-mortem | Liens entre tâches utile |
| Export Notion auto | Iteration 2 | Workflow rapide |
| Propriétés IA Notion | Iteration 3 | Laisser Notion gérer Priorité/Difficulté/Étiquettes |

### Rejetées

| Décision | Iteration | Raison |
|----------|-----------|--------|
| Option forcer mono-tâche | Iteration 1 | Skill doit être intelligent |
| Tags générés par skill | Iteration 3 | IA Notion les génère |
| Estimation temps sous-tâches | Dive Format | Bruit inutile |

---

## 🏗️ Architecture décidée

```
code-promptor/
├── SKILL.md                          # Principal (~300 lignes)
├── config/
│   ├── notion-ids.md                 # IDs Notion
│   └── projects-cache.md             # Cache projets
├── references/
│   ├── output-format.md              # 3 formats de brief
│   ├── processing-rules.md           # Extraction (existant enrichi)
│   ├── multi-task-detection.md       # Algorithme détection
│   ├── subtask-templates.md          # Templates sous-tâches
│   ├── type-mapping.md               # Mapping → Types Notion
│   └── voice-cleaning.md             # Nettoyage vocal
└── templates/
    ├── brief-quickfix.md
    ├── brief-standard.md
    ├── brief-major.md
    └── checkpoint-format.md
```

---

## 🎯 Livrables produits

| Livrable | Statut |
|----------|--------|
| Cahier des charges complet | ✅ Généré |
| Journal d'exploration | ✅ Ce document |
| Skill code-promptor v2.1 | 🔜 À générer via skill-factory |

---

## 📝 Notes pour skill-factory

### Points d'attention pour la génération

1. **Description YAML** : Doit inclure "session", "batch", "multi-tâches", "Notion"
2. **Triggers** : "promptor session", "session promptor", "batch promptor"
3. **Références critiques** : multi-task-detection.md, output-format.md
4. **Intégration Notion** : Dépendance MCP, fallback si erreur
5. **Rétrocompatibilité** : Mode single (hors session) doit continuer à fonctionner

### Complexité estimée du skill

| Aspect | Niveau |
|--------|--------|
| SKILL.md | Avancé (~300 lignes) |
| Références | 6 fichiers |
| Templates | 4 fichiers |
| Config | 2 fichiers |
| **Total fichiers** | ~13 |

---

## 🔗 Chaînage suggéré

À la fin de la génération du skill, proposer :
- → `notion-task-enricher` si tâche simple (pas de brief complet)
- → `estimator` si besoin chiffrage client
- → `brainstormer` si feature complexe nécessite exploration

---

**Fin du journal d'exploration**

---

*Session Brainstormer terminée avec succès*
*EMS final : 95/100 🌳*
*Prêt pour génération via skill-factory*
