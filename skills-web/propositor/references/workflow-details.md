# Workflow Details — Propositor

> Complete specifications for each phase and checkpoint format

---

## Pre-Workflow: Estimator Data Retrieval

### Mandatory Input

Propositor **cannot proceed** without valid Estimator output.

### Detection Logic

```
IF estimator_output in conversation_context
    → Parse automatically
    → Extract: charge_table, budget_table, features, stack
ELSE IF user_uploads_file
    → Validate format (look for ESTIMATOR tags)
    → Parse content
ELSE
    → Ask user: "Please provide the Estimator output (file or paste)"
    → Do NOT proceed until received
```

### Validation Checks

| Check | Criteria | Action |
|-------|----------|--------|
| Tags present | `<!-- ESTIMATOR_DATA_START/END -->` | Required |
| Data parseable | Valid Markdown tables | Required |
| Amounts coherent | Totals match | Warning if mismatch |

---

## Phase 1: Client Qualification

### Objective
Identify client context and calibrate proposal parameters.

### Qualification Questions

1. **Client name**: For personalization
2. **Client sector**: startup / PME / grand-compte / public / GMS / industriel
3. **Request context**: spontaneous / consultation / formal RFP
4. **Response deadline**: Urgency level
5. **References to include**: Similar projects (if any)

### Auto-Detection Logic

```
IF client_sector == "public" OR brief mentions "appel d'offres"
    → template = "ao-public"
    → tone = "formel"
    → detail_level = "very_detailed"

ELSE IF client_sector == "grand-compte"
    → template = auto_from_project_type
    → tone = "formel"
    → detail_level = "detailed"

ELSE IF client_sector == "startup"
    → template = auto_from_project_type
    → tone = "direct"
    → detail_level = "concise"

ELSE
    → template = auto_from_project_type
    → tone = "standard"
    → detail_level = "balanced"
```

### Template Auto-Selection from Project Type

| Estimator Project Type | Default Template |
|-----------------------|------------------|
| dev | `dev` |
| refonte | `refonte` |
| tma | `tma` |
| audit | `audit` |

### Coherence Validation

At this stage, validate Estimator data:

```markdown
⚠️ **Coherence Alerts**:

🔴 **Blocking**:
- Total (45,000 €) doesn't match lot sum (43,500 €)

🟡 **Warning**:
- Planning duration (8 weeks) seems short for 120 JH
- FCT-007 referenced but not documented

**Options:**
→ `corriger` — Return to Estimator for fixes
→ `ignorer` — Continue despite alerts (not recommended)
→ `détail` — See full inconsistency details
```

### Checkpoint 1 Format

```markdown
📍 Checkpoint 1 — Client Qualification

**Client identified**: [Name] — [Sector]
**Context**: [spontaneous/consultation/RFP]

**Auto-detected parameters**:
- Template: [dev/refonte/tma/audit/ao-public]
- Tone: [formel/standard/direct]
- Detail level: [concise/balanced/detailed/very_detailed]

**Estimator data imported**:
- Project: [Name]
- Recommended budget: XX XXX € HT
- Workload: XX JH (mid scenario)

✅ Coherence verified — No alerts
[OR]
⚠️ Alerts detected — See above

**Options:**
→ `valider` — Proceed to structure
→ `changer-template [name]` — Force different template
→ `changer-ton [level]` — Adjust formality
→ `question [topic]` — Clarify a point
```

---

## Phase 2: Structure & Outline

### Objective
Define the document structure adapted to template and client.

### Structure Selection

Based on template, present the adapted table of contents:

```markdown
**Template selected**: [name] — [short description]

**Proposed outline**:
1. [Section 1]
2. [Section 2]
3. [Section 3]
...

**Customizable sections**:
- Client references: [included/excluded]
- Team CVs: [included/excluded]
- Detailed technical annex: [included/excluded]
```

### Optional Sections

| Section | Default | When to Include |
|---------|---------|-----------------|
| References | ✅ Yes | Always unless `--no-references` |
| Team CVs | ❌ No | On request or `--with-cv` |
| Technical annex | ❌ No | Complex projects, public tenders |
| Gantt chart | ✅ if >30 JH | Projects with significant duration |

### Checkpoint 2 Format

```markdown
📍 Checkpoint 2 — Proposal Structure

**Template**: [name] — [description]

**Proposed outline**:
1. Page de garde
2. Synthèse exécutive
3. Compréhension du besoin
4. Solution proposée
5. Méthodologie
6. Planning
7. Équipe projet
8. Proposition financière
9. Conditions
10. Annexes

**Included options**:
- ✅ Gantt chart (XX JH > 30)
- ✅ Client references
- ❌ Team CVs

💡 **Suggestions**:
- Add a similar [sector] project reference?
- Include [certification] mention?

**Options:**
→ `valider` — Proceed to writing
→ `ajouter-section [name]` — Add a section
→ `supprimer-section [name]` — Remove a section
→ `ajouter-reference [project]` — Include a reference
```

---

## Phase 3: Section-by-Section Writing

### Objective
Generate content adapted to tone and client expectations.

### Writing Order

1. **Executive Summary** (most critical — optional checkpoint)
2. **Needs Understanding**
3. **Proposed Solution**
4. **Methodology**
5. **Planning** (with Gantt if applicable)
6. **Team**
7. **Financial Proposal**
8. **Conditions**
9. **Annexes**

### Section Guidelines

#### Executive Summary
- Length: 10-15 lines
- Content: Context + Solution + Key benefits + Budget/Timeline
- Tone: Adapted to client type
- A decision-maker should understand the offer from this section alone

#### Needs Understanding
- Source: Estimator context + Brainstormer report if available
- Structure: Context → Stakes → Objectives → Scope
- Show deep understanding of client's challenges

#### Proposed Solution
- Functional overview (high-level)
- Technical choices (from Estimator, with commercial arguments)
- Differentiators and added value
- Optional: architecture diagram

#### Methodology
- Approach: Agile / V-cycle / Hybrid (justify choice)
- Phases and milestones
- Governance (meetings, reporting)
- Risk management approach

#### Planning
- Gantt diagram (Mermaid) if >30 JH
- Key milestones table
- Dependencies highlighted

#### Team
- Profiles involved
- Roles and responsibilities
- Availability
- Optional: CVs in annex

#### Financial Proposal
- Summary table (from Estimator)
- Detail by lot
- Options (if any)
- Payment schedule

#### Conditions
- Validity period (default: 30 days)
- Client prerequisites
- IP clause
- Confidentiality
- Reference to GTC

### Optional Checkpoint 3 Format

```markdown
📍 Checkpoint 3 — Executive Summary Validation

**Generated summary**:
[Summary content]

**Applied tone**: [formel/standard/direct]

**This checkpoint is optional** — The executive summary is often the most critical section.

**Options:**
→ `valider` — Continue writing
→ `modifier` — Adjust the summary
→ `changer-ton [level]` — Reformulate with different tone
→ `skip-checkpoints` — Generate remaining sections without intermediate checkpoints
```

---

## Phase 4: Finalization

### Objective
Assemble, verify, and prepare for export.

### Assembly Actions

1. Combine all sections
2. Generate table of contents
3. Add page de garde
4. Include annexes
5. Final formatting

### Final Validation Checks

| Check | Criteria | Type |
|-------|----------|------|
| Amounts coherent | Match throughout document | Blocking |
| Dates realistic | Planning feasible | Warning |
| No placeholders | No [XXX] remaining | Blocking |
| References complete | All FCT-xxx documented | Warning |
| Spelling/grammar | Basic check | Info |

### Checkpoint Final Format

```markdown
📍 Final Checkpoint — Complete Proposal

**Document generated**: Commercial Proposal — [Project] — [Client]
**Reference**: PROP-[YYYY]-[NNN]
**Estimated pages**: ~XX pages

**Verifications**:
✅ Financial coherence OK
✅ Realistic planning (XX weeks for XX JH)
✅ All sections completed
✅ No remaining placeholders

**Summary**:
- Budget: XX XXX € HT (mid scenario)
- Duration: XX weeks
- Team: X profiles

**Options:**
→ `exporter` — Generate final document
→ `modifier-section [name]` — Edit a section
→ `previsualiser` — View complete document
→ `critiquor` — Launch quality review before export
```

---

## Error Handling

| Situation | Response |
|-----------|----------|
| No Estimator input | Block and request data |
| Incoherent data | Alert with details, offer correction path |
| Missing client info | Ask qualification questions |
| Template mismatch | Suggest appropriate template |
| User requests unsupported feature | Explain limitation, suggest alternative |

---

## Checkpoint Granularity

Checkpoint frequency adapts to context:

| Context | Checkpoints | Phases with CP |
|---------|-------------|----------------|
| Standard project, known client | Minimal (2) | Structure + Final |
| New client | Standard (3) | Qualification + Structure + Final |
| Public tender | Detailed (4+) | All phases + Summary validation |
| Large project (>100 JH) | Detailed (4+) | All phases + critical sections |
