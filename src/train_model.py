import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os

# Set MLflow tracking URI (local for now)
mlflow.set_tracking_uri("file:///home/lithium/P12/mlruns")
mlflow.set_experiment("Crop_Yield_Prediction")

def calculate_profitability(y_true, y_pred, pesticides):
    """
    Custom metric: Profitability Proxy.
    Assume Price per unit yield = 200
    Assume Cost per unit pesticide = 10
    Profit = (Yield * 200) - (Pesticides * 10)
    We want to see if our model predicts yield accurately enough to estimate profit.
    Actually, for a regression model, we just log the error. 
    But let's log the 'Predicted Total Profit' vs 'Actual Total Profit' difference as a metric.
    """
    price = 200
    cost = 10
    actual_profit = (y_true * price) - (pesticides * cost)
    pred_profit = (y_pred * price) - (pesticides * cost)
    return np.mean(np.abs(actual_profit - pred_profit))

def train_model():
    # 1. Load Data
    data_path = "/home/lithium/P12/data/processed/merged_data.csv"
    df = pd.read_csv(data_path)
    
    # Features & Target
    X = df.drop(columns=['Yield_hg_ha', 'Year']) # Year is likely not a predictive feature for future generalization unless time-series split
    y = df['Yield_hg_ha']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Preprocessing
    categorical_features = ['Area', 'Item']
    numerical_features = ['avg_rainfall_mm', 'avg_temp_c', 'Pesticides_tonnes']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])

    # --- Experiment 1: Ridge Regression (Baseline) ---
    with mlflow.start_run(run_name="Ridge_Baseline"):
        print("Running Experiment 1: Ridge Regression...")
        pipeline_ridge = Pipeline([
            ('preprocessor', preprocessor),
            ('regressor', Ridge())
        ])
        
        # Grid Search for Ridge
        param_grid_ridge = {'regressor__alpha': [0.1, 1.0, 10.0]}
        grid_ridge = GridSearchCV(pipeline_ridge, param_grid_ridge, cv=3, scoring='neg_mean_squared_error')
        grid_ridge.fit(X_train, y_train)
        
        best_ridge = grid_ridge.best_estimator_
        y_pred_ridge = best_ridge.predict(X_test)
        
        # Metrics
        rmse = np.sqrt(mean_squared_error(y_test, y_pred_ridge))
        mae = mean_absolute_error(y_test, y_pred_ridge)
        r2 = r2_score(y_test, y_pred_ridge)
        profit_error = calculate_profitability(y_test, y_pred_ridge, X_test['Pesticides_tonnes'])
        
        # Log
        mlflow.log_params(grid_ridge.best_params_)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("profitability_error", profit_error)
        mlflow.sklearn.log_model(best_ridge, "model")
        
        print(f"Ridge - RMSE: {rmse}, R2: {r2}")

    # --- Experiment 2: Random Forest (Challenger) ---
    with mlflow.start_run(run_name="RandomForest_Challenger"):
        print("Running Experiment 2: Random Forest...")
        pipeline_rf = Pipeline([
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor(random_state=42))
        ])
        
        # Randomized Search (faster than Grid for RF)
        # Keeping it small for demo speed
        param_grid_rf = {
            'regressor__n_estimators': [10, 20],
            'regressor__max_depth': [5, 10]
        }
        grid_rf = GridSearchCV(pipeline_rf, param_grid_rf, cv=2, scoring='neg_mean_squared_error')
        grid_rf.fit(X_train, y_train)
        
        best_rf = grid_rf.best_estimator_
        y_pred_rf = best_rf.predict(X_test)
        
        # Metrics
        rmse = np.sqrt(mean_squared_error(y_test, y_pred_rf))
        mae = mean_absolute_error(y_test, y_pred_rf)
        r2 = r2_score(y_test, y_pred_rf)
        profit_error = calculate_profitability(y_test, y_pred_rf, X_test['Pesticides_tonnes'])
        
        # Log
        mlflow.log_params(grid_rf.best_params_)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("profitability_error", profit_error)
        mlflow.sklearn.log_model(best_rf, "model")
        
        print(f"RandomForest - RMSE: {rmse}, R2: {r2}")
        
        # Save Best Model locally for App
        joblib.dump(best_rf, "/home/lithium/P12/models/best_model.pkl")
        print("Best model saved to models/best_model.pkl")

if __name__ == "__main__":
    os.makedirs("/home/lithium/P12/models", exist_ok=True)
    train_model()
