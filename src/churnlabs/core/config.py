import yaml
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CONFIG_DIR = PROJECT_ROOT / "config"


def _load_yaml(file_name: str) -> dict[str, Any]:
    """
    Load a YAML configuration file from the config directory.

    Args:
        file_name (str): Name of the YAML file to load.

    Returns:
        dict[str, Any]: Parsed YAML content as a dictionary.

    Raises:
        FileNotFoundError: If the YAML file does not exist.
        yaml.YAMLError: If the file content is not valid YAML.
    """
    config_file_path = CONFIG_DIR / file_name

    if not config_file_path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {config_file_path}")

    with config_file_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return data or {}


def get_data_config() -> dict[str, Any]:
    """
    Load and parse the project's data configuration file.

    Returns:
        dict[str, Any]: Parsed YAML configuration as dictionary.
    """
    return _load_yaml("data-config.yaml")
