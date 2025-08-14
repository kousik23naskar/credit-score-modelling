import os
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s'
)

list_of_files = [
    ".github/workflows/.gitkeep",
    "data/.gitkeep",
    "config/config.yaml",
    "config/schema.yaml",
    "reports/figures/.gitkeep",
    "params.yaml",
    "dvc.yaml",
    "app.py",
    "main.py",
    "notebooks/EDA.ipynb",
    "notebooks/modelling_with_optbinning.ipynb",
    "Dockerfile",
    "requirements.txt",
    "setup.py",

    # All code directly inside src/
    "src/__init__.py",
    "src/components/__init__.py",
    "src/components/data_ingestion.py",
    "src/components/data_validation.py",
    "src/components/data_transformation.py",
    "src/components/model_trainer.py",
    "src/components/model_evaluation.py",
    "src/components/model_pusher.py",
    "src/components/model_prediction.py",
    "src/schema/__init__.py",
    "src/schema/prediction_schema.py",
    "src/config/__init__.py",
    "src/config/load_config.py",
    "src/entity/__init__.py",
    "src/entity/config_entity.py",
    "src/entity/artifacts_entity.py",
    "src/exception/__init__.py",
    "src/logger/__init__.py",
    "src/pipeline/__init__.py",
    "src/pipeline/data_ingestion_pipeline.py",
    "src/pipeline/data_validation_pipeline.py",
    "src/pipeline/data_transformation_pipeline.py",
    "src/pipeline/model_trainer_pipeline.py",
    "src/pipeline/model_evaluation_pipeline.py",
    "src/pipeline/model_pusher_pipeline.py",
    "src/pipeline/predict.py",
    "src/utils/__init__.py",
    "src/utils/file_ops.py",
    "src/utils/metrics.py",
    "src/utils/mlflow_ops.py",
    "src/utils/risk_level.py"
]

for filepath in list_of_files:
    filepath = Path(filepath)

    if filepath.parent != "":
        filepath.parent.mkdir(parents=True, exist_ok=True)
        logging.info(f"Creating directory: {filepath.parent} for the file {filepath.name}")

    if not filepath.exists() or filepath.stat().st_size == 0:
        with open(filepath, "w"):
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filepath} already exists")