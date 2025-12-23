# Criteria Grids by Theme

> Complete reference for all 23 thematic criteria grids used by CRITIQUOR v2

---

## Automatic Theme Detection

CRITIQUOR analyzes these signals to detect theme:
- Dominant lexical field
- Specific technical terms
- Language register (formal, technical, creative)
- Document structure
- Intention markers (action verbs, persuasive turns)

Classification results in one or more themes. If unclear or hybrid, use Universal Criteria as fallback.

---

## Grid Selection Logic

```
Document received
       │
       ▼
Analyze lexical field + structure + register
       │
       ▼
┌──────────────────────────────────────┐
│  Theme clearly identified?           │
├──────────────────────────────────────┤
│  YES → Use thematic grid             │
│  PARTIAL → Mix thematic + universal  │
│  NO → Use universal criteria         │
└──────────────────────────────────────┘
       │
       ▼
Add custom criteria if requested
       │
       ▼
Redistribute weights (total = 100%)
```

---

## EXISTING GRIDS (16)

---

### 1. Marketing

| Criterion | Description |
|-----------|-------------|
| Message clarity | Is the main message immediately understandable? |
| Brand coherence | Are tone and style aligned with brand image? |
| Persuasion impact | Does the text make people want to act or adhere? |
| Value proposition | Is the benefit for the reader clearly expressed? |
| Argument structure | Do arguments chain logically? |
| Audience relevance | Is the message adapted to the target? |
| Tone and personality | Does the text have a distinctive and engaging voice? |

---

### 2. Commercial / Sales

| Criterion | Description |
|-----------|-------------|
| Pitch strength | Does the hook capture attention? |
| Objection handling | Are potential barriers anticipated and addressed? |
| Call-to-Action (CTA) | Is the expected action clear and incentivizing? |
| Client benefits | Are concrete advantages for the client highlighted? |
| Persuasive structure | Does the text follow a convincing progression? |
| Credibility | Are proofs, references, guarantees present? |

---

### 3. Professional (emails, notes, internal communications)

| Criterion | Description |
|-----------|-------------|
| Clarity | Is the message understandable on first reading? |
| Relevance | Does content respond to the need/context? |
| Action orientation | Are next steps or expectations explicit? |
| Formal tone | Is the register appropriate to professional context? |
| Logical structuring | Is information organized coherently? |
| Conciseness | Does the text get to the point without superfluity? |

---

### 4. Management / Leadership

| Criterion | Description |
|-----------|-------------|
| Vision | Is the direction or objective clearly expressed? |
| Strategic coherence | Does the message fit into an overall logic? |
| Change management | Are impacts and transitions accompanied? |
| Instruction clarity | Are expectations unambiguous? |
| Mobilization | Does the message engage and motivate teams? |
| Exemplarity | Is the tone coherent with promoted values? |

---

### 5. Technical

| Criterion | Description |
|-----------|-------------|
| Accuracy | Is technical information correct? |
| Logical coherence | Does the technical reasoning hold? |
| Exhaustiveness | Are all necessary aspects covered? |
| Terminological rigor | Are technical terms used correctly? |
| Accessibility | Is the level adapted to the target technical audience? |
| Structure | Does the organization facilitate understanding? |

---

### 6. IT / Development

| Criterion | Description |
|-----------|-------------|
| Technical precision | Are concepts and terms exact? |
| Readability | Is the document easy to browse and understand? |
| Absence of ambiguities | Does each element have only one possible interpretation? |
| Modular structure | Is information divided logically? |
| Conceptual correctness | Are paradigms and patterns properly applied? |
| Reproducibility | Do instructions allow reproducing the result? |

---

### 7. AI / Machine Learning

| Criterion | Description |
|-----------|-------------|
| Scientific accuracy | Are ML/AI concepts correctly exposed? |
| ML concept coherence | Are terms (model, training, inference, etc.) used appropriately? |
| Explanation rigor | Are mechanisms explained without misleading shortcuts? |
| Methodological relevance | Is the described approach appropriate to the problem? |
| Bias/security consideration | Are risks and limits mentioned? |

---

### 8. Scientific

| Criterion | Description |
|-----------|-------------|
| Accuracy | Are facts and data correct? |
| Source coherence | Are references reliable and well used? |
| Methodology | Is the scientific approach rigorous? |
| Neutrality | Is the tone objective, without apparent bias? |
| Experimental logic | Does the reasoning follow a valid approach? |

---

### 9. Legal

| Criterion | Description |
|-----------|-------------|
| Compliance | Does the text respect the applicable legal framework? |
| Lexical precision | Are legal terms used correctly? |
| Interpretation risk | Does the text lend itself to divergent readings? |
| Legal structure | Does the document follow domain conventions? |
| Terminological neutrality | Is vocabulary free of bias? |

---

### 10. Finance

| Criterion | Description |
|-----------|-------------|
| Rigor | Are calculations and data exact? |
| Data coherence | Are figures coherent with each other? |
| Indicator clarity | Are KPIs and metrics well defined? |
| Risk analysis | Are financial risks identified? |
| Decision synthesis | Does the document help decision-making? |

---

### 11. HR (Human Resources)

| Criterion | Description |
|-----------|-------------|
| Neutrality | Is the text free of discrimination? |
| Human relevance | Does content consider the human factor? |
| Structure | Is information well organized? |
| Bias risks | Could formulations be poorly perceived? |
| Appropriate tone | Is the register adapted to HR context? |

---

### 12. Literary

| Criterion | Description |
|-----------|-------------|
| Style | Does writing have aesthetic quality? |
| Rhythm | Does sentence cadence serve the purpose? |
| Narrative coherence | Does the story or subject hold together? |
| Originality | Does the text bring something singular? |
| Fluidity | Is reading pleasant and smooth? |

---

### 13. Screenplay / Fiction

| Criterion | Description |
|-----------|-------------|
| Narrative construction | Is the story well architected? |
| Dramatic arc | Does tension evolve satisfactorily? |
| Character coherence | Are characters credible and consistent? |
| Narrative tension | Does the story maintain interest? |
| Dialogue quality | Do exchanges ring true? |

---

### 14. Psychology

| Criterion | Description |
|-----------|-------------|
| Neutrality | Is the subject objective and non-judgmental? |
| Conceptual coherence | Are psychology concepts well used? |
| Human relevance | Does the text show human understanding? |
| Sensitivity | Is the tone adapted to delicate subjects? |
| Notion precision | Are psychological terms exact? |

---

### 15. Strategy

| Criterion | Description |
|-----------|-------------|
| Vision | Is strategic orientation clear? |
| Coherence | Do elements articulate logically? |
| Impact | Can the strategy produce expected effects? |
| Tactical relevance | Are means adapted to objectives? |
| Decision clarity | Does the document guide toward clear decisions? |

---

### 16. Universal Criteria (Fallback)

Use when theme is unclear, hybrid, or not covered above:

| Criterion | Description |
|-----------|-------------|
| Clarity | Is the message understandable? |
| Coherence | Are elements logically linked? |
| Logical structure | Is organization relevant? |
| Relevance | Does content respond to the need? |
| Readability | Is the text easy to read? |
| Impact | Does the document produce the desired effect? |
| Completeness | Are all necessary elements present? |
| Fluidity | Is reading fluid? |
| Tonal coherence | Is tone constant and appropriate? |
| Argumentative coherence | Do arguments hold? |
| Terminological coherence | Is vocabulary used consistently? |
| Adapted expertise level | Does the level match the audience? |

---

## NEW GRIDS (7) — v2.0

---

### 17. Prompt Engineering (NEW)

**Triggers**: "prompt", "instruction", "système", "Claude", "GPT", "LLM", XML tags, role/task/format structure

| Criterion | Description | Suggested Weight |
|-----------|-------------|------------------|
| Intention clarity | Is the prompt's objective explicit? | 20% |
| Structure | Logical organization (context → task → format)? | 15% |
| Specificity | Sufficient detail without over-constraining? | 15% |
| Examples | Quality and presence of few-shots? | 12% |
| Edge case handling | Are edge cases anticipated? | 12% |
| Tone/persona | Is requested personality coherent? | 10% |
| Output constraints | Is expected format clearly defined? | 10% |
| Optimal length | Neither too verbose nor too succinct? | 6% |

---

### 18. UX Writing / Microcopy (NEW)

**Triggers**: "button", "error message", "onboarding", "tooltip", "notification", "CTA", "interface", texts <50 words

| Criterion | Description | Suggested Weight |
|-----------|-------------|------------------|
| Immediate clarity | Understandable in <3 seconds? | 25% |
| Actionability | Does user know what to do? | 20% |
| Brand tone | Consistent with product identity? | 15% |
| Concision | No word wasted? | 15% |
| Empathy | Acknowledges user context? | 10% |
| Accessibility | Inclusive, simple language? | 10% |
| Hierarchy | Main info first? | 5% |

---

### 19. SEO Content (NEW)

**Triggers**: "SEO", "référencement", "blog article", "web content", "keyword", "SERP", meta tags

| Criterion | Description | Suggested Weight |
|-----------|-------------|------------------|
| Keyword relevance | Natural integration of target terms? | 18% |
| Hn structure | Logical, optimized heading hierarchy? | 15% |
| Readability | Short sentences, airy paragraphs? | 15% |
| Unique value | Contribution vs existing content? | 15% |
| Internal linking | Link opportunities identified? | 10% |
| Meta description | Catchy and within limits? | 10% |
| Adapted length | Matches search intent? | 10% |
| E-E-A-T signals | Expertise, authority, trust demonstrated? | 7% |

---

### 20. API Documentation (NEW)

**Triggers**: "API", "endpoint", "REST", "webhook", "OpenAPI", "Swagger", `GET/POST/PUT/DELETE`, HTTP codes

| Criterion | Description | Suggested Weight |
|-----------|-------------|------------------|
| Technical accuracy | Endpoints, parameters, types correct? | 25% |
| Exhaustiveness | All cases covered (success, errors)? | 18% |
| Code examples | Present, functional, copy-pasteable? | 15% |
| RESTful structure | Conventions respected? | 12% |
| Error clarity | Codes and messages explicit? | 12% |
| Onboarding | Effective quick start? | 10% |
| Versioning | Version management documented? | 8% |

---

### 21. Pitch Deck (NEW)

**Triggers**: "pitch", "deck", "slides", "presentation", "investor", numbered slide structure

| Criterion | Description | Suggested Weight |
|-----------|-------------|------------------|
| Impact per slide | One key message per slide? | 20% |
| Storytelling | Coherent narrative arc? | 18% |
| Hook | Memorable opening? | 15% |
| Ask clarity | Explicit request (investment, partnership)? | 15% |
| Proof points | Data, traction, credibility? | 12% |
| Concision | No text overload? | 12% |
| Call-to-action | Actionable closing? | 8% |

---

### 22. Newsletter / Email Marketing (NEW)

**Triggers**: "newsletter", "email marketing", "campaign", "emailing", "Unsubscribe", promo structure

| Criterion | Description | Suggested Weight |
|-----------|-------------|------------------|
| Email subject | Potential open rate? | 20% |
| First paragraph hook | Hook in first 50 words? | 18% |
| Value delivered | Useful content vs pure promo? | 15% |
| Single CTA | One clear objective? | 15% |
| Personalization | Personalizable elements identified? | 12% |
| Scannability | Diagonal reading possible? | 12% |
| Unsubscribe | Present and visible? | 8% |

---

### 23. Meeting Notes / CR (NEW)

**Triggers**: "compte-rendu", "CR", "meeting", "réunion", "notes de", "PV", action lists

| Criterion | Description | Suggested Weight |
|-----------|-------------|------------------|
| Decision exhaustiveness | All decisions captured? | 22% |
| Assigned actions | Who does what, by when? | 20% |
| Clarity | Understandable without attending? | 18% |
| Structure | Logical organization (context, discussions, decisions, actions)? | 15% |
| Objectivity | Factual, no abusive interpretation? | 12% |
| Concision | No unnecessary verbatim? | 8% |
| Next steps | Follow-up clearly identified? | 5% |

---

## Custom Criteria

Users can add criteria on the fly:
- "Critique ce texte et ajoute le critère SEO"
- "Analyze with focus on accessibility"

### Common Custom Criteria

| Custom Criterion | Typical Use Case | Default Weight |
|------------------|------------------|----------------|
| SEO | Web content, blog posts | 10-15% |
| Accessibility | Public communications | 10-15% |
| GDPR compliance | Legal, data-related | 15-20% |
| Brand voice | Marketing content | 10-15% |
| Inclusivity | HR, public comms | 10-15% |

### Integration Process

1. Acknowledge the custom criterion
2. Define it briefly (or ask user if unclear)
3. Assign appropriate weight
4. Redistribute weights to maintain 100% total

---

## Grid Commands

| Command | Effect |
|---------|--------|
| `grilles` | List all 23 available grids |
| `--grille [name]` | Force specific grid |
| `--grille prompt` | Force Prompt Engineering |
| `--grille ux` | Force UX Writing |
| `--grille seo` | Force SEO Content |
| `--grille api` | Force API Documentation |
| `--grille pitch` | Force Pitch Deck |
| `--grille newsletter` | Force Newsletter |
| `--grille cr` | Force Meeting Notes |

---

## Detection Confidence

After detection, display confidence:

```
**Thème détecté** : IT/Développement 🎯 (confiance haute)
**Thème détecté** : Marketing + Commercial 📊 (hybride)
**Thème détecté** : Universel ⚠️ (thème non identifié)
```
