# utils/loader.py

import pandas as pd
import os
import streamlit as st

# Build path relative to this file's location so it works on any machine
_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_HERE)

@st.cache_data
def load():
    data_path = os.path.join(_PROJECT_ROOT, "data", "processed", "asrs_clean.parquet")
    
    try:
        # Load the parquet file
        df = pd.read_parquet(data_path)
        print(f"Data loaded successfully! Shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {data_path}")
        print("Please check if the file exists and the path is correct.")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Optional: You can also add a function to get basic info about the dataset
def get_data_info():
    """
    Get basic information about the loaded data
    """
    df = load()
    if df is not None:
        return {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict()
        }
    return None
