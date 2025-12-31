# Intégrer Code-Promptor dans EPCI Claude Code avec MCP Notion

📦 **Major** | ⏱️ 8h | 🎯 Confidence: HIGH

## Objectif

Créer une commande `/promptor` dans le plugin EPCI Claude Code qui reproduit la logique métier du skill web code-promptor : transformer des dictées vocales ou textuelles en tâches structurées, puis les exporter directement vers Notion via le MCP officiel. L'outil servira de pense-bête rapide pour capturer des idées à la volée, indépendamment du workflow EPCI principal.

## Description

Le skill web code-promptor v2.1 offre une expérience de capture d'idées fluide : dictée → détection multi-tâches → génération de briefs formatés → export Notion. L'objectif est de porter cette expérience dans Claude Code en tirant parti :
- Du MCP Notion officiel (`@notionhq/notion-mcp-server`) pour l'export direct
- De la configuration locale `.claude/settings.local.json` pour les secrets
- De l'accès au codebase pour un contexte enrichi (optionnel)

## Exploration Summary

### Stack identifiée
- **Plugin EPCI** : Commands (markdown) + Skills (markdown) + Python (hooks/scripts)
- **MCP existants** : Context7, Sequential, Magic, Playwright
- **MCP à ajouter** : Notion (`@notionhq/notion-mcp-server` v2.0.0)

### Patterns architecture
- Commandes dans `src/commands/*.md`
- Skills dans `src/skills/<nom>/SKILL.md` + references/ + templates/
- Configuration locale dans `.claude/settings.local.json` (gitignored)

### Fichiers candidats
| Fichier | Action |
|---------|--------|
| `src/commands/promptor.md` | Créer |
| `src/skills/promptor/SKILL.md` | Créer |
| `src/skills/promptor/references/*.md` | Créer (3 fichiers) |
| `src/skills/promptor/templates/*.md` | Créer (3 fichiers) |
| `.claude/settings.local.json` | Enrichir section `notion` |
| `src/mcp/config.py` | Ajouter serveur `notion` |
| `CLAUDE.md` | Documenter nouvelle commande |

## Technical Validation

### Spike MCP Notion — Verdict: GO ✅

| Aspect | Résultat |
|--------|----------|
| Package officiel | `@notionhq/notion-mcp-server` disponible |
| Installation | `npx -y @notionhq/notion-mcp-server` (sans installation permanente) |
| Authentification | Variable `NOTION_TOKEN` |
| Tool création | `create-a-page` avec propriétés JSON |
| Tool requête | `query-data-source` pour recherche |

### Spike Secrets — Verdict: GO ✅

| Aspect | Résultat |
|--------|----------|
| Fichier existant | `.claude/settings.local.json` |
| Gitignored | Oui (pattern global `~/.config/git/ignore`) |
| Permissions | 600 (owner only) |
| Extension | Ajouter section `notion` dans le JSON existant |

## Exigences fonctionnelles

- [FR1] : La commande `/promptor [texte]` génère un brief et l'exporte vers Notion en mode one-shot
- [FR2] : La commande `/promptor session` démarre un mode session avec projet verrouillé
- [FR3] : L'algorithme de détection multi-tâches (seuil 40 pts) segmente les dictées en tâches indépendantes
- [FR4] : Un checkpoint interactif affiche les tâches détectées avec commandes (ok, merge, edit, drop)
- [FR5] : Trois formats de brief adaptatifs : Quick fix (1h), Standard (4h), Major (8h)
- [FR6] : Les sous-tâches sont auto-générées selon le type et domaine détectés
- [FR7] : L'export Notion crée des pages avec mapping propriétés (Nom, Type, Temps estimé, État, DAY, Projet)
- [FR8] : La configuration Notion est lue depuis `.claude/settings.local.json`
- [FR9] : En cas d'erreur Notion, le brief est affiché en texte avec option retry

## Exigences non-fonctionnelles

- [NFR1] : Le MCP Notion doit être optionnel — la commande fonctionne sans (affichage brief uniquement)
- [NFR2] : Les tokens Notion ne doivent jamais apparaître dans les logs ou outputs
- [NFR3] : La latence de création Notion doit être < 3s par tâche
- [NFR4] : La commande doit supporter la dictée vocale (nettoyage hésitations)

## Contraintes techniques

- Le MCP Notion officiel utilise l'API 2025-09-03 avec `data_source_id` (pas `database_id`)
- Les propriétés Notion doivent matcher le schéma existant de la base Tâches
- Le fichier `.claude/settings.local.json` doit rester compatible avec la structure actuelle

## Plan d'implémentation

### 1. Infrastructure MCP Notion
- [ ] Ajouter configuration serveur `notion` dans `src/mcp/config.py`
- [ ] Créer validation du token Notion au démarrage
- [ ] Implémenter fallback si MCP Notion indisponible
- [ ] Documenter configuration dans `src/skills/mcp/references/notion.md`

### 2. Configuration locale
- [ ] Définir schéma section `notion` dans `.claude/settings.local.json`
- [ ] Créer script de validation config `src/scripts/validate_notion_config.py`
- [ ] Ajouter template `.claude/settings.local.json.example` (sans secrets)
- [ ] Documenter setup dans README ou CLAUDE.md

### 3. Skill Promptor — Core
- [ ] Créer `src/skills/promptor/SKILL.md` avec logique métier principale
- [ ] Porter `references/multi-task-detection.md` depuis code-promptor
- [ ] Porter `references/output-format.md` (3 formats briefs)
- [ ] Porter `references/voice-cleaning.md` (nettoyage dictée)

### 4. Skill Promptor — Templates
- [ ] Créer `templates/brief-quickfix.md` (1h)
- [ ] Créer `templates/brief-standard.md` (4h)
- [ ] Créer `templates/brief-major.md` (8h)
- [ ] Adapter les templates au contexte CLI

### 5. Commande /promptor
- [ ] Créer `src/commands/promptor.md` avec workflow complet
- [ ] Implémenter mode one-shot (`/promptor [texte]`)
- [ ] Implémenter mode session (`/promptor session`)
- [ ] Implémenter checkpoint interactif (tableau + commandes)
- [ ] Implémenter export Notion via MCP

### 6. Finalisation
- [ ] Ajouter validation skill `src/scripts/validate_skill.py src/skills/promptor/`
- [ ] Mettre à jour CLAUDE.md section Commands
- [ ] Tester workflow complet (dictée → Notion)
- [ ] Documenter dans `docs/` si nécessaire

## Notes

- L'outil est standalone, pas d'intégration avec `/brief` ou `/epci`
- Le mapping propriétés Notion est identique à code-promptor web (compatibilité base existante)
- Pas de cache projets nécessaire — un seul projet par configuration locale
- Pas de fonctionnalité `ref [n]` (dépendances) en v1
