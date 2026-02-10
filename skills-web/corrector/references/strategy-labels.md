# Strategy Labels Reference

> Catalog of goal-oriented variant labels organized by intent and stakes level

---

## Core Principle

Labels describe **what the variant prioritizes or trades off**, not its formality level. The user should be able to choose a variant based on the label alone, without reading the content.

**Label format**: 2-4 words, action/goal-oriented.

---

## Labels by Intent

### Follow-up / Reminder

| Stakes | Label A | Label B | Label C | Label D |
|--------|---------|---------|---------|---------|
| Transactional | "Concise and clear" | "Warmer" | — | — |
| Relational | "Polite and direct" | "Create urgency" | "Leave the door open" | — |
| High-tension | "Cordial reminder" | "Soft formal notice" | "Last resort" | "Escalate" |

### Decline / Refusal

| Stakes | Label A | Label B | Label C | Label D |
|--------|---------|---------|---------|---------|
| Transactional | "Brief and clear" | "Softer" | — | — |
| Relational | "Firm and clear" | "Soften the blow" | "Suggest alternative" | — |
| High-tension | "Non-negotiable" | "Diplomatic" | "Preserve relationship" | "Defer decision" |

### Proposal / Suggestion

| Stakes | Label A | Label B | Label C | Label D |
|--------|---------|---------|---------|---------|
| Transactional | "Straight to the point" | "More engaging" | — | — |
| Relational | "Confident pitch" | "Collaborative approach" | "Low-pressure" | — |
| High-tension | "Bold proposal" | "Build consensus" | "Test the waters" | — |

### Negotiation

| Stakes | Label A | Label B | Label C | Label D |
|--------|---------|---------|---------|---------|
| Relational | "Hold position" | "Offer compromise" | "Create urgency" | — |
| High-tension | "Stand firm" | "Meet halfway" | "Strategic concession" | "Walk-away signal" |

### Bad News / Difficult Message

| Stakes | Label A | Label B | Label C | Label D |
|--------|---------|---------|---------|---------|
| Relational | "Direct and factual" | "Empathetic" | "Solution-focused" | — |
| High-tension | "Rip the bandaid" | "Cushion the impact" | "Frame as opportunity" | "Apologetic" |

### Request / Ask

| Stakes | Label A | Label B | Label C | Label D |
|--------|---------|---------|---------|---------|
| Transactional | "Efficient" | "Warmer" | — | — |
| Relational | "Direct ask" | "Give context first" | "Make it easy to say yes" | — |
| High-tension | "Assertive" | "Humble request" | "Justify thoroughly" | — |

### Thank You / Acknowledgment

| Stakes | Label A | Label B | Label C |
|--------|---------|---------|---------|
| Transactional | "Quick thanks" | "Genuine warmth" | — |
| Relational | "Professional gratitude" | "Personal touch" | "Pay it forward" |

### Feedback / Criticism

| Stakes | Label A | Label B | Label C | Label D |
|--------|---------|---------|---------|---------|
| Relational | "Direct and constructive" | "Sandwich approach" | "Question-led" | — |
| High-tension | "Frank assessment" | "Diplomatic framing" | "Coach mindset" | "Written warning tone" |

### Apology

| Stakes | Label A | Label B | Label C |
|--------|---------|---------|---------|
| Transactional | "Quick acknowledgment" | "Take full responsibility" | — |
| Relational | "Own the mistake" | "Explain without excusing" | "Focus on fix" |
| High-tension | "Full accountability" | "Damage control" | "Restore trust" |

### Confirmation / Validation

| Stakes | Label A | Label B |
|--------|---------|---------|
| Transactional | "Short and clear" | "Reassuring" |
| Relational | "Confirm and build" | "Confirm with next steps" |

### Introduction / Cold Outreach

| Stakes | Label A | Label B | Label C |
|--------|---------|---------|---------|
| Relational | "Professional and concise" | "Personal connection" | "Value-first" |
| High-tension | "Authority positioning" | "Mutual benefit" | "Referral leverage" |

---

## Label Construction Rules

### DO
- Use active, specific language: "Create urgency", "Hold position"
- Describe the outcome or trade-off: "Preserve relationship", "Rip the bandaid"
- Keep labels self-explanatory: reader understands strategy without reading content
- Adapt to context: same intent can have different labels depending on stakes

### DON'T
- ❌ Use formality levels as labels: "Formal", "Informal", "Casual"
- ❌ Use vague descriptors: "Version A", "Alternative", "Option 2"
- ❌ Use single adjectives without context: "Nice", "Strong", "Soft"
- ❌ Repeat similar labels across variants: "Direct" and "Straight to the point" in same set

---

## Dynamic Label Generation

When the input doesn't match any predefined intent above, generate labels by asking:

1. **What does Variant A prioritize?** → Label A
2. **What does Variant B sacrifice that A doesn't?** → Label B
3. **What angle hasn't been covered?** → Label C

Example for an unusual context (responding to a neighbor complaint):
- "Acknowledge and de-escalate"
- "Set boundaries politely"
- "Propose mediation"

---

## Language Adaptation

Labels must be generated in the **same language as the user's input**.

### French equivalents for common labels

| English | French |
|---------|--------|
| Polite and direct | Poli et direct |
| Create urgency | Créer l'urgence |
| Hold position | Tenir sa position |
| Soften the blow | Adoucir le refus |
| Suggest alternative | Proposer une alternative |
| Rip the bandaid | Droit au but |
| Preserve relationship | Ménager la relation |
| Direct and factual | Direct et factuel |
| Warmer | Plus chaleureux |
| Solution-focused | Orienté solution |
| Stand firm | Ferme et clair |
| Meet halfway | Compromis |
