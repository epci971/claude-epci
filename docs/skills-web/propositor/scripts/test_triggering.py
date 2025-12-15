#!/usr/bin/env python3
"""
Propositor Skill - Triggering Test Suite
=========================================

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
    "use propositor",
    "utilise le skill propositor",
    "lance propositor",
    
    # French keywords - proposal
    "rédige une proposition commerciale",
    "prépare une propale",
    "fais une proposition commerciale",
    "génère une offre commerciale",
    "crée une propale pour ce projet",
    
    # French keywords - quote/offer
    "prépare un devis",
    "formalise le devis",
    "rédige une offre",
    "prépare l'offre commerciale",
    
    # English keywords
    "write a commercial proposal",
    "prepare a quote",
    "generate a proposal",
    "create a business proposal",
    
    # With context
    "à partir de l'estimation, fais une propale",
    "transforme ce chiffrage en proposition commerciale",
    "voici l'estimation, génère la proposition",
    
    # RFP responses
    "réponds à cet appel d'offres",
    "prépare la réponse à l'AO",
    "rédige le mémoire technique",
    
    # Template-specific
    "fais une proposition de TMA",
    "prépare une offre d'audit",
    "rédige une propale de développement",
    
    # Implicit but clear
    "mets en forme cette offre pour le client",
    "formalise cette estimation pour le client",
]

SHOULD_NOT_TRIGGER = [
    # Estimator domain
    "estime ce projet",
    "fais un chiffrage",
    "combien coûterait ce développement",
    "calcule les JH",
    
    # Invoicing/Accounting
    "génère une facture",
    "fais la facturation",
    "prépare le bon de commande",
    
    # Contract/Legal
    "rédige le contrat",
    "prépare les CGV",
    "fais les conditions légales",
    
    # Planning
    "crée un planning projet",
    "fais un Gantt",
    "planifie les sprints",
    
    # Code/Development
    "écris du code",
    "développe cette fonctionnalité",
    "code cette feature",
    
    # Documentation
    "documente l'API",
    "écris un README",
    "rédige la doc technique",
    
    # Other skills
    "résume cette réunion",
    "brainstorm sur cette idée",
    "critique ce document",
    "corrige cet email",
    
    # General questions
    "qu'est-ce qu'une propale",
    "comment rédiger une offre",
    "explique-moi les appels d'offres",
    
    # Without estimator context
    "fais une proposition",  # Too vague, no estimation context
]

# =============================================================================
# SKILL DESCRIPTION (for reference)
# =============================================================================

SKILL_DESCRIPTION = """
Commercial proposal generator requiring estimator output. Creates professional,
client-adapted proposals with 5 templates (dev, refonte, TMA, audit, ao-public).
Adapts tone to client type (startup/PME/grand-compte/public/GMS/industriel).
Generates Mermaid Gantt charts and validates data coherence. Interactive workflow
with checkpoints. Use when preparing quotes, responding to RFPs, formalizing offers,
or user says "proposition commerciale", "propale", "offre", "devis".
Not for estimation (use estimator first), invoicing, or contract legal review.
"""

# =============================================================================
# DEPENDENCY TEST CASES
# =============================================================================

DEPENDENCY_TESTS = [
    {
        "name": "With Estimator Output",
        "context": "Estimator output present in conversation",
        "query": "génère la proposition commerciale",
        "expected": "Proceed with proposal generation"
    },
    {
        "name": "Without Estimator Output",
        "context": "No estimator output in conversation",
        "query": "génère la proposition commerciale",
        "expected": "Request estimator output first"
    },
    {
        "name": "With File Upload",
        "context": "User uploads estimation.md file",
        "query": "voici l'estimation, fais la propale",
        "expected": "Parse file and proceed"
    },
]

# =============================================================================
# TEST RUNNER
# =============================================================================

def print_test_cases():
    """Print all test cases for manual verification."""
    
    print("=" * 70)
    print("PROPOSITOR SKILL - TRIGGERING TEST CASES")
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
    
    print("\n" + "-" * 70)
    
    print("\n📘 DEPENDENCY TESTS:\n")
    for i, test in enumerate(DEPENDENCY_TESTS, 1):
        print(f"  {i}. {test['name']}")
        print(f"     Context: {test['context']}")
        print(f"     Query: \"{test['query']}\"")
        print(f"     Expected: {test['expected']}")
        print()
    
    print("=" * 70)
    print("MANUAL TEST INSTRUCTIONS")
    print("=" * 70)
    print("""
1. Install the skill in Claude.ai or Claude Code

2. For SHOULD_TRIGGER tests:
   - First run estimator to generate estimation output
   - Then send the query to Claude
   - Verify Propositor skill activates
   - Mark as ✅ PASS or ❌ FAIL

3. For SHOULD_NOT_TRIGGER tests:
   - Send the query to Claude
   - Verify Propositor skill does NOT activate
   - Mark as ✅ PASS or ❌ FAIL

4. For DEPENDENCY tests:
   - Test with and without estimator output
   - Verify correct behavior in each case

5. Calculate success rate:
   - Target: 100% for SHOULD_TRIGGER
   - Target: 100% for SHOULD_NOT_TRIGGER
   - Acceptable: >90% with documented edge cases
""")

def generate_test_report_template():
    """Generate a markdown template for test results."""
    
    report = """# Propositor Skill - Triggering Test Report

> Date: [YYYY-MM-DD]
> Tester: [Name]
> Skill Version: 1.0.0

---

## Summary

| Category | Total | Passed | Failed | Rate |
|----------|-------|--------|--------|------|
| SHOULD_TRIGGER | {should} | | | |
| SHOULD_NOT_TRIGGER | {should_not} | | | |
| DEPENDENCY_TESTS | {dep} | | | |
| **TOTAL** | {total} | | | |

---

## SHOULD_TRIGGER Results

| # | Query | Result | Notes |
|---|-------|--------|-------|
""".format(
        should=len(SHOULD_TRIGGER),
        should_not=len(SHOULD_NOT_TRIGGER),
        dep=len(DEPENDENCY_TESTS),
        total=len(SHOULD_TRIGGER) + len(SHOULD_NOT_TRIGGER) + len(DEPENDENCY_TESTS)
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

## DEPENDENCY_TESTS Results

| # | Test | Context | Result | Notes |
|---|------|---------|--------|-------|
"""
    
    for i, test in enumerate(DEPENDENCY_TESTS, 1):
        report += f"| {i} | {test['name']} | {test['context']} | ☐ | |\n"
    
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
# COHERENCE VALIDATION TESTS
# =============================================================================

def print_coherence_tests():
    """Print coherence validation test cases."""
    
    print("\n" + "=" * 70)
    print("COHERENCE VALIDATION TEST CASES")
    print("=" * 70)
    
    tests = [
        {
            "name": "Amount Mismatch",
            "input": "Total: 45000€, Lots sum: 43500€",
            "expected": "🔴 Blocking alert"
        },
        {
            "name": "Planning Too Short",
            "input": "120 JH, 8 weeks planned",
            "expected": "🟡 Warning alert"
        },
        {
            "name": "Missing FCT Reference",
            "input": "FCT-007 in task, not in features",
            "expected": "🟡 Warning alert"
        },
        {
            "name": "Placeholder Remaining",
            "input": "[XXX] in final document",
            "expected": "🔴 Blocking alert"
        },
        {
            "name": "All Coherent",
            "input": "All data matches",
            "expected": "✅ No alerts"
        },
    ]
    
    print("\n📋 COHERENCE TESTS:\n")
    for i, test in enumerate(tests, 1):
        print(f"  {i}. {test['name']}")
        print(f"     Input: {test['input']}")
        print(f"     Expected: {test['expected']}")
        print()

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--report":
            # Generate test report template
            report = generate_test_report_template()
            print(report)
        elif sys.argv[1] == "--coherence":
            # Print coherence tests
            print_coherence_tests()
    else:
        # Print all test cases
        print_test_cases()
        
        print("\nAdditional commands:")
        print("  python test_triggering.py --report > test_report.md")
        print("  python test_triggering.py --coherence")
