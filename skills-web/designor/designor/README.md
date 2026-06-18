# Designor — Installation & Quick Start

**Version** : 1.2.0
**Date** : 30 avril 2026
**Author** : Édouard

## What is this?

`designor` is an expert prompt elicitor for **Claude Design** (Anthropic Labs, launched April 17, 2026). It transforms vague design intentions into structured, token-optimized prompts ready to paste into Claude Design, with preparation checklist and token economy tips.

The skill stops at brief production — it does NOT execute the prompt or generate the artifact.

## Installation

Drop the entire `designor/` folder into your skills directory:

```bash
# For personal skills (Claude.ai)
cp -r designor/ /path/to/skills/user/

# Typical paths:
# /mnt/skills/user/designor/    (Anthropic-hosted environment)
# ~/.claude/skills/designor/    (Claude Code local)
```

## Verify installation

Run the triggering tests:

```bash
cd designor/scripts
python test_triggering.py
```

Expected output:
```
🎉 All tests passed!
  positive   ✅ PASS
  negative   ✅ PASS
  ambiguous  ✅ PASS
  templates  ✅ PASS
  modes      ✅ PASS
```

## First test queries

Once deployed, try these in a new Claude conversation:

- **Simple test** : `"designor un dashboard pour mon PMS"`
  → Should detect template `ui` + mode `standard`, launch Phase 0 audit

- **Ambiguous test** : `"designor pour ma landing"`
  → Should ask ONE disambiguation question (ui vs one-pager)

- **Revise test** : `"designor revise"` with a previous prompt + critique
  → Should skip Phase 0, produce directed critique revision prompt

## File structure

```
designor/
├── SKILL.md                              # Main skill file (entry point)
├── README.md                             # This file
├── references/
│   ├── phase-0-audit.md                  # Pre-elicitation audit details
│   ├── templates-by-deliverable.md       # 6 XML templates + quick brief
│   ├── style-anchors.md                  # 5-dimension library (versioned)
│   ├── revise-pattern.md                 # Directed critique iteration
│   └── token-economy.md                  # Tokens optimization patterns
└── scripts/
    └── test_triggering.py                # Automated triggering tests
```

## Architecture overview

- **3 modes** : `quick` (3-5 questions) / `standard` (8-12) / `deep` (15-20 + variants)
- **6 deliverable templates** : `ui` / `wireframe-handoff` / `deck` / `one-pager` / `social` / `explore`
- **Phase 0 audit** : 3 blocking questions (deliverable type / visual inspiration / design system)
- **Output structure** : always 3 sections (prompt + preparation checklist + token economy tips)
- **Sub-command** : `designor revise` for directed critique iteration

## Integrations

- ← `brainstormer` — upstream if product intent unclear
- → `critiquor` — downstream for prompt review
- → `perplexitor` — for freshness check on style anchors (deep mode)
- → Notion — optional brief export

## Version history

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-30 | Initial release — 3 modes × 6 templates, Phase 0 audit, modular anchors library, revise sub-command |
| 1.1.0 | 2026-04-30 | Critiquor pass — Tool Notes (agnostification), obsolescence disclaimer, pivot mid-elicitation procedure |
| 1.2.0 | 2026-04-30 | Style anchors validation pass (5 Perplexity searches) — Aquacro renamed → Liquid Glass, Editorial promoted to stable, Retro-futuriste split into 3 anchors, Soft pastel renamed → Tactile maximalism, Néo-brutaliste enriched |

## License

Personal use. Author: Édouard.

## Support

For issues or improvements, iterate via `critiquor` sub-skill or pass through `skill-factory` for major refactor.
