# Tone Examples Reference

> Complete email examples for each tone level

---

## Tone Spectrum Overview

```
RELAXED ←――――――――――――――――――――――――――――――――→ VERY FORMAL
   │              │              │              │
Informal    Standard-Relaxed  Standard      Formal      Very Formal
            (DEFAULT)
```

---

## 1. Relaxed (Détendu)

### Characteristics
- Informal greetings ("Salut", "Hey")
- Contractions and casual phrasing
- Emoji acceptable (sparingly)
- First-name basis assumed
- Short sentences, conversational flow

### Use cases
- Close colleagues
- Internal team chat
- Friendly follow-ups
- Non-critical updates

### Example (French)
```
Salut Pierre,

Petit update rapide : j'ai fini la PR sur le module paiement, elle est prête 
pour review quand tu as 5 min.

Rien d'urgent, mais si tu peux y jeter un œil avant demain ce serait top.

À plus !

[Signature]
```

### Example (English)
```
Hey Sarah,

Quick heads up - finished the payment module PR, ready for review when 
you get a chance.

No rush, but if you can take a look before tomorrow that'd be great.

Cheers!

[Signature]
```

---

## 2. Standard-Relaxed (Standard-décontracté) — DEFAULT

### Characteristics
- Professional but natural greeting ("Bonjour Pierre")
- Fluid, conversational professional tone
- Direct without being abrupt
- Warmth without over-familiarity
- Clear structure with natural transitions

### Use cases
- Regular clients
- Trusted partners
- Cross-team collaboration
- Project updates and follow-ups

### Example (French)
```
Bonjour Pierre,

Petit retour suite à notre échange d'hier : j'ai avancé sur l'intégration 
du module de paiement et la PR est prête pour review.

J'ai documenté les choix techniques dans le README, notamment sur la gestion 
des webhooks Stripe. Si certains points méritent discussion, on peut en 
parler lors de notre point de demain.

N'hésite pas si tu as des questions d'ici là.

Bonne fin de journée,

[Signature]
```

### Example (English)
```
Hi Sarah,

Following up on our chat yesterday - I've made progress on the payment 
module integration and the PR is ready for review.

I've documented the technical decisions in the README, particularly around 
Stripe webhook handling. If anything needs discussion, we can cover it in 
tomorrow's sync.

Let me know if you have any questions in the meantime.

Best,

[Signature]
```

---

## 3. Standard (Standard)

### Characteristics
- Neutral professional greeting ("Bonjour Monsieur Dupont")
- Balanced, professional tone
- Clear and direct communication
- Minimal personality injection
- Structured and organized

### Use cases
- New contacts
- Formal requests
- Cross-company communication
- Documentation of decisions

### Example (French)
```
Bonjour Monsieur Dupont,

Suite à notre réunion du 15 novembre, je vous transmets le compte-rendu 
des décisions prises concernant le projet de refonte du site web.

Les points suivants ont été validés :
- Migration vers Symfony 7.4 prévue pour le T1 2025
- Budget alloué : 45 000 € HT
- Livraison de la phase 1 : 28 février 2025

Je reste à votre disposition pour tout complément d'information.

Cordialement,

[Signature]
```

### Example (English)
```
Dear Mr. Thompson,

Following our meeting on November 15th, please find below a summary of 
the decisions made regarding the website redesign project.

The following points have been validated:
- Migration to Symfony 7.4 planned for Q1 2025
- Allocated budget: €45,000 (excluding VAT)
- Phase 1 delivery: February 28, 2025

Please don't hesitate to reach out if you require any additional information.

Best regards,

[Signature]
```

---

## 4. Formal (Formel)

### Characteristics
- Formal greeting with title ("Madame la Directrice")
- Polished, conventional language
- Respectful distance maintained
- Longer, more elaborate sentences
- Traditional business formulas

### Use cases
- Senior executives
- Official matters
- First contact with important stakeholders
- Sensitive topics

### Example (French)
```
Madame la Directrice,

J'ai l'honneur de vous soumettre le rapport d'avancement du projet de 
digitalisation que vous avez bien voulu nous confier.

Conformément au cahier des charges établi, l'ensemble des développements 
de la première phase ont été réalisés dans les délais impartis. Les tests 
de recette sont actuellement en cours et devraient s'achever d'ici la fin 
de la semaine prochaine.

Je me tiens à votre entière disposition pour vous présenter ces travaux 
lors d'une réunion à votre convenance.

Je vous prie d'agréer, Madame la Directrice, l'expression de mes 
salutations distinguées.

[Signature]
```

### Example (English)
```
Dear Director Thompson,

I am pleased to submit the progress report for the digitalization project 
that you entrusted to our team.

In accordance with the established specifications, all developments for 
the first phase have been completed within the allocated timeframe. 
Acceptance testing is currently underway and is expected to conclude by 
the end of next week.

I remain at your disposal to present these deliverables at a meeting 
at your convenience.

Yours sincerely,

[Signature]
```

---

## 5. Very Formal (Très formel)

### Characteristics
- Ceremonial greeting with full titles
- Protocol-heavy language
- Elaborate, traditional formulas
- Maximum respectful distance
- Careful, measured phrasing

### Use cases
- Legal correspondence
- Institutional communication
- Government/public administration
- High-stakes situations

### Example (French)
```
Monsieur le Président-Directeur Général,

Par la présente, j'ai l'honneur de porter à votre connaissance les 
conclusions du comité de pilotage relatives au projet de transformation 
numérique de l'établissement.

À l'issue des travaux menés par l'ensemble des parties prenantes, il 
apparaît que les objectifs fixés dans la lettre de mission du 
12 septembre 2024 ont été atteints dans leur intégralité.

Je me permets de solliciter un entretien à votre meilleure convenance 
afin de vous exposer en détail les recommandations formulées par le comité.

Dans l'attente de votre réponse, je vous prie d'agréer, Monsieur le 
Président-Directeur Général, l'expression de ma très haute considération.

[Signature]
```

### Example (English)
```
Dear Chairman of the Board,

I have the honour of bringing to your attention the conclusions of the 
steering committee regarding the institution's digital transformation project.

Following the work conducted by all stakeholders, it has been determined 
that the objectives outlined in the terms of reference dated 
September 12, 2024, have been fully achieved.

I respectfully request an audience at your earliest convenience to present 
the committee's recommendations in detail.

I remain at your disposal and beg to remain, Sir, your most obedient servant.

[Signature]
```

---

## Tone Selection Guidelines

### When user specifies tone
Use exactly what's requested for Block 1 (main email).

### When no tone specified
Default to **Standard-Relaxed**.

### Variant generation rules

| Main Tone | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| Relaxed | Standard-Relaxed | Standard |
| Standard-Relaxed | Standard | Formal |
| Standard | Standard-Relaxed | Formal |
| Formal | Standard | Very Formal |
| Very Formal | Formal | Standard |

---

## Adaptation Signals

### Signals suggesting more formal tone
- First contact with unknown recipient
- Mention of executives, directors, VIPs
- Legal, financial, or sensitive topics
- Official documents, contracts
- Complaints or escalations

### Signals suggesting more relaxed tone
- Mention of "team", "colleagues"
- Casual context clues ("quick update", "heads up")
- Previous familiarity indicated
- Internal communication
- Positive/celebratory content
