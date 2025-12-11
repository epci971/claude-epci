---
name: testing-strategy
description: >-
  Stratégies et patterns de test. Pyramide de tests, TDD, mocking, fixtures.
  Use when: Phase 2 implémentation, définir stratégie de test, review QA.
  Not for: outils spécifiques stack (→ skills stack).
---

# Testing Strategy

## Overview

Guide des stratégies de test pour un code fiable et maintenable.

## Pyramide de tests

```
         /\
        /E2E\        Peu, lents, coûteux
       /──────\
      /Integra-\     Quelques-uns, moyens
     /──tion────\
    /────────────\
   /    Unit      \  Beaucoup, rapides, peu coûteux
  /────────────────\
```

| Niveau | Quantité | Vitesse | Coût | Focus |
|--------|----------|---------|------|-------|
| Unit | 70% | < 10ms | Faible | Logique isolée |
| Integration | 20% | < 1s | Moyen | Composants ensemble |
| E2E | 10% | > 1s | Élevé | Flux utilisateur |

## Test-Driven Development (TDD)

### Cycle RED-GREEN-REFACTOR

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│   RED   │────►│  GREEN  │────►│REFACTOR │
│(test    │     │(code    │     │(amélio- │
│ échoue) │     │ minimal)│     │ rer)    │
└─────────┘     └─────────┘     └────┬────┘
     ▲                               │
     └───────────────────────────────┘
```

### Règles TDD

1. **Test AVANT le code** — Toujours
2. **Un seul test à la fois** — Focus
3. **Code minimal** — Juste pour faire passer le test
4. **Refactor si vert** — Jamais sur rouge

## Patterns de test

### Arrange-Act-Assert (AAA)

```php
public function testUserValidation(): void
{
    // Arrange - Setup
    $user = new User('test@example.com');

    // Act - Execute
    $result = $user->validate();

    // Assert - Verify
    $this->assertTrue($result);
}
```

### Given-When-Then (BDD)

```gherkin
Given un utilisateur avec email valide
When je valide l'utilisateur
Then la validation réussit
```

## Couverture de tests

### Ce qu'il faut tester

| Priorité | Type | Exemple |
|----------|------|---------|
| Haute | Happy path | Création réussie |
| Haute | Edge cases | Limites, null, empty |
| Haute | Error cases | Exceptions attendues |
| Moyenne | Boundary | Min, max, overflow |
| Basse | Corner cases | Combinaisons rares |

### Matrice de couverture

```
                    Input
                 Valid  Invalid
              ┌───────┬────────┐
Output  OK    │   ✅  │   ❌   │
              ├───────┼────────┤
        Error │   ❌  │   ✅   │
              └───────┴────────┘
```

## Mocking

### Quand mocker ✅

- Dépendances externes (API, DB, filesystem)
- Comportements lents ou coûteux
- Cas difficiles à reproduire (erreurs réseau)
- Services tiers non contrôlables

### Quand NE PAS mocker ❌

- Le code qu'on teste (SUT)
- Les value objects
- Les logiques simples
- Les dépendances internes stables

### Types de test doubles

| Type | Usage | Exemple |
|------|-------|---------|
| Dummy | Remplit paramètre | `new NullLogger()` |
| Stub | Retourne valeur fixe | `$mock->willReturn(42)` |
| Spy | Enregistre les appels | `$mock->expects($this->once())` |
| Mock | Vérifie comportement | `$mock->expects(...)->with(...)` |
| Fake | Implémentation simplifiée | `InMemoryRepository` |

## Fixtures et Factories

### Fixtures

```php
// Données statiques, prévisibles
$user = $this->fixtures->getReference('user-admin');
```

### Factories

```php
// Données dynamiques, flexibles
$user = UserFactory::new()
    ->admin()
    ->verified()
    ->create();
```

## Anti-patterns à éviter

| Anti-pattern | Problème | Solution |
|--------------|----------|----------|
| Test du mock | Teste l'implémentation | Tester le comportement |
| Test flaky | Passe/échoue aléatoirement | Éliminer dépendances temporelles |
| Test couplé | Dépend d'autres tests | Tests isolés |
| Test lent | Suite > 10 min | Plus de unit, moins d'E2E |
| Test fragile | Casse pour rien | Tester les contrats, pas l'implémentation |
| Over-mocking | Mock de tout | Préférer les vrais objets simples |

## Checklist avant merge

- [ ] Tests pour le happy path
- [ ] Tests pour les edge cases
- [ ] Tests pour les erreurs attendues
- [ ] Pas de tests qui dépendent d'autres tests
- [ ] Pas de tests flaky
- [ ] Tous les tests passent
- [ ] Coverage acceptable (>80% pour code critique)
