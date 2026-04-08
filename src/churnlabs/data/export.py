import pandas as pd
from pathlib import Path

from churnlabs.core.config import get_data_config, PROJECT_ROOT


def export_processed_data(df: pd.DataFrame) -> Path:
    """
    Save processed dataframe as a Parquet file based on data-config.yaml.

    Args:
        df (pd.DataFrame): Cleaned dataframe to export.

    Returns:
        Path: Full path of the exported Parquet file.

    Raises:
        KeyError: If required config keys are missing.
    """
    config = get_data_config()

    data_config = config["data"]
    processed_dir = data_config["processed_dir"]
    processed_file = data_config["processed_file"]

    file_path: Path = PROJECT_ROOT / processed_dir / processed_file

    file_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(file_path, engine="pyarrow", index=False)

    return file_path
