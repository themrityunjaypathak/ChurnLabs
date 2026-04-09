import json
import logging
import joblib
import requests
import io
from pathlib import Path
from typing import Any

from sklearn.pipeline import Pipeline

from churnlabs.core.config import get_huggingface_config

logger = logging.getLogger(__name__)


def _load_remote(url: str) -> bytes:
    """
    Fetch artifact content from a remote URL.

    Args:
        url (str): Remote file URL.

    Returns:
        bytes: Raw file content.
    """
    logger.info("Loading remote artifacts: %s", url)
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.content


def load_model() -> Pipeline:
    """
    Load trained model or pipeline from local path or remote source.

    Returns:
        Pipeline: Loaded Scikit-learn model or pipeline.
    """
    config = get_huggingface_config()

    local_path = Path(config["artifacts"]["model_path"])

    if local_path.exists():
        logger.info("Loading model from local path: %s", local_path)
        return joblib.load(local_path)

    base_url = config["huggingface"]["base_url"]
    remote_path = config["remote"]["model_file"]

    url = f"{base_url}/{remote_path}"
    content = _load_remote(url)

    return joblib.load(io.BytesIO(content))


def load_metrics() -> dict[str, Any]:
    """
    Load evaluation metrics from local path or remote source.

    Returns:
        dict[str, Any]: Metrics dictionary.
    """
    config = get_huggingface_config()

    local_path = Path(config["artifacts"]["metrics_path"])

    if local_path.exists():
        logger.info("Loading metrics from local path: %s", local_path)
        with local_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    base_url = config["huggingface"]["base_url"]
    remote_path = config["remote"]["metrics_file"]

    url = f"{base_url}/{remote_path}"
    content = _load_remote(url)

    return json.loads(content.decode("utf-8"))
