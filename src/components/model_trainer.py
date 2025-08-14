# src/components/model_trainer.py

import sys
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from optbinning import Scorecard
from src.exception import AppException
from src.logger import logger
from src.utils.file_ops import load_joblib, save_joblib
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifacts_entity import DataTransformationArtifact, ModelTrainerArtifact

class ModelTrainer:
    """
    Trains a Scorecard model using OptBinning and logs it with MLflow.
    """
    def __init__(self, cfg: ModelTrainerConfig, trans_artifact: DataTransformationArtifact):
        try:
            self.cfg = cfg
            self.trans_artifact = trans_artifact
            logger.info("✅ ModelTrainer initialized.")
        except Exception as e:
            raise AppException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            # Load train data and binning object
            X_train = load_joblib(self.trans_artifact.X_train_path)
            y_train = load_joblib(self.trans_artifact.y_train_path)
            binning_process = load_joblib(self.trans_artifact.binning_object_path)

            # Initialize Scorecard with unfitted estimator
            scorecard = Scorecard(
                binning_process=binning_process,
                estimator=LogisticRegression(**self.cfg.estimator_params),
                scaling_method=self.cfg.scaling_method,
                scaling_method_params=self.cfg.scaling_method_params,
                intercept_based=True
            )

            # Fit the scorecard
            scorecard.fit(X_train, y_train)
            logger.info("✅ Scorecard model trained.")

            # Save model artifact
            model_dir = Path(self.cfg.trained_model_dir)
            model_dir.mkdir(parents=True, exist_ok=True)
            model_path = model_dir / self.cfg.model_file_name
            save_joblib(model_path, scorecard)
            logger.info(f"💾 Model saved at: {model_path}")

            return ModelTrainerArtifact(trained_model_path=str(model_path))
            
        except Exception as e:
            logger.error(f"❌ Model training failed: {e}")
            raise AppException(e, sys)