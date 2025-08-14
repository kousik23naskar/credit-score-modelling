# src/components/model_pusher.py

import sys
import shutil
from pathlib import Path
from src.exception import AppException
from src.logger import logger
from src.entity.config_entity import ModelPusherConfig
from src.entity.artifacts_entity import ModelTrainerArtifact, ModelPusherArtifact


class ModelPusher:
    """
    Pushes the trained model to the final export directory (e.g., for serving or deployment).
    """

    def __init__(self, cfg: ModelPusherConfig, trainer_artifact: ModelTrainerArtifact):
        self.cfg = cfg
        self.trainer_artifact = trainer_artifact
        logger.info("✅ ModelPusher initialized.")

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            src_path = Path(self.trainer_artifact.trained_model_path)
            dst_dir = Path(self.cfg.export_dir)
            dst_dir.mkdir(parents=True, exist_ok=True)

            dst_path = dst_dir / src_path.name
            shutil.copy(src_path, dst_path)

            logger.info(f"🚚 Model copied from {src_path} to {dst_path}")

            return ModelPusherArtifact(pushed_model_path=str(dst_path))
            
        except Exception as e:
            logger.error(f"❌ Model pusher failed: {e}")
            raise AppException(e, sys)