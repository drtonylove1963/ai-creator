"""
Base Agent class for building autonomous AI agents.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AgentStatus(Enum):
    """Agent execution status."""
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    name: str
    description: str = ""
    model: str = "default"
    temperature: float = 0.7
    max_iterations: int = 10
    tools: List[str] = field(default_factory=list)
    memory_enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResponse:
    """Response from an agent."""
    agent_name: str
    content: Any
    status: AgentStatus
    iterations: int
    thoughts: List[str] = field(default_factory=list)
    actions: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "agent_name": self.agent_name,
            "content": self.content,
            "status": self.status.value,
            "iterations": self.iterations,
            "thoughts": self.thoughts,
            "actions": self.actions,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }


class Agent(ABC):
    """
    Base class for all agents.

    An agent is an autonomous entity that can perceive its environment,
    make decisions, and take actions to achieve specific goals.
    """

    def __init__(self, config: AgentConfig):
        """
        Initialize the agent.

        Args:
            config: Agent configuration
        """
        self.config = config
        self.status = AgentStatus.IDLE
        self.memory: List[Dict[str, Any]] = []
        self.iteration_count = 0

    @abstractmethod
    def think(self, input_data: Any) -> str:
        """
        Agent's thinking process - analyze input and decide on action.

        Args:
            input_data: Input data to process

        Returns:
            Thought or reasoning process
        """
        pass

    @abstractmethod
    def act(self, thought: str, input_data: Any) -> Any:
        """
        Execute an action based on the thought process.

        Args:
            thought: The reasoning from the think step
            input_data: Original input data

        Returns:
            Result of the action
        """
        pass

    def run(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """
        Main execution loop for the agent.

        Args:
            input_data: Input data to process
            context: Optional context information

        Returns:
            Agent response with results
        """
        self.status = AgentStatus.THINKING
        self.iteration_count = 0
        thoughts = []
        actions = []

        try:
            # Think-Act loop
            for i in range(self.config.max_iterations):
                self.iteration_count = i + 1

                # Think phase
                thought = self.think(input_data)
                thoughts.append(thought)

                # Check if we should stop
                if self._should_stop(thought):
                    break

                # Act phase
                self.status = AgentStatus.ACTING
                result = self.act(thought, input_data)
                actions.append({
                    "iteration": i + 1,
                    "thought": thought,
                    "result": result,
                })

                # Store in memory if enabled
                if self.config.memory_enabled:
                    self._store_memory(input_data, thought, result)

                # Update input for next iteration if needed
                input_data = self._update_input(input_data, result)

            self.status = AgentStatus.COMPLETED
            final_result = actions[-1]["result"] if actions else None

            return AgentResponse(
                agent_name=self.config.name,
                content=final_result,
                status=self.status,
                iterations=self.iteration_count,
                thoughts=thoughts,
                actions=actions,
            )

        except Exception as e:
            self.status = AgentStatus.ERROR
            return AgentResponse(
                agent_name=self.config.name,
                content=None,
                status=self.status,
                iterations=self.iteration_count,
                thoughts=thoughts,
                actions=actions,
                metadata={"error": str(e)},
            )

    def _should_stop(self, thought: str) -> bool:
        """
        Determine if the agent should stop iterating.

        Args:
            thought: Current thought

        Returns:
            True if should stop, False otherwise
        """
        # Override this in subclasses for custom stopping conditions
        stop_phrases = ["DONE", "COMPLETE", "FINISHED"]
        return any(phrase in thought.upper() for phrase in stop_phrases)

    def _store_memory(self, input_data: Any, thought: str, result: Any) -> None:
        """
        Store interaction in memory.

        Args:
            input_data: Input data
            thought: Thought process
            result: Action result
        """
        self.memory.append({
            "timestamp": datetime.now(),
            "input": input_data,
            "thought": thought,
            "result": result,
        })

    def _update_input(self, original_input: Any, result: Any) -> Any:
        """
        Update input for next iteration based on result.

        Args:
            original_input: Original input
            result: Result from last action

        Returns:
            Updated input for next iteration
        """
        # By default, keep original input
        # Override in subclasses for different behavior
        return original_input

    def reset(self) -> None:
        """Reset the agent to initial state."""
        self.status = AgentStatus.IDLE
        self.memory.clear()
        self.iteration_count = 0

    def get_memory(self) -> List[Dict[str, Any]]:
        """
        Get agent's memory.

        Returns:
            List of memory entries
        """
        return self.memory.copy()
