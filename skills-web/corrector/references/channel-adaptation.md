# Channel Adaptation Reference

> Rules for adapting message length, structure, tone, and formatting per communication channel

---

## Channel Detection

### Priority: Explicit > Implicit > Ask

**Explicit signals** (always override inference):

| Signal | Channel |
|--------|---------|
| "WhatsApp", "SMS", "texto", "message" (casual) | `chat` |
| "Slack", "Teams", "channel", "DM pro" | `pro` |
| "mail", "email", "courrier", "courriel" | `email` |
| "LinkedIn", "post", "publication", "réseau" | `social` |

**Implicit signals** (infer when no explicit cue):

| Signal | Likely channel |
|--------|---------------|
| Informal "tu" + very short input | `chat` |
| Mentions colleague name + work context | `pro` |
| Polite formulas in input ("Cordialement") | `email` |
| Mentions "profil", "connexion", "réseau" | `social` |
| Mentions "Didier", "Alain" + location context | `chat` (personal) |
| Mentions client + formal context | `email` |

**No signal detected**: Ask one question using `ask_user_input_v0` with options: WhatsApp/SMS, Slack/Teams, Email, LinkedIn.

---

## Channel Specifications

### Chat (WhatsApp / SMS / iMessage)

| Property | Rule |
|----------|------|
| **Length** | 2-6 lines maximum. Absolute max ~500 characters |
| **Structure** | None. Pure flowing prose, no headers or bullet points |
| **Greeting** | Short or none: "Bonjour Didier," or just start directly |
| **Sign-off** | Minimal or none. No "Cordialement". At most: "Bonne journée" |
| **Tone** | Natural, warm, conversational. Can use light contractions |
| **Paragraphs** | 1-2 max, separated by single line break |
| **Formatting** | No bold, no lists, no markdown. Plain text only |
| **`message_compose` kind** | `textMessage` |

**Example**:
```
Bonjour Didier,

Je me permets de revenir vers vous car j'ai reçu plusieurs demandes 
de réservation pour la maison et le bungalow sur votre période. 
Êtes-vous toujours intéressé ? J'aurais besoin de votre retour 
rapidement pour répondre aux autres demandes.
```

---

### Professional Messaging (Slack / Teams)

| Property | Rule |
|----------|------|
| **Length** | 3-10 lines. Can go up to ~800 characters |
| **Structure** | Light: dashes for lists if 3+ items, otherwise prose |
| **Greeting** | Casual-pro: "Salut Pierre," or "Hey team," |
| **Sign-off** | Light or none: "Merci !", "Let me know" |
| **Tone** | Professional-casual. Direct, efficient, collaborative |
| **Paragraphs** | 2-3 max |
| **Formatting** | Slack-compatible: `*bold*`, `-` for lists, `>` for quotes |
| **`message_compose` kind** | `other` |

**Example**:
```
Salut Pierre,

Quick update sur le module paiement : la PR est prête pour review.
J'ai documenté les choix techniques dans le README, notamment 
la gestion des webhooks Stripe.

Si tu as des questions, on peut en parler au standup demain.
```

---

### Email

| Property | Rule |
|----------|------|
| **Length** | Free. Adapt to content complexity |
| **Structure** | Full: greeting → hook/context → body → closing → sign-off |
| **Greeting** | Adapted to relationship: "Bonjour Pierre," / "Madame la Directrice," |
| **Sign-off** | Full formula matching tone: "Cordialement," / "Bien à vous," / "Je vous prie..." |
| **Tone** | Range from standard-relaxed to very formal depending on context |
| **Paragraphs** | As many as needed, logically organized |
| **Formatting** | Standard email: bold sparingly, lists if 3+ items |
| **Subject line** | REQUIRED. Clear, specific, actionable |
| **`message_compose` kind** | `email` (includes `subject` field) |

**Structure template**:
```
[Greeting],

[Hook: Why am I writing? 1-2 sentences. Reference to previous exchange if relevant]

[Body: Main content, organized logically. Technical details adapted to audience. 
Clear action items if any]

[Closing: Next steps or call to action. Availability for questions]

[Sign-off formula],

[No signature placeholder — handled by mail client]
```

**Subject line rules**:
- Specific and informative: "Disponibilité location juillet — besoin de confirmation"
- Never generic: ~~"Question"~~, ~~"Suivi"~~, ~~"Information"~~
- Include key context: project name, date, action needed
- Each variant can have a different subject if strategy differs

---

### Social (LinkedIn / Professional Networks)

| Property | Rule |
|----------|------|
| **Length** | DM: 3-10 lines. Post: 5-15 lines |
| **Structure** | Strong hook first line. Short paragraphs (2-3 sentences each) |
| **Greeting** | DM: "Bonjour [Prénom]," / Post: None (start with hook) |
| **Sign-off** | DM: Light. Post: CTA or question to drive engagement |
| **Tone** | Professional, authentic. Avoid corporate jargon |
| **Paragraphs** | Short, scannable. One idea per paragraph |
| **Formatting** | LinkedIn-compatible: line breaks for readability |
| **`message_compose` kind** | `other` |

**DM example**:
```
Bonjour Marie,

J'ai vu votre publication sur la transformation digitale des 
collectivités — le sujet me parle particulièrement car j'accompagne 
plusieurs communes dans leur modernisation applicative.

Seriez-vous ouverte à un échange de 15 minutes sur le sujet ?
```

---

## Cross-Channel Rules

### Rules that apply to ALL channels

1. **No invention**: Never add facts, dates, or commitments not in the input
2. **Language match**: Output in the same language as user input
3. **Audience awareness**: Technical jargon only for technical recipients
4. **Ready to send**: Every variant must be usable without modification
5. **No [Signature] placeholder**: Let the client/app handle signatures

### Tone Adaptation by Relationship

| Relationship type | Default tone | Channel preference |
|-------------------|-------------|-------------------|
| Close colleague | Casual-professional | Slack/Chat |
| Regular client/partner | Standard-relaxed | Email/Chat |
| New contact | Standard-professional | Email |
| Senior executive | Formal | Email |
| Institutional/Legal | Very formal | Email |
| Personal (vacation rental clients) | Warm-professional | Chat |

---

## Channel Escalation Patterns

Some messages may need to escalate across channels. The skill should suggest this when appropriate:

| Starting channel | Escalation signal | Suggested action |
|-----------------|-------------------|-----------------|
| Chat → Email | Complex topic, need for paper trail | "This might work better as an email for traceability" |
| Slack → Email | Formal request, external stakeholder | "Consider sending this as a formal email" |
| Email → Chat | Urgent, needs quick response | "A quick WhatsApp might get faster response" |
