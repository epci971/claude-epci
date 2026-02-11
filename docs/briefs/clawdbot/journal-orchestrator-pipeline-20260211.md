# Journal d'Exploration — Pipeline Orchestration

> Session: brainstorm-orchestrator-pipeline-20260211-162100
> 5 iterations | EMS: 20 → 76 | 13 decisions

---

## Progression EMS

| Iteration | EMS | Delta | Evenement cle |
|-----------|-----|-------|---------------|
| Init | 20 | - | Session initialisee, 2 docs sources charges |
| It.1 | 42 | +22 | Brief valide, framing, HMW generes |
| It.2 | 57 | +15 | SPEC-03 Notion explore, D1+D2+D3 verrouillees |
| It.3 | 67 | +10 | Interfaces mappees, D4+D5, zones grises fermees |
| It.4 | 76 | +9 | Config multi-projet, securite, D6+D7+D8 |
| It.5 (post) | 76 | - | D1 revisee + D9/D10/D11 ajoutees (post-brainstorm) |

## Decisions chronologiques

| # | Timestamp | Decision | Trigger |
|---|-----------|----------|---------|
| D1 | It.2 | Specs dans Git, chemin dans Notion | Limite 2000 chars rich_text Notion |
| D2 | It.2 | curl/jq pur (pas MCP) | Question sur MCP Notion disponible |
| D3 | It.2 | Telegram basique (notifs + kill) | Question scope notifications |
| D4 | It.3 | Quota V1 = reactif M2+M3 | Challenge : seuils M1 speculatifs |
| D5 | It.3 | Specs dans docs/specs/pipeline/ | Question emplacement fichiers |
| D6 | It.4 | Telegram polling (pas webhook) | Analyse polling vs webhook |
| D7 | It.4 | Export brainstorm = script manuel | Analyse scope pipeline auto |
| D8 | It.4 | Kill switch = getUpdates (pas daemon) | Question architecture kill switch |
| D1r | Post | Specs dans Notion body (defaut), Git optionnel | Challenge : body Notion sans limite, 70+ pages testees |
| D9 | Post | Dependances via relation "Bloque par" | Question : que faire si tache B depend de tache A non mergee ? |
| D10 | Post | Auto-merge GitHub natif (gh pr merge --auto) | Question : comment eviter le merge manuel de chaque PR ? |
| D11 | Post | PRs "safe" auto-approuvees (label + GitHub Action) | Extension D10 : PRs simples n'ont pas besoin de review humaine |
| D12 | Post | /spec sync direct vers Notion via API | Automatiser creation backlog depuis spec, zero etape manuelle |
| D13 | Post | Projet = relation vers table Projets existante | Table Projets deja dans Notion, eviter duplication select |

## Persona switches

| Iteration | Persona | Trigger |
|-----------|---------|---------|
| Init-It.2 | [#] Architecte | Default — structurer les 3 specs |
| It.3 (mid) | [!] Sparring | Challenge seuils quota M1 |
| It.4 | [>] Pragmatique | Convergence, fermer les threads |

## Techniques appliquees

- **Decomposition par composant**: SPEC-02/03/04 explorees separement puis interfaces
- **Challenge assumptions**: Remise en question des seuils quota speculatifs
- **Progressive disclosure**: Questions incrementales plutot que todo list massive
- **Risk-first exploration**: Zones grises identifiees et traitees en priorite

## Points de friction

1. **Limite rich_text Notion** — Decouverte en It.2, resolue par D1 (specs dans Git)
2. **Quota estimation** — Le BRIEF donnait des chiffres speculatifs, resolue par D4 (reactif seulement)
3. **Kill switch architecture** — Daemon vs polling, resolue par D8 (integre au cycle cron)
4. **D1 revisee (Notion body vs Git)** — La limite 2000 chars concerne les proprietes rich_text, pas le body de page. Notion body est sans limite pratique. Resolue par D1r (hybride : Notion defaut, Git optionnel)
5. **Auto-merge et dependances** — Les taches peuvent dependre les unes des autres, le merge manuel bloque la chaine. Resolue par D9+D10+D11 (3 niveaux auto-merge)

## Sources consultees

- BRIEF-Pipeline-V3.md (540 lignes, architecture complete)
- SPEC-02-orchestrator.md (1032 lignes, spec detaillee orchestrateur)
- src/skills/implement-auto/ (8 steps, 5 references, contrat JSON)
- Session brainstorm implement-auto precedente (EMS 86)
