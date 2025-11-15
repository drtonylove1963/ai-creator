# AI Creator

A versatile toolkit for building and deploying AI-powered creative applications.

## Overview

AI Creator is a framework designed to help developers build AI applications with ease. Whether you're working on content generation, image creation, or other AI-driven projects, this toolkit provides the foundation you need.

## Features

- **Modular Architecture**: Easy to extend and customize for your needs
- **Agent System**: Build autonomous AI agents that can think and act
- **Multi-Agent Orchestration**: Coordinate multiple agents working together
- **Skills System**: Agents can learn and use specialized capabilities
- **Web-Based GUI**: Intuitive interface for managing and running agents
- **Pre-built Agents**: TextAgent, ImageAgent, and AnalysisAgent ready to use
- **Built-in Skills**: 12+ ready-to-use skills for code, research, communication, and data
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

### Using the GUI

Launch the web interface for a visual way to interact with agents:

```bash
# Launch the GUI
python launch_gui.py

# Or launch on a custom port
python launch_gui.py --port 8080

# Create a shareable public link
python launch_gui.py --share
```

The GUI provides:
- **Single Agent Execution**: Run individual agents with easy configuration
- **Multi-Agent Orchestration**: Coordinate multiple agents visually
- **Agent Tools**: Explore and test available tools
- **Skills Management**: Import, create, and manage agent skills
- **Execution History**: View and analyze past runs
- **Built-in Documentation**: Integrated help and examples

Programmatic GUI launch:
```python
from ai_creator import launch_gui

# Launch the GUI from your code
launch_gui(share=False, server_port=7860)
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

## Skills System

Agents can learn and use specialized capabilities called skills:

### Using Built-in Skills

```python
from ai_creator import TextAgent
from ai_creator.skills.builtin import CodeGenerationSkill, SummarizationSkill

# Create agent and add skills
agent = TextAgent(name="SkillfulAgent")
agent.add_skill(CodeGenerationSkill())
agent.add_skill(SummarizationSkill())

# Use a skill
result = agent.use_skill(
    "code_generation",
    {"description": "Create a function to sort a list"}
)
print(result.output)
```

### Available Skill Categories

- **Code**: code_generation, code_review, debug
- **Research**: web_search, summarization, fact_check
- **Communication**: email_writing, report_generation, translation
- **Data**: data_analysis, data_visualization, data_cleaning

### Creating Custom Skills

```python
from ai_creator import Skill, SkillConfig, SkillResult, SkillCategory

class MySkill(Skill):
    def __init__(self):
        config = SkillConfig(
            name="my_skill",
            description="Custom skill",
            category=SkillCategory.CUSTOM
        )
        super().__init__(config)

    def execute(self, input_data, **kwargs):
        # Your skill logic
        return SkillResult(
            skill_name=self.config.name,
            success=True,
            output="Result"
        )
```

Or use the template generator:

```python
from ai_creator import create_skill_template

template = create_skill_template(
    name="MySkill",
    description="Does something amazing",
    category="custom",
    output_path="my_skill.py"
)
```

See `ai_creator/skills/README.md` for comprehensive skill documentation.

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
│   ├── skills/          # Skills system
│   │   ├── base.py      # Base skill classes
│   │   ├── registry.py  # Skill registry
│   │   ├── loader.py    # Skill loading/creation
│   │   └── builtin/     # Built-in skills
│   │       ├── code_skills.py
│   │       ├── research_skills.py
│   │       ├── communication_skills.py
│   │       └── data_skills.py
│   ├── gui/             # Web-based GUI
│   │   ├── app.py       # Main Gradio application
│   │   ├── agent_ui.py  # Single agent interface
│   │   ├── manager_ui.py # Multi-agent interface
│   │   └── tools_ui.py  # Tools interface
│   └── utils/           # Utility functions
├── examples/            # Example scripts
│   ├── basic_usage.py
│   ├── agent_basics.py
│   ├── agent_manager.py
│   ├── custom_agent.py
│   ├── skills_example.py
│   └── gui_example.py
├── tests/               # Test suite
├── launch_gui.py        # GUI launcher script
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Examples

See the `examples/` directory for comprehensive examples:

- `basic_usage.py`: Basic Creator API usage
- `agent_basics.py`: Individual agent usage
- `agent_manager.py`: Multi-agent orchestration
- `custom_agent.py`: Creating custom agents
- `skills_example.py`: Using skills with agents
- `gui_example.py`: Launching the GUI programmatically

Run any example:
```bash
python examples/agent_basics.py
```

Or launch the GUI:
```bash
python launch_gui.py
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
