# Checkpoint Format — Validation Templates

> Templates for session init, checkpoints, and summaries

---

## Session Initialization

### Init Message (after activation)

```
🎯 **Session Promptor active**

Mode: Traitement en série
Règle: Chaque dictée = brief(s) indépendant(s)
Export: Direct vers Notion

📂 **Projet Notion ?** (ou 'aucun' pour tâches sans projet)
```

### Project Confirmation

```
✅ Projet: **{project_name}** verrouillé pour cette session.

Envoyez votre première dictée.
```

### No Project Mode

```
✅ Mode sans projet activé.

Les tâches seront créées sans relation Projet.
Vous pouvez les organiser manuellement ensuite.

Envoyez votre première dictée.
```

---

## Mono-Task Flow

### Direct Generation (no checkpoint)

For mono-task, skip checkpoint and generate directly:

```
[Brief generated]

═══════════════════════════════════════════════════════════════════
✅ Tâche créée : [{title}]({notion_url})
📂 Projet: {project_name} | 🏷️ Type: {type} | ⏱️ {hours}h
═══════════════════════════════════════════════════════════════════

Prochaine dictée ?
```

---

## Multi-Task Checkpoint

### Standard Format

```
📋 **{n} tâches détectées dans cette dictée**

┌───┬────────────────────────────────────────┬───────────┬────────────┬───────┐
│ # │ Titre suggéré                          │ Type      │ Complexité │ Temps │
├───┼────────────────────────────────────────┼───────────┼────────────┼───────┤
│ 1 │ {title_1}                              │ {type_1}  │ {level_1}  │ {h}h  │
│ 2 │ {title_2}                              │ {type_2}  │ {level_2}  │ {h}h  │
│ 3 │ {title_3}                              │ {type_3}  │ {level_3}  │ {h}h  │
└───┴────────────────────────────────────────┴───────────┴────────────┴───────┘

📝 **Segments extraits :**
   1 ← "{segment_1}"
   2 ← "{segment_2}"
   3 ← "{segment_3}"

📖 **Commandes disponibles :**
   `ok`          Générer tous les briefs
   `ok 1,2`      Générer seulement certains briefs
   `merge 1,2`   Fusionner en une seule tâche
   `edit N "x"`  Modifier le titre de la tâche N
   `drop N`      Supprimer la tâche N
   `split N`     Découper en sous-tâches détaillées
   `reanalyze`   Relancer la détection

Ton choix ?
```

### With Low Confidence

```
📋 **{n} tâches détectées** (⚠️ confiance: MOYENNE)

[same table]

📝 **Segments extraits :**
[segments]

⚠️ Le découpage semble incertain. Vérifiez avant validation.

📖 **Commandes disponibles :**
[commands]
```

### Dense Dictation Warning

```
📋 **{n} tâches détectées** (⚠️ dictée très dense)

[table]

⚠️ Plus de 5 tâches détectées. Vérifiez que le découpage est correct.
Considérez `merge` pour regrouper les tâches liées.

[commands]
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

[Brief n]
═══════════════════════════════════════════════════════════════════

✅ {n} tâches créées dans Notion

| # | Tâche | Lien |
|---|-------|------|
| 1 | {title_1} | [→]({url_1}) |
| 2 | {title_2} | [→]({url_2}) |

─────────────────────────────────────────────────────────────────
Prochaine dictée ?
```

### After `ok 1,3`

```
⏳ Génération des briefs 1 et 3...

[Brief 1]
═══════════════════════════════════════════════════════════════════

[Brief 3]
═══════════════════════════════════════════════════════════════════

✅ 2 tâches créées (1 ignorée)

[table with links]

─────────────────────────────────────────────────────────────────
Prochaine dictée ?
```

### After `merge 1,3`

```
🔗 Fusion des tâches 1 et 3...

📋 **2 tâches après fusion**

┌───┬────────────────────────────────────────┬───────────┬────────────┬───────┐
│ # │ Titre suggéré                          │ Type      │ Complexité │ Temps │
├───┼────────────────────────────────────────┼───────────┼────────────┼───────┤
│ 1 │ {merged_title}                         │ {type}    │ {level}    │ {h}h  │
│ 2 │ {title_2}                              │ {type_2}  │ {level_2}  │ {h}h  │
└───┴────────────────────────────────────────┴───────────┴────────────┴───────┘

💡 Le titre fusionné peut être modifié avec `edit 1 "nouveau titre"`

Ton choix ?
```

### After `edit 2 "Nouveau titre"`

```
✏️ Titre modifié

📋 **3 tâches**

[updated table with new title]

Ton choix ?
```

### After `drop 2`

```
🗑️ Tâche 2 supprimée

📋 **2 tâches restantes**

[updated table]

Ton choix ?
```

### After `reanalyze`

```
🔄 Relance de la détection...

[New checkpoint with potentially different segmentation]
```

---

## Brief Separator

Between multiple briefs:

```
═══════════════════════════════════════════════════════════════════
📋 TÂCHE {n}/{total} — Copier dans Notion
═══════════════════════════════════════════════════════════════════
```

---

## Session End Summary

### Standard End

```
📊 **Résumé session Promptor**

| # | Tâche | Type | Temps | Lien |
|---|-------|------|-------|------|
| 1 | {title_1} | {type_1} | {h}h | [→]({url_1}) |
| 2 | {title_2} | {type_2} | {h}h | [→]({url_2}) |
| 3 | {title_3} | {type_3} | {h}h | [→]({url_3}) |

✅ **{n} tâches créées** dans projet {project_name}
⏱️ **Temps total estimé** : {total}h

Session terminée. Nouvelle session avec `promptor session`.
```

### End Without Project

```
📊 **Résumé session Promptor**

| # | Tâche | Type | Temps | Lien |
|---|-------|------|-------|------|
[table]

✅ **{n} tâches créées** (sans projet assigné)
⏱️ **Temps total estimé** : {total}h

💡 Pensez à organiser ces tâches dans vos projets Notion.

Session terminée.
```

---

## Error States

### Notion API Error

```
⚠️ **Erreur Notion** — Impossible de créer la tâche

Erreur: {error_message}

📋 **Brief sauvegardé ci-dessous** (copier-coller manuel possible)

═══════════════════════════════════════════════════════════════════
[Complete brief content]
═══════════════════════════════════════════════════════════════════

🔄 Commandes: `retry` pour réessayer, `skip` pour continuer
```

### Project Not Found

```
🤔 **Projet "{input}" non trouvé**

Projets disponibles :
1. Gardel
2. C2I Outremer
3. [Rechercher dans Notion]

Quel projet ? (numéro ou nom)
```

### Ambiguous Project

```
🤔 **Plusieurs projets correspondent à "{input}"**

1. Gardel (correspondance: 65%)
2. Gardel-Test (correspondance: 45%)

Lequel ? (1 ou 2)
```

---

## Status Command

```
User: "status"

Claude:
📊 **État session Promptor**

| Élément | Valeur |
|---------|--------|
| Projet | {project_name} |
| Tâches créées | {n} |
| Temps total | {h}h |
| Début session | {time} |

Dernière tâche : [{last_title}]({last_url})
```
