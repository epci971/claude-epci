# Categories & Detection Logic

> Reference for automatic brainstorming type detection and pivot criteria

---

## Brainstorming Types

| Type | Description | Primary Focus |
|------|-------------|---------------|
| **Technical** | Architecture, code, infrastructure, APIs, performance | How to build it |
| **Business** | Strategy, process, organization, clients, market | Why and for whom |
| **Creative** | Product, UX, content, design, innovation | What it could be |
| **Analytical** | Audit, comparison, evaluation, due diligence | What is the current state |

---

## Detection Indicators

### Technical Type

**Lexical signals** (weight: high):
- Architecture, API, database, backend, frontend
- Performance, scalability, security, infrastructure
- Integration, deployment, migration, refactoring
- Code, algorithm, protocol, framework, library
- Stack, server, endpoint, microservice

**Structural signals** (weight: medium):
- Technical constraints mentioned
- System components discussed
- Performance metrics referenced
- Technical debt or legacy systems
- Code snippets or technical specifications

**Confidence threshold**: 3+ lexical signals OR 2 lexical + 1 structural

**Suggested frameworks**: Comparative Matrix, ADR (Architecture Decision Record)

---

### Business Type

**Lexical signals** (weight: high):
- Strategy, market, client, revenue, growth
- Process, workflow, organization, team
- ROI, budget, timeline, stakeholders
- Competition, positioning, value proposition
- KPI, metrics, conversion, retention

**Structural signals** (weight: medium):
- Business goals mentioned
- Financial considerations
- Stakeholder concerns
- Market dynamics discussed
- Revenue or cost implications

**Confidence threshold**: 3+ lexical signals OR 2 lexical + 1 structural

**Suggested frameworks**: SWOT, Business Model Canvas, Porter's Five Forces

---

### Creative Type

**Lexical signals** (weight: high):
- Product, feature, user experience, design
- Innovation, concept, prototype, MVP
- User, persona, journey, touchpoint
- Brand, content, messaging, storytelling
- Ideation, brainstorm, creative, novel

**Structural signals** (weight: medium):
- User needs emphasized
- Multiple solution options explored
- Aesthetic or emotional considerations
- Novel approaches sought
- "What if" questions prevalent

**Confidence threshold**: 3+ lexical signals OR 2 lexical + 1 structural

**Suggested frameworks**: Six Thinking Hats, Design Thinking, Crazy 8s

---

### Analytical Type

**Lexical signals** (weight: high):
- Audit, analysis, evaluation, assessment
- Compare, benchmark, criteria, metrics
- Strengths, weaknesses, risks, opportunities
- Due diligence, review, compliance
- Data, evidence, findings, conclusions

**Structural signals** (weight: medium):
- Existing state examined
- Criteria-based evaluation
- Multiple options compared
- Evidence-based conclusions
- Objective assessment requested

**Confidence threshold**: 3+ lexical signals OR 2 lexical + 1 structural

**Suggested frameworks**: SWOT, Weighted Criteria Grid, Gap Analysis

---

## Detection Algorithm

```
1. SCAN input for lexical signals
   │
   ├─ Count matches per type
   ├─ Weight domain-specific terms higher (×1.5)
   └─ Track signal density (signals per 100 words)

2. ANALYZE structure signals
   │
   ├─ Check for type-specific patterns
   ├─ Consider context and constraints
   └─ Note explicit type mentions ("technical challenge", "business decision")

3. CALCULATE confidence scores
   │
   ├─ Technical: (lexical_count × 1.0) + (structural_count × 0.5)
   ├─ Business: (lexical_count × 1.0) + (structural_count × 0.5)
   ├─ Creative: (lexical_count × 1.0) + (structural_count × 0.5)
   └─ Analytical: (lexical_count × 1.0) + (structural_count × 0.5)

4. DETERMINE primary type
   │
   ├─ Highest score = primary type
   ├─ If top two within 20% → hybrid approach
   └─ If all scores < 2.0 → ask user or use Analytical default

5. SELECT secondary type (if applicable)
   │
   ├─ Second highest if score > 50% of primary
   └─ Combine framework suggestions from both

6. CONFIDENCE LEVELS
   │
   ├─ High (score ≥ 4.0): State type confidently
   ├─ Medium (2.0-3.9): State type with "appears to be"
   └─ Low (< 2.0): Ask user to confirm type
```

---

## Hybrid Detection

Some brainstorms span multiple types:

| Combination | Example | Approach |
|-------------|---------|----------|
| Technical + Business | "New API that increases revenue" | Lead with Technical, include Business metrics |
| Creative + Technical | "Innovative feature implementation" | Lead with Creative, ground with Technical constraints |
| Business + Analytical | "Market entry strategy with competitor analysis" | Interleave both frameworks |
| Analytical + Technical | "System audit with architecture recommendations" | Analytical first, Technical solutions |

**Hybrid indicator phrases**:
- "...but also need to consider..." → Second type follows
- "From a [type] perspective..." → Explicit type mention
- "Both [type1] and [type2]..." → Confirmed hybrid

---

## Type-Specific Question Patterns

### Technical Questions
- "What are the technical constraints?"
- "What systems need to integrate?"
- "What's the expected load/scale?"
- "What's the current tech stack?"
- "What are the security requirements?"

### Business Questions
- "Who is the target audience?"
- "What's the business objective?"
- "What's the budget/timeline?"
- "Who are the stakeholders?"
- "What's the expected ROI?"

### Creative Questions
- "What problem does this solve for users?"
- "What would the ideal experience look like?"
- "What makes this different from alternatives?"
- "What emotional response should it trigger?"
- "What constraints can we challenge?"

### Analytical Questions
- "What criteria matter most?"
- "What's the current baseline?"
- "What data do we have?"
- "What are the key trade-offs?"
- "What evidence supports this?"

---

## Pivot Detection Criteria

### When to Suggest Pivot

**Quantitative triggers**:
| Trigger | Threshold | Action |
|---------|-----------|--------|
| Off-topic responses | >50% of user's last 3 responses drift from original topic | Suggest pivot |
| Sub-topic engagement | Deep dive generates 2× more content than main thread | Suggest pivot |
| Type mismatch | Detected type changes significantly mid-session | Suggest reframing |

**Qualitative triggers**:
- User says: "actually...", "the real question is...", "what I really need..."
- User shows frustration with current direction
- Deep dive reveals root cause different from stated problem
- Success criteria seem misaligned with exploration direction

### Pivot Suggestion Format

```
💡 **Pivot suggestion**

I notice our exploration is gravitating toward [new topic] rather than [original topic].

This could mean:
- [New topic] is the real underlying question
- [Original topic] depends on solving [new topic] first
- We should split this into two separate brainstorms

Options:
→ `pivot` — Reorient to focus on [new topic]
→ `continue` — Stay on [original topic], note [new topic] for later
→ `split` — Create checkpoint for [original], start fresh on [new topic]
```

### Pivot Execution

When user confirms pivot:
1. Document the pivot in journal (from → to → reason)
2. Reformulate the new topic
3. Re-evaluate type detection
4. Adjust template if needed
5. Reset iteration counter with note: "Iteration 1 (post-pivot)"
6. Preserve relevant context from pre-pivot exploration

---

## Override Behavior

User can force type detection:
- "This is a technical brainstorm" → Force Technical
- "Focus on the business aspects" → Force Business
- "Let's be creative here" → Force Creative
- "I need an analysis" → Force Analytical

When overridden:
1. Acknowledge the override
2. Adjust question patterns to match type
3. Adjust framework suggestions to match type
4. Adjust report structure emphasis to match type
5. Note override in journal metadata

---

## History Search Relevance

### Relevance Scoring for Past Conversations

| Factor | Weight | Scoring |
|--------|--------|---------|
| Topic similarity | 40% | Semantic match 0-100% |
| Recency | 25% | Last week: 100%, Last month: 70%, Older: 40% |
| Outcome usefulness | 20% | Had decisions: +30%, Had actions: +20% |
| Same type | 15% | Same type: 100%, Related: 50%, Different: 0% |

**Relevance threshold**: 70%+ to surface in initialization

### What to Extract from History

If relevant history found:
- Key decisions made previously
- Open questions left unresolved
- Relevant context/constraints discovered
- Actions that were planned (check if completed)

### History Search Presentation

```
📚 **Relevant past exploration found**

On [date], we discussed [related topic]:
- Key decision: [decision]
- Open question: [question still relevant?]
- Context: [relevant constraint or insight]

Should we build on this, or start fresh?
```
