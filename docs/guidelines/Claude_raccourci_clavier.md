<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Liste exhaustive des raccourcis clavier et commandes disponibles par défaut dans Claude Code

J'ai effectué une recherche approfondie en analysant plus de 65 sources, incluant la documentation officielle de Claude Code, des guides communautaires et des ressources spécialisées. Voici la référence complète[^1_1][^1_2][^1_3][^1_4][^1_5][^1_6].

## 1. Raccourcis clavier

### Contrôles généraux

| Raccourci | Description | Contexte |
| :-- | :-- | :-- |
| **Ctrl+C** | Annuler l'entrée ou génération actuelle | Interruption standard[^1_1][^1_3] |
| **Ctrl+D** | Quitter la session Claude Code | Signal EOF[^1_1][^1_3] |
| **Ctrl+G** | Ouvrir dans l'éditeur de texte par défaut | Éditer prompt ou réponse[^1_7][^1_3] |
| **Ctrl+L** | Effacer l'écran du terminal | Conserve l'historique[^1_1][^1_3] |
| **Ctrl+O** | Basculer la sortie détaillée | Affiche l'utilisation des outils[^1_1][^1_3] |
| **Ctrl+R** | Recherche inverse dans l'historique | Recherche interactive[^1_1][^1_3] |
| **Ctrl+V** / **Cmd+V** (iTerm2) / **Alt+V** (Windows) | Coller une image depuis le presse-papiers | Colle image ou chemin[^1_1][^1_8][^1_3] |
| **Ctrl+B** | Mettre tâches en arrière-plan | Pour tmux: presser 2×[^1_1][^1_3] |
| **Esc + Esc** | Rembobiner code/conversation | Restaurer état précédent[^1_1][^1_8][^1_9] |
| **Shift+Tab** / **Alt+M** | Basculer modes de permission | Auto-accept/Plan/Normal[^1_8][^1_9][^1_4] |
| **Option+P** (macOS) / **Alt+P** (autres) | Changer de modèle | Sans effacer le prompt[^1_3][^1_4] |
| **Option+T** (macOS) / **Alt+T** (autres) | Basculer extended thinking | Nécessite /terminal-setup[^1_3][^1_4] |
| **↑/↓** | Naviguer dans l'historique | Rappel des entrées précédentes[^1_1][^1_8] |
| **←/→** | Naviguer entre onglets | Dialogues et menus[^1_3] |
| **?** | Afficher raccourcis disponibles | Aide contextuelle[^1_3] |

### Édition de texte

| Raccourci | Description |
| :-- | :-- |
| **Ctrl+K** | Supprimer jusqu'à fin de ligne (stocke texte)[^1_1][^1_3] |
| **Ctrl+U** | Supprimer ligne entière (stocke texte)[^1_1][^1_3] |
| **Ctrl+Y** | Coller texte supprimé[^1_3] |
| **Alt+Y** | Cycler historique de collage[^1_3] |
| **Alt+B** | Reculer d'un mot[^1_3] |
| **Alt+F** | Avancer d'un mot[^1_3] |
| **Ctrl+A** | Début de ligne[^1_1] |
| **Ctrl+E** | Fin de ligne[^1_1] |
| **Ctrl+W** | Supprimer mot[^1_1] |

**Note macOS**: Les raccourcis Option/Alt nécessitent de configurer Option comme Meta dans votre terminal (iTerm2, Terminal.app, VS Code)[^1_3].

### Entrée multiligne

| Méthode | Raccourci | Contexte |
| :-- | :-- | :-- |
| Échappement rapide | `\` + **Enter** | Fonctionne dans tous les terminaux[^1_8][^1_3] |
| macOS défaut | **Option+Enter** | Par défaut sur macOS[^1_8][^1_3] |
| Shift+Enter | **Shift+Enter** | iTerm2, WezTerm, Ghostty, Kitty[^1_8][^1_3] |
| Séquence contrôle | **Ctrl+J** | Caractère line feed[^1_3] |
| Mode collage | Coller directement | Pour blocs de code, logs[^1_8][^1_3] |

### Commandes rapides

| Raccourci | Description |
| :-- | :-- |
| **/** au début | Commande ou skill[^1_3][^1_5] |
| **!** au début | Mode Bash (exécution directe)[^1_3] |
| **@** | Mention de fichier (autocomplétion)[^1_3] |


***

## 2. Mode Vim

Activer avec `/vim` ou configurer en permanence via `/config`[^1_3][^1_10][^1_11][^1_6].

### Changement de mode

| Commande | Action | Depuis mode |
| :-- | :-- | :-- |
| **Esc** | Mode NORMAL | INSERT[^1_3][^1_6] |
| **i** | Insérer avant curseur | NORMAL[^1_3][^1_6] |
| **I** | Insérer début de ligne | NORMAL[^1_3][^1_6] |
| **a** | Insérer après curseur | NORMAL[^1_3][^1_6] |
| **A** | Insérer fin de ligne | NORMAL[^1_3][^1_6] |
| **o** | Ouvrir ligne en dessous | NORMAL[^1_3][^1_6] |
| **O** | Ouvrir ligne au-dessus | NORMAL[^1_3][^1_6] |

### Navigation (mode NORMAL)

| Commande | Action |
| :-- | :-- |
| **h/j/k/l** | Gauche/Bas/Haut/Droite[^1_3][^1_6] |
| **w** | Mot suivant[^1_3][^1_6] |
| **e** | Fin du mot[^1_3][^1_6] |
| **b** | Mot précédent[^1_3][^1_6] |
| **0** | Début de ligne[^1_3][^1_6] |
| **\$** | Fin de ligne[^1_3][^1_6] |
| **^** | Premier caractère non-blanc[^1_3][^1_6] |
| **gg** | Début de l'entrée[^1_3][^1_6] |
| **G** | Fin de l'entrée[^1_3][^1_6] |
| **f{char}** | Sauter au caractère suivant[^1_3][^1_6] |
| **F{char}** | Sauter au caractère précédent[^1_3][^1_6] |

### Édition (mode NORMAL)

| Commande | Action |
| :-- | :-- |
| **x** | Supprimer caractère[^1_3][^1_6] |
| **dd** | Supprimer ligne[^1_3][^1_6] |
| **D** | Supprimer jusqu'à fin de ligne[^1_3][^1_6] |
| **dw/de/db** | Supprimer mot/jusqu'à fin/arrière[^1_3][^1_6] |
| **cc** | Changer ligne[^1_3][^1_6] |
| **C** | Changer jusqu'à fin de ligne[^1_3][^1_6] |
| **yy/Y** | Copier ligne[^1_3][^1_6] |
| **p** | Coller après curseur[^1_3][^1_6] |
| **P** | Coller avant curseur[^1_3][^1_6] |
| **>>** | Indenter ligne[^1_3][^1_6] |
| **<<** | Désindenter ligne[^1_3][^1_6] |
| **.** | Répéter dernière modification[^1_3][^1_6] |


***

## 3. Commandes slash intégrées

### Liste complète (40+ commandes)

| Commande | Objectif |
| :-- | :-- |
| **/add-dir** | Ajouter répertoires de travail supplémentaires[^1_12][^1_5][^1_13] |
| **/agents** | Gérer sous-agents IA personnalisés[^1_12][^1_5][^1_14] |
| **/bashes** | Lister et gérer tâches en arrière-plan[^1_12][^1_5] |
| **/bug** | Signaler bogues (envoie conversation à Anthropic)[^1_12][^1_15][^1_5] |
| **/clear** | Effacer historique conversation[^1_12][^1_3][^1_5] |
| **/compact [instructions]** | Compacter conversation avec focus optionnel[^1_12][^1_3][^1_5] |
| **/config** | Ouvrir interface Paramètres (onglet Config)[^1_12][^1_3][^1_5] |
| **/context** | Visualiser utilisation contexte (grille colorée)[^1_12][^1_3][^1_5] |
| **/cost** | Afficher statistiques utilisation jetons[^1_12][^1_3][^1_5] |
| **/doctor** | Vérifier santé installation Claude Code[^1_12][^1_15][^1_5] |
| **/exit** | Quitter REPL[^1_12][^1_3][^1_5] |
| **/export [filename]** | Exporter conversation vers fichier/presse-papiers[^1_12][^1_5] |
| **/help** | Obtenir aide utilisation[^1_12][^1_3][^1_15][^1_5] |
| **/hooks** | Gérer configurations hooks[^1_12][^1_5][^1_16] |
| **/ide** | Gérer intégrations IDE et statut[^1_12][^1_5] |
| **/init** | Initialiser projet avec guide CLAUDE.md[^1_12][^1_3][^1_15][^1_5] |
| **/install-github-app** | Configurer Claude GitHub Actions[^1_12][^1_5] |
| **/keybindings** | Créer/ouvrir fichier configuration raccourcis[^1_4] |
| **/login** | Changer compte Anthropic[^1_12][^1_15][^1_5] |
| **/logout** | Se déconnecter compte Anthropic[^1_12][^1_15][^1_5] |
| **/mcp** | Gérer connexions serveurs MCP et OAuth[^1_12][^1_17][^1_5][^1_18] |
| **/memory** | Modifier fichiers mémoire CLAUDE.md[^1_12][^1_15][^1_5] |
| **/model** | Sélectionner/modifier modèle IA[^1_12][^1_15][^1_5] |
| **/output-style [style]** | Définir style sortie[^1_12][^1_5] |
| **/permissions** | Afficher/mettre à jour permissions[^1_12][^1_3][^1_5][^1_19][^1_20] |
| **/plan** | Entrer mode plan directement[^1_12][^1_3][^1_5] |
| **/plugin** | Gérer plugins Claude Code[^1_12][^1_5] |
| **/pr-comments** | Afficher commentaires pull request[^1_12][^1_15][^1_5] |
| **/privacy-settings** | Afficher/mettre à jour paramètres confidentialité[^1_12][^1_5] |
| **/release-notes** | Afficher notes version[^1_12][^1_5] |
| **/rename <name>** | Renommer session actuelle[^1_12][^1_5] |
| **/remote-env** | Configurer environnement session distante[^1_12][^1_5] |
| **/resume [session]** | Reprendre conversation par ID/nom[^1_12][^1_3][^1_5] |
| **/review** | Demander révision code[^1_12][^1_15][^1_5] |
| **/rewind** | Rembobiner conversation et/ou code[^1_12][^1_3][^1_5] |
| **/sandbox** | Activer bash sandbox avec isolation[^1_12][^1_5] |
| **/security-review** | Révision sécurité modifications branche[^1_12][^1_5] |
| **/stats** | Visualiser utilisation quotidienne, historique[^1_12][^1_5] |
| **/status** | Ouvrir Paramètres (onglet Statut)[^1_12][^1_3][^1_15][^1_5] |
| **/statusline** | Configurer interface ligne d'état[^1_12][^1_5] |
| **/tasks** | Lister et gérer tâches arrière-plan[^1_3] |
| **/teleport** | Reprendre session distante claude.ai[^1_12][^1_5] |
| **/terminal-setup** | Installer liaison Shift+Entrée[^1_21][^1_12][^1_15][^1_5] |
| **/theme** | Modifier thème couleur[^1_12][^1_3][^1_5] |
| **/todos** | Lister éléments TODO[^1_12][^1_3][^1_5] |
| **/usage** | Afficher limites plan et taux[^1_12][^1_5] |
| **/vim** | Entrer mode vim[^1_12][^1_3][^1_15][^1_5] |

### Commandes slash personnalisées

**Emplacements**[^1_17][^1_5][^1_22]:

- **Projet**: `.claude/commands/` (partagées avec équipe)
- **Personnel**: `~/.claude/commands/` (disponibles partout)

**Syntaxe**: `/<command-name> [arguments]`[^1_17][^1_5][^1_23]

**Exemple création**[^1_2][^1_17][^1_5]:

```bash
# Commande projet
mkdir -p .claude/commands
echo "Analyze this code for performance issues:" > .claude/commands/optimize.md

# Commande personnelle
mkdir -p ~/.claude/commands
echo "Review this code for security:" > ~/.claude/commands/security.md
```

**Arguments disponibles**[^1_17][^1_5]:

- `$ARGUMENTS`: capture tous les arguments
- `$1`, `$2`, etc.: arguments individuels (style shell)
- `${CLAUDE_SESSION_ID}`: ID de session actuelle

**Frontmatter YAML optionnel**[^1_17][^1_5]:

```yaml
---
allowed-tools: Bash(git:*), Read, Edit
argument-hint: [issue-number]
description: Fix GitHub issue
model: claude-3-5-haiku-20241022
disable-model-invocation: true
---
```


### Commandes MCP

Format: `/mcp__<server-name>__<prompt-name> [arguments]`[^1_17][^1_5][^1_24]

Exemples:

```bash
/mcp__github__list_prs
/mcp__github__pr_review 456
/mcp__jira__create_issue "Bug title" high
```

Gestion: utiliser `/mcp` pour voir serveurs, statut, authentification OAuth[^1_17][^1_5][^1_18][^1_24].

***

## 4. Flags CLI (ligne de commande)

### Flags de base

| Flag | Description | Exemple |
| :-- | :-- | :-- |
| **-p, --print** | Mode impression sans interaction | `claude -p "query"`[^1_2][^1_12][^1_13] |
| **-c, --continue** | Continuer dernière conversation | `claude -c`[^1_2][^1_12][^1_13] |
| **-r, --resume** | Reprendre session spécifique | `claude -r "abc123" "query"`[^1_2][^1_12][^1_13] |
| **-v, --version** | Afficher version | `claude -v`[^1_13] |

### Modèle et prompt système

| Flag | Description | Exemple |
| :-- | :-- | :-- |
| **--model** | Définir modèle session | `claude --model sonnet`[^1_2][^1_12][^1_13] |
| **--system-prompt** | Remplacer prompt système complet | `claude --system-prompt "You are..."`[^1_12][^1_13] |
| **--system-prompt-file** | Charger depuis fichier | `claude -p --system-prompt-file ./prompt.txt`[^1_12][^1_13] |
| **--append-system-prompt** | Ajouter au prompt standard | `claude --append-system-prompt "Use TypeScript"`[^1_12][^1_13] |
| **--append-system-prompt-file** | Ajouter depuis fichier | `claude --append-system-prompt-file custom.txt`[^1_12] |

### Permissions et sécurité

| Flag | Description | Exemple |
| :-- | :-- | :-- |
| **--allowedTools** | Autoriser outils sans demande | `claude --allowedTools "Bash(git:*)" "Read"`[^1_2][^1_12][^1_19][^1_13] |
| **--disallowedTools** | Interdire outils | `claude --disallowedTools "Bash(curl:*)"`[^1_2][^1_12][^1_13] |
| **--dangerously-skip-permissions** | Sauter toutes permissions ⚠️ | `claude --dangerously-skip-permissions`[^1_2][^1_12][^1_13][^1_25] |
| **--permission-mode** | Mode permission initial | `claude --permission-mode plan`[^1_13] |

### Répertoires et contexte

| Flag | Description | Exemple |
| :-- | :-- | :-- |
| **--add-dir** | Ajouter répertoires supplémentaires | `claude --add-dir ../frontend ../backend`[^1_2][^1_12][^1_13] |
| **--max-turns** | Limiter tours agentiques | `claude -p --max-turns 3 "query"`[^1_2][^1_12][^1_13] |

### Debug et autres

| Flag | Description | Exemple |
| :-- | :-- | :-- |
| **--debug** | Mode debug avec catégorie | `claude --debug "api,mcp"`[^1_13][^1_25] |
| **--verbose** | Logging verbeux | `claude --verbose`[^1_13][^1_25] |
| **--ide** | Connexion IDE au démarrage | `claude --ide`[^1_13] |
| **--fallback-model** | Modèle fallback sur surcharge | `claude -p --fallback-model sonnet "q"`[^1_13] |
| **--mcp-debug** | Debug MCP spécifiquement | `claude --mcp-debug`[^1_25] |
| **--config-dir** | Répertoire config personnalisé | `claude --config-dir ~/.my-config`[^1_25] |


***

## 5. Outils et permissions

### Outils disponibles

Claude Code a accès aux outils suivants (selon permissions)[^1_19][^1_20][^1_26]:

**Fichiers**:

- `Read`: lire fichiers
- `Write`: écrire nouveaux fichiers
- `Edit`: éditer fichiers existants
- `MultiEdit`: éditions multiples simultanées
- `DeleteFile`: supprimer fichiers
- `Glob`: recherche par pattern de fichiers
- `Grep`: recherche dans contenu fichiers
- `LS`: lister fichiers et répertoires

**Système**:

- `Bash`: exécuter commandes shell
- `Task`: déléguer aux sous-agents
- `TaskOutput`: récupérer sortie tâches background

**Web**:

- `WebFetch`: récupérer contenu web
- `WebSearch`: recherche web

**Autres**:

- `Skill`: invoquer skills/commandes slash
- `TodoRead`/`TodoWrite`: gérer TODOs
- `NotebookRead`/`NotebookEdit`: notebooks Jupyter
- `AskUserQuestion`: poser questions clarification


### Syntaxe règles de permission

**Correspondance exacte**[^1_19][^1_27][^1_20]:

```
Read(./src/main.js)
Bash(git status)
Skill(/commit)
```

**Wildcards**[^1_19][^1_27][^1_20]:

```
Read(./src/*)          # Tous fichiers src/
Bash(git:*)            # Toutes commandes git
Skill(/review-pr:*)    # review-pr avec arguments
mcp__github__*         # Tous outils GitHub MCP
```

**Configuration dans settings.json**[^1_19][^1_27][^1_28]:

```json
{
  "permissions": {
    "allow": [
      "Read(./src/*)",
      "Edit(./src/*)",
      "Bash(git:*)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Bash(rm:*)"
    ]
  }
}
```


***

## 6. Hooks

### Types de hooks

| Hook | Quand s'exécute |
| :-- | :-- |
| **UserPromptSubmit** | Après soumission prompt[^1_29][^1_16][^1_25] |
| **PreToolUse** | Avant utilisation outil[^1_29][^1_16][^1_30][^1_31][^1_25] |
| **PostToolUse** | Après utilisation outil[^1_29][^1_16][^1_30][^1_31][^1_25] |
| **Notification** | Sur notifications[^1_25] |
| **Stop** | Avant arrêt Claude[^1_16][^1_25] |
| **Setup** | Initialisation repository[^1_16] |
| **PreResponse** | Avant réponse Claude[^1_25] |
| **PostResponse** | Après réponse Claude[^1_25] |

### Configuration exemple

**Emplacement**: `.claude/settings.json`[^1_29][^1_16][^1_30][^1_31]

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": {
          "tool_name": "Write|Edit",
          "file_paths": ["*.py", "api/**/*.py"]
        },
        "hooks": [
          {
            "type": "command",
            "command": "ruff check --fix $CLAUDE_FILE_PATHS && black $CLAUDE_FILE_PATHS",
            "timeout": 30,
            "run_in_background": false
          }
        ]
      }
    ]
  }
}
```


### Variables d'environnement hooks

- `$CLAUDE_FILE_PATHS`: chemins fichiers modifiés[^1_29][^1_16]
- `$CLAUDE_PROJECT_DIR`: répertoire projet[^1_16][^1_28]
- `$CLAUDE_SESSION_ID`: ID session actuelle[^1_17][^1_16]
- `$CLAUDE_PLUGIN_ROOT`: racine plugin (pour plugins)[^1_16]

***

## 7. Sous-agents

### Sous-agents intégrés

| Nom | Description | Outils |
| :-- | :-- | :-- |
| **Explore** | Exploration codebase | Read, Grep, Glob (lecture seule)[^1_32][^1_14] |
| **Plan** | Planification sans exécution | Aucun outil d'édition[^1_27][^1_14] |
| **general-purpose** | Usage général | Tous outils standard[^1_32][^1_14] |

### Gestion avec /agents

- Créer nouveau sous-agent (projet ou utilisateur)[^1_14][^1_33]
- Éditer configuration et accès outils[^1_14][^1_33]
- Supprimer sous-agents personnalisés[^1_14]
- Voir sous-agents disponibles[^1_14][^1_33]


### Emplacements

- **Utilisateur**: `~/.claude/agents/`[^1_14][^1_28]
- **Projet**: `.claude/agents/`[^1_14][^1_28]


### Format fichier sous-agent

```yaml
---
name: code-reviewer
description: Reviews code for bugs and improvements
model: claude-sonnet-4-20250514
tools: [Read, Grep, Glob]
skills: [code-quality, security-checks]
---

You are a code reviewer. Analyze code for:
- Security vulnerabilities
- Performance issues
- Best practices
```


### Invocation

**Automatique**: Claude délègue selon description et contexte[^1_32][^1_14]

**Explicite**[^1_14][^1_33]:

```
Use the code-reviewer subagent to check this file
Have the test-runner subagent fix failing tests
```

**Foreground vs Background**[^1_14][^1_33]:

- **Foreground**: bloque conversation, permissions interactives
- **Background**: concurrent, permissions héritées, `Ctrl+B` pour basculer

***

## 8. Serveurs MCP

### Commandes MCP

```bash
# Ajouter serveur
claude mcp add <server-name> <command-to-run>

# Lister serveurs
claude
> /mcp

# Vérifier statut
> /mcp status
```


### Scopes MCP

Trois scopes pour installation[^1_34][^1_18][^1_35]:

- **User-level**: `~/.claude.json`
- **Project-level**: `.mcp.json`
- **Per-project**: dans config


### Serveurs populaires

- **Context7**: documentation à jour[^1_34][^1_24][^1_36]
- **GitHub**: intégration GitHub[^1_24][^1_36]
- **Playwright**: automatisation navigateur[^1_34][^1_37][^1_35]
- **Perplexity**: recherche avec IA[^1_24]
- **Slack**: gestion channels/messages[^1_36]
- **GPT Researcher**: recherche avec citations[^1_36]

***

## 9. Configuration

### Hiérarchie fichiers

| Niveau | Fichier | Description |
| :-- | :-- | :-- |
| Enterprise | `managed-settings.json` | Organisation entière[^1_28] |
| Utilisateur | `~/.claude/settings.json` | Tous projets utilisateur[^1_19][^1_38][^1_28] |
| Projet | `.claude/settings.json` | Projet spécifique (commit git)[^1_19][^1_38][^1_28] |
| Local | `.claude/settings.local.json` | Local (pas commit)[^1_38][^1_28] |

Précédence: Local > Projet > Utilisateur > Enterprise[^1_28]

### Variables d'environnement principales

| Variable | Description |
| :-- | :-- |
| **ANTHROPIC_API_KEY** | Clé API (requis)[^1_39][^1_40][^1_41] |
| **ANTHROPIC_MODEL** | Modèle par défaut[^1_39][^1_42] |
| **CLAUDE_CONFIG_DIR** | Répertoire config custom[^1_25][^1_40][^1_42] |
| **CLAUDE_CODE_DISABLE_BACKGROUND_TASKS** | Désactiver tâches background[^1_28] |
| **SLASH_COMMAND_TOOL_CHAR_BUDGET** | Budget caractères skills (défaut: 15000)[^1_17][^1_5] |
| **MCP_TIMEOUT** | Timeout serveurs MCP[^1_25] |
| **MAX_MCP_OUTPUT_TOKENS** | Limite tokens sortie MCP[^1_25] |
| **CLAUDE_CODE_SHELL_PREFIX** | Préfixe commandes shell[^1_25] |
| **LOG_LEVEL** | Niveau logging[^1_39][^1_40] |

### Mémoire (CLAUDE.md)

**Emplacements**[^1_28]:

- **Global**: `~/.claude/CLAUDE.md`
- **Projet**: `CLAUDE.md` ou `.claude/CLAUDE.md`
- **Local**: `CLAUDE.local.md`

Contient contexte persistant, conventions projet, instructions pour Claude[^1_15][^1_14][^1_28].

***

## 10. Personnalisation raccourcis (Keybindings)

### Fichier keybindings.json

Créer avec: `/keybindings`[^1_4]

Emplacement: `~/.claude/keybindings.json`[^1_4]

### Structure

```json
{
  "$schema": "https://code.claude.com/docs/schemas/keybindings.json",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+u": null
      }
    }
  ]
}
```


### Contextes disponibles

- `Global`: partout dans l'app[^1_4]
- `Chat`: zone saisie chat principale[^1_4]
- `Autocomplete`: menu autocomplétion[^1_4]
- `Confirmation`: dialogues permission[^1_4]
- `HistorySearch`: recherche historique (Ctrl+R)[^1_4]
- `Task`: tâche arrière-plan active[^1_4]
- `ThemePicker`: sélecteur thème[^1_4]
- `MessageSelector`: sélection message rewind[^1_4]
- Et 8 autres contextes[^1_4]


### Syntaxe touches

**Modificateurs**: `ctrl`, `alt`/`opt`, `shift`, `meta`/`cmd`[^1_4]

**Exemples**:

```
ctrl+k
shift+tab
meta+p
ctrl+shift+c
ctrl+k ctrl+s  # Chord (séquence)
```

**Désactiver raccourci**: mettre à `null`[^1_4]

```json
"ctrl+s": null
```

**Raccourcis réservés** (ne peuvent être redéfinis)[^1_4]:

- `Ctrl+C`: interruption
- `Ctrl+D`: sortie

***

## 11. Tips essentiels

### Recherche historique (Ctrl+R)

1. Appuyer `Ctrl+R` pour activer[^1_1][^1_3]
2. Taper terme recherche (surligné dans résultats)
3. `Ctrl+R` à nouveau pour résultats plus anciens
4. Accepter: `Tab`/`Esc` (éditer) ou `Enter` (exécuter)
5. Annuler: `Ctrl+C` ou `Backspace` sur recherche vide

### Mode Bash (!)

Exécuter commandes directement sans passer par Claude[^1_3]:

```bash
! npm test
! git status
! ls -la
```

Ajoute commande et sortie au contexte. Supporte `Ctrl+B` pour background[^1_3].

### Checkpointing et rewind

- `Esc + Esc`: ouvrir menu rewind[^1_1][^1_8][^1_9]
- Restaurer code et/ou conversation à point précédent
- `/rewind`: même fonction[^1_12][^1_5]


### Visualiser contexte

```bash
> /context
```

Affiche grille colorée utilisation contexte, warnings si dépassement[^1_12][^1_3][^1_5][^1_33].

### Compacter conversation

```bash
> /compact [instructions focus optionnelles]
```

Résume historique pour libérer tokens[^1_12][^1_3][^1_5][^1_43].

### Stats et coûts

```bash
> /cost      # Stats jetons
> /stats     # Utilisation quotidienne, historique
> /usage     # Limites plan (abonnés)
```


***

## 12. Dépannage

### /doctor

```bash
> /doctor
```

Vérifie santé installation, configuration, connexions[^1_12][^1_15][^1_5][^1_43].

### Logs verbeux

```bash
claude --verbose
# ou pendant session
> Ctrl+O  # Toggle verbose output
```


### Debug MCP

```bash
claude --mcp-debug
# ou
claude --debug "mcp"
```


***

## Ressources

### Documentation officielle

- https://code.claude.com/docs[^1_1][^1_12][^1_3][^1_17][^1_4]
- https://docs.anthropic.com/claude-code


### Communauté

- Reddit: r/ClaudeAI, r/ClaudeCode[^1_7][^1_44][^1_36][^1_38][^1_45]
- GitHub: awesome-claude-code[^1_36][^1_45][^1_46]


### Outils tiers populaires

- **ccusage**: analyse utilisation[^1_36][^1_40][^1_45]
- **claude-powerline**: statusline personnalisée[^1_36][^1_45]
- **SuperClaude**: framework configuration[^1_36][^1_45][^1_46]
- **Claude Squad**: orchestrateur multi-instances[^1_36][^1_45][^1_46]
- **claudekit**: toolkit CLI avec checkpointing[^1_36][^1_46]

***

Cette référence exhaustive couvre tous les raccourcis clavier et commandes disponibles par défaut dans Claude Code au 21 janvier 2026. J'ai également créé un fichier de référence complet téléchargeable avec tous ces détails organisés de manière structurée.
<span style="display:none">[^1_47][^1_48][^1_49][^1_50][^1_51][^1_52][^1_53][^1_54][^1_55][^1_56][^1_57][^1_58][^1_59][^1_60][^1_61][^1_62][^1_63][^1_64][^1_65][^1_66][^1_67][^1_68][^1_69]</span>

<div align="center">⁂</div>

[^1_1]: https://nikiforovall.blog/claude-code-rules/tips-and-tricks/keyboard-shortcuts/

[^1_2]: https://shipyard.build/blog/claude-code-cheat-sheet/

[^1_3]: https://code.claude.com/docs/en/interactive-mode

[^1_4]: https://code.claude.com/docs/en/keybindings

[^1_5]: https://code.claude.com/docs/fr/slash-commands

[^1_6]: https://code.claude.com/docs/fr/interactive-mode

[^1_7]: https://www.reddit.com/r/ClaudeAI/comments/1okloon/pro_tip_use_ctrlg_to_edit_longer_claude_code/

[^1_8]: https://capacity.so/en/blog/how-to-use-claude-code-tips-and-shortcuts

[^1_9]: https://awesomeclaude.ai/code-cheatsheet

[^1_10]: https://dev.to/rajeshroyal/vim-mode-edit-prompts-at-the-speed-of-thought-3l6c

[^1_11]: https://aiagent.marktechpost.com/post/8-practical-claude-code-features-to-help-developers-build-faster-and-smarter

[^1_12]: https://code.claude.com/docs/en/cli-reference

[^1_13]: https://www.gradually.ai/en/claude-code-commands/

[^1_14]: https://code.claude.com/docs/en/sub-agents

[^1_15]: https://www.youtube.com/watch?v=Cxd4b5JYqKE

[^1_16]: https://code.claude.com/docs/en/hooks

[^1_17]: https://code.claude.com/docs/en/slash-commands

[^1_18]: https://www.reddit.com/r/mcp/comments/1kzsc2x/claude_code_and_mcp/

[^1_19]: https://www.instructa.ai/blog/claude-code/how-to-use-allowed-tools-in-claude-code

[^1_20]: https://www.anthropic.com/engineering/claude-code-best-practices

[^1_21]: https://www.sketchdev.io/hubfs/AI Code Shortcuts.pdf

[^1_22]: https://cloudartisan.com/posts/2025-04-14-claude-code-tips-slash-commands/

[^1_23]: https://anthropic.mintlify.app/en/docs/claude-code/slash-commands

[^1_24]: https://mcpcat.io/guides/adding-an-mcp-server-to-claude-code/

[^1_25]: https://dev.to/holasoymalva/the-ultimate-claude-code-guide-every-hidden-trick-hack-and-power-feature-you-need-to-know-2l45

[^1_26]: https://gist.github.com/wong2/e0f34aac66caf890a332f7b6f9e2ba8f

[^1_27]: https://platform.claude.com/docs/en/agent-sdk/permissions

[^1_28]: https://code.claude.com/docs/en/settings

[^1_29]: https://apidog.com/blog/claude-code-hooks/

[^1_30]: https://www.eesel.ai/blog/hooks-in-claude-code

[^1_31]: https://apidog.com/fr/blog/claude-code-hooks-fr/

[^1_32]: https://platform.claude.com/docs/en/agent-sdk/subagents

[^1_33]: https://www.youtube.com/watch?v=dk0kn2evY38

[^1_34]: https://code.claude.com/docs/en/mcp

[^1_35]: https://www.youtube.com/watch?v=X7lgIa6guKg

[^1_36]: https://www.reddit.com/r/ClaudeCoder/comments/1og9vkg/catalogue_of_claude_code_tools_heres_everything_i/

[^1_37]: https://www.youtube.com/watch?v=52KBhQqqHuc

[^1_38]: https://www.reddit.com/r/ClaudeAI/comments/1l24a93/claude_code_settingsjson/?tl=pt-br

[^1_39]: https://www.claudeinsider.com/docs/configuration/environment

[^1_40]: https://ccusage.com/guide/environment-variables

[^1_41]: https://github.com/jezweb/how-to-claude-code/blob/main/06-configuration/environment-variables.md

[^1_42]: https://www.reddit.com/r/ClaudeAI/comments/1lp8g4w/how_to_find_claude_code_environment_variables_and/

[^1_43]: https://skywork.ai/blog/claude-code-sdk-command-list-latest-reference/

[^1_44]: https://www.reddit.com/r/ClaudeAI/comments/1mdsdm6/vimrc_for_claude_code_vim_mode/

[^1_45]: https://www.reddit.com/r/ClaudeAI/comments/1ofltdr/i_spent_way_too_long_cataloguing_claude_code/

[^1_46]: https://github.com/hesreallyhim/awesome-claude-code

[^1_47]: https://www.youtube.com/watch?v=XiDD1lrWYBM

[^1_48]: https://www.builder.io/blog/claude-code

[^1_49]: https://claude.ai/public/artifacts/e2725e41-cca5-48e5-9c15-6eab92012e75

[^1_50]: https://code.claude.com/docs/en/jetbrains

[^1_51]: https://www.youtube.com/watch?v=DfWHX7kszQI

[^1_52]: https://www.youtube.com/watch?v=SSVp0uszFcM

[^1_53]: https://github.com/wshobson/commands

[^1_54]: https://blog.korny.info/2025/10/10/better-claude-code-permissions

[^1_55]: https://www.youtube.com/watch?v=52KBhQqqHuc\&vl=fr

[^1_56]: https://sfeir.com/pages/livre-blanc-claude-code-securite-permissions-controles.html

[^1_57]: https://www.youtube.com/watch?v=fkQrySWqUa0

[^1_58]: https://jimmysong.io/ai/claude-code-tools/

[^1_59]: https://www.reddit.com/r/ClaudeAI/comments/1lf5gwp/sub_agent_multiagent_claude_code_commands_for/

[^1_60]: https://www.anthropic.com/engineering/advanced-tool-use

[^1_61]: https://devoriales.com/post/400/claude-code-cheat-sheet-the-reference-guide

[^1_62]: https://github.com/davepoon/claude-code-subagents-collection

[^1_63]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview

[^1_64]: https://www.eesel.ai/blog/claude-code-cli-reference

[^1_65]: https://www.implicator.ai/five-claude-code-tools-that-radically-expand-what-engineers-can-do/

[^1_66]: https://www.eesel.ai/blog/settings-json-claude-code

[^1_67]: https://www.eesel.ai/blog/terminal-configuration-claude-code

[^1_68]: https://claudeai.dev/docs/configuration/

[^1_69]: https://www.reddit.com/r/ClaudeCode/comments/1o2rym1/claude_code_config_settings_confirming_location/

