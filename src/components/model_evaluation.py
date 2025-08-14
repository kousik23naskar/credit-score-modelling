# src/components/model_evaluation.py

import sys
from pathlib import Path
from scipy.stats import ks_2samp
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
from src.exception import AppException
from src.logger import logger
from src.utils.file_ops import load_joblib, save_json
from src.utils.metrics import calculate_psi
from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artifacts_entity import DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact

class ModelEvaluation:
    """
    Evaluates model performance on Train, Test, and OOT datasets using several metrics.
    """

    def __init__(self, config: ModelEvaluationConfig, trans_artifact: DataTransformationArtifact,
                 trainer_artifact: ModelTrainerArtifact):
        try:
            self.eval_cfg = config
            self.trans_artifact = trans_artifact
            self.trainer_artifact = trainer_artifact
            logger.info("✅ ModelEvaluation initialized.")
        except Exception as e:
            raise AppException(e, sys)

    def evaluate(self, X, y, model, name="Model"):
        proba = model.predict_proba(X)[:, 1]
        auc = roc_auc_score(y, proba)
        pr_auc = average_precision_score(y, proba)
        gini = 2 * auc - 1
        ks = ks_2samp(proba[y == 1], proba[y == 0]).statistic
        brier = brier_score_loss(y, proba)

        logger.info(
            f"{name} — AUC: {auc:.3f}, GINI: {gini:.3f}, PR-AUC: {pr_auc:.3f}, KS: {ks:.3f}, Brier: {brier:.3f}"
        )

        return {"auc": auc, "gini": gini, "pr_auc": pr_auc, "ks": ks, "brier": brier, "proba": proba}

    def initiate_evaluation(self) -> ModelEvaluationArtifact:
        try:
            model = load_joblib(self.trainer_artifact.trained_model_path)
            X_train = load_joblib(self.trans_artifact.X_train_path)
            X_test = load_joblib(self.trans_artifact.X_test_path)
            X_oot = load_joblib(self.trans_artifact.X_oot_path)
            y_train = load_joblib(self.trans_artifact.y_train_path)
            y_test = load_joblib(self.trans_artifact.y_test_path)
            y_oot = load_joblib(self.trans_artifact.y_oot_path)

            logger.info("🔍 Running model evaluation...")

            metrics_train = self.evaluate(X_train, y_train, model, name="Train")
            metrics_test = self.evaluate(X_test, y_test, model, name="Test")
            metrics_oot = self.evaluate(X_oot, y_oot, model, name="OOT")

            psi = calculate_psi(metrics_train["proba"], metrics_oot["proba"])
            logger.info(f"PSI between train & OOT: {psi:.3f}")

            # Remove raw probabilities for JSON compatibility
            for metrics in (metrics_train, metrics_test, metrics_oot):
                metrics.pop("proba", None)

            final_metrics = {
                "train": metrics_train,
                "test": metrics_test,
                "oot": metrics_oot,
                "psi": psi
            }

            metrics_path = Path(self.eval_cfg.evaluation_artifact_dir) / self.eval_cfg.metrics_file_name
            metrics_path.parent.mkdir(parents=True, exist_ok=True)
            save_json(metrics_path, final_metrics)

            logger.info(f"✅ Evaluation metrics saved at: {metrics_path}")

            return ModelEvaluationArtifact(evaluation_metrics_path=str(metrics_path))

        except Exception as e:
            logger.error(f"❌ Model evaluation failed: {e}")
            raise AppException(e, sys)