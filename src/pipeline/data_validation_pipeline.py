# src/pipeline/data_validation_pipeline.py

import sys
from src.config.load_config import LoadConfig
from src.components.data_validation import DataValidation
from src.utils.file_ops import load_json, save_json
from src.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact
from src.exception import AppException
from src.logger import logger
from dataclasses import asdict

class DataValidationPipeline:
    def __init__(self):
        self.cfg = LoadConfig()
        self.validation_config = self.cfg.get_data_validation_config()

    def run(self) -> DataValidationArtifact:
        try:
            logger.info("===== 📋 [Step 2] Data Validation Started =====")
            ingestion_dict = load_json("artifacts/data_ingestion/ingestion_artifact.json")
            ingestion_artifact = DataIngestionArtifact(**ingestion_dict)

            validator = DataValidation(ingestion_artifact, self.validation_config)
            validation_artifact = validator.validate_data_file()

            if not validation_artifact.validation_status:
                logger.warning("❌ Validation failed. Halting pipeline.")
                raise ValueError("Data validation failed due to schema issues.")
            
            save_json("artifacts/data_validation/validation_artifact.json", asdict(validation_artifact))
            logger.info(f"✅ Data Validation Completed. Report saved at: {validation_artifact.validation_report_file_path}")

            return validation_artifact
        except Exception as e:
            logger.error(f"❌ Data Validation Pipeline Failed: {e}")
            raise AppException(e, sys)

def main():
    try:
        pipeline = DataValidationPipeline()
        artifact = pipeline.run()
        logger.info(f"[main] Validation Artifact: {artifact}")
    except Exception as e:
        raise AppException(e, sys)

if __name__ == "__main__":
    main()
