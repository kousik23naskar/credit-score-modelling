# src/config/load_config.py

from pyprojroot import here
from src.utils.file_ops import read_yaml
from src.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig,
    ModelPusherConfig
)


class LoadConfig:
    def __init__(self, config_file: str = "config/config.yaml"):
        config_path = here() / config_file
        self.config = read_yaml(config_path)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        di = self.config["data_ingestion"]
        return DataIngestionConfig(
            kaggle_dataset=di["kaggle_dataset"],
            raw_data_dir=di["raw_data_dir"],
            downloaded_data_dir=di["downloaded_data_dir"],
            raw_data_file_name=di["raw_data_file_name"]
        )

    def get_data_validation_config(self) -> DataValidationConfig:
        validation_cfg = self.config["data_validation"]

        # Resolve schema path relative to project root
        schema_path = here() / validation_cfg["schema_file_path"]
        schema = read_yaml(schema_path)

        return DataValidationConfig(
            schema_file_path=schema_path,
            validation_artifact_dir=validation_cfg["validation_artifact_dir"],
            validation_report_file=validation_cfg["validation_report_file"],
            schema=schema
        )

    def get_data_transformation_config(self) -> DataTransformationConfig:
        dt = self.config["data_transformation"]

        # Get absolute path for transformed data directory
        trans_dir = here() / dt["transformed_data_dir"]

        return DataTransformationConfig(
            transformed_data_dir=str(trans_dir),
            transformed_data_file_name=dt["transformed_data_file_name"],
            binning_object_file=dt["binning_object_file"],
            target_column=dt["target_column"],
            test_size=dt["test_size"],
            oot_size=dt["oot_size"],
            random_state=dt["random_state"],
            X_train_path=str(trans_dir / dt["X_train_file"]),
            X_test_path=str(trans_dir / dt["X_test_file"]),
            X_oot_path=str(trans_dir / dt["X_oot_file"]),
            y_train_path=str(trans_dir / dt["y_train_file"]),
            y_test_path=str(trans_dir / dt["y_test_file"]),
            y_oot_path=str(trans_dir / dt["y_oot_file"]),
        )

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        mt = self.config["model_trainer"]
        params = read_yaml(here() / "params.yaml")
        trainer_params = params["model_trainer"]

        return ModelTrainerConfig(
            trained_model_dir=mt["trained_model_dir"],
            model_file_name=mt["model_file_name"],
            estimator_params=trainer_params["estimator_params"],
            scaling_method=trainer_params["scaling_method"],
            scaling_method_params=trainer_params["scaling_method_params"],
            mlflow_tracking_uri=mt["mlflow_tracking_uri"],
            experiment_name=mt["experiment_name"],
            run_name=mt["run_name"]
        )
    
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        me = self.config["model_evaluation"]
        return ModelEvaluationConfig(
            evaluation_artifact_dir=me["evaluation_artifact_dir"],
            metrics_file_name=me["metrics_file_name"]
        )

    def get_model_pusher_config(self) -> ModelPusherConfig:
        mp = self.config["model_pusher"]
        return ModelPusherConfig(
            export_dir=mp["export_dir"]
        )