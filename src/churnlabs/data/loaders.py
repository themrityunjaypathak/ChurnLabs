from pathlib import Path
import pandas as pd


from churnlabs.core.config import get_data_config, PROJECT_ROOT


def load_raw_data() -> pd.DataFrame:
    """
    Load raw dataset as defined in data-config.yaml.

    Returns:
        pd.DataFrame: DataFrame loaded from CSV file.

    Raises:
        FileNotFoundError: If raw CSV file does not exist.
        KeyError: If required config keys are missing.
    """
    config = get_data_config()

    data_config = config["data"]
    raw_dir = data_config["raw_dir"]
    raw_file = data_config["raw_file"]

    file_path: Path = PROJECT_ROOT / raw_dir / raw_file

    if not file_path.exists():
        raise FileNotFoundError(f"Raw data file not found at: {file_path}")

    if file_path.suffix.lower() != ".csv":
        raise TypeError(
            f"Invalid file type '{file_path.suffix}'. Expected '.csv' file."
        )

    return pd.read_csv(file_path)
