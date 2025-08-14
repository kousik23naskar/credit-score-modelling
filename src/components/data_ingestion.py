# src/components/data_ingestion.py

import sys
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi
from src.exception import AppException
from src.logger import logger
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifacts_entity import DataIngestionArtifact


class DataIngestion:
    """
    Responsible for downloading raw data from Kaggle and saving it locally.
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            logger.info(f"🔧 DataIngestion initialized with config: {self.data_ingestion_config}")
        except Exception as e:
            logger.error(f"Error initializing DataIngestion: {e}")
            raise AppException(e, sys)

    def download_data(self) -> DataIngestionArtifact:
        """
        Download dataset from Kaggle and save it to the configured location.
        """
        try:
            logger.info("🌐 Authenticating with Kaggle API...")
            api = KaggleApi()
            api.authenticate()

            dataset_ref = self.data_ingestion_config.kaggle_dataset
            download_dir = Path(self.data_ingestion_config.downloaded_data_dir)
            download_dir.mkdir(parents=True, exist_ok=True)

            logger.info(f"📥 Downloading dataset: {dataset_ref}")
            api.dataset_download_files(dataset_ref, path=str(download_dir), unzip=True)
            logger.info(f"✅ Dataset {dataset_ref} downloaded and extracted to {download_dir}")

            raw_data_path = download_dir / self.data_ingestion_config.raw_data_file_name
            print(type(raw_data_path))

            if not raw_data_path.exists():
                raise FileNotFoundError(f"Expected raw data file not found at {raw_data_path}")

            logger.info(f"📄 Raw data file found at: {raw_data_path}")

            return DataIngestionArtifact(data_csv_file_path=raw_data_path)

        except Exception as e:
            logger.error(f"❌ Data ingestion failed: {e}")
            raise AppException(e, sys)