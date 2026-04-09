import pandas as pd
from sklearn.model_selection import train_test_split

from churnlabs.core.config import get_training_config


def split_data(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Split dataset into training and testing sets based on training-config.yaml.

    Args:
        df (pd.DataFrame): Full dataset including features and target column.

    Returns:
        tuple:
            - pd.DataFrame: X_train (training features)
            - pd.DataFrame: X_test (testing features)
            - pd.Series: y_train (training target)
            - pd.Series: y_test (testing target)

    Raises:
        KeyError: If required config keys are missing.
    """
    config = get_training_config()

    X = df.drop(columns=[config["training"]["target_column"]])
    y = df[config["training"]["target_column"]]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=config["training"]["test_size"],
        random_state=config["training"]["random_state"],
        stratify=y if config["training"]["stratify"] else None,
    )

    return X_train, X_test, y_train, y_test
