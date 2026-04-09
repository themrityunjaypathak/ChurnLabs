import pandas as pd


def target_encoder(
    y_train: pd.Series, y_test: pd.Series
) -> tuple[pd.Series, pd.Series]:
    """
    Encode binary target values ("Yes"/"No") into numerical format (1/0).

    Args:
        y_train (pd.Series): Training target values.
        y_test (pd.Series): Testing target values.

    Returns:
        tuple:
            - pd.Series: Encoded training target (1 for "Yes", 0 for "No")
            - pd.Series: Encoded testing target (1 for "Yes", 0 for "No")

    Raises:
        KeyError: If target values contain labels other than "Yes" or "No".
    """
    y_train_encoded = y_train.map({"Yes": 1, "No": 0})
    y_test_encoded = y_test.map({"Yes": 1, "No": 0})

    return y_train_encoded, y_test_encoded
