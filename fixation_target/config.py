"""Configuration loading and saving utilities for fixation targets."""

import json
from pathlib import Path


def load_config(config_path: Path | str) -> dict:
    """Load fixation target configuration from JSON file.

    Args:
        config_path: Path to the JSON configuration file.

    Returns:
        Dictionary containing the configuration parameters.

    Raises:
        FileNotFoundError: If the config file doesn't exist.
        json.JSONDecodeError: If the JSON is invalid.

    """
    config_path = Path(config_path)
    with config_path.open() as f:
        return json.load(f)


def save_config(config: dict, config_path: Path | str) -> None:
    """Save fixation target configuration to JSON file.

    Args:
        config: Configuration dictionary to save.
        config_path: Path where to save the JSON file.

    """
    config_path = Path(config_path)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with config_path.open("w") as f:
        json.dump(config, f, indent=2)
