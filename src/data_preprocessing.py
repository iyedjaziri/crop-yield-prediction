import pandas as pd
import os

def load_and_merge_data():
    """
    Loads raw CSV files, cleans them, and merges them into a single dataset.
    """
    base_path = "/home/lithium/P12/Crop Yield Prediction Dataset"
    
    # Load Datasets
    print("Loading datasets...")
    yield_df = pd.read_csv(os.path.join(base_path, "yield.csv"))
    rain_df = pd.read_csv(os.path.join(base_path, "rainfall.csv"))
    temp_df = pd.read_csv(os.path.join(base_path, "temp.csv"))
    pest_df = pd.read_csv(os.path.join(base_path, "pesticides.csv"))

    # --- Cleaning & Renaming ---

    # 1. Yield Data
    # Keep: Area, Item, Year, Value (Yield)
    # Rename Value -> Yield_hg_ha
    yield_df = yield_df[['Area', 'Item', 'Year', 'Value']].rename(columns={'Value': 'Yield_hg_ha'})
    
    # 2. Rainfall Data
    # Rename ' Area' -> 'Area', ' average_rain_fall_mm_per_year' -> 'avg_rainfall_mm'
    # Check for leading spaces in column names
    rain_df.columns = [col.strip() for col in rain_df.columns]
    rain_df = rain_df.rename(columns={'average_rain_fall_mm_per_year': 'avg_rainfall_mm'})
    # Convert rainfall to numeric (handle errors if any non-numeric chars exist)
    rain_df['avg_rainfall_mm'] = pd.to_numeric(rain_df['avg_rainfall_mm'], errors='coerce')

    # 3. Temperature Data
    # Rename 'year' -> 'Year', 'country' -> 'Area', 'avg_temp' -> 'avg_temp_c'
    temp_df = temp_df.rename(columns={'year': 'Year', 'country': 'Area', 'avg_temp': 'avg_temp_c'})
    
    # 4. Pesticides Data
    # Keep: Area, Year, Value
    # Rename Value -> Pesticides_tonnes
    pest_df = pest_df[['Area', 'Year', 'Value']].rename(columns={'Value': 'Pesticides_tonnes'})

    # --- Merging ---
    print("Merging datasets...")
    
    # Merge Yield + Rainfall
    merged_df = pd.merge(yield_df, rain_df, on=['Area', 'Year'], how='inner')
    
    # Merge + Pesticides
    merged_df = pd.merge(merged_df, pest_df, on=['Area', 'Year'], how='inner')
    
    # Merge + Temperature
    merged_df = pd.merge(merged_df, temp_df, on=['Area', 'Year'], how='inner')
    
    # --- Final Cleaning ---
    # Drop NAs
    initial_len = len(merged_df)
    merged_df = merged_df.dropna()
    print(f"Dropped {initial_len - len(merged_df)} rows with missing values.")
    
    # Save
    output_path = "/home/lithium/P12/data/processed/merged_data.csv"
    merged_df.to_csv(output_path, index=False)
    print(f"Merged data saved to {output_path}")
    print(f"Final shape: {merged_df.shape}")
    return merged_df

if __name__ == "__main__":
    load_and_merge_data()
