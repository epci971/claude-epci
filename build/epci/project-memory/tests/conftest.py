#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pytest fixtures for EPCI Project Memory tests.
"""

import pytest
from typing import List, Dict, Any


@pytest.fixture
def sample_features() -> List[Dict[str, Any]]:
    """Sample feature data for testing."""
    return [
        {
            "slug": "user-authentication",
            "title": "User Authentication with OAuth",
            "complexity": "STANDARD",
            "files_modified": [
                "src/Service/AuthService.php",
                "src/Controller/AuthController.php",
                "src/Entity/User.php"
            ],
            "completed_at": "2025-01-15T10:00:00Z",
        },
        {
            "slug": "email-notifications",
            "title": "Email Notification System",
            "complexity": "STANDARD",
            "files_modified": [
                "src/Service/NotificationService.php",
                "src/Event/UserRegistered.php",
                "src/Listener/SendEmailListener.php"
            ],
            "completed_at": "2025-01-10T14:30:00Z",
        },
        {
            "slug": "user-profile",
            "title": "User Profile Management",
            "complexity": "SMALL",
            "files_modified": [
                "src/Entity/UserProfile.php",
                "src/Controller/ProfileController.php"
            ],
            "completed_at": "2025-01-05T09:00:00Z",
        },
        {
            "slug": "api-rate-limiting",
            "title": "API Rate Limiting",
            "complexity": "STANDARD",
            "files_modified": [
                "src/Middleware/RateLimitMiddleware.php",
                "src/Service/RateLimiter.php"
            ],
            "completed_at": "2025-01-01T11:00:00Z",
        },
    ]


@pytest.fixture
def sample_brief_auth() -> str:
    """Sample brief for authentication feature."""
    return "Ajouter un système d'authentification OAuth pour les utilisateurs"


@pytest.fixture
def sample_brief_notification() -> str:
    """Sample brief for notification feature."""
    return "Ajouter un système de notifications par email et push"


@pytest.fixture
def sample_brief_vague() -> str:
    """Sample vague brief that needs clarification."""
    return "Améliorer le système"


@pytest.fixture
def sample_context() -> Dict[str, Any]:
    """Sample project context."""
    return {
        "domain": "notification",
        "patterns": ["event-driven", "service-layer"],
        "stack": "symfony",
        "keywords": ["notification", "email", "push"],
    }


@pytest.fixture
def sample_gaps() -> List[Dict[str, Any]]:
    """Sample gaps from analyzer."""
    return [
        {
            "category": "channels",
            "description": "Notification channels not specified",
            "priority": "high",
            "example_question": "Quels canaux de notification : email, push, in-app ?"
        },
        {
            "category": "delivery_guarantee",
            "description": "Delivery guarantee unclear",
            "priority": "medium",
            "example_question": "Garantie de livraison : temps réel ou batch ?"
        },
    ]
