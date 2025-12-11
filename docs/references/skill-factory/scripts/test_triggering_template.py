#!/usr/bin/env python3
"""
Skill Triggering Test Template
==============================

This script provides a framework for testing skill triggering behavior.
Customize the TEST_CASES for your specific skill.

Usage:
    python test_triggering.py

Requirements:
    - Python 3.8+
    - No external dependencies (uses only stdlib)

Customization:
    1. Update SKILL_NAME with your skill name
    2. Modify TEST_CASES with your test scenarios
    3. Run tests and verify results manually in Claude
"""

import json
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

# =============================================================================
# CONFIGURATION - Customize for your skill
# =============================================================================

SKILL_NAME = "your-skill-name"  # Replace with actual skill name

# =============================================================================
# TEST CASES - Define your test scenarios
# =============================================================================

@dataclass
class TestCase:
    """Represents a single test case for triggering verification."""
    query: str
    should_trigger: bool
    category: str
    description: str
    expected_behavior: Optional[str] = None


# Define your test cases here
TEST_CASES = [
    # ==========================================================================
    # EXPLICIT TRIGGERING - Should ALWAYS trigger
    # ==========================================================================
    TestCase(
        query=f"Use the {SKILL_NAME} skill to [action]",
        should_trigger=True,
        category="explicit",
        description="Direct skill invocation",
        expected_behavior="Skill activates and performs requested action"
    ),
    TestCase(
        query=f"Apply {SKILL_NAME} to [input]",
        should_trigger=True,
        category="explicit",
        description="Alternative explicit invocation",
        expected_behavior="Skill activates"
    ),
    
    # ==========================================================================
    # IMPLICIT TRIGGERING - Should trigger based on semantic matching
    # ==========================================================================
    TestCase(
        query="[Natural language request matching skill purpose]",
        should_trigger=True,
        category="implicit",
        description="Natural language trigger - primary use case",
        expected_behavior="Skill activates based on semantic match"
    ),
    TestCase(
        query="[Another natural request with trigger keywords]",
        should_trigger=True,
        category="implicit",
        description="Natural language trigger - secondary use case",
        expected_behavior="Skill activates"
    ),
    TestCase(
        query="[Request using domain-specific terminology]",
        should_trigger=True,
        category="implicit",
        description="Domain terminology trigger",
        expected_behavior="Skill activates"
    ),
    
    # ==========================================================================
    # OUT-OF-SCOPE - Should NOT trigger
    # ==========================================================================
    TestCase(
        query="[Request that seems related but is out of scope]",
        should_trigger=False,
        category="out-of-scope",
        description="Related but excluded use case",
        expected_behavior="Skill does NOT activate"
    ),
    TestCase(
        query="[Generic request that shouldn't trigger this skill]",
        should_trigger=False,
        category="out-of-scope",
        description="Generic request - no trigger",
        expected_behavior="Normal Claude response, no skill"
    ),
    TestCase(
        query="What's the weather today?",
        should_trigger=False,
        category="out-of-scope",
        description="Completely unrelated request",
        expected_behavior="Normal Claude response"
    ),
    
    # ==========================================================================
    # EDGE CASES - Boundary conditions
    # ==========================================================================
    TestCase(
        query="[Request with partial keyword match]",
        should_trigger=True,  # or False, depending on design
        category="edge-case",
        description="Partial keyword match",
        expected_behavior="Define expected behavior"
    ),
    TestCase(
        query="[Request with misspelled keywords]",
        should_trigger=True,  # semantic matching should handle
        category="edge-case",
        description="Misspelled trigger words",
        expected_behavior="Skill may or may not activate"
    ),
    TestCase(
        query="[Ambiguous request that could match multiple skills]",
        should_trigger=True,  # or False
        category="edge-case",
        description="Ambiguous multi-skill match",
        expected_behavior="Document which skill should win"
    ),
]


# =============================================================================
# TEST RUNNER
# =============================================================================

def run_tests():
    """Generate test report and instructions."""
    
    print("=" * 70)
    print(f"TRIGGERING TEST SUITE FOR: {SKILL_NAME}")
    print(f"Generated: {datetime.now().isoformat()}")
    print("=" * 70)
    
    # Group by category
    categories = {}
    for tc in TEST_CASES:
        if tc.category not in categories:
            categories[tc.category] = []
        categories[tc.category].append(tc)
    
    # Print test cases by category
    for category, cases in categories.items():
        print(f"\n{'='*70}")
        print(f"CATEGORY: {category.upper()}")
        print(f"Expected: {'TRIGGER' if cases[0].should_trigger else 'NO TRIGGER'}")
        print("=" * 70)
        
        for i, tc in enumerate(cases, 1):
            print(f"\n--- Test {category.upper()}-{i}: {tc.description} ---")
            print(f"Query: \"{tc.query}\"")
            print(f"Should trigger: {'✅ YES' if tc.should_trigger else '❌ NO'}")
            if tc.expected_behavior:
                print(f"Expected: {tc.expected_behavior}")
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    total = len(TEST_CASES)
    should_trigger = sum(1 for tc in TEST_CASES if tc.should_trigger)
    should_not_trigger = total - should_trigger
    
    print(f"Total test cases: {total}")
    print(f"  - Should trigger: {should_trigger}")
    print(f"  - Should NOT trigger: {should_not_trigger}")
    
    print("\nCategories:")
    for category, cases in categories.items():
        print(f"  - {category}: {len(cases)} tests")
    
    # Instructions
    print("\n" + "=" * 70)
    print("MANUAL TESTING INSTRUCTIONS")
    print("=" * 70)
    print("""
1. Open Claude Code or Claude.ai with the skill enabled
2. For each test case above:
   a. Enter the query exactly as shown
   b. Observe if the skill activates
   c. Compare with expected behavior
3. Record results in the test matrix below
4. Investigate any mismatches
    """)
    
    # Generate result matrix template
    print("\n" + "=" * 70)
    print("RESULT MATRIX (copy and fill)")
    print("=" * 70)
    print("""
| # | Category | Query | Expected | Actual | Pass |
|---|----------|-------|----------|--------|------|""")
    
    for i, tc in enumerate(TEST_CASES, 1):
        expected = "TRIGGER" if tc.should_trigger else "NO"
        query_short = tc.query[:30] + "..." if len(tc.query) > 30 else tc.query
        print(f"| {i} | {tc.category} | {query_short} | {expected} | ___ | ☐ |")


def export_json():
    """Export test cases as JSON for programmatic use."""
    
    data = {
        "skill_name": SKILL_NAME,
        "generated": datetime.now().isoformat(),
        "test_cases": [
            {
                "query": tc.query,
                "should_trigger": tc.should_trigger,
                "category": tc.category,
                "description": tc.description,
                "expected_behavior": tc.expected_behavior
            }
            for tc in TEST_CASES
        ]
    }
    
    filename = f"test_cases_{SKILL_NAME}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nExported to: {filename}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        export_json()
    else:
        run_tests()
        
        print("\n" + "-" * 70)
        print("TIP: Run with --json to export test cases as JSON file")
        print("-" * 70)
