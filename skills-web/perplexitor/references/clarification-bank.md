# Clarification Bank — Questions Contextuelles

> Banque de questions pour le mode Guidé (clarté < 60)

---

## Principes

1. **Maximum 1 question** — Jamais d'interrogatoire
2. **Question composite** — Regrouper si possible
3. **Toujours proposer P1** — Best effort en parallèle
4. **Option skip** — "Tape `go` pour continuer avec mon interprétation"

---

## Questions par Type d'Ambiguïté

### Temporalité Floue

**Détection** : Pas de période mentionnée + sujet évolutif

**Question** :
> Tu cherches des infos récentes (2024-2025) ou un historique plus large ?

**Variantes** :
- "Quelle période t'intéresse : actualités récentes ou vue d'ensemble historique ?"
- "Focus sur les derniers mois ou vision long terme ?"

---

### Scope Trop Large

**Détection** : Sujet vaste + pas d'angle précis

**Question** :
> Tu veux une vue d'ensemble de [sujet] ou un aspect précis ?
> (ex: [aspect 1], [aspect 2], [aspect 3]...)

**Exemples** :
- "Tu veux une vue d'ensemble de Docker ou un aspect précis ? (networking, volumes, orchestration, sécurité...)"
- "Tu cherches quoi sur l'IA : tendances générales, un domaine spécifique, ou des outils concrets ?"

---

### Intention Incertaine

**Détection** : Impossible de classifier (factuelle vs exploratoire vs décisionnelle)

**Question** :
> Tu cherches à comprendre, comparer, ou décider quelque chose ?

**Variantes** :
- "C'est pour apprendre sur le sujet, comparer des options, ou prendre une décision ?"
- "Besoin d'infos générales, d'un comparatif, ou d'aide pour choisir ?"

---

### Contexte Manquant

**Détection** : Sujet technique sans contexte d'usage

**Question** :
> C'est pour quel contexte : perso, pro, académique ?
> [Si tech] Quelle stack / environnement ?

**Exemples** :
- "C'est pour un projet pro ou perso ? Quelle stack ?"
- "Contexte : startup, grande entreprise, side project ?"

---

### Niveau de Détail

**Détection** : Ambiguïté entre réponse courte et analyse approfondie

**Question** :
> Tu veux une réponse rapide ou une analyse détaillée avec sources ?

**Variantes** :
- "Besoin d'un aperçu rapide ou d'un deep dive avec données chiffrées ?"
- "Quick answer ou recherche approfondie ?"

---

### Domaine Ambigu

**Détection** : Terme polysémique (ex: "tests", "migration", "cloud")

**Question** :
> Tu parles de [sens 1], [sens 2], ou [sens 3] ?

**Exemples** :
- "Tu parles de tests logiciels, tests A/B, ou tests médicaux ?"
- "Migration : données, infrastructure, ou framework ?"
- "Cloud : hébergement, stockage, ou services managés ?"

---

## Templates de Question Composite

### Template 1 : Domaine + Contexte
```
Tu parles de [domaine A] ou [domaine B] ? Et c'est pour quel contexte ?
```

### Template 2 : Scope + Profondeur
```
Tu veux [vue large] ou [focus précis] ? Et plutôt aperçu rapide ou analyse détaillée ?
```

### Template 3 : Intention + Période
```
C'est pour [comprendre | comparer | décider] ? Et sur quelle période ?
```

---

## Format de Sortie Mode Guidé

```markdown
## 🔎 Perplexitor

**Demande** : [reformulation nettoyée]
**Type** : [Type détecté] (incertain)
**Clarté** : [Score]/100

---

### 🎯 P1 — Best effort ([hypothèse]) [Mode]

```
[Prompt généré avec la meilleure interprétation]
```

⏱️ ~[temps] | 📊 [sources]

---

**❓ Pour affiner** :

[Question contextuelle]

Options :
- **[Option A]** → [conséquence sur le prompt]
- **[Option B]** → [conséquence sur le prompt]
- **[Option C]** → [conséquence sur le prompt]

Tape `go` pour continuer avec mon interprétation ([hypothèse retenue]).
```

---

## Exemples Complets

### Exemple 1 : Domaine Ambigu

**Input** : "cherche des infos sur les migrations"

**Output** :
```markdown
## 🔎 Perplexitor

**Demande** : Recherche sur les migrations
**Type** : Exploratoire (incertain)
**Clarté** : 28/100

---

### 🎯 P1 — Best effort (migrations techniques) 🔬

```
État de l'art des stratégies de migration de systèmes d'information en 2025.
Types couverts : migration vers le cloud, migration de données, 
migration de frameworks et langages.
Bonnes pratiques, outils recommandés, risques courants et comment les éviter.
Sources récentes (2024-2025) en français et anglais.
```

⏱️ ~3-5 min | 📊 20-30 sources

---

**❓ Pour affiner** :

Tu parles de quel type de migration ?
- **Technique** (cloud, données, framework) → P1 ci-dessus
- **Base de données** (schéma, ORM) → je reformule
- **Autre** (migratoire, oiseaux...) → précise-moi

Tape `go` pour continuer avec l'interprétation technique.
```

---

### Exemple 2 : Scope Large

**Input** : "je veux en savoir plus sur kubernetes"

**Output** :
```markdown
## 🔎 Perplexitor

**Demande** : En savoir plus sur Kubernetes
**Type** : Exploratoire
**Clarté** : 45/100

---

### 🎯 P1 — Best effort (vue d'ensemble) 🔬

```
État de l'art de Kubernetes en 2025.
Architecture et concepts clés, écosystème (Helm, Operators, service mesh).
Cas d'usage typiques, avantages par rapport aux alternatives, 
et quand ne PAS utiliser Kubernetes.
Format : synthèse structurée pour quelqu'un qui découvre K8s.
Sources récentes (2024-2025) en français et anglais.
```

⏱️ ~3-5 min | 📊 20-30 sources

---

**❓ Pour affiner** :

Tu veux une vue d'ensemble ou un aspect précis de Kubernetes ?
- **Vue d'ensemble** → P1 ci-dessus
- **Aspect précis** → dis-moi lequel (réseau, stockage, sécurité, monitoring, CI/CD...)

Tape `go` pour la vue d'ensemble.
```

---

## Règles de Non-Clarification

Ne PAS poser de question si :

| Situation | Action |
|-----------|--------|
| Clarté ≥ 60 | Mode Express, pas de question |
| Question rhétorique | Interpréter littéralement |
| Contexte évident | Utiliser le bon sens |
| Demande explicite simple | Répondre directement |

---

## Gestion du Skip

Si l'utilisateur tape `go`, `continue`, `génère`, ou ne répond pas :

1. **Utiliser l'hypothèse P1** comme base
2. **Générer P2 et P3** selon le type détecté
3. **Mentionner l'hypothèse** : "Basé sur mon interprétation ([hypothèse])..."
