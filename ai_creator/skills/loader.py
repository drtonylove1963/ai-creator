"""
Skill loader for importing and creating skills.
"""

import json
import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Type
from ai_creator.skills.base import Skill, SkillConfig, SkillCategory, SkillResult


class SkillLoader:
    """
    Loader for importing skills from various sources.
    """

    @staticmethod
    def load_from_file(file_path: str) -> Skill:
        """
        Load a skill from a Python file.

        Args:
            file_path: Path to Python file containing skill

        Returns:
            Loaded skill instance

        Raises:
            ValueError: If skill cannot be loaded
        """
        path = Path(file_path)
        if not path.exists():
            raise ValueError(f"File not found: {file_path}")

        if not path.suffix == '.py':
            raise ValueError(f"File must be a Python file (.py): {file_path}")

        # Load module from file
        spec = importlib.util.spec_from_file_location("custom_skill", file_path)
        if spec is None or spec.loader is None:
            raise ValueError(f"Could not load module from {file_path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules["custom_skill"] = module
        spec.loader.exec_module(module)

        # Find Skill subclass
        skill_class = None
        for item_name in dir(module):
            item = getattr(module, item_name)
            if (isinstance(item, type) and
                issubclass(item, Skill) and
                item is not Skill):
                skill_class = item
                break

        if skill_class is None:
            raise ValueError(f"No Skill subclass found in {file_path}")

        # Instantiate skill
        # Try to find config in module
        config = getattr(module, 'skill_config', None)
        if config is None:
            # Create default config
            config = SkillConfig(
                name=skill_class.__name__,
                description=skill_class.__doc__ or "Custom skill"
            )

        return skill_class(config)

    @staticmethod
    def load_from_dict(skill_dict: Dict[str, Any]) -> SkillConfig:
        """
        Load skill configuration from dictionary.

        Args:
            skill_dict: Dictionary with skill configuration

        Returns:
            SkillConfig instance
        """
        category_str = skill_dict.get('category', 'custom')
        category = SkillCategory(category_str)

        return SkillConfig(
            name=skill_dict['name'],
            description=skill_dict.get('description', ''),
            category=category,
            version=skill_dict.get('version', '1.0.0'),
            author=skill_dict.get('author', 'Unknown'),
            requires=skill_dict.get('requires', []),
            parameters=skill_dict.get('parameters', {}),
            metadata=skill_dict.get('metadata', {})
        )

    @staticmethod
    def load_from_json(json_path: str) -> SkillConfig:
        """
        Load skill configuration from JSON file.

        Args:
            json_path: Path to JSON file

        Returns:
            SkillConfig instance
        """
        path = Path(json_path)
        if not path.exists():
            raise ValueError(f"File not found: {json_path}")

        with open(path, 'r') as f:
            skill_dict = json.load(f)

        return SkillLoader.load_from_dict(skill_dict)

    @staticmethod
    def export_config(skill: Skill, output_path: str) -> None:
        """
        Export skill configuration to JSON file.

        Args:
            skill: Skill to export
            output_path: Path to output JSON file
        """
        config_dict = {
            'name': skill.config.name,
            'description': skill.config.description,
            'category': skill.config.category.value,
            'version': skill.config.version,
            'author': skill.config.author,
            'requires': skill.config.requires,
            'parameters': skill.config.parameters,
            'metadata': skill.config.metadata,
        }

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w') as f:
            json.dump(config_dict, f, indent=2)


def load_skill(source: str, source_type: str = 'file') -> Skill:
    """
    Convenience function to load a skill from various sources.

    Args:
        source: Path to skill file or JSON string
        source_type: Type of source ('file', 'json', 'dict')

    Returns:
        Loaded skill instance
    """
    loader = SkillLoader()

    if source_type == 'file':
        return loader.load_from_file(source)
    elif source_type == 'json':
        return loader.load_from_json(source)
    else:
        raise ValueError(f"Unknown source type: {source_type}")


def create_skill_template(
    name: str,
    description: str,
    category: str = "custom",
    output_path: Optional[str] = None
) -> str:
    """
    Create a skill template file.

    Args:
        name: Name of the skill
        description: Description of the skill
        category: Category of the skill
        output_path: Optional path to save template

    Returns:
        Template code as string
    """
    template = f'''"""
{name} - {description}

This is a custom skill created for AI Creator agents.
"""

from ai_creator.skills import Skill, SkillConfig, SkillResult, SkillCategory
from typing import Any


# Skill configuration
skill_config = SkillConfig(
    name="{name}",
    description="{description}",
    category=SkillCategory.{category.upper()},
    version="1.0.0",
    author="Your Name",
    requires=[],  # Add any required dependencies
    parameters={{}},  # Add configurable parameters
)


class {name.replace(" ", "")}Skill(Skill):
    """
    {description}
    """

    def __init__(self, config: SkillConfig = skill_config):
        """Initialize the skill."""
        super().__init__(config)
        # Add custom initialization here

    def initialize(self) -> None:
        """Initialize the skill (called once before first use)."""
        super().initialize()
        # Add custom initialization logic here

    def validate_input(self, input_data: Any) -> bool:
        """
        Validate input data.

        Args:
            input_data: Input to validate

        Returns:
            True if valid, False otherwise
        """
        # Add custom validation logic here
        return True

    def execute(self, input_data: Any, **kwargs) -> SkillResult:
        """
        Execute the skill.

        Args:
            input_data: Input data for the skill
            **kwargs: Additional keyword arguments

        Returns:
            SkillResult with execution results
        """
        try:
            # TODO: Implement your skill logic here

            # Example: Process input_data
            result = f"Processed: {{input_data}}"

            # Return success result
            return SkillResult(
                skill_name=self.config.name,
                success=True,
                output=result,
                metadata={{"input": input_data}}
            )

        except Exception as e:
            # Return failure result
            return SkillResult(
                skill_name=self.config.name,
                success=False,
                output=None,
                error=str(e)
            )


# Create skill instance for easy import
{name.replace(" ", "").lower()}_skill = {name.replace(" ", "")}Skill()
'''

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(template)

    return template
