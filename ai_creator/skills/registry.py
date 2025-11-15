"""
Skill registry for managing and organizing skills.
"""

from typing import Dict, List, Optional, Type
from ai_creator.skills.base import Skill, SkillCategory


class SkillRegistry:
    """
    Registry for managing skills.

    The SkillRegistry allows you to:
    - Register skills by name
    - Organize skills by category
    - Search and filter skills
    - Get skill information
    """

    def __init__(self):
        """Initialize the skill registry."""
        self.skills: Dict[str, Skill] = {}
        self._categories: Dict[SkillCategory, List[str]] = {
            category: [] for category in SkillCategory
        }

    def register(self, skill: Skill) -> None:
        """
        Register a skill.

        Args:
            skill: Skill instance to register
        """
        name = skill.config.name
        if name in self.skills:
            raise ValueError(f"Skill '{name}' already registered")

        self.skills[name] = skill
        category = skill.config.category
        if name not in self._categories[category]:
            self._categories[category].append(name)

    def unregister(self, skill_name: str) -> bool:
        """
        Unregister a skill.

        Args:
            skill_name: Name of skill to unregister

        Returns:
            True if unregistered, False if not found
        """
        if skill_name not in self.skills:
            return False

        skill = self.skills[skill_name]
        category = skill.config.category
        self._categories[category].remove(skill_name)
        del self.skills[skill_name]
        return True

    def get(self, skill_name: str) -> Optional[Skill]:
        """
        Get a skill by name.

        Args:
            skill_name: Name of the skill

        Returns:
            Skill instance or None if not found
        """
        return self.skills.get(skill_name)

    def list_skills(
        self,
        category: Optional[SkillCategory] = None
    ) -> List[str]:
        """
        List all registered skills.

        Args:
            category: Optional category to filter by

        Returns:
            List of skill names
        """
        if category:
            return self._categories[category].copy()
        return list(self.skills.keys())

    def list_by_category(self) -> Dict[str, List[str]]:
        """
        List skills organized by category.

        Returns:
            Dictionary mapping category names to skill lists
        """
        return {
            category.value: names
            for category, names in self._categories.items()
            if names
        }

    def search(self, query: str) -> List[str]:
        """
        Search for skills by name or description.

        Args:
            query: Search query

        Returns:
            List of matching skill names
        """
        query_lower = query.lower()
        matches = []

        for name, skill in self.skills.items():
            if (query_lower in name.lower() or
                query_lower in skill.config.description.lower()):
                matches.append(name)

        return matches

    def get_info(self, skill_name: str) -> Optional[Dict]:
        """
        Get information about a skill.

        Args:
            skill_name: Name of the skill

        Returns:
            Skill information dictionary or None
        """
        skill = self.get(skill_name)
        return skill.get_info() if skill else None

    def get_all_info(self) -> List[Dict]:
        """
        Get information about all skills.

        Returns:
            List of skill information dictionaries
        """
        return [skill.get_info() for skill in self.skills.values()]

    def execute_skill(
        self,
        skill_name: str,
        input_data,
        **kwargs
    ):
        """
        Execute a skill by name.

        Args:
            skill_name: Name of skill to execute
            input_data: Input data for the skill
            **kwargs: Additional arguments

        Returns:
            SkillResult from execution

        Raises:
            ValueError: If skill not found
        """
        skill = self.get(skill_name)
        if not skill:
            raise ValueError(f"Skill '{skill_name}' not found")

        return skill.run(input_data, **kwargs)

    def get_stats(self, skill_name: Optional[str] = None) -> Dict:
        """
        Get execution statistics.

        Args:
            skill_name: Optional specific skill name

        Returns:
            Statistics dictionary
        """
        if skill_name:
            skill = self.get(skill_name)
            if not skill:
                raise ValueError(f"Skill '{skill_name}' not found")
            return skill.get_stats()

        # Return stats for all skills
        return {
            name: skill.get_stats()
            for name, skill in self.skills.items()
        }

    def clear(self) -> None:
        """Clear all registered skills."""
        self.skills.clear()
        for category in self._categories:
            self._categories[category].clear()

    def __len__(self) -> int:
        """Get number of registered skills."""
        return len(self.skills)

    def __contains__(self, skill_name: str) -> bool:
        """Check if skill is registered."""
        return skill_name in self.skills


# Global skill registry
skill_registry = SkillRegistry()
