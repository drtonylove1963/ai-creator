"""
Example of creating a custom agent.

This script demonstrates how to create your own specialized agent
by extending the base Agent class.
"""

from typing import Any
from ai_creator import Agent, AgentConfig, AgentManager


class ResearchAgent(Agent):
    """
    Custom agent that performs research tasks.

    This agent simulates a research process:
    1. Formulate research questions
    2. Gather information (simulated)
    3. Synthesize findings
    4. Draw conclusions
    """

    def __init__(self, name: str = "ResearchAgent", **kwargs):
        """Initialize the ResearchAgent."""
        config = AgentConfig(
            name=name,
            description="Agent for conducting research and synthesis",
            max_iterations=5,
            **kwargs
        )
        super().__init__(config)
        self.research_questions = []
        self.findings = []

    def think(self, input_data: Any) -> str:
        """Formulate research approach."""
        if isinstance(input_data, dict):
            topic = input_data.get("topic", "")
            depth = input_data.get("depth", "basic")
        else:
            topic = str(input_data)
            depth = "basic"

        # Generate research questions based on iteration
        iteration = self.iteration_count + 1

        if iteration == 1:
            thought = f"I need to research: {topic}. Starting with fundamental questions."
            self.research_questions.append(f"What is {topic}?")
        elif iteration == 2:
            thought = f"Expanding research on {topic}. Exploring applications."
            self.research_questions.append(f"How is {topic} used?")
        elif iteration == 3:
            thought = f"Deep dive into {topic}. Analyzing implications."
            self.research_questions.append(f"What are the implications of {topic}?")
        elif iteration == 4:
            thought = f"Synthesizing findings about {topic}."
        else:
            thought = f"Finalizing research on {topic}. DONE"

        return thought

    def act(self, thought: str, input_data: Any) -> Any:
        """Execute research actions."""
        if "DONE" in thought:
            # Synthesize all findings
            return self._synthesize_research()

        if isinstance(input_data, dict):
            topic = input_data.get("topic", "")
        else:
            topic = str(input_data)

        # Simulate gathering information
        iteration = self.iteration_count

        if iteration == 1:
            finding = f"Basic understanding: {topic} is a fundamental concept in AI."
            self.findings.append(finding)
        elif iteration == 2:
            finding = f"Applications: {topic} is applied in various domains including automation and analysis."
            self.findings.append(finding)
        elif iteration == 3:
            finding = f"Implications: {topic} has significant impact on technology and society."
            self.findings.append(finding)
        elif iteration == 4:
            finding = "Synthesis in progress..."
            self.findings.append(finding)

        return finding

    def _synthesize_research(self) -> dict:
        """Synthesize all research findings."""
        return {
            "topic": "Research Topic",
            "questions_explored": self.research_questions,
            "findings": self.findings,
            "conclusion": f"Based on {len(self.findings)} findings, research is complete.",
            "confidence": 0.85,
        }


class CodeGeneratorAgent(Agent):
    """
    Custom agent that generates code.

    This agent follows a structured approach to code generation:
    1. Understand requirements
    2. Plan the structure
    3. Generate code
    4. Add documentation
    """

    def __init__(self, name: str = "CodeGeneratorAgent", **kwargs):
        """Initialize the CodeGeneratorAgent."""
        config = AgentConfig(
            name=name,
            description="Agent for generating code",
            max_iterations=4,
            **kwargs
        )
        super().__init__(config)
        self.code_structure = []

    def think(self, input_data: Any) -> str:
        """Plan code generation approach."""
        if isinstance(input_data, dict):
            requirement = input_data.get("requirement", "")
            language = input_data.get("language", "python")
        else:
            requirement = str(input_data)
            language = "python"

        iteration = self.iteration_count + 1

        if iteration == 1:
            return f"Understanding requirement: {requirement}"
        elif iteration == 2:
            return f"Planning code structure for {language}"
        elif iteration == 3:
            return "Generating code implementation"
        else:
            return "Adding documentation. DONE"

    def act(self, thought: str, input_data: Any) -> Any:
        """Execute code generation."""
        if isinstance(input_data, dict):
            requirement = input_data.get("requirement", "")
            language = input_data.get("language", "python")
        else:
            requirement = str(input_data)
            language = "python"

        iteration = self.iteration_count

        if iteration == 1:
            # Analyze requirements
            return {"stage": "requirements", "analysis": f"Need to create: {requirement}"}
        elif iteration == 2:
            # Plan structure
            structure = ["imports", "class/function definition", "implementation", "tests"]
            self.code_structure = structure
            return {"stage": "structure", "plan": structure}
        elif iteration == 3:
            # Generate code
            code = f"""
def example_function():
    '''Generated function for: {requirement}'''
    # TODO: Implement {requirement}
    pass
"""
            return {"stage": "code", "implementation": code}
        else:
            # Add documentation
            return {
                "stage": "complete",
                "language": language,
                "requirement": requirement,
                "structure": self.code_structure,
                "code": "# Complete code with documentation",
                "ready": True,
            }


def example_research_agent():
    """Example using custom ResearchAgent."""
    print("\n" + "=" * 60)
    print("Example 1: Custom Research Agent")
    print("=" * 60)

    # Create research agent
    research_agent = ResearchAgent(name="AIResearcher")

    # Conduct research
    research_task = {
        "topic": "Machine Learning",
        "depth": "comprehensive"
    }

    print(f"\nResearch Task: {research_task['topic']}")
    response = research_agent.run(research_task)

    print(f"\nStatus: {response.status.value}")
    print(f"Iterations: {response.iterations}")
    print(f"\nResearch Process:")
    for i, thought in enumerate(response.thoughts, 1):
        print(f"  Step {i}: {thought}")

    print(f"\nFinal Research Report:")
    for key, value in response.content.items():
        print(f"  {key}: {value}")


def example_code_generator_agent():
    """Example using custom CodeGeneratorAgent."""
    print("\n" + "=" * 60)
    print("Example 2: Custom Code Generator Agent")
    print("=" * 60)

    # Create code generator agent
    code_agent = CodeGeneratorAgent(name="CodeGen")

    # Generate code
    code_task = {
        "requirement": "Create a function to validate email addresses",
        "language": "python"
    }

    print(f"\nCode Generation Task: {code_task['requirement']}")
    response = code_agent.run(code_task)

    print(f"\nStatus: {response.status.value}")
    print(f"Iterations: {response.iterations}")

    print(f"\nGeneration Process:")
    for action in response.actions:
        print(f"  Iteration {action['iteration']}: {action['thought']}")

    print(f"\nGenerated Code:")
    print(response.content)


def example_multi_custom_agents():
    """Example using multiple custom agents together."""
    print("\n" + "=" * 60)
    print("Example 3: Multiple Custom Agents Working Together")
    print("=" * 60)

    # Create manager and register custom agents
    manager = AgentManager()
    manager.register_agent(ResearchAgent(name="Researcher"))
    manager.register_agent(CodeGeneratorAgent(name="Developer"))

    # Research then implement
    print("\nWorkflow: Research -> Code Generation")

    # Step 1: Research
    research_response = manager.run_agent(
        "Researcher",
        {"topic": "Binary Search Algorithm"}
    )
    print(f"\n1. Research completed: {research_response.content['conclusion']}")

    # Step 2: Generate code based on research
    code_response = manager.run_agent(
        "Developer",
        {
            "requirement": "Implement binary search algorithm",
            "language": "python"
        }
    )
    print(f"\n2. Code generation completed")
    print(f"   Ready: {code_response.content.get('ready', False)}")


def main():
    """Run all custom agent examples."""
    print("AI Creator - Custom Agent Examples")
    print("=" * 60)
    print("\nThese examples show how to create your own specialized agents")
    print("by extending the base Agent class.")

    example_research_agent()
    example_code_generator_agent()
    example_multi_custom_agents()

    print("\n" + "=" * 60)
    print("All custom agent examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
