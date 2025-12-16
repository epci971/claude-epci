#!/usr/bin/env python3
"""
Estimator Skill - Triggering Test Suite
========================================

Tests to verify the skill triggers correctly on expected queries
and does NOT trigger on out-of-scope queries.

Usage:
    python test_triggering.py

Expected results:
    - All SHOULD_TRIGGER queries → Skill activates
    - All SHOULD_NOT_TRIGGER queries → Skill does NOT activate
"""

# =============================================================================
# TEST CASES
# =============================================================================

SHOULD_TRIGGER = [
    # Explicit triggers
    "use estimator",
    "utilise le skill estimator",
    "lance estimator sur ce brief",
    
    # French keywords
    "estime ce projet",
    "fais une estimation",
    "chiffre ce développement",
    "donne-moi un chiffrage",
    "évalue le coût de cette application",
    "combien coûterait ce projet",
    "quel budget pour cette plateforme",
    
    # English keywords
    "estimate this project",
    "give me a cost estimate",
    "how much would this cost",
    "calculate the workload",
    
    # JH / Man-days
    "combien de jours/homme",
    "estime les JH",
    "quelle charge de travail",
    "évalue la charge",
    
    # Project types
    "estime cette refonte",
    "chiffre cet audit technique",
    "estimation pour une TMA",
    "budget pour un nouveau développement",
    
    # With context
    "j'ai un brief client, peux-tu l'estimer",
    "voici les specs, fais un chiffrage",
    "à partir de ce brainstorm, estime le projet",
    
    # Implicit but clear
    "prépare un devis technique",
    "évalue ce cahier des charges",
]

SHOULD_NOT_TRIGGER = [
    # Propositor domain (commercial proposal)
    "rédige une proposition commerciale",
    "prépare une propale",
    "fais une offre commerciale",
    
    # Financial/Accounting
    "génère une facture",
    "fais la comptabilité",
    "calcule la TVA",
    
    # Planning (planificator domain)
    "crée un planning projet",
    "fais un diagramme de Gantt",
    "planifie les sprints",
    
    # Code/Development
    "écris du code",
    "développe cette fonctionnalité",
    "corrige ce bug",
    
    # Documentation
    "documente cette API",
    "écris un README",
    "rédige les specs techniques",
    
    # General questions
    "qu'est-ce que Symfony",
    "comment fonctionne React",
    "explique-moi les microservices",
    
    # Other skills
    "résume cette réunion",
    "corrige cet email",
    "brainstorm sur cette idée",
    
    # Vague requests
    "aide-moi",
    "j'ai besoin d'aide",
    "que peux-tu faire",
]

# =============================================================================
# SKILL DESCRIPTION (for reference)
# =============================================================================

SKILL_DESCRIPTION = """
Project estimation tool with interactive workflow. Breaks down projects into
functional components, calculates cost ranges (optimistic/realistic/pessimistic)
with auto-detected risk coefficients. Generates structured Markdown ready for
propositor. Supports dev, refonte, TMA, and audit projects with 3 granularity
levels. Use when user needs to estimate costs, calculate workload, prepare
project budgets, or says "estime", "chiffrage", "JH", "combien coûterait".
Not for invoicing, accounting, contract review, or projects without technical scope.
"""

# =============================================================================
# TEST RUNNER
# =============================================================================

def print_test_cases():
    """Print all test cases for manual verification."""
    
    print("=" * 70)
    print("ESTIMATOR SKILL - TRIGGERING TEST CASES")
    print("=" * 70)
    
    print("\n📗 SHOULD TRIGGER (skill should activate):\n")
    for i, query in enumerate(SHOULD_TRIGGER, 1):
        print(f"  {i:2}. \"{query}\"")
    
    print(f"\n  Total: {len(SHOULD_TRIGGER)} queries")
    
    print("\n" + "-" * 70)
    
    print("\n📕 SHOULD NOT TRIGGER (skill should NOT activate):\n")
    for i, query in enumerate(SHOULD_NOT_TRIGGER, 1):
        print(f"  {i:2}. \"{query}\"")
    
    print(f"\n  Total: {len(SHOULD_NOT_TRIGGER)} queries")
    
    print("\n" + "=" * 70)
    print("MANUAL TEST INSTRUCTIONS")
    print("=" * 70)
    print("""
1. Install the skill in Claude.ai or Claude Code
2. For each SHOULD_TRIGGER query:
   - Send the query to Claude
   - Verify the Estimator skill activates
   - Mark as ✅ PASS or ❌ FAIL

3. For each SHOULD_NOT_TRIGGER query:
   - Send the query to Claude
   - Verify the Estimator skill does NOT activate
   - Mark as ✅ PASS or ❌ FAIL

4. Calculate success rate:
   - Target: 100% for SHOULD_TRIGGER
   - Target: 100% for SHOULD_NOT_TRIGGER
   - Acceptable: >90% with documented edge cases
""")

def generate_test_report_template():
    """Generate a markdown template for test results."""
    
    report = """# Estimator Skill - Triggering Test Report

> Date: [YYYY-MM-DD]
> Tester: [Name]
> Skill Version: 1.0.0

---

## Summary

| Category | Total | Passed | Failed | Rate |
|----------|-------|--------|--------|------|
| SHOULD_TRIGGER | {should} | | | |
| SHOULD_NOT_TRIGGER | {should_not} | | | |
| **TOTAL** | {total} | | | |

---

## SHOULD_TRIGGER Results

| # | Query | Result | Notes |
|---|-------|--------|-------|
""".format(
        should=len(SHOULD_TRIGGER),
        should_not=len(SHOULD_NOT_TRIGGER),
        total=len(SHOULD_TRIGGER) + len(SHOULD_NOT_TRIGGER)
    )
    
    for i, query in enumerate(SHOULD_TRIGGER, 1):
        report += f"| {i} | \"{query}\" | ☐ | |\n"
    
    report += """
---

## SHOULD_NOT_TRIGGER Results

| # | Query | Result | Notes |
|---|-------|--------|-------|
"""
    
    for i, query in enumerate(SHOULD_NOT_TRIGGER, 1):
        report += f"| {i} | \"{query}\" | ☐ | |\n"
    
    report += """
---

## Issues Found

1. [Issue description]
2. [Issue description]

## Recommendations

1. [Recommendation]
2. [Recommendation]

---

*Test report generated by test_triggering.py*
"""
    
    return report

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        # Generate test report template
        report = generate_test_report_template()
        print(report)
    else:
        # Print test cases
        print_test_cases()
        
        print("\nTo generate a test report template, run:")
        print("  python test_triggering.py --report > test_report.md")
