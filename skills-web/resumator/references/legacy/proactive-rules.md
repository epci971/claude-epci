# Proactive Rules Reference

> Rules for generating insights and suggestions

---

## Philosophy

Resumator v2.0.0 is **proactive**, not passive. It:
1. Suggests improvements participants may not have considered
2. Detects technical debt mentioned but not flagged
3. Captures ideas floated but not actioned
4. Enriches with research when valuable

**Key principle**: Always mark what comes from the skill vs. the source.

---

## Insight Categories

### 1. 🔧 Improvement Suggestions

**Purpose**: Proactively suggest optimizations.

| Pattern Detected | Suggestion |
|------------------|------------|
| Manual process | Suggest automation |
| File exchange (Excel, CSV) | Suggest direct integration |
| Multiple validations | Suggest workflow optimization |
| Repeated tasks | Suggest templating |
| Ad-hoc communication | Suggest notification system |
| No monitoring | Suggest logging/alerting |
| Hardcoded values | Suggest configuration |

**Format**:
```markdown
### 🔧 Improvement Suggestions

- **Automation opportunity**: Manual validation could use automated rules (e.g., auto-approve < €500)
- **Integration potential**: Excel exchange suggests need for direct API connector
```

**Rules**:
- Be specific, not generic
- Reference actual discussion
- Explain benefit
- Max 3-4 suggestions

---

### 2. 🔶 Technical Debt Detection

**Purpose**: Flag shortcuts and temporary solutions.

**Trigger phrases (French)**:
- "pour l'instant"
- "solution temporaire"
- "on verra plus tard"
- "workaround"
- "en attendant"
- "quick fix"
- "ça marche mais c'est pas propre"
- "on fait comme ça pour le moment"
- "c'est pas idéal mais"

**Trigger phrases (English)**:
- "for now"
- "temporary solution"
- "we'll fix it later"
- "workaround"
- "in the meantime"
- "quick fix"
- "it works but it's not clean"
- "not ideal but"

**Format**:
```markdown
### 🔶 Technical Debt Detected

- 🔶 "On fait comme ça pour l'instant" — Manual export; error risk
- 🔶 "Workaround en attendant la nouvelle API" — Deprecated dependency
```

**Rules**:
- Quote or paraphrase original
- Explain potential impact
- Don't judge, just flag
- Include all instances

---

### 3. 💭 Ideas to Explore

**Purpose**: Capture ideas not turned into actions.

**Detection patterns**:
- "On pourrait peut-être..." / "We could maybe..."
- "Ce serait bien de..." / "It would be nice to..."
- "J'ai pensé à..." / "I was thinking..."
- Ideas without group follow-up
- Suggestions with positive response but no action

**Format**:
```markdown
### 💭 Ideas to Explore

- 💭 Real-time dashboard for order tracking (Marie)
- 💭 Slack notifications for stock alerts (Pierre)
- 💭 Automated report generation (discussed, not assigned)
```

**Rules**:
- Attribute when identifiable
- Keep concise
- Include all floated ideas

---

### 4. 🌐 Skill Enrichments

**Purpose**: Add value through research and knowledge.

**When to enrich**:
- Unknown technical terms
- Tools/libraries without explanation
- Best practices for discussed patterns
- Current standards

**Format**:
```markdown
### 🌐 Skill Enrichments

- 🌐 *Context7 MCP*: Provides up-to-date docs for dev frameworks — Source: [URL]
- 🌐 *ETL Best Practice*: Standard pipelines include validation step — Source: [URL]
- ⚠️ *Diagram completion*: Added error handling per Django conventions
```

**Rules**:
- Always cite source URL for web research
- Mark 🌐 for web, ⚠️ for skill completion
- Keep relevant
- Max 2-3 unless highly relevant

---

## Confidence Levels

### High (Always Include)
- Explicit debt language ("workaround")
- Clear automation opportunities
- Explicit ideas ("I suggest...")

### Medium (Include with Caveat)
- Implicit inefficiencies
- Patterns that typically benefit from optimization
- Implied but not explicit ideas

### Low (Softer Phrasing)
- Potential issues that may be intentional
- Context-dependent suggestions

**Soft phrasing examples**:
- "This pattern sometimes benefits from..."
- "Depending on context, consider..."
- "If applicable, could be optimized by..."

---

## Formatting

### Section Structure

```markdown
## 💡 Insights & Leads

### 🔧 Improvement Suggestions
- **[Title]**: [Description]

### 💭 Ideas to Explore
- 💭 [Idea] ([attribution])

### 🔶 Technical Debt Detected
- 🔶 "[Quote]" — [Impact]

### 🌐 Skill Enrichments
- 🌐 *[Topic]*: [Info] — Source: [URL]
```

### Empty Sections

```markdown
### 🔶 Technical Debt Detected

[None explicitly mentioned]
```

---

## Quality Guidelines

### DO
- Be specific and actionable
- Reference actual discussion
- Explain the "why"
- Use clear indicators
- Keep practical

### DON'T
- Generate generic advice
- Overwhelm with suggestions
- Be judgmental
- Repeat other sections
- Assume business context

---

## Integration

### Link to Actions
```markdown
- **Automation opportunity**: Consider automating validation
  → *Could be added to Action Items*
```

### Link to Open Questions
```markdown
- **Integration potential**: API connection could replace Excel
  → *Depends on: API availability (see Open Questions)*
```

### Link to Next Meeting
```markdown
## 🔜 Next Meeting Suggestions

- [ ] Discuss validation automation (see Insights)
- [ ] Review technical debt items
```
