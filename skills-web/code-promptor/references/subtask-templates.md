# Subtask Templates — Auto-Generation Rules

> Intelligence for generating contextual subtasks even when not dictated

---

## Overview

Code-Promptor generates implementation subtasks automatically based on:
1. **Task type** (Bug, Feature, Refacto, etc.)
2. **Technical domain** (Backend, Frontend, DevOps)
3. **Technology stack** (Symfony, Django, React)

Subtasks are NOT dictated by user — they are intelligently suggested.

---

## Generation Rules

### When to Generate

| Complexity | Generate Subtasks? |
|------------|-------------------|
| Quick fix | ❌ No (too simple) |
| Standard | ✅ Yes (2-3 phases) |
| Major | ✅ Yes (5-6 phases) |

### Phase Structure

**Standard (4h)**: 2-3 phases
```
1. [Domain] — Core work
2. [Domain 2] — Secondary work (if multi-domain)
3. Finalisation
```

**Major (8h)**: 5-6 phases
```
1. Architecture & Préparation
2. Backend — Core Logic
3. Backend — Integration (if needed)
4. Frontend — Main Views
5. Frontend — Administration (if needed)
6. Finalisation
```

---

## Templates by Task Type

### 🐛 Bug Fix

```markdown
## Plan d'implémentation

1. **Diagnostic**
   - [ ] Reproduire le bug en local
   - [ ] Identifier la cause racine
   - [ ] Vérifier les logs/erreurs associés

2. **Correction**
   - [ ] Appliquer le correctif
   - [ ] Tester la correction
   - [ ] Vérifier les effets de bord

3. **Finalisation**
   - [ ] Ajouter test de non-régression
   - [ ] Documenter la cause si pertinent
```

### ✨ Feature (Standard)

```markdown
## Plan d'implémentation

1. **[Domain] — Développement principal**
   - [ ] Créer la structure de base
   - [ ] Implémenter la logique métier
   - [ ] Ajouter les validations

2. **Interface/API**
   - [ ] Exposer la fonctionnalité
   - [ ] Gérer les cas d'erreur
   - [ ] Documenter l'usage

3. **Finalisation**
   - [ ] Tests unitaires
   - [ ] Tests d'intégration
   - [ ] Documentation
```

### ✨ Feature (Major)

```markdown
## Plan d'implémentation

1. **Architecture & Préparation**
   - [ ] Définir le modèle de données
   - [ ] Créer les migrations
   - [ ] Documenter les interfaces

2. **Backend — Logique métier**
   - [ ] Créer le service principal
   - [ ] Implémenter les règles métier
   - [ ] Ajouter la validation des données

3. **Backend — Intégration**
   - [ ] Client API externe (si applicable)
   - [ ] Gestion erreurs et retry
   - [ ] Tâches asynchrones (si applicable)

4. **Frontend — Vues principales**
   - [ ] Composant/page principal
   - [ ] Formulaires et interactions
   - [ ] États de chargement/erreur

5. **Frontend — Administration**
   - [ ] Interface de configuration
   - [ ] Vues de monitoring

6. **Finalisation**
   - [ ] Tests unitaires (coverage >80%)
   - [ ] Tests d'intégration
   - [ ] Documentation technique
   - [ ] Documentation utilisateur
```

### 🔧 Refactoring

```markdown
## Plan d'implémentation

1. **Analyse**
   - [ ] Auditer le code existant
   - [ ] Identifier les dépendances
   - [ ] Définir la cible

2. **Refactoring**
   - [ ] Extraire/réorganiser le code
   - [ ] Appliquer les patterns
   - [ ] Nettoyer le code mort

3. **Finalisation**
   - [ ] Mettre à jour les tests
   - [ ] Vérifier les performances
   - [ ] Documenter les changements
```

### 🔌 Integration

```markdown
## Plan d'implémentation

1. **Préparation**
   - [ ] Analyser la documentation API
   - [ ] Obtenir les credentials de test
   - [ ] Définir le mapping de données

2. **Développement**
   - [ ] Créer le client API
   - [ ] Implémenter l'authentification
   - [ ] Mapper les données entrantes/sortantes

3. **Robustesse**
   - [ ] Gestion des erreurs API
   - [ ] Retry avec backoff
   - [ ] Logging et monitoring

4. **Finalisation**
   - [ ] Tests avec sandbox
   - [ ] Tests d'erreurs simulées
   - [ ] Documentation d'intégration
```

### 📚 Documentation

```markdown
## Plan d'implémentation

1. **Analyse**
   - [ ] Identifier le contenu à documenter
   - [ ] Définir le format et la structure
   - [ ] Collecter les informations

2. **Rédaction**
   - [ ] Rédiger le contenu principal
   - [ ] Ajouter exemples et illustrations
   - [ ] Réviser et corriger

3. **Publication**
   - [ ] Intégrer au système de doc
   - [ ] Valider les liens et références
   - [ ] Communiquer la disponibilité
```

---

## Templates by Domain

### Backend API

```markdown
1. **API — Endpoint**
   - [ ] Créer le controller/view
   - [ ] Définir la route et méthodes HTTP
   - [ ] Implémenter la validation des inputs
   - [ ] Configurer les permissions/auth

2. **API — Service**
   - [ ] Créer le service métier
   - [ ] Implémenter la logique
   - [ ] Gérer les erreurs métier

3. **API — Documentation**
   - [ ] Documenter l'endpoint (Swagger/OpenAPI)
   - [ ] Ajouter les exemples de requêtes
```

### Backend Service

```markdown
1. **Service — Structure**
   - [ ] Créer la classe de service
   - [ ] Définir l'interface/contrat
   - [ ] Configurer l'injection de dépendances

2. **Service — Logique**
   - [ ] Implémenter les méthodes principales
   - [ ] Ajouter la validation
   - [ ] Gérer les exceptions

3. **Service — Tests**
   - [ ] Tests unitaires
   - [ ] Mocks des dépendances
```

### Frontend Component

```markdown
1. **Composant — Structure**
   - [ ] Créer le composant
   - [ ] Définir les props/interface
   - [ ] Implémenter le rendu de base

2. **Composant — Logique**
   - [ ] Ajouter la gestion d'état
   - [ ] Implémenter les interactions
   - [ ] Gérer les cas limites

3. **Composant — Style**
   - [ ] Appliquer les styles (CSS/Tailwind)
   - [ ] Assurer le responsive
   - [ ] Vérifier l'accessibilité
```

### Frontend Page

```markdown
1. **Page — Layout**
   - [ ] Créer la structure de page
   - [ ] Configurer le routing
   - [ ] Intégrer dans la navigation

2. **Page — Contenu**
   - [ ] Intégrer les composants
   - [ ] Connecter aux données
   - [ ] Gérer les états (loading, error, empty)

3. **Page — Interactions**
   - [ ] Implémenter les actions utilisateur
   - [ ] Gérer les formulaires
   - [ ] Ajouter les feedbacks visuels
```

---

## Templates by Stack

### Symfony

```markdown
1. **Symfony — Backend**
   - [ ] Créer l'Entity avec annotations
   - [ ] Générer la migration Doctrine
   - [ ] Créer le Repository avec méthodes custom
   - [ ] Implémenter le Service

2. **Symfony — Controller**
   - [ ] Créer le Controller avec routes
   - [ ] Ajouter le Form Type (si formulaire)
   - [ ] Configurer la validation (Assert)
   - [ ] Implémenter les réponses JSON/Twig
```

### Django

```markdown
1. **Django — Models**
   - [ ] Définir le Model avec champs
   - [ ] Créer et appliquer la migration
   - [ ] Ajouter les méthodes de manager

2. **Django — Views**
   - [ ] Créer la View/ViewSet
   - [ ] Implémenter le Serializer
   - [ ] Configurer les URLs
   - [ ] Ajouter les permissions

3. **Django — Async** (si applicable)
   - [ ] Créer la tâche Celery
   - [ ] Configurer le scheduling
```

### React

```markdown
1. **React — Component**
   - [ ] Créer le composant fonctionnel
   - [ ] Définir les types/interfaces TypeScript
   - [ ] Implémenter avec hooks (useState, useEffect)

2. **React — State Management**
   - [ ] Créer le hook custom (si logique réutilisable)
   - [ ] Connecter au Context/Redux (si global)

3. **React — Tests**
   - [ ] Tests Jest/RTL
   - [ ] Tests d'interactions
```

---

## Adaptive Generation

### Context Detection

The skill detects context from the dictation to customize subtasks:

| Detected | Customization |
|----------|--------------|
| "API" mentioned | Add API documentation subtask |
| "formulaire" mentioned | Add form validation subtask |
| "externe" / "tiers" | Add integration robustness subtasks |
| "performance" | Add optimization/profiling subtask |
| "sécurité" | Add security audit subtask |
| "migration" | Add rollback plan subtask |

### Example

**Dictation**: "Créer l'API d'export PDF avec gestion des gros fichiers"

**Detected**: API + PDF + "gros fichiers" (performance concern)

**Generated subtasks include**:
```markdown
- [ ] Configurer les headers de réponse (Content-Type, Content-Disposition)
- [ ] Implémenter le streaming pour gros fichiers
- [ ] Ajouter timeout et limite de taille
```

---

## Finalisation Phase (Always)

Every Standard/Major brief ends with:

```markdown
X. **Finalisation**
   - [ ] Tests unitaires
   - [ ] Tests d'intégration (si multi-composants)
   - [ ] Documentation technique
   - [ ] Revue de code (si équipe)
```

For Major features, add:
```markdown
   - [ ] Documentation utilisateur
   - [ ] Plan de déploiement
```
