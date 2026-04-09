import yaml
import tomllib
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


def _load_toml(file_name: str) -> dict[str, Any]:
    """
    Load a TOML configuration file from the project's root directory.

    Args:
        file_name (str): Name of the TOML file to load.

    Returns:
        dict[str, Any]: Parsed TOML content as a dictionary.

    Raises:
        FileNotFoundError: If the TOML file does not exist.
        tomllib.TOMLDecodeError: If the file content is not valid TOML.
    """
    toml_file_path = PROJECT_ROOT / file_name

    if not toml_file_path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {toml_file_path}")

    with open(toml_file_path, "rb") as f:
        data = tomllib.load(f)

    return data or {}


def get_data_config() -> dict[str, Any]:
    """
    Load and parse the project's data configuration file.

    Returns:
        dict[str, Any]: Parsed YAML configuration as dictionary.
    """
    return _load_yaml("data-config.yaml")


def get_training_config() -> dict[str, Any]:
    """
    Load and parse the project's model training configuration file.

    Returns:
        dict[str, Any]: Parsed YAML configuration as dictionary.
    """
    return _load_yaml("training-config.yaml")


def get_model_config() -> dict[str, Any]:
    """
    Load and parse the project's model configuration file.

    Returns:
        dict[str, Any]: Parsed YAML configuration as dictionary.
    """
    return _load_yaml("model-config.yaml")


def get_artifacts_config() -> dict[str, Any]:
    """
    Load and parse the project's artifcats configuration file.

    Returns:
        Dict[str, Any]: Parsed YAML configuration as dictionary.
    """
    return _load_yaml("artifacts-config.yaml")


def get_huggingface_config() -> dict[str, Any]:
    """
    Load and parse the project's huggingface configuration file.

    Returns:
        Dict[str, Any]: Parsed YAML configuration as dictionary.
    """
    return _load_yaml("huggingface-config.yaml")


def get_model_version() -> str:
    """
    Load and return the project version from pyproject.toml.

    Returns:
        str: The current project version.
    """
    pyproject_data = _load_toml("pyproject.toml")
    return pyproject_data.get("project", {}).get("version", "0.0.0")
