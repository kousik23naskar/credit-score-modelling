# src/entity/config_entity.py
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    kaggle_dataset: str
    raw_data_dir: str
    downloaded_data_dir: str
    raw_data_file_name: str

@dataclass
class DataValidationConfig:
    schema_file_path: str
    validation_artifact_dir: str
    validation_report_file: str
    schema: dict

@dataclass
class DataTransformationConfig:
    transformed_data_dir: str
    transformed_data_file_name: str
    binning_object_file: str
    target_column: str
    test_size: float
    oot_size: float
    random_state: int
    X_train_path: str
    X_test_path: str
    X_oot_path: str
    y_train_path: str
    y_test_path: str
    y_oot_path: str

@dataclass
class ModelTrainerConfig:
    trained_model_dir: str
    model_file_name: str
    estimator_params: dict
    scaling_method: str
    scaling_method_params: dict
    mlflow_tracking_uri: str
    experiment_name: str
    run_name: str

@dataclass
class ModelEvaluationConfig:
    evaluation_artifact_dir: str
    metrics_file_name: str

@dataclass
class ModelPusherConfig:
    export_dir: str
