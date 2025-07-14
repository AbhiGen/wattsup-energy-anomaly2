import os
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
        # Use absolute path relative to project root
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'features.csv')
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Feature file not found at {data_path}")
        
        # Load data and handle non-numeric columns
        df = pd.read_csv(data_path)
        
        # Drop timestamp column if it exists (it's not useful for anomaly detection)
        if 'timestamp' in df.columns:
            df = df.drop('timestamp', axis=1)
        
        # Ensure all columns are numeric
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        X = df[numeric_columns]
        
        print(f"Loaded data with shape: {X.shape}")
        print(f"Features: {list(X.columns)}")
        
        # Fit the model with the data
        model.fit(X)
        return model, X
    except Exception as e:
        print(f"Error loading model or data: {e}")
        raise

# Initialize SHAP explainer - modified to work with IsolationForest
try:
    model, X = load_model_and_data()
    
    # For IsolationForest, we'll use a simpler approach since it's not directly compatible with SHAP
    # We'll use feature importance based on the decision function
    explainer = None
    print("Model and data loaded successfully. SHAP will use feature importance approximation.")
    
except Exception as e:
    print(f"Failed to initialize SHAP explainer: {e}")
    explainer = None
    model = None
    X = None

def get_shap_explanation_for_index(index):
    """
    Get SHAP explanation for a specific data point.
    For IsolationForest, we'll return feature importance approximation.
    """
    global explainer, model, X
    
    if model is None or X is None:
        return {"error": "Model not loaded"}
    
    try:
        if index >= len(X):
            return {"error": "Index out of range"}
        
        # Get the specific data point
        data_point = X.iloc[index:index+1]
        
        # For IsolationForest, we'll compute feature importance using a proxy method
        # Calculate the decision function for the point and neighbors
        decision_score = model.decision_function(data_point)[0]
        
        # Simple feature importance: how much each feature deviates from mean
        feature_importance = {}
        for col in X.columns:
            mean_val = X[col].mean()
            point_val = data_point[col].iloc[0]
            deviation = abs(point_val - mean_val) / (X[col].std() + 1e-6)
            feature_importance[col] = deviation
        
        # Normalize importance scores
        max_importance = max(feature_importance.values()) if feature_importance else 1
        normalized_importance = {k: v/max_importance for k, v in feature_importance.items()}
        
        return {
            "feature_importance": normalized_importance,
            "decision_score": decision_score,
            "data_point": data_point.to_dict('records')[0]
        }
        
    except Exception as e:
        return {"error": str(e)}

def precompute_shap_for_anomalies():
    """
    Precompute SHAP explanations for anomalous data points.
    For IsolationForest, we'll identify anomalies and compute feature importance.
    """
    global model, X, shap_explanations
    
    if model is None or X is None:
        return
    
    try:
        # Get anomaly predictions
        anomaly_predictions = model.predict(X)
        anomaly_indices = np.where(anomaly_predictions == -1)[0]
        
        print(f"Found {len(anomaly_indices)} anomalies. Computing explanations...")
        
        # Compute explanations for each anomaly
        for idx in anomaly_indices[:50]:  # Limit to first 50 anomalies
            explanation = get_shap_explanation_for_index(idx)
            if "error" not in explanation:
                shap_explanations[idx] = explanation
        
        print(f"Precomputed explanations for {len(shap_explanations)} anomalies")
        
    except Exception as e:
        print(f"Error precomputing SHAP explanations: {e}")