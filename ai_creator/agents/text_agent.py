"""
Text generation and processing agent.
"""

from typing import Any
from ai_creator.agents.base import Agent, AgentConfig


class TextAgent(Agent):
    """
    Agent specialized in text generation and processing tasks.

    This agent can:
    - Generate creative text
    - Rewrite and refine content
    - Summarize text
    - Transform text styles
    """

    def __init__(self, name: str = "TextAgent", **kwargs):
        """
        Initialize the TextAgent.

        Args:
            name: Agent name
            **kwargs: Additional configuration parameters
        """
        config = AgentConfig(
            name=name,
            description="Agent for text generation and processing",
            **kwargs
        )
        super().__init__(config)
        self.task_type = None

    def think(self, input_data: Any) -> str:
        """
        Analyze the text task and plan the approach.

        Args:
            input_data: Input containing text task

        Returns:
            Thought process
        """
        # Determine task type
        if isinstance(input_data, dict):
            task = input_data.get("task", "")
            content = input_data.get("content", "")
        else:
            task = "generate"
            content = str(input_data)

        # Analyze what needs to be done
        if "summary" in task.lower() or "summarize" in task.lower():
            self.task_type = "summarize"
            return f"I need to summarize the following content: {content[:100]}..."
        elif "rewrite" in task.lower() or "refine" in task.lower():
            self.task_type = "rewrite"
            return f"I need to rewrite/refine: {content[:100]}..."
        elif "generate" in task.lower() or "create" in task.lower():
            self.task_type = "generate"
            return f"I need to generate text based on: {content}"
        else:
            self.task_type = "process"
            return f"I need to process the text: {content[:100]}..."

    def act(self, thought: str, input_data: Any) -> Any:
        """
        Execute the text processing action.

        Args:
            thought: The reasoning from the think step
            input_data: Original input data

        Returns:
            Processed text result
        """
        if isinstance(input_data, dict):
            content = input_data.get("content", "")
        else:
            content = str(input_data)

        # Execute based on task type
        if self.task_type == "summarize":
            return self._summarize(content)
        elif self.task_type == "rewrite":
            return self._rewrite(content)
        elif self.task_type == "generate":
            return self._generate(content)
        else:
            return self._process(content)

    def _summarize(self, text: str) -> str:
        """Summarize text (placeholder implementation)."""
        # TODO: Implement actual AI summarization
        return f"Summary: {text[:200]}... [AI summarization would go here]"

    def _rewrite(self, text: str) -> str:
        """Rewrite text (placeholder implementation)."""
        # TODO: Implement actual AI rewriting
        return f"Rewritten: {text} [AI rewriting would go here]"

    def _generate(self, prompt: str) -> str:
        """Generate text (placeholder implementation)."""
        # TODO: Implement actual AI generation
        return f"Generated text based on prompt: '{prompt}' [AI generation would go here] DONE"

    def _process(self, text: str) -> str:
        """Process text (placeholder implementation)."""
        # TODO: Implement actual AI processing
        return f"Processed: {text} [AI processing would go here] DONE"
