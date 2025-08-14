# src/pipeline/data_ingestion_pipeline.py

import sys
from src.config.load_config import LoadConfig
from src.components.data_ingestion import DataIngestion
from src.utils.file_ops import save_json
from src.exception import AppException
from src.logger import logger
from src.entity.artifacts_entity import DataIngestionArtifact
from dataclasses import asdict


class DataIngestionPipeline:
    def __init__(self):
        self.cfg = LoadConfig()
        self.config = self.cfg.get_data_ingestion_config()
        self.ingestion = DataIngestion(self.config)

    def run(self) -> DataIngestionArtifact:
        try:
            logger.info("===== 📥 [Step 1] Data Ingestion Started =====")
            ingestion_artifact: DataIngestionArtifact  = self.ingestion.download_data()
            save_json("artifacts/data_ingestion/ingestion_artifact.json", asdict(ingestion_artifact))
            logger.info(f"✅ Data Ingestion Completed. File saved at: {ingestion_artifact.data_csv_file_path}")
            return ingestion_artifact
        except Exception as e:
            logger.error(f"❌ Data Ingestion Pipeline Failed: {e}")
            raise AppException(e, sys)


def main():
    try:
        pipeline = DataIngestionPipeline()
        artifact = pipeline.run()
        logger.info(f"[main] Ingestion Artifact: {artifact}")
    except Exception as e:
        raise AppException(e, sys)


if __name__ == "__main__":
    main()