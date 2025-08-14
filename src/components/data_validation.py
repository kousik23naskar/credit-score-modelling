# src/components/data_validation.py

import sys
from pathlib import Path
import pandas as pd
from src.exception import AppException
from src.logger import logger
from src.entity.config_entity import DataValidationConfig
from src.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact

class DataValidation:
    """
    Validates dataset columns and types based on provided schema.
    Stores validation report in configured artifact directory.
    """

    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        """
        Initialize DataValidation with ingestion artifact and validation config.

        Args:
            data_ingestion_artifact (DataIngestionArtifact): Data ingestion output artifact.
            data_validation_config (DataValidationConfig): Configurations for validation.
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            logger.info("DataValidation initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing DataValidation: {e}")
            raise AppException(e, sys)

    def validate_data_file(self) -> DataValidationArtifact:
        """
        Check columns and types against schema, write validation report.

        Returns:
            DataValidationArtifact: Validation status and report path.
        """
        try:
            logger.info("Starting data validation.")

            data_path = self.data_ingestion_artifact.data_csv_file_path
            df = pd.read_csv(data_path)

            expected_schema = self.data_validation_config.schema["columns"]  # dict of col_name: dtype_str
            #target_column = self.data_validation_config.schema["target_column"]

            # Check columns presence
            missing_columns = [col for col in expected_schema if col not in df.columns]
            extra_columns = [col for col in df.columns if col not in expected_schema]

            type_mismatches = []

            for col, expected_type in expected_schema.items():
                if col in df.columns:
                    actual_dtype = str(df[col].dtype)
                    # Simple check: expected type is a string like 'int', 'float', 'object'
                    # Map pandas dtype to simple string for comparison
                    if expected_type == "int" and not pd.api.types.is_integer_dtype(df[col]):
                        type_mismatches.append((col, expected_type, actual_dtype))
                    elif expected_type == "float" and not pd.api.types.is_float_dtype(df[col]):
                        type_mismatches.append((col, expected_type, actual_dtype))
                    elif expected_type == "object" and not pd.api.types.is_object_dtype(df[col]):
                        type_mismatches.append((col, expected_type, actual_dtype))

            validation_status = True
            report_lines = [] # Create validation report string

            if missing_columns:
                validation_status = False
                report_lines.append(f"Missing columns: {missing_columns}")
            if extra_columns:
                report_lines.append(f"Extra columns (unexpected): {extra_columns}")
            if type_mismatches:
                validation_status = False
                for col, expected, actual in type_mismatches:
                    report_lines.append(f"Type mismatch for column '{col}': expected {expected}, found {actual}")

            if validation_status:
                report_lines.append("Data validation PASSED.")
            else:
                report_lines.insert(0, "Data validation FAILED.")

            # Write report to file using config
            validation_dir = Path(self.data_validation_config.validation_artifact_dir)
            validation_dir.mkdir(parents=True, exist_ok=True)

            validation_report_path = validation_dir / self.data_validation_config.validation_report_file #validation_report_file: "validation.txt"

            with open(validation_report_path, "w") as file:
                file.write("\n".join(report_lines))

            logger.info(f"Validation report saved to: {validation_report_path}")
            logger.info(f"Validation status: {validation_status}")

            return DataValidationArtifact(
                validation_status=validation_status,
                validation_report_file_path=validation_report_path
            )

        except Exception as e:
            logger.error(f"Exception during data validation: {e}")
            raise AppException(e, sys)