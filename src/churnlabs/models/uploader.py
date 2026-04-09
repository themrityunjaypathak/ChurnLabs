import logging
from pathlib import Path
from huggingface_hub import HfApi

from churnlabs.core.config import get_huggingface_config

logger = logging.getLogger(__name__)


def upload_artifacts(token: str | None = None) -> None:
    """
    Upload model and metrics artifacts to Hugging Face repository.

    Args:
        token (str | None): Hugging Face access token.
    """
    config = get_huggingface_config()

    repo_id = config["huggingface"]["repo_id"]
    model_path = Path(config["artifacts"]["model_path"])
    metrics_path = Path(config["artifacts"]["metrics_path"])

    api = HfApi(token=token)

    files = [
        (model_path, config["remote"]["model_file"]),
        (metrics_path, config["remote"]["metrics_file"]),
    ]

    for local_path, repo_path in files:
        if local_path.exists():
            logger.info("Uploading %s → %s", local_path, repo_path)

            api.upload_file(
                path_or_fileobj=str(local_path),
                path_in_repo=repo_path,
                repo_id=repo_id,
            )
        else:
            logger.warning("File not found: %s", local_path)
