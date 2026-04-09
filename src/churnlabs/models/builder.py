from sklearn.base import BaseEstimator
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from churnlabs.core.config import get_model_config


def build_model() -> BaseEstimator:
    """
    Build and return a machine learning model based on model-config.yaml.

    The model type and its parameters are defined in the configuration file.

    Returns:
        sklearn.base.BaseEstimator: Instantiated model object.

    Raises:
        KeyError: If required config keys are missing.
        ValueError: If the specified model type is not supported.
    """

    config = get_model_config()

    model_type = config["model"]["type"]
    params = config["model"]["params"]

    if model_type == "dummy_classifier":
        return DummyClassifier(**params)

    elif model_type == "logistic_regression":
        return LogisticRegression(**params)

    elif model_type == "random_forest":
        return RandomForestClassifier(**params)

    else:
        raise ValueError(f"Unsupported model type: {model_type}")
