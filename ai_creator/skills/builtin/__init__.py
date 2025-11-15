"""
Built-in skills for AI Creator agents.

This module provides a collection of pre-built skills that agents can use.
"""

from ai_creator.skills.builtin.code_skills import (
    CodeGenerationSkill,
    CodeReviewSkill,
    DebugSkill,
)
from ai_creator.skills.builtin.research_skills import (
    WebSearchSkill,
    SummarizationSkill,
    FactCheckSkill,
)
from ai_creator.skills.builtin.communication_skills import (
    EmailWritingSkill,
    ReportGenerationSkill,
    TranslationSkill,
)
from ai_creator.skills.builtin.data_skills import (
    DataAnalysisSkill,
    DataVisualizationSkill,
    DataCleaningSkill,
)

__all__ = [
    # Code skills
    "CodeGenerationSkill",
    "CodeReviewSkill",
    "DebugSkill",
    # Research skills
    "WebSearchSkill",
    "SummarizationSkill",
    "FactCheckSkill",
    # Communication skills
    "EmailWritingSkill",
    "ReportGenerationSkill",
    "TranslationSkill",
    # Data skills
    "DataAnalysisSkill",
    "DataVisualizationSkill",
    "DataCleaningSkill",
]


def register_all_builtin_skills(registry):
    """
    Register all built-in skills with a registry.

    Args:
        registry: SkillRegistry instance
    """
    # Code skills
    registry.register(CodeGenerationSkill())
    registry.register(CodeReviewSkill())
    registry.register(DebugSkill())

    # Research skills
    registry.register(WebSearchSkill())
    registry.register(SummarizationSkill())
    registry.register(FactCheckSkill())

    # Communication skills
    registry.register(EmailWritingSkill())
    registry.register(ReportGenerationSkill())
    registry.register(TranslationSkill())

    # Data skills
    registry.register(DataAnalysisSkill())
    registry.register(DataVisualizationSkill())
    registry.register(DataCleaningSkill())
