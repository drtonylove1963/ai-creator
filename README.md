# AI Creator

A versatile toolkit for building and deploying AI-powered creative applications.

## Overview

AI Creator is a framework designed to help developers build AI applications with ease. Whether you're working on content generation, image creation, or other AI-driven projects, this toolkit provides the foundation you need.

## Features

- **Modular Architecture**: Easy to extend and customize for your needs
- **Agent System**: Build autonomous AI agents that can think and act
- **Multi-Agent Orchestration**: Coordinate multiple agents working together
- **Pre-built Agents**: TextAgent, ImageAgent, and AnalysisAgent ready to use
- **Tool Registry**: Extensible tools that agents can use
- **Memory System**: Agents can remember past interactions
- **Simple API**: Intuitive interface for common AI tasks
- **Comprehensive Examples**: Get started quickly with working examples

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd ai-creator

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from ai_creator import Creator

# Initialize the creator
creator = Creator()

# Use AI capabilities
result = creator.generate("Your prompt here")
print(result)
```

### Using Agents

```python
from ai_creator import TextAgent, AgentManager

# Create a text generation agent
agent = TextAgent(name="MyAgent")

# Run the agent
response = agent.run("Write a haiku about AI")
print(response.content)

# Use multiple agents together
manager = AgentManager()
manager.register_agent(TextAgent(name="Writer"))
manager.register_agent(AnalysisAgent(name="Analyzer"))

# Run agents sequentially
responses = manager.run_sequential(
    agent_names=["Writer", "Analyzer"],
    input_data="Create and analyze a product description"
)
```

## Agent System

AI Creator includes a powerful agent system for building autonomous AI agents:

### Built-in Agents

- **TextAgent**: Text generation, summarization, and rewriting
- **ImageAgent**: Image generation, analysis, and modification
- **AnalysisAgent**: Sentiment analysis, entity extraction, topic identification

### Creating Custom Agents

```python
from ai_creator import Agent, AgentConfig

class MyCustomAgent(Agent):
    def __init__(self, name="CustomAgent", **kwargs):
        config = AgentConfig(name=name, **kwargs)
        super().__init__(config)

    def think(self, input_data):
        # Your thinking logic here
        return "I need to process this input..."

    def act(self, thought, input_data):
        # Your action logic here
        return "Processed result"

# Use your custom agent
agent = MyCustomAgent()
response = agent.run("Some input")
```

### Agent Manager

Orchestrate multiple agents:

```python
from ai_creator import AgentManager, TextAgent, AnalysisAgent

manager = AgentManager()
manager.register_agent(TextAgent(name="Writer"))
manager.register_agent(AnalysisAgent(name="Analyzer"))

# Sequential execution
responses = manager.run_sequential(
    agent_names=["Writer", "Analyzer"],
    input_data="Your task"
)

# Parallel execution
responses = manager.run_parallel(
    agent_names=["Writer", "Analyzer"],
    input_data="Shared input"
)

# Agent collaboration
result = manager.collaborate(
    task="Complete this task together",
    agent_names=["Writer", "Analyzer"],
    max_rounds=3
)
```

## Project Structure

```
ai-creator/
├── ai_creator/          # Main package directory
│   ├── __init__.py      # Package initialization
│   ├── core/            # Core functionality
│   ├── agents/          # Agent system
│   │   ├── base.py      # Base agent classes
│   │   ├── manager.py   # Agent orchestration
│   │   ├── text_agent.py
│   │   ├── image_agent.py
│   │   ├── analysis_agent.py
│   │   └── tools.py     # Agent tools
│   └── utils/           # Utility functions
├── examples/            # Example scripts
│   ├── basic_usage.py
│   ├── agent_basics.py
│   ├── agent_manager.py
│   └── custom_agent.py
├── tests/               # Test suite
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Examples

See the `examples/` directory for comprehensive examples:

- `basic_usage.py`: Basic Creator API usage
- `agent_basics.py`: Individual agent usage
- `agent_manager.py`: Multi-agent orchestration
- `custom_agent.py`: Creating custom agents

Run any example:
```bash
python examples/agent_basics.py
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for your own purposes.

## Support

For issues, questions, or contributions, please open an issue on GitHub.
