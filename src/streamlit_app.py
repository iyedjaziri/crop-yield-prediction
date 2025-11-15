import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Agritech Answers", layout="wide")

API_URL = "http://localhost:8000"

st.title("🌱 Agritech Answers: Yield Prediction & Recommendation")

# Sidebar for Inputs
st.sidebar.header("Input Parameters")

# Load Area list (hardcoded for demo or fetch from API if possible, but API might not be up yet)
# Ideally, we should fetch this from the backend, but for simplicity, we'll use a text input or a few common ones
area = st.sidebar.text_input("Area (Country)", "India")
rainfall = st.sidebar.number_input("Average Rainfall (mm)", min_value=0.0, value=1000.0)
temp = st.sidebar.number_input("Average Temperature (°C)", min_value=-10.0, max_value=60.0, value=25.0)
pesticides = st.sidebar.number_input("Pesticides Used (tonnes)", min_value=0.0, value=100.0)

tab1, tab2 = st.tabs(["🔮 Predict Yield", "💡 Recommend Crops"])

with tab1:
    st.header("Predict Crop Yield")
    crop = st.text_input("Crop Name", "Maize")
    
    if st.button("Predict Yield"):
        payload = {
            "Area": area,
            "Item": crop,
            "avg_rainfall_mm": rainfall,
            "avg_temp_c": temp,
            "Pesticides_tonnes": pesticides
        }
        
        try:
            response = requests.post(f"{API_URL}/predict", json=payload)
            if response.status_code == 200:
                result = response.json()
                st.success(f"Predicted Yield: **{result['predicted_yield']:.2f} hg/ha**")
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")

with tab2:
    st.header("Recommend Most Profitable Crops")
    
    if st.button("Get Recommendations"):
        payload = {
            "Area": area,
            "avg_rainfall_mm": rainfall,
            "avg_temp_c": temp,
            "Pesticides_tonnes": pesticides
        }
        
        try:
            response = requests.post(f"{API_URL}/recommend", json=payload)
            if response.status_code == 200:
                result = response.json()
                top_crops = result['top_crops']
                
                for i, rec in enumerate(top_crops, 1):
                    st.subheader(f"{i}. {rec['crop']}")
                    st.write(f"Predicted Yield: {rec['predicted_yield']:.2f} hg/ha")
                    st.write(f"Estimated Profitability: ${rec['profitability']:.2f}")
                    st.markdown("---")
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")
