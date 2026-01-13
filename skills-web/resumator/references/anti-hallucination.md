# Règles anti-hallucination

## Principe fondamental

> **Toute affirmation doit avoir une source traçable ou être marquée comme incertaine.**

Ceci est le différenciateur clé de Resumator : zéro invention, traçabilité totale.

---

## Règles obligatoires

### 1. Citation systématique

| Type d'information | Citation requise |
|-------------------|------------------|
| Fait vérifiable | [N] ou [🌐N] obligatoire |
| Opinion/avis | [N] + mention "selon [source]" |
| Statistique/chiffre | [N] obligatoire + date si ancienne |
| Date/deadline | [N] ou "mentionné dans la source" |
| Affirmation technique | [N] ou [🌐N] obligatoire |

### 2. Marquage des incertitudes

Si une information ne peut être vérifiée :

```markdown
⚠️ **Non vérifié** : [information]
```

ou inline :

```markdown
... cette fonctionnalité serait disponible (⚠️ non vérifié).
```

### 3. Formulations interdites

| ❌ Interdit | ✅ Correct |
|------------|-----------|
| "Probablement..." | "Selon [N], ..." ou "⚠️ non vérifié" |
| "Il semble que..." | "[N] indique que..." |
| "On peut supposer..." | "Hypothèse : ... (non sourcé)" |
| "Généralement..." | "[N] recommande..." ou citer études |
| Affirmation sans [N] | Toujours citer la source |

### 4. Synthèse vs Invention

| ✅ Synthèse acceptable | ❌ Invention interdite |
|----------------------|---------------------|
| Reformuler en conservant le sens | Ajouter des informations non présentes |
| Combiner infos de plusieurs sources (tracées) | Inventer des connexions non explicites |
| Simplifier un concept complexe | Supposer des intentions/motivations |
| Structurer des éléments épars | Combler les trous avec des suppositions |

---

## Format des citations

### Sources fournies
```
[1] — Première source fournie
[2] — Deuxième source fournie
[N] — Nième source
```

### Sources web recherchées
```
[🌐1] — Première source web
[🌐2] — Deuxième source web
[🌐N] — Nième source web
```

### Citation inline
```markdown
Claude Code permet de déléguer des tâches depuis le terminal [1].
La limite de contexte est de 200k tokens [🌐1].
```

### Citation multi-sources
```markdown
L'installation requiert Node.js 18+ [1][🌐2] et npm [2].
```

---

## Gestion des contradictions

### Détection
Quand deux sources disent des choses différentes :

```markdown
> ⚠️ **Contradiction détectée** :
> - Source [1] : "Limite à 100k tokens"
> - Source [2] : "Limite à 200k tokens"
> 
> **Résolution** : La documentation officielle [🌐1] confirme 200k.
```

### Si non résolvable

```markdown
> ⚠️ **Information contradictoire** :
> - Selon [1] : [version A]
> - Selon [2] : [version B]
> 
> Cette contradiction n'a pas pu être résolue. Vérification recommandée.
```

---

## Niveaux de confiance

### Par source

| Score | Signification | Usage |
|-------|--------------|-------|
| ⭐⭐⭐⭐⭐ | Source primaire, officielle | Peut être citée directement |
| ⭐⭐⭐⭐ | Source secondaire fiable | Citer avec attribution |
| ⭐⭐⭐ | Source communautaire | Citer + "selon [communauté]" |
| ⭐⭐ | Source à vérifier | Marquer ⚠️ ou écarter |
| ⭐ | Source non fiable | Écarter |

### Par information

```markdown
| Information | Confiance | Raison |
|-------------|-----------|--------|
| Installation via npm | ⭐⭐⭐⭐⭐ | Doc officielle [🌐1] |
| Limite 200k tokens | ⭐⭐⭐⭐⭐ | Annonce Anthropic [🌐2] |
| "Meilleur que Cursor" | ⭐⭐⭐ | Opinion Reddit [3] |
| Support Windows | ⚠️ | Non confirmé officiellement |
```

---

## Checklist avant génération

Avant de générer le rapport, vérifier :

- [ ] Chaque fait a une citation [N] ou [🌐N]
- [ ] Aucune affirmation sans source
- [ ] Contradictions documentées ou résolues
- [ ] Incertitudes marquées ⚠️
- [ ] Opinions attribuées à leur source
- [ ] Chiffres/stats datés si anciens
- [ ] Bibliographie complète en fin de document

---

## Exemples

### ✅ Bon exemple

```markdown
## Installation

Claude Code s'installe via npm avec la commande `npm install -g claude-code` [1]. 
Le processus nécessite Node.js 18 ou supérieur [🌐1]. Sur macOS, une étape 
supplémentaire de configuration Terminal est requise [1].

> ⚠️ **Note** : Le support Windows est mentionné comme "coming soon" [🌐2] 
> mais aucune date n'est confirmée.
```

### ❌ Mauvais exemple

```markdown
## Installation

Claude Code s'installe facilement via npm. Il faut probablement Node.js 
récent. Sur macOS, il y a quelques configurations à faire. Le support 
Windows devrait arriver bientôt.
```

Problèmes :
- "facilement" = jugement non sourcé
- "probablement" = incertitude non marquée
- "quelques configurations" = vague, non sourcé
- "devrait arriver bientôt" = supposition non sourcée
