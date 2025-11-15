"""
Helper functions for common tasks.
"""

import json
from pathlib import Path
from typing import Any, Dict


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a JSON file.

    Args:
        config_path: Path to the configuration file

    Returns:
        Configuration dictionary
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(path, 'r') as f:
        return json.load(f)


def save_output(data: Any, output_path: str, format: str = 'json') -> None:
    """
    Save output data to a file.

    Args:
        data: Data to save
        output_path: Path where to save the file
        format: Output format ('json' or 'text')
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if format == 'json':
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    else:
        with open(path, 'w') as f:
            f.write(str(data))
