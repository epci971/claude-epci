# Cahier des Charges — F10: Flags Universels

> **Document**: CDC-F10-001
> **Version**: 1.0.0
> **Date**: 2025-12-15
> **Statut**: Validé
> **Feature ID**: F10
> **Version cible**: EPCI v3.1
> **Priorité**: P1
> **Source**: Analyse WD Framework v2.0 [NEW]

---

## 1. Contexte Global EPCI

### 1.1 Philosophie EPCI v4.0

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PHILOSOPHIE EPCI                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🎯 SIMPLICITÉ        — 5 commandes ciblées, pas 22                │
│  📋 TRAÇABILITÉ       — Feature Document pour chaque feature        │
│  ⏸️  BREAKPOINTS       — L'humain valide entre les phases           │
│  🔄 TDD               — Red → Green → Refactor systématique         │
│  🧩 MODULARITÉ        — Skills, Agents, Commands séparés            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 État Actuel (Baseline v3.0.0)

EPCI v3.0.0 a un seul flag binaire : `--large`. Ce n'est pas assez granulaire pour contrôler finement le comportement.

### 1.3 Glossaire Pertinent

| Terme | Définition |
|-------|------------|
| **Flag** | Option modifiant le comportement d'une commande |
| **Thinking Flag** | Flag contrôlant la profondeur d'analyse |
| **Auto-activation** | Activation automatique d'un flag basée sur le contexte |
| **Précédence** | Ordre de priorité entre flags conflictuels |

---

## 2. Description de la Feature

### 2.1 Contexte et Justification

**Source** : Analyse comparative WD Framework v2.0

**Problème** : Le flag `--large` actuel est :
- Binaire (on/off, pas de nuances)
- Manuel uniquement (pas d'auto-activation)
- Limité (ne couvre pas tous les cas)

**Solution** : Système de flags universels avec :
- 4 catégories de flags
- Auto-activation intelligente
- Règles de précédence claires
- Intégration avec toutes les commandes

### 2.2 Objectif

Permettre un **contrôle fin et intuitif** du comportement EPCI via des flags qui peuvent être :
1. Explicitement spécifiés par l'utilisateur
2. Auto-activés selon le contexte
3. Combinés selon des règles de précédence

---

## 3. Catégories de Flags

### 3.1 THINKING FLAGS — Profondeur d'analyse

```yaml
--think              # Standard (~4K tokens)
                     # Analyse multi-fichiers, dépendances directes
                     # Auto: 3-10 fichiers impactés

--think-hard         # Approfondi (~10K tokens)
                     # Analyse système entier, impacts indirects
                     # Auto: >10 fichiers OU refactoring OU migration

--ultrathink         # Critique (~32K tokens)
                     # Refonte majeure, décisions irréversibles
                     # JAMAIS auto (explicite uniquement)
```

### 3.2 COMPRESSION FLAGS — Gestion tokens

```yaml
--uc                 # Ultra-compressed output (30-50% tokens)
                     # Symboles: ✓/✗/⚠️, abréviations
                     # Auto: context > 75% utilisé

--verbose            # Output détaillé, explications complètes
                     # Opposé de --uc
```

### 3.3 WORKFLOW FLAGS — Contrôle exécution

```yaml
--safe               # Mode conservateur
                     # Toutes validations, confirmations supplémentaires
                     # Auto: production, données sensibles

--fast               # Skip validations optionnelles
                     # Pour itérations rapides en dev
                     # Incompatible avec --safe

--dry-run            # Simulation sans modifications
                     # Affiche ce qui serait fait
```

### 3.4 WAVE FLAGS — Orchestration multi-vagues

```yaml
--wave               # Active le découpage en vagues
                     # Pour features LARGE uniquement

--wave-strategy      # Stratégie de découpage
    progressive      # Itératif, validation entre vagues
    systematic       # Méthodique, analyse complète puis exécution
```

---

## 4. Auto-Activation

### 4.1 Règles d'Auto-Activation

| Flag | Condition | Seuil |
|------|-----------|-------|
| `--think` | Fichiers impactés | 3-10 fichiers |
| `--think-hard` | Fichiers OU refactoring | >10 fichiers OU migration |
| `--uc` | Context window usage | > 75% |
| `--safe` | Fichiers sensibles | `**/auth/**`, `**/payment/**` |
| `--wave` | Complexité LARGE | score > 0.7 |

### 4.2 Algorithme d'Auto-Activation

```python
def auto_activate_flags(context: FeatureContext) -> List[str]:
    flags = []

    # Thinking flags
    file_count = len(context.impacted_files)
    if file_count > 10 or context.is_refactoring or context.is_migration:
        flags.append("--think-hard")
    elif file_count >= 3:
        flags.append("--think")

    # Compression flags
    if context.context_usage > 0.75:
        flags.append("--uc")

    # Safety flags
    sensitive_patterns = ["**/auth/**", "**/payment/**", "**/security/**"]
    if any(match(f, p) for f in context.files for p in sensitive_patterns):
        flags.append("--safe")

    # Wave flags
    if context.complexity_score > 0.7:
        flags.append("--wave")

    return flags
```

---

## 5. Règles de Précédence

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FLAG PRECEDENCE RULES                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Flags explicites > Auto-activation                             │
│  2. --safe > --fast (safety first)                                 │
│  3. Thinking: --ultrathink > --think-hard > --think                │
│  4. --uc auto-active si context > 75%                              │
│  5. --wave implicite si --think-hard + LARGE                       │
│                                                                     │
│  CONFLITS                                                          │
│  ├── --safe + --fast → Erreur, incompatible                        │
│  ├── --uc + --verbose → --verbose gagne (explicite)                │
│  └── --think + --think-hard → --think-hard gagne                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.1 Matrice de Compatibilité

| Flag A | Flag B | Résultat |
|--------|--------|----------|
| `--safe` | `--fast` | ❌ Erreur |
| `--uc` | `--verbose` | B gagne si explicite |
| `--think` | `--think-hard` | B gagne |
| `--think-hard` | `--ultrathink` | B gagne |
| `--wave` | `--safe` | ✅ Compatible (validation entre vagues) |
| `--dry-run` | Tout | ✅ Compatible |

---

## 6. Intégration Commandes

### 6.1 Exemples d'Usage

```bash
# Équivalent ancien --large
/epci --think-hard --wave

# Feature sécurité avec toutes validations
/epci --persona-security --think-hard --safe

# Quick fix sans overhead
/epci-quick --fast

# Refonte majeure
/epci --ultrathink --wave-strategy systematic

# Debug avec analyse approfondie
/epci-spike 1h --think-hard "Pourquoi les perfs sont dégradées?"

# Simulation avant exécution
/epci --dry-run
```

### 6.2 Affichage Flags Actifs

À chaque commande, afficher les flags actifs :

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🚀 EPCI Workflow — user-preferences                                │
├─────────────────────────────────────────────────────────────────────┤
│ FLAGS: --think-hard (auto) | --safe (auto) | --wave (explicit)     │
│ PERSONA: --persona-backend (auto)                                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 7. Documentation des Flags

### 7.1 Fichier `settings/flags.md`

```markdown
# EPCI Flags Reference

## Thinking Flags
| Flag | Tokens | Auto-Trigger | Usage |
|------|--------|--------------|-------|
| --think | ~4K | 3-10 files | Standard analysis |
| --think-hard | ~10K | >10 files, refactor | Deep analysis |
| --ultrathink | ~32K | Never | Critical decisions |

## Compression Flags
| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| --uc | 30-50% reduction | context > 75% |
| --verbose | Full details | Never |

## Workflow Flags
| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| --safe | Max validation | Sensitive files |
| --fast | Skip optional | Never |
| --dry-run | Simulate only | Never |

## Wave Flags
| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| --wave | Enable waves | score > 0.7 |
| --wave-strategy | progressive/systematic | With --wave |

## Precedence Rules
1. Explicit > Auto
2. Safety > Speed
3. Higher thinking > Lower
```

---

## 8. Critères d'Acceptation

| ID | Critère | Méthode de vérification |
|----|---------|-------------------------|
| F10-AC1 | Tous flags documentés | `settings/flags.md` existe |
| F10-AC2 | Auto-activation fonctionne | Tests automatisés |
| F10-AC3 | Précédence respectée | Tests conflits |
| F10-AC4 | Intégration toutes commandes | Test chaque commande |
| F10-AC5 | --uc réduit tokens | Mesure avant/après |

---

## 9. Dépendances

### 9.1 Dépendances Entrantes (cette feature dépend de)

| Feature | Type | Description |
|---------|------|-------------|
| Aucune | — | Feature fondamentale indépendante |

### 9.2 Dépendances Sortantes (dépendent de cette feature)

| Feature | Type | Description |
|---------|------|-------------|
| F03 Breakpoints | Faible | Affichage flags dans breakpoints |
| F07 Orchestration | Forte | Flags contrôlent mode orchestration |
| F09 Personas | Faible | `--persona-X` intégré |
| F11 Wave | Forte | `--wave*` flags |

---

## 10. Effort Estimé

| Tâche | Effort |
|-------|--------|
| Documentation flags | 4h |
| Parsing flags | 4h |
| Auto-activation | 6h |
| Intégration commandes | 6h |
| Tests | 4h |
| **Total** | **24h (3j)** |

---

## 11. Livrables

1. `settings/flags.md` — Documentation complète
2. Module de parsing des flags
3. Module d'auto-activation
4. Intégration avec toutes les commandes EPCI
5. Tests unitaires et d'intégration

---

## 12. Migration depuis `--large`

| Ancien | Nouveau équivalent |
|--------|-------------------|
| `--large` | `--think-hard --wave` |
| (pas d'équivalent) | `--think` |
| (pas d'équivalent) | `--ultrathink` |
| (pas d'équivalent) | `--safe` |
| (pas d'équivalent) | `--fast` |

---

## 13. Hors Périmètre

- Flags persistants par projet (géré par Project Memory)
- Flags custom définis par l'utilisateur
- Interface graphique pour sélectionner les flags
- Historique des flags utilisés

---

*Document généré depuis CDC-EPCI-UNIFIE-v4.md*
