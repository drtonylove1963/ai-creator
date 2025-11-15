"""
Skills system examples for AI Creator.

This script demonstrates how to use skills with agents.
"""

from ai_creator import TextAgent, AgentConfig, skill_registry, create_skill_template
from ai_creator.skills.builtin import (
    CodeGenerationSkill,
    SummarizationSkill,
    EmailWritingSkill,
    DataAnalysisSkill,
    register_all_builtin_skills,
)


def example_basic_skill_usage():
    """Example of using a skill directly."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Skill Usage")
    print("=" * 60)

    # Create a skill
    code_skill = CodeGenerationSkill()

    # Use the skill
    result = code_skill.run({
        "description": "Create a function to calculate factorial",
        "language": "python"
    })

    print(f"\nSkill: {result.skill_name}")
    print(f"Success: {result.success}")
    print(f"Execution time: {result.execution_time:.3f}s")
    print(f"\nGenerated Code:")
    print(result.output)

    # Get skill stats
    print(f"\n{code_skill.get_stats()}")


def example_agent_with_skills():
    """Example of agents using skills."""
    print("\n" + "=" * 60)
    print("Example 2: Agent with Skills")
    print("=" * 60)

    # Create an agent
    agent = TextAgent(name="SkillfulAgent")

    # Add skills to the agent
    agent.add_skill(CodeGenerationSkill())
    agent.add_skill(SummarizationSkill())
    agent.add_skill(EmailWritingSkill())

    print(f"\nAgent '{agent.config.name}' has skills:")
    for skill_name in agent.list_skills():
        print(f"  • {skill_name}")

    # Use a skill through the agent
    print("\n--- Using code_generation skill ---")
    skill_result = agent.use_skill(
        "code_generation",
        {"description": "Create a binary search function"}
    )

    print(f"Success: {skill_result.success}")
    print(f"Output: {skill_result.output[:200]}...")

    # Use another skill
    print("\n--- Using email_writing skill ---")
    email_result = agent.use_skill(
        "email_writing",
        {
            "subject": "Project Update",
            "context": "The new features are ready for review"
        }
    )

    print(f"Subject: {email_result.output['subject']}")
    print(f"Body preview: {email_result.output['body'][:150]}...")


def example_skill_registry():
    """Example of using the skill registry."""
    print("\n" + "=" * 60)
    print("Example 3: Skill Registry")
    print("=" * 60)

    # Register all built-in skills
    register_all_builtin_skills(skill_registry)

    # List all skills
    print(f"\nTotal skills registered: {len(skill_registry)}")
    print("\nSkills by category:")
    for category, skills in skill_registry.list_by_category().items():
        print(f"\n{category.upper()}:")
        for skill_name in skills:
            print(f"  • {skill_name}")

    # Get skill information
    print("\n--- Skill Information: code_generation ---")
    info = skill_registry.get_info("code_generation")
    for key, value in info.items():
        print(f"{key}: {value}")

    # Search for skills
    print("\n--- Search for 'data' skills ---")
    results = skill_registry.search("data")
    print(f"Found {len(results)} skills: {', '.join(results)}")

    # Execute a skill from registry
    print("\n--- Execute skill from registry ---")
    result = skill_registry.execute_skill(
        "data_analysis",
        "Sample dataset"
    )
    print(f"Success: {result.success}")
    print(f"Output: {result.output}")


def example_creating_custom_skill():
    """Example of creating a custom skill."""
    print("\n" + "=" * 60)
    print("Example 4: Creating Custom Skills")
    print("=" * 60)

    # Create a skill template
    template = create_skill_template(
        name="SentimentAnalysis",
        description="Analyze sentiment of text",
        category="analysis"
    )

    print("Skill template generated:")
    print(template[:500] + "...")

    # You can save this template to a file
    # create_skill_template(
    #     name="SentimentAnalysis",
    #     description="Analyze sentiment of text",
    #     category="analysis",
    #     output_path="my_custom_skill.py"
    # )

    print("\nTemplate saved! You can now:")
    print("1. Edit the generated file to implement your logic")
    print("2. Import and use your custom skill")
    print("3. Share your skill with others")


def example_skill_statistics():
    """Example of tracking skill statistics."""
    print("\n" + "=" * 60)
    print("Example 5: Skill Statistics")
    print("=" * 60)

    skill = DataAnalysisSkill()

    # Use the skill multiple times
    for i in range(5):
        result = skill.run(f"Dataset {i+1}")

    # Get statistics
    stats = skill.get_stats()
    print("\nSkill Performance Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


def example_skill_with_agent_workflow():
    """Example of complete workflow with agent and multiple skills."""
    print("\n" + "=" * 60)
    print("Example 6: Complete Workflow")
    print("=" * 60)

    # Create agent with research capabilities
    config = AgentConfig(
        name="ResearchAgent",
        description="Agent with research and communication skills",
        skills=["web_search", "summarization", "email_writing"]
    )
    agent = TextAgent(name=config.name)

    # Add multiple skills
    from ai_creator.skills.builtin import WebSearchSkill
    agent.add_skill(WebSearchSkill())
    agent.add_skill(SummarizationSkill())
    agent.add_skill(EmailWritingSkill())

    print(f"\n{agent.config.name} capabilities:")
    skill_info = agent.get_skill_info()
    for name, info in skill_info.items():
        print(f"  • {name}: {info['description']}")

    # Workflow: Search -> Summarize -> Email
    print("\n--- Workflow: Research and Report ---")

    # Step 1: Search
    print("\n1. Searching for information...")
    search_result = agent.use_skill("web_search", "latest AI developments")
    print(f"   Found {search_result.output['total_results']} results")

    # Step 2: Summarize
    print("\n2. Summarizing findings...")
    summary_result = agent.use_skill(
        "summarization",
        "Long text about AI developments..."
    )
    print(f"   Summary: {summary_result.output['summary']}")

    # Step 3: Create email
    print("\n3. Creating email report...")
    email_result = agent.use_skill(
        "email_writing",
        {
            "subject": "AI Research Summary",
            "context": "Here are the latest AI developments..."
        }
    )
    print(f"   Email created: {email_result.output['subject']}")

    print("\n✅ Workflow completed successfully!")


def main():
    """Run all skill examples."""
    print("AI Creator - Skills System Examples")
    print("=" * 60)

    example_basic_skill_usage()
    example_agent_with_skills()
    example_skill_registry()
    example_creating_custom_skill()
    example_skill_statistics()
    example_skill_with_agent_workflow()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
