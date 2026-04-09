import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline

from churnlabs.models.transformer import build_transformer


def build_pipeline(model: BaseEstimator, X: pd.DataFrame) -> Pipeline:
    """
    Build a complete machine learning pipeline.

    The pipeline:
        Applies feature transformation
        Trains the provided model

    Args:
        model: Instantiated machine learning model.
        X (pd.DataFrame): Feature dataset used to configure the transformer.

    Returns:
        Pipeline: Scikit-learn Pipeline combining feature transformation and model.
    """
    transformer = build_transformer(X)

    pipeline = Pipeline(
        steps=[
            ("preprocessor", transformer),
            ("model", model),
        ]
    )

    return pipeline
