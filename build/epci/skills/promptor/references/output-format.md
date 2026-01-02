# Output Format — Brief Structure Reference

> 3 complexity levels with adaptive formatting

---

## Complexity Detection

| Level | Word Count | Verb Type | Time | Plan |
|-------|------------|-----------|------|------|
| **Quick fix** | < 50 | Corrective | 1h | No |
| **Standard** | 50-200 | Creative | 4h | Yes |
| **Major** | > 200 | Architectural | 8h | Yes (detailed) |

### Verb Classification

| Level | Verbs |
|-------|-------|
| Quick fix | corriger, fixer, débugger, réparer, ajuster |
| Standard | créer, ajouter, implémenter, développer |
| Major | concevoir, architecturer, refondre, migrer |

### Force Major Triggers

Even if < 200 words:
- Multiple external integrations
- Database schema changes
- Authentication/security changes
- Multi-domain (backend + frontend + devops)

---

## Common Header

```markdown
# [Title — Action Verb + Object]

📦 **[Complexity]** | ⏱️ [Time] | 🎯 Confidence: [HIGH|MEDIUM|LOW]
```

### Title Rules

- Start with action verb
- 5-12 words max
- No person references
- Specific, not generic

---

## Quick Fix (1h)

```markdown
# [Title]

📦 **Quick fix** | ⏱️ 1h | 🎯 Confidence: [LEVEL]

## Objectif
[2-3 sentences describing the fix]

## Contexte
[Where the issue occurs]

## Correction attendue
- [Action 1]
- [Action 2]
- [Verification step]

## Notes
- [Notes or "Aucune note complémentaire."]
```

**Characteristics**: No plan, ~100-150 words

---

## Standard (4h)

```markdown
# [Title]

📦 **Standard** | ⏱️ 4h | 🎯 Confidence: [LEVEL]

## Objectif
[2-4 sentences]

## Description
[1-2 paragraphs]

## Exigences fonctionnelles
- [FR1]
- [FR2]

## Contraintes techniques
- [Constraints or "Aucune contrainte explicitement mentionnée."]

## Plan d'implémentation

1. **[Phase 1]**
   - [ ] Subtask
   - [ ] Subtask

2. **Finalisation**
   - [ ] Tests
   - [ ] Documentation

## Notes
- [Notes or "Aucune note complémentaire."]
```

**Characteristics**: 2-3 phases, ~200-300 words

---

## Major (8h)

```markdown
# [Title]

📦 **Feature majeure** | ⏱️ 8h | 🎯 Confidence: [LEVEL]

## Objectif
[3-4 sentences]

## Description
[2-3 paragraphs]

## Exigences fonctionnelles
- [FR1-4]

## Exigences non-fonctionnelles
- [NFR1-2]

## Contraintes techniques
- [Technical constraints]

## Plan d'implémentation

1. **Architecture & Préparation**
   - [ ] Models, migrations
   
2. **Backend — Core Logic**
   - [ ] Service, business rules

3. **Backend — Integration**
   - [ ] External APIs

4. **Frontend — Main Views**
   - [ ] Components, interactions

5. **Finalisation**
   - [ ] Tests (coverage >80%)
   - [ ] Documentation

## Notes
- [Decisions, risks, dependencies]
```

**Characteristics**: 5-6 phases, ~400-500 words, NFR required

---

## Multi-Brief Separator

```markdown
═══════════════════════════════════════════════════════════════════
📋 TÂCHE 1/3 — Copier dans Notion
═══════════════════════════════════════════════════════════════════

[Brief 1]

═══════════════════════════════════════════════════════════════════
✅ 3 briefs générés — Prêts pour Notion
═══════════════════════════════════════════════════════════════════
```

---

## Absence Markers

| Section | Marker |
|---------|--------|
| FR | "Aucun FR explicitement mentionné." |
| NFR | "Aucun NFR explicitement mentionné." |
| Constraints | "Aucune contrainte technique explicitement mentionnée." |
| Notes | "Aucune note complémentaire." |
