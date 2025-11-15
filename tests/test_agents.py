"""
Tests for the agent system.
"""

import pytest
from ai_creator.agents import (
    Agent,
    AgentConfig,
    AgentResponse,
    AgentStatus,
    TextAgent,
    ImageAgent,
    AnalysisAgent,
)


class TestAgentConfig:
    """Test cases for AgentConfig."""

    def test_agent_config_creation(self):
        """Test creating an agent configuration."""
        config = AgentConfig(
            name="TestAgent",
            description="Test agent",
            model="test-model",
            temperature=0.5,
        )
        assert config.name == "TestAgent"
        assert config.description == "Test agent"
        assert config.model == "test-model"
        assert config.temperature == 0.5

    def test_agent_config_defaults(self):
        """Test default values in agent configuration."""
        config = AgentConfig(name="TestAgent")
        assert config.description == ""
        assert config.model == "default"
        assert config.temperature == 0.7
        assert config.max_iterations == 10
        assert config.memory_enabled is True


class TestTextAgent:
    """Test cases for TextAgent."""

    def test_text_agent_creation(self):
        """Test creating a text agent."""
        agent = TextAgent(name="TestTextAgent")
        assert agent.config.name == "TestTextAgent"
        assert agent.status == AgentStatus.IDLE

    def test_text_agent_generation(self):
        """Test text generation."""
        agent = TextAgent()
        response = agent.run("Generate a greeting")

        assert response.agent_name == "TextAgent"
        assert response.status == AgentStatus.COMPLETED
        assert response.content is not None
        assert response.iterations > 0

    def test_text_agent_with_task(self):
        """Test text agent with specific task."""
        agent = TextAgent()
        task = {
            "task": "generate",
            "content": "Write a haiku about AI"
        }
        response = agent.run(task)

        assert response.status == AgentStatus.COMPLETED
        assert len(response.thoughts) > 0
        assert len(response.actions) > 0

    def test_text_agent_summarize(self):
        """Test text summarization."""
        agent = TextAgent()
        task = {
            "task": "summarize",
            "content": "This is a long piece of text that needs to be summarized..."
        }
        response = agent.run(task)

        assert response.status == AgentStatus.COMPLETED
        assert "Summary" in str(response.content)

    def test_text_agent_memory(self):
        """Test that agent stores memory."""
        agent = TextAgent()
        agent.run("Test task 1")
        agent.run("Test task 2")

        memory = agent.get_memory()
        assert len(memory) >= 2

    def test_text_agent_reset(self):
        """Test agent reset."""
        agent = TextAgent()
        agent.run("Test task")
        agent.reset()

        assert agent.status == AgentStatus.IDLE
        assert len(agent.get_memory()) == 0
        assert agent.iteration_count == 0


class TestImageAgent:
    """Test cases for ImageAgent."""

    def test_image_agent_creation(self):
        """Test creating an image agent."""
        agent = ImageAgent(name="TestImageAgent")
        assert agent.config.name == "TestImageAgent"
        assert agent.status == AgentStatus.IDLE

    def test_image_agent_generation(self):
        """Test image generation."""
        agent = ImageAgent()
        task = {
            "task": "generate",
            "description": "A sunset over mountains"
        }
        response = agent.run(task)

        assert response.status == AgentStatus.COMPLETED
        assert isinstance(response.content, dict)
        assert response.content["type"] == "generated_image"

    def test_image_agent_with_params(self):
        """Test image generation with parameters."""
        agent = ImageAgent()
        task = {
            "task": "generate",
            "description": "Abstract art",
            "params": {"style": "modern", "colors": ["blue", "red"]}
        }
        response = agent.run(task)

        assert response.status == AgentStatus.COMPLETED
        assert "params" in response.content

    def test_image_agent_analysis(self):
        """Test image analysis."""
        agent = ImageAgent()
        task = {
            "task": "analyze",
            "description": "image_ref_123"
        }
        response = agent.run(task)

        assert response.status == AgentStatus.COMPLETED
        assert response.content["type"] == "image_analysis"
        assert "analysis" in response.content


class TestAnalysisAgent:
    """Test cases for AnalysisAgent."""

    def test_analysis_agent_creation(self):
        """Test creating an analysis agent."""
        agent = AnalysisAgent(name="TestAnalysisAgent")
        assert agent.config.name == "TestAnalysisAgent"
        assert agent.status == AgentStatus.IDLE

    def test_sentiment_analysis(self):
        """Test sentiment analysis."""
        agent = AnalysisAgent()
        task = {
            "type": "sentiment",
            "content": "This is great! I love it!"
        }
        response = agent.run(task)

        assert response.status == AgentStatus.COMPLETED
        assert response.content["type"] == "sentiment_analysis"
        assert "sentiment" in response.content

    def test_entity_extraction(self):
        """Test entity extraction."""
        agent = AnalysisAgent()
        task = {
            "type": "entities",
            "content": "Apple Inc. announced new products in California."
        }
        response = agent.run(task)

        assert response.status == AgentStatus.COMPLETED
        assert response.content["type"] == "entity_extraction"
        assert "entities" in response.content

    def test_topic_identification(self):
        """Test topic identification."""
        agent = AnalysisAgent()
        task = {
            "type": "topics",
            "content": "Technology is changing rapidly..."
        }
        response = agent.run(task)

        assert response.status == AgentStatus.COMPLETED
        assert response.content["type"] == "topic_identification"
        assert "topics" in response.content

    def test_general_analysis(self):
        """Test general analysis."""
        agent = AnalysisAgent()
        task = {
            "type": "general",
            "content": "Some content to analyze"
        }
        response = agent.run(task)

        assert response.status == AgentStatus.COMPLETED
        assert "insights" in response.content


class TestAgentResponse:
    """Test cases for AgentResponse."""

    def test_agent_response_to_dict(self):
        """Test converting response to dictionary."""
        agent = TextAgent()
        response = agent.run("Test")

        response_dict = response.to_dict()
        assert isinstance(response_dict, dict)
        assert "agent_name" in response_dict
        assert "content" in response_dict
        assert "status" in response_dict
        assert "iterations" in response_dict
        assert "thoughts" in response_dict
        assert "actions" in response_dict


class TestAgentConfiguration:
    """Test agent configuration and customization."""

    def test_custom_max_iterations(self):
        """Test custom max iterations."""
        config = AgentConfig(name="Test", max_iterations=3)
        agent = TextAgent(name=config.name, max_iterations=3)

        # Agent should stop after max_iterations
        response = agent.run("Test")
        assert response.iterations <= 3

    def test_memory_disabled(self):
        """Test agent with memory disabled."""
        config = AgentConfig(name="Test", memory_enabled=False)

        class TestAgent(Agent):
            def think(self, input_data):
                return "thinking"
            def act(self, thought, input_data):
                return "done DONE"

        agent = TestAgent(config)
        agent.run("Test")

        # Memory should be empty when disabled
        assert len(agent.get_memory()) == 0
