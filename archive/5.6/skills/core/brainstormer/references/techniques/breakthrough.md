# Techniques de Deblocage (Breakthrough)

> 3 techniques pour sortir des impasses et stimuler la creativite.
> Phase recommandee: Divergent / Deblocage

---

## Inner Child Conference

**Description:** Approche de deblocage creatif en adoptant une perspective naive et sans filtre. Poser les questions qu'un enfant poserait, sans crainte de paraitre ignorant. Reveler les complexites inutiles et les assumptions non questionees.

**Quand utiliser:**
- Over-engineering detecte
- Solution devenue trop complexe
- Besoin de simplification radicale

**Phase recommandee:** Divergent

**Questions types:**
1. Pourquoi c'est si complique ? (ton enfantin)
2. C'est quoi le truc le plus simple qui marcherait ?
3. Pourquoi on peut pas juste faire [solution naive] ?

**Exemple:**
> Architecture microservices complexe avec 12 services. Inner Child: "Pourquoi y'a autant de boites ? Ca fait quoi chaque boite ? Pourquoi elles se parlent autant ?" → Revele que 4 services n'ont qu'un seul appelant et pourraient etre merges. 3 services font la meme chose avec des noms differents. Solution: consolider en 5 services.

---

## Chaos Engineering

**Description:** Stress-test des idees et solutions par injection de chaos. Imaginer des scenarios de defaillance, des conditions extremes, des comportements inattendus pour reveler les faiblesses avant qu'elles ne se manifestent en production.

**Quand utiliser:**
- Validation de la robustesse d'une architecture
- Preparation au lancement d'une feature critique
- Identification des points de defaillance

**Phase recommandee:** Divergent

**Questions types:**
1. Que se passe-t-il si ce service tombe ?
2. Comment le systeme reagit-il a un pic de 10x le trafic normal ?
3. Que se passe-t-il si la base de donnees repond en 30s au lieu de 30ms ?

**Exemple:**
> Feature de checkout: Chaos scenarios: 1) Payment provider timeout apres debit mais avant confirmation → Solution: idempotency + reconciliation. 2) Pic Black Friday 50x normal → Solution: queue async + rate limiting gracieux. 3) DB master failover mid-transaction → Solution: retry logic + saga pattern.

---

## Nature's Solutions

**Description:** Bio-inspiration et patterns naturels pour resoudre des problemes techniques. La nature a eu des milliards d'annees pour optimiser ses solutions. Observer comment les systemes biologiques gerent la complexite, la resilience, la communication.

**Quand utiliser:**
- Problemes de scalabilite et distribution
- Recherche de patterns de resilience
- Optimisation de systemes complexes

**Phase recommandee:** Divergent

**Questions types:**
1. Comment la nature resout-elle ce type de probleme ?
2. Quel organisme gere efficacement cette contrainte ?
3. Quel pattern biologique pourrait s'appliquer ici ?

**Exemple:**
> Probleme de consensus distribue: Pattern "Essaim d'abeilles" - Les abeilles exploratrices votent pour un nouveau site en dansant, l'intensite du vote influence les autres, convergence progressive vers un consensus. Application: algorithme de leader election ou chaque noeud "vote" avec une intensite proportionnelle a sa confiance, propagation du vote aux voisins, convergence naturelle vers un leader sans point central de coordination.

---

## Quand Utiliser les Techniques Breakthrough

| Signal | Technique Recommandee |
|--------|----------------------|
| "C'est trop complique" | Inner Child Conference |
| "Ca marchera jamais en prod" | Chaos Engineering |
| "On a tout essaye" | Nature's Solutions |
| Equipe frustree/bloquee | Inner Child Conference |
| Pre-production critique | Chaos Engineering |
| Innovation de rupture necessaire | Nature's Solutions |

## Anti-patterns

- **Ne pas forcer** une technique breakthrough si l'exploration est fluide
- **Limiter a 1 technique** par session de deblocage
- **Documenter les insights** meme s'ils semblent triviaux sur le moment
