# src/pipeline/data_transformation_pipeline.py

import sys
from src.config.load_config import LoadConfig
from src.components.data_transformation import DataTransformation
from src.utils.file_ops import load_json, save_json
from src.entity.artifacts_entity import DataIngestionArtifact, DataTransformationArtifact
from src.exception import AppException
from src.logger import logger
from dataclasses import asdict

class DataTransformationPipeline:
    def __init__(self):
        self.cfg = LoadConfig()
        self.transformation_config = self.cfg.get_data_transformation_config()

    def run(self) -> DataTransformationArtifact:
        try:
            logger.info("===== 🔄 [Step 3] Data Transformation Started =====")
            ingestion_dict = load_json("artifacts/data_ingestion/ingestion_artifact.json")
            ingestion_artifact = DataIngestionArtifact(**ingestion_dict)

            transformer = DataTransformation(self.transformation_config, ingestion_artifact.data_csv_file_path)
            transformation_artifact = transformer.initiate_data_transformation()

            save_json("artifacts/data_transformation/transformation_artifact.json", asdict(transformation_artifact))
            logger.info(f"✅ Data Transformation Completed. Output at: {transformation_artifact.transformed_csv_file_path}")

            return transformation_artifact
        except Exception as e:
            logger.error(f"❌ Data Transformation Pipeline Failed: {e}")
            raise AppException(e, sys)

def main():
    try:
        pipeline = DataTransformationPipeline()
        artifact = pipeline.run()
        logger.info(f"[main] Transformation Artifact: {artifact}")
    except Exception as e:
        raise AppException(e, sys)

if __name__ == "__main__":
    main()
