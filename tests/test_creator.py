"""
Tests for the Creator class.
"""

import pytest
from ai_creator import Creator


class TestCreator:
    """Test cases for the Creator class."""

    def test_creator_initialization(self):
        """Test that Creator can be initialized."""
        creator = Creator()
        assert creator is not None
        assert isinstance(creator.config, dict)

    def test_creator_with_config(self):
        """Test Creator initialization with config."""
        config = {"model": "test-model", "temperature": 0.7}
        creator = Creator(config=config)
        assert creator.config == config

    def test_generate(self):
        """Test the generate method."""
        creator = Creator()
        prompt = "Test prompt"
        result = creator.generate(prompt)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_create_image(self):
        """Test the create_image method."""
        creator = Creator()
        description = "A test image"
        result = creator.create_image(description)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_analyze(self):
        """Test the analyze method."""
        creator = Creator()
        content = "Test content for analysis"
        result = creator.analyze(content)
        assert isinstance(result, dict)
        assert "analysis" in result
