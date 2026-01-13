# Template : 📋 Réunion

## Compatibilité v2

Ce template conserve le comportement de Resumator v2 pour les comptes-rendus de réunion.

---

## Structure du rapport

```markdown
# 📋 Compte-Rendu de Réunion — [YYYY-MM-DD]

**Objet** : [Titre intelligent <80 chars, style objet email]
**Type** : [Type détecté] / [Sous-type si applicable]
**Participants** : [Liste des participants identifiés]
**Durée** : [Durée estimée ou mentionnée]

---

## 🎯 Résumé Exécutif

[3-5 bullet points des points clés, décisions majeures, actions critiques]

---

## 📌 Contexte

[Paragraphe situant la réunion : projet concerné, étape, enjeux, 
liens avec réunions précédentes si mentionnés]

---

## 💬 Sujets Discutés

### 1. [Premier sujet majeur]

[Développement du sujet avec les points abordés, arguments échangés,
conclusions partielles]

[Si flux détecté → Diagramme Mermaid contextuel]

### 2. [Deuxième sujet]

[...]

### N. [Autres sujets]

---

## ✅ Décisions Prises

| # | Décision | Contexte | Impact |
|---|----------|----------|--------|
| D1 | [Décision] | [Pourquoi] | [Conséquence] |
| D2 | ... | ... | ... |

---

## 📝 Actions

| Responsable | Action | Échéance | Statut |
|-------------|--------|----------|--------|
| [Nom] | [Action verbale] | [Date/délai] | 🟢/🟡/🔴 |
| ... | ... | ... | ... |

> 📊 **Complétude** : X% des actions ont un responsable ET une échéance

### Légende des statuts
- 🟢 Responsable ET échéance définis
- 🟡 Responsable OU échéance (un manquant)
- 🔴 Ni responsable ni échéance

---

## 💡 Insights & Pistes

### 🔧 Améliorations suggérées
- [Opportunité d'amélioration identifiée]

### 🔶 Dette technique détectée
- [Workaround, solution temporaire mentionnée]

### 💭 Idées à explorer
- [Idée évoquée mais non actionnée]

---

## ⚠️ Points de Vigilance

- [Risque ou préoccupation exprimée]
- [Bloquant potentiel identifié]

---

## ❓ Questions Ouvertes

- [Question restée sans réponse]
- [Point nécessitant clarification]

---

## 🔜 Prochaines Étapes

- [ ] [Suggestion de prochaine réunion ou action]
- [ ] [Suivi recommandé]

---

## 📚 Glossaire

| Terme | Définition |
|-------|------------|
| [Acronyme] | [Signification] |
| [Terme technique] | [Explication] |

---

## 💬 Verbatims Clés

> "[Citation impactante]" — [Auteur]

---

*Généré par Resumator v3.0 — [Date]*
```

---

## Détection du type de réunion

| Type | Indicateurs | Plan adapté |
|------|-------------|-------------|
| **Pilotage/Décision** | "décision", "valider", "arbitrer", budget, deadlines, "go/no-go" | Focus décisions, impacts |
| **Information** | "informer", "présenter", "point d'avancement", updates | Focus synthèse, suivi |
| **Brainstorming** | "idées", "propositions", "explorer", créatif | Focus idées, pas de décisions |
| **Formation/Atelier** | "formation", "exercice", "atelier", apprentissage | Focus acquis, exercices |
| **Revue individuelle** | 1:1, feedback, performance, objectifs | Focus feedback, actions perso |
| **Technique/Archi** | "architecture", "workflow", "API", "BDD", termes tech | Focus diagrammes, specs |
| **Générique** | Aucun indicateur clair | Plan neutre équilibré |

---

## Règles spécifiques réunion

### Actions
- EXHAUSTIVITÉ : Chaque engagement verbal = ligne dans le tableau
- Format : Verbe d'action + objet (ex: "Finaliser le document X")
- Échéance : Date précise ou relative ("demain", "fin de semaine")

### Diagrammes contextuels
- Placer dans la section où le flux est discuté
- Max 4 diagrammes pour niveau 3
- Types fréquents : flowchart (process), sequence (échanges), gantt (planning)

### Proactive insights
- 🔧 Si mention de répétition manuelle → suggérer automatisation
- 🔶 Si "pour l'instant", "temporaire", "workaround" → dette technique
- 💭 Si "on pourrait", "il faudrait" sans action → idée à explorer

---

## Adaptations par niveau

| Section | Niv 1-2 | Niv 3 | Niv 4-5 |
|---------|---------|-------|---------|
| Résumé exécutif | = tout | ✅ | ✅ |
| Contexte | ❌ | ✅ | ✅ enrichi |
| Sujets discutés | Bullet points | Détaillé | Exhaustif |
| Décisions | Liste | Tableau | Tableau + impacts |
| Actions | Liste | Tableau + statuts | Tableau + historique |
| Insights | ❌ | ✅ | ✅ + recherche web |
| Glossaire | ❌ | Si acronymes | ✅ complet |
| Verbatims | ❌ | 1-2 max | Tous pertinents |
