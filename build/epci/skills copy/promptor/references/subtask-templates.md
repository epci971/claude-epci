# Subtask Templates — Auto-Generation Rules

> Intelligence for generating contextual subtasks

---

## Generation Rules

| Complexity | Generate? |
|------------|-----------|
| Quick fix | No |
| Standard | Yes (2-3 phases) |
| Major | Yes (5-6 phases) |

---

## Templates by Task Type

### Bug Fix

```markdown
1. **Diagnostic**
   - [ ] Reproduire le bug en local
   - [ ] Identifier la cause racine

2. **Correction**
   - [ ] Appliquer le correctif
   - [ ] Tester la correction

3. **Finalisation**
   - [ ] Test de non-régression
```

### Feature (Standard)

```markdown
1. **[Domain] — Développement**
   - [ ] Créer la structure
   - [ ] Implémenter la logique

2. **Interface/API**
   - [ ] Exposer la fonctionnalité
   - [ ] Gérer les erreurs

3. **Finalisation**
   - [ ] Tests
   - [ ] Documentation
```

### Feature (Major)

```markdown
1. **Architecture & Préparation**
   - [ ] Définir modèles de données
   - [ ] Créer migrations

2. **Backend — Logique métier**
   - [ ] Créer service principal
   - [ ] Implémenter règles métier

3. **Backend — Intégration**
   - [ ] Client API externe
   - [ ] Gestion erreurs et retry

4. **Frontend — Vues principales**
   - [ ] Composant principal
   - [ ] États loading/error

5. **Finalisation**
   - [ ] Tests (coverage >80%)
   - [ ] Documentation technique
```

---

## Templates by Domain

### Backend API

```markdown
1. **API — Endpoint**
   - [ ] Créer controller/view
   - [ ] Définir route
   - [ ] Validation inputs

2. **API — Service**
   - [ ] Créer service métier
   - [ ] Gérer erreurs
```

### Frontend Component

```markdown
1. **Composant — Structure**
   - [ ] Créer composant
   - [ ] Définir props/interface

2. **Composant — Logique**
   - [ ] Gestion d'état
   - [ ] Interactions

3. **Composant — Style**
   - [ ] Appliquer styles
   - [ ] Responsive
```

---

## Templates by Stack

### Symfony

```markdown
- [ ] Créer Entity avec annotations
- [ ] Générer migration Doctrine
- [ ] Créer Repository
- [ ] Implémenter Service
- [ ] Créer Controller avec routes
```

### Django

```markdown
- [ ] Définir Model
- [ ] Créer migration
- [ ] Créer View/ViewSet
- [ ] Implémenter Serializer
- [ ] Configurer URLs
```

### React

```markdown
- [ ] Créer composant fonctionnel
- [ ] Définir types TypeScript
- [ ] Implémenter hooks
- [ ] Tests Jest/RTL
```

---

## Adaptive Generation

| Detected | Customization |
|----------|--------------|
| "API" mentioned | Add API documentation subtask |
| "formulaire" | Add form validation subtask |
| "externe" / "tiers" | Add integration robustness |
| "performance" | Add optimization subtask |
| "sécurité" | Add security audit subtask |

---

## Finalisation Phase (Always)

```markdown
X. **Finalisation**
   - [ ] Tests unitaires
   - [ ] Tests d'intégration (si multi-composants)
   - [ ] Documentation technique
```

For Major, add:
```markdown
   - [ ] Documentation utilisateur
   - [ ] Plan de déploiement
```
