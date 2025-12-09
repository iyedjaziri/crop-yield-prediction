from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(title="Agritech Answers API")

# Load Model and Data
# Load Model and Data
# Determine base path (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "merged_data.csv")

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
    
    # Crop Prices (Market Simulation) - $/ton
    CROP_PRICES = {
        "Maize": 500,          # Cereal (High demand)
        "Rice, paddy": 600,    # Cereal (High value)
        "Wheat": 450,          # Cereal
        "Potatoes": 150,       # Tuber (High yield, lower price)
        "Sweet potatoes": 140, # Tuber
        "Cassava": 120,        # Root
        "Yams": 130,           # Root
        "Sorghum": 400,        # Cereal
        "Soybeans": 550,       # Legume
        "Plantains and others": 160 # Fruit/Veg
    }

    # Iterate through all unique crops
    for crop in unique_crops:
        # Create input for this crop
        crop_input = input_data.model_dump() # Use model_dump for Pydantic v2
        crop_input['Item'] = crop
        input_df = pd.DataFrame([crop_input])
        
        try:
            predicted_yield = model.predict(input_df)[0]
            
            # Calculate Profitability Proxy
            # Profit = (Yield * Specific_Price) - (Pesticides * Cost)
            price = CROP_PRICES.get(crop, 200) # Default 200 if unknown
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
