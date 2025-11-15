from fastapi.testclient import TestClient
from src.app import app
import pytest
import os

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Agritech Answers API"}

def test_predict_endpoint(client):
    # Only run if model exists, otherwise skip or mock
    if not os.path.exists("/home/lithium/P12/models/best_model.pkl"):
        pytest.skip("Model not found, skipping prediction test")
        
    payload = {
        "Area": "India",
        "Item": "Maize",
        "avg_rainfall_mm": 1000.0,
        "avg_temp_c": 25.0,
        "Pesticides_tonnes": 100.0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "predicted_yield" in response.json()
    assert isinstance(response.json()["predicted_yield"], float)

def test_recommend_endpoint(client):
    if not os.path.exists("/home/lithium/P12/models/best_model.pkl"):
        pytest.skip("Model not found, skipping recommendation test")

    payload = {
        "Area": "India",
        "avg_rainfall_mm": 1000.0,
        "avg_temp_c": 25.0,
        "Pesticides_tonnes": 100.0
    }
    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    assert "top_crops" in response.json()
    assert len(response.json()["top_crops"]) <= 3
