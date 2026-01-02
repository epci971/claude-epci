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

## Notion API (Direct)

> **Note**: Uses direct API via curl instead of MCP due to serialization bug in MCP Notion.

### Create Task

Using Bash tool with curl:

```bash
curl -s -X POST 'https://api.notion.com/v1/pages' \
  -H 'Authorization: Bearer {token}' \
  -H 'Content-Type: application/json' \
  -H 'Notion-Version: 2022-06-28' \
  -d '{
    "parent": {"database_id": "{tasks_database_id}"},
    "properties": {
      "Nom": {"title": [{"text": {"content": "Task title"}}]},
      "Type": {"multi_select": [{"name": "Evolution"}]},
      "Temps estimé": {"number": 4},
      "DAY": {"multi_select": [{"name": "BACKLOG"}]},
      "Projet": {"relation": [{"id": "{default_project_id}"}]}
    },
    "children": [
      {"type": "callout", "callout": {"icon": {"emoji": "📦"}, "rich_text": [{"text": {"content": "Standard | ⏱️ 4h"}}]}},
      {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Objectif"}}]}},
      {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Description here..."}}]}},
      {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Exigences fonctionnelles"}}]}},
      {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Requirement 1"}}]}},
      {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Notes"}}]}},
      {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Additional notes..."}}]}}
    ]
  }'
```

### Property Formats

| Property | Format |
|----------|--------|
| `title` | `{"title": [{"text": {"content": "..."}}]}` |
| `multi_select` | `{"multi_select": [{"name": "Value"}]}` |
| `number` | `{"number": 4}` |
| `relation` | `{"relation": [{"id": "page_id"}]}` |
| `rich_text` | `{"rich_text": [{"text": {"content": "..."}}]}` |

### Block Types for Children

| Block | Format |
|-------|--------|
| `heading_2` | `{"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "..."}}]}}` |
| `paragraph` | `{"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "..."}}]}}` |
| `bulleted_list_item` | `{"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "..."}}]}}` |
| `callout` | `{"type": "callout", "callout": {"icon": {"emoji": "📦"}, "rich_text": [{"text": {"content": "..."}}]}}` |

### Response Handling

On success, extract from response:
- `id`: Page ID (for URL construction)
- `properties.Identifiant de la tâche.unique_id.number`: Task number (QDT-xxx)
- `url`: Direct Notion URL

### Error Handling

```bash
# Check response for error
if echo "$response" | grep -q '"object":"error"'; then
  # Display brief for manual copy
  echo "⚠️ Erreur Notion — Copier manuellement"
fi
```

---

## Fallback Behavior

If Notion is not configured or unavailable:

1. Display brief as formatted text
2. Show message: "📋 Brief prêt — Copier dans Notion manuellement"
3. Continue session normally

No error thrown — graceful degradation.
