# Configuration Notion

> Configuration complète pour l'intégration Notion de code-promptor

---

## Architecture

```
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│      BASE PROJETS               │       │      BASE TÂCHES                │
│  (recherche de projet)          │◄──────│  (création des tâches)          │
│                                 │       │                                 │
│  • Gardel-DataWareHouse         │       │  Tâche 1 → Projet: Gardel       │
│  • EPCI-Workflow-IADD           │       │  Tâche 2 → Projet: Gardel       │
│  • StBarth-202511               │       │  Tâche 3 → Projet: EPCI         │
│  • toDo (Inbox)                 │       │  Tâche 4 → Projet: toDo         │
└─────────────────────────────────┘       └─────────────────────────────────┘
```

---

## Base de données Tâches

> C'est ici que les tâches sont CRÉÉES

```yaml
database_id: "12e6c54939df80049226dc6215904a74"
database_url: "https://www.notion.so/12e6c54939df80049226dc6215904a74"
data_source_id: "12e6c549-39df-80ab-a332-000bd7bad408"
```

---

## Base de données Projets

> C'est ici qu'on RECHERCHE les projets (on ne crée pas dedans)

```yaml
database_id: "12e6c54939df8099834bd8d9d717b8ca"
database_url: "https://www.notion.so/12e6c54939df8099834bd8d9d717b8ca"
data_source_id: "12e6c549-39df-80ba-884e-000b1a258661"
```

---

## Projet par défaut (Inbox)

> Utilisé quand aucun projet n'est spécifié

```yaml
page_id: "15a6c54939df801781eee12c65031315"
page_url: "https://www.notion.so/15a6c54939df801781eee12c65031315"
name: "toDo"
```

---

## Mapping des propriétés Tâches

| Propriété skill | Propriété Notion | Type | Format |
|-----------------|------------------|------|--------|
| titre | `Nom` | title | string |
| description | `Description` | text | Markdown |
| projet | `Projet` | relation | JSON array d'URLs |
| priorite | `Priorité` | select | Basse\|Moyenne\|Haute\|Critique |
| duree | `Temps estimé` | number | float (heures) |
| echeance | `Échéance` | date | ISO-8601 |
| etat | `État` | status | voir valeurs ci-dessous |
| type | `Type` | multi_select | JSON array |
| difficulte | `Difficulté` | select | Facile\|Moyenne\|Difficile\|Très difficile |
| module | `Module` | multi_select | JSON array |
| tags | `Étiquettes` | multi_select | JSON array |
| jour | `DAY` | multi_select | JSON array |
| moment | `MOMENT` | multi_select | JSON array |

---

## Propriétés remplies par Promptor

| Propriété | Source | Valeur par défaut |
|-----------|--------|-------------------|
| `Nom` | Titre du brief | - |
| `Description` | Contenu markdown | - |
| `Projet` | Session init ou défaut | toDo |
| `Temps estimé` | Complexité (1/4/8) | 4 |
| `État` | Fixe | "En attente" |
| `Type` | Auto-détecté | "Tache" |
| `DAY` | Fixe | "BACKLOG" |

## Propriétés laissées à Notion AI

- Priorité
- Difficulté
- Module
- Étiquettes
- Résumé

---

## Valeurs des selects

### Priorité

| Valeur | Couleur | Usage |
|--------|---------|-------|
| Basse | vert | Tâches non urgentes |
| Moyenne | jaune | Standard |
| Haute | rouge | Urgent |
| Critique | gris | Bloquant immédiat |

### État (groupés)

**To-do** :
- `A planifier`
- `A affecter`
- `En attente` ← **défaut pour nouvelles tâches**
- `À lire`
- `À analyser`

**In progress** :
- `En cours`
- `En pause`
- `Attente élément`
- `Retour interne`
- `Retour client`

**Complete** :
- `Attente validation`
- `A facturer`
- `Terminé`
- `Annulé`
- `Refusé`
- `Archivé`

### Type

| Value | Detection Keywords |
|-------|-------------------|
| Tache | (default) |
| Ticket Interne | ticket interne |
| Ticket Client | client, ticket client |
| Support | support, assistance |
| Réunion | réunion, meeting |
| Formation | formation, training |
| Evolution | créer, ajouter, feature |
| Bloquant | bug, fixer, corriger |
| Tache interne | interne |
| Backend | API, service, BDD |
| Frontend | UI, composant, React |

### Difficulté

```
Facile, Moyenne, Difficile, Très difficile
```

### Module

```
Design & rédaction, Setup & DevOps,
Développement Backend, Développement Front,
Contenus & SEO, Qualité & conformité,
Mise en production & post-livraison
```

### DAY

```
BACKLOG, LUNDI, MARDI, MERCREDI, JEUDI, VENDREDI, SAMEDI, DIMANCHE
```

### MOMENT

```
MATIN, APRES-MIDI, SOIREE
```

---

## Exemples de création

### Tâche simple avec projet

```javascript
// notion-create-pages
{
  "parent": {
    "data_source_id": "12e6c549-39df-80ab-a332-000bd7bad408"
  },
  "pages": [{
    "properties": {
      "Nom": "Implémenter l'export PDF des rapports",
      "Temps estimé": 4,
      "État": "En attente",
      "Type": "[\"Evolution\"]",
      "DAY": "[\"BACKLOG\"]",
      "Projet": "[\"https://www.notion.so/27e6c54939df80caab49d5f4ba40009f\"]"
    },
    "content": "## Objectif\n\nPermettre l'export PDF...\n\n## Plan d'implémentation\n- [ ] Créer service\n- [ ] Ajouter endpoint"
  }]
}
```

### Tâche bug (Bloquant)

```javascript
{
  "parent": {
    "data_source_id": "12e6c549-39df-80ab-a332-000bd7bad408"
  },
  "pages": [{
    "properties": {
      "Nom": "Corriger le bug d'affichage des dates",
      "Temps estimé": 1,
      "État": "En attente",
      "Type": "[\"Bloquant\"]",
      "DAY": "[\"BACKLOG\"]",
      "Projet": "[\"https://www.notion.so/27e6c54939df80caab49d5f4ba40009f\"]"
    },
    "content": "## Objectif\n\nCorriger l'affichage...\n\n## Correction attendue\n- Identifier le composant\n- Appliquer le fix"
  }]
}
```

### Tâche sans projet (défaut toDo)

```javascript
{
  "parent": {
    "data_source_id": "12e6c549-39df-80ab-a332-000bd7bad408"
  },
  "pages": [{
    "properties": {
      "Nom": "Tâche à trier",
      "Temps estimé": 4,
      "État": "En attente",
      "Type": "[\"Tache\"]",
      "DAY": "[\"BACKLOG\"]",
      "Projet": "[\"https://www.notion.so/15a6c54939df801781eee12c65031315\"]"
    },
    "content": "..."
  }]
}
```

### Batch de tâches (multi-task)

```javascript
{
  "parent": {
    "data_source_id": "12e6c549-39df-80ab-a332-000bd7bad408"
  },
  "pages": [
    {
      "properties": {
        "Nom": "Tâche 1",
        "Temps estimé": 1,
        "État": "En attente",
        "Type": "[\"Bloquant\"]",
        "DAY": "[\"BACKLOG\"]",
        "Projet": "[\"https://www.notion.so/27e6c54939df80caab49d5f4ba40009f\"]"
      },
      "content": "..."
    },
    {
      "properties": {
        "Nom": "Tâche 2",
        "Temps estimé": 4,
        "État": "En attente",
        "Type": "[\"Evolution\"]",
        "DAY": "[\"BACKLOG\"]",
        "Projet": "[\"https://www.notion.so/27e6c54939df80caab49d5f4ba40009f\"]"
      },
      "content": "..."
    }
  ]
}
```

---

## Recherche de projet

```javascript
// notion-search dans la base Projets
{
  "query": "Gardel",
  "data_source_url": "collection://12e6c549-39df-80ba-884e-000b1a258661"
}
```

---

## Error Handling

### Projet non trouvé

```
🤔 **Projet "{input}" non trouvé**

Options :
1. Utiliser toDo (projet par défaut)
2. Rechercher dans Notion
3. Entrer l'URL du projet

Ton choix ?
```

### Erreur API Notion

```
⚠️ **Erreur Notion** — {error_message}

[Brief complet affiché pour copier-coller]

🔄 `retry` pour réessayer | `skip` pour continuer
```
