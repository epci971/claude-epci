# Notion Configuration

> Configuration for Notion integration in Promptor

---

## Local Configuration

Notion credentials in `.claude/settings.local.json`:

```json
{
  "notion": {
    "token": "ntn_YOUR_INTEGRATION_TOKEN",
    "tasks_database_id": "YOUR_TASKS_DATABASE_ID",
    "default_project_id": "YOUR_DEFAULT_PROJECT_PAGE_ID"
  }
}
```

### Fields

| Field | Description | Required |
|-------|-------------|----------|
| `token` | Notion integration token (ntn_xxx) | Yes |
| `tasks_database_id` | Database ID where tasks are created | Yes |
| `default_project_id` | Default project page ID | Yes |

### How to Get IDs

1. **Token**: Create integration at https://www.notion.so/profile/integrations
2. **Database ID**: Open database in Notion, copy from URL after workspace name
3. **Project ID**: Open project page, copy from URL

---

## Properties Mapping

### Properties Filled by Promptor

| Property | Source | Default |
|----------|--------|---------|
| `Nom` | Brief title | - |
| `Description` | Brief content (markdown) | - |
| `Type` | Auto-detected | "Tache" |
| `Temps estimé` | Complexity (1/4/8) | 4 |
| `État` | Fixed | "En attente" |
| `DAY` | Fixed | "BACKLOG" |
| `Projet` | Config default | From settings |

### Properties Left to Notion AI

- Priorité
- Difficulté
- Module
- Étiquettes

---

## Type Values

| Type Notion | Detection Keywords |
|-------------|-------------------|
| Tache | (default) |
| Evolution | créer, ajouter, feature |
| Bloquant | bug, fixer, corriger |
| Backend | API, service, BDD |
| Frontend | UI, composant, React |
| Réunion | réunion, meeting |
| Formation | formation, training |
| Support | support, assistance |

---

## État Values (Status)

### To-do
- `En attente` ← **default for new tasks**
- `A planifier`
- `À analyser`

### In progress
- `En cours`
- `En pause`
- `Attente élément`

### Complete
- `Terminé`
- `Annulé`

---

## DAY Values

```
BACKLOG, LUNDI, MARDI, MERCREDI, JEUDI, VENDREDI, SAMEDI, DIMANCHE
```

Default: `BACKLOG`

---

## MCP Notion API

### Create Task

Using MCP tool `create-a-page`:

```json
{
  "parent": {
    "data_source_id": "{tasks_database_id}"
  },
  "properties": {
    "Nom": "Task title",
    "Temps estimé": 4,
    "État": "En attente",
    "Type": "[\"Evolution\"]",
    "DAY": "[\"BACKLOG\"]",
    "Projet": "[\"https://www.notion.so/{project_id}\"]"
  },
  "content": "Markdown content of the brief"
}
```

### Notes

- Multi-select properties use JSON array format: `"[\"Value\"]"`
- Relation properties use URL format: `"[\"https://www.notion.so/{page_id}\"]"`
- `data_source_id` format: Add hyphens to database ID (UUID format)

---

## Fallback Behavior

If Notion is not configured or unavailable:

1. Display brief as formatted text
2. Show message: "📋 Brief prêt — Copier dans Notion manuellement"
3. Continue session normally

No error thrown — graceful degradation.
