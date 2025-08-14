# src/pipeline/model_pusher_pipeline.py

import sys
from src.config.load_config import LoadConfig
from src.components.model_pusher import ModelPusher
from src.utils.file_ops import load_json, save_json
from src.entity.artifacts_entity import ModelTrainerArtifact, ModelPusherArtifact
from src.exception import AppException
from src.logger import logger
from dataclasses import asdict

class ModelPusherPipeline:
    def __init__(self):
        self.cfg = LoadConfig()
        self.pusher_config = self.cfg.get_model_pusher_config()

    def run(self) -> ModelPusherArtifact:
        try:
            logger.info("===== 🚀 [Step 6] Model Pusher Started =====")
            trainer_art = ModelTrainerArtifact(**load_json("artifacts/model_trainer/model_artifact.json"))

            pusher = ModelPusher(self.pusher_config, trainer_art)
            pusher_artifact = pusher.initiate_model_pusher()

            #save_json("artifacts/model_pusher/model_pusher_artifact.json", asdict(pusher_artifact))
            save_json(f"{self.pusher_config.export_dir}/model_pusher_artifact.json", asdict(pusher_artifact))
            logger.info(f"✅ Model Pusher Completed. Model pushed to: {pusher_artifact.pushed_model_path}")

            return pusher_artifact
        except Exception as e:
            logger.error(f"❌ Model Pusher Pipeline Failed: {e}")
            raise AppException(e, sys)

def main():
    try:
        pipeline = ModelPusherPipeline()
        artifact = pipeline.run()
        logger.info(f"[main] Model Pusher Artifact: {artifact}")
    except Exception as e:
        raise AppException(e, sys)

if __name__ == "__main__":
    main()
