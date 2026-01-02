# Type Mapping — Notion Type Detection

> Rules for mapping detected task types to Notion Type property

---

## Notion Type Values

| Type Notion | Usage |
|-------------|-------|
| Tache | Generic tasks (default) |
| Evolution | New features |
| Bloquant | Bugs, blockers |
| Backend | Backend-specific |
| Frontend | Frontend-specific |
| Réunion | Meetings |
| Formation | Training |
| Support | Support tasks |

---

## Detection Priority

1. Domain-specific (Backend/Frontend)
2. Bug/Blocker indicators
3. Feature indicators
4. Default (Tache)

---

## Detection Matrix

| Detection | Keywords | Type |
|-----------|----------|------|
| **Bug** | bug, fix, fixer, corriger, réparer, cassé, crash, erreur | **Bloquant** |
| **Feature** | créer, ajouter, nouveau, implémenter, développer, feature | **Evolution** |
| **Backend** | API, service, endpoint, BDD, Symfony, Django, controller | **Backend** |
| **Frontend** | UI, interface, composant, React, Vue, formulaire, bouton | **Frontend** |
| **Refacto** | refacto, nettoyer, optimiser, restructurer | **Tache** |
| **Meeting** | réunion, meeting, call, sync | **Réunion** |
| **Training** | formation, training, onboarding | **Formation** |
| **Support** | support, assistance, aide | **Support** |
| **Default** | (none of above) | **Tache** |

---

## Multi-Type Handling

### Backend + Feature
```
"Créer une nouvelle API" → Backend (more specific)
```

### Frontend + Bug
```
"Fixer le bug d'affichage" → Bloquant (bug priority)
```

### Backend + Frontend
```
"API et composant React" → MULTI-TASK (2 tasks)
```

---

## Priority Escalation

Escalate to **Bloquant** if:
```
"urgent", "critique", "bloquant", "ASAP", "prioritaire"
```

---

## Confidence Levels

| Confidence | Criteria |
|------------|----------|
| HIGH | Clear keyword match, single type |
| MEDIUM | Multiple types, one dominant |
| LOW | Vague, no clear keywords |

---

## Examples

| Dictation | Type |
|-----------|------|
| "Fixer le bug de login" | Bloquant |
| "Créer l'export PDF" | Evolution |
| "Nouvelle API utilisateurs" | Backend |
| "Composant React dashboard" | Frontend |
| "Refacto du service auth" | Tache |
| "Réunion planning sprint" | Réunion |

---

## Notion Format

Type property is **Multi-select**, format as JSON array:

```javascript
"Type": "[\"Backend\"]"
```

Default if no type detected:
```javascript
"Type": "[\"Tache\"]"
```
