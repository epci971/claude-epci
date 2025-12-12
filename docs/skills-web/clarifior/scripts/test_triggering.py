#!/usr/bin/env python3
"""
Triggering Test Suite for Clarifior Skill
==========================================

This script validates that the skill triggers correctly on expected inputs
and does NOT trigger on out-of-scope requests.

Usage: python test_triggering.py
"""

# =============================================================================
# TEST CASES
# =============================================================================

# Queries that SHOULD trigger the skill
SHOULD_TRIGGER = [
    # Explicit French triggers
    "clarifie : donc euh je dois rappeler Marc demain",
    "reformule ça : en fait je voulais dire que le projet avance bien",
    "nettoie ce message : bah en gros faut faire le truc là",
    "utilise Clarifior sur ce texte : donc voilà quoi",
    "lance Clarifior : je sais pas trop comment dire mais bon",
    
    # Explicit English triggers
    "clarify: so um I need to call the client tomorrow",
    "rephrase this: basically we should like update the docs",
    "clean up: you know the thing with the project and stuff",
    
    # Natural language (implicit triggers)
    "j'ai dicté ce message, peux-tu le nettoyer ?",
    "voici un message vocal à reformuler",
    "peux-tu clarifier ce que j'ai dit ?",
    "reformulation de mon message dicté",
    
    # Direct invocation
    "Clarifior : donc euh le client a dit que...",
    "utilise le skill clarifior",
]

# Queries that should NOT trigger the skill
SHOULD_NOT_TRIGGER = [
    # Code requests
    "écris-moi une fonction Python pour trier une liste",
    "debug this JavaScript code",
    "create a React component",
    
    # Email generation (execution, not clarification)
    "écris un email professionnel pour le client",
    "rédige une lettre de motivation",
    "génère un email de relance",
    
    # Document creation
    "crée un rapport de vente",
    "fais-moi une présentation PowerPoint",
    "génère un contrat",
    
    # General questions
    "qu'est-ce que le machine learning ?",
    "explique-moi comment fonctionne React",
    "quelle est la capitale de la France ?",
    
    # Analysis requests (not reformulation)
    "analyse ce document",
    "résume cet article",
    "compare ces deux textes",
    
    # Similar but different intents
    "traduis ce texte en anglais",
    "corrige les fautes d'orthographe",
    "améliore le style de ce texte",
]

# Edge cases to test
EDGE_CASES = [
    # Empty or very short
    ("", "Should return polite error"),
    ("ok", "Should ask for more context"),
    ("le", "Should ask for more context"),
    
    # Already clear message
    ("clarifie : Réunion demain 14h salle A", "Should process normally, note clarity"),
    
    # Multiple languages
    ("clarify: donc euh the meeting is tomorrow", "Should handle mixed language"),
    
    # Very long message
    ("reformule : " + "donc en fait " * 50 + "voilà", "Should handle long input"),
    
    # Special characters
    ("clarifie : j'ai besoin d'aide avec l'email de Jean-Pierre", "Should handle apostrophes"),
]

# =============================================================================
# TEST RUNNER
# =============================================================================

def print_header(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}\n")

def print_test(query: str, expected: str, index: int):
    """Print a single test case."""
    truncated = query[:60] + "..." if len(query) > 60 else query
    print(f"  {index:2d}. [{expected}] {truncated}")

def run_tests():
    """Run all test cases and print results."""
    
    print_header("CLARIFIOR SKILL - TRIGGERING TEST SUITE")
    
    # Should trigger tests
    print_header("SHOULD TRIGGER (Expected: ✅)")
    for i, query in enumerate(SHOULD_TRIGGER, 1):
        print_test(query, "✅", i)
    print(f"\n  Total: {len(SHOULD_TRIGGER)} test cases")
    
    # Should not trigger tests
    print_header("SHOULD NOT TRIGGER (Expected: ❌)")
    for i, query in enumerate(SHOULD_NOT_TRIGGER, 1):
        print_test(query, "❌", i)
    print(f"\n  Total: {len(SHOULD_NOT_TRIGGER)} test cases")
    
    # Edge cases
    print_header("EDGE CASES (Manual Review)")
    for i, (query, note) in enumerate(EDGE_CASES, 1):
        display = query if query else "(empty string)"
        truncated = display[:40] + "..." if len(display) > 40 else display
        print(f"  {i}. {truncated}")
        print(f"     → {note}")
    print(f"\n  Total: {len(EDGE_CASES)} test cases")
    
    # Summary
    print_header("SUMMARY")
    total = len(SHOULD_TRIGGER) + len(SHOULD_NOT_TRIGGER) + len(EDGE_CASES)
    print(f"  Should Trigger:     {len(SHOULD_TRIGGER):3d} cases")
    print(f"  Should NOT Trigger: {len(SHOULD_NOT_TRIGGER):3d} cases")
    print(f"  Edge Cases:         {len(EDGE_CASES):3d} cases")
    print(f"  {'─'*30}")
    print(f"  TOTAL:              {total:3d} cases")
    
    print("\n" + "="*60)
    print(" To validate: Test each query in Claude with the skill active")
    print(" Record results in the test matrix below")
    print("="*60)

# =============================================================================
# TEST MATRIX TEMPLATE
# =============================================================================

TEST_MATRIX = """
## Test Results Matrix

| # | Query Type | Query (truncated) | Expected | Actual | Pass? |
|---|------------|-------------------|----------|--------|-------|
| 1 | Explicit FR | "clarifie : donc euh..." | Trigger | | |
| 2 | Explicit EN | "clarify: so um..." | Trigger | | |
| 3 | Natural | "j'ai dicté ce message..." | Trigger | | |
| 4 | Code | "écris-moi une fonction..." | No trigger | | |
| 5 | Email | "écris un email..." | No trigger | | |
| 6 | Empty | "" | Error msg | | |
| 7 | Short | "ok" | Ask context | | |

### Pass Criteria
- ✅ PASS: Behavior matches expected
- ❌ FAIL: Behavior differs from expected
- ⚠️ PARTIAL: Triggers but wrong mode/output

### Overall Status
- [ ] All SHOULD_TRIGGER cases pass
- [ ] All SHOULD_NOT_TRIGGER cases pass  
- [ ] Edge cases handled gracefully
- [ ] Output format correct
- [ ] Language detection works
"""

if __name__ == "__main__":
    run_tests()
    print("\n" + TEST_MATRIX)
