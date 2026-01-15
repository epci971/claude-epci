# Techniques d'Analyse

> 8 techniques pour evaluer, prioriser et decider.
> Phase recommandee: Convergent (sauf Question Storming: Deblocage)

---

## MoSCoW

**Description:** Methode de priorisation categorisant les elements en Must (indispensable), Should (important), Could (souhaitable) et Won't (hors scope). Permet de clarifier les priorites et de gerer les attentes.

**Quand utiliser:**
- Trop de features a trier
- Besoin de definir le MVP
- Negociation du scope avec stakeholders

**Phase recommandee:** Convergent

**Questions types:**
1. Cette fonctionnalite est-elle bloquante pour le lancement ?
2. Quel est l'impact business si on la reporte en v2 ?
3. Quelles sont les dependances techniques de cette feature ?

**Exemple:**
> Pour une refonte d'API: Must = endpoints existants, Should = nouveaux endpoints demandes, Could = optimisations performance, Won't = migration GraphQL (v2).

---

## 5 Whys

**Description:** Technique d'analyse causale iterative. En demandant "Pourquoi ?" cinq fois successivement, on remonte du symptome a la cause racine du probleme.

**Quand utiliser:**
- Probleme recurrent non resolu
- Symptome evident mais cause floue
- Besoin de comprendre l'origine d'un bug

**Phase recommandee:** Convergent

**Questions types:**
1. Pourquoi ce probleme se produit-il ?
2. Pourquoi cette condition existe-t-elle ?
3. Pourquoi n'avons-nous pas detecte ca plus tot ?

**Exemple:**
> Bug de performance: Pourquoi lent ? → Requetes N+1. Pourquoi N+1 ? → Pas d'eager loading. Pourquoi ? → ORM mal configure. Pourquoi ? → Pas de revue des requetes. Pourquoi ? → Pas de monitoring SQL. Cause racine: absence de monitoring.

---

## SWOT

**Description:** Analyse strategique evaluant les Forces (Strengths), Faiblesses (Weaknesses), Opportunites (Opportunities) et Menaces (Threats) d'une option. Vision 360 pour decisions eclairees.

**Quand utiliser:**
- Comparaison d'approches techniques
- Evaluation d'une nouvelle technologie
- Decision d'architecture importante

**Phase recommandee:** Convergent

**Questions types:**
1. Quels sont les avantages techniques de cette approche ?
2. Quelles limitations ou risques sont inherents ?
3. Quelles opportunites futures cette approche ouvre-t-elle ?

**Exemple:**
> Adoption de microservices: Forces = scalabilite, deploiement independant. Faiblesses = complexite operationnelle, latence reseau. Opportunites = equipes autonomes. Menaces = debugging distribue, cout infra.

---

## Scoring

**Description:** Matrice de decision multicriteres. Definir des criteres ponderes, noter chaque option, calculer les scores pour une decision objective et tracable.

**Quand utiliser:**
- Plusieurs options techniques a comparer
- Besoin de justifier un choix aupres des stakeholders
- Criteres multiples avec poids differents

**Phase recommandee:** Convergent

**Questions types:**
1. Quels sont les criteres de decision les plus importants ?
2. Comment ponderer performance vs maintenabilite ?
3. Quelle note donneriez-vous a chaque option sur ce critere ?

**Exemple:**
> Choix de base de donnees: Criteres = Performance (30%), Scalabilite (25%), Cout (25%), Expertise equipe (20%). PostgreSQL: 4.2/5. MongoDB: 3.8/5. DynamoDB: 3.5/5. Decision: PostgreSQL.

---

## Pre-mortem

**Description:** Exercice d'anticipation des echecs. Se projeter dans un futur ou le projet a echoue, identifier les causes possibles, evaluer probabilite x impact, definir des mitigations preventives.

**Quand utiliser:**
- Avant une decision finale importante
- Projet a risque identifie
- Lancement d'une feature critique

**Phase recommandee:** Convergent

**Questions types:**
1. Si ce projet echoue dans 3 mois, quelles seront les causes ?
2. Quelle est la probabilite de ce scenario d'echec ?
3. Quelle action preventive peut reduire ce risque ?

**Exemple:**
> Migration de BDD: Risque 1 = Corruption de donnees (P:2, I:3, Score:6) → Mitigation: backup incremental + rollback automatise. Risque 2 = Downtime prolonge (P:2, I:2, Score:4) → Mitigation: migration en blue-green.

---

## Constraint Mapping

**Description:** Visualisation exhaustive de toutes les contraintes d'un projet. Categoriser en contraintes techniques, business, temporelles, reglementaires pour avoir une vision complete des limites.

**Quand utiliser:**
- Debut de projet pour cadrer le possible
- Blocage inexplique sur une solution
- Besoin de challenger les contraintes implicites

**Phase recommandee:** Convergent

**Questions types:**
1. Quelles sont les contraintes techniques non negociables ?
2. Quelles contraintes business impactent la solution ?
3. Y a-t-il des contraintes reglementaires (GDPR, PCI-DSS) ?

**Exemple:**
> Refonte checkout: Contraintes techniques = API payment existante, timeout 30s. Business = pas de regression conversion. Temporelles = release avant Black Friday. Reglementaires = PCI-DSS niveau 1.

---

## Assumption Reversal

**Description:** Challenger les hypotheses de base en les inversant. Reveler les assumptions implicites qui limitent la reflexion et ouvrir de nouvelles pistes de solution.

**Quand utiliser:**
- Solution bloquee dans un schema de pensee
- Besoin de penser "out of the box"
- Verification des hypotheses fondamentales

**Phase recommandee:** Convergent

**Questions types:**
1. Quelles hypotheses faisons-nous implicitement ?
2. Que se passerait-il si cette hypothese etait fausse ?
3. Comment resoudrions-nous le probleme sans cette contrainte ?

**Exemple:**
> Hypothese: "Les utilisateurs ont besoin d'un compte pour acheter". Inversion: Et si on permettait l'achat en guest ? Decouverte: 30% des abandons de panier sont lies a la creation de compte. Solution: guest checkout avec option de creer un compte apres achat.

---

## Question Storming

**Description:** Generer des questions avant de chercher des reponses. Au lieu de brainstormer des solutions, brainstormer des questions pour explorer le probleme sous tous ses angles.

**Quand utiliser:**
- Probleme mal defini ou flou
- Equipe qui saute trop vite aux solutions
- Besoin de recadrer la reflexion

**Phase recommandee:** Deblocage

**Questions types:**
1. Quelles questions n'avons-nous pas encore posees ?
2. Qu'est-ce qu'un nouvel arrivant demanderait en voyant ce probleme ?
3. Quelle question nous fait peur de poser ?

**Exemple:**
> Probleme: "L'onboarding est trop long". Questions generees: Pourquoi a-t-on besoin de toutes ces infos ? Qui a decide de cet ordre d'etapes ? Quels users completent vraiment tout ? Que font les concurrents ? → La question "Qui a decide..." revele que personne ne sait, menant a une remise a plat complete.
