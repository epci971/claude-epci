---
name: code-conventions
description: >-
  Conventions de code génériques et bonnes pratiques. Nommage, structure de
  fichiers, commentaires, gestion d'erreurs. Use when: implémentation Phase 2,
  review de code. Not for: conventions spécifiques stack (→ skills stack).
---

# Code Conventions

## Overview

Conventions de code universelles pour un code lisible et maintenable.

## Nommage

| Élément | Convention | Exemple |
|---------|------------|---------|
| Classes | PascalCase | `UserService` |
| Méthodes | camelCase | `getUserById()` |
| Variables | camelCase | `$userName` |
| Constantes | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| Fichiers | kebab-case ou PascalCase | `user-service.ts` |
| Bases de données | snake_case | `user_accounts` |

### Règles de nommage

| Règle | Bon | Mauvais |
|-------|-----|---------|
| Explicite | `getUserEmailById` | `get` |
| Pas d'abbréviations | `configuration` | `cfg` |
| Verbes pour actions | `calculateTotal()` | `total()` |
| Noms pour données | `userCount` | `countUser` |
| Booléens avec is/has | `isActive`, `hasPermission` | `active`, `permission` |

## Structure de fichier

### Ordre dans une classe

```
1. Constantes
2. Propriétés statiques
3. Propriétés d'instance
4. Constructeur
5. Méthodes publiques
6. Méthodes protégées
7. Méthodes privées
```

### Limites de taille

| Élément | Idéal | Maximum |
|---------|-------|---------|
| Fonction | < 20 lignes | 50 lignes |
| Classe | < 200 lignes | 400 lignes |
| Fichier | < 300 lignes | 500 lignes |
| Paramètres | ≤ 3 | 5 |
| Niveaux d'indentation | ≤ 3 | 4 |

## Gestion d'erreurs

### DO ✅

```
- Fail fast (valider en entrée)
- Exceptions typées et spécifiques
- Messages d'erreur explicites avec contexte
- Logging structuré des erreurs
- Recovery strategy quand possible
```

### DON'T ❌

```
- Catch vide (swallow exceptions)
- Exception générique partout
- Retourner null pour les erreurs
- Ignorer les erreurs
- Log sans contexte
```

### Pattern de gestion

```
try {
    // Code à risque
} catch (SpecificException $e) {
    // Log avec contexte
    $this->logger->error('Operation failed', [
        'operation' => 'create_user',
        'error' => $e->getMessage(),
        'context' => $context
    ]);
    // Rethrow ou recover
    throw new DomainException('User creation failed', 0, $e);
}
```

## Commentaires

| Type | Quand | Format |
|------|-------|--------|
| Doc | API publique | `/** @param ... @return ... */` |
| TODO | Amélioration future | `// TODO: [ticket] description` |
| FIXME | Bug connu | `// FIXME: [ticket] description` |
| Inline | Logique complexe uniquement | `// Explication du pourquoi` |

### Règles commentaires

- **Commenter le POURQUOI**, pas le QUOI
- Éviter les commentaires évidents
- Mettre à jour les commentaires avec le code
- Préférer un code auto-documenté

## Principes DRY, KISS, YAGNI

| Principe | Signification | Check |
|----------|---------------|-------|
| **DRY** | Don't Repeat Yourself | Pas de copier-coller |
| **KISS** | Keep It Simple, Stupid | Solution la plus simple |
| **YAGNI** | You Aren't Gonna Need It | Pas de code "au cas où" |

## Quick Reference Checklist

| Règle | ✅ Check |
|-------|---------|
| Nommage explicite | Pas de `x`, `data`, `temp` |
| Une responsabilité | Fonction = 1 chose |
| Pas de magic numbers | Constantes nommées |
| Pas de duplication | Factoriser si > 2 occurrences |
| Gestion d'erreurs | Pas de catch vide |
| Taille raisonnable | Fonctions < 50 lignes |
| Indentation limitée | Max 4 niveaux |

## Code Smells à éviter

| Smell | Symptôme | Solution |
|-------|----------|----------|
| Long Method | > 50 lignes | Extract Method |
| Large Class | > 400 lignes | Extract Class |
| Feature Envy | Utilise trop une autre classe | Move Method |
| Data Clumps | Mêmes params répétés | Extract Class/DTO |
| Primitive Obsession | Trop de primitives | Value Objects |
| Switch Statements | Switch sur types | Polymorphisme |
