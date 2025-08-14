# src/pipeline/model_evaluation_pipeline.py

import sys
from src.config.load_config import LoadConfig
from src.components.model_evaluation import ModelEvaluation
from src.utils.file_ops import load_json, save_json
from src.entity.artifacts_entity import DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact
from src.exception import AppException
from src.logger import logger
from dataclasses import asdict
from src.utils.mlflow_ops import (
    setup_mlflow,
    start_mlflow_run,
    log_metrics
)


class ModelEvaluationPipeline:
    def __init__(self):
        self.cfg = LoadConfig()
        self.eval_config = self.cfg.get_model_evaluation_config()
        # Get MLflow config too (to get tracking URI and experiment name)
        self.trainer_config = self.cfg.get_model_trainer_config()


    def run(self) -> ModelEvaluationArtifact:
        try:
            logger.info("===== 🧪 [Step 5] Model Evaluation Started =====")

            # Load previous artifacts
            trans_artifact = DataTransformationArtifact(**load_json("artifacts/data_transformation/transformation_artifact.json"))
            trainer_artifact = ModelTrainerArtifact(**load_json("artifacts/model_trainer/model_artifact.json"))
            mlflow_meta = load_json("artifacts/model_trainer/mlflow_run.json")  # Contains run_id

            # Evaluate model
            evaluator = ModelEvaluation(self.eval_config, trans_artifact, trainer_artifact)
            eval_artifact = evaluator.initiate_evaluation()

            save_json("artifacts/model_evaluation/model_evaluation_artifact.json", asdict(eval_artifact))
            logger.info(f"✅ Model Evaluation Completed. Metrics saved at: {eval_artifact.evaluation_metrics_path}")

            # Setup MLflow from config
            setup_mlflow(
                tracking_uri=self.trainer_config.mlflow_tracking_uri,
                experiment_name=self.trainer_config.experiment_name
            )

            # Log evaluation metrics under same run_id
            metrics_dict = load_json(eval_artifact.evaluation_metrics_path)
            with start_mlflow_run(run_id=mlflow_meta["run_id"]):
                for split in ["train", "test", "oot"]:
                    split_metrics = metrics_dict.get(split, {})
                    log_metrics({f"{split}_{k}": v for k, v in split_metrics.items()})

                # Log PSI separately
                log_metrics({"psi": metrics_dict["psi"]})

            return eval_artifact
        except Exception as e:
            logger.error(f"❌ Model Evaluation Pipeline Failed: {e}")
            raise AppException(e, sys)

def main():
    try:
        pipeline = ModelEvaluationPipeline()
        artifact = pipeline.run()
        logger.info(f"[main] Model Evaluation Artifact: {artifact}")
    except Exception as e:        
        raise AppException(e, sys)

if __name__ == "__main__":
    main()