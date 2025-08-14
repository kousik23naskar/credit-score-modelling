# src/pipeline/model_trainer_pipeline.py

import sys
import mlflow
from pyprojroot import here
from src.config.load_config import LoadConfig
from src.components.model_trainer import ModelTrainer
from src.utils.file_ops import load_json, save_json
from src.entity.artifacts_entity import DataTransformationArtifact, ModelTrainerArtifact
from src.exception import AppException
from src.logger import logger
from dataclasses import asdict
from src.utils.mlflow_ops import setup_mlflow, start_mlflow_run, log_params, log_param, log_model_artifact


class ModelTrainerPipeline:
    def __init__(self):
        self.cfg = LoadConfig()
        self.trainer_config = self.cfg.get_model_trainer_config()

    def run(self) -> ModelTrainerArtifact:
        try:
            logger.info("===== 🤖 [Step 4] Model Training Started =====")
            trans_dict = load_json("artifacts/data_transformation/transformation_artifact.json")
            trans_artifact = DataTransformationArtifact(**trans_dict)

            trainer = ModelTrainer(self.trainer_config, trans_artifact)
            trainer_artifact = trainer.initiate_model_trainer()

            save_json("artifacts/model_trainer/model_artifact.json", asdict(trainer_artifact))
            logger.info(f"✅ Model Training Completed. Model saved at: {trainer_artifact.trained_model_path}")

            # Log with MLflow
            setup_mlflow(
                tracking_uri=self.trainer_config.mlflow_tracking_uri,
                experiment_name=self.trainer_config.experiment_name
            )

            with start_mlflow_run(run_name=self.trainer_config.run_name) as run:
                run_id = run.info.run_id  # Capture run_id for reuse
                log_params(self.trainer_config.estimator_params)
                log_params(self.trainer_config.scaling_method_params)
                log_param("scaling_method", self.trainer_config.scaling_method)
                log_model_artifact(trainer_artifact.trained_model_path)

                # Save run_id for reuse
                save_json("artifacts/model_trainer/mlflow_run.json", {"run_id": run_id})

            return trainer_artifact
        except Exception as e:
            logger.error(f"❌ Model Training Pipeline Failed: {e}")
            raise AppException(e, sys)

def main():
    try:
        pipeline = ModelTrainerPipeline()
        artifact = pipeline.run()
        logger.info(f"[main] Model Trainer Artifact: {artifact}")
    except Exception as e:
        raise AppException(e, sys)

if __name__ == "__main__":
    main()