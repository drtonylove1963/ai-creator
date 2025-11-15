"""
Tests for the AgentManager.
"""

import pytest
from ai_creator.agents import (
    AgentManager,
    TextAgent,
    ImageAgent,
    AnalysisAgent,
    AgentStatus,
)


class TestAgentManager:
    """Test cases for AgentManager."""

    def test_manager_creation(self):
        """Test creating an agent manager."""
        manager = AgentManager()
        assert manager is not None
        assert len(manager.list_agents()) == 0

    def test_register_agent(self):
        """Test registering an agent."""
        manager = AgentManager()
        agent = TextAgent(name="TestAgent")

        manager.register_agent(agent)
        assert "TestAgent" in manager.list_agents()
        assert manager.get_agent("TestAgent") == agent

    def test_register_multiple_agents(self):
        """Test registering multiple agents."""
        manager = AgentManager()
        agent1 = TextAgent(name="Agent1")
        agent2 = ImageAgent(name="Agent2")
        agent3 = AnalysisAgent(name="Agent3")

        manager.register_agent(agent1)
        manager.register_agent(agent2)
        manager.register_agent(agent3)

        agents = manager.list_agents()
        assert len(agents) == 3
        assert "Agent1" in agents
        assert "Agent2" in agents
        assert "Agent3" in agents

    def test_unregister_agent(self):
        """Test unregistering an agent."""
        manager = AgentManager()
        agent = TextAgent(name="TestAgent")

        manager.register_agent(agent)
        assert "TestAgent" in manager.list_agents()

        result = manager.unregister_agent("TestAgent")
        assert result is True
        assert "TestAgent" not in manager.list_agents()

    def test_unregister_nonexistent_agent(self):
        """Test unregistering a non-existent agent."""
        manager = AgentManager()
        result = manager.unregister_agent("NonExistent")
        assert result is False

    def test_get_agent(self):
        """Test getting an agent by name."""
        manager = AgentManager()
        agent = TextAgent(name="TestAgent")
        manager.register_agent(agent)

        retrieved_agent = manager.get_agent("TestAgent")
        assert retrieved_agent == agent

    def test_get_nonexistent_agent(self):
        """Test getting a non-existent agent."""
        manager = AgentManager()
        agent = manager.get_agent("NonExistent")
        assert agent is None

    def test_run_agent(self):
        """Test running an agent."""
        manager = AgentManager()
        agent = TextAgent(name="TestAgent")
        manager.register_agent(agent)

        response = manager.run_agent("TestAgent", "Test input")
        assert response.agent_name == "TestAgent"
        assert response.status == AgentStatus.COMPLETED

    def test_run_nonexistent_agent(self):
        """Test running a non-existent agent raises error."""
        manager = AgentManager()

        with pytest.raises(ValueError, match="Agent 'NonExistent' not found"):
            manager.run_agent("NonExistent", "Test input")

    def test_run_sequential(self):
        """Test running agents sequentially."""
        manager = AgentManager()
        agent1 = TextAgent(name="Agent1")
        agent2 = TextAgent(name="Agent2")

        manager.register_agent(agent1)
        manager.register_agent(agent2)

        responses = manager.run_sequential(
            agent_names=["Agent1", "Agent2"],
            input_data="Test input"
        )

        assert len(responses) == 2
        assert responses[0].agent_name == "Agent1"
        assert responses[1].agent_name == "Agent2"

    def test_run_sequential_with_output_passing(self):
        """Test sequential execution with output passing."""
        manager = AgentManager()
        agent1 = TextAgent(name="Agent1")
        agent2 = AnalysisAgent(name="Agent2")

        manager.register_agent(agent1)
        manager.register_agent(agent2)

        responses = manager.run_sequential(
            agent_names=["Agent1", "Agent2"],
            input_data="Test input",
            pass_output=True
        )

        assert len(responses) == 2
        # Second agent should receive output from first agent
        assert responses[1].status == AgentStatus.COMPLETED

    def test_run_parallel(self):
        """Test running agents in parallel."""
        manager = AgentManager()
        agent1 = TextAgent(name="Agent1")
        agent2 = ImageAgent(name="Agent2")
        agent3 = AnalysisAgent(name="Agent3")

        manager.register_agent(agent1)
        manager.register_agent(agent2)
        manager.register_agent(agent3)

        responses = manager.run_parallel(
            agent_names=["Agent1", "Agent2", "Agent3"],
            input_data="Shared input"
        )

        assert len(responses) == 3
        # All agents should complete
        for response in responses:
            assert response.status == AgentStatus.COMPLETED

    def test_collaborate(self):
        """Test agent collaboration."""
        manager = AgentManager()
        agent1 = TextAgent(name="Agent1")
        agent2 = AnalysisAgent(name="Agent2")

        manager.register_agent(agent1)
        manager.register_agent(agent2)

        result = manager.collaborate(
            task="Create and analyze content",
            agent_names=["Agent1", "Agent2"],
            max_rounds=2
        )

        assert "task" in result
        assert "rounds" in result
        assert "collaboration_log" in result
        assert result["rounds"] <= 2

    def test_execution_history(self):
        """Test execution history tracking."""
        manager = AgentManager()
        agent = TextAgent(name="TestAgent")
        manager.register_agent(agent)

        # Run agent multiple times
        manager.run_agent("TestAgent", "Input 1")
        manager.run_agent("TestAgent", "Input 2")

        history = manager.get_execution_history()
        assert len(history) == 2
        assert history[0]["agent_name"] == "TestAgent"
        assert history[0]["input"] == "Input 1"

    def test_clear_history(self):
        """Test clearing execution history."""
        manager = AgentManager()
        agent = TextAgent(name="TestAgent")
        manager.register_agent(agent)

        manager.run_agent("TestAgent", "Input")
        assert len(manager.get_execution_history()) > 0

        manager.clear_history()
        assert len(manager.get_execution_history()) == 0

    def test_reset_all_agents(self):
        """Test resetting all agents."""
        manager = AgentManager()
        agent1 = TextAgent(name="Agent1")
        agent2 = TextAgent(name="Agent2")

        manager.register_agent(agent1)
        manager.register_agent(agent2)

        # Run agents
        manager.run_agent("Agent1", "Input")
        manager.run_agent("Agent2", "Input")

        # Agents should have memory
        assert len(agent1.get_memory()) > 0
        assert len(agent2.get_memory()) > 0

        # Reset all
        manager.reset_all_agents()

        # Memory should be cleared
        assert len(agent1.get_memory()) == 0
        assert len(agent2.get_memory()) == 0
        assert agent1.status == AgentStatus.IDLE
        assert agent2.status == AgentStatus.IDLE


class TestAgentCoordination:
    """Test complex agent coordination scenarios."""

    def test_multi_agent_workflow(self):
        """Test a complex multi-agent workflow."""
        manager = AgentManager()

        writer = TextAgent(name="Writer")
        analyzer = AnalysisAgent(name="Analyzer")

        manager.register_agent(writer)
        manager.register_agent(analyzer)

        # Step 1: Writer creates content
        write_response = manager.run_agent("Writer", "Create a product description")
        assert write_response.status == AgentStatus.COMPLETED

        # Step 2: Analyzer analyzes the content
        analyze_response = manager.run_agent(
            "Analyzer",
            {"type": "general", "content": write_response.content}
        )
        assert analyze_response.status == AgentStatus.COMPLETED

        # Check history
        history = manager.get_execution_history()
        assert len(history) == 2

    def test_agent_collaboration_rounds(self):
        """Test multiple collaboration rounds."""
        manager = AgentManager()
        agent1 = TextAgent(name="Agent1")
        agent2 = TextAgent(name="Agent2")

        manager.register_agent(agent1)
        manager.register_agent(agent2)

        result = manager.collaborate(
            task="Collaborative writing",
            agent_names=["Agent1", "Agent2"],
            max_rounds=3
        )

        # Should have collaboration log for each round
        assert len(result["collaboration_log"]) <= 3
        assert "final_results" in result
