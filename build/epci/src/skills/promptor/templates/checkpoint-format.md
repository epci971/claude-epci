# Checkpoint Format — CLI Templates

> Templates for session init, checkpoints, and summaries in CLI

---

## Session Initialization

```
🎯 **Session Promptor active**

Mode: Traitement en série
Règle: Chaque dictée = brief(s) indépendant(s)
Export: Notion (si configuré)

Envoyez votre première dictée.
```

---

## Mono-Task Output

```
[Brief generated]

═══════════════════════════════════════════════════════════════════
✅ Tâche créée : [{title}]({notion_url})
📂 Projet: {project_name} | 🏷️ Type: {type} | ⏱️ {hours}h
═══════════════════════════════════════════════════════════════════

Prochaine dictée ?
```

### Without Notion

```
[Brief generated]

═══════════════════════════════════════════════════════════════════
📋 Brief prêt — Copier dans Notion manuellement
🏷️ Type: {type} | ⏱️ {hours}h
═══════════════════════════════════════════════════════════════════

Prochaine dictée ?
```

---

## Multi-Task Checkpoint

```
📋 **{n} tâches détectées** [confiance: {HAUTE|MOYENNE}]

┌───┬────────────────────────────────────────┬───────────┬────────────┬───────┐
│ # │ Titre suggéré                          │ Type      │ Complexité │ Temps │
├───┼────────────────────────────────────────┼───────────┼────────────┼───────┤
│ 1 │ {title_1}                              │ {type_1}  │ {level_1}  │ {h}h  │
│ 2 │ {title_2}                              │ {type_2}  │ {level_2}  │ {h}h  │
└───┴────────────────────────────────────────┴───────────┴────────────┴───────┘

📝 Segments extraits:
   1 ← "{segment_1}"
   2 ← "{segment_2}"

📖 Commandes:
   ok          Générer tous les briefs
   ok 1,2      Sélection partielle
   merge 1,2   Fusionner en une tâche
   edit N "x"  Modifier titre N
   drop N      Supprimer N

Ton choix ?
```

---

## Checkpoint Commands Response

### After `ok`

```
⏳ Génération des {n} briefs...

[Brief 1]
═══════════════════════════════════════════════════════════════════

[Brief 2]
═══════════════════════════════════════════════════════════════════

✅ {n} tâches créées

| # | Tâche | Lien |
|---|-------|------|
| 1 | {title_1} | [→]({url_1}) |
| 2 | {title_2} | [→]({url_2}) |

─────────────────────────────────────────────────────────────────
Prochaine dictée ?
```

### After `merge 1,2`

```
🔗 Fusion des tâches 1 et 2...

📋 **{n-1} tâches après fusion**

[Updated table]

💡 Modifier le titre fusionné: edit 1 "nouveau titre"

Ton choix ?
```

### After `edit N "x"`

```
✏️ Titre modifié

[Updated table]

Ton choix ?
```

### After `drop N`

```
🗑️ Tâche {N} supprimée

[Updated table]

Ton choix ?
```

---

## Session End Summary

```
📊 **Résumé session Promptor**

| # | Tâche | Type | Temps | Lien |
|---|-------|------|-------|------|
| 1 | {title_1} | {type_1} | {h}h | [→]({url_1}) |
| 2 | {title_2} | {type_2} | {h}h | [→]({url_2}) |

✅ **{n} tâches créées**
⏱️ **Temps total estimé**: {total}h

Session terminée.
```

---

## Error States

### Notion Error

```
⚠️ **Erreur Notion** — {error_message}

📋 Brief sauvegardé ci-dessous (copier-coller manuel)

═══════════════════════════════════════════════════════════════════
[Complete brief]
═══════════════════════════════════════════════════════════════════

🔄 `retry` pour réessayer | `skip` pour continuer
```

### No Notion Config

```
ℹ️ **Notion non configuré**

Briefs affichés en texte uniquement.
Configurez `.claude/settings.local.json` pour export automatique.
```

---

## Status Command

```
📊 **État session Promptor**

| Élément | Valeur |
|---------|--------|
| Notion | {Configuré | Non configuré} |
| Tâches créées | {n} |
| Temps total | {h}h |

Dernière tâche: {last_title}
```
