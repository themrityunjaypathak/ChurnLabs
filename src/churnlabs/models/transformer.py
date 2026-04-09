import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def build_transformer(X: pd.DataFrame) -> ColumnTransformer:
    """
    Build a feature transformation pipeline for numerical and categorical features.

    The transformer:
        Scales numerical columns (except "seniorcitizen")
        One-hot encodes categorical columns
        Passes remaining columns through unchanged

    Args:
        X (pd.DataFrame): Feature dataset used to identify column types.

    Returns:
        ColumnTransformer: Configured transformer ready for fitting.
    """
    num_cols = [
        col
        for col in X.select_dtypes(include="number").columns
        if col != "seniorcitizen"
    ]

    num_trf = Pipeline(steps=[("scaler", StandardScaler())])

    cat_cols = X.select_dtypes(include="category").columns

    cat_trf = Pipeline(
        steps=[("ohe", OneHotEncoder(sparse_output=False, drop="first"))]
    )

    transformer = ColumnTransformer(
        transformers=[
            ("categorical", cat_trf, cat_cols),
            ("numerical", num_trf, num_cols),
        ],
        remainder="passthrough",
    )

    return transformer
