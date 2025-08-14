# src/pipeline/predict.py

import sys
import pandas as pd
from src.config.load_config import LoadConfig
from src.utils.file_ops import load_json, load_joblib
from src.entity.artifacts_entity import ModelPusherArtifact, DataTransformationArtifact
from src.components.model_prediction import ModelPrediction
from src.logger import logger
from src.exception import AppException


class PredictPipeline:
    def __init__(self):
        self.cfg = LoadConfig()        
        self.pusher_artifact_path = "artifacts/model_trainer/model_artifact.json"
        self.trans_artifact_path = "artifacts/data_transformation/transformation_artifact.json"

    def run(self) -> pd.DataFrame:
        try:
            logger.info("===== 🧠  [Step 7] Starting Model Prediction =====")

            # Load artifacts
            pusher_dict = load_json(self.pusher_artifact_path)
            trans_dict = load_json(self.trans_artifact_path)            
            
            pusher_artifact = ModelPusherArtifact(**pusher_dict)
            trans_artifact = DataTransformationArtifact(**trans_dict)

            predictor = ModelPrediction(pusher_artifact, trans_artifact)

            # Load sample input data for prediction
            X_test = load_joblib(trans_artifact.X_test_path)
            sample_input = X_test.sample(1)

            logger.info(f"📥 Sample Input Data:\n{sample_input.to_string(index=False)}")

            # Run prediction
            prediction_result = predictor.initiate_model_prediction(sample_input)

            #logger.info(f"📌 Prediction Output:\n{prediction_result.to_string(index=False)}")
            return prediction_result

        except Exception as e:
            logger.error(f"❌ Prediction Pipeline Failed: {e}")
            raise AppException(e, sys)


def main():
    try:
        pipeline = PredictPipeline()
        prediction_df = pipeline.run()
        logger.info(f"📊 Prediction completed successfully. Prediction Output:\n{prediction_df.to_string(index=False)}")
    except Exception as e:
        raise AppException(e, sys)


if __name__ == "__main__":
    main()