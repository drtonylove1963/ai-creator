"""
AI Creator - A versatile toolkit for building AI-powered creative applications.
"""

__version__ = "0.1.0"
__author__ = "AI Creator Team"

from ai_creator.core.creator import Creator
from ai_creator.agents import (
    Agent,
    AgentConfig,
    AgentResponse,
    AgentManager,
    TextAgent,
    ImageAgent,
    AnalysisAgent,
)

__all__ = [
    "Creator",
    "Agent",
    "AgentConfig",
    "AgentResponse",
    "AgentManager",
    "TextAgent",
    "ImageAgent",
    "AnalysisAgent",
]
