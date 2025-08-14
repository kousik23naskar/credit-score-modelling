# src/utils/mlflow_ops.py

import mlflow
from pyprojroot import here
from urllib.parse import urlparse
from pathlib import Path
from src.utils.file_ops import load_joblib


def setup_mlflow(tracking_uri: str, experiment_name: str):
    """
    Set up MLflow tracking URI and experiment name.
    """
    parsed_uri = urlparse(tracking_uri)
    if parsed_uri.scheme in ("http", "https"):
        mlflow.set_tracking_uri(tracking_uri)
    else:
        uri_path = here() / tracking_uri
        mlflow.set_tracking_uri(f"file://{uri_path}")

    mlflow.set_experiment(experiment_name)


def start_mlflow_run(run_name: str = None, run_id: str = None):
    """
    Start an MLflow run with either a given run_name or run_id.
    """
    if run_id:
        return mlflow.start_run(run_id=run_id)
    else:
        return mlflow.start_run(run_name=run_name)


def log_params(params: dict):
    for key, value in params.items():
        mlflow.log_param(key, value)


def log_param(key: str, value):
    if value is not None:
        mlflow.log_param(key, str(value))


def log_metrics(metrics: dict):
    for key, value in metrics.items():
        mlflow.log_metric(key, value)


def log_model_artifact(model_path: str, artifact_path: str = "model"):
    """
    Log a model artifact to MLflow. If remote MLflow, register the model.
    """
    tracking_uri = mlflow.get_tracking_uri()
    tracking_url_type_store = urlparse(tracking_uri).scheme

    # Load model from local path
    model = load_joblib(model_path)

    model_name = Path(model_path).stem

    if tracking_url_type_store in ("http", "https"):
        # Log model and register it
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path=artifact_path,
            registered_model_name=model_name
        )
    else:
        # Just log the raw file as artifact (local store)
        mlflow.log_artifact(model_path, artifact_path=artifact_path)