"""
Agent system for AI Creator.

This module provides a flexible agent architecture for building autonomous AI agents.
"""

from ai_creator.agents.base import Agent, AgentConfig, AgentResponse
from ai_creator.agents.manager import AgentManager
from ai_creator.agents.text_agent import TextAgent
from ai_creator.agents.image_agent import ImageAgent
from ai_creator.agents.analysis_agent import AnalysisAgent

__all__ = [
    "Agent",
    "AgentConfig",
    "AgentResponse",
    "AgentManager",
    "TextAgent",
    "ImageAgent",
    "AnalysisAgent",
]
