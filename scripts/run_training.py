import os
import time
import logging
from dotenv import load_dotenv
from datetime import datetime, timezone

from churnlabs.core.logger import setup_logging
from churnlabs.data.loaders import load_processed_data
from churnlabs.features.split import split_data
from churnlabs.models.pipeline import build_pipeline
from churnlabs.models.encoder import target_encoder
from churnlabs.models.builder import build_model
from churnlabs.models.artifact import save_model, save_metrics
from churnlabs.models.evaluation import (
    evaluate_model_cv,
    evaluate_model_cv_with_threshold,
    evaluate_model,
)
from churnlabs.models.uploader import upload_artifacts
from churnlabs.core.config import (
    get_training_config,
    get_model_config,
    get_model_version,
)

load_dotenv()


def main():
    logger = logging.getLogger(__name__)

    training_config = get_training_config()
    random_state = training_config["training"]["random_state"]

    model_config = get_model_config()
    best_threshold = model_config["threshold"]["value"]

    start_time = time.perf_counter()
    logger.info("Training pipeline started")

    logger.info("Loading processed dataset")
    df = load_processed_data()
    logger.info("Dataset shape: %s", df.shape)

    logger.info("Using random_state: %s", random_state)

    logger.info("Splitting the data into training and testing set")
    X_train, X_test, y_train, y_test = split_data(df)

    logger.info(
        "Train shape: %s, Test shape: %s",
        X_train.shape,
        X_test.shape,
    )

    logger.info("Encoding target variable")
    y_train, y_test = target_encoder(y_train, y_test)

    logger.info("Building model from model-config.yaml")
    model = build_model()
    logger.info("Model built: %s", model.__class__.__name__)

    logger.info("Model parameters: %s", model.get_params())

    if not hasattr(model, "predict_proba"):
        raise ValueError("Selected model does not support probability predictions")

    logger.info("Building pipeline")
    pipe = build_pipeline(model, X_train)

    logger.info("Running cross-validation")
    cv_results = evaluate_model_cv(pipe, X_train, y_train)
    logger.info("Cross-validation results: %s", cv_results)

    logger.info("Using decision threshold: %.4f", best_threshold)

    logger.info("Running cross-validation with decision threshold")
    cv_threshold_results = evaluate_model_cv_with_threshold(
        pipeline=pipe,
        X=X_train,
        y=y_train,
        threshold=best_threshold,
    )
    logger.info(
        "Cross-validation results with decision threshold: %s", cv_threshold_results
    )

    logger.info("Fitting model on training data")
    pipe.fit(X_train, y_train)

    test_results = evaluate_model(pipe, X_test, y_test, threshold=best_threshold)
    logger.info("Test set results: %s", test_results)

    min_recall = training_config["training"]["min_recall"]

    if test_results["recall"] < min_recall:
        logger.error(
            "Recall %.4f below required threshold %.4f",
            test_results["recall"],
            min_recall,
        )
        raise ValueError("Model recall below business requirements")

    logger.info("Saving model and artifacts")

    save_model(pipe)

    metadata = {
        "model_version": get_model_version(),
        "trained_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "threshold": best_threshold,
        "n_features": X_train.shape[1],
        "n_train_samples": X_train.shape[0],
        "n_test_samples": X_test.shape[0],
        "features": list(X_train.columns),
        "cross_validation_default": cv_results,
        "cross_validation_with_decision_threshold": cv_threshold_results,
        "test_set": test_results,
    }
    save_metrics(metadata)

    end_time = time.perf_counter()
    elapsed = end_time - start_time
    logger.info("Training completed in %.2f seconds", elapsed)

    logger.info("Uploading artifacts to Hugging Face")
    upload_artifacts(token=os.getenv("HF_TOKEN"))

    return {
        "threshold": best_threshold,
        "cross_validation_default": cv_results,
        "cross_validation_with_decision_threshold": cv_threshold_results,
        "test_set": test_results,
    }


if __name__ == "__main__":
    setup_logging()
    main()
