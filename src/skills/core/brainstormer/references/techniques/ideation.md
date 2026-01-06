# Techniques d'Ideation

> 6 techniques pour generer des idees et explorer des possibilites.
> Phase recommandee: Divergent

---

## SCAMPER

**Description:** 7 lentilles creatives pour transformer une idee existante: Substitute, Combine, Adapt, Modify/Magnify, Put to other uses, Eliminate, Reverse/Rearrange. Methode systematique pour l'innovation incrementale.

**Quand utiliser:**
- Ameliorer une feature existante
- Trouver des variations sur un concept
- Debloquer la creativite de l'equipe

**Phase recommandee:** Divergent

**Questions types:**
1. **Substitute**: Quel composant pourrait-on remplacer ?
2. **Combine**: Quelles features pourrait-on fusionner ?
3. **Adapt**: Quelle solution d'un autre domaine pourrait s'appliquer ?
4. **Modify**: Que se passe-t-il si on multiplie par 10 ?
5. **Put to other uses**: Ce composant pourrait-il servir ailleurs ?
6. **Eliminate**: Que peut-on supprimer sans perdre de valeur ?
7. **Reverse**: Et si on inversait le flux ?

**Exemple:**
> Feature de recherche: Substitute = remplacer SQL par Elasticsearch. Combine = fusionner recherche + filtres en une UX unifiee. Eliminate = supprimer la pagination au profit du scroll infini. Reverse = au lieu de chercher, suggerer proactivement.

---

## Six Thinking Hats

**Description:** 6 perspectives structurees de De Bono pour analyser un sujet: White (faits), Red (emotions), Black (risques), Yellow (benefices), Green (creativite), Blue (process). Permet d'explorer systematiquement tous les angles.

**Quand utiliser:**
- Discussion qui tourne en rond
- Besoin de perspectives multiples
- Decision complexe avec enjeux emotionnels

**Phase recommandee:** Divergent

**Questions types:**
1. **White Hat**: Quels sont les faits objectifs dont on dispose ?
2. **Red Hat**: Quel est votre ressenti instinctif sur cette option ?
3. **Black Hat**: Quels sont les risques et points negatifs ?
4. **Yellow Hat**: Quels sont les benefices et opportunites ?
5. **Green Hat**: Quelles alternatives creatives existent ?
6. **Blue Hat**: Comment structurer notre reflexion ?

**Exemple:**
> Adoption de TypeScript: White = 40% moins de bugs runtime selon etudes. Red = Equipe enthousiaste mais craint la courbe d'apprentissage. Black = Migration couteuse, tooling a adapter. Yellow = Meilleure maintenabilite long terme. Green = Migration progressive par module. Blue = Pilote sur un microservice d'abord.

---

## Mind Mapping

**Description:** Arborescence visuelle partant d'un concept central vers des branches et sous-branches. Permet de structurer les idees de facon non-lineaire et de voir les connexions entre concepts.

**Quand utiliser:**
- Explorer un domaine complexe
- Organiser des idees en vrac
- Identifier les connexions cachees

**Phase recommandee:** Divergent

**Questions types:**
1. Quel est le concept central de cette feature ?
2. Quelles sont les grandes categories qui en decoulent ?
3. Quels liens existent entre ces branches ?

**Exemple:**
> Mind map "Systeme de notifications": Centre = Notifications. Branches = Types (push, email, in-app), Triggers (actions user, events systeme, scheduled), Preferences (frequence, canaux, opt-out), Technique (queue, templates, tracking). Connexions revelees: le tracking est lie aux preferences pour l'A/B testing.

---

## What If Scenarios

**Description:** Exploration de scenarios hypothetiques pour tester les limites et reveler les implications cachees. Poser des "Et si..." pour decouvrir des contraintes ou opportunites non evidentes.

**Quand utiliser:**
- Tester la robustesse d'une solution
- Explorer les cas limites
- Anticiper l'evolution future

**Phase recommandee:** Divergent

**Questions types:**
1. Et si le nombre d'utilisateurs etait multiplie par 100 ?
2. Et si cette API externe n'etait plus disponible ?
3. Et si cette feature devait fonctionner offline ?

**Exemple:**
> Feature de chat: "Et si 10000 users etaient connectes simultanement ?" → Revele le besoin de WebSocket avec load balancing. "Et si un message faisait 10MB ?" → Besoin de limites et compression. "Et si l'utilisateur changeait de device mid-conversation ?" → Besoin de sync multi-device.

---

## Analogical Thinking

**Description:** Transfert de patterns et solutions d'autres domaines vers le probleme actuel. Chercher des analogies dans la nature, d'autres industries ou des systemes connus pour inspirer des solutions.

**Quand utiliser:**
- Probleme sans solution evidente dans le domaine
- Besoin d'innovation radicale
- Recherche de patterns eprouves

**Phase recommandee:** Divergent

**Questions types:**
1. Quel systeme naturel resout un probleme similaire ?
2. Comment une autre industrie gere-t-elle ce type de defi ?
3. Quel pattern architectural connu s'applique ici ?

**Exemple:**
> Probleme de load balancing: Analogie avec le systeme nerveux qui distribue les signaux. Ou avec les fourmis qui optimisent les chemins. Solution inspiree: algorithme de pheromones pour router les requetes vers les serveurs les moins charges, avec "evaporation" progressive des routes sous-optimales.

---

## First Principles

**Description:** Deconstruction jusqu'aux verites fondamentales, en eliminant toutes les assumptions heritees. Repartir de zero pour reconstruire une solution sans les biais des solutions existantes.

**Quand utiliser:**
- Solution existante sous-optimale mais "c'est comme ca"
- Innovation de rupture necessaire
- Remise en question des standards du domaine

**Phase recommandee:** Divergent

**Questions types:**
1. Pourquoi faisons-nous les choses de cette facon ?
2. Quelles sont les verites fondamentales de ce probleme ?
3. Si on repartait de zero, que ferait-on differemment ?

**Exemple:**
> Systeme d'authentification: First principles = Un user doit prouver son identite. Assumption eliminee: "Il faut un mot de passe". Verite fondamentale: possession d'un device de confiance suffit. Solution: passwordless avec magic links + device fingerprinting, comme l'a fait Slack.
