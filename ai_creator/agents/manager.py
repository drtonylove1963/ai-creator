"""
Agent Manager for orchestrating multiple agents.
"""

from typing import Any, Dict, List, Optional
from ai_creator.agents.base import Agent, AgentResponse, AgentStatus


class AgentManager:
    """
    Manages and orchestrates multiple agents.

    The AgentManager can:
    - Register and manage multiple agents
    - Route tasks to appropriate agents
    - Coordinate multi-agent collaboration
    - Aggregate results from multiple agents
    """

    def __init__(self):
        """Initialize the agent manager."""
        self.agents: Dict[str, Agent] = {}
        self.execution_history: List[Dict[str, Any]] = []

    def register_agent(self, agent: Agent) -> None:
        """
        Register an agent with the manager.

        Args:
            agent: Agent to register
        """
        self.agents[agent.config.name] = agent

    def unregister_agent(self, agent_name: str) -> bool:
        """
        Unregister an agent from the manager.

        Args:
            agent_name: Name of the agent to unregister

        Returns:
            True if unregistered, False if not found
        """
        if agent_name in self.agents:
            del self.agents[agent_name]
            return True
        return False

    def get_agent(self, agent_name: str) -> Optional[Agent]:
        """
        Get an agent by name.

        Args:
            agent_name: Name of the agent

        Returns:
            Agent instance or None if not found
        """
        return self.agents.get(agent_name)

    def list_agents(self) -> List[str]:
        """
        List all registered agents.

        Returns:
            List of agent names
        """
        return list(self.agents.keys())

    def run_agent(
        self,
        agent_name: str,
        input_data: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Run a specific agent.

        Args:
            agent_name: Name of the agent to run
            input_data: Input data for the agent
            context: Optional context information

        Returns:
            Agent response

        Raises:
            ValueError: If agent not found
        """
        agent = self.get_agent(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found")

        response = agent.run(input_data, context)

        # Store in execution history
        self.execution_history.append({
            "agent_name": agent_name,
            "input": input_data,
            "response": response.to_dict(),
        })

        return response

    def run_sequential(
        self,
        agent_names: List[str],
        input_data: Any,
        pass_output: bool = True
    ) -> List[AgentResponse]:
        """
        Run multiple agents sequentially.

        Args:
            agent_names: List of agent names to run in order
            input_data: Initial input data
            pass_output: If True, pass each agent's output to the next agent

        Returns:
            List of agent responses
        """
        responses = []
        current_input = input_data

        for agent_name in agent_names:
            response = self.run_agent(agent_name, current_input)
            responses.append(response)

            if pass_output and response.content:
                current_input = response.content

        return responses

    def run_parallel(
        self,
        agent_names: List[str],
        input_data: Any
    ) -> List[AgentResponse]:
        """
        Run multiple agents in parallel (simulated - actual parallel execution
        would require async/threading).

        Args:
            agent_names: List of agent names to run
            input_data: Input data for all agents

        Returns:
            List of agent responses
        """
        responses = []

        for agent_name in agent_names:
            response = self.run_agent(agent_name, input_data)
            responses.append(response)

        return responses

    def collaborate(
        self,
        task: str,
        agent_names: Optional[List[str]] = None,
        max_rounds: int = 3
    ) -> Dict[str, Any]:
        """
        Agents collaborate on a task through multiple rounds of interaction.

        Args:
            task: The task to accomplish
            agent_names: Agents to participate (all if None)
            max_rounds: Maximum collaboration rounds

        Returns:
            Collaboration results including all agent outputs
        """
        if agent_names is None:
            agent_names = self.list_agents()

        collaboration_log = []
        current_context = {"task": task, "round": 0}

        for round_num in range(max_rounds):
            current_context["round"] = round_num + 1
            round_results = []

            for agent_name in agent_names:
                # Prepare input with context from previous agents
                agent_input = {
                    "task": task,
                    "previous_results": collaboration_log,
                    "round": round_num + 1,
                }

                response = self.run_agent(agent_name, agent_input, current_context)
                round_results.append({
                    "agent": agent_name,
                    "response": response.to_dict(),
                })

            collaboration_log.append({
                "round": round_num + 1,
                "results": round_results,
            })

            # Check if task is complete
            if self._is_task_complete(round_results):
                break

        return {
            "task": task,
            "rounds": len(collaboration_log),
            "collaboration_log": collaboration_log,
            "final_results": collaboration_log[-1]["results"] if collaboration_log else [],
        }

    def _is_task_complete(self, round_results: List[Dict[str, Any]]) -> bool:
        """
        Check if the collaborative task is complete.

        Args:
            round_results: Results from the current round

        Returns:
            True if task is complete
        """
        # Task is complete if all agents report COMPLETED status
        return all(
            result["response"]["status"] == AgentStatus.COMPLETED.value
            for result in round_results
        )

    def get_execution_history(self) -> List[Dict[str, Any]]:
        """
        Get the execution history.

        Returns:
            List of execution records
        """
        return self.execution_history.copy()

    def clear_history(self) -> None:
        """Clear execution history."""
        self.execution_history.clear()

    def reset_all_agents(self) -> None:
        """Reset all registered agents to their initial state."""
        for agent in self.agents.values():
            agent.reset()
