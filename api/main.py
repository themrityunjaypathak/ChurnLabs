import time
import logging
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings
from api.schema import (
    CustomerRequest,
    Message,
    Health,
    Info,
    PredictionResponse,
    PredictionLabel,
)
from api.utils import load_model, load_threshold, load_metrics
from churnlabs.core.logger import setup_logging


setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.model = load_model()
        app.state.metrics = load_metrics()
        app.state.threshold = load_threshold()
        logger.info(
            "API initialized | model_version=%s | threshold=%.4f",
            app.state.metrics.get("model_version", "unknown"),
            app.state.threshold,
        )
    except Exception:
        logger.exception("Failed to initialize application state")
        app.state.model = None
        app.state.threshold = None
        app.state.metrics = None

    yield


app = FastAPI(
    title="ChurnLabs : Customer Churn Prediction API",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins or ["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/", tags=["General"], status_code=200, response_model=Message)
def root() -> Message:
    return Message(message="Customer Churn Prediction API is running")


@app.get("/health", tags=["Utility"], status_code=200, response_model=Health)
def health(request: Request) -> Health:
    model_loaded = request.app.state.model is not None
    threshold_loaded = request.app.state.threshold is not None
    metrics_loaded = request.app.state.metrics is not None

    return Health(
        status="ok"
        if all([model_loaded, threshold_loaded, metrics_loaded])
        else "error",
        model_loaded=model_loaded,
        metrics_loaded=metrics_loaded,
        threshold_loaded=threshold_loaded,
    )


@app.get("/info", tags=["Utility"], status_code=200, response_model=Info)
def model_info(request: Request) -> Info:
    metadata = request.app.state.metrics

    if metadata is None:
        raise HTTPException(
            status_code=500,
            detail="Training metadata not available",
        )

    test_set = metadata.get("test_set", {})

    return Info(
        model_version=metadata.get("model_version", "unknown"),
        trained_at=metadata.get("trained_at", "unknown"),
        threshold=metadata.get("threshold", 0.5),
        test_accuracy=test_set.get("accuracy", 0),
        test_precision=test_set.get("precision", 0.0),
        test_recall=test_set.get("recall", 0.0),
        test_f1=test_set.get("f1", 0.0),
        test_roc_auc=test_set.get("roc_auc", 0.0),
        test_pr_auc=test_set.get("pr_auc", 0.0),
    )


@app.post(
    "/predict",
    tags=["Prediction"],
    status_code=200,
    response_model=PredictionResponse,
)
def predict_customer_churn(
    customer: CustomerRequest, request: Request
) -> PredictionResponse:
    model = request.app.state.model
    threshold = request.app.state.threshold

    if model is None or threshold is None:
        logger.error("Model or threshold not loaded")
        raise HTTPException(status_code=500, detail="Model or threshold not available")

    try:
        data = pd.DataFrame([customer.model_dump()])
        if data.isnull().any().any():
            raise HTTPException(status_code=400, detail="Invalid input data")

        start = time.perf_counter()
        proba = float(model.predict_proba(data)[:, 1][0])
        end = time.perf_counter()
        logger.info("Inference time: %.4f sec", end - start)

        prediction = int(proba >= threshold)
        logger.info(
            "Prediction generated successfully | probability=%.4f | threshold=%.4f | prediction=%d",
            proba,
            threshold,
            prediction,
        )

        return PredictionResponse(
            churn_probability=round(float(proba), 4),
            prediction=prediction,
            label=PredictionLabel.churn
            if prediction == 1
            else PredictionLabel.not_churn,
            threshold_used=threshold,
        )

    except Exception:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail="Prediction failed")
