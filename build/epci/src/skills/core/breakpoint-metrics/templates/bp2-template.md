# BP2 Template — Post-Phase 2 (Code Implémenté)

## Format

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT PHASE 2 — Code Implémenté                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📊 MÉTRIQUES                                                        │
│ ├── Tâches: {COMPLETED}/{TOTAL} complétées                         │
│ ├── Tests: {TEST_COUNT} {TEST_STATUS}                              │
│ ├── Coverage: {COVERAGE}%                                          │
│ └── Déviations: {DEVIATION_STATUS}                                 │
│                                                                     │
│ ✅ VALIDATIONS                                                      │
│ ├── @code-reviewer: {CR_VERDICT} ({CR_SUMMARY})                    │
│ ├── @security-auditor: {SA_VERDICT}                                │
│ └── @qa-reviewer: {QA_VERDICT}                                     │
│                                                                     │
│ 💡 SUGGESTIONS PROACTIVES (F06)                                     │
│ {SUGGESTIONS_SECTION}                                               │
│                                                                     │
│ 📋 PREVIEW PHASE 3                                                  │
│ ├── Commit structuré avec message conventionnel                    │
│ ├── Génération documentation (@doc-generator)                      │
│ └── Préparation PR                                                 │
│                                                                     │
│ 🔗 Feature Document: {FEATURE_DOC_PATH}                            │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ Options:                                                            │
│   • Tapez "Continuer" → Passer à Phase 3 (Finalisation)           │
│   • Tapez "Corriger issues" → Adresser les problèmes signalés     │
│   • Tapez "Voir rapports" → Afficher rapports des agents          │
│   • Tapez "Annuler" → Abandonner le workflow                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{COMPLETED}` | Tasks completed | 7 |
| `{TOTAL}` | Total tasks | 7 |
| `{TEST_COUNT}` | Number of tests | 12 |
| `{TEST_STATUS}` | Test result emoji + status | ✅ passing |
| `{COVERAGE}` | Code coverage percentage | 87 |
| `{DEVIATION_STATUS}` | Deviation summary | Aucune / 2 mineures documentées |
| `{CR_VERDICT}` | @code-reviewer result | APPROVED |
| `{CR_SUMMARY}` | Short summary | 0 Critical, 2 Minor |
| `{SA_VERDICT}` | @security-auditor result | PASSED / N/A |
| `{QA_VERDICT}` | @qa-reviewer result | PASSED / N/A |
| `{FEATURE_DOC_PATH}` | Relative path to Feature Doc | docs/features/user-auth.md |

## Verdict Display

### @code-reviewer

| Verdict | Display |
|---------|---------|
| APPROVED | `✅ @code-reviewer: APPROVED (0 Critical, X Minor)` |
| APPROVED_WITH_FIXES | `⚠️ @code-reviewer: APPROVED_WITH_FIXES (X issues)` |
| NEEDS_REVISION | `❌ @code-reviewer: NEEDS_REVISION (X Critical)` |

### @security-auditor (Conditional)

| Status | Display |
|--------|---------|
| Not invoked | `@security-auditor: N/A (non requis)` |
| PASSED | `✅ @security-auditor: PASSED` |
| WARNINGS | `⚠️ @security-auditor: WARNINGS (X)` |
| FAILED | `❌ @security-auditor: FAILED (X vulnérabilités)` |

### @qa-reviewer (Conditional)

| Status | Display |
|--------|---------|
| Not invoked | `@qa-reviewer: N/A (non requis)` |
| PASSED | `✅ @qa-reviewer: PASSED` |
| NEEDS_MORE_TESTS | `⚠️ @qa-reviewer: NEEDS_MORE_TESTS (X edge cases)` |

## Compact Version (for token optimization)

```
---
⏸️ **BP2 — Code Implémenté**
📊 {COMPLETED}/{TOTAL} tâches | {TEST_COUNT} tests {TEST_STATUS} | Coverage: {COVERAGE}%
✅ @code-reviewer: {CR_VERDICT} | @security-auditor: {SA_VERDICT} | @qa-reviewer: {QA_VERDICT}
📋 Preview Phase 3: Commit, docs, PR
🔗 {FEATURE_DOC_PATH}

→ "Continuer" | "Corriger" | "Rapports" | "Annuler"
---
```

## Conditional Sections

### When Critical Issues Found

```
│ 🚨 ISSUES CRITIQUES                                                 │
│ ├── {ISSUE_1_TITLE} (fichier:ligne)                                │
│ └── {ISSUE_2_TITLE} (fichier:ligne)                                │
│                                                                     │
│ ⚠️ Action requise: Corriger avant de continuer                     │
```

### When --large mode

All agents shown (not just conditional):

```
│ ✅ VALIDATIONS (mode --large: validation complète)                 │
│ ├── @code-reviewer: {CR_VERDICT}                                   │
│ ├── @security-auditor: {SA_VERDICT} (obligatoire)                 │
│ └── @qa-reviewer: {QA_VERDICT} (obligatoire)                      │
```

### When Tests Failing

```
│ 📊 MÉTRIQUES                                                        │
│ ├── Tâches: {COMPLETED}/{TOTAL} complétées                         │
│ ├── Tests: {TEST_COUNT} ❌ {FAILING_COUNT} failing                 │
│ └── ⚠️ Tests doivent passer avant continuation                     │
```

### Suggestions Section (F06)

When proactive suggestions are available from code review and pattern detection:

```
│ 💡 SUGGESTIONS PROACTIVES                                           │
│ ├── [P1] 🔒 Input non validé (src/Controller/User.php:42)          │
│ │   └── Suggestion: Ajouter validation Assert\Email                │
│ ├── [P2] ⚡ N+1 Query potentiel (src/Service/Order.php:87)         │
│ │   └── Suggestion: Utiliser JOIN FETCH                            │
│ └── [P3] 🧹 Magic number détecté (src/Calculator.php:15)           │
│     └── Suggestion: Extraire constante DISCOUNT_RATE               │
│     └── Actions: [Accepter tout] [Voir détails] [Ignorer]          │
```

When no suggestions:

```
│ 💡 SUGGESTIONS PROACTIVES                                           │
│ └── Aucune suggestion détectée                                     │
```

**Variables:**

| Variable | Description | Example |
|----------|-------------|---------|
| `{SUGGESTIONS_SECTION}` | Formatted suggestions from F06 engine | See above |

**BP2 suggestion types** (implementation phase):
- P1: Security issues (input validation, SQL injection, XSS, CSRF)
- P2: Performance (N+1, large payload), Quality (god class, long method)
- P3: Style (magic numbers, dead code)

**Suggestion Actions:**
- `[Accepter tout]` - Apply all auto-fixable suggestions
- `[Voir détails]` - Show full suggestion details
- `[Ignorer]` - Skip suggestions for this session
- Individual suggestion feedback tracked for learning (F08)
