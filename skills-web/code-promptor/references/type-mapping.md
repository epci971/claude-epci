# Type Mapping — Notion Type Detection

> Rules for mapping detected task types to Notion Type property

---

## Overview

Code-Promptor auto-detects task type from dictation content and maps to Notion's Type property values.

---

## Notion Type Values

Based on the target database:

| Type Notion | Color | Usage |
|-------------|-------|-------|
| Tache | Blue | Generic tasks |
| Ticket Interne | Purple | Internal tickets |
| Ticket Client | Purple | Client-facing tickets |
| Support | Gray | Support tasks |
| Réunion | Gray | Meetings |
| Formation | Green | Training |
| Evolution | Green | New features |
| Bloquant | Red | Bugs, blockers |
| Tache interne | Yellow | Internal tasks |
| Backend | Gray | Backend-specific |
| Frontend | Gray | Frontend-specific |

---

## Detection Rules

### Priority Order

Detection follows this priority (first match wins):

```
1. Domain-specific (Backend/Frontend)
2. Bug/Blocker indicators
3. Feature indicators
4. Default (Tache)
```

### Detection Matrix

| Detection | Keywords | Type Notion |
|-----------|----------|-------------|
| **Bug/Blocker** | bug, fix, fixer, corriger, réparer, cassé, broken, crash, erreur, problème, régression | **Bloquant** |
| **Feature** | créer, ajouter, nouveau, nouvelle, implémenter, développer, feature, fonctionnalité, évolution | **Evolution** |
| **Backend** | API, service, endpoint, BDD, base de données, Symfony, Django, Laravel, controller, repository, model, migration, backend | **Backend** |
| **Frontend** | UI, interface, composant, component, React, Vue, Angular, affichage, formulaire, bouton, page, écran, CSS, style, frontend | **Frontend** |
| **Refacto** | refacto, refactoring, nettoyer, optimiser, restructurer, améliorer le code | **Tache** |
| **Documentation** | doc, documentation, readme, guide, wiki, documenter | **Tache** |
| **Test** | test, tester, QA, validation, vérifier, coverage | **Tache** |
| **Meeting** | réunion, meeting, call, sync, point | **Réunion** |
| **Training** | formation, training, onboarding, tuto | **Formation** |
| **Support** | support, assistance, aide, dépannage | **Support** |
| **Default** | (none of above) | **Tache** |

---

## Keyword Patterns

### Bug Detection (→ Bloquant)

**French**:
```
bug, bogue, fixer, corriger, réparer, cassé, planté, crash, 
erreur, problème, défaut, régression, dysfonctionnement,
ne marche pas, ne fonctionne pas, broken
```

**English**:
```
bug, fix, broken, crash, error, issue, defect, regression,
not working, fails, failing
```

**Contextual**:
```
"depuis hier", "ne marche plus", "urgent", "critique", "bloquant"
```

### Feature Detection (→ Evolution)

**French**:
```
créer, ajouter, nouveau, nouvelle, implémenter, développer,
mettre en place, concevoir, feature, fonctionnalité, évolution,
amélioration, permettre de
```

**English**:
```
create, add, new, implement, develop, build, feature,
enable, allow
```

### Backend Detection (→ Backend)

```
API, REST, GraphQL, endpoint, route, controller,
service, repository, model, entity, migration,
BDD, base de données, database, SQL, query,
Symfony, Django, Laravel, Express, FastAPI,
backend, back-end, serveur, server
```

### Frontend Detection (→ Frontend)

```
UI, interface, composant, component, 
React, Vue, Angular, Svelte,
affichage, display, formulaire, form,
bouton, button, page, écran, screen,
CSS, style, Tailwind, responsive,
frontend, front-end, client
```

---

## Multi-Type Handling

When multiple types are detected:

### Backend + Feature
```
Dictation: "Créer une nouvelle API pour les exports"
Detected: Feature + Backend
Result: **Backend** (more specific)
```

### Frontend + Bug
```
Dictation: "Fixer le bug d'affichage du formulaire"
Detected: Bug + Frontend  
Result: **Bloquant** (bug takes priority)
```

### Backend + Frontend
```
Dictation: "Développer l'API et le composant React"
Multi-task detected → 2 tasks:
- Task 1: **Backend**
- Task 2: **Frontend**
```

---

## Priority Modifiers

### Escalation to Bloquant

Even if Feature detected, escalate to Bloquant if:
```
"urgent", "critique", "bloquant", "ASAP", "prioritaire"
```

### Example
```
Dictation: "Ajouter urgente la validation email"
Base: Evolution (ajouter = feature)
Modifier: "urgent" detected
Result: **Bloquant**
```

---

## Confidence Levels

| Confidence | Criteria |
|------------|----------|
| HIGH | Clear keyword match, single type |
| MEDIUM | Multiple types, one dominant |
| LOW | Vague, no clear keywords |

### Display

```
Type: Evolution (confiance: HAUTE)
```

or

```
Type: Tache (⚠️ type incertain, vérifiez)
```

---

## Examples

### Clear Cases

| Dictation | Type |
|-----------|------|
| "Fixer le bug de login" | Bloquant |
| "Créer l'export PDF" | Evolution |
| "Nouvelle API utilisateurs" | Backend |
| "Composant React pour le dashboard" | Frontend |
| "Refacto du service auth" | Tache |
| "Réunion planning sprint" | Réunion |

### Ambiguous Cases

| Dictation | Analysis | Type |
|-----------|----------|------|
| "Améliorer les performances du dashboard" | Améliorer=feature, dashboard=frontend | Frontend |
| "Le formulaire ne valide pas" | Ne...pas=bug, formulaire=frontend | Bloquant |
| "Service de notification" | Service=backend | Backend |
| "Mettre à jour la doc API" | Doc=tache, API=backend | Tache |

---

## Integration with Notion

### Property Format

The Type property in Notion is **Multi-select**, so format as JSON array:

```javascript
"Type": "[\"Backend\"]"
```

For tasks that truly span multiple types (rare):
```javascript
"Type": "[\"Backend\", \"Frontend\"]"
```

### Default Behavior

If no type detected with confidence:
```javascript
"Type": "[\"Tache\"]"
```

---

## Override Option

User can override detected type in checkpoint:

```
📋 **1 tâche détectée**

│ # │ Titre                    │ Type     │
│ 1 │ Améliorer le formulaire  │ Frontend │

Pour changer le type: `type 1 Evolution`
```
