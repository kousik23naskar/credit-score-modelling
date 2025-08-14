# src/components/model_prediction.py

import sys
import pandas as pd
from src.logger import logger
from src.exception import AppException
from src.utils.file_ops import load_joblib
from src.entity.artifacts_entity import DataTransformationArtifact, ModelPusherArtifact


class ModelPrediction:
    def __init__(
        self,
        model_artifact: ModelPusherArtifact,
        trans_artifact: DataTransformationArtifact = None  # Optional for CLI sampling
    ):
        self.model_artifact = model_artifact
        self.trans_artifact = trans_artifact

    def initiate_model_prediction(self, input_df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Load model
            model = load_joblib(self.model_artifact.pushed_model_path)
            logger.info(f"✅ Model loaded from: {self.model_artifact.pushed_model_path}")

            # Predict probability of default
            default_proba = model.predict_proba(input_df)[:, 1]
            logger.info("📉 Predicted default probabilities.")

            # Predict credit score
            credit_scores = model.score(input_df).round()
            logger.info("🧾 Predicted credit scores.")

            # Map credit score to levels and descriptions
            bins = [-float("inf"), 380, 450, 520, 590, 660, 730, 800, float("inf")]
            labels = [1, 2, 3, 4, 5, 6, 7, 8]
            descriptions = {
                1: "Very Poor", 2: "Poor", 3: "Average", 4: "Above Average",
                5: "Good", 6: "Very Good", 7: "Excellent", 8: "Exceptional"
            }

            credit_levels = pd.cut(credit_scores, bins=bins, labels=labels, include_lowest=True)
            level_descs = credit_levels.map(descriptions, na_action=None)

            print(f"🔍 Check for any NaNs: {credit_levels.isna().sum()}, {level_descs.isna().sum()}")

            logger.info("📦 Assembling prediction results")

            # Final output
            result = input_df.copy()
            result["credit_score"] = credit_scores
            result["credit_level"] = credit_levels
            result["credit_description"] = level_descs
            result["default_probability"] = default_proba

            logger.info("✅ Prediction completed successfully.")
            return result

        except Exception as e:
            logger.error(f"❌ Prediction failed: {e}")
            raise AppException(e, sys)