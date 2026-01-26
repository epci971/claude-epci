# TDD Rules Reference

Règles du cycle TDD simplifié pour `/quick`: Red-Green-Verify (skip Refactor).

## Cycle TDD pour /quick

```
┌─────────────────────────────────────────────────────────────────┐
│                    TDD CYCLE (QUICK MODE)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌───────┐                                                      │
│   │  RED  │ ← Write test that FAILS                             │
│   └───┬───┘                                                      │
│       │ Test fails? ✓                                            │
│       ▼                                                          │
│   ┌───────┐                                                      │
│   │ GREEN │ ← Write MINIMAL code to pass                        │
│   └───┬───┘                                                      │
│       │ Test passes? ✓                                           │
│       ▼                                                          │
│   ┌────────┐                                                     │
│   │ VERIFY │ ← Run ALL tests + lint                             │
│   └───┬────┘                                                     │
│       │ All pass? ✓                                              │
│       ▼                                                          │
│     DONE                                                         │
│                                                                  │
│   ┌──────────┐                                                   │
│   │ REFACTOR │ ← SKIP (speed > perfection)                      │
│   └──────────┘   Use /refactor later if needed                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Différence avec /implement

| Phase | /quick | /implement |
|-------|--------|------------|
| RED | Obligatoire | Obligatoire |
| GREEN | Obligatoire | Obligatoire |
| REFACTOR | **SKIP** | Obligatoire |
| VERIFY | Obligatoire | Obligatoire |

**Rationale**: Pour /quick, la vitesse est prioritaire. Le refactoring peut être fait plus tard avec `/refactor`.

## Phase RED

### Objectif
Écrire un test qui décrit le comportement attendu et **échoue**.

### Règles
1. Test doit être spécifique et ciblé
2. Test doit échouer pour la bonne raison
3. Si le test passe immédiatement → le test est mauvais

### Exemple (Jest)

```typescript
// LoginButton.test.tsx
describe('LoginButton', () => {
  it('should be horizontally centered', () => {
    render(<LoginButton />);
    const button = screen.getByRole('button');
    const styles = window.getComputedStyle(button.parentElement);
    expect(styles.display).toBe('flex');
    expect(styles.justifyContent).toBe('center');
  });
});
```

### Vérification
```bash
npm test -- --testPathPattern="LoginButton"
# Expected: FAIL
```

## Phase GREEN

### Objectif
Écrire le **minimum de code** pour faire passer le test.

### Règles
1. Code minimal uniquement
2. Pas d'optimisation prématurée
3. Pas de features supplémentaires
4. Suivre les patterns existants

### Exemple

```typescript
// LoginButton.tsx
export function LoginButton() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center' }}>
      <button>Login</button>
    </div>
  );
}
```

### Vérification
```bash
npm test -- --testPathPattern="LoginButton"
# Expected: PASS
```

## Phase VERIFY

### Objectif
S'assurer que le changement ne casse rien d'autre.

### Actions
1. Exécuter **tous** les tests (pas seulement les nouveaux)
2. Exécuter le linter
3. Vérifier qu'il n'y a pas de régressions

### Commandes par Stack

| Stack | Test Command | Lint Command |
|-------|--------------|--------------|
| JavaScript/React | `npm test` | `npm run lint` |
| Python/Django | `pytest` | `ruff check .` |
| PHP/Symfony | `./vendor/bin/phpunit` | `./vendor/bin/php-cs-fixer check` |
| Java/Spring | `./gradlew test` | `./gradlew checkstyle` |

## Gestion des Échecs

### Test échoue en GREEN

```
RETRY PROTOCOL (max 2):
├── Attempt 1: Analyser l'erreur, ajuster le code
│   └─ Re-run test
├── Attempt 2: Approche différente
│   └─ Re-run test
└── Attempt 3: ESCALATE
    └─ Options: /debug, investigation manuelle, abort
```

### Régression en VERIFY

Si un test existant échoue après le changement :

1. **Identifier** le test qui régresse
2. **Analyser** pourquoi le changement l'affecte
3. **Décider**:
   - Ajuster le nouveau code pour ne pas casser l'ancien
   - Ou mettre à jour le test existant si le comportement change intentionnellement

## Bonnes Pratiques

### DO
- Écrire des tests petits et focalisés
- Nommer les tests clairement (describe what, not how)
- Utiliser des assertions spécifiques
- Suivre les conventions de test du projet

### DON'T
- Écrire des tests qui testent plusieurs choses
- Hardcoder des valeurs qui pourraient changer
- Tester l'implémentation plutôt que le comportement
- Ignorer les tests qui échouent

## Exemples de Tests par Stack

### Python/pytest

```python
def test_user_email_validation():
    """Email validation rejects invalid format."""
    user = User(email="invalid")
    with pytest.raises(ValidationError):
        user.full_clean()
```

### PHP/PHPUnit

```php
public function testUserEmailValidation(): void
{
    $this->expectException(ValidationException::class);
    $user = new User();
    $user->setEmail('invalid');
    $user->validate();
}
```

### Java/JUnit

```java
@Test
void userEmailValidation_invalidFormat_throwsException() {
    User user = new User();
    user.setEmail("invalid");
    assertThrows(ValidationException.class, user::validate);
}
```

## Intégration avec tdd-enforcer

Le core skill `tdd-enforcer` est invoqué automatiquement en mode "guided" :

```python
# Mode for /quick
tdd_config = {
    "mode": "guided",      # Remind but allow skip with confirmation
    "skip_refactor": True, # Skip refactor phase
    "max_retries": 2       # Max retry attempts before escalation
}
```
