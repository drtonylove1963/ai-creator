"""
Tests for agent tools.
"""

import pytest
from ai_creator.agents.tools import (
    Tool,
    ToolRegistry,
    text_length,
    word_count,
    extract_keywords,
    format_json,
    calculate,
    default_registry,
)


class TestToolFunctions:
    """Test individual tool functions."""

    def test_text_length(self):
        """Test text length calculation."""
        assert text_length("hello") == 5
        assert text_length("") == 0
        assert text_length("hello world") == 11

    def test_word_count(self):
        """Test word counting."""
        assert word_count("hello world") == 2
        assert word_count("one") == 1
        assert word_count("") == 1  # split() returns ['']
        assert word_count("one two three four") == 4

    def test_extract_keywords(self):
        """Test keyword extraction."""
        text = "python programming language python code development"
        keywords = extract_keywords(text, top_n=3)

        assert isinstance(keywords, list)
        assert len(keywords) <= 3
        assert "python" in keywords  # Should be most frequent

    def test_extract_keywords_custom_count(self):
        """Test keyword extraction with custom count."""
        text = "artificial intelligence machine learning deep learning neural networks"
        keywords = extract_keywords(text, top_n=2)

        assert len(keywords) <= 2

    def test_format_json(self):
        """Test JSON formatting."""
        data = {"key": "value", "number": 42}
        result = format_json(data)

        assert isinstance(result, str)
        assert "key" in result
        assert "value" in result

    def test_format_json_custom_indent(self):
        """Test JSON formatting with custom indent."""
        data = {"test": "data"}
        result = format_json(data, indent=4)

        assert isinstance(result, str)
        assert "    " in result  # Should have 4-space indent

    def test_calculate_basic(self):
        """Test basic calculations."""
        assert calculate("2 + 2") == 4
        assert calculate("10 - 5") == 5
        assert calculate("3 * 4") == 12
        assert calculate("15 / 3") == 5

    def test_calculate_complex(self):
        """Test complex calculations."""
        assert calculate("(2 + 3) * 4") == 20
        assert calculate("10 + 5 * 2") == 20

    def test_calculate_invalid(self):
        """Test that invalid expressions raise errors."""
        with pytest.raises(ValueError):
            calculate("import os")  # Should reject non-math code

        with pytest.raises(ValueError):
            calculate("print('hello')")  # Should reject non-math code


class TestTool:
    """Test Tool class."""

    def test_tool_creation(self):
        """Test creating a tool."""
        def test_func(x: int) -> int:
            return x * 2

        tool = Tool(
            name="test_tool",
            description="Test tool",
            function=test_func,
            parameters={"x": "integer"}
        )

        assert tool.name == "test_tool"
        assert tool.description == "Test tool"
        assert tool.function(5) == 10


class TestToolRegistry:
    """Test ToolRegistry class."""

    def test_registry_creation(self):
        """Test creating a tool registry."""
        registry = ToolRegistry()
        assert len(registry.list_tools()) == 0

    def test_register_tool(self):
        """Test registering a tool."""
        registry = ToolRegistry()

        def my_func(x: str) -> str:
            return x.upper()

        tool = Tool(
            name="uppercase",
            description="Convert to uppercase",
            function=my_func,
            parameters={"x": "string"}
        )

        registry.register(tool)
        assert "uppercase" in registry.list_tools()

    def test_get_tool(self):
        """Test getting a tool."""
        registry = ToolRegistry()

        def my_func(x: int) -> int:
            return x + 1

        tool = Tool(
            name="increment",
            description="Increment by 1",
            function=my_func,
            parameters={"x": "integer"}
        )

        registry.register(tool)
        retrieved_tool = registry.get("increment")

        assert retrieved_tool == tool
        assert retrieved_tool.function(5) == 6

    def test_get_nonexistent_tool(self):
        """Test getting a non-existent tool raises error."""
        registry = ToolRegistry()

        with pytest.raises(KeyError, match="Tool 'nonexistent' not found"):
            registry.get("nonexistent")

    def test_execute_tool(self):
        """Test executing a tool."""
        registry = ToolRegistry()

        def multiply(a: int, b: int) -> int:
            return a * b

        tool = Tool(
            name="multiply",
            description="Multiply two numbers",
            function=multiply,
            parameters={"a": "integer", "b": "integer"}
        )

        registry.register(tool)
        result = registry.execute("multiply", a=3, b=4)

        assert result == 12

    def test_list_tools(self):
        """Test listing tools."""
        registry = ToolRegistry()

        tool1 = Tool("tool1", "desc1", lambda: None, {})
        tool2 = Tool("tool2", "desc2", lambda: None, {})

        registry.register(tool1)
        registry.register(tool2)

        tools = registry.list_tools()
        assert len(tools) == 2
        assert "tool1" in tools
        assert "tool2" in tools

    def test_get_tool_info(self):
        """Test getting tool information."""
        registry = ToolRegistry()

        tool = Tool(
            name="test",
            description="A test tool",
            function=lambda x: x,
            parameters={"x": "any"}
        )

        registry.register(tool)
        info = registry.get_tool_info("test")

        assert info["name"] == "test"
        assert info["description"] == "A test tool"
        assert info["parameters"] == {"x": "any"}


class TestDefaultRegistry:
    """Test the default tool registry."""

    def test_default_registry_has_tools(self):
        """Test that default registry has built-in tools."""
        tools = default_registry.list_tools()

        assert "text_length" in tools
        assert "word_count" in tools
        assert "extract_keywords" in tools
        assert "format_json" in tools
        assert "calculate" in tools

    def test_use_default_registry_tools(self):
        """Test using tools from default registry."""
        # Text length
        result = default_registry.execute("text_length", text="hello")
        assert result == 5

        # Word count
        result = default_registry.execute("word_count", text="hello world")
        assert result == 2

        # Calculate
        result = default_registry.execute("calculate", expression="5 + 3")
        assert result == 8

    def test_default_registry_tool_info(self):
        """Test getting info about default tools."""
        info = default_registry.get_tool_info("text_length")

        assert info["name"] == "text_length"
        assert "length" in info["description"].lower()
        assert "text" in info["parameters"]
