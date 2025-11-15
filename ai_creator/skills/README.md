

# Skills System

The Skills system allows agents to learn and use specialized capabilities to accomplish tasks.

## What are Skills?

Skills are modular, reusable capabilities that agents can acquire and use. They are:
- **Specialized**: Each skill focuses on a specific capability
- **Reusable**: Skills can be shared across different agents
- **Trackable**: Execution statistics help monitor performance
- **Extensible**: Easy to create custom skills

## Quick Start

### Using Built-in Skills

```python
from ai_creator import TextAgent
from ai_creator.skills.builtin import CodeGenerationSkill

# Create an agent
agent = TextAgent(name="MyAgent")

# Add a skill
agent.add_skill(CodeGenerationSkill())

# Use the skill
result = agent.use_skill(
    "code_generation",
    {"description": "Create a function to sort a list"}
)

print(result.output)
```

### Using the Skill Registry

```python
from ai_creator import skill_registry
from ai_creator.skills.builtin import register_all_builtin_skills

# Register all built-in skills
register_all_builtin_skills(skill_registry)

# List available skills
print(skill_registry.list_by_category())

# Execute a skill
result = skill_registry.execute_skill(
    "summarization",
    "Long text to summarize..."
)
```

## Built-in Skills

### Code Skills
- **code_generation**: Generate code from descriptions
- **code_review**: Review code and provide feedback
- **debug**: Debug code and find issues

### Research Skills
- **web_search**: Search the web for information
- **summarization**: Summarize text content
- **fact_check**: Verify and fact-check information

### Communication Skills
- **email_writing**: Compose professional emails
- **report_generation**: Generate structured reports
- **translation**: Translate text between languages

### Data Skills
- **data_analysis**: Analyze datasets and provide insights
- **data_visualization**: Create visualizations from data
- **data_cleaning**: Clean and preprocess data

## Creating Custom Skills

### Using the Template Generator

```python
from ai_creator import create_skill_template

# Generate a template
template = create_skill_template(
    name="MyCustomSkill",
    description="Does something amazing",
    category="custom",
    output_path="my_skill.py"
)
```

### Manual Creation

```python
from ai_creator import Skill, SkillConfig, SkillResult, SkillCategory

class MySkill(Skill):
    def __init__(self):
        config = SkillConfig(
            name="my_skill",
            description="My custom skill",
            category=SkillCategory.CUSTOM,
            version="1.0.0",
            author="Your Name"
        )
        super().__init__(config)

    def execute(self, input_data, **kwargs):
        try:
            # Your skill logic here
            result = f"Processed: {input_data}"

            return SkillResult(
                skill_name=self.config.name,
                success=True,
                output=result
            )
        except Exception as e:
            return SkillResult(
                skill_name=self.config.name,
                success=False,
                output=None,
                error=str(e)
            )
```

## Loading Skills from Files

```python
from ai_creator import SkillLoader

# Load a skill from a Python file
skill = SkillLoader.load_from_file("path/to/skill.py")

# Add to agent
agent.add_skill(skill)
```

## Skill Statistics

Track skill performance:

```python
skill = CodeGenerationSkill()

# Use the skill
skill.run("Generate code...")

# Get statistics
stats = skill.get_stats()
print(stats)
# Output: {
#     'executions': 1,
#     'successes': 1,
#     'failures': 0,
#     'success_rate': '100.00%',
#     'avg_time': '0.05s'
# }
```

## Agent Skills Management

```python
agent = TextAgent(name="MyAgent")

# Add skills
agent.add_skill(CodeGenerationSkill())
agent.add_skill(SummarizationSkill())

# List skills
print(agent.list_skills())  # ['code_generation', 'summarization']

# Check if agent has a skill
if agent.has_skill("code_generation"):
    result = agent.use_skill("code_generation", "...")

# Remove a skill
agent.remove_skill("code_generation")

# Get skill information
info = agent.get_skill_info("summarization")
print(info)
```

## Best Practices

1. **Naming**: Use descriptive, lowercase names with underscores
2. **Error Handling**: Always handle exceptions in `execute()` method
3. **Documentation**: Provide clear descriptions and docstrings
4. **Validation**: Implement `validate_input()` for input checking
5. **Categories**: Use appropriate skill categories for organization
6. **Versioning**: Update version numbers when modifying skills
7. **Dependencies**: List required dependencies in `requires` field

## Sharing Skills

### Export Skill Configuration

```python
from ai_creator import SkillLoader

skill = MySkill()
SkillLoader.export_config(skill, "skill_config.json")
```

### Import Configuration

```python
config = SkillLoader.load_from_json("skill_config.json")
skill = MySkill(config)
```

## Advanced Usage

### Custom Initialization

```python
class DatabaseSkill(Skill):
    def initialize(self):
        super().initialize()
        # Connect to database
        self.connection = connect_to_db()

    def execute(self, input_data, **kwargs):
        # Use self.connection
        pass
```

### Context-Aware Execution

```python
class ContextualSkill(Skill):
    def can_execute(self, context=None):
        # Check if required resources are available
        return context and "api_key" in context

    def execute(self, input_data, **kwargs):
        context = kwargs.get("context", {})
        if not self.can_execute(context):
            return SkillResult(
                skill_name=self.config.name,
                success=False,
                error="Missing required context"
            )
        # Execute with context
```

## Examples

See `examples/skills_example.py` for comprehensive examples including:
- Basic skill usage
- Agents with multiple skills
- Skill registry operations
- Creating custom skills
- Complete workflows

## API Reference

### Skill
Base class for all skills.

**Methods:**
- `execute(input_data, **kwargs) -> SkillResult`: Execute the skill
- `run(input_data, **kwargs) -> SkillResult`: Run with error handling
- `initialize()`: Initialize skill resources
- `validate_input(input_data) -> bool`: Validate input
- `can_execute(context) -> bool`: Check if can execute
- `get_stats() -> Dict`: Get execution statistics
- `get_info() -> Dict`: Get skill information

### SkillRegistry
Manage and organize skills.

**Methods:**
- `register(skill)`: Register a skill
- `unregister(name) -> bool`: Unregister a skill
- `get(name) -> Skill`: Get a skill
- `list_skills(category=None) -> List`: List skills
- `search(query) -> List`: Search for skills
- `execute_skill(name, input_data, **kwargs)`: Execute skill by name

### SkillLoader
Load and export skills.

**Methods:**
- `load_from_file(path) -> Skill`: Load from Python file
- `load_from_json(path) -> SkillConfig`: Load config from JSON
- `export_config(skill, path)`: Export configuration

## Troubleshooting

**Skill not found:**
```python
# Make sure skill is registered or added to agent
agent.add_skill(MySkill())
```

**Import errors:**
```python
# Check all dependencies are installed
pip install -r requirements.txt
```

**Validation failures:**
```python
# Override validate_input for custom validation
def validate_input(self, input_data):
    return isinstance(input_data, dict) and "key" in input_data
```

## Contributing

To contribute a skill:
1. Create your skill following best practices
2. Add tests
3. Document usage
4. Submit pull request

## Future Enhancements

Planned features:
- Skill dependencies and auto-loading
- Skill marketplace
- Version management
- Skill composition (combining skills)
- Performance profiling
- Async skill execution
