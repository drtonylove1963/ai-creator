"""
Basic agent usage examples for AI Creator.

This script demonstrates how to create and use individual agents.
"""

from ai_creator import TextAgent, ImageAgent, AnalysisAgent, AgentConfig


def example_text_agent():
    """Example using TextAgent for text generation."""
    print("\n" + "=" * 60)
    print("Example 1: Text Generation Agent")
    print("=" * 60)

    # Create a text agent
    text_agent = TextAgent(name="MyTextAgent")

    # Generate text
    prompt = "Create a short poem about artificial intelligence"
    response = text_agent.run({"task": "generate", "content": prompt})

    print(f"\nAgent: {response.agent_name}")
    print(f"Status: {response.status.value}")
    print(f"Iterations: {response.iterations}")
    print(f"\nThoughts:")
    for i, thought in enumerate(response.thoughts, 1):
        print(f"  {i}. {thought}")
    print(f"\nResult: {response.content}")


def example_image_agent():
    """Example using ImageAgent for image generation."""
    print("\n" + "=" * 60)
    print("Example 2: Image Generation Agent")
    print("=" * 60)

    # Create an image agent with custom configuration
    config = AgentConfig(
        name="MyImageAgent",
        description="Specialized image generation agent",
        temperature=0.8,
    )
    image_agent = ImageAgent(name=config.name)

    # Generate an image
    image_task = {
        "task": "generate",
        "description": "A futuristic city with flying cars at sunset",
        "params": {"style": "cyberpunk", "resolution": "1024x1024"}
    }
    response = image_agent.run(image_task)

    print(f"\nAgent: {response.agent_name}")
    print(f"Status: {response.status.value}")
    print(f"Iterations: {response.iterations}")
    print(f"\nResult: {response.content}")


def example_analysis_agent():
    """Example using AnalysisAgent for content analysis."""
    print("\n" + "=" * 60)
    print("Example 3: Analysis Agent")
    print("=" * 60)

    # Create an analysis agent
    analysis_agent = AnalysisAgent(name="MyAnalysisAgent")

    # Analyze sentiment
    analysis_task = {
        "type": "sentiment",
        "content": "This is an amazing product! I absolutely love it. Highly recommended!"
    }
    response = analysis_agent.run(analysis_task)

    print(f"\nAgent: {response.agent_name}")
    print(f"Status: {response.status.value}")
    print(f"\nAnalysis Result:")
    print(response.content)

    # Extract entities
    print("\n" + "-" * 60)
    entity_task = {
        "type": "entities",
        "content": "Apple Inc. CEO Tim Cook announced the new iPhone in Cupertino on September 12, 2023."
    }
    response = analysis_agent.run(entity_task)
    print("\nEntity Extraction Result:")
    print(response.content)


def example_agent_memory():
    """Example demonstrating agent memory capabilities."""
    print("\n" + "=" * 60)
    print("Example 4: Agent Memory")
    print("=" * 60)

    # Create agent with memory enabled
    agent = TextAgent(name="MemoryAgent")

    # Run multiple tasks
    tasks = [
        "Generate a product name for a smart watch",
        "Generate a tagline for this product",
        "Generate a description for this product",
    ]

    for i, task in enumerate(tasks, 1):
        print(f"\nTask {i}: {task}")
        response = agent.run(task)
        print(f"Result: {response.content}")

    # Check agent's memory
    print("\n" + "-" * 60)
    print("Agent Memory:")
    memory = agent.get_memory()
    for i, entry in enumerate(memory, 1):
        print(f"\n{i}. Timestamp: {entry['timestamp']}")
        print(f"   Input: {entry['input']}")
        print(f"   Thought: {entry['thought']}")
        print(f"   Result: {entry['result'][:100]}...")


def main():
    """Run all agent examples."""
    print("AI Creator - Agent System Examples")
    print("=" * 60)

    example_text_agent()
    example_image_agent()
    example_analysis_agent()
    example_agent_memory()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
