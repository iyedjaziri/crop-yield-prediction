from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(title="Agritech Answers API")

# Load Model and Data
MODEL_PATH = "/home/lithium/P12/models/best_model.pkl"
DATA_PATH = "/home/lithium/P12/data/processed/merged_data.csv"

model = None
unique_crops = []

@app.on_event("startup")
def load_artifacts():
    global model, unique_crops
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        print("Warning: Model not found. Please train the model first.")
    
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        unique_crops = df['Item'].unique().tolist()
    else:
        print("Warning: Data not found.")

class PredictionInput(BaseModel):
    Area: str
    Item: str
    avg_rainfall_mm: float
    avg_temp_c: float
    Pesticides_tonnes: float

class RecommendationInput(BaseModel):
    Area: str
    avg_rainfall_mm: float
    avg_temp_c: float
    Pesticides_tonnes: float

@app.get("/")
def home():
    return {"message": "Welcome to Agritech Answers API"}

@app.post("/predict")
def predict_yield(input_data: PredictionInput):
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Create DataFrame for prediction
    input_df = pd.DataFrame([input_data.dict()])
    
    try:
        prediction = model.predict(input_df)[0]
        return {"predicted_yield": float(prediction)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend")
def recommend_crops(input_data: RecommendationInput):
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    recommendations = []
    
    # Iterate through all unique crops
    for crop in unique_crops:
        # Create input for this crop
        crop_input = input_data.dict()
        crop_input['Item'] = crop
        input_df = pd.DataFrame([crop_input])
        
        try:
            predicted_yield = model.predict(input_df)[0]
            
            # Calculate Profitability Proxy
            # Profit = (Yield * 200) - (Pesticides * 10)
            price = 200
            cost = 10
            profit = (predicted_yield * price) - (input_data.Pesticides_tonnes * cost)
            
            recommendations.append({
                "crop": crop,
                "predicted_yield": float(predicted_yield),
                "profitability": float(profit)
            })
        except Exception as e:
            continue
            
    # Sort by profitability
    recommendations.sort(key=lambda x: x['profitability'], reverse=True)
    
    return {"top_crops": recommendations[:3]}
