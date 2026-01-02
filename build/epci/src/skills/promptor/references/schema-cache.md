# Notion Schema Cache

> Auto-discovery and caching of Notion database schema for dynamic property mapping.

---

## Overview

Instead of hardcoding property types, Promptor queries the Notion database schema
on first use and caches it locally. This ensures correct property formats even when
the database structure changes.

---

## Cache Location

```
.project-memory/cache/notion-schema.json
```

---

## Schema Structure

```json
{
  "database_id": "12e6c549-39df-8004-9226-dc6215904a74",
  "cached_at": "2026-01-02T15:00:00.000Z",
  "properties": {
    "Nom": {
      "type": "title",
      "format": {"title": [{"text": {"content": "VALUE"}}]}
    },
    "Type": {
      "type": "multi_select",
      "format": {"multi_select": [{"name": "VALUE"}]},
      "options": ["Evolution", "Bloquant", "Tache", "Backend", "Frontend"]
    },
    "DAY": {
      "type": "multi_select",
      "format": {"multi_select": [{"name": "VALUE"}]},
      "options": ["BACKLOG", "LUNDI", "MARDI", "MERCREDI", "JEUDI", "VENDREDI"]
    },
    "Temps estimé": {
      "type": "number",
      "format": {"number": 0}
    },
    "Projet": {
      "type": "relation",
      "format": {"relation": [{"id": "PAGE_ID"}]}
    },
    "État": {
      "type": "status",
      "format": {"status": {"name": "VALUE"}},
      "options": ["En attente", "En cours", "Terminé"]
    }
  }
}
```

---

## Workflow

### 1. Check Cache

Before creating a Notion page, check if schema cache exists and is valid:

```bash
CACHE_FILE=".project-memory/cache/notion-schema.json"

if [ -f "$CACHE_FILE" ]; then
  # Check if cache is less than 24h old
  CACHE_AGE=$(($(date +%s) - $(stat -c %Y "$CACHE_FILE")))
  if [ $CACHE_AGE -lt 86400 ]; then
    # Use cached schema
    SCHEMA=$(cat "$CACHE_FILE")
  fi
fi
```

### 2. Fetch Schema (if needed)

Query database schema via Notion API:

```bash
curl -s -X GET "https://api.notion.com/v1/databases/${DATABASE_ID}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Notion-Version: 2022-06-28"
```

### 3. Parse and Cache

Extract property types from API response:

```json
{
  "properties": {
    "Type": {
      "id": "EGYe",
      "name": "Type",
      "type": "multi_select",
      "multi_select": {
        "options": [
          {"id": "xxx", "name": "Evolution", "color": "gray"},
          {"id": "yyy", "name": "Bloquant", "color": "red"}
        ]
      }
    }
  }
}
```

Transform to cache format and save.

### 4. Use Schema for Page Creation

When creating a page, use cached schema to format properties correctly:

```python
def format_property(name, value, schema):
    prop_type = schema["properties"][name]["type"]

    if prop_type == "title":
        return {"title": [{"text": {"content": value}}]}
    elif prop_type == "multi_select":
        return {"multi_select": [{"name": value}]}
    elif prop_type == "select":
        return {"select": {"name": value}}
    elif prop_type == "number":
        return {"number": value}
    elif prop_type == "date":
        return {"date": {"start": value}}
    elif prop_type == "relation":
        return {"relation": [{"id": value}]}
    elif prop_type == "status":
        return {"status": {"name": value}}
    elif prop_type == "rich_text":
        return {"rich_text": [{"text": {"content": value}}]}
```

---

## Cache Invalidation

Cache is invalidated when:

1. **Age > 24h** — Automatic refresh
2. **API error 400** — Schema may have changed, force refresh
3. **Manual** — Delete `.project-memory/cache/notion-schema.json`

---

## Fallback Behavior

If schema fetch fails:

1. Use hardcoded defaults from `notion-config.md`
2. Log warning for debugging
3. Continue with best-effort property formatting

---

## Property Type Reference

| Notion Type | API Format |
|-------------|------------|
| `title` | `{"title": [{"text": {"content": "..."}}]}` |
| `rich_text` | `{"rich_text": [{"text": {"content": "..."}}]}` |
| `number` | `{"number": N}` |
| `select` | `{"select": {"name": "..."}}` |
| `multi_select` | `{"multi_select": [{"name": "..."}]}` |
| `date` | `{"date": {"start": "YYYY-MM-DD"}}` |
| `checkbox` | `{"checkbox": true/false}` |
| `relation` | `{"relation": [{"id": "page_id"}]}` |
| `status` | `{"status": {"name": "..."}}` |
| `people` | `{"people": [{"id": "user_id"}]}` |

---

## Implementation Notes

### For Claude Code (Bash-based)

Since we use Bash/curl for Notion API calls, the schema caching logic
should be implemented as follows:

1. **Before first export in session**: Check/fetch schema
2. **Store in memory**: Keep schema in conversation context
3. **Persist to file**: Save to `.project-memory/cache/` for future sessions

### Key Instructions for Claude

When executing Notion export:

1. **Read cache file** if exists
2. **If no cache or stale**: Fetch schema from API
3. **Parse property types** from schema
4. **Build JSON payload** with correct formats
5. **On 400 error**: Refresh schema and retry once

---

## Example: Full Schema Fetch

```bash
# Fetch database schema
SCHEMA_RESPONSE=$(curl -s -X GET \
  "https://api.notion.com/v1/databases/12e6c54939df80049226dc6215904a74" \
  -H "Authorization: Bearer ntn_xxx" \
  -H "Notion-Version: 2022-06-28")

# Extract property types with jq
echo "$SCHEMA_RESPONSE" | jq '{
  database_id: .id,
  cached_at: now | strftime("%Y-%m-%dT%H:%M:%S.000Z"),
  properties: .properties | to_entries | map({
    key: .key,
    value: {
      type: .value.type,
      options: (if .value.type == "multi_select" then .value.multi_select.options | map(.name)
               elif .value.type == "select" then .value.select.options | map(.name)
               elif .value.type == "status" then .value.status.options | map(.name)
               else null end)
    }
  }) | from_entries
}' > .project-memory/cache/notion-schema.json
```
