import json
import joblib
from pathlib import Path
from typing import Tuple, Dict, Any
from sklearn.base import BaseEstimator

from churnlabs.core.config import get_artifacts_config, PROJECT_ROOT


def _get_artifact_paths() -> Tuple[Path, Path]:
    """
    Construct artifacts file paths for model and metrics.

    This function:
        Reads artifacts configuration from YAML
        Creates required directories if they do not exist
        Returns full file paths for model and metrics

    Returns:
        Tuple[Path, Path]:
            model_path: Path to save the trained model
            metrics_path: Path to save the evaluation metrics
    """
    config = get_artifacts_config()

    root_dir = PROJECT_ROOT / config["artifacts"]["root_dir"]
    model_dir = root_dir / config["artifacts"]["model_dir"]
    metrics_dir = root_dir / config["artifacts"]["metrics_dir"]

    model_dir.mkdir(parents=True, exist_ok=True)
    metrics_dir.mkdir(parents=True, exist_ok=True)

    model_path = model_dir / config["artifacts"]["model_filename"]
    metrics_path = metrics_dir / config["artifacts"]["metrics_filename"]

    return model_path, metrics_path


def save_model(model: BaseEstimator) -> Path:
    """
    Save trained model or pipeline to the configured artifacts directory.

    Args:
        model (BaseEstimator): Trained Scikit-learn model or pipeline.

    Returns:
        Path: File path where the model is saved.

    Raises:
        OSError: If the model file cannot be written.
    """
    model_path, _ = _get_artifact_paths()
    joblib.dump(model, model_path, compress=3)
    return model_path


def save_metrics(metrics: Dict[str, Any]) -> Path:
    """
    Save evaluation metrics as JSON in the configured artifacts directory.

    Args:
        metrics (Dict[str, Any]): Dictionary containing evaluation metrics.

    Returns:
        Path: File path where the metrics are saved.

    Raises:
        OSError: If the metrics file cannot be written.
        TypeError: If metrics are not JSON serializable.
    """
    _, metrics_path = _get_artifact_paths()

    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)

    return metrics_path
