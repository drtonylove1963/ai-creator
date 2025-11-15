"""
Agent Manager examples for orchestrating multiple agents.

This script demonstrates how to use AgentManager to coordinate
multiple agents working together.
"""

from ai_creator import AgentManager, TextAgent, ImageAgent, AnalysisAgent


def example_sequential_agents():
    """Example of running agents sequentially."""
    print("\n" + "=" * 60)
    print("Example 1: Sequential Agent Execution")
    print("=" * 60)

    # Create agent manager
    manager = AgentManager()

    # Create and register agents
    text_agent = TextAgent(name="TextAgent")
    analysis_agent = AnalysisAgent(name="AnalysisAgent")

    manager.register_agent(text_agent)
    manager.register_agent(analysis_agent)

    print(f"Registered agents: {manager.list_agents()}")

    # Run agents sequentially
    print("\nRunning agents sequentially...")
    initial_input = "Create a short story about a robot learning to paint"

    responses = manager.run_sequential(
        agent_names=["TextAgent", "AnalysisAgent"],
        input_data=initial_input,
        pass_output=True  # Pass output from one agent to the next
    )

    for i, response in enumerate(responses, 1):
        print(f"\n--- Agent {i}: {response.agent_name} ---")
        print(f"Status: {response.status.value}")
        print(f"Result: {response.content}")


def example_parallel_agents():
    """Example of running agents in parallel."""
    print("\n" + "=" * 60)
    print("Example 2: Parallel Agent Execution")
    print("=" * 60)

    # Create agent manager
    manager = AgentManager()

    # Create and register multiple agents
    text_agent = TextAgent(name="TextAgent")
    image_agent = ImageAgent(name="ImageAgent")
    analysis_agent = AnalysisAgent(name="AnalysisAgent")

    manager.register_agent(text_agent)
    manager.register_agent(image_agent)
    manager.register_agent(analysis_agent)

    # Run agents in parallel with the same input
    print("\nRunning agents in parallel with same input...")
    shared_input = "A beautiful sunset over the ocean"

    responses = manager.run_parallel(
        agent_names=["TextAgent", "ImageAgent", "AnalysisAgent"],
        input_data=shared_input
    )

    for response in responses:
        print(f"\n--- {response.agent_name} ---")
        print(f"Status: {response.status.value}")
        print(f"Iterations: {response.iterations}")
        print(f"Result: {response.content}")


def example_agent_collaboration():
    """Example of agents collaborating on a task."""
    print("\n" + "=" * 60)
    print("Example 3: Multi-Agent Collaboration")
    print("=" * 60)

    # Create agent manager
    manager = AgentManager()

    # Create specialized agents
    text_agent = TextAgent(name="ContentCreator")
    analysis_agent = AnalysisAgent(name="ContentAnalyzer")
    image_agent = ImageAgent(name="VisualDesigner")

    manager.register_agent(text_agent)
    manager.register_agent(analysis_agent)
    manager.register_agent(image_agent)

    # Agents collaborate on creating a marketing campaign
    print("\nTask: Create a marketing campaign for an eco-friendly water bottle")
    result = manager.collaborate(
        task="Create a marketing campaign for an eco-friendly water bottle",
        agent_names=["ContentCreator", "ContentAnalyzer", "VisualDesigner"],
        max_rounds=2
    )

    print(f"\nCollaboration completed in {result['rounds']} rounds")
    print(f"\nFinal results:")
    for agent_result in result["final_results"]:
        print(f"\n--- {agent_result['agent']} ---")
        print(f"Status: {agent_result['response']['status']}")
        if agent_result['response']['content']:
            print(f"Contribution: {agent_result['response']['content']}")


def example_custom_workflow():
    """Example of a custom multi-agent workflow."""
    print("\n" + "=" * 60)
    print("Example 4: Custom Multi-Agent Workflow")
    print("=" * 60)

    manager = AgentManager()

    # Register agents
    manager.register_agent(TextAgent(name="Writer"))
    manager.register_agent(AnalysisAgent(name="Editor"))
    manager.register_agent(TextAgent(name="Refiner"))

    # Custom workflow: Write -> Analyze -> Refine
    print("\nWorkflow: Writer -> Editor -> Refiner")

    # Step 1: Writer creates content
    print("\n1. Writer creates initial content...")
    response1 = manager.run_agent(
        "Writer",
        {"task": "generate", "content": "Write about the benefits of AI"}
    )
    print(f"Writer output: {response1.content}")

    # Step 2: Editor analyzes the content
    print("\n2. Editor analyzes the content...")
    response2 = manager.run_agent(
        "Editor",
        {"type": "general", "content": response1.content}
    )
    print(f"Editor analysis: {response2.content}")

    # Step 3: Refiner improves based on analysis
    print("\n3. Refiner improves the content...")
    response3 = manager.run_agent(
        "Refiner",
        {
            "task": "rewrite",
            "content": response1.content,
            "improvements": response2.content
        }
    )
    print(f"Refined output: {response3.content}")

    # View execution history
    print("\n" + "-" * 60)
    print("Execution History:")
    history = manager.get_execution_history()
    for i, entry in enumerate(history, 1):
        print(f"{i}. {entry['agent_name']} executed")


def main():
    """Run all agent manager examples."""
    print("AI Creator - Agent Manager Examples")
    print("=" * 60)

    example_sequential_agents()
    example_parallel_agents()
    example_agent_collaboration()
    example_custom_workflow()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
