# Examples

This directory contains example scripts demonstrating how to use AI Creator.

## Running Examples

Run any example with:

```bash
python examples/<example_name>.py
```

## Examples Included

### Basic Examples

- **`basic_usage.py`**: Core functionality including text generation, image creation, and content analysis
  - Demonstrates the basic Creator API
  - Shows simple text, image, and analysis operations

### Agent Examples

- **`agent_basics.py`**: Individual agent usage
  - TextAgent for text generation
  - ImageAgent for image tasks
  - AnalysisAgent for content analysis
  - Agent memory and state management

- **`agent_manager.py`**: Multi-agent orchestration
  - Running agents sequentially
  - Running agents in parallel
  - Agent collaboration on complex tasks
  - Custom multi-agent workflows

- **`custom_agent.py`**: Creating custom agents
  - Building a ResearchAgent from scratch
  - Building a CodeGeneratorAgent
  - Using custom agents in workflows

## Quick Start Examples

### Single Agent

```bash
python examples/agent_basics.py
```

This will demonstrate:
- Creating and using individual agents
- Agent thinking and acting process
- Agent memory capabilities

### Multi-Agent System

```bash
python examples/agent_manager.py
```

This will demonstrate:
- Coordinating multiple agents
- Sequential and parallel execution
- Agent collaboration

### Custom Agent

```bash
python examples/custom_agent.py
```

This will demonstrate:
- How to create your own specialized agents
- Implementing custom think() and act() methods
- Using custom agents in complex workflows

## Creating Your Own Examples

To create your own examples:

1. Import the necessary modules from `ai_creator`
2. Create agents or use the Creator class
3. Define your task or workflow
4. Run and handle results

Example template:

```python
from ai_creator import TextAgent, AgentManager

# Create your agent
agent = TextAgent(name="MyAgent")

# Run the agent
response = agent.run("Your task here")

# Use the results
print(f"Result: {response.content}")
print(f"Status: {response.status.value}")
```

## Learning Path

We recommend exploring the examples in this order:

1. **basic_usage.py** - Understand the basic API
2. **agent_basics.py** - Learn about individual agents
3. **agent_manager.py** - Explore multi-agent systems
4. **custom_agent.py** - Build your own agents

## Next Steps

After exploring these examples:
- Check the main README.md for complete API documentation
- Review the test files in `tests/` for more usage patterns
- Start building your own AI applications!
