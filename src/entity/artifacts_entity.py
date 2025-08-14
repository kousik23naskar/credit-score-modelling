# src/entity/artifacts_entity.py
from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    data_csv_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    validation_report_file_path: str

@dataclass
class DataTransformationArtifact:
    transformed_csv_file_path: str
    binning_object_path: str
    X_train_path: str
    X_test_path: str
    X_oot_path: str
    y_train_path: str
    y_test_path: str
    y_oot_path: str


@dataclass
class ModelTrainerArtifact:
    trained_model_path: str
    # roc_auc: float = None
    # gini: float = None
    # pr_auc: float = None
    # ks: float = None
    # brier: float = None

@dataclass
class ModelEvaluationArtifact:
    evaluation_metrics_path: str


@dataclass
class ModelPusherArtifact:
    pushed_model_path: str