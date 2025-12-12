# Routing Logic — Detailed Reference

> Complete decision logic and examples for Clarifior

---

## Decision Algorithm

```
START

IF message is empty OR length < 10 characters
    → Polite error message
    → END

IF message is incomprehensible (coherence < threshold)
    → Block 1: partial attempt
    → Block 4: clarification request
    → END

CALCULATE complexity_score:
    score = 0
    IF length > 500 chars THEN score += 1
    IF multiple_action_verbs THEN score += 1
    IF process_steps_detected THEN score += 1
    IF ai_tool_reference THEN score += 2
    IF multiple_questions THEN score += 1

IF length < 200 chars AND complexity_score < 2
    → FAST MODE
    → Generate: Block 1 + Block 2
    → Block 3: NO
    → Block 4: only if ambiguity

IF length >= 200 chars OR complexity_score >= 2
    → FULL MODE
    → Generate: Block 1 + Block 2
    → Block 3: IF (complexity_score >= 2 OR ai_reference)
    → Block 4: IF ambiguity detected

END
```

---

## Complexity Detection

### Action Verbs (weight: +1 if multiple)

French indicators:
- créer, faire, générer, écrire, rédiger
- analyser, vérifier, contrôler, auditer
- envoyer, transmettre, partager
- modifier, changer, mettre à jour
- organiser, planifier, préparer

English indicators:
- create, make, generate, write
- analyze, check, verify, audit
- send, share, transmit
- modify, change, update
- organize, plan, prepare

### Process/Steps Indicators (weight: +1)

Keywords suggesting multi-step:
- "d'abord... ensuite... puis..."
- "étape 1, étape 2..."
- "en premier lieu... en second lieu..."
- "first... then... finally..."
- "step by step"

### AI/Tool References (weight: +2)

Explicit mentions:
- "demande à Claude", "prompt pour Claude"
- "génère avec l'IA", "fais un prompt"
- "ask Claude", "prompt for"
- "use AI to", "generate with"

---

## Block 3 (ASPECCT) Field Generation

### Mandatory Fields

| Field | Always Include |
|-------|----------------|
| **Action** | ✅ Yes |
| **Context** | ✅ Yes |

### Conditional Fields

| Field | Include When |
|-------|--------------|
| **Steps** | Multi-step process detected |
| **Persona** | Specific role mentioned or useful |
| **Examples** | Examples provided in input OR would help clarify |
| **Constraints** | Limits, format, tone, deadline mentioned |
| **Template** | Specific output format expected |

### Field Formatting

```
- **Action**: [Clear statement of main objective]
- **Steps**: 
  1. [First step]
  2. [Second step]
  3. [Third step]
- **Persona**: [Role for AI, if applicable]
- **Examples**: [Concrete examples, if applicable]
- **Context**: [Background information]
- **Constraints**: [Limits and requirements]
- **Template**: [Expected output format]
```

---

## Block 4 (Clarification) Triggers

### Generate Block 4 When:

1. **Missing critical information**
   - Unclear recipient ("lui", "elle" without reference)
   - Vague object ("le truc", "le document")
   - Ambiguous timing ("bientôt", "la prochaine fois")

2. **Multiple possible interpretations**
   - Action could mean different things
   - Context suggests different outcomes

3. **Very short message with insufficient context**
   - <50 characters
   - No clear action verb
   - No identifiable subject

### Do NOT Generate Block 4 When:

- Message is clear even if short
- All necessary information is present
- Intent is unambiguous
- Minor details are missing but not blocking

### Block 4 Format

```
**Clarifications Needed**

1. [First question - most important]
2. [Second question - if needed]
3. [Third question - if needed]

*Alternative reformulation if helpful:*
[Suggested improved version]
```

Maximum: 3 questions. Be concise and direct.

---

## Complete Examples

### Example 1 — Simple Message (Fast Mode)

**Input**:
```
clarifie : donc euh je dois pas oublier de rappeler Marc demain matin pour le devis
```

**Analysis**:
- Length: ~80 chars → <200 ✓
- Complexity score: 0 (single action, no AI reference)
- Mode: FAST

**Output**:

**Clarified Reformulation**

Rappeler Marc demain matin au sujet du devis.

---

**Actionable Version**

Tâche : Appeler Marc demain matin pour faire le point sur le devis en attente.

---

### Example 2 — Complex Message (Full Mode with Block 3)

**Input**:
```
reformule ça : alors en fait je voudrais créer un prompt pour Claude qui permette de générer des emails de relance client automatiquement en fonction du contexte donc il faudrait qu'il prenne en compte le nom du client le montant de la facture et depuis combien de temps elle est en retard et qu'il adapte le ton en fonction
```

**Analysis**:
- Length: ~350 chars → >200 ✓
- Complexity score: 
  - Multiple actions (+1)
  - Process steps implied (+1)
  - AI reference "prompt pour Claude" (+2)
  - Total: 4
- Mode: FULL with Block 3

**Output**:

**Clarified Reformulation**

Je souhaite créer un prompt pour Claude qui génère automatiquement des emails de relance client. Le prompt doit prendre en compte le nom du client, le montant de la facture et le délai de retard, puis adapter le ton en conséquence.

---

**Actionable Version**

Créer un prompt de génération d'emails de relance client pour Claude avec les paramètres suivants :
- Variables d'entrée : nom client, montant facture, jours de retard
- Logique d'adaptation du ton selon l'ancienneté du retard
- Output : email prêt à envoyer

---

**Structured Prompt**

- **Action**: Générer un email de relance client personnalisé
- **Steps**:
  1. Identifier le niveau de relance selon les jours de retard
  2. Sélectionner le ton approprié (cordial → ferme → mise en demeure)
  3. Personnaliser avec les variables client
  4. Générer l'email complet
- **Context**: Recouvrement de factures impayées, besoin d'automatisation
- **Constraints**: Ton adaptatif, variables dynamiques, format professionnel
- **Template**: Email avec objet, corps structuré et formule de politesse

---

### Example 3 — Ambiguous Message (with Block 4)

**Input**:
```
nettoie : faut que je lui envoie le truc pour vendredi
```

**Analysis**:
- Length: ~50 chars → <200 ✓
- Complexity score: 0
- Ambiguities detected:
  - "lui" → Who?
  - "le truc" → What?
  - "vendredi" → Which Friday?
- Mode: FAST with Block 4

**Output**:

**Clarified Reformulation**

Je dois lui envoyer le document pour vendredi.

---

**Actionable Version**

Envoyer [document à préciser] à [destinataire à préciser] avant vendredi.

---

**Clarifications Needed**

1. Quel document ou élément doit être envoyé ?
2. Qui est le destinataire ?
3. Vendredi de cette semaine ou une date spécifique ?

---

### Example 4 — Already Clear Message

**Input**:
```
reformule : Envoyer le rapport mensuel des ventes à Sophie Martin avant jeudi 15 décembre
```

**Analysis**:
- Length: ~90 chars → <200 ✓
- Complexity score: 0
- No ambiguity
- Mode: FAST

**Output**:

**Clarified Reformulation**

Envoyer le rapport mensuel des ventes à Sophie Martin avant le jeudi 15 décembre.

---

**Actionable Version**

Tâche : Transmettre le rapport mensuel des ventes à Sophie Martin.
Deadline : Jeudi 15 décembre.

*Note : Message déjà clair et complet.*

---

### Example 5 — Multiple Intents

**Input**:
```
clarifie : donc euh faut que je fasse la présentation pour lundi et aussi que je rappelle le client Dupont pour le contrat et puis faut pas oublier de commander les fournitures
```

**Analysis**:
- Length: ~180 chars → <200 ✓
- Multiple distinct actions detected
- Complexity score: 1 (multiple actions)
- Mode: FAST but structured output

**Output**:

**Clarified Reformulation**

Je dois préparer la présentation pour lundi, rappeler le client Dupont concernant le contrat, et commander les fournitures.

---

**Actionable Version**

Trois tâches identifiées :

1. **Présentation** — Préparer pour lundi
2. **Client Dupont** — Rappeler au sujet du contrat
3. **Fournitures** — Passer commande

---

### Example 6 — Incomprehensible Message

**Input**:
```
clarifie : le machin là avec le truc et le bidule
```

**Analysis**:
- No identifiable action
- No clear subject
- Incomprehensible
- Mode: Error + Block 4

**Output**:

**Clarified Reformulation**

*(Message trop vague pour être reformulé avec précision)*

---

**Clarifications Needed**

1. De quoi parlez-vous exactement ?
2. Quelle action souhaitez-vous effectuer ?
3. Y a-t-il un contexte particulier (projet, personne, deadline) ?

Merci de reformuler avec plus de détails.

---

## Language Detection

### Behavior

The skill responds in the same language as the input:
- French input → French output
- English input → English output
- Mixed → Prefer French, mention if unclear

### French Verbal Tics to Remove

```
euh, heu, bah, ben, donc, en fait, du coup, genre,
voilà, tu vois, quoi, hein, bon, enfin, disons
```

### English Verbal Tics to Remove

```
um, uh, like, you know, so, basically, I mean,
well, kind of, sort of, actually, literally
```
