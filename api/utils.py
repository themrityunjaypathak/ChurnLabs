import io
import json
import logging
from typing import Any
from pathlib import Path

import joblib
import requests
from sklearn.pipeline import Pipeline

from churnlabs.core.config import get_model_config
from churnlabs.models.artifact import _get_artifact_paths
from churnlabs.core.config import get_huggingface_config

logger = logging.getLogger(__name__)


_CACHE: dict[str, Any] = {}


def _fetch_remote_bytes(url: str) -> bytes:
    for attempt in range(3):
        try:
            logger.info("Fetching remote artifacts: %s", url)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.content
        except Exception:
            logger.warning("Attempt %d failed", attempt + 1)

    raise RuntimeError("Failed to fetch artifacts after retries")


def load_model() -> Pipeline:
    """Load trained model or pipeline (local → remote fallback, cached)."""

    if "model" in _CACHE:
        return _CACHE["model"]

    config = get_huggingface_config()
    model_path, _ = _get_artifact_paths()
    model_path = Path(model_path)

    if model_path.exists():
        logger.info("Loading model from local artifacts")
        model = joblib.load(model_path)

    else:
        base_url = config["huggingface"]["base_url"]
        remote_path = config["remote"]["model_file"]
        url = f"{base_url}/{remote_path}"

        content = _fetch_remote_bytes(url)
        model = joblib.load(io.BytesIO(content))

    _CACHE["model"] = model
    return model


def load_metrics() -> dict[str, Any]:
    """Load evaluation metrics (local → remote fallback, cached)."""

    if "metrics" in _CACHE:
        return _CACHE["metrics"]

    config = get_huggingface_config()
    _, metrics_path = _get_artifact_paths()
    metrics_path = Path(metrics_path)

    if metrics_path.exists():
        logger.info("Loading metrics from local artifacts")
        with metrics_path.open("r", encoding="utf-8") as f:
            metrics = json.load(f)

    else:
        base_url = config["huggingface"]["base_url"]
        remote_path = config["remote"]["metrics_file"]
        url = f"{base_url}/{remote_path}"

        content = _fetch_remote_bytes(url)
        metrics = json.loads(content.decode("utf-8"))

    _CACHE["metrics"] = metrics
    return metrics


def load_threshold() -> float:
    """Load decision threshold from model-config.YAML."""
    config = get_model_config()
    return config["threshold"]["value"]
