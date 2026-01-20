#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Clarification Analyzer

Analyzes briefs to extract keywords, detect domains, and identify missing information.
Used by the intelligent clarification system (F05).

Usage:
    from project_memory.clarification_analyzer import (
        extract_keywords,
        detect_domain,
        identify_missing_info
    )

    keywords = extract_keywords("Add user authentication with OAuth")
    domain = detect_domain(keywords)
    gaps = identify_missing_info(brief, domain.name)
"""

import re
from dataclasses import dataclass, field
from typing import List, Set, Dict, Optional
from enum import Enum


# =============================================================================
# CONSTANTS
# =============================================================================

class Domain(Enum):
    """Technical domains for feature classification."""
    AUTH = "auth"
    API = "api"
    UI = "ui"
    DATA = "data"
    INFRA = "infra"
    NOTIFICATION = "notification"
    PAYMENT = "payment"
    SEARCH = "search"
    UNKNOWN = "unknown"


# Domain keyword mappings
DOMAIN_KEYWORDS: Dict[Domain, Set[str]] = {
    Domain.AUTH: {
        "auth", "authentication", "login", "logout", "password", "oauth", "jwt",
        "token", "session", "permission", "role", "user", "register", "signup",
        "signin", "sso", "ldap", "security", "credential", "2fa", "mfa"
    },
    Domain.API: {
        "api", "endpoint", "rest", "graphql", "webhook", "request", "response",
        "http", "route", "controller", "swagger", "openapi", "json", "xml",
        "serialization", "deserialize", "client", "server"
    },
    Domain.UI: {
        "ui", "frontend", "component", "button", "form", "modal", "page",
        "view", "template", "css", "style", "layout", "responsive", "animation",
        "ux", "design", "interface", "dashboard", "menu", "navigation"
    },
    Domain.DATA: {
        "database", "model", "entity", "migration", "query", "sql", "orm",
        "repository", "schema", "table", "column", "index", "relation",
        "foreign", "primary", "constraint", "data", "storage", "persistence"
    },
    Domain.INFRA: {
        "deploy", "docker", "kubernetes", "ci", "cd", "pipeline", "config",
        "environment", "server", "cloud", "aws", "gcp", "azure", "terraform",
        "ansible", "monitoring", "logging", "cache", "redis", "queue"
    },
    Domain.NOTIFICATION: {
        "notification", "email", "sms", "push", "alert", "message", "send",
        "template", "queue", "async", "event", "listener", "subscriber",
        "broadcast", "channel", "real-time", "websocket"
    },
    Domain.PAYMENT: {
        "payment", "stripe", "paypal", "invoice", "subscription", "billing",
        "checkout", "cart", "order", "transaction", "refund", "price", "tax"
    },
    Domain.SEARCH: {
        "search", "filter", "sort", "pagination", "elasticsearch", "index",
        "query", "fulltext", "autocomplete", "suggestion", "facet", "ranking"
    },
}

# Required information per domain
DOMAIN_REQUIREMENTS: Dict[Domain, List[str]] = {
    Domain.AUTH: ["auth_method", "user_roles", "session_strategy"],
    Domain.API: ["http_methods", "response_format", "error_handling"],
    Domain.UI: ["target_device", "accessibility", "state_management"],
    Domain.DATA: ["data_model", "validation_rules", "relationships"],
    Domain.INFRA: ["environment", "scaling_strategy", "monitoring"],
    Domain.NOTIFICATION: ["channels", "delivery_guarantee", "templates"],
    Domain.PAYMENT: ["provider", "currency", "compliance"],
    Domain.SEARCH: ["search_scope", "ranking_criteria", "performance"],
    Domain.UNKNOWN: ["scope", "constraints", "dependencies"],
}

# French and English stopwords
STOPWORDS: Set[str] = {
    # English
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "can", "need", "to", "of",
    "in", "for", "on", "with", "at", "by", "from", "as", "into", "through",
    "during", "before", "after", "above", "below", "between", "under",
    "again", "further", "then", "once", "here", "there", "when", "where",
    "why", "how", "all", "each", "few", "more", "most", "other", "some",
    "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too",
    "very", "just", "and", "but", "if", "or", "because", "until", "while",
    "it", "its", "this", "that", "these", "those", "i", "me", "my", "we",
    "our", "you", "your", "he", "him", "his", "she", "her", "they", "them",
    # French
    "le", "la", "les", "un", "une", "des", "du", "de", "et", "est", "sont",
    "a", "aux", "avec", "ce", "ces", "dans", "en", "par", "pour", "sur",
    "qui", "que", "quoi", "dont", "où", "si", "ne", "pas", "plus", "moins",
    "tout", "tous", "toute", "toutes", "autre", "autres", "même", "aussi",
    "je", "tu", "il", "elle", "nous", "vous", "ils", "elles", "on",
    "mon", "ton", "son", "notre", "votre", "leur", "mes", "tes", "ses",
    "être", "avoir", "faire", "pouvoir", "vouloir", "devoir", "aller",
    # Common code/tech terms to ignore
    "add", "create", "update", "delete", "remove", "get", "set", "new",
    "feature", "system", "module", "function", "method", "class", "file",
}


# =============================================================================
# DATACLASSES
# =============================================================================

@dataclass
class DomainInfo:
    """Domain detection result."""
    name: str
    confidence: float
    keywords_matched: List[str] = field(default_factory=list)


@dataclass
class GapInfo:
    """Missing information gap."""
    category: str
    description: str
    priority: str  # "high", "medium", "low"
    example_question: str


@dataclass
class BriefAnalysis:
    """Complete brief analysis result."""
    keywords: List[str]
    domain: DomainInfo
    gaps: List[GapInfo]
    scope_indicators: List[str] = field(default_factory=list)


# =============================================================================
# FUNCTIONS
# =============================================================================

def extract_keywords(brief: str) -> List[str]:
    """
    Extract significant keywords from a brief.

    Args:
        brief: The raw brief text.

    Returns:
        List of normalized keywords, ordered by significance.
    """
    if not brief:
        return []

    # Normalize text
    text = brief.lower()

    # Remove special characters but keep hyphens in words
    text = re.sub(r'[^\w\s-]', ' ', text)

    # Split into words
    words = text.split()

    # Filter and normalize
    keywords = []
    seen = set()

    for word in words:
        # Skip short words and stopwords
        if len(word) < 3 or word in STOPWORDS:
            continue

        # Normalize: remove trailing hyphens, numbers-only
        word = word.strip('-')
        if not word or word.isdigit():
            continue

        # Deduplicate
        if word not in seen:
            seen.add(word)
            keywords.append(word)

    return keywords


def detect_domain(keywords: List[str]) -> DomainInfo:
    """
    Detect the technical domain from keywords.

    Args:
        keywords: List of extracted keywords.

    Returns:
        DomainInfo with detected domain and confidence.
    """
    if not keywords:
        return DomainInfo(
            name=Domain.UNKNOWN.value,
            confidence=0.0,
            keywords_matched=[]
        )

    keyword_set = set(keywords)
    scores: Dict[Domain, List[str]] = {}

    for domain, domain_keywords in DOMAIN_KEYWORDS.items():
        matched = keyword_set & domain_keywords
        if matched:
            scores[domain] = list(matched)

    if not scores:
        return DomainInfo(
            name=Domain.UNKNOWN.value,
            confidence=0.0,
            keywords_matched=[]
        )

    # Find best match
    best_domain = max(scores, key=lambda d: len(scores[d]))
    matched_keywords = scores[best_domain]

    # Calculate confidence (matched / total keywords, capped at 1.0)
    confidence = min(len(matched_keywords) / max(len(keywords), 1), 1.0)

    return DomainInfo(
        name=best_domain.value,
        confidence=round(confidence, 2),
        keywords_matched=matched_keywords
    )


def identify_missing_info(brief: str, domain: str) -> List[GapInfo]:
    """
    Identify missing information in the brief based on domain.

    Args:
        brief: The raw brief text.
        domain: The detected domain name.

    Returns:
        List of GapInfo describing missing information.
    """
    gaps = []
    brief_lower = brief.lower()

    # Get domain enum
    try:
        domain_enum = Domain(domain)
    except ValueError:
        domain_enum = Domain.UNKNOWN

    requirements = DOMAIN_REQUIREMENTS.get(domain_enum, DOMAIN_REQUIREMENTS[Domain.UNKNOWN])

    # Check each requirement
    gap_templates = _get_gap_templates()

    for req in requirements:
        if req in gap_templates:
            template = gap_templates[req]
            # Check if any indicator words are present
            if not any(indicator in brief_lower for indicator in template.get("indicators", [])):
                gaps.append(GapInfo(
                    category=req,
                    description=template["description"],
                    priority=template["priority"],
                    example_question=template["question"]
                ))

    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    gaps.sort(key=lambda g: priority_order.get(g.priority, 2))

    return gaps


def analyze_brief(brief: str) -> BriefAnalysis:
    """
    Perform complete brief analysis.

    Args:
        brief: The raw brief text.

    Returns:
        BriefAnalysis with keywords, domain, and gaps.
    """
    keywords = extract_keywords(brief)
    domain = detect_domain(keywords)
    gaps = identify_missing_info(brief, domain.name)

    # Extract scope indicators
    scope_indicators = _extract_scope_indicators(brief)

    return BriefAnalysis(
        keywords=keywords,
        domain=domain,
        gaps=gaps,
        scope_indicators=scope_indicators
    )


# =============================================================================
# INTERNAL HELPERS
# =============================================================================

def _get_gap_templates() -> Dict[str, Dict]:
    """Get gap detection templates."""
    return {
        # Auth domain
        "auth_method": {
            "description": "Authentication method not specified",
            "priority": "high",
            "indicators": ["oauth", "jwt", "session", "token", "sso", "ldap", "basic"],
            "question": "Quelle méthode d'authentification : OAuth, JWT, session-based ?"
        },
        "user_roles": {
            "description": "User roles/permissions not defined",
            "priority": "medium",
            "indicators": ["role", "permission", "admin", "user", "guest", "acl"],
            "question": "Quels rôles utilisateur prévoyez-vous ?"
        },
        "session_strategy": {
            "description": "Session management strategy unclear",
            "priority": "low",
            "indicators": ["session", "stateless", "stateful", "cookie", "storage"],
            "question": "Stratégie de session : stateless (JWT) ou stateful ?"
        },

        # API domain
        "http_methods": {
            "description": "HTTP methods/endpoints not specified",
            "priority": "high",
            "indicators": ["get", "post", "put", "delete", "patch", "crud"],
            "question": "Quelles opérations CRUD sont nécessaires ?"
        },
        "response_format": {
            "description": "Response format not specified",
            "priority": "medium",
            "indicators": ["json", "xml", "format", "schema", "response"],
            "question": "Format de réponse attendu : JSON, XML ?"
        },
        "error_handling": {
            "description": "Error handling strategy unclear",
            "priority": "low",
            "indicators": ["error", "exception", "validation", "handling"],
            "question": "Quelle stratégie de gestion d'erreurs ?"
        },

        # UI domain
        "target_device": {
            "description": "Target devices not specified",
            "priority": "high",
            "indicators": ["mobile", "desktop", "tablet", "responsive", "device"],
            "question": "Cibles : desktop, mobile, les deux ?"
        },
        "accessibility": {
            "description": "Accessibility requirements unclear",
            "priority": "medium",
            "indicators": ["a11y", "accessibility", "wcag", "aria", "screen reader"],
            "question": "Exigences d'accessibilité (WCAG) ?"
        },
        "state_management": {
            "description": "State management approach unclear",
            "priority": "low",
            "indicators": ["state", "redux", "context", "store", "vuex"],
            "question": "Approche de gestion d'état ?"
        },

        # Data domain
        "data_model": {
            "description": "Data model not defined",
            "priority": "high",
            "indicators": ["entity", "model", "schema", "field", "attribute"],
            "question": "Quelles entités et attributs principaux ?"
        },
        "validation_rules": {
            "description": "Validation rules not specified",
            "priority": "medium",
            "indicators": ["validation", "constraint", "required", "format", "rule"],
            "question": "Quelles règles de validation appliquer ?"
        },
        "relationships": {
            "description": "Entity relationships unclear",
            "priority": "medium",
            "indicators": ["relation", "foreign", "one-to-many", "many-to-many", "belongs"],
            "question": "Quelles relations entre entités ?"
        },

        # Notification domain
        "channels": {
            "description": "Notification channels not specified",
            "priority": "high",
            "indicators": ["email", "sms", "push", "in-app", "channel"],
            "question": "Quels canaux : email, SMS, push, in-app ?"
        },
        "delivery_guarantee": {
            "description": "Delivery guarantee unclear",
            "priority": "medium",
            "indicators": ["realtime", "batch", "guarantee", "retry", "queue"],
            "question": "Garantie de livraison : temps réel ou batch acceptable ?"
        },
        "templates": {
            "description": "Notification templates not defined",
            "priority": "low",
            "indicators": ["template", "content", "format", "personalization"],
            "question": "Templates personnalisables nécessaires ?"
        },

        # Generic
        "scope": {
            "description": "Feature scope unclear",
            "priority": "high",
            "indicators": ["include", "exclude", "scope", "limit", "boundary"],
            "question": "Quel est le périmètre exact de cette feature ?"
        },
        "constraints": {
            "description": "Technical constraints not specified",
            "priority": "medium",
            "indicators": ["constraint", "limitation", "requirement", "must", "cannot"],
            "question": "Y a-t-il des contraintes techniques particulières ?"
        },
        "dependencies": {
            "description": "Dependencies not identified",
            "priority": "low",
            "indicators": ["depend", "require", "need", "integrate", "existing"],
            "question": "Quelles dépendances avec des composants existants ?"
        },

        # Infra domain
        "environment": {
            "description": "Target environment not specified",
            "priority": "high",
            "indicators": ["prod", "staging", "dev", "environment", "deploy"],
            "question": "Environnement cible : prod, staging, dev ?"
        },
        "scaling_strategy": {
            "description": "Scaling requirements unclear",
            "priority": "medium",
            "indicators": ["scale", "load", "performance", "capacity", "horizontal"],
            "question": "Exigences de scalabilité ?"
        },
        "monitoring": {
            "description": "Monitoring strategy unclear",
            "priority": "low",
            "indicators": ["monitor", "log", "metric", "alert", "observability"],
            "question": "Stratégie de monitoring requise ?"
        },

        # Payment domain
        "provider": {
            "description": "Payment provider not specified",
            "priority": "high",
            "indicators": ["stripe", "paypal", "provider", "gateway", "processor"],
            "question": "Quel fournisseur de paiement : Stripe, PayPal, autre ?"
        },
        "currency": {
            "description": "Currency handling unclear",
            "priority": "medium",
            "indicators": ["currency", "euro", "dollar", "multi-currency", "conversion"],
            "question": "Quelles devises supporter ?"
        },
        "compliance": {
            "description": "Compliance requirements unclear",
            "priority": "high",
            "indicators": ["pci", "gdpr", "compliance", "regulation", "legal"],
            "question": "Exigences de conformité (PCI-DSS, GDPR) ?"
        },

        # Search domain
        "search_scope": {
            "description": "Search scope not defined",
            "priority": "high",
            "indicators": ["scope", "field", "entity", "content", "fulltext"],
            "question": "Sur quelles entités/champs rechercher ?"
        },
        "ranking_criteria": {
            "description": "Ranking criteria unclear",
            "priority": "medium",
            "indicators": ["rank", "relevance", "score", "boost", "weight"],
            "question": "Critères de tri/ranking des résultats ?"
        },
        "performance": {
            "description": "Performance requirements unclear",
            "priority": "medium",
            "indicators": ["performance", "latency", "speed", "cache", "index"],
            "question": "Exigences de performance (latence max) ?"
        },
    }


def _extract_scope_indicators(brief: str) -> List[str]:
    """Extract scope-related indicators from brief."""
    indicators = []
    brief_lower = brief.lower()

    # Inclusion patterns
    inclusion_patterns = [
        r"includ(?:e|ing|es)\s+(\w+(?:\s+\w+)?)",
        r"avec\s+(\w+(?:\s+\w+)?)",
        r"support(?:er|ing)?\s+(\w+(?:\s+\w+)?)",
    ]

    # Exclusion patterns
    exclusion_patterns = [
        r"(?:not|without|except|excluding|sans|sauf)\s+(\w+(?:\s+\w+)?)",
        r"hors\s+(?:scope|périmètre)",
    ]

    for pattern in inclusion_patterns:
        matches = re.findall(pattern, brief_lower)
        indicators.extend([f"+{m}" for m in matches])

    for pattern in exclusion_patterns:
        matches = re.findall(pattern, brief_lower)
        indicators.extend([f"-{m}" for m in matches])

    return indicators


# =============================================================================
# CLI (for testing)
# =============================================================================

def main():
    """CLI entry point for testing."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python clarification_analyzer.py '<brief>'")
        print("Example: python clarification_analyzer.py 'Add user authentication with OAuth'")
        return 1

    brief = ' '.join(sys.argv[1:])
    analysis = analyze_brief(brief)

    print(f"Keywords: {analysis.keywords}")
    print(f"Domain: {analysis.domain.name} (confidence: {analysis.domain.confidence})")
    print(f"Matched: {analysis.domain.keywords_matched}")
    print(f"Gaps ({len(analysis.gaps)}):")
    for gap in analysis.gaps:
        print(f"  [{gap.priority}] {gap.category}: {gap.description}")
        print(f"       → {gap.example_question}")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
