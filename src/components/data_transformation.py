# src/components/data_transformation.py

import sys
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple
from sklearn.model_selection import train_test_split
from optbinning import BinningProcess
from src.exception import AppException
from src.logger import logger
from src.utils.file_ops import save_joblib
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifacts_entity import DataTransformationArtifact


class DataTransformation:
    """
    Handles data preprocessing:
    - Outlier capping
    - Train/Test/OOT split
    - OptBinning transformation
    """

    def __init__(self, config: DataTransformationConfig, input_csv: str):
        try:
            self.config = config
            self.input_path = Path(input_csv)
            self.output_dir = Path(self.config.transformed_data_dir)
            self.output_dir.mkdir(parents=True, exist_ok=True)

            self.binning_object_path = self.output_dir / self.config.binning_object_file
            self.transformed_csv_path = self.output_dir / self.config.transformed_data_file_name

            logger.info(f"✅ DataTransformation initialized. Input CSV: {self.input_path}")
        except Exception as e:
            raise AppException(e, sys)

    def cap_outliers(self, df: pd.DataFrame, lower=0.01, upper=0.99) -> pd.DataFrame:
        """
        Clip numeric columns at 1st and 99th percentiles to handle outliers.
        """
        try:
            for col in df.select_dtypes(include="number"):
                if col != self.config.target_column:
                    lo = df[col].quantile(lower)
                    hi = df[col].quantile(upper)
                    df[col] = np.clip(df[col], lo, hi)
            logger.info("📉 Outlier capping completed.")
            return df
        except Exception as e:
            raise AppException(e, sys)

    def split_data(self, df: pd.DataFrame) -> Tuple:
        """
        Splits data into Train/Test/OOT sets with stratification.
        """
        try:
            df_dev, df_oot = train_test_split(
                df,
                test_size=self.config.oot_size,
                stratify=df[self.config.target_column],
                random_state=self.config.random_state
            )

            X_dev = df_dev.drop(columns=self.config.target_column)
            y_dev = df_dev[self.config.target_column]

            X_oot = df_oot.drop(columns=self.config.target_column)
            y_oot = df_oot[self.config.target_column]

            X_train, X_test, y_train, y_test = train_test_split(
                X_dev,
                y_dev,
                test_size=self.config.test_size,
                stratify=y_dev,
                random_state=self.config.random_state
            )

            # Save splits as joblib
            save_joblib(self.config.X_train_path, X_train)
            save_joblib(self.config.X_test_path, X_test)
            save_joblib(self.config.X_oot_path, X_oot)
            save_joblib(self.config.y_train_path, y_train)
            save_joblib(self.config.y_test_path, y_test)
            save_joblib(self.config.y_oot_path, y_oot)

            logger.info("🗂️ Train, test, and OOT sets saved.")
            return X_train, X_test, X_oot, y_train, y_test, y_oot
        except Exception as e:
            raise AppException(e, sys)

    def apply_binning(self, X_train: pd.DataFrame, y_train: pd.Series) -> BinningProcess:
        """
        Fits an OptBinning process on the training data.
        """
        try:
            cat_cols = X_train.select_dtypes(include="object").columns.tolist()
            binning_process = BinningProcess(
                variable_names=X_train.columns.tolist(),
                categorical_variables=cat_cols
            )
            binning_process.fit(X_train, y_train)
            logger.info("📊 Binning process fitted.")
            return binning_process
        except Exception as e:
            raise AppException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Complete orchestration of the data transformation step.
        """
        try:
            df = pd.read_csv(self.input_path)
            logger.info(f"📥 Raw data loaded from {self.input_path}")

            df = self.cap_outliers(df)

            # Save transformed dataframe as CSV
            df.to_csv(self.transformed_csv_path, index=False)
            logger.info(f"Transformed CSV saved at: {self.transformed_csv_path}")
            
            X_train, X_test, X_oot, y_train, y_test, y_oot = self.split_data(df)
            bp = self.apply_binning(X_train, y_train)
            
            # Save binning object using joblib utility
            save_joblib(self.binning_object_path, bp)
            logger.info(f"Binning object saved to {self.binning_object_path}")

            return DataTransformationArtifact(
                transformed_csv_file_path=str(self.transformed_csv_path),
                binning_object_path=str(self.binning_object_path),
                X_train_path=self.config.X_train_path,
                X_test_path=self.config.X_test_path,
                X_oot_path=self.config.X_oot_path,
                y_train_path=self.config.y_train_path,
                y_test_path=self.config.y_test_path,
                y_oot_path=self.config.y_oot_path
            )
        except Exception as e:
            logger.error(f"❌ Exception in data transformation: {e}")
            raise AppException(e, sys)