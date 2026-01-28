# Clarity Scoring

> Scoring system for input clarity assessment in brainstorm clarification phase.

## Clarity Score Formula

Score range: **0.0 - 1.0**

| Factor | Weight | Indicators |
|--------|--------|------------|
| Specificity | 0.3 | Named entities, concrete nouns |
| Completeness | 0.3 | Who, what, why present |
| Actionability | 0.2 | Verbs, outcomes mentioned |
| Context | 0.2 | Domain references, constraints |

### Calculation

```
clarity_score = (specificity × 0.3) + (completeness × 0.3)
              + (actionability × 0.2) + (context × 0.2)
```

---

## Score Thresholds

| Score Range | Level | Action |
|-------------|-------|--------|
| >= 0.8 | High clarity | Skip clarification, proceed to reformulation |
| 0.6 - 0.79 | Medium clarity | Light clarification (1-2 questions) |
| < 0.6 | Low clarity | Full clarification (2-3 questions) |

---

## Specificity Anchors (0.0 - 1.0)

| Score | Anchor | Examples |
|-------|--------|----------|
| **0.2** | Vague concept only | "improve the app" |
| **0.4** | General area identified | "improve login" |
| **0.6** | Specific feature named | "add OAuth login" |
| **0.8** | Feature with details | "add Google OAuth for admin users" |
| **1.0** | Fully specified | "add Google OAuth2 with refresh tokens for admin dashboard" |

**Indicators:**
- Named entities (Google, React, PostgreSQL)
- Concrete nouns (login, dashboard, API)
- Specific versions or technologies

---

## Completeness Anchors (0.0 - 1.0)

| Score | Anchor | Present Elements |
|-------|--------|------------------|
| **0.2** | Only topic | What (vague) |
| **0.4** | Topic + reason | What + Why |
| **0.6** | Topic + reason + target | What + Why + Who |
| **0.8** | + constraints | What + Why + Who + limits |
| **1.0** | Full picture | What + Why + Who + limits + success |

**Checklist:**
- [ ] What: Feature/change described
- [ ] Why: Problem/need explained
- [ ] Who: Users/stakeholders identified
- [ ] Limits: Constraints mentioned
- [ ] Success: Outcome defined

---

## Actionability Anchors (0.0 - 1.0)

| Score | Anchor | Examples |
|-------|--------|----------|
| **0.2** | Abstract wish | "would be nice to have" |
| **0.4** | Direction indicated | "we should improve" |
| **0.6** | Verb + object | "implement OAuth" |
| **0.8** | Verb + object + qualifier | "implement Google OAuth this sprint" |
| **1.0** | Clear action with scope | "implement Google OAuth for admin panel with 2-week deadline" |

**Indicators:**
- Action verbs (implement, add, fix, create)
- Measurable outcomes
- Timeline references

---

## Context Anchors (0.0 - 1.0)

| Score | Anchor | Context Present |
|-------|--------|-----------------|
| **0.2** | No context | Standalone request |
| **0.4** | Domain mentioned | "for our e-commerce" |
| **0.6** | Technical context | "in our Django backend" |
| **0.8** | + existing constraints | "using existing User model" |
| **1.0** | Full ecosystem | "integrates with current auth, follows team patterns" |

**Indicators:**
- Technology stack references
- Existing system references
- Team/project patterns mentioned
- Integration points identified

---

## Question Mapping

Based on clarity score, generate appropriate questions:

| Score | Questions | Focus Categories |
|-------|-----------|------------------|
| < 0.6 | 3 questions | Scope, Users, Success |
| 0.6 - 0.8 | 2 questions | Scope, Constraints |
| > 0.8 | 1 question | Confirmation only |

### Question Categories

| Category | Question Pattern | Use When |
|----------|------------------|----------|
| **Scope** | "What's the boundary of this feature?" | Specificity low |
| **Users** | "Who is the primary user?" | Completeness low |
| **Constraints** | "Any technical or business constraints?" | Context low |
| **Success** | "How will you know it's successful?" | Actionability low |
| **Confirmation** | "Is this reformulation correct?" | High clarity |

---

## Turbo Mode Adjustments

When `--turbo` flag is active:

| Setting | Turbo Value |
|---------|-------------|
| Max questions | 2 |
| Focus categories | Scope + Priority only |
| Skip if score | >= 0.7 |

---

## EMS Integration

Initial EMS Clarity axis based on clarity_score:

| Clarity Score | Initial EMS Clarity |
|---------------|---------------------|
| >= 0.8 | 60 |
| 0.6 - 0.79 | 45 |
| 0.4 - 0.59 | 30 |
| < 0.4 | 20 |

After brief validation: Clarity += 20 (validated reformulation)

---

*Clarity Scoring v1.0 - EPCI Brainstorm v6.0*
