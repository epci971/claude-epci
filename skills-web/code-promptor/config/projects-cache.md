# Projects Cache — Project Page Resolution

> Cache des pages Projet pour résolution rapide sans recherche MCP

---

## Overview

Le cache stocke les **pages** de la base Projets pour une résolution rapide.

**Format relation Projet** : JSON array d'URLs
```javascript
"Projet": "[\"https://www.notion.so/{page_id}\"]"
```

---

## Projets en cache

### toDo (Projet par défaut)

| Champ | Valeur |
|-------|--------|
| **Page ID** | `15a6c54939df801781eee12c65031315` |
| **URL** | `https://www.notion.so/15a6c54939df801781eee12c65031315` |
| **Aliases** | todo, inbox, défaut, aucun, default |
| **Is Default** | ✅ Oui |

```yaml
- page_id: "15a6c54939df801781eee12c65031315"
  url: "https://www.notion.so/15a6c54939df801781eee12c65031315"
  name: "toDo"
  aliases: ["todo", "inbox", "défaut", "aucun", "default"]
  is_default: true
```

---

### Gardel-DataWareHouse

| Champ | Valeur |
|-------|--------|
| **Page ID** | `27e6c54939df80caab49d5f4ba40009f` |
| **URL** | `https://www.notion.so/27e6c54939df80caab49d5f4ba40009f` |
| **Aliases** | gardel, usine, sucre, sucrerie, datawarehouse, dwh |
| **Keywords** | TCB, laboratoire, canne, brix, pol, analyse, sucre |
| **Stack** | Django, React, PostgreSQL |

```yaml
- page_id: "27e6c54939df80caab49d5f4ba40009f"
  url: "https://www.notion.so/27e6c54939df80caab49d5f4ba40009f"
  name: "Gardel-DataWareHouse"
  aliases: ["gardel", "usine", "sucre", "sucrerie", "datawarehouse", "dwh"]
  keywords: ["TCB", "laboratoire", "canne", "brix", "pol", "analyse"]
  stack: ["Django", "React", "PostgreSQL"]
```

---

### EPCI-Workflow-IADD

| Champ | Valeur |
|-------|--------|
| **Page ID** | `1b66c54939df80fe8e2ee37ec94a4fdf` |
| **URL** | `https://www.notion.so/1b66c54939df80fe8e2ee37ec94a4fdf` |
| **Aliases** | epci, iadd, workflow, claude code |
| **Keywords** | plugin, claude, workflow, IADD, methodology |

```yaml
- page_id: "1b66c54939df80fe8e2ee37ec94a4fdf"
  url: "https://www.notion.so/1b66c54939df80fe8e2ee37ec94a4fdf"
  name: "EPCI-Workflow-IADD"
  aliases: ["epci", "iadd", "workflow", "claude code"]
  keywords: ["plugin", "claude", "workflow", "IADD", "methodology"]
```

---

### StBarth-202511

| Champ | Valeur |
|-------|--------|
| **Page ID** | `2a36c54939df807cad6def89b1d86078` |
| **URL** | `https://www.notion.so/2a36c54939df807cad6def89b1d86078` |
| **Aliases** | stbarth, st barth, saint barth, sbh |
| **Keywords** | client, site, prestashop |

```yaml
- page_id: "2a36c54939df807cad6def89b1d86078"
  url: "https://www.notion.so/2a36c54939df807cad6def89b1d86078"
  name: "StBarth-202511"
  aliases: ["stbarth", "st barth", "saint barth", "sbh"]
  keywords: ["client", "site"]
```

---

### Montée en version 7.4

| Champ | Valeur |
|-------|--------|
| **Page ID** | `28e6c54939df80e4a4bdf01563664c82` |
| **URL** | `https://www.notion.so/28e6c54939df80e4a4bdf01563664c82` |
| **Aliases** | montée version, upgrade, 7.4, symfony 7 |
| **Keywords** | symfony, upgrade, migration, version |
| **Stack** | Symfony |

```yaml
- page_id: "28e6c54939df80e4a4bdf01563664c82"
  url: "https://www.notion.so/28e6c54939df80e4a4bdf01563664c82"
  name: "Montée en version 7.4"
  aliases: ["montée version", "upgrade", "7.4", "symfony 7"]
  keywords: ["symfony", "upgrade", "migration", "version"]
  stack: ["Symfony"]
```

---

## Resolution Algorithm

### Priority Order

```
1. Alias exact match     → 100% confidence → Auto-select
2. Name partial match    → 85% confidence  → Auto-select  
3. Keyword + stack match → 75% confidence  → Auto-select
4. Keyword only          → 70% confidence  → Auto-select with note
5. MCP Search            → Variable        → Depends on results
6. No match              → Use default     → toDo
```

### Exemples de résolution

| Input | Match | Projet | Confidence |
|-------|-------|--------|------------|
| "gardel" | alias exact | Gardel-DataWareHouse | 100% |
| "Gardel" | alias (case-insensitive) | Gardel-DataWareHouse | 100% |
| "le projet TCB" | keyword | Gardel-DataWareHouse | 70% |
| "epci" | alias exact | EPCI-Workflow-IADD | 100% |
| "stbarth" | alias exact | StBarth-202511 | 100% |
| "upgrade symfony" | keyword | Montée en version 7.4 | 70% |
| "aucun" | alias default | toDo | 100% |
| "xyz123" | no match | toDo (fallback) | 0% |

---

## MCP Search Fallback

Si aucun match en cache :

```javascript
// Recherche dans la base Projets
{
  "query": "{project_name}",
  "data_source_url": "collection://12e6c549-39df-80ba-884e-000b1a258661"
}
```

---

## Ajouter un projet au cache

1. Récupérer l'URL du projet depuis Notion
2. Extraire le page_id (dernière partie de l'URL avant `?`)
3. Définir des aliases (noms courts, références courantes)
4. Ajouter des keywords (termes du domaine)
5. Noter le stack technique si pertinent

### Template

```yaml
- page_id: "{id}"
  url: "https://www.notion.so/{id}"
  name: "{Nom exact}"
  aliases: ["{alias1}", "{alias2}"]
  keywords: ["{kw1}", "{kw2}"]
  stack: ["{tech1}"]
```

---

## Session Commands

### Voir le cache

```
liste projets
```

### Changer de projet en session

```
projet gardel
projet epci
projet aucun  → toDo
```

### Rechercher hors cache

```
projet "Nouveau Projet"  → déclenche MCP search
```
