"""
Base classes for the skill system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class SkillCategory(Enum):
    """Categories of skills."""
    COMMUNICATION = "communication"
    CODE = "code"
    RESEARCH = "research"
    DATA = "data"
    CREATIVE = "creative"
    ANALYSIS = "analysis"
    AUTOMATION = "automation"
    CUSTOM = "custom"


@dataclass
class SkillConfig:
    """Configuration for a skill."""
    name: str
    description: str
    category: SkillCategory = SkillCategory.CUSTOM
    version: str = "1.0.0"
    author: str = "Unknown"
    requires: List[str] = field(default_factory=list)  # Required dependencies
    parameters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SkillResult:
    """Result from executing a skill."""
    skill_name: str
    success: bool
    output: Any
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "skill_name": self.skill_name,
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "execution_time": self.execution_time,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }


class Skill(ABC):
    """
    Base class for all skills.

    A skill is a specialized capability that an agent can learn and use.
    Skills are modular, reusable, and can be combined to create complex behaviors.
    """

    def __init__(self, config: SkillConfig):
        """
        Initialize the skill.

        Args:
            config: Skill configuration
        """
        self.config = config
        self.execution_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.total_execution_time = 0.0
        self._initialized = False

    @abstractmethod
    def execute(self, input_data: Any, **kwargs) -> SkillResult:
        """
        Execute the skill.

        Args:
            input_data: Input data for the skill
            **kwargs: Additional keyword arguments

        Returns:
            SkillResult with execution results
        """
        pass

    def initialize(self) -> None:
        """
        Initialize the skill (called once before first use).
        Override this method for custom initialization logic.
        """
        self._initialized = True

    def validate_input(self, input_data: Any) -> bool:
        """
        Validate input data before execution.

        Args:
            input_data: Input to validate

        Returns:
            True if valid, False otherwise
        """
        # Default implementation - override for custom validation
        return True

    def can_execute(self, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Check if skill can be executed in the given context.

        Args:
            context: Execution context

        Returns:
            True if skill can execute, False otherwise
        """
        return self._initialized

    def run(self, input_data: Any, **kwargs) -> SkillResult:
        """
        Run the skill with error handling and metrics tracking.

        Args:
            input_data: Input data
            **kwargs: Additional arguments

        Returns:
            SkillResult with execution results
        """
        import time

        # Initialize if not already done
        if not self._initialized:
            self.initialize()

        # Validate input
        if not self.validate_input(input_data):
            return SkillResult(
                skill_name=self.config.name,
                success=False,
                output=None,
                error="Input validation failed"
            )

        # Execute skill
        start_time = time.time()
        self.execution_count += 1

        try:
            result = self.execute(input_data, **kwargs)
            result.execution_time = time.time() - start_time
            self.total_execution_time += result.execution_time

            if result.success:
                self.success_count += 1
            else:
                self.failure_count += 1

            return result

        except Exception as e:
            self.failure_count += 1
            return SkillResult(
                skill_name=self.config.name,
                success=False,
                output=None,
                error=f"Execution error: {str(e)}",
                execution_time=time.time() - start_time
            )

    def get_stats(self) -> Dict[str, Any]:
        """
        Get execution statistics for this skill.

        Returns:
            Dictionary with statistics
        """
        success_rate = (
            (self.success_count / self.execution_count * 100)
            if self.execution_count > 0
            else 0
        )

        avg_execution_time = (
            (self.total_execution_time / self.execution_count)
            if self.execution_count > 0
            else 0
        )

        return {
            "skill_name": self.config.name,
            "executions": self.execution_count,
            "successes": self.success_count,
            "failures": self.failure_count,
            "success_rate": f"{success_rate:.2f}%",
            "total_time": f"{self.total_execution_time:.2f}s",
            "avg_time": f"{avg_execution_time:.2f}s",
        }

    def reset_stats(self) -> None:
        """Reset execution statistics."""
        self.execution_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.total_execution_time = 0.0

    def get_info(self) -> Dict[str, Any]:
        """
        Get skill information.

        Returns:
            Dictionary with skill details
        """
        return {
            "name": self.config.name,
            "description": self.config.description,
            "category": self.config.category.value,
            "version": self.config.version,
            "author": self.config.author,
            "requires": self.config.requires,
            "parameters": self.config.parameters,
        }

    def __repr__(self) -> str:
        """String representation."""
        return f"<Skill: {self.config.name} ({self.config.category.value})>"
