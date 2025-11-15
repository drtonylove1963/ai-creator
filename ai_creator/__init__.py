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

# GUI module - optional import (requires gradio)
try:
    from ai_creator.gui import launch_gui, create_app
    _gui_available = True
except ImportError:
    _gui_available = False
    launch_gui = None
    create_app = None

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

# Add GUI exports if available
if _gui_available:
    __all__.extend(["launch_gui", "create_app"])
