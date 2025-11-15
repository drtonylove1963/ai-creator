"""
Tests for utility functions.
"""

import json
import pytest
from pathlib import Path
from ai_creator.utils import load_config, save_output


class TestUtils:
    """Test cases for utility functions."""

    def test_save_output_json(self, tmp_path):
        """Test saving output in JSON format."""
        data = {"key": "value", "number": 42}
        output_file = tmp_path / "test_output.json"

        save_output(data, str(output_file), format='json')

        assert output_file.exists()
        with open(output_file, 'r') as f:
            loaded_data = json.load(f)
        assert loaded_data == data

    def test_save_output_text(self, tmp_path):
        """Test saving output in text format."""
        data = "Test text content"
        output_file = tmp_path / "test_output.txt"

        save_output(data, str(output_file), format='text')

        assert output_file.exists()
        with open(output_file, 'r') as f:
            content = f.read()
        assert content == data

    def test_load_config(self, tmp_path):
        """Test loading configuration from file."""
        config_data = {"setting1": "value1", "setting2": 123}
        config_file = tmp_path / "config.json"

        with open(config_file, 'w') as f:
            json.dump(config_data, f)

        loaded_config = load_config(str(config_file))
        assert loaded_config == config_data

    def test_load_config_file_not_found(self):
        """Test that load_config raises error for missing file."""
        with pytest.raises(FileNotFoundError):
            load_config("nonexistent_file.json")
