# Brainstorm Commands Reference

> Reference complete des commandes disponibles pendant une session `/brainstorm`.

---

## Standard Commands

| Commande | Action |
|----------|--------|
| `continue` | Iteration suivante (3-5 questions) |
| `dive [topic]` | Approfondir un aspect |
| `pivot` | Reorienter si vrai besoin emerge |
| `status` | Afficher EMS detaille (5 axes) |
| `modes` | Afficher/changer persona |
| `mode [nom]` | Forcer persona (architecte/sparring/pragmatique) |
| `premortem` | Exercice anticipation risques |
| `diverge` | Forcer phase Divergent |
| `converge` | Forcer phase Convergent + @planner |
| `scoring` | Evaluer et prioriser idees |
| `framework [x]` | Appliquer framework (moscow/5whys/swot) |
| `technique [x]` | Afficher technique complete via @technique-advisor |
| `spike [duration] [q]` | Exploration technique (voir spike-process.md) |
| `security-check` | Invoquer @security-auditor |
| `plan-preview` | Invoquer @planner |
| `save` | Sauvegarder session |
| `back` | Iteration precedente |
| `energy` | Forcer energy check |
| `finish` | Generer brief + journal |

---

## Party Mode Commands (v5.0)

Mode multi-persona pour discussions collaboratives.

| Commande | Action |
|----------|--------|
| `party` | Demarrer discussion multi-persona |
| `party add [persona]` | Ajouter persona au round actuel |
| `party focus [persona]` | Deep dive d'un persona specifique |
| `party exit` | Quitter party mode, retour standard |

**Personas disponibles**: Architect, Security, Frontend, Backend, QA

---

## Expert Panel Commands (v5.0)

Panel d'experts pour discussions en 3 phases.

| Commande | Action |
|----------|--------|
| `panel` | Demarrer panel d'experts (phase discussion) |
| `panel debate` | Passer en phase debate (stress-test) |
| `panel socratic` | Passer en phase socratic (questions) |
| `panel exit` | Quitter panel mode, retour standard |

**Experts disponibles**: Martin, Fowler, Newman, Gamma, Beck
