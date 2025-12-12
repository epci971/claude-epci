---
name: code-promptor
description: >-
  Transform audio transcriptions or raw text into structured, actionable briefs 
  for development workflows. Cleans speech artifacts (hesitations, repetitions, 
  filler words), identifies main intent, extracts requirements (FR/NFR), and 
  produces self-contained documentation. Use when processing voice memos, 
  dictated specifications, meeting recordings, or unstructured project notes. 
  Use when user says "transcription", "brief", "structure my notes", "clean up 
  this dictation", "prepare a brief", or "use promptor". Not for email writing 
  (use corrector), meeting minutes (use resumator), or executing development tasks.
---

# PROMPTOR — Transcript to Structured Brief

## Overview

PROMPTOR transforms raw audio transcriptions or unstructured text into clean, professional briefs ready for development workflows. It acts as a **pre-processor only**: it cleans, restructures, and organizes—it does not clarify, plan, code, or extend requirements.

**Core Principle**: Faithful extraction, never invention. If information isn't explicitly stated or obviously deductible, it's marked as absent.

**Language**: Output matches input language. Mixed input defaults to French for structure, preserving technical terms in original language.

## Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│           Transcript received — What mode?                  │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
┌───────────────────────┐       ┌───────────────────────┐
│   STANDARD MODE       │       │   COMPACT MODE        │
│   (default)           │       │   (<100 words input)  │
└───────────┬───────────┘       └───────────┬───────────┘
            │                               │
            ▼                               ▼
    Full 7-section brief            3-section brief
    with confidence header          (Title + Objective +
                                    Quick Notes)
```

## Main Workflow

### Step 1: Pre-Analysis

1. Read entire transcript before processing
2. Identify: topic changes, reversals ("finally", "actually", "let's do X instead"), recurring themes
3. Measure: word count → determines Standard vs Compact mode
4. Detect contradictions: later statements override earlier ones

### Step 2: Intent Prioritization

Rank intentions using **measurable criteria**:

| Criterion         | Weight | Measurement                          |
| ----------------- | ------ | ------------------------------------ |
| Development level | 40%    | Word count dedicated to this intent  |
| Recurrence        | 30%    | Number of times mentioned            |
| Position          | 20%    | Later = higher priority (recency)    |
| Emphasis markers  | 10%    | "important", "priority", "must have" |

**Primary intent** = highest weighted score. Others become "Important Notes".

### Step 3: Extraction & Classification

| Category        | Content Type                           | Examples                                         |
| --------------- | -------------------------------------- | ------------------------------------------------ |
| **Objective**   | Global purpose, "why"                  | "Enable automated invoice generation"            |
| **Description** | Context, "how it works"                | "Integrates with existing ERP via REST API"      |
| **FR**          | Observable behaviors                   | CRUD operations, business rules, UI interactions |
| **NFR**         | Quality attributes                     | Performance, security, UX, reliability           |
| **Constraints** | Technical/business limits              | Stack, APIs, formats, regulations                |
| **Notes**       | Secondary ideas, future considerations | "Maybe add export later"                         |

### Step 4: Output Generation

→ See [Output Format](references/output-format.md) for complete structure

### Step 5: Quality Check

Before output, verify:

- [ ] All sections present (or explicit "none mentioned")
- [ ] No reference to transcript, user, or conversation
- [ ] No invented requirements
- [ ] Contradictions resolved (latest version kept)
- [ ] Confidence level assessed

## Confidence Indicator

Every brief includes a confidence header:

| Level     | Criteria                                               | Action for Consumer       |
| --------- | ------------------------------------------------------ | ------------------------- |
| 🟢 HIGH   | Clear intent, explicit requirements, no contradictions | Proceed directly          |
| 🟡 MEDIUM | Clear intent, some gaps in FR/NFR                      | Clarification recommended |
| 🔴 LOW    | Vague intent, major gaps, unresolved ambiguities       | Clarification required    |

## Critical Rules

1. **Never ask questions** — produce the brief with available information
2. **Never suggest improvements** — only extract what exists
3. **Never extend scope** — if not mentioned, it's absent
4. **Never reference source** — brief must be self-contained
5. **Never combine distinct features** — one brief per clear intent
6. **Each transcript is isolated** — no context from previous conversations

## Compact Mode (Short Inputs)

For transcripts < 100 words with single clear intent:

```markdown
<!-- PROMPTOR_META: confidence=high|medium|low, mode=compact -->

# [Title]

## Objective

[2-3 sentences]

## Quick Notes

- [Key point 1]
- [Key point 2]
- [Or: No additional notes]
```

## Knowledge Base

- [Output Format](references/output-format.md) — Complete brief structure
- [Processing Rules](references/processing-rules.md) — Detailed extraction methodology
- [Example Brief](templates/brief-example.md) — Concrete input→output example

## Limitations

This skill does NOT:

- Ask clarifying questions (that's the next workflow step)
- Suggest features or improvements
- Generate code, plans, or technical specifications
- Process multiple distinct features in one brief
- Remember context between conversations
- Work on already-structured documents (use for raw/oral input only)

## Version History

| Version | Date    | Changes                                                                                                  |
| ------- | ------- | -------------------------------------------------------------------------------------------------------- |
| 2.0.0   | 2025-12 | Complete rewrite from GPT migration, added confidence indicator, compact mode, measurable prioritization |

## Current: v2.0.0

## Owner

- **Author**: Édouard
- **Contact**: Via Claude.ai
