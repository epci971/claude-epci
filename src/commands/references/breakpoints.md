# Breakpoint Templates Reference

> Shared breakpoint display templates for EPCI commands.

## Standard Breakpoint Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT — {TITLE}                                             │
├─────────────────────────────────────────────────────────────────────┤
│ FLAGS: {flags with sources}                                         │
├─────────────────────────────────────────────────────────────────────┤
│ {CONTENT SECTIONS}                                                  │
├─────────────────────────────────────────────────────────────────────┤
│ Options:                                                            │
│   • {Option 1}                                                      │
│   • {Option 2}                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Flag Sources Legend

| Source | Meaning |
|--------|---------|
| `(auto)` | Auto-activated based on context |
| `(explicit)` | User-specified |
| `(alias)` | Expanded from alias (e.g., --large) |
| `(auto: persona)` | Activated by persona |
| `(auto: X.XX)` | Activated by scoring threshold |

## Metrics Section Template

```
📊 MÉTRIQUES
├── Complexité: {CATEGORY} (score: {SCORE})
├── Fichiers impactés: {FILE_COUNT}
├── Temps estimé: {TIME_ESTIMATE}
└── Risque: {RISK_LEVEL}
```

## Validations Section Template

```
✅ VALIDATIONS
├── @{agent}: {VERDICT}
│   ├── {Check 1}: {STATUS}
│   └── {Check 2}: {STATUS}
└── Skills chargés: {SKILLS_LIST}
```

## Options Templates

### Continue/Modify/Cancel

```
Options:
  • Tapez "Continuer" → Passer à la phase suivante
  • Tapez "Modifier" → Réviser le contenu
  • Tapez "Annuler" → Abandonner le workflow
```

### Validate/Adjust/Cancel

```
Options:
  • "Valider" → Procéder
  • "Modifier" → Ajuster
  • "Annuler" → Abandonner
```

## Lightweight Breakpoint (Quick)

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📋 PLAN: {N} tâches | ~{LOC} LOC | {FILE_COUNT} fichier(s)         │
├─────────────────────────────────────────────────────────────────────┤
│ [1] {Task 1}                                                        │
│ [2] {Task 2}                                                        │
│ Auto-continue dans 3s... (Entrée=modifier, Échap=annuler)          │
└─────────────────────────────────────────────────────────────────────┘
```

## Completion Templates

### Success

```
✅ **{WORKFLOW} COMPLETE**

{Summary content}
Next: {Next step suggestion}
```

### Error

```
❌ **ERREUR**

{Error description}
💡 Suggestion: {Fix suggestion}
```
