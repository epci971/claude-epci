# Techniques de Perspective

> 3 techniques pour changer de point de vue et reveler des angles morts.
> Phase recommandee: Convergent (Role Playing), Divergent (Time Travel), Deblocage (Reversal)

---

## Role Playing

**Description:** Adopter le point de vue de differents stakeholders pour comprendre leurs besoins, contraintes et motivations. Se mettre dans la peau de l'utilisateur, de l'ops, du CEO, du hacker...

**Quand utiliser:**
- Design d'experience utilisateur
- Anticipation des objections des stakeholders
- Comprehension des besoins non exprimes

**Phase recommandee:** Convergent

**Questions types:**
1. Comment un utilisateur novice percevrait-il cette interface ?
2. Qu'est-ce qui inquieterait l'equipe ops dans cette architecture ?
3. Quel serait le premier reflexe d'un attaquant face a cette feature ?

**Exemple:**
> Feature de paiement - Role "Hacker": "Je chercherais a modifier le montant cote client, a rejouer une transaction, a enumerer les cartes valides via les messages d'erreur." → Revele 3 vulnerabilites a adresser: signature serveur des montants, idempotency keys, messages d'erreur generiques.

---

## Time Travel

**Description:** Se projeter dans le futur ou le passe pour evaluer une decision avec une perspective temporelle differente. Imaginer le code dans 2 ans, ou comment on aurait fait avec les technos d'il y a 5 ans.

**Quand utiliser:**
- Decisions d'architecture long terme
- Evaluation de la dette technique
- Anticipation de l'evolution du produit

**Phase recommandee:** Divergent

**Questions types:**
1. Comment ce code sera-t-il percu dans 2 ans ?
2. Quelles technologies auront change d'ici la ?
3. Si on avait fait ce choix il y a 3 ans, quel serait l'etat aujourd'hui ?

**Exemple:**
> Choix de framework frontend: Time Travel +3 ans: "React sera-t-il toujours dominant ? Les Web Components auront-ils perce ? Notre equipe aura-t-elle triple ?" → Decision: abstraire la couche UI pour faciliter une migration future, investir dans les standards web plutot que les specifites framework.

---

## Reversal Inversion

**Description:** Inverser le probleme pour reveler les assumptions cachees et decouvrir de nouvelles solutions. Au lieu de "Comment ameliorer X ?", demander "Comment pourrait-on empirer X ?" puis inverser les reponses.

**Quand utiliser:**
- Blocage creatif, pas d'idees nouvelles
- Besoin de challenger les evidences
- Recherche de solutions contre-intuitives

**Phase recommandee:** Deblocage

**Questions types:**
1. Comment pourrait-on rendre cette feature pire ?
2. Que faudrait-il faire pour que ce projet echoue a coup sur ?
3. Si on voulait faire fuir les utilisateurs, que ferait-on ?

**Exemple:**
> Probleme: "Ameliorer le taux de conversion". Inversion: "Comment faire fuir les clients ?" → Ajouter des etapes, cacher le prix, forcer la creation de compte, ralentir le site, ne pas rassurer sur la securite. Reversal: Reduire les etapes a 2, afficher le prix tot, permettre guest checkout, optimiser la perf, ajouter badges de confiance.
