# Journal d'Exploration — Promptor Notion Integration

**Date** : 2025-12-31
**Durée** : ~45 minutes
**EMS Final** : 82/100

---

## Progression EMS

| Iteration | EMS | Delta | Phase | Actions clés |
|-----------|-----|-------|-------|--------------|
| Init | 0 | - | - | Lancement brainstorm |
| Iter 1 | 35 | +35 | 🔀 Divergent | Exploration code-promptor, questions HMW |
| Iter 2 | 55 | +20 | 🔀 Divergent | Validation décisions Q1-Q5, architecture proposée |
| Spike | - | - | 🔬 Technical | MCP Notion + Secrets investigation |
| Iter 3 | 82 | +27 | 🎯 Convergent | Synthèse finale, architecture validée |

---

## Exploration Code-Promptor

### Analyse du skill web (skills-web/code-promptor/)

**Structure découverte** :
```
skills-web/code-promptor/
├── SKILL.md                 (9,055 bytes)
├── CAHIER_DES_CHARGES.md    (20,144 bytes)
├── JOURNAL_EXPLORATION.md   (9,156 bytes)
├── config/
│   ├── notion-ids.md
│   └── projects-cache.md
├── references/
│   ├── output-format.md
│   ├── multi-task-detection.md
│   ├── subtask-templates.md
│   ├── type-mapping.md
│   ├── processing-rules.md
│   └── voice-cleaning.md
└── templates/
    ├── checkpoint-format.md
    ├── brief-quickfix.md
    ├── brief-standard.md
    └── brief-major.md
```

**Logique métier identifiée** :
1. Mode Session vs One-shot
2. Nettoyage vocal (hésitations, fillers)
3. Détection multi-tâches agressive (seuil 40 pts)
4. Checkpoint interactif avec commandes (ok, merge, edit, drop)
5. 3 formats adaptatifs (1h/4h/8h)
6. Auto-génération sous-tâches par type/domaine
7. Export Notion direct

---

## Questions de Cadrage

### Q1. Mode d'interaction
- **Options** : (a) Session, (b) One-shot, (c) Hybride
- **Décision** : **(c) Hybride** — comme code-promptor actuel
- **Raison** : Flexibilité maximale

### Q2. Configuration Notion
- **Options** : (a) `.env.local`, (b) `.project-memory/`, (c) `.notion-ids`
- **Décision** : **`.claude/settings.local.json`** section `notion`
- **Raison** : Déjà gitignored, structure existante, chaque dev a le sien

### Q3. Relation projets
- **Options** : (a) Auto-détection, (b) Config explicite, (c) Demander
- **Décision** : **(b) Config explicite** dans `.claude/settings.local.json`
- **Raison** : Déjà dans le contexte projet, pas besoin de résolution

### Q4. Checkpoint CLI
- **Options** : (a) Complet, (b) Simplifié, (c) Auto
- **Décision** : **(a) Complet** — tableau + commandes interactives
- **Raison** : Feedback utilisateur précieux

### Q5. Intégration EPCI
- **Options** : (a) Complémentaire, (b) Fusion, (c) Chaînage
- **Décision** : **(a) Complémentaire** — standalone
- **Raison** : Pense-bête indépendant, pas de complexité ajoutée

### Q6. Cache projets
- **Options** : (a) Pas de cache, (b) Cache optionnel
- **Décision** : **(a) Pas de cache**
- **Raison** : Un seul projet par config locale

### Q7. Dépendances ref [n]
- **Options** : (a) Oui, (b) Non
- **Décision** : **(b) Non** en v1
- **Raison** : Garder simple, ajouter plus tard si besoin

### Q8. Format propriétés Notion
- **Options** : (a) Identique, (b) Configurable
- **Décision** : **(a) Identique** à code-promptor
- **Raison** : Compatibilité base Notion existante

---

## Spikes Techniques

### Spike 1 : MCP Notion

**Durée** : ~15 min
**Verdict** : GO ✅

**Découvertes** :
1. Package officiel : `@notionhq/notion-mcp-server` par Notion
2. Version 2.0.0 avec API 2025-09-03
3. Installation via `npx -y` (pas d'installation permanente)
4. Auth via `NOTION_TOKEN` env variable
5. 21 tools disponibles dont `create-a-page`, `query-data-source`

**Configuration type** :
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_TOKEN": "ntn_xxx"
      }
    }
  }
}
```

**Sources** :
- https://developers.notion.com/docs/mcp
- https://github.com/makenotion/notion-mcp-server

### Spike 2 : Gestion Secrets

**Durée** : ~10 min
**Verdict** : GO ✅

**Découvertes** :
1. `.claude/settings.local.json` existe et est gitignored
2. Pattern global dans `~/.config/git/ignore`
3. Permissions 600 (owner only) — sécurisé
4. Structure extensible — peut ajouter section `notion`

**Structure recommandée** :
```json
{
  "permissions": { ... },
  "notion": {
    "token": "ntn_xxx",
    "tasks_database_id": "12e6c54939df80049226dc6215904a74",
    "default_project_id": "27e6c54939df80caab49d5f4ba40009f"
  }
}
```

---

## Architecture Finale

### Nouveaux fichiers à créer

```
src/
├── commands/
│   └── promptor.md                    # Commande principale
├── skills/
│   └── promptor/
│       ├── SKILL.md                   # Logique métier
│       ├── references/
│       │   ├── multi-task-detection.md
│       │   ├── output-format.md
│       │   └── voice-cleaning.md
│       └── templates/
│           ├── brief-quickfix.md
│           ├── brief-standard.md
│           └── brief-major.md
└── mcp/
    └── config.py                      # Ajouter serveur notion
```

### Fichiers à modifier

| Fichier | Modification |
|---------|--------------|
| `.claude/settings.local.json` | Ajouter section `notion` |
| `src/mcp/config.py` | Ajouter config serveur `notion` |
| `CLAUDE.md` | Documenter commande `/promptor` |

---

## Points Clés Retenus

1. **Dictée vocale fonctionne déjà** en CLI — pas besoin d'adaptation spéciale
2. **MCP Notion officiel** disponible et maintenu par Notion
3. **Secrets dans `.claude/`** — pattern validé et sécurisé
4. **Standalone** — pas d'intégration avec workflow EPCI
5. **Mapping identique** à code-promptor pour compatibilité Notion

---

## Prochaines Étapes

1. Créer l'infrastructure MCP Notion dans EPCI
2. Porter les fichiers references/ depuis code-promptor
3. Adapter les templates au contexte CLI
4. Implémenter la commande /promptor
5. Tester le workflow complet

---

*Journal généré par /brainstorm — EPCI v4.4*
