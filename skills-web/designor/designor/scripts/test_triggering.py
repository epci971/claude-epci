#!/usr/bin/env python3
"""
Test triggering script for the `designor` skill.

Validates that the skill description correctly triggers on expected user queries
and does NOT trigger on queries that should route elsewhere.

Run: python test_triggering.py
"""

import re
from typing import List, Tuple

# Trigger keywords from SKILL.md description
POSITIVE_TRIGGERS = [
    "designor",
    "prompt claude design",
    "brief design",
    "nouveau prototype claude",
    "wireframe handoff",
    "générer un deck claude",
    "direction visuelle",
    "variantes design",
    "designor revise",
    "designor un deck",
    "designor pour mon site",
    "claude design prompt",
    "élicitation design",
    "pitch deck claude design",
    "one-pager pour claude design",
    "carousel linkedin pour claude design",
]

# Queries that should NOT trigger designor (route to other skills)
NEGATIVE_TRIGGERS = [
    # → promptor (general prompts)
    "génère un prompt pour gpt",
    "promptor un prompt sur le climat",
    "améliore ce prompt général",
    # → brainstormer (ideation)
    "brainstormer une feature pour mon app",
    "explore l'idée d'un nouveau produit",
    "j'ai une idée de SaaS",
    # → frontend-design (Anthropic — code generation)
    "code-moi un composant React",
    "génère du HTML pour ma landing",
    "crée une page Tailwind",
    # → estimator/propositor
    "estime le coût de ce projet",
    "fais une propale commerciale",
    # → resumator
    "résume ce document",
    "fais un CR de cette réunion",
    # → corrector
    "corrige ce mail",
    "reformule cette réponse client",
    # Generic queries
    "quel temps fait-il aujourd'hui",
    "explique-moi le RGPD",
    "écris-moi un poème",
]

# Ambiguous queries — designor MAY trigger but should ask for disambiguation
AMBIGUOUS_TRIGGERS = [
    "j'ai besoin d'un design",
    "fais-moi un truc visuel",
    "design pour mon site",
    "prompt pour design",
]


def matches_trigger(query: str, triggers: List[str]) -> Tuple[bool, str]:
    """Check if query matches any trigger keyword (case-insensitive substring match)."""
    query_lower = query.lower()
    for trigger in triggers:
        if trigger.lower() in query_lower:
            return True, trigger
    return False, ""


def test_positive_triggers():
    """Test that all positive triggers are recognized."""
    print("=" * 60)
    print("TEST 1 — Positive triggers (should activate designor)")
    print("=" * 60)
    
    failures = []
    for query in POSITIVE_TRIGGERS:
        matched, trigger = matches_trigger(query, POSITIVE_TRIGGERS)
        status = "✅" if matched else "❌"
        print(f"{status} '{query}' → matched: {trigger}")
        if not matched:
            failures.append(query)
    
    print(f"\nResult: {len(POSITIVE_TRIGGERS) - len(failures)}/{len(POSITIVE_TRIGGERS)} passed")
    return len(failures) == 0


def test_negative_triggers():
    """Test that negative triggers do NOT match designor."""
    print("\n" + "=" * 60)
    print("TEST 2 — Negative triggers (should NOT activate designor)")
    print("=" * 60)
    
    failures = []
    for query in NEGATIVE_TRIGGERS:
        matched, trigger = matches_trigger(query, POSITIVE_TRIGGERS)
        status = "✅" if not matched else "❌"
        print(f"{status} '{query}' → matched: {trigger if matched else 'none (correct)'}")
        if matched:
            failures.append((query, trigger))
    
    print(f"\nResult: {len(NEGATIVE_TRIGGERS) - len(failures)}/{len(NEGATIVE_TRIGGERS)} passed")
    if failures:
        print("\n⚠️  False positives detected:")
        for query, trigger in failures:
            print(f"   '{query}' falsely matched '{trigger}'")
    return len(failures) == 0


def test_ambiguous_triggers():
    """Document ambiguous triggers (manual review)."""
    print("\n" + "=" * 60)
    print("TEST 3 — Ambiguous triggers (should ask for disambiguation)")
    print("=" * 60)
    print("These queries may match designor but require clarification:")
    
    for query in AMBIGUOUS_TRIGGERS:
        matched, trigger = matches_trigger(query, POSITIVE_TRIGGERS)
        status = "🤔" if matched else "✅"
        print(f"{status} '{query}' → matched: {trigger if matched else 'none'}")
    
    print("\nNote: ambiguous queries require Phase 0 audit + ask_user_input_v0 disambiguation.")
    return True


def test_template_keywords():
    """Test that deliverable type keywords are detected."""
    print("\n" + "=" * 60)
    print("TEST 4 — Template keyword detection")
    print("=" * 60)
    
    template_keywords = {
        "ui": ["prototype", "app", "interface", "dashboard", "écran"],
        "wireframe-handoff": ["wireframe", "handoff", "maquette dev"],
        "deck": ["deck", "présentation", "pitch", "slides", "investisseur"],
        "one-pager": ["one-pager", "fiche produit", "landing courte", "sales sheet"],
        "social": ["post", "carousel", "linkedin", "instagram", "social media"],
        "explore": ["variantes", "explorations", "directions", "plusieurs styles"],
    }
    
    test_queries = [
        ("designor un dashboard SaaS", "ui"),
        ("designor un wireframe pour handoff Claude Code", "wireframe-handoff"),
        ("designor un pitch deck investisseur", "deck"),
        ("designor un one-pager produit", "one-pager"),
        ("designor un carousel linkedin", "social"),
        ("designor 3 variantes de homepage", "explore"),
    ]
    
    failures = []
    for query, expected_template in test_queries:
        query_lower = query.lower()
        detected = None
        for template, keywords in template_keywords.items():
            for kw in keywords:
                if kw in query_lower:
                    detected = template
                    break
            if detected:
                break
        
        status = "✅" if detected == expected_template else "❌"
        print(f"{status} '{query}' → expected: {expected_template}, detected: {detected}")
        if detected != expected_template:
            failures.append((query, expected_template, detected))
    
    print(f"\nResult: {len(test_queries) - len(failures)}/{len(test_queries)} passed")
    return len(failures) == 0


def test_mode_keywords():
    """Test that mode keywords are detected."""
    print("\n" + "=" * 60)
    print("TEST 5 — Mode keyword detection")
    print("=" * 60)
    
    test_queries = [
        ("designor rapide pour un dashboard", "quick"),
        ("designor quick pour une landing", "quick"),
        ("designor approfondi pour un deck stratégique", "deep"),
        ("designor deep pour un projet client", "deep"),
        ("designor un one-pager", "standard"),  # default
    ]
    
    failures = []
    for query, expected_mode in test_queries:
        query_lower = query.lower()
        if any(kw in query_lower for kw in ["rapide", "quick", "vite", "simple"]):
            detected = "quick"
        elif any(kw in query_lower for kw in ["approfondi", "deep", "complet", "stratégique"]):
            detected = "deep"
        else:
            detected = "standard"
        
        status = "✅" if detected == expected_mode else "❌"
        print(f"{status} '{query}' → expected: {expected_mode}, detected: {detected}")
        if detected != expected_mode:
            failures.append((query, expected_mode, detected))
    
    print(f"\nResult: {len(test_queries) - len(failures)}/{len(test_queries)} passed")
    return len(failures) == 0


def main():
    print("\n" + "=" * 60)
    print("DESIGNOR SKILL — TRIGGERING TESTS")
    print("=" * 60 + "\n")
    
    results = {
        "positive": test_positive_triggers(),
        "negative": test_negative_triggers(),
        "ambiguous": test_ambiguous_triggers(),
        "templates": test_template_keywords(),
        "modes": test_mode_keywords(),
    }
    
    print("\n" + "=" * 60)
    print("OVERALL RESULTS")
    print("=" * 60)
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name:15} {status}")
    
    all_passed = all(results.values())
    print("\n" + ("🎉 All tests passed!" if all_passed else "⚠️  Some tests failed."))
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
