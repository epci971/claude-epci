#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Similarity Matcher

Calculates similarity between briefs and existing features using Jaccard similarity.
Used by the intelligent clarification system (F05).

Usage:
    from project_memory.similarity_matcher import (
        find_similar_features,
        calculate_similarity
    )

    similar = find_similar_features(features, keywords, threshold=0.7)
"""

import re
from dataclasses import dataclass
from typing import List, Set, Tuple, Dict, Any, Optional


# =============================================================================
# DATACLASSES
# =============================================================================

@dataclass
class SimilarFeature:
    """A feature matched by similarity."""
    slug: str
    title: str
    score: float
    matched_keywords: List[str]
    complexity: str
    files_modified: List[str]


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def normalize_text(text: str) -> Set[str]:
    """
    Normalize text to a set of lowercase words.

    Args:
        text: Input text to normalize.

    Returns:
        Set of normalized words.
    """
    if not text:
        return set()

    # Lowercase and remove special characters
    text = text.lower()
    text = re.sub(r'[^\w\s-]', ' ', text)

    # Split and filter
    words = set()
    for word in text.split():
        word = word.strip('-')
        if len(word) >= 2 and not word.isdigit():
            words.add(word)

    return words


def calculate_jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """
    Calculate Jaccard similarity between two sets.

    Jaccard = |A ∩ B| / |A ∪ B|

    Args:
        set1: First set of words.
        set2: Second set of words.

    Returns:
        Similarity score between 0 and 1.
    """
    if not set1 or not set2:
        return 0.0

    intersection = len(set1 & set2)
    union = len(set1 | set2)

    if union == 0:
        return 0.0

    return intersection / union


def calculate_similarity(keywords: List[str], feature_title: str, feature_slug: str = "") -> Tuple[float, List[str]]:
    """
    Calculate similarity between keywords and a feature.

    Uses a weighted combination of:
    - Jaccard similarity on title words
    - Direct keyword matches in slug

    Args:
        keywords: List of keywords from the brief.
        feature_title: Title of the feature to compare.
        feature_slug: Optional slug for additional matching.

    Returns:
        Tuple of (score, matched_keywords).
    """
    if not keywords:
        return 0.0, []

    keyword_set = set(keywords)

    # Normalize feature text
    title_words = normalize_text(feature_title)
    slug_words = normalize_text(feature_slug.replace('-', ' '))

    # Combine feature words
    feature_words = title_words | slug_words

    # Calculate Jaccard similarity
    jaccard = calculate_jaccard_similarity(keyword_set, feature_words)

    # Find exact matches
    matched = list(keyword_set & feature_words)

    # Boost score if we have direct matches
    match_boost = min(len(matched) * 0.1, 0.3)  # Max 30% boost

    final_score = min(jaccard + match_boost, 1.0)

    return round(final_score, 3), matched


def find_similar_features(
    features: List[Dict[str, Any]],
    keywords: List[str],
    threshold: float = 0.3
) -> List[SimilarFeature]:
    """
    Find features similar to the given keywords.

    Args:
        features: List of feature dictionaries with 'slug', 'title', 'complexity', 'files_modified'.
        keywords: Keywords extracted from the brief.
        threshold: Minimum similarity score (default 0.3 for broader matching).

    Returns:
        List of SimilarFeature sorted by score descending.
    """
    if not features or not keywords:
        return []

    results = []

    for feature in features:
        slug = feature.get('slug', '')
        title = feature.get('title', slug)  # Fallback to slug if no title

        score, matched = calculate_similarity(keywords, title, slug)

        if score >= threshold:
            results.append(SimilarFeature(
                slug=slug,
                title=title,
                score=score,
                matched_keywords=matched,
                complexity=feature.get('complexity', 'UNKNOWN'),
                files_modified=feature.get('files_modified', [])[:5]  # Limit to 5
            ))

    # Sort by score descending
    results.sort(key=lambda f: f.score, reverse=True)

    return results


def find_best_match(
    features: List[Dict[str, Any]],
    keywords: List[str],
    min_score: float = 0.5
) -> Optional[SimilarFeature]:
    """
    Find the single best matching feature.

    Args:
        features: List of feature dictionaries.
        keywords: Keywords from the brief.
        min_score: Minimum score to consider a match.

    Returns:
        Best matching SimilarFeature or None.
    """
    matches = find_similar_features(features, keywords, threshold=min_score)
    return matches[0] if matches else None


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def extract_common_patterns(similar_features: List[SimilarFeature]) -> List[str]:
    """
    Extract common patterns from similar features.

    Looks at file paths to identify common architectural patterns.

    Args:
        similar_features: List of matched features.

    Returns:
        List of detected patterns (e.g., "Repository pattern", "Service layer").
    """
    patterns = set()

    pattern_indicators = {
        "Repository": ["repository", "repo"],
        "Service": ["service", "services"],
        "Controller": ["controller", "controllers"],
        "Entity/Model": ["entity", "model", "models"],
        "Event-driven": ["event", "listener", "handler"],
        "Command/Query": ["command", "query", "handler"],
        "DTO": ["dto", "request", "response"],
    }

    all_files = []
    for feature in similar_features:
        all_files.extend(feature.files_modified)

    files_lower = [f.lower() for f in all_files]

    for pattern_name, indicators in pattern_indicators.items():
        for indicator in indicators:
            if any(indicator in f for f in files_lower):
                patterns.add(pattern_name)
                break

    return list(patterns)


# =============================================================================
# CLI (for testing)
# =============================================================================

def main():
    """CLI entry point for testing."""
    import json
    import sys

    # Example features for testing
    test_features = [
        {
            "slug": "user-authentication",
            "title": "User Authentication with OAuth",
            "complexity": "STANDARD",
            "files_modified": ["src/Service/AuthService.php", "src/Controller/AuthController.php"]
        },
        {
            "slug": "email-notifications",
            "title": "Email Notification System",
            "complexity": "STANDARD",
            "files_modified": ["src/Service/NotificationService.php", "src/Event/UserRegistered.php"]
        },
        {
            "slug": "user-profile",
            "title": "User Profile Management",
            "complexity": "SMALL",
            "files_modified": ["src/Entity/UserProfile.php"]
        }
    ]

    if len(sys.argv) < 2:
        print("Usage: python similarity_matcher.py '<keywords>'")
        print("Example: python similarity_matcher.py 'auth login oauth user'")
        print("\nUsing default test keywords: ['notification', 'email', 'user']")
        keywords = ["notification", "email", "user"]
    else:
        keywords = sys.argv[1].split()

    print(f"Keywords: {keywords}")
    print(f"Searching {len(test_features)} features...\n")

    matches = find_similar_features(test_features, keywords, threshold=0.2)

    if matches:
        print(f"Found {len(matches)} matches:")
        for match in matches:
            print(f"\n  {match.slug} (score: {match.score})")
            print(f"    Title: {match.title}")
            print(f"    Matched: {match.matched_keywords}")
            print(f"    Complexity: {match.complexity}")

        patterns = extract_common_patterns(matches)
        if patterns:
            print(f"\nDetected patterns: {patterns}")
    else:
        print("No matches found above threshold")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
