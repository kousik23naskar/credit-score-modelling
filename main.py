# main.py

from fastapi import FastAPI, HTTPException
import pandas as pd
from src.schema.prediction_schema import CreditData

from src.config.load_config import LoadConfig
from src.entity.artifacts_entity import ModelPusherArtifact
from src.components.model_prediction import ModelPrediction
from src.logger import logger
from src.utils.file_ops import load_json
from src.utils.risk_level import get_risk_level 

app = FastAPI(title="Credit Risk Prediction API")

# === Load configuration ===
cfg = LoadConfig()

# === Load saved artifacts ===
pusher_dict = load_json(f"{cfg.get_model_pusher_config().export_dir}/model_pusher_artifact.json")

pusher_artifact = ModelPusherArtifact(**pusher_dict)

# === Initialize model predictor ===
predictor = ModelPrediction(pusher_artifact)   # no trans_artifact


# === Prediction Endpoint ===
@app.post("/predict/")
def predict_credit_risk(data: CreditData):
    try:
        # ✅ Log incoming request
        logger.info(f"Input data received: {data.model_dump_json()}")
        
        input_df = pd.DataFrame([data.model_dump()])
        prediction_df = predictor.initiate_model_prediction(input_df)

        default_prob = round(prediction_df["default_probability"].iloc[0], 4)
        credit_score = int(prediction_df["credit_score"].iloc[0])
        credit_level = int(prediction_df["credit_level"].iloc[0])
        description = prediction_df["credit_description"].iloc[0]

        logger.info(f"Prediction successful: Score={credit_score}, Probability={default_prob}")

        return {
            "credit_score": credit_score,
            "credit_level": credit_level,
            "credit_description": description,
            "default_probability": default_prob,
            "risk_level": get_risk_level(default_prob)
        }

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed. Please check the input or model.")
    
# Run command: uvicorn main:app --reload --port 8000