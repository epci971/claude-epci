# Template : 📊 Audit

## Usage

Analyse critique avec évaluation par critères, scoring et recommandations priorisées.

---

## Structure du rapport

```markdown
# 📊 Audit : [Sujet]

> **Type** : [Technique/Organisationnel/Sécurité/Performance/...]
> **Périmètre** : [Ce qui est audité]
> **Date** : [YYYY-MM-DD]

---

## 🎯 Score Global

```
██████████████████░░ 72/100
```

| Dimension | Score | Tendance |
|-----------|-------|----------|
| [Dimension 1] | 85/100 | ✅ |
| [Dimension 2] | 60/100 | ⚠️ |
| [Dimension 3] | 70/100 | ➡️ |

**Verdict** : [Synthèse en 1-2 phrases]

---

## 📋 Synthèse Exécutive

### Points forts 💪
- [Point fort 1]
- [Point fort 2]

### Points d'amélioration 🔧
- [Point faible 1]
- [Point faible 2]

### Actions prioritaires 🎯
1. [Action critique 1]
2. [Action importante 2]
3. [Action souhaitable 3]

---

## 📊 Grille d'Évaluation Détaillée

### Dimension 1 : [Nom]

| Critère | Score | Constat | Recommandation |
|---------|-------|---------|----------------|
| [Critère 1.1] | ⭐⭐⭐⭐ | [Observation] | [Action] |
| [Critère 1.2] | ⭐⭐ | [Observation] | [Action] |
| [Critère 1.3] | ⭐⭐⭐⭐⭐ | [Observation] | — |

**Score dimension** : 75/100

**Analyse** : [Synthèse de la dimension]

### Dimension 2 : [Nom]

[Même structure...]

### Dimension N : [Nom]

[...]

---

## 🔍 Constats Détaillés

### Constat 1 : [Titre]

**Observation** : [Description factuelle]

**Impact** : 🔴 Critique / 🟡 Important / 🟢 Mineur

**Preuve** : [Source/évidence]

**Recommandation** : [Action corrective]

### Constat 2 : [Titre]

[Même structure...]

---

## ✅ Points de Conformité

| Exigence | Statut | Commentaire |
|----------|--------|-------------|
| [Exigence 1] | ✅ Conforme | [Détail] |
| [Exigence 2] | ⚠️ Partiel | [Détail] |
| [Exigence 3] | ❌ Non conforme | [Détail] |

---

## ⚠️ Risques Identifiés

| Risque | Probabilité | Impact | Criticité | Mitigation |
|--------|-------------|--------|-----------|------------|
| [Risque 1] | Haute | Fort | 🔴 | [Action] |
| [Risque 2] | Moyenne | Moyen | 🟡 | [Action] |
| [Risque 3] | Basse | Faible | 🟢 | [Action] |

### Matrice des risques

```
Impact ↑
  Fort  │ 🟡  🔴  🔴
 Moyen  │ 🟢  🟡  🔴
 Faible │ 🟢  🟢  🟡
        └─────────────→ Probabilité
          Basse Moyenne Haute
```

---

## 📈 Plan d'Action

### Actions immédiates (< 1 semaine)

| # | Action | Responsable | Échéance | Effort |
|---|--------|-------------|----------|--------|
| 1 | [Action] | [Qui] | [Date] | [J/H] |

### Actions court terme (< 1 mois)

| # | Action | Responsable | Échéance | Effort |
|---|--------|-------------|----------|--------|
| 2 | [Action] | [Qui] | [Date] | [J/H] |

### Actions moyen terme (< 3 mois)

| # | Action | Responsable | Échéance | Effort |
|---|--------|-------------|----------|--------|
| 3 | [Action] | [Qui] | [Date] | [J/H] |

---

## 📊 Métriques de Suivi

| KPI | Valeur actuelle | Cible | Échéance |
|-----|-----------------|-------|----------|
| [KPI 1] | [Valeur] | [Cible] | [Date] |
| [KPI 2] | [Valeur] | [Cible] | [Date] |

---

## 🔄 Comparaison avec Audit Précédent

[Si applicable]

| Dimension | Précédent | Actuel | Évolution |
|-----------|-----------|--------|-----------|
| [Dim 1] | 65/100 | 75/100 | ↗️ +10 |
| [Dim 2] | 70/100 | 60/100 | ↘️ -10 |

---

## 📎 Annexes

### A. Méthodologie d'audit
[Description de l'approche]

### B. Référentiel utilisé
[Standards, normes, bonnes pratiques]

### C. Liste des entretiens/observations
[Si applicable]

### D. Documents analysés
[Liste des sources]

---

## 🏷️ Métadonnées

| Champ | Valeur |
|-------|--------|
| Auditeur | [Resumator v3.0] |
| Date | [YYYY-MM-DD] |
| Version | 1.0 |
| Prochaine révision | [Date suggérée] |

---

*Audit généré par Resumator v3.0 — [Date]*
```

---

## Spécificités audit

### Objectivité
- Constats factuels, pas d'opinions
- Chaque constat a une preuve/source
- Scoring cohérent et justifié

### Priorisation
- Actions classées par criticité
- Effort estimé pour chaque action
- Responsables identifiés si possible

### Suivi
- KPIs mesurables proposés
- Échéances réalistes
- Lien avec audits précédents si existants

---

## Types d'audit supportés

| Type | Focus | Critères typiques |
|------|-------|-------------------|
| **Technique** | Code, architecture | Qualité, maintenabilité, performance |
| **Sécurité** | Vulnérabilités | OWASP, bonnes pratiques |
| **Performance** | Vitesse, scalabilité | Temps de réponse, charge |
| **UX** | Expérience utilisateur | Usabilité, accessibilité |
| **Organisationnel** | Process, équipe | Efficacité, communication |
| **Conformité** | Réglementaire | RGPD, normes sectorielles |

---

## Adaptations par niveau

| Section | Niv 1-2 | Niv 3 | Niv 4-5 |
|---------|---------|-------|---------|
| Score global | ✅ | ✅ | ✅ + dimensions |
| Synthèse | = tout | ✅ | ✅ |
| Grille détaillée | ❌ | Par dimension | Par critère |
| Constats | Top 3 | Tous | + preuves détaillées |
| Risques | Liste | Tableau | + matrice |
| Plan d'action | Actions clés | Priorisé | + effort/responsable |
| Métriques | ❌ | ❌ | ✅ |
| Comparaison | ❌ | ❌ | Si dispo |
| Annexes | ❌ | ❌ | ✅ |
