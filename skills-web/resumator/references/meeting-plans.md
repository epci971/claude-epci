# Meeting Plans Reference

> 7 structured plans by meeting type + adaptation guidelines

---

## Plan Selection Logic

```
1. Scan content for type indicators
2. Match to closest plan type
3. If no clear match → Generic plan
4. Adapt sections to actual content
5. Apply v2.0.0 enhancements (diagrams, insights, glossary)
```

---

## Plan 1: Steering / Decision Meeting

**Indicators**: "decision", "validate", "arbitrate", "budget", "deadline", "go/no-go", "approval"

### Structure

```markdown
## 📌 Context
[Why this meeting, what needs decision]

## 🎯 Problem Statement
[Core issue requiring decision]

## 💡 Solutions Discussed
[Options analyzed]

## ✅ Decisions Made
[Clear decisions]

## 📝 Action Items
| Owner | Action | Deadline | Status |

## ⚠️ Watch Points
[Risks, dependencies, blockers]
```

**Diagram opportunities**: Decision trees, approval workflows

---

## Plan 2: Information Meeting

**Indicators**: "inform", "present", "update", "status", "progress", "announcement"

### Structure

```markdown
## 📌 Context
[Purpose and scope]

## 📢 Key Information
[Announcements and updates by topic]

## ⚠️ Watch Points
[Items requiring attention]

## ❓ Open Questions
[Unresolved questions]

## 📝 Action Items
| Owner | Action | Deadline | Status |
```

**Diagram opportunities**: Timelines, progress flows

---

## Plan 3: Brainstorming

**Indicators**: "ideas", "proposals", "explore", "brainstorm", "creative", "what if"

### Structure

```markdown
## 📌 Context
[Topic being explored]

## 💡 Ideas Discussed
[All ideas, grouped thematically]

## ⭐ Selected Leads
[Ideas for further exploration]

## 🚫 Discarded Leads
[Dismissed ideas and why]

## 📝 Next Steps
| Owner | Action | Deadline | Status |
```

**Diagram opportunities**: Mind maps, concept relationships

---

## Plan 4: Training / Workshop

**Indicators**: "training", "workshop", "exercise", "learn", "formation", "atelier"

### Structure

```markdown
## 🎯 Session Objectives
[Learning goals]

## 📚 Content Covered
[Topics by section]

## ❓ Questions Asked
[Participant questions with answers]

## 📌 Key Takeaways
[Summary of learning]

## 📝 Next Steps
| Owner | Action | Deadline | Status |
```

**Diagram opportunities**: Process demonstrations, procedures

---

## Plan 5: Individual Review / 1:1

**Indicators**: One-on-one, "feedback", "evaluation", "objectives", "performance", "1:1"

### Structure

```markdown
## 📌 Context
[Purpose, period covered]

## 💬 Feedback Exchanged
[Key feedback]

## ⭐ Strengths
[Identified strengths]

## 📈 Areas for Improvement
[Development areas]

## 🎯 Defined Objectives
[Goals for next period]

## 📝 Action Items
| Owner | Action | Deadline | Status |
```

**Diagram opportunities**: Development paths, skill maps

---

## Plan 6: Technical / Architecture Meeting

**Indicators**: "architecture", "design", "workflow", "API", "database", "ETL", "integration", "service", "component"

### Structure

```markdown
## 📌 Context
[Technical problem or design challenge]

## 🏗️ Architecture Discussed
[Systems, components, layers]

## 🔄 Flows & Processes
[Data flows, workflows, sequences]

## ⚙️ Technical Decisions
[Technology choices, patterns]

## ⚠️ Technical Risks
[Identified risks, dependencies]

## 📝 Action Items
| Owner | Action | Deadline | Status |
```

**Diagram opportunities (HIGH PRIORITY)**:
- System architecture (flowchart)
- Sequence diagrams for integrations
- ER diagrams for data models
- State diagrams for lifecycles
- Class diagrams for services
- Package structures

---

## Plan 7: Generic (Fallback)

**Use when**: No clear type, mixed content, unusual format

### Structure

```markdown
## 📌 Context
[Background and purpose]

## 💬 Topics Discussed
[Organized logically]

## ✅ Decisions Made
[Any decisions]

## 📝 Action Items
| Owner | Action | Deadline | Status |

## ⚠️ Watch Points
[Issues, concerns]

## ❓ Open Questions
[Unresolved items]
```

**Diagram opportunities**: Any detected flows

---

## Adaptation Guidelines

### Adding Sections

Add if content warrants:
- **💬 Key Quotes**: Notable statements
- **📊 Figures Mentioned**: Specific metrics
- **📅 Key Dates**: Timeline discussed
- **👥 Stakeholders**: Stakeholder mapping

### Handling Empty Sections

- Display "[No items identified]" or "[All resolved]"
- **Never skip Action Items** — show "No actions identified" if empty

### Merging Sections

If content overlaps:
- "Decisions" + "Actions" if decisions imply actions
- "Watch Points" + "Open Questions" → "Points of Attention"

---

## Action Item Extraction Rules

### Include ✅

- Explicit: "Jean will do X"
- Commitments: "I'll handle it"
- Deadlines: "by Friday"
- Requests: "Can you check Y?"
- Implicit: "we should..." with implied owner
- Follow-ups: "I'll send you..."

### Exclude ❌

- Vague: "We should think about..." (no owner)
- Past: "I already did X"
- Unassigned questions: "Who could...?" (unless answered)

### Deadline Format

| Mentioned | Format |
|-----------|--------|
| Specific | "December 15" |
| Relative | "Tomorrow", "Next week" |
| Vague | "Soon", "ASAP" |
| None | "-" |

### Owner Attribution

- Name if stated
- Role if unknown: "Tech lead"
- "Team" for collective
- "TBD" if unassigned

### Status Assignment

| Condition | Status |
|-----------|--------|
| Owner AND deadline | 🟢 |
| Owner OR deadline | 🟡 |
| Neither | 🔴 |

---

## v2.0.0 Enhancements (All Plans)

Always apply:
1. ✅ Detect and generate Mermaid diagrams
2. ✅ Generate proactive insights section
3. ✅ Extract glossary
4. ✅ Calculate action completeness score
5. ✅ Suggest next meeting topics
6. ✅ Flag technical debt
7. ✅ Include YAML metadata
8. ✅ Output as downloadable `.md` artifact
