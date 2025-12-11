# Criteria Grids by Theme

> Complete reference for all thematic criteria grids used by CRITIQUOR

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

## 1. Marketing

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

## 2. Commercial / Sales

| Criterion | Description |
|-----------|-------------|
| Pitch strength | Does the hook capture attention? |
| Objection handling | Are potential barriers anticipated and addressed? |
| Call-to-Action (CTA) | Is the expected action clear and incentivizing? |
| Client benefits | Are concrete advantages for the client highlighted? |
| Persuasive structure | Does the text follow a convincing progression? |
| Credibility | Are proofs, references, guarantees present? |

---

## 3. Professional (emails, notes, internal communications)

| Criterion | Description |
|-----------|-------------|
| Clarity | Is the message understandable on first reading? |
| Relevance | Does content respond to the need/context? |
| Action orientation | Are next steps or expectations explicit? |
| Formal tone | Is the register appropriate to professional context? |
| Logical structuring | Is information organized coherently? |
| Conciseness | Does the text get to the point without superfluity? |

---

## 4. Management / Leadership

| Criterion | Description |
|-----------|-------------|
| Vision | Is the direction or objective clearly expressed? |
| Strategic coherence | Does the message fit into an overall logic? |
| Change management | Are impacts and transitions accompanied? |
| Instruction clarity | Are expectations unambiguous? |
| Mobilization | Does the message engage and motivate teams? |
| Exemplarity | Is the tone coherent with promoted values? |

---

## 5. Technical

| Criterion | Description |
|-----------|-------------|
| Accuracy | Is technical information correct? |
| Logical coherence | Does the technical reasoning hold? |
| Exhaustiveness | Are all necessary aspects covered? |
| Terminological rigor | Are technical terms used correctly? |
| Accessibility | Is the level adapted to the target technical audience? |
| Structure | Does the organization facilitate understanding? |

---

## 6. IT / Development

| Criterion | Description |
|-----------|-------------|
| Technical precision | Are concepts and terms exact? |
| Readability | Is the document easy to browse and understand? |
| Absence of ambiguities | Does each element have only one possible interpretation? |
| Modular structure | Is information divided logically? |
| Conceptual correctness | Are paradigms and patterns properly applied? |
| Reproducibility | Do instructions allow reproducing the result? |

---

## 7. AI / Machine Learning

| Criterion | Description |
|-----------|-------------|
| Scientific accuracy | Are ML/AI concepts correctly exposed? |
| ML concept coherence | Are terms (model, training, inference, etc.) used appropriately? |
| Explanation rigor | Are mechanisms explained without misleading shortcuts? |
| Methodological relevance | Is the described approach appropriate to the problem? |
| Bias/security consideration | Are risks and limits mentioned? |

---

## 8. Scientific

| Criterion | Description |
|-----------|-------------|
| Accuracy | Are facts and data correct? |
| Source coherence | Are references reliable and well used? |
| Methodology | Is the scientific approach rigorous? |
| Neutrality | Is the tone objective, without apparent bias? |
| Experimental logic | Does the reasoning follow a valid approach? |

---

## 9. Legal

| Criterion | Description |
|-----------|-------------|
| Compliance | Does the text respect the applicable legal framework? |
| Lexical precision | Are legal terms used correctly? |
| Interpretation risk | Does the text lend itself to divergent readings? |
| Legal structure | Does the document follow domain conventions? |
| Terminological neutrality | Is vocabulary free of bias? |

---

## 10. Finance

| Criterion | Description |
|-----------|-------------|
| Rigor | Are calculations and data exact? |
| Data coherence | Are figures coherent with each other? |
| Indicator clarity | Are KPIs and metrics well defined? |
| Risk analysis | Are financial risks identified? |
| Decision synthesis | Does the document help decision-making? |

---

## 11. HR (Human Resources)

| Criterion | Description |
|-----------|-------------|
| Neutrality | Is the text free of discrimination? |
| Human relevance | Does content consider the human factor? |
| Structure | Is information well organized? |
| Bias risks | Could formulations be poorly perceived? |
| Appropriate tone | Is the register adapted to HR context? |

---

## 12. Literary

| Criterion | Description |
|-----------|-------------|
| Style | Does writing have aesthetic quality? |
| Rhythm | Does sentence cadence serve the purpose? |
| Narrative coherence | Does the story or subject hold together? |
| Originality | Does the text bring something singular? |
| Fluidity | Is reading pleasant and smooth? |

---

## 13. Screenplay / Fiction

| Criterion | Description |
|-----------|-------------|
| Narrative construction | Is the story well architected? |
| Dramatic arc | Does tension evolve satisfactorily? |
| Character coherence | Are characters credible and consistent? |
| Narrative tension | Does the story maintain interest? |
| Dialogue quality | Do exchanges ring true? |

---

## 14. Psychology

| Criterion | Description |
|-----------|-------------|
| Neutrality | Is the subject objective and non-judgmental? |
| Conceptual coherence | Are psychology concepts well used? |
| Human relevance | Does the text show human understanding? |
| Sensitivity | Is the tone adapted to delicate subjects? |
| Notion precision | Are psychological terms exact? |

---

## 15. Strategy

| Criterion | Description |
|-----------|-------------|
| Vision | Is strategic orientation clear? |
| Coherence | Do elements articulate logically? |
| Impact | Can the strategy produce expected effects? |
| Tactical relevance | Are means adapted to objectives? |
| Decision clarity | Does the document guide toward clear decisions? |

---

## 16. Universal Criteria (Fallback)

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

## Custom Criteria Examples

Users can add these on the fly:

| Custom Criterion | Typical Use Case | Default Weight |
|------------------|------------------|----------------|
| SEO | Web content, blog posts | 10-15% |
| Accessibility | Public communications | 10-15% |
| GDPR compliance | Legal, data-related | 15-20% |
| Brand voice | Marketing content | 10-15% |
| Inclusivity | HR, public comms | 10-15% |

**Integration process**:
1. Acknowledge the custom criterion
2. Define it briefly (or ask user if unclear)
3. Assign appropriate weight
4. Redistribute weights to maintain 100% total

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
