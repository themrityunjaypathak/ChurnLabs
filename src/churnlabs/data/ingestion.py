from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

from churnlabs.core.config import get_data_config, PROJECT_ROOT
from churnlabs.core.settings import Settings


def fetch_data(query: str, db_url: str) -> pd.DataFrame:
    """
    Fetch data from database using a SQL query.
    """
    engine = create_engine(db_url)
    return pd.read_sql(query, engine)


def save_raw_data(df: pd.DataFrame, output_path: Path) -> None:
    """
    Export dataframe as CSV file to specified path.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def run_ingestion() -> None:
    """
    Run data ingestion pipeline:
    - Load config file
    - Fetch data from database
    - Save data as CSV file at specified path
    """
    config = get_data_config()
    settings = Settings()

    raw_data_path = (
        PROJECT_ROOT / config["data"]["raw_dir"] / config["data"]["raw_file"]
    )

    table_name = config["database"]["table_name"]

    query = f"SELECT * FROM {table_name}"

    df = fetch_data(query=query, db_url=settings.db_url)
    save_raw_data(df, raw_data_path)
