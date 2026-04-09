import numpy as np
import pandas as pd
from typing import Optional
from sklearn.model_selection import cross_validate, cross_val_predict, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    make_scorer,
    precision_score,
    recall_score,
    accuracy_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
)


def evaluate_model_cv(
    pipeline: Pipeline,
    X: pd.DataFrame,
    y: pd.Series,
    cv=None,
    scoring: Optional[dict[str, object]] = None,
) -> dict[str, float]:
    """
    Perform cross-validation on a pipeline and return mean and standard deviation
    of evaluation metrics.

    Args:
        pipeline (Pipeline): Scikit-learn Pipeline containing preprocessing and model.
        X (pd.DataFrame): Feature matrix.
        y (pd.Series): Target vector.
        cv: Cross-validation strategy or number of folds.
            If None, defaults to StratifiedKFold with 5 splits.
        scoring (dict[str, object] | None): Dictionary of scoring metrics.
            If None, default classification metrics are used:
            accuracy, precision, recall, f1, roc_auc, pr_auc.

    Returns:
        dict[str, float]: Dictionary containing mean and standard deviation
        of each evaluation metric across folds.
    """
    if scoring is None:
        scoring = {
            "accuracy": "accuracy",
            "precision": make_scorer(precision_score, zero_division=0),
            "recall": make_scorer(recall_score, zero_division=0),
            "f1": "f1",
            "roc_auc": "roc_auc",
            "pr_auc": "average_precision",
        }

    if cv is None:
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    scores = cross_validate(
        pipeline,
        X,
        y,
        cv=cv,
        scoring=scoring,
        return_train_score=False,
        n_jobs=-1,
    )

    results = {}

    for metric, values in scores.items():
        if metric.startswith("test_"):
            metric_name = metric.replace("test_", "")
            results[f"{metric_name}_mean"] = np.mean(values)
            results[f"{metric_name}_std"] = np.std(values)

    return results


def evaluate_model_cv_with_threshold(
    pipeline: Pipeline,
    X: pd.DataFrame,
    y: pd.Series,
    cv=None,
    threshold: float = 0.5,
) -> dict[str, float]:
    """
    Perform cross-validation using out-of-fold predicted probabilities
    and evaluate metrics using a specified decision threshold.

    Steps:
        1. Generate out-of-fold predicted probabilities using cross-validation
        2. Apply the specified probability threshold to obtain class predictions
        3. Compute evaluation metrics

    Args:
        pipeline (Pipeline): Model pipeline.
        X (pd.DataFrame): Feature matrix.
        y (pd.Series): Target vector.
        cv: Cross-validation strategy.
            If None, defaults to StratifiedKFold with 5 splits.
        threshold (float): Probability cutoff for converting probabilities to class labels.

    Returns:
        dict[str, float]: Dictionary containing evaluation metrics
        computed on out-of-fold predictions.
    """
    if cv is None:
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    y_proba_cv = cross_val_predict(
        pipeline,
        X,
        y,
        cv=cv,
        method="predict_proba",
        n_jobs=-1,
    )[:, 1]

    y_pred_cv = (y_proba_cv >= threshold).astype(int)

    results = {
        "accuracy": accuracy_score(y, y_pred_cv),
        "precision": precision_score(y, y_pred_cv, zero_division=0),
        "recall": recall_score(y, y_pred_cv, zero_division=0),
        "f1": f1_score(y, y_pred_cv, zero_division=0),
        "roc_auc": roc_auc_score(y, y_proba_cv),
        "pr_auc": average_precision_score(y, y_proba_cv),
    }

    return results


def evaluate_model(
    pipeline: Pipeline, X_test: pd.DataFrame, y_test: pd.Series, threshold: float = 0.5
) -> dict[str, float]:
    """
    Evaluate a trained pipeline on the test dataset.

    Steps:
        1. Generate predicted probabilities on the test set
        2. Apply the specified decision threshold to obtain class predictions
        3. Compute evaluation metrics

    Metrics:
        Accuracy
        Precision
        Recall
        F1 Score
        ROC AUC (threshold independent)
        PR AUC (threshold independent)

    Args:
        pipeline (Pipeline): Trained Scikit-learn Pipeline.
        X_test (pd.DataFrame): Test feature matrix.
        y_test (pd.Series): Test target vector.
        threshold (float): Probability cutoff for classification.

    Returns:
        dict[str, float]: Dictionary containing evaluation metrics
        computed on the test set.
    """
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= threshold).astype(int)

    results = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "pr_auc": average_precision_score(y_test, y_proba),
    }

    return results
