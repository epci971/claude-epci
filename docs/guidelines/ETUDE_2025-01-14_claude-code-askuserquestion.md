# 🔬 Étude Complémentaire : AskUserQuestion — L'Outil de Clarification Interactive

> **Niveau** : 4 (Approfondi) | **Date** : 2025-01-14 | **Sources** : 1 fournie + 8 web
> **Confiance globale** : ⭐⭐⭐⭐ (4/5)
> **Complément à** : ETUDE_2025-01-14_claude-code-2.1.md

---

## 🎯 Synthèse Exécutive

L'outil **AskUserQuestion**, introduit en version 2.0.21, inverse le paradigme traditionnel de l'interaction AI : au lieu que l'utilisateur perfectionne son prompt, c'est **Claude qui vous interview**. Cette fonctionnalité, souvent sous-estimée, permet de réduire les cycles de rework de **50 à 80%** en résolvant les ambiguïtés avant l'exécution du code.

**Points clés** :
- Claude présente des questions QCM avec options contextualisées
- Intégration native avec Plan Mode pour le "spec-based development"
- Timeout de 60 secondes par question
- Non disponible dans les sous-agents (main thread uniquement)

**Verdict** : Fonctionnalité transformative pour la qualité du code. L'activer dans les settings devrait être un réflexe pour tout projet complexe.

---

## 📌 Contexte et Périmètre

### Pourquoi cette étude complémentaire ?

La vidéo source [1] mentionne AskUserQuestion comme "fonctionnalité clairement sous-côtée". Cette étude approfondit son fonctionnement, ses patterns d'usage et son intégration dans les workflows modernes.

### Questions auxquelles elle répond

- Comment fonctionne techniquement AskUserQuestion ?
- Comment l'activer et le configurer ?
- Quels sont les patterns d'usage recommandés ?
- Quelles sont les limitations à connaître ?

### Délimitation

- **Inclus** : Fonctionnement, configuration, patterns, limitations
- **Exclu** : Intégrations tierces (Linear, Cyrus), SDK programmatique

---

## 🔍 Méthodologie

### Source fournie

| # | Type | Source | Fiabilité |
|---|------|--------|-----------|
| [1] | Transcription YouTube | "Cloud Code 2.1 : La Mise à Jour MASSIVE" — Para | ⭐⭐⭐⭐ |

### Sources web recherchées

| # | URL | Titre | Date | Fiabilité |
|---|-----|-------|------|-----------|
| [🌐1] | atcyrus.com | "What is Claude Code's AskUserQuestion tool?" | Jan 2026 | ⭐⭐⭐⭐⭐ |
| [🌐2] | smartscope.blog | "Claude Code AskUserQuestion Tool Guide" | - | ⭐⭐⭐⭐ |
| [🌐3] | egghead.io | "Create Interactive AI Tools with AskUserQuestion" | - | ⭐⭐⭐⭐ |
| [🌐4] | geeky-gadgets.com | "Claude's Best Hidden Features" | Jan 2026 | ⭐⭐⭐ |
| [🌐5] | GitHub Gist | "Internal claude code tools implementation" | Oct 2025 | ⭐⭐⭐⭐⭐ |
| [🌐6] | platform.claude.com | "Handle approvals and user input" | - | ⭐⭐⭐⭐⭐ |
| [🌐7] | GitHub Issues | "#10346 - Missing Documentation" | Oct 2025 | ⭐⭐⭐⭐ |
| [🌐8] | GitHub Issues | "#12852 - All above bug" | Dec 2025 | ⭐⭐⭐ |

---

## 📚 Corps de l'étude

### 1. Qu'est-ce que AskUserQuestion ?

#### 1.1 Le problème résolu

La plus grande faiblesse des assistants de code AI est leur tendance à **faire des suppositions sur les prompts ambigus** [🌐2]. Le cycle classique :

```
Instruction vague → AI suppose → Code incorrect → Correction → AI suppose encore → Boucle infinie
```

AskUserQuestion **casse ce cycle** en permettant à Claude de poser des questions de clarification structurées avant d'écrire une seule ligne de code.

#### 1.2 L'inversion du paradigme

> "Pendant des années, nous nous sommes obsédés sur le prompt engineering — créer les instructions parfaites pour que l'AI fasse ce qu'on veut. AskUserQuestion inverse silencieusement cette relation. Maintenant, c'est le modèle qui vous prompte." [🌐1]

Quand Claude demande "Cette API doit-elle échouer immédiatement ou réessayer avec backoff ?" avant d'écrire du code, les **tradeoffs deviennent explicites**. Au lieu de découvrir des suppositions enfouies lors de la code review, vous confrontez les décisions de design en amont — quand elles sont peu coûteuses à changer.

#### 1.3 Date d'introduction

- **Version** : Claude Code v2.0.21 [🌐2][🌐7]
- **Changelog** : "Added an interactive question tool"
- **Documentation officielle** : Toujours manquante (issue #10346) [🌐7]

---

### 2. Fonctionnement Technique

#### 2.1 Structure des questions

Le schéma JSON de l'outil [🌐5] :

```typescript
interface AskUserQuestionTool {
  questions: Question[];  // 1-4 questions (required)
  answers?: Record<string, string>;  // Réponses collectées
}

interface Question {
  question: string;      // Question complète, claire, avec "?"
  header: string;        // Label court (max 12 caractères)
  multiSelect: boolean;  // Permettre sélections multiples
  options: Option[];     // 2-4 options
}

interface Option {
  label: string;         // Texte affiché (1-5 mots, concis)
  description: string;   // Explication du choix
}
```

#### 2.2 Caractéristiques clés

| Aspect | Valeur |
|--------|--------|
| Nombre de questions | 1 à 4 par invocation |
| Options par question | 2 à 4 |
| Longueur header | Max 12 caractères |
| Sélection multiple | Via `multiSelect: true` |
| Option "Autre" | Toujours disponible automatiquement |
| Timeout | 60 secondes |

#### 2.3 Exemple d'interface CLI

```
╭─────────────────────────────────────────────────────────╮
│  🔧 Auth method                                         │
│                                                         │
│  Which authentication method should we use?             │
│                                                         │
│  ○ OAuth 2.0                                           │
│    Industry standard, supports third-party login        │
│                                                         │
│  ● JWT (Recommended)                                    │
│    Simple, stateless, good for APIs                     │
│                                                         │
│  ○ Session-based                                        │
│    Traditional, requires server-side storage            │
│                                                         │
│  ○ Other...                                             │
│    Custom text input                                    │
╰─────────────────────────────────────────────────────────╯
```

#### 2.4 Options recommandées

Claude analyse le codebase et le contexte pour **auto-générer des options sensées** avec parfois une marque "(Recommended)" [🌐2] :

> "Question de Claude : Comment les erreurs API doivent-elles être gérées ?
> A) Échec immédiat (Simple, facile à débugger)
> B) Avec retry (Auto-retry jusqu'à 3 fois) **(Recommended)**
> C) Handler custom (Implémenter une logique personnalisée)"

---

### 3. Configuration et Activation

#### 3.1 Activation automatique

AskUserQuestion est **activé par défaut** dans Claude Code. Aucune configuration n'est nécessaire pour que Claude l'utilise quand il détecte de l'ambiguïté.

#### 3.2 Encourager son utilisation

Pour inciter Claude à utiliser l'outil plus systématiquement, vous pouvez :

**Via CLAUDE.md** :
```markdown
# Règles de développement

Avant de commencer à coder :
1. Utilise AskUserQuestion pour clarifier toute ambiguïté
2. N'assume jamais les choix d'architecture
3. Demande confirmation sur les patterns (auth, error handling, etc.)
```

**Via prompt direct** :
```
"Interview-moi sur les spécifications avant de coder"
```

**Via Plan Mode** (recommandé par Boris Cherny [🌐1]) :
```
1. Toujours utiliser Plan mode
2. Donner à Claude un moyen de vérifier son output
3. Tenir les mêmes standards pour le code humain et Claude
```

#### 3.3 Forcer l'utilisation (use case avancé)

```bash
claude --system-prompt "Tu es un architecte. N'utilise QUE l'outil AskUserQuestion pour recueillir les requirements." "Aide-moi à définir l'architecture de mon app"
```

---

### 4. Patterns d'Usage Recommandés

#### 4.1 Spec-Based Development

Le pattern le plus puissant, popularisé par @trq212 sur Twitter [🌐1] :

```
┌─────────────────────────────────────────────────────────┐
│  ÉTAPE 1 : Interview                                    │
│  ─────────────────                                      │
│  • Prompt minimal : "Je veux ajouter l'auth"            │
│  • Claude utilise AskUserQuestion                       │
│  • Questions : méthode auth ? gestion tokens ? etc.     │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  ÉTAPE 2 : Spécification                                │
│  ────────────────────                                   │
│  • Claude génère un document de spec détaillé           │
│  • Toutes les décisions sont explicites                 │
│  • Revue et validation humaine                          │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  ÉTAPE 3 : Exécution (nouvelle session)                 │
│  ───────────────────────────────────────                │
│  • Nouvelle session avec la spec comme contexte         │
│  • Claude exécute avec précision                        │
│  • Ambiguïté = 0, rework = minimal                      │
└─────────────────────────────────────────────────────────┘
```

**Résultat** : Code qui correspond à l'intent dès le premier essai [🌐1].

#### 4.2 Combinaison avec Plan Mode

Activer Plan Mode (`Shift+Tab` x2) puis laisser AskUserQuestion clarifier [🌐2] :

```
┌─────────────────────────────────────────────────────────┐
│  1. Entrée Plan Mode (Shift+Tab x2)                     │
│  2. Claude analyse et propose un plan                   │
│  3. AskUserQuestion clarifie les zones grises           │
│  4. Plan affiné avec toutes les décisions               │
│  5. ExitPlanMode → Exécution                            │
└─────────────────────────────────────────────────────────┘
```

> "Vous atteignez un état où '90% est décidé à l'étape de planification', améliorant dramatiquement la productivité en solo. C'est comme avoir un excellent PM/tech lead à côté de vous." [🌐2]

#### 4.3 Choose-Your-Own-Adventure Development

Chaque question est un **fork dans le chemin** [🌐1] :

```
                    ┌─── OAuth → External providers
                    │
    Auth method? ───┼─── JWT → Stateless API
                    │
                    └─── Session → Traditional web

                    ┌─── Fail fast → Simple debugging
                    │
    Error handling? ┼─── Retry → Resilient
                    │
                    └─── Custom → Flexible

    ... et ainsi de suite
```

Au moment où Claude commence à coder, vous avez **navigué l'arbre de décisions ensemble** — et vous avez un enregistrement clair de chaque choix.

#### 4.4 Usage non-code

AskUserQuestion peut être utilisé pour des applications **au-delà du code** [🌐3] :

- Life coach interactif
- Project planner
- Onboarding wizard
- Decision framework

```bash
claude --system-prompt "Tu es un life coach" \
       --model haiku \
       "Aide-moi à déterminer la prochaine étape de ma vie 
        en utilisant uniquement AskUserQuestion"
```

---

### 5. Limitations et Points d'Attention

#### 5.1 Limitations techniques

| Limitation | Impact | Workaround |
|------------|--------|------------|
| **Timeout 60 secondes** | Délibération longue = échec | Choisir option recommandée puis ajuster |
| **Non disponible en sous-agents** | Seul le main thread peut poser des questions | Clarifier avant de lancer les sous-agents |
| **4-6 questions max par session** | Peut être insuffisant pour specs complexes | Diviser en plusieurs sessions |
| **Documentation manquante** | Difficile à découvrir | Utiliser cette étude + GitHub issues |

#### 5.2 Bugs connus

**Bug "All above are correct"** (#12852) [🌐8] :
- Quand on sélectionne "Toutes les réponses ci-dessus", seule la string littérale est passée
- Les options sous-jacentes ne sont pas transmises
- **Status** : Identifié, non résolu

**Bug affichage vide** (#10229, #9912) :
- Parfois les questions ne s'affichent pas
- Claude voit "User answered: ⎿" sans réponse
- **Workaround** : Réessayer ou reformuler le prompt

#### 5.3 Bonnes pratiques

1. **Ne pas forcer l'outil** : Laisser Claude décider quand c'est pertinent
2. **Utiliser les recommandations** : En cas de doute, l'option "(Recommended)" est analysée contextuellement
3. **Combiner avec Plan Mode** : Maximise l'efficacité
4. **Clarifier AVANT les sous-agents** : Ils ne peuvent pas poser de questions

---

### 6. Impact sur la Productivité

#### 6.1 Métriques rapportées

| Métrique | Amélioration | Source |
|----------|--------------|--------|
| Réduction cycles de rework | 50-80% | [🌐2] |
| Décisions clarifiées au planning | ~90% | [🌐2] |
| Code correct au premier essai | Significatif | [🌐1] |

#### 6.2 Bénéfices qualitatifs

- **Tradeoffs explicites** : Les décisions d'architecture sont documentées
- **Historique des choix** : Chaque question/réponse = documentation
- **Collaboration améliorée** : Les non-techniques peuvent participer via QCM
- **Onboarding facilité** : Nouveau sur le projet ? Les questions guident

---

## 💡 Insights et Recommandations

### Insights clés

1. **Inversion du prompt engineering** : AskUserQuestion fait de Claude l'interviewer et de vous l'expert. C'est souvent plus efficace que de perfectionner vos prompts.

2. **Le bottleneck shift** : "Quand les agents AI deviennent plus capables, le goulot d'étranglement passe de 'l'AI peut-elle faire ça ?' à 'l'AI comprend-elle ce que je veux vraiment ?'" [🌐1]

3. **Documentation déficiente mais outil puissant** : L'issue #10346 montre que même Anthropic n'a pas documenté cette fonctionnalité — mais son impact est transformatif pour ceux qui la découvrent.

### Recommandations actionnables

| Priorité | Recommandation | Justification |
|----------|----------------|---------------|
| 🔴 Haute | Adopter le spec-based development | Réduction 50-80% du rework |
| 🔴 Haute | Toujours combiner avec Plan Mode | Synergie maximale |
| 🟡 Moyenne | Ajouter des règles dans CLAUDE.md | Encourage l'utilisation systématique |
| 🟡 Moyenne | Former l'équipe à répondre aux QCM | Même les non-devs peuvent participer |
| 🟢 Basse | Surveiller les bugs (GitHub issues) | Fonctionnalité encore jeune |

---

## ⚠️ Risques et Points d'Attention

- **Timeout strict** : 60 secondes peuvent être courtes pour des décisions complexes
- **Non disponible en background** : Planifier les clarifications avant les sous-agents async
- **Documentation absente** : Se fier aux sources communautaires et GitHub

---

## ❓ Questions Ouvertes

- Quand Anthropic publiera-t-elle la documentation officielle ?
- Le timeout de 60 secondes sera-t-il configurable ?
- Les sous-agents pourront-ils un jour utiliser AskUserQuestion ?

---

## 🔮 Perspectives

### Évolutions prévisibles

- Documentation officielle (issue #10346 toujours ouverte)
- Intégration avec plus d'outils de gestion de projet (Linear, Jira, etc.)
- Possibilité de custom questions via SDK

### Signal fort

Boris Cherny (créateur de Claude Code) recommande explicitement d'utiliser Plan Mode + vérification [🌐1]. AskUserQuestion est au cœur de cette approche.

---

## 📖 Bibliographie

### Sources primaires
| # | Source | Sections |
|---|--------|----------|
| [1] | Transcription YouTube "Claude Code 2.1" | Mention AskUserQuestion |

### Sources web
| # | URL | Titre | Fiabilité |
|---|-----|-------|-----------|
| [🌐1] | atcyrus.com | "AskUserQuestion tool guide" | ⭐⭐⭐⭐⭐ |
| [🌐2] | smartscope.blog | "Reduce Rework 50-80%" | ⭐⭐⭐⭐ |
| [🌐3] | egghead.io | "Create Interactive AI Tools" | ⭐⭐⭐⭐ |
| [🌐4] | geeky-gadgets.com | "Claude's Best Hidden Features" | ⭐⭐⭐ |
| [🌐5] | GitHub Gist bgauryy | "Internal tools implementation" | ⭐⭐⭐⭐⭐ |
| [🌐6] | platform.claude.com | "Handle user input" | ⭐⭐⭐⭐⭐ |
| [🌐7] | GitHub #10346 | "Missing Documentation" | ⭐⭐⭐⭐ |
| [🌐8] | GitHub #12852 | "All above bug" | ⭐⭐⭐ |

---

## 📊 Annexe : Cheatsheet AskUserQuestion

### Quand l'utiliser ?

| Situation | Action |
|-----------|--------|
| Choix d'architecture (auth, DB, API) | ✅ Laisser Claude poser les questions |
| Instruction ambiguë ("ajoute cette feature") | ✅ Claude clarifie automatiquement |
| Spec complexe | ✅ Spec-based development |
| Task simple et claire | ❌ Pas nécessaire |
| Sous-agent background | ❌ Non supporté |

### Commandes utiles

```bash
# Encourager l'interview
"Interview-moi sur les requirements avant de coder"

# Forcer l'utilisation
claude --system-prompt "N'utilise QUE AskUserQuestion" "..."

# Activer Plan Mode
Shift+Tab (x2)
```

### Workflow recommandé

```
1. /plan ou Shift+Tab x2 → Entrer Plan Mode
2. Prompt minimal : "Je veux [feature]"
3. Répondre aux questions QCM de Claude
4. Valider la spécification générée
5. Nouvelle session avec spec → Exécution
```

---

## 🏷️ Métadonnées

| Champ | Valeur |
|-------|--------|
| Sujet | AskUserQuestion — Clarification Interactive |
| Date | 2025-01-14 |
| Niveau | 4 (Approfondi) |
| Sources fournies | 1 |
| Sources web retenues | 8 |
| Mots | ~2 400 |
| Confiance globale | ⭐⭐⭐⭐ |

---

*Généré par Resumator v3.0 — 2025-01-14*
*Complément à l'étude principale sur Claude Code 2.1*
