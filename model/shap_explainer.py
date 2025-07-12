import shap
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

# Global storage for pre-computed SHAP explanations
shap_explanations = {}

def load_model_and_data():
    """
    Load the anomaly detection model and feature dataset.
    Returns:
        tuple: (model, X)
    """
    try:
        model = IsolationForest(contamination=0.1, random_state=42)
        data_path = '../data/features.csv'
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Feature file not found at {data_path}")
        X = pd.read_csv(data_path)
        return model, X
    except Exception as e:
        print(f"Error loading model or data: {e}")
        raise

# Initialize SHAP explainer
try:
    model, X = load_model_and_data()
    explainer = shap.Explainer(model, X)
except Exception as e:
    print(f"Failed to initialize SHAP explainer: {e}")
    explainer = None

def precompute_shap_for_anomalies(anomaly_indices):
    """
    Pre-compute SHAP explanations for anomaly indices.
    Args:
        anomaly_indices (list): List of indices where anomalies were detected
    """
    global shap_explanations
    if explainer is None:
        print("SHAP explainer not initialized")
        return
    shap_explanations = {i: explainer(X.iloc[[i]]) for i in anomaly_indices}

def get_shap_explanation_for_index(index, features_df):
    """
    Get SHAP explanation for a specific index.
    Args:
        index (int): Index of the data point
        features_df (pd.DataFrame): DataFrame containing features
    Returns:
        dict: SHAP values mapped to feature names
    """
    try:
        if explainer is None:
            return {"error": "SHAP explainer not initialized"}
        # Use pre-computed SHAP values if available
        if index in shap_explanations:
            shap_values = shap_explanations[index]
        else:
            sample = features_df.iloc[[index]]
            shap_values = explainer(sample)
        
        feature_names = features_df.columns
        values = shap_values.values[0]
        return {feature_names[i]: round(float(values[i]), 4) for i in range(len(feature_names))}
    except Exception as e:
        print(f"SHAP error for index {index}: {e}")
        return {"error": str(e)}