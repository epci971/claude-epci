# Journal d'Exploration — Pipeline Orchestration

> Session: brainstorm-orchestrator-pipeline-20260211-162100
> 4 iterations | EMS: 20 → 76 | 8 decisions

---

## Progression EMS

| Iteration | EMS | Delta | Evenement cle |
|-----------|-----|-------|---------------|
| Init | 20 | - | Session initialisee, 2 docs sources charges |
| It.1 | 42 | +22 | Brief valide, framing, HMW generes |
| It.2 | 57 | +15 | SPEC-03 Notion explore, D1+D2+D3 verrouillees |
| It.3 | 67 | +10 | Interfaces mappees, D4+D5, zones grises fermees |
| It.4 | 76 | +9 | Config multi-projet, securite, D6+D7+D8 |

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

## Sources consultees

- BRIEF-Pipeline-V3.md (540 lignes, architecture complete)
- SPEC-02-orchestrator.md (1032 lignes, spec detaillee orchestrateur)
- src/skills/implement-auto/ (8 steps, 5 references, contrat JSON)
- Session brainstorm implement-auto precedente (EMS 86)
