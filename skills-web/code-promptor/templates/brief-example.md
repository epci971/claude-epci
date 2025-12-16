# Brief Example — Input → Output Reference

> Concrete example demonstrating PROMPTOR transformation

---

## Example 1: Standard Mode (Medium Complexity)

### INPUT (Raw Transcript)

```
Alors euh donc voilà, l'idée c'est qu'on a besoin d'un truc pour gérer les factures 
quoi. En gros euh les commerciaux ils font leurs devis sur le CRM là, Salesforce, 
et après bah faut que ça génère une facture automatiquement tu vois.

Au début je pensais faire un export CSV et puis reimporter mais non en fait c'est 
trop galère, on va plutôt faire une intégration directe avec l'API Salesforce.

Donc euh il faut que le système il récupère les devis validés, qu'il génère la 
facture au format PDF, et qu'il l'envoie par mail au client. Ah et aussi faut 
stocker ça dans notre ERP, c'est SAP.

C'est important que ce soit rapide hein, genre moins de 30 secondes pour générer 
une facture. Et faut que ça marche bien parce que les commerciaux ils vont râler 
sinon.

On est sur Symfony 6 côté back et React pour le front. Ah et faut que ça soit 
conforme RGPD évidemment vu qu'on stocke des données clients.

Peut-être qu'on ajoutera un tableau de bord plus tard pour voir les stats mais 
bon c'est pas prioritaire pour l'instant.
```

### OUTPUT (Generated Brief)

```markdown
<!-- PROMPTOR_META
confidence: high
mode: standard
source_complexity: medium
extraction_gaps: 0
-->

# Module de facturation automatique avec intégration Salesforce-SAP

## Objective

Cette fonctionnalité vise à automatiser la génération de factures à partir des devis validés dans Salesforce. Elle permettra aux commerciaux d'obtenir des factures PDF envoyées automatiquement aux clients, tout en assurant la synchronisation avec l'ERP SAP. Le besoin principal est d'éliminer les manipulations manuelles entre le CRM et le système de facturation.

## Description

Le module s'intègre dans un écosystème existant comprenant Salesforce (CRM) et SAP (ERP). Le flux de travail consiste à surveiller les devis validés dans Salesforce, générer automatiquement les factures correspondantes, les transmettre aux clients par email, et synchroniser les données avec SAP pour la comptabilité.

L'intégration se fait via l'API Salesforce plutôt que par export/import CSV, choix retenu pour sa fiabilité et son automatisation complète.

## Functional Requirements

- [FR1] Le système récupère automatiquement les devis ayant le statut "validé" depuis Salesforce via son API
- [FR2] Le système génère une facture au format PDF à partir des données du devis
- [FR3] Le système envoie automatiquement la facture par email au client concerné
- [FR4] Le système synchronise les données de facturation avec l'ERP SAP

## Non-Functional Requirements

- [NFR1] Le temps de génération d'une facture doit être inférieur à 30 secondes
- [NFR2] Le système doit être conforme aux exigences RGPD pour le stockage des données clients

## Constraints & Technical Context

- Stack backend : Symfony 6
- Stack frontend : React
- CRM source : Salesforce (intégration via API)
- ERP cible : SAP
- Format de sortie : PDF

## Important Notes

- Un tableau de bord de statistiques est envisagé pour une phase ultérieure mais n'est pas prioritaire pour cette itération
- L'approche par export CSV a été initialement considérée puis abandonnée au profit de l'intégration API directe
```

---

## Example 2: Compact Mode (Simple Input)

### INPUT (Short Transcript)

```
J'ai besoin d'un bouton sur la page produit qui permet d'exporter la fiche en PDF. 
C'est pour les clients qui veulent imprimer. Rien de compliqué.
```

### OUTPUT (Compact Brief)

```markdown
<!-- PROMPTOR_META
confidence: high
mode: compact
-->

# Bouton d'export PDF sur fiche produit

## Objective

Permettre aux clients d'exporter et imprimer les fiches produit au format PDF via un bouton dédié sur la page produit.

## Quick Notes

- Fonctionnalité destinée à l'impression par les clients
- Aucune complexité particulière signalée
```

---

## Example 3: Low Confidence (Vague Input)

### INPUT (Poor Transcript)

```
Euh ouais donc faudrait améliorer le truc là, le machin des commandes. C'est pas 
top en ce moment. Faudrait que ça soit mieux quoi. Peut-être plus rapide ou je 
sais pas. On verra.
```

### OUTPUT (Low Confidence Brief)

```markdown
<!-- PROMPTOR_META
confidence: low
mode: standard
source_complexity: short
extraction_gaps: 3+
-->

# Amélioration du module de commandes

## Objective

Une amélioration du système de gestion des commandes est souhaitée. Les aspects précis à améliorer et les critères de succès restent à définir.

## Description

Le système actuel de commandes est perçu comme insatisfaisant. Les axes d'amélioration potentiels incluent la performance, mais aucune direction claire n'a été établie.

## Functional Requirements

- Aucun FR explicitement mentionné dans la source.

## Non-Functional Requirements

- [NFR1] Amélioration de la rapidité évoquée comme piste potentielle (non confirmée)

## Constraints & Technical Context

- Aucune contrainte technique ou métier explicitement mentionnée.

## Important Notes

- L'intention reste vague et nécessite une clarification approfondie
- Aucun critère de succès défini
- La décision finale reportée ("on verra")
```

---

## Key Transformation Patterns

### Speech → Professional

| Raw | Clean |
|-----|-------|
| "le truc là" | "le système/module" |
| "ça marche bien" | "le système fonctionne de manière fiable" |
| "c'est important que" | "[NFR] Exigence de..." |
| "faut que" | "Le système doit" |
| "tu vois" | [supprimé] |
| "genre" | [supprimé ou reformulé] |

### Contradiction Resolution

| Before | After |
|--------|-------|
| "On fait CSV... non en fait API" | Only API mentioned in brief |
| "Peut-être X ou Y" | Note ambiguity, don't choose |
| "D'abord A, puis finalement B" | Only B in requirements |

### Intent Classification

| Phrase Pattern | Classification |
|----------------|----------------|
| "L'idée c'est de..." | Objective |
| "En gros ça fonctionne comme..." | Description |
| "Il faut que le système..." | FR |
| "C'est important que ce soit rapide" | NFR |
| "On est sur Symfony" | Constraint |
| "Peut-être plus tard..." | Important Notes |
