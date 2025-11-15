"""
Tools that agents can use to perform various tasks.
"""

from typing import Any, Dict, List, Callable
from dataclasses import dataclass


@dataclass
class Tool:
    """Definition of a tool that an agent can use."""
    name: str
    description: str
    function: Callable
    parameters: Dict[str, Any]


class ToolRegistry:
    """
    Registry for managing tools available to agents.
    """

    def __init__(self):
        """Initialize the tool registry."""
        self.tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """
        Register a tool.

        Args:
            tool: Tool to register
        """
        self.tools[tool.name] = tool

    def get(self, tool_name: str) -> Tool:
        """
        Get a tool by name.

        Args:
            tool_name: Name of the tool

        Returns:
            Tool instance

        Raises:
            KeyError: If tool not found
        """
        if tool_name not in self.tools:
            raise KeyError(f"Tool '{tool_name}' not found")
        return self.tools[tool_name]

    def execute(self, tool_name: str, **kwargs) -> Any:
        """
        Execute a tool.

        Args:
            tool_name: Name of the tool
            **kwargs: Tool parameters

        Returns:
            Tool execution result
        """
        tool = self.get(tool_name)
        return tool.function(**kwargs)

    def list_tools(self) -> List[str]:
        """
        List all available tools.

        Returns:
            List of tool names
        """
        return list(self.tools.keys())

    def get_tool_info(self, tool_name: str) -> Dict[str, Any]:
        """
        Get information about a tool.

        Args:
            tool_name: Name of the tool

        Returns:
            Tool information
        """
        tool = self.get(tool_name)
        return {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters,
        }


# Default tool registry
default_registry = ToolRegistry()


# Built-in tools

def text_length(text: str) -> int:
    """
    Calculate text length.

    Args:
        text: Input text

    Returns:
        Length of text
    """
    return len(text)


def word_count(text: str) -> int:
    """
    Count words in text.

    Args:
        text: Input text

    Returns:
        Number of words
    """
    return len(text.split())


def extract_keywords(text: str, top_n: int = 5) -> List[str]:
    """
    Extract keywords from text (simple implementation).

    Args:
        text: Input text
        top_n: Number of top keywords to extract

    Returns:
        List of keywords
    """
    # Simple implementation - just return most common words
    words = text.lower().split()
    word_freq = {}
    for word in words:
        if len(word) > 3:  # Skip short words
            word_freq[word] = word_freq.get(word, 0) + 1

    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_words[:top_n]]


def format_json(data: Dict[str, Any], indent: int = 2) -> str:
    """
    Format data as JSON string.

    Args:
        data: Data to format
        indent: Indentation level

    Returns:
        JSON formatted string
    """
    import json
    return json.dumps(data, indent=indent)


def calculate(expression: str) -> float:
    """
    Safely evaluate a mathematical expression.

    Args:
        expression: Math expression to evaluate

    Returns:
        Result of calculation
    """
    # Simple safe evaluation (in production, use a proper parser)
    try:
        # Only allow numbers and basic operators
        allowed_chars = "0123456789+-*/()., "
        if all(c in allowed_chars for c in expression):
            return eval(expression)
        else:
            raise ValueError("Invalid characters in expression")
    except Exception as e:
        raise ValueError(f"Could not evaluate expression: {e}")


# Register default tools
default_registry.register(Tool(
    name="text_length",
    description="Calculate the length of text",
    function=text_length,
    parameters={"text": "string"}
))

default_registry.register(Tool(
    name="word_count",
    description="Count words in text",
    function=word_count,
    parameters={"text": "string"}
))

default_registry.register(Tool(
    name="extract_keywords",
    description="Extract keywords from text",
    function=extract_keywords,
    parameters={"text": "string", "top_n": "integer (optional, default=5)"}
))

default_registry.register(Tool(
    name="format_json",
    description="Format data as JSON",
    function=format_json,
    parameters={"data": "dict", "indent": "integer (optional, default=2)"}
))

default_registry.register(Tool(
    name="calculate",
    description="Evaluate a mathematical expression",
    function=calculate,
    parameters={"expression": "string"}
))
