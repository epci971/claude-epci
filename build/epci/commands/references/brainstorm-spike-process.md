# Brainstorm Spike Process Reference

> Reference pour la commande `spike` dans `/brainstorm`.
> Exploration technique time-boxed pour valider la faisabilite.

---

## Quand utiliser `spike`

Pendant le brainstorm, si une **incertitude technique** emerge:
- "Est-ce que l'API X peut gerer nos volumes ?"
- "GraphQL est-il adapte a notre cas ?"
- "Comment integrer Redis avec notre stack ?"

## Commande

```
spike [duration] [question technique]
```

**Exemples:**
```
spike 30min Est-ce que Stripe supporte les webhooks async ?
spike 1h GraphQL vs REST pour notre API mobile
spike 2h Integration Redis avec notre stack Django
```

## Process

### 1. Framing (5 min)

Afficher le setup avant exploration:

```
-------------------------------------------------------
SPIKE MODE | [duration]
-------------------------------------------------------
**Question:** [Question technique precise]

**Criteres de succes:**
- [ ] Critere 1 (mesurable)
- [ ] Critere 2 (mesurable)

**Scope:**
- Inclus: [Ce qu'on explore]
- Exclus: [Ce qu'on n'explore pas]
-------------------------------------------------------
```

### 2. Exploration

- Invoquer `@Explore` (thorough level)
- Lire documentation, tester hypotheses
- Creer prototypes **jetables** (pas de code production)
- Respecter strictement le time-box

**Regles:**
- Le code produit est jetable
- Documenter les decouvertes au fur et a mesure
- Rester focus sur la question initiale

### 3. Verdict

A la fin du time-box, determiner:

| Verdict | Signification | Action |
|---------|---------------|--------|
| **GO** | Faisable, approche identifiee | Continuer brainstorm avec cette info |
| **NO-GO** | Non faisable ou trop couteux | Pivoter vers alternative |
| **MORE_RESEARCH** | Besoin d'un autre spike | Planifier spike supplementaire |

### 4. Retour au Brainstorm

Afficher resume et reprendre:

```
-------------------------------------------------------
SPIKE COMPLETE | [duration]
-------------------------------------------------------
Verdict: [GO | NO-GO | MORE_RESEARCH]

Decouvertes cles:
1. [Decouverte 1]
2. [Decouverte 2]

Impact sur le brief:
- [Ajustement 1]
- [Ajustement 2]

-> Retour au brainstorm (EMS recalcule)
-------------------------------------------------------
```

## Integration

Le verdict et les decouvertes sont integres:
- Dans le **brief final** (section "Technical Validation")
- Dans le **journal** (historique du spike)
