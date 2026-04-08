from typing import Final
import pandas as pd


EXPECTED_COLUMNS: Final[list[str]] = [
    "customerid",
    "gender",
    "seniorcitizen",
    "partner",
    "dependents",
    "tenure",
    "phoneservice",
    "multiplelines",
    "internetservice",
    "onlinesecurity",
    "onlinebackup",
    "deviceprotection",
    "techsupport",
    "streamingtv",
    "streamingmovies",
    "contract",
    "paperlessbilling",
    "paymentmethod",
    "monthlycharges",
    "totalcharges",
    "churn",
]


EXPECTED_CATEGORIES: Final[dict[str, set[str]]] = {
    "churn": {"Yes", "No"},
    "gender": {"Male", "Female"},
    "partner": {"Yes", "No"},
    "dependents": {"Yes", "No"},
    "phoneservice": {"Yes", "No"},
    "multiplelines": {"Yes", "No", "No phone service"},
    "internetservice": {"DSL", "Fiber optic", "No"},
    "onlinesecurity": {"Yes", "No", "No internet service"},
    "onlinebackup": {"Yes", "No", "No internet service"},
    "deviceprotection": {"Yes", "No", "No internet service"},
    "techsupport": {"Yes", "No", "No internet service"},
    "streamingtv": {"Yes", "No", "No internet service"},
    "streamingmovies": {"Yes", "No", "No internet service"},
    "contract": {"Month-to-month", "One year", "Two year"},
    "paperlessbilling": {"Yes", "No"},
    "paymentmethod": {
        "Bank transfer (automatic)",
        "Credit card (automatic)",
        "Electronic check",
        "Mailed check",
    },
}


def validate_schema(df: pd.DataFrame) -> None:
    """
    Perform schema validation on the raw dataset.

    Checks:
        Column names (case-insensitive match)
        Missing values in critical columns
        Allowed categories for categorical features

    Raises:
        ValueError: If schema mismatch or invalid categories are detected.
    """
    df_cols = set(df.columns.str.lower())
    if df_cols != set(EXPECTED_COLUMNS):
        raise ValueError(
            f"Schema mismatch.\nExpected columns: {EXPECTED_COLUMNS}\nGot: {list(df.columns)}"
        )

    CRITICAL_COLUMNS = ["churn", "tenure", "monthlycharges"]
    missing = df[CRITICAL_COLUMNS].isnull().sum()
    if missing.any():
        raise ValueError(f"Missing values in critical columns:\n{missing}")

    for col, allowed_values in EXPECTED_CATEGORIES.items():
        if col in df.columns:
            unique_vals = set(df[col].dropna().unique())
            if not unique_vals.issubset(allowed_values):
                raise ValueError(
                    f"Unexpected category in '{col}'. "
                    f"Allowed: {allowed_values}, Found: {unique_vals}"
                )


def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic data cleaning.

    Steps:
        1. Normalize column names (strip whitespaces and convert to lowercase)
        2. Validate schema against expected features and categories
        3. Drop unnecessary columns
        4. Convert 'totalcharges' to numeric and remove invalid rows
        5. Strip whitespace from string/object columns
        6. Replace inconsistent values in 'service_cols' ('No internet service' → 'No')
        7. Downcast integer and float columns for memory efficiency
        8. Convert remaining string/object columns to categorical dtype

    Args:
        df (pd.DataFrame): Raw input dataframe.

    Returns:
        pd.DataFrame: Cleaned and optimized dataframe.
    """
    df = df.copy()

    df.columns = df.columns.str.strip().str.lower()

    validate_schema(df)

    df = df.drop(columns=["customerid"], errors="ignore")

    if "totalcharges" in df.columns:
        df["totalcharges"] = pd.to_numeric(df["totalcharges"], errors="coerce")
        df = df.dropna(subset=["totalcharges"])

    string_cols = df.select_dtypes(include=["object", "string"]).columns
    df[string_cols] = df[string_cols].apply(lambda col: col.str.strip())

    service_cols = [
        "onlinebackup",
        "onlinesecurity",
        "deviceprotection",
        "techsupport",
        "streamingtv",
        "streamingmovies",
    ]

    for col in service_cols:
        if col in df.columns:
            df[col] = df[col].replace("No internet service", "No")

    int_cols = df.select_dtypes(include=["int64"]).columns
    df[int_cols] = df[int_cols].apply(pd.to_numeric, downcast="integer")

    float_cols = df.select_dtypes(include=["float64"]).columns
    df[float_cols] = df[float_cols].apply(pd.to_numeric, downcast="float")

    string_cols = df.select_dtypes(include=["object", "string"]).columns
    df[string_cols] = df[string_cols].astype("category")

    df = df.reset_index(drop=True)

    return df
